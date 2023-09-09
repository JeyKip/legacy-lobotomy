# Legacy Lobotomy

Legacy Lobotomy is a practical article series about improving a legacy Django application step by step.

The `main` branch contains the latest state of the project. Earlier stages are kept in separate branches so the changes from each article can be reviewed independently.

The project is based on a real application with common problems found in legacy systems: limited test coverage, mixed responsibilities, slow database queries, security issues, difficult API code, and outdated dependencies.

## What the series covers

The series includes topics such as:

- setting up and understanding an existing Django project
- adding automated tests with pytest
- testing the Django admin panel with Selenium
- refactoring and improving Django admin code
- refactoring Django and Django REST Framework code
- improving validation and API design
- finding and fixing security issues
- creating realistic test data
- working with Django management commands
- upgrading Django and Django REST Framework to newer versions
- upgrading and replacing old dependencies
- finding database and performance problems
- profiling APIs and improving performance

## Articles

Start with the introductory article:

**[Legacy Lobotomy — Confident Refactoring of a Django Project](https://levelup.gitconnected.com/legacy-lobotomy-confident-refactoring-of-a-django-project-adbeb064c455)**

It explains the project, how the tutorials are organized, and contains the current list of articles in the series.

You can also find my other articles on [Medium](https://medium.com/@jeykip1990).

## Repository structure

The `main` branch always contains the latest state of the project.

Each article usually has two related branches that show the project before and after the changes described in each article. These branches are kept so readers can follow the changes step by step or start from the point used in a particular article.

For example:

* [initial-codebase](https://github.com/JeyKip/legacy-lobotomy/tree/initial-codebase) contains the original state of the project
* [running-the-project](https://github.com/JeyKip/legacy-lobotomy/tree/running-the-project) contains the changes from the first tutorial
* later branches continue from the previous state as the project is gradually improved

After a new article is completed, `main` is fast-forwarded to the latest branch. This means that `main` always shows the most up-to-date version of the project, while the article branches remain available as snapshots of earlier stages.

Each article links to the branches used in that tutorial.

## Status

Legacy Lobotomy is an ongoing series. New articles and code changes are added as the project moves through different parts of the legacy codebase.