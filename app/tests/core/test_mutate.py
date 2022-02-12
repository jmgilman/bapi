from unittest import mock

from app.core import mutate


@mock.patch("app.core.search.DirectiveSearcher.search")
@mock.patch("bdantic.models.file.Directives")
def test_directives(directives, search):
    mut = mutate.DirectivesMutator()
    result = mut.mutate(directives)
    assert result == directives

    directives.filter.return_value = "test"
    mut = mutate.DirectivesMutator(filter_expr="[?ty == 'Open']")
    result = mut.mutate(directives)
    assert result == "test"
    directives.filter.assert_called_once_with("[?ty == 'Open']")

    search.return_value = "test"
    mut = mutate.DirectivesMutator(search_expr="Home Depot")
    result = mut.mutate(directives)
    assert result == "test"
    search.assert_called_once_with("Home Depot")
