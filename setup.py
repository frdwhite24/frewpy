from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as f:
    req = f.read()
dependencies = req.splitlines()

setup(
    name="frewpy",
    version="0.0.0",
    author="Fred White",
    author_email="fred.white@arup.com",
    description="A python wrapper for the Oasys Frew geotechnical software package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.arup.com/ait/frewpy",
    packages=setuptools.find_packages(),
    install_requires=dependencies,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Windows",
    ],
    python_requires=">=3.7",
)
