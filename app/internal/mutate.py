from .search import DirectiveSearcher
from ..models import MutatePriority
from bdantic import models
from dataclasses import dataclass
from typing import Optional


@dataclass
class DirectivesMutator:
    """Mutates a list of directives via filtering/search.

    Attributes:
        filter_expr: The JMESPath filter expression.
        search_expr: The string to perform a full text search with.
        priority: Whether filtering or searching should be applied first.
    """

    filter_expr: Optional[str] = None
    search_expr: Optional[str] = None
    priority: Optional[MutatePriority] = MutatePriority.filter

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
            return DirectiveSearcher(data).search(self.search_expr)
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
