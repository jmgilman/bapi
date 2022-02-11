from beancount import loader
from bdantic import models


def main():
    bf = models.BeancountFile.parse(
        loader.load_file("testing/static.beancount")
    )

    with open("testing/file.json", "w") as f:
        f.write(bf.json(by_alias=True, exclude_none=True))

    with open("testing/realize.json", "w") as f:
        f.write(bf.realize().json())

    with open("testing/static.json", "w") as f:
        f.write(bf.entries.json())


if __name__ == "__main__":
    main()
