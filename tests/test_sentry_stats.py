"""testing of Sentry wrapper"""
import unittest
from configparser import ConfigParser
from ..sentry_stats import SentryStats


class SentryStatsTest(unittest.TestCase):
    """
    Sentry Stats test cases
    """
    def setUp(self):
        """
        set up the tests,
        mainly get the API key
        """
        parser = ConfigParser()
        # maybe in the future we use a different config file
        # for testing..
        parser.read("config.ini")
        self.sentry_key = parser.get("api_keys", "sentry")
        self.organization = parser.get("event_filters", "organization")
        self.project = parser.get("event_filters", "project")

    def test_get_projects(self):
        """
        basic test that the raw project json can be retrieved
        """
        stats = SentryStats(self.sentry_key, self.organization)
        projects = stats.retrieve_projects_raw()
        self.assertIsNotNone(projects)
        for project in projects:
            self.assertIsNotNone(project["status"])
            self.assertIsNotNone(project["slug"])

    def test_get_events(self):
        """
        basic test that the raw project json can be retrieved
        """
        stats = SentryStats(self.sentry_key, self.organization)
        events = stats.retrieve_events_raw(self.project)
        self.assertIsNotNone(events)
        for event in events:
            print event["eventID"]
            self.assertIsNotNone(event["dateCreated"])
            self.assertIsNotNone(event["dateReceived"])
            # note that sometimes the user node is not present
            # self.assertIsNotNone(event["user"])
            # self.assertIsNotNone(event["user"]["ip_address"])
            self.assertIsNotNone(event["entries"])
            self.assertIsNotNone(event["type"])
            self.assertIsNotNone(event["message"])
