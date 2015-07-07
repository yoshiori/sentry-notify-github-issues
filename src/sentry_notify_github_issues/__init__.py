try:
    VERSION = __import__('pkg_resources') \
        .get_distribution('sentry-notify-github-issues').version
except Exception, e:
    VERSION = 'unknown'
