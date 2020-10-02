# Changelog

All notable changes to this project will be documented in this file. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html) convention with the format Major.Minor.Patch.

Sections include (in this order):

- Added (new features)
- Changed (changes to existing features)
- Fixed (fixed bugs)
- Deprecated (soon to be removed features)
- Removed (features now removed)

## [Unreleased]

### Added

- Continuous Integration pipeline to check for linting issues.
- Bug and Discussion GitLab issue templates.
- Developer guide to help contributors with getting started and contributing towards the library.
- Added the MIT license.
- Project roadmap to help keep development on the right path.
- Examples showing use cases of the library including: getting stage information, looping through models, extracting results to excel, plotting results to PDF.
- Static typing throughout the library checked with `mypy`.
- Custom frewpy exceptions `FrewError` and `NodeError`. These are to be made more specific as work continues.
- `utils.py` has been added with the following new functions: `model_to_json()`, `check_json_path()`, `load_data()`, `clear_results()`, `get_titles()`, `get_file_history()`, `get_file_version()`, `get_frew_version()`, `get_stage_names()`, `get_num_design_cases()`, `get_design_case_names()`, and `check_results_present()`.
- Unit tests for all odules.
- `FrewModel.water` with the method `get_water_pressures()` has been added.
- `FrewModel.struts` has been added but does not currently have any methods associated with it.
- `FrewModel.wall.plot_results_html()` has been added to output a Bokeh plot to a .html file.
- `FrewModel.soil.get_materials()` and `FrewModel.soil.get_material_properties()` have been added.

### Changed

- Frewpy models have been modularised for easier future development and contributions.
- Readme has been updated to include proper instructions and information.
- Changed from `pywin32` to `comtypes` for COM interaction as their version numbers are easier to deal with and it is very lightweight.
- `FrewModel` now has the following attributes: `file_path`, `folder_path`, `wall`, `soil`, and `water`.
- Object `FrewModel` now has the following methods: `FrewModel.get()`, `FrewModel.analyse()`, and `FrewModel.save()`.
- `FrewModel.wall.get_num_nodes()` and `FrewModel.wall.get_num_stages()` have been moved to `utils.py`.
- `FrewModel.wall.plot_results()` has been renamed `FrewModel.wall.plot_results_pdf()`.

### Fixed

- Requirements have been broadened so the library can be installed into virtual environments with fewer errors coming up.
- When plotting results to PDF stage numbers now refer to the correct stage number; indexing from 0 like in Frew.

### Removed

- `FrewModel.close()` is no longer available. It is no longer necessary to close the model at the end of the script as any COM interface interaction is contained within the respective method (opened and closed within the state of the method).

## [v0.0.0] - March 2020

### Added

- `analyse()` and `close()` methods within main model class.
- `FrewModel.wall` has been added, containing the methods: `get_num_nodes()`, `get_num_stages()`, `get_node_levels()`, `get_results()`, `get_wall_stiffness()`, `get_envelopes()`, and `plot_results()`.

[unreleased]: https://gitlab.arup.com/ait/frewpy/-/compare/v0.0.0...develop
[v0.0.0]: https://gitlab.arup.com/ait/frewpy/-/tree/v0.0.0
