# Django-Nimble
[![build-status-image]][travis]
[![coverage-status-image]][codecov]

Jack be nimble, jack be quick.

The goal of this project is to provide an open-source tool to facilitate the
management of agile projects in large organisations.

## Installation
Run `pip install django-nimble`

## Running tests
`setup.py test`

## Configuration
### Authentication
The nimble module requires user-authentication.  How this is established is not
restricted.  All that is required by nimble is that the following named views
are provided:
- login
- logout

## Installed Apps
Add the following to your INSTALLED_APPS setting:
```
INSTALLED_APPS = (
    ...
    'nimble.apps.NimbleConfig',
    'rest_framework',
    'bootstrap3',
)
```
Since nimble overrides the view of rest_framework API it must appear above the
rest_framework in the list.

[build-status-image]: https://secure.travis-ci.org/heoga/django-nimble.svg?branch=master
[travis]: http://travis-ci.org/heoga/django-nimble?branch=master
[coverage-status-image]: https://codecov.io/gh/heoga/django-nimble/branch/master/graph/badge.svg
[codecov]: https://codecov.io/gh/heoga/django-nimble?branch=master
