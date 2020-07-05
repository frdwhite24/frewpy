# Developer Guide

## Introduction

Firstly, thank you for considering contributing towards frewpy, it is greatly appreciated and will definitely benefit both the wider community and also your own technical development. Please take your time when reading this contribution guide as it will make the overall experience much easier, and explain why things the way they are. It will also make it much more straight forward for the core developers to coordinate all the contributions to keep the project on the right tracks. In return, the core developers should reciprocate the care when addressing your issue, assessing changes and helping you finalize your merge requests.

There are many ways to contribute, from submitting a feature request on the GitLab repository, to extending the core functionality of the library so that it comfortably enables engineers to do everything they require with Frew. This core functionality could be as simple as retrieving information from a Frew model, or as complex as enabling quicker design iterations or integration with other Oasys software. Other possible contributions could be providing examples of the library being used, and detailed reporting of any bugs to ensure it is a clean, reliable library for anyone to use.

Please don't submit issues for non-frewpy related problems. This is to ensure the issues are clear and helpful for the community to browse and for developers to use to progress the project. Feature requests where frewpy is suggested to be used to carry out the whole design process will be closed and asked to be broken down into smaller, feature-specific requests. The intention of frewpy is to enable engineers to carry out their design work as a tool in their arsenal, not simply output a finished detailed design (at the moment anyway!).

## Responsibilities

