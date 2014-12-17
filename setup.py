
from __future__ import absolute_import, print_function

requires = [
    "ConfigArgParse>=0.9.3",
    "flask>=0.10.1"
#    "mesos.native>=0.21.0"
]

config = {
    'name': 'dispatch',
    'version': '0.0.1',
    'description': 'execute scripts anywhere on your mesos cluster',
    'author': 'Thomas Rampelberg',
    'author_email': 'thomas@mesosphere.io',

    'packages': [
        'dispatch'
    ],
    'entry_points': {
        'console_scripts': [
            'dispatch = dispatch.main:main',
        ]
    },
    'setup_requires': [ ],
    'install_requires': requires,
    'dependency_links': [ ],
    'tests_require': [ ],
    'scripts': [ ]
}

if __name__ == "__main__":
    from setuptools import setup

    setup(**config)
