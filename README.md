# frewpy

Frewpy is a python library aimed at making interaction with Oasys Frew simple, quick and reliable. Parts of the library use the COM interface to interract with Frew, but most of the library is simple JSON manipulation which allows designs to be automated and will play a part in larger automation efforts down the line. Frewpy requires Oasys Frew 19.4 Build 24 as this is the first build that has JSON input/output functionality.

[Click here](http://www.frewpy-docs.s3-website-eu-west-1.amazonaws.com/) to read the Documentation for Frewpy.

## Installation

This installation guide assumes you already have the correct version of Oasys Frew installed, with a version greater than Python 3.6 also installed. If you do not have Python set up on your PC, follow [this guide](https://gitlab.arup.com/ait/how-to-wiki/-/wikis/Python/Getting-Started) to do so.

To install frewpy into your chosen virtual environment, use one of the commands below. If you are not sure which command to go with, use the one marked _Default_.

If you'd like the latest unreleased features, you can install the development version. Note that features may not be covered by tests and strong checking. You'll require Git for Windows to be installed on your PC, if you haven't done so you can [download it here](https://gitforwindows.org/). If you have knowingly set up an SSH key for your PC on your GitLab account, then use that command over the HTTPs one. If you haven't set up an SSH key, it is recommended you set up an ED25519 type SSH key by following [the Gitlab Docs on this topic](https://docs.gitlab.com/ee/ssh/).

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

With the model object instantiated, you now have access to all of the methods and attributes within frewpy. If you wish to get the results or export the results to excel, for example, type one of the following lines of code:

```python
wall_results = model.wall.get_results()

out_path = r'C:\Users\fred.white\Desktop'
model.wall.results_to_excel(out_path)
```

> Note: if you try to return the results of a model without any results in, you will be asked to analyse the model first.

The `examples` directory held within the repository will provide you more examples of how you may use `frewpy`. These examples, and the rest of the available methods are also shown in the [documentation for frewpy](http://www.frewpy-docs.s3-website-eu-west-1.amazonaws.com/). Alternatively you can read the source code to understand what is possible with the library.

## Support and contributing

If you are learning Python, contributing to open source projects is [one of the best ways to learn to code](https://rubygarage.org/blog/how-contribute-to-open-source-projects).

If you have a project which requires something additional to what frewpy currently offers, it could be beneficial for you to contribute towards frewpy in line with carrying out the project work. Frewpy is built with a simple, scalable structure and is easy to extend if it doesn't currently do what you need it to do. **Don't be afraid to get in contact to see how you can contribute**, and if you do extend the functionality please get in contact to show us the cool stuff you've done!

If you require support when using frewpy, would like to get involved in the project, or have any features or bugs please either log an issue on this repository using the appropriate template, or contact the development team and we will do our best to respond.

> For a more detailed guide on contributing towards frewpy, visit the frewpy documentation Developer Guide.

## Authors and achnowledgement

All development has currently come from Fred White and Josh Wheeler in the Infrastructure London Group (ILG) Digital Team. Guidance has come from engineers in the London Geotechnics team including Joel Brook and Jack Taggart.

## Technologies

This platform was developed in a Windows environment with `python 3.6`. Support for other `python 3` versions is assumed possible but has not been tested.

## License

Frewpy is licensed under the MIT License.
