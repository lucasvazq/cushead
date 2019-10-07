
3040/5000
## Introduction

You can contribute to this repository in multiple ways: making issues that detect problems or describe new features, creating PR or simply responding comments.
All kinds of positive interaction, which adds to the project, will be considered as a contribution.

Here is a [list][1] provided by github, to which we cling, which defines the different types of contributors:

- **Author**: The person / s or organization that created the project

- **Owner**: The person / s who has administrative ownership over the organization or repository (not always the same as the original author)

 - **Maintainers**: Contributors who are responsible for driving the vision and managing the organizational aspects of the project (They may also be authors or owners of the project.)

 - **Contributors**: Everyone who has contributed something back to the project

 - **Community Members**: People who use the project. They might be active in conversations or express their opinion on the project’s direction

## Issue Creation:

If you think there is something in the repository that needs to be changed, or if it needs to be added, create an Issue describing the problem.
You can also use it to ask questions or open discussion topics.
Always try to comply with the template provided.

Depending on the type of problem you are defining, different types of labels will be applied. These are going to refer to the type of problem that you are posing and serve to indicate the steps to be followed by the developers or the rest of the community.

## Pull Request:

Pull requests imply a change in our repository. It can be in the documentation, as in some configuration or the main code. The source code of this repository, being made in python, we try to apply certain style rules.

When you create a PR, if you have modified any .py file, an application called restyled.io will try to review your contribution with 4 code review packages. Leave a message and make a new PR indicating the steps to follow to meet the required styles.
The formatters used by the application are:

- autopep8

- black

- reorder-python-imports

- yapf

Others application, are doing some checks too:

- travis-ci: Check if script run correctly

- codacy: Verify the quality of code

- guardrails: Search security problems

In addition, the person in charge of manually reviewing the code, will apply a review with the code verifiers: **flake8** and **pylint**

Also, the docstring used need to follows the Google Style and comments must be in english

Note: The test part, and the requirement to meet 100% with coverage is not required. This we do every so often, not in each PR

## Labels

### Status #cfcfcf

- approved
- wip
- wontfix
- dont merge
- merge

### High priority #000000

- bug
- security
- master

### Comunity #0366D6

- discusion
- question
- good first issue
- help wanted

### Type #d11f5a

- dependencies
- documentation
- enhancement
- fix
- review

## Special #C6FF91

- hacktoberfest

### General labels

- approved: 

# remove:
cool


### Issues labels

### PR labels

## Reviews

## Community participation

All interaction with the community must be respectful and with the intention of adding value. The project promotes any type of non-offensive vocabulary. The use of English language is recommended because it is the most universal, a question asked and answered in English has the possibility of having more scope than if it is answered in another language



[1]: https://opensource.guide/how-to-contribute/#anatomy-of-an-open-source-project
