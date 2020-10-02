# frewpy

Frewpy is a python library aimed at making interaction with Oasys Frew simple,
quick and reliable. Parts of the library use the COM interface to interract
with Frew, but most of the library is simple JSON manipulation which allows
designs to be automated and will play a part in larger automation efforts down
the line. Frewpy requires at least Oasys Frew 19.4 Build 24 as this is the
first build that has JSON I/O functionality.

[Click here](https://frewpy.readthedocs.io/en/stable/) to read the
Documentation for Frewpy.

## Installation

The library is distributed using the
[Python Package Index](https://pypi.org/project/frewpy/). Therefore, users can
simply use `pip` to install `frewpy` using `pip install`. For more guidance,
see the [pip docs](https://pip.pypa.io/en/stable/quickstart/).

## Getting Started

Once you have successfully installed frewpy you'll need to import the
`FrewModel` object at the top of your script and define the file path to the
model you wish to manipulate. With these defined, you can instantiate the model
object.

```python
from frewpy import FrewModel
file_path = r'path/to/frew/json'
model = FrewModel(file_path)
```

With the model object instantiated, you now have access to all of the methods
and attributes within frewpy. If you wish to get the results or export the
results to excel, for example, type one of the following lines of code:

```python
wall_results = model.wall.get_results()

out_path = r'path/to/output/folder'
model.wall.results_to_excel(out_path)
```

> Note: if you try to return the results of a model without any results in, you
> will be asked to analyse the model first.

The `examples` directory held within the repository will provide you more
examples of how you may use `frewpy`. These examples, and the rest of the
available methods are also shown in the
[frewpy documentation](https://frewpy.readthedocs.io/en/stable/index.html).
Alternatively you can read the source code to understand what is possible with
the library.

## Support and contributing

If you are learning Python, contributing to open source projects is
[one of the best ways to learn to code](https://rubygarage.org/blog/how-contribute-to-open-source-projects).

If you have a project which requires something additional to what frewpy
currently offers, it could be beneficial for you to contribute towards frewpy
in line with carrying out the project work. Frewpy is built with a simple,
scalable structure and is easy to extend if it doesn't currently do what you
need it to do. **Don't be afraid to get in contact to see how you can
contribute**, and if you do extend the functionality please get in contact to
show us the cool stuff you've done!

If you require support when using frewpy, would like to get involved in the
project, or have any features or bugs please either log an issue on this
repository using the appropriate template, or contact one of the core
developers and we will do our best to respond.

> For a more detailed guide on contributing towards frewpy, visit the frewpy
> documentation Developer Guide.

## Authors and achnowledgement

All development has currently come from Fred White and Josh Wheeler. Guidance
has come from engineers in the Arup London Geotechnics team.

## Technologies

This platform was developed in a Windows environment with `python 3.7`. Using
other `python 3` versions is assumed possible but has not been tested and so
is not officially supported.

## License

Frewpy is licensed under the MIT License.
