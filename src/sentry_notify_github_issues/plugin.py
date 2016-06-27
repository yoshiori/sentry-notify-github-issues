from django import forms
from django.utils.translation import ugettext_lazy as _
from sentry.plugins.bases.notify import NotificationPlugin
from sentry.models import Activity
from sentry.utils.strings import strip
from sentry.utils import json
import urllib2

import sentry_notify_github_issues

class NotifyGitHubIssuesForm(forms.Form):
    repo = forms.CharField(label=_('Repository Name'),
        widget=forms.TextInput(attrs={'placeholder': 'e.g. getsentry/sentry'}),
        help_text=_('Enter your repository name, including the owner.'))

    access_token = forms.CharField(label=_('access token'),
        widget=forms.TextInput(attrs={'placeholder': 'e.g. xxxxxxxxxxxxxxxxxxxxxxxx'}),
        help_text=_('Enter your personal access token, create here https://github.com/settings/tokens/new'))

    api_endpoint = forms.CharField(label=_('API endpoint'),
        widget=forms.TextInput(attrs={'placeholder': 'e.g. https://github.example.com/api/v3/'}),
        help_text=_('if Github Enterprise, Enter api endpoint. '), required=False)

    label = forms.CharField(label=_('label'),
        widget=forms.TextInput(attrs={'placeholder': 'e.g. sentry'}),
        help_text=_('Enter label text.'), required=False)

class NotifyGitHubIssuesPlugin(NotificationPlugin):
    slug = 'notify-github-issues'
    title = _('GitHub Issues Notification')
    author = 'Yoshiori SHOJI'
    author_url = 'https://github.com/yoshiori'
    version = sentry_notify_github_issues.VERSION
    description = "Integrate GitHub issues by linking a repository to a project."
    resource_links = [
        ('Bug Tracker', 'https://github.com/yoshiori/sentry-notify-github-issues/issues'),
        ('Source', 'https://github.com/yoshiori/sentry-notify-github-issues'),
    ]
    conf_key = slug
    project_conf_form = NotifyGitHubIssuesForm

    def is_configured(self, project):
        return all((self.get_option(k, project) for k in ('repo', 'access_token')))

    def notify_users(self, group, event, fail_silently=False):
        repo = self.get_option('repo', group.project)
        api_endpoint = self.get_option('api_endpoint', group.project) or "https://api.github.com/"
        url = '%srepos/%s/issues' % (api_endpoint, repo,)

        title = event.error()
        body = '%s\n\n[<a href="%s">View on Sentry</a>]' % (strip(group.culprit), group.get_absolute_url())
        labels = self.get_option('label', group.project)

        data = {
          "title": title,
          "body": body,
        }
        if labels:
            data["labels"] = [x.strip() for x in labels.split(",")]

        req = urllib2.Request(url, json.dumps(data))
        req.add_header('User-Agent', 'sentry-notify-github-issues/%s' % self.version)
        req.add_header('Authorization', 'token %s' % self.get_option('access_token', group.project))
        req.add_header('Content-Type', 'application/json')
        resp = urllib2.urlopen(req)
        data = json.loads(resp.read())

        self.create_sentry_issue(group, data["title"], data["html_url"], "GH-%s" % data["number"])

    def create_sentry_issue(self, group, title, location, label):
        issue_information = {
            'title': title,
            'provider': self.get_title(),
            'location': location,
            'label': label,
        }
        Activity.objects.create(
            project=group.project,
            group=group,
            type=Activity.CREATE_ISSUE,
            data=issue_information,
        )
