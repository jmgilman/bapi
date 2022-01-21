from beancount.parser.grammar import ParserSyntaxError
from beancount.ops.balance import BalanceError

from app.models.core import BeanFileError


def test_from_errors():
    errors = []
    errors.append(
        ParserSyntaxError(
            source={"filename": "file.beancount", "lineno": 1234},
            message="syntax error, unexpected INDENT",
            entry=None,
        )
    )
    errors.append(
        BalanceError(
            source={"filename": "file.beancount", "lineno": 4321},
            message="Balance failed for 'Assets:Bank'",
            entry=None,
        )
    )

    bfe = BeanFileError.from_errors(errors)
    assert "ParserSyntaxError" in bfe
    assert len(bfe["ParserSyntaxError"]) == 1
    assert bfe["ParserSyntaxError"][0].filename == errors[0].source["filename"]
    assert bfe["ParserSyntaxError"][0].lineno == errors[0].source["lineno"]

    assert "BalanceError" in bfe
    assert len(bfe["BalanceError"]) == 1
    assert bfe["BalanceError"][0].filename == errors[1].source["filename"]
    assert bfe["BalanceError"][0].lineno == errors[1].source["lineno"]
