import enum
from dataclasses import dataclass

from app.core import search
from bdantic import models


class MutatePriority(str, enum.Enum):
    """An enum controlling the order in which filtering/searching occurs."""

    filter = "filter"
    search = "search"


@dataclass
class DirectivesMutator:
    """Mutates a list of directives via filtering/search.

    Attributes:
        filter_expr: The JMESPath filter expression.
        search_expr: The string to perform a full text search with.
        priority: Whether filtering or searching should be applied first.
    """

    filter_expr: str | None = None
    search_expr: str | None = None
    priority: MutatePriority | None = MutatePriority.filter

    def mutate(self, data: models.Directives) -> models.Directives:
        """Mutates the directives using the configured filter/search expression.

        Args:
            data: The directives to mutate.

        Returns:
            A mutated version of the directives.
        """
        if self.priority == MutatePriority.filter:
            return self.search(self.filter(data))
        else:
            return self.filter(self.search(data))

    def search(self, data: models.Directives) -> models.Directives:
        """Performs a full-text search using the configured search expression.

        Args:
            data: The directives to search against

        Returns:
            A mutated version of the directives.
        """
        if self.search_expr:
            return search.DirectiveSearcher(data).search(self.search_expr)
        else:
            return data

    def filter(self, data: models.Directives) -> models.Directives:
        """Performs a filter using the configured JMESPath filter expression.

        Args:
            data: The directives to filter

        Returns:
            A mutated version of the directives.
        """
        if self.filter_expr:
            result = data.filter(self.filter_expr)
            if result:
                return result
            else:
                return models.Directives(__root__=[])

        return data
