# frewpy

A library to wrap the Oasys Frew COM interface with pythonic terms and object oriented programming. The aim of frewpy is to make the COM interface accessible to engineers using python. This allows designs to be automated and will play a part in larger automation efforts down the line. Frewpy requires Oasys Frew 19.4 Build 24 as this is the first build that has JSON input/output functionality.

[Click here](http://www.frewpy-docs.s3-website-eu-west-1.amazonaws.com/) to read the Documentation for Frewpy.

## Installation

This installation guide assumes you already have the correct version of Oasys Frew installed, with a version greater than Python 3.6 also installed. If you do not have Python set up on your computer, follow [this guide](https://gitlab.arup.com/ait/how-to-wiki/-/wikis/Python/Getting-Started) to do so.

To install frewpy into your chosen virtual environment, use one of the commands below. If you are not sure which command to go with, use the one marked _Default_.

If you'd like the latest unreleased features, you can install the development version. Note that features may not be covered by tests and strong checking. You'll require Git to be installed on your computer, if you haven't done so you can [download it here](https://gitforwindows.org/). If you have knowingly set up an SSH key for your laptop on your GitLab account, then use that command over the HTTPs one. If you haven't set up an SSH key, it is recommended you set up an ED25519 type SSH key by following [the Gitlab Docs on this topic](https://docs.gitlab.com/ee/ssh/).

If you receive an SSL error, contact the development team as this is a known issue for people pip installing any packages on Arup laptops and there is a work around provided by Arup IT. Alternatively you can follow [this Yammer discussion.](https://www.yammer.com/arup.com/threads/660618752778240)

| Type                                   | Command                                                                                |
| -------------------------------------- | -------------------------------------------------------------------------------------- |
| _(Default)_ Latest Stable Build v0.0.0 | `pip install https://gitlab.arup.com/ait/frewpy/-/archive/v0.0.0/frewpy-v0.0.0.tar.gz` |
| Development version (SSH)              | `pip install git+ssh://git@gitlab.arup.com/ait/frewpy.git@develop`                     |
| Development version (HTTPs)            | `pip install git+https://git@gitlab.arup.com/ait/frewpy.git@develop`                   |

## Getting Started

Once you have successfully installed frewpy you'll need to import the `FrewModel` object at the top of your script and define the file path to the model you wish to manipulate. With these defined, you can instantiate the model object.

```python
from frewpy import FrewModel
file_path = r'C:\Users\fred.white\Documents\windows-work\frewpy\models\SLS B4 South Basement.json'
model = FrewModel(file_path)
```

With the model object instantiated, you now have access to all of the methods and attributes within that Class. If you wish to get the results or export the results to excel, for example, type one of the following lines of code:

```python
wall_results = model.get_results()
model.results_to_excel()
```

> Currently if you try to return the results of a model without any results in, you will be asked to analyse the model first.

The `examples` directory held within the repository will provide you more examples of how you may use `frewpy`. You may also [visit the documentation](http://www.frewpy-docs.s3-website-eu-west-1.amazonaws.com/) or read the source code to understand what is possible with the library.

## Support and contributing

If you just want to learn to code in Python then help contribute, as described in [this article](https://rubygarage.org/blog/how-contribute-to-open-source-projects), contributing to open source projects is one of the best ways to learn to code.

If you have a project which requires something additional to what frewpy currently offers, it could be beneficial to collaborate and expand our offering using project funds. Frewpy is built with a structure like lego blocks and is easy to extend if it doesn't currently do what you need it to do. **Don't be afraid to get in contact to see how you can contribute**, and if you do extend the functionality please get in contact to show us the cool stuff you've done!

If you require support when using frewpy, would like to get involved in the project, or have any features or bugs please either log an issue on this repository using the appropriate template, or contact the development team and we will do our best to respond.

## Authors and achnowledgement

All development has currently come from Fred White in the Infrastructure London Group (ILG) Digital Team. Further extensions and guidance has been contributed by a core team of geotechnical engineers within London Geotechnics: Jack Taggart, Paul Bailie, Pishun Tantivangphaisal and Cameron Hughes.

## Technologies

This platform was developed in a Windows environment with `python 3.6`. Support for other `python 3` versions is assumed possible but has not been tested.

## License

This repository is private, and is currently under exclusive copyright by default. Refer [here](https://choosealicense.com/no-permission/) for more information. It is intended to open up the licence once a certain point in development has been reached.
