from .base import BaseProvider
from .bitbucket.bitbucket_provider import BitbucketProvider
from .gitlab.gitlab_provider import GitlabProvider


def get_gitlab_vcs_provider() -> BaseProvider:
    return GitlabProvider()


def get_bitbucket_vcs_provider() -> BaseProvider:
    return BitbucketProvider()
