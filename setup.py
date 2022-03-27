from pathlib import Path
from setuptools import setup, find_packages

HERE = Path(__file__).parent
README = HERE / "README.md"

setup(
    name="ddcb",
    description="A terminal game inspired by the psone classic.",
    long_description=README.read_text(),

    packages=find_packages(where='src'),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "requests",
        "beautifulsoup4",
        "lxml",
    ],

    author="Taylor VanCoevering",
)
