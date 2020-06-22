## Introduction

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html) convention with the format Major.Minor.Patch.

Sections include (in this order):

- Added (new features)
- Changed (changes to existing features)
- Fixed (fixed bugs)
- Deprecated (soon to be removed features)
- Removed (features now removed)

## [Unreleased]

### Added

- frewpy exceptions class for raising custom exceptions for error handling during development.
- `FrewModel.calculations` has been added, containing the methods: `total_pressures()`, `net_pressures()`, `net_total_pressures()`.
- `FrewModel.soil` has been added, containing the methods: `get_soil_pressures()`.
- `FrewModel.struts` has been added but does not currently have any methods associated with it.
- `FrewModel.water` has been added, containing the methods: `get_water_pressures()`.

### Changed

- frewpy models have been modularised for easier future development and contributions.
- testing infrastructure has been added so this can be done as contributions are happening.
- Readme has been updated to include proper instructions and information.

### Fixed

- Requirements have been broadened so the library can be installed into virtual environments with fewer errors coming up.

## [v0.0.0] - March 2020

### Added

- `analyse()` and `close()` methods within main model class.
- `FrewModel.wall` has been added, containing the methods: `get_num_nodes()`, `get_num_stages()`, `get_node_levels()`, `get_results()`, `get_wall_stiffness()`, `get_envelopes()`, and `plot_results()`.

[unreleased]: https://gitlab.arup.com/ait/frewpy/-/compare/v0.0.0...develop
[v0.0.0]: https://gitlab.arup.com/ait/frewpy/-/tree/v0.0.0
