from src.svg_wheel import generate_svg_wheel
from src.utils import (
    get_packages,
    remove_irrelevant_packages,
    save_to_file,
)


def main(*args):
    packages = remove_irrelevant_packages(get_packages())
    save_to_file(packages)
    generate_svg_wheel(packages)
    print("Exiting...")


if __name__ == '__main__':
    main()
