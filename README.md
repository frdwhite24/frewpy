# frewpy

A library to wrap the Oasys Frew COM interface with pythonic terms and object oriented programming. The aim of frewpy is to make the COM interface accessible to engineers using python. This allows designs to be automated and will play a part in larger automation efforts down the line. Frewpy requires Oasys Frew 19.4 Build 24 as this is the first build that has JSON input/output functionality.

[Click here](http://www.frewpy-docs.s3-website-eu-west-1.amazonaws.com/) to read the Documentation for Frewpy.

## Installation

To install frewpy into your chosen virtual environment, use one of the commands below. If you are not sure which command to go with, use the one marked _default_.

If you'd like the latest unreleased features, you can install the development version. Note that features may not be covered by tests and strong checking. You'll require Git to be installed on your computer, if you haven't done so you can [download it here](https://gitforwindows.org/). If you have knowingly set up an SSH key for your laptop on your GitLab account, then use that command over the HTTPS one. If you haven't set up an SSH key, it is recommended you set up an ED25519 type SSH key by following [the Gitlab Docs on this topic](https://docs.gitlab.com/ee/ssh/).

If you receive an SSL error, contact the development team as this is a known issue for people pip installing any packages on Arup laptops and there is a work around provided by Arup IT. Alternatively you can follow [this Yammer discussion.](https://www.yammer.com/arup.com/threads/660618752778240)

| Type                                   | Command                                                                                |
| -------------------------------------- | -------------------------------------------------------------------------------------- |
| _(Default)_ Latest Stable Build v0.0.0 | `pip install https://gitlab.arup.com/ait/frewpy/-/archive/v0.0.0/frewpy-v0.0.0.tar.gz` |
| Development version (SSH)              | `pip install git+ssh://git@gitlab.arup.com/ait/frewpy.git@develop`                     |
| Development version (HTTPS)            | `pip install git+https://git@gitlab.arup.com/ait/frewpy.git@develop`                   |

## Getting Started

Once you have successfully installed frewpy you'll need to import the `FrewModel` object at the top of your script and define the file path to the model you wish to manipulate. With these defined, you can instantiate the model object.

```python
from frewpy import FrewModel
file_path = r'C:\Users\fred.white\Documents\windows-work\frewpy\models\SLS B4 South Basement.json'
model = FrewModel(file_path)
```

With the model object instantiated, you can then use frewpy however you want. The model object has a series of generic methods such as `model.analyse()` and `model.close()`, and is also split into 5 key areas. These key areas aim to organise the COM interface methods available to the user into common themes which should make navigating and finding what you want to do much easier. The key areas are:

- `model.wall`
- `model.struts`
- `model.soil`
- `model.water`
- `model.calculate`

If you need to get results from a model, you'll need to anaylse the model before using another method to get results. Lastly, you must close the COM interface connection once you have done whatever you need to do.

```python
model.analyse()
wall_results = model.wall.get_results()
model.close()
```

If you wish to see a working example based on these principles, open up `example.py` in the repository files.

## Support and contributing

If you require support when using frewpy, would like to get involved in the project, or have any features or bugs please either log an issue on this repository using the appropriate template, or contact the development team and we will do our best to respond. If you have a project which requires something additional to what frewpy currently offers, it could be beneficial to collaborate and expand our offering using project funds. We have a frewpy users MS Teams chat for the core users, and hopefully most discussion will take place on the repository using issues and the appropriate labels.

## Authors and achnowledgement

All development has currently come from Fred White in the Infrastructure London Group (ILG) Digital Team. Further extensions and guidance has been contributed by a core team of geotechnical engineers within London Geotechnics: Jack Taggart, Paul Bailie, Pishun Tantivangphaisal and Cameron Hughes.

## Technologies

This platform was developed in a Windows environment with `python 3.6`. The dependencies of the library are very limited and so support for other `python 3` versions is assumed possible.

## License

This repository is private, and is currently under exclusive copyright by default. Refer [here](https://choosealicense.com/no-permission/) for more information. It is intended to open up the licence once a certain point in development has been reached.
