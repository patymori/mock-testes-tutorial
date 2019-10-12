import setuptools
import pathlib

readme_path = pathlib.Path("README.md")
with readme_path.open() as f:
    README = f.read()

setuptools.setup(
    name="my_project",
    version="0.1",
    author="Paty Morimoto",
    author_email="excermori@yahoo.com.br",
    description="",
    long_description=README,
    long_description_content_type="text/markdown",
    license="GNU General Public License v3.0",
    packages=setuptools.find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests"]
    ),
    include_package_data=True,
    python_requires=">=3.7",
    test_suite="tests",
    classifiers=[
        "Development Status :: 2 - Beta",
        "Environment :: Other Environment",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
    entry_points="""\
        [console_scripts]
            my_app=core.app:execute
    """,
)
