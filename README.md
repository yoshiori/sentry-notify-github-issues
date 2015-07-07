# sentry-notify-github-issues

A Sentry notification plugin for GitHub Issues.

## Installation
```sh
pip install git+https://github.com/yoshiori/sentry-notify-github-issues
```

## Configuration
- Repository Name
  - Github's repository name. (required)
  - e.g. user_name/project_name
- access token
    - Personal access token (required)
    - create [here](https://github.com/settings/tokens/new)
- API endpoint
    - GitHub API endpoint. (default: https://api.github.com/)
    - This is required only if you are using Github Enterprise.
- label
    - Issues label text.
    - Separated by a comma if you want to specify more than one.
    - e.g. sentry,error
