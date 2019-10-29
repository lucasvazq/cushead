# Introduction

You can contribute to this repository in multiple ways: making issues that detect problems or describe new features,
creating PR or simply responding comments.
All kinds of positive interaction, which adds to the project, will be considered as a contribution.

Here is a [list][1] provided by github, to which we cling, which defines the different types of contributors:

- **Author**: The person / s or organization that created the project

- **Owner**: The person / s who has administrative ownership over the organization or repository (not always the same
as the original author)

 - **Maintainers**: Contributors who are responsible for driving the vision and managing the organizational aspects of
 the project (They may also be authors or owners of the project.)

 - **Contributors**: Everyone who has contributed something back to the project

 - **Community Members**: People who use the project. They might be active in conversations or express their opinion on
 the project’s direction

## Language

All interaction with the community must be respectful and with the intention of adding value. The project promotes any
type of non-offensive vocabulary. The use of English language is recommended because it is the most universal, a
question asked and answered in English has the possibility of having more scope than if it is answered in another
language.

## Workflow

In addition to the conceptualization of the types of contributions, we also want to define the different types of work
that are carried out to culminate in these contributions.

1. Detection of a problem and its approach: It involves the creation and description of an issue

2. Supervision of the issue: It involves the aggregation of labels, the improvement in the writing of the problem and
the addition of some response to give feedback. The label determines the status of the issue: if it is closed, or if it
is in progress. It is fair to always notify the user of the decision made.

3. Assignments and branches: Following an issue someone must be assigned to solve the problem. For this, those
responsible are provided with a specific branch on which they must work to solve the problem.

4. The creation of the PR: The work carried out through the branch must be specified through a PR. Its status can be
Woking In Progress or ready to review.

5. Supervision of the PR: It involves handling the PR request. Labels must be added and questions answered

6. Review: The PR must be reviewed. For this there are a number of applications that do it automatically and then a person
makes it manually. The review returns a request for improvement to the PR, or gives way for it to merge.

7. Merge: The PR is merged, and the base branch is updated.

## Issue Creation:

If you think there is something in the repository that needs to be changed, or if it needs to be added, create an Issue
describing the problem.
You can also use it to ask questions or open discussion topics.
Always try to comply with the template provided.

Depending on the type of problem you are defining, different types of labels will be applied. These are going to refer
to the type of problem that you are posing and serve to indicate the steps to be followed by the developers or the rest
of the community.

## Supervision

Steps

1. Check if the Issue / PR follow the determinated template structure.

2. Add labels

3. Improve or help to improve the description

4. Answer question and give feedback

<details>

<summary><b>Labels list</b></summary>

>
> #### Status
> 
> Color: ![#cfcfcf][color_1]
> 
> Issues:
> 
> - approved: Can work on it
> 
> PR:
> 
> - don't merge: Don't merge the PR
> 
> - merge: Merge the PR
>

>
> #### High priority
> 
> Color: ![#000000][color_2]
> 
> - bug: Something doesn't work as expected
> 
> - security: Security issue
> 
> - master: Something that occurs in master branch
>

>
> #### Comunity
> 
> Color: ![#0366d6][color_3]
> 
> - discusion: Debate about something
> 
> - question: Question
> 
> - good first issue: To attract new contributors
> 
> - help wanted: Help is needed or to attract new contributors
>

>
> #### Type
>
> Color: ![#d11f5a][color_4]
>
> - dependencies: Update a dependency
>
> - documentation: Documentation development
>
> - enhancement: New feature
>
> - fix: Something need to be fixed or improved
>
> - review: Proposes analysis
>

>
> #### Special
> 
> Color: ![#94e582][color_5]
> 
> - hacktoberfest: https://hacktoberfest.digitalocean.com/
>

</details>

## Assigned and Branchs

When a problem is determined through an issue and become approved with the "approved" label, there is free way to start
working on it.
To do so, one person or several must be designated as responsible for solving the problem. It can be the person who
does the PR, someone inside the project or anyone who offers.

When assignments are made, a new branch is automatically generated with the following name format: issue-[Issue Nº]
Example: issue-25. This is the branch that must be used to work and then perform a PR

## Pull Request:

Pull requests imply a change in our repository. It can be in the documentation, as in some configuration or the main
code. The source code of this repository, being made in python, we try to apply certain style rules.

When you create a PR, if you have modified any .py file, an application called [restyled.io][2] will try to review your
contribution with 4 code review packages. Leave a message and make a new PR indicating the steps to follow to meet the
required styles.
The formatters used by the application are:

- autopep8

- black

- reorder-python-imports

- yapf

Others application, are doing some checks too:

- travis-ci: Check if script run correctly

- codacy: Verify the quality of code

- guardrails: Search security problems

In addition, the person in charge of manually reviewing the code, will apply a review with the code verifiers:
**flake8** and **pylint**

Also, the docstring used need to follows the Google Style and comments must be in english

Note: The test part, and the requirement to meet 100% with coverage is not required. This we do every so often, not in
each PR

## Merge

Automatic merge with label 'merge' by the application [probot-auto-merge][3]

[1]: https://opensource.guide/how-to-contribute/#anatomy-of-an-open-source-project
[2]: https://restyled.io
[3]: https://github.com/apps/probot-auto-merge

[color_1]: https://placehold.it/15/cfcfcf/000000?text=+
[color_2]: https://placehold.it/15/000000/000000?text=+
[color_3]: https://placehold.it/15/0366d6/000000?text=+
[color_4]: https://placehold.it/15/d11f5a/000000?text=+
[color_5]: https://placehold.it/15/94e582/000000?text=+

```
flake8
(dlint: 0.9.0, flake8-annotations-complexity: 0.0.2, flake8-bandit: 2.1.2, flake8-broken-line: 0.1.1, flake8-bugbear: 19.8.0, flake8-comprehensions: <cached_property.cached_property object at 0x7f639efd9810>, flake8-darglint: 0.4.1, flake8-debugger: 3.1.0, flake8-docstrings: 1.5.0, pydocstyle: 4.0.1, flake8-eradicate: 0.2.3, flake8-executable: 2.0.3, flake8-print: 3.1.1, flake8-string-format: 0.2.3, flake8_builtins: 1.4.1, flake8_coding: 1.3.2, flake8_commas: 2.0.0, flake8_isort: 2.3, flake8_pep3101: 1.2.1, flake8_quotes: 2.1.0, logging-format: 0.6.0, mccabe: 0.6.1, naming: 0.8.2, pycodestyle: 2.5.0, pyflakes: 2.1.1, radon: 2.4.0, rst-docstrings: 0.0.11, wemake-python-styleguide: 0.12.5)
```
