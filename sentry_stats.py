"""
sentry stats functions
"""
import requests


class SentryStats(object):
    """
    class for getting sentry stats
    """
    def __init__(self, api_key, organization):
        """
        init
        """
        self.api_key = api_key
        self.organization = organization

    def _headers(self):
        return {"Authorization": "Bearer " + self.api_key}

    def retrieve_events_raw(self, project):
        """
        get the raw events for a particular project
        """
        result = requests.get(
            "https://app.getsentry.com/api/0/projects/{}/{}/events/".format(
                self.organization, project),
            headers=self._headers()
            )
        result.raise_for_status()
        payload = result.json()
        return payload, result.headers["Link"]

    def retrieve_projects_raw(self):
        """
        get a raw list of projects
        """
        result = requests.get(
            "https://app.getsentry.com/api/0/projects/",
            headers=self._headers()
            )
        result.raise_for_status()
        payload = result.json()
        return payload, result.headers["Link"]
