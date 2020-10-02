from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as f:
    req = f.read()
dependencies = req.splitlines()

setup(
    name="frewpy",
    version="0.1.1",
    author="Fred White",
    description="A python wrapper for the Oasys Frew geotechnical software package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/frdwhite24/frewpy",
    packages=find_packages(),
    install_requires=dependencies,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows :: Windows 10",
    ],
    python_requires=">=3.7",
)
