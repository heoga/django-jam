# JAM - Agile Lifecycle Management for Django
[![build-status-image]][travis]
The goal of this project is to provide an open-source tool to facilitate the
managment of agile projects in large organisations.

## Installation
Clone from Github & run `pip install django-jam`

## Running tests
`setup.py test`

## Configuration
### Authentication
The JAM module requires user-authentication.  How this is established is not
restricted.  All that is required by JAM is that the following named views are provided:
- login
- logout

## Installed Apps
Add the following to your INSTALLED_APPS setting:
```
INSTALLED_APPS = (
    ...
    'jam.apps.JamConfig',
    'rest_framework',
    'bootstrap3',
)
```
Since jam overrides the view of rest_framework API it must appear above the
rest_framework in the list.

[build-status-image]: https://secure.travis-ci.org/heoga/django-jam.svg?branch=master
[travis]: http://travis-ci.org/heoga/django-jam?branch=master