1. Follow the [basic programming principles](https://www.c-sharpcorner.com/article/software-design-principles-dry-kiss-yagni/) at all times (in particular: Don't Repeat Yourself, and Keep It Simple, Stupid). Single responsibility functions/methods and descriptive naming are key to this.
1. Ensure all code is fully tested and passing with `pytest` before merging in the branch.
1. Ensure all code is without linting issues using black formatter (or the pipeline will fail and your commit will not be accepted) and is statically typed and checked with `mypy`.
1. Ensure that where functionality is changed or extended, the documentation is changed to reflect the work that was done.
1. Keep the development going in the right direction by following the roadmap and associated issues.
1. Where possible, use existing functions to extend the functionality before writing new functions.
1. Report bugs when found using the bug template so that all important information is logged.
1. Create issues for any major changes and enhancements that you wish to make so that it can be discussed transparently and receive appropriate community feedback before being implemented.
1. Keep feature-specific development small and incremental, preferably not one whole workflow but pieces of that workflow.
1. Encourage others to contribute and benefit from frewpy to help expand the user base and community.

## Your First Contribution

Unsure where to begin with contributing to frewpy? You'll probably want to pick up one of the issues marked _"good first issue"_ or _"needs help"_. Issues aren't necessarily just problems with the library, issues are GitLab's approach to an all encompassing item list, where labels define the nature of the item. The following issue labels are used on this project:

- good first issue: an easy to pick up, small issue that could be tackled by beginners.
- needs help: specifically required for the next version release.
- support: specific support required for users or developers of frewpy, the intention is to allow others to query it as an FAQ area if they encounter issues.
- suggestion: a suggestion for the library which is not yet agreed as a feature but something that might improve the library.
- enhancement: an agreed feature due to be developed which will enhance the functionality of the library
- discussion: a point which requires discussion from the community relating to the library.
- documentation: issues relating to improvements or modifications to the documentation.
- bug: something encountered when using or developing frewpy that needs fixing.

## Getting Started

### Setup

You'll need to have a [text editor](https://gitlab.arup.com/ait/how-to-wiki/-/wikis/Programming/Getting-Started), [python](https://gitlab.arup.com/ait/how-to-wiki/-/wikis/Python/Getting-Started), [Git for Windows](https://gitlab.arup.com/ait/how-to-wiki/-/wikis/Version-Control/Git) and greater than Oasys Frew version 19.4 build 24 installed on your PC.

> Please note: you might need Developer access to the repository before you're able to do anything. If this is the case then please contact the development team and we can help you out.

Next you'll need to clone the repository to somewhere local using your Git for Windows Bash. Once cloned, you'll need to pip install both the `requirements.txt` and the `requirements-dev.txt` into your project virtual environment. This will provide you with the correct libraries required to contribute towards frewpy.

### Branching

This repository functions using the [Gitflow Workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow) which means if you want to contribute, you'll need to pull your own branch off `develop` as this and the `master` branch are protected and **noone** has the permissions to push to them. In practice this is very simple to do and means anything you change to the code base in your branch will not break the rest of the library. This provides you with a great sandbox to play around with!

To branch off develop simply use the command `git checkout -b {branch name} develop`. Branch names must follow the naming convention of `type-short-description` where `type` can be: "feature", "admin", "bugfix", or "hotfix", and the `short-description` is a 1 to 3 word description of what you're doing on the branch. For example `feature-soil-pressures` or `admin-contribution-guide` are valid branch names.

### Testing

Once you've written code, you'll need to write some unit tests using the `pytest` library. You can look at other tests for inspiration in the tests directory or the [documentation](https://docs.pytest.org/en/stable/getting-started.html), but they're pretty basic to get going with and very quick to do. You can run the `coverage_report.bat` file and the VS Code extension [Coverage Gutters](https://marketplace.visualstudio.com/items?itemName=ryanluker.vscode-coverage-gutters) to have in-line coverage markings which help with writing unit tests that cover all aspects of your code. To run the tests, use the `test_project.bat` file for ease.

### Committing code

Every time you commit to the repository, a [Continuous Integration (CI) pipeline](https://about.gitlab.com/stages-devops-lifecycle/continuous-integration/) will run the [Black formatter](https://github.com/psf/black) check with a line length of 79 characters and fail if it recognises that any files need formatting changes. It is intended to extend this CI pipeline to include type checking and running the any tests but currently that has not been implemented. When writing your commit messages, please use the format:

```
Short Header
<blank line>
Explanation and reasoning for what was done.
<blank line>
Related or resolved issues
```

For example:

```
Refactoring soil module

This module had a profiler run through it and it was found to be very inefficient. Threading has been added to make it run faster and the number of local variables has been reduced to make it more human readable.

Related #13 #4
Resolves #14
```

If you have written something that you feel the library would benefit from having in the core code base, you can put in a merge request from your branch to the develop branch. Communicating what you have done and why, and that you'd like it to be reviewed. You don't need to explicitly say everything you have written in code as this is obvious from the diffs when comparing the branches, the main point to get across is why you've done what you've done. For example:

> "Allow users to set and get the water table levels so sensitivity analysis can be carried out"

rather than

> "Written methods get_water_table and set_water_table with the variables water_level and node_num"

## Reporting Bugs

To report a bug, simply create an issue in the repository and select the 'Bug' template in the drop down. This'll prompt you to fill in key information about the bug such as the exact situation in which the bug occurs, and how to replicate that environment.

## Submitting Feature Ideas

If you find yourself wishing frewpy did something in particular that it doesn't do already, you're probably not alone. Submitting a feature idea will let others know that this functionality is needed by many, and will make it more likely that it gets added to the library. Do this by creating an issue and using the appropriate labels to mark the issue for discussion/ suggestion and enhancement, noting the points in the below text. Make sure to fully scope the feature, thinking through why it's needed and how it might work.

The idea behind frewpy is to get Arup engineers into using python, or just programming logic, when approaching their designs. It's core aim is to make interacting with engineering software quicker, easier and more reliable than alternative methods. It is not intended that the core frewpy library solves specific engineering problems but rather enables engineers to solve their problems. This distinction is key and is what separates the core code base with the project examples in the examples directory. If you have a feature idea which is specific to the project you are on, it is probably better placed in the examples directory for others to use. If scripts in the examples directory become very popular, it might be worth converting it into the core code base in which case the feature idea can be submitted.

If you have a feature idea which would be applicable and helpful across many projects, it could be good to include it in the core frewpy code base and so it is worth submitting it or contacting the development team.

Please also check the project roadmap to see if the feature you are suggesting is planned for future releases.

## Code review process

The merge request will be reviewed in many ways, including: code quality, code styling, static typing, applicability, unit testing. Comments will be provided on the merge request which should then help the contributor to improve their contribution. Once all comments have been addressed, the feature will be merged into the core frewpy code base.

If you get a comment to 'rebase' your merge request, it means that a lot of the code base has changed since you branched off develop, and that you need to update your branch so it's easier to merge. To do this, simply type `git pull origin develop` when checked out in your branch. You can then fix any of the conflicts that might surface, and double check your contribution still operates as intended.

[Source for the template of this contributions guide](https://github.com/nayafia/contributing-template)
