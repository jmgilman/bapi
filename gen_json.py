from beancount import loader
from beancount.core import realization
from bdantic import models


def main():
    entries, _, _ = loader.load_file("testing/static.beancount")
    realize = realization.realize(entries)

    directives = models.Directives.parse(entries)
    real_acct = models.RealAccount.parse(realize)

    with open("testing/static.json", "w") as f:
        f.write(directives.json())

    with open("testing/realize.json", "w") as f:
        f.write(real_acct.json())


if __name__ == "__main__":
    main()
