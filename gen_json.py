from beancount import loader
from bdantic import models


def main():
    bf = models.BeancountFile.parse(
        loader.load_file("testing/static.beancount")
    )

    with open("testing/static.json", "w") as f:
        f.write(bf.entries.json())

    with open("testing/realize.json", "w") as f:
        f.write(bf.realize().json())


if __name__ == "__main__":
    main()
