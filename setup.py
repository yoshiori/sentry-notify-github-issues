#!/usr/bin/env python
from setuptools import setup, find_packages

tests_require = [
    'nose',
]

install_requires = [
    'sentry>=5.0.0',
]

setup(
    name='sentry-notify-github-issues',
    version='1.0.0',
    author='Yoshiori Shoji',
    author_email='yoshiori@gmail.com',
    url='http://github.com/yoshiori/sentry-notify-github-issues',
    description='A Sentry notification plugin for GitHub issues.',
    long_description=__doc__,
    license='MTI',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    zip_safe=False,
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={'test': tests_require},
    test_suite='runtests.runtests',
    include_package_data=True,
    entry_points={
       'sentry.apps': [
            'notify_github_issues = sentry_notify_github_issues',
        ],
       'sentry.plugins': [
            'notify_github_issues = sentry_notify_github_issues.plugin:NotifyGitHubIssuesPlugin'
        ],
    },
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)
