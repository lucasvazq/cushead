# Contribution guide

You can contribute to this repository in multiple ways: making Issues that mention inconveniences or describe new
features, creating PR or simply responding comments. All kinds of positive interaction will be considered as a
contribution.

Here is a [list][contribution-list] provided by Github, to which we cling, which defines the different types of contributors:

- **Author**: The person / s or organization that created the project.

- **Owner**: The person / s who has administrative ownership over the organization or repository (not always the same
as the original author).

 - **Maintainers**: Contributors who are responsible for driving the vision and managing the organizational aspects of
 the project (They may also be authors or owners of the project).

 - **Contributors**: Everyone who has contributed something back to the project.

 - **Community Members**: People who use the project. They might be active in conversations or express their opinion on
 the project’s direction.

## Language

All interactions with the community must be respectful and with the intention of adding value. The project promotes any
type of non-offensive vocabulary. The use of the English language is recommended because it is the most universal.
A question asked and answered in English has the possibility of having more scope than if it is answered in another
language.

## Workflow

In addition to the conceptualization of the types of contributions, we also want to define the different types of work
that are carried out to culminate in these contributions.

Next, a brief introduction to the key parts of the workflow is made. A more detailed description is given below.

### Creation of an Issue

If you think there is something in the repository that needs to be changed, or if it needs to be added, create an Issue
describing the problem.
You can also use it to ask questions or open discussion topics.
Always try to comply with the template provided.

Depending on the type of problem you are defining, different types of labels will be applied. These are going to refer
to the type of problem that you are posing and serve to indicate the steps to be followed by the developers or the rest
of the community to solve your approach.

### Supervision of the Issue

It involves the aggregation of labels, the improvement in the description, and the addition of some response to give
feedback for the actions taken.
The label determines the status of the issue: if it is closed, or if it is in progress.
It is fair to always notify the user of the decision made.

Supervision consists of a series of steps:

1. Check if the Issue follow the determinated template structure.

2. Add labels, project, milestone and estimates ([Zenhub][zenhub] metric) as necessary.

3. Improve or help to improve the description.

4. Answer question and give feedback.

5. Update the status (Closed, approved or WIP).

**Status**

Closed: When an Issue doesn't is invalid, duplicated or already solved.

Approved: given through 'approved' label.

Working In Progress (WIP): refers to an Issue that has PR open or a modified branch.
It's added throught the title: (WIP) I: ISSUE NAME.

Example: `(WIP) I: Foo Bar`

### Assignments and branches

When a problem is determined through an issue and become approved with the "approved" label, there is already a free
road to start working on it.
To do so, one person or several must be designated as responsible for solving the problem. It can be the person who
does the PR, someone internal to the project or anyone who offers.

When assignments are made, a new branch is automatically generated with the following name format: issue-[Issue Nº]

Example: `issue-25`

This is the branch that must be used to work and then perform a PR.

The automation in the creation of branch is made with [create-issue-branch][create-issue-branch] application.

### Creation of the PR

The work carried out through the branch needs to end in a PR.
PR can have various status: WIP, RR, BRC or RM.

**Status**

Working In Progress (WIP): refers to a work that isn't ended yet.
The creation of a PR at an early stage of work, helps to detect errors and direct the project in the right direction
early. This status blocks the possibility of merging and review thanks to the [WIP][wip] application.

Ready to Review (RR): When the development is considered finished and need to pass the review stage.

Beign Reviewed and Corrected (BRC): The stage when the work is being reviewed.

Ready to Merge (RM): When the PR pass the review and is ready to be merged.

## Supervision of the PR

As the Issue supervision point, this involves the aggregation of labels, the improvement in the description and
the give of feedback. It also involves the aggregation of titles that determines the status of the PR.
This status is described in the prev title, and its needs to be specified through the title like the Issues.

Example: `(RM) PR: I 25: ISSUE NAME`

## Reviews

Pull requests imply a change in the repository. It can be in the documentation, as in some configuration or the main
code. For the source code of this repository, being made in python, we try to apply certain style rules.

When you create a PR, if you have modified any .py file, an application called [restyled.io][restyled-io] will try to review your
contribution with 4 code review packages. If you missing something, it leaves a message and makes a new PR to your
commits with the correction needed to meet the required styles.

The formatters used by the application are:

- [autopep8][autopep8]

- [black][black]

- [reorder-python-imports][reorder-python-imports]

- [yapf][yapf]

Others application, are doing some checks too:

- [travis-ci][travis-ci] [EXTERNAL]: Check if script run correctly

- [codacy][codacy] [EXTERNAL]: Verify the quality of code

- [guardrails][guardrails] [EXTERNAL]: Search security problems

In addition, the person in charge of manually reviewing the code will apply a review with the following code verifiers:

- [pylint][pylint]

- [flake8][flake8]

Also, the docstring used need to follows the [Google Style][google-python-style] and comments must be in english.

Note: The test part, and the requirement to meet 100% of coverage is not required. This we do every so often, not in
each PR

## Merge

When the PR pass the review, it's ready to merge.
For this, add to it the label 'merge' and it's being automatic merged to their base branch thanks to
[probot-auto-merge][probot-auto-merge] application

## Ancillary

### Labels List

<details>

<summary><b>Open</b></summary>

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

### Other applications

[codecov][codecov]:

[dependabot][dependabot]

[imgbot][imgbot]

[nextrelease][nextrelease]

[welcome-bot][welcome-bot]


[codecov]: https://codecov.io/gh/lucasvazq/cushead
[dependabot]: https://dependabot.com/
[imgbot]: https://imgbot.net/
[nextrelease]: https://www.nextrelease.io/
[welcome-bot]: https://probot.github.io/apps/welcome/

[contribution-list]: https://opensource.guide/how-to-contribute/#anatomy-of-an-open-source-project

[restyled-io]: https://restyled.io
[zenhub]: https://zenhub.com
[create-issue-branch]: https://github.com/robvanderleek/create-issue-branch
[wip]: https://github.com/marketplace/wip
[probot-auto-merge]: https://github.com/apps/probot-auto-merge

[autopep8]: https://github.com/hhatto/autopep8
[black]: https://github.com/psf/black
[reorder-python-imports]: https://github.com/asottile/reorder_python_imports
[yapf]: https://github.com/google/yapf

[travis-ci]: https://travis-ci.org/lucasvazq/cushead
[codacy]: https://app.codacy.com/manual/lucasvazq/cushead/dashboard
[guardrails]: https://www.guardrails.io/

[pylint]: https://www.pylint.org/
[flake8]: http://flake8.pycqa.org/en/latest/

[google-python-style]: http://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings

[color_1]: https://placehold.it/15/cfcfcf/000000?text=+
[color_2]: https://placehold.it/15/000000/000000?text=+
[color_3]: https://placehold.it/15/0366d6/000000?text=+
[color_4]: https://placehold.it/15/d11f5a/000000?text=+
[color_5]: https://placehold.it/15/94e582/000000?text=+
