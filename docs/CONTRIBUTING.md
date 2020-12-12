# Introduction

You can contribute to this repository in multiple ways: making issues that detect problems or describe new features,
creating PR or simply responding comments.
All kinds of positive interaction, which adds value to the project, will be considered as a contribution.

## Comunication

All interactions with the community must be respectful.
The use of the English language is recommended when it's possible.

## Workflow

Below is listed the development process that is most commonly used in this repository.

1. Detection of a problem and its approach:
  It involves the creation and description of an issue.

2. Supervision of the issue:
  It involves the aggregation of labels, the improvement in the description, and the addition of some answers to give feedback if necessary.

3. Developing the solution:
  if the issue requires development, it must be done through a branch based on the develop branch. When the development is considered complete, a PR must be made to apply the changes.

4. Review:
  The PR must be reviewed.
  For this, there are a number of applications that do it automatically and then a contributor makes it manually.
  The review returns a request for improvement to the PR or gives way for it to merge.

5. Merge:
  When the PR is approved, the changes are applied so they will be included in the next version of the package.

## Standars:

- Commits style: [gitmoji][gitmoji]
- Code formatter: [black][black]
- Docstrings style: [google][google-docstring]
- Max line length: 199
- Type hints?: Yes
- Min code coverage accepted: 100%

For more details take a look at [python-observer][python-observer], a package used in this repo that checks the code in every PR.

[gitmoji]: https://gitmoji.carloscuesta.me/
[black]: https://github.com/psf/black
[google-docstring]: https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings
[python-observer]: https://github.com/lucasvazq/python-observer
