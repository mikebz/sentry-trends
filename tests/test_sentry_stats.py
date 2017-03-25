"""testing of Sentry wrapper"""
import unittest
import string
from random import choice
from configparser import ConfigParser
from sentry_stats import SentryStats


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
        projects, link = stats.retrieve_projects_raw()
        self.assertIsNotNone(projects)
        self.assertIsNotNone(link)
        for project in projects:
            self.assertIsNotNone(project["status"])
            self.assertIsNotNone(project["slug"])

    def test_get_events(self):
        """
        basic test that the raw project json can be retrieved
        """
        stats = SentryStats(self.sentry_key, self.organization)
        events, link = stats.retrieve_events_raw(self.project)
        self.assertIsNotNone(events)
        self.assertIsNotNone(link)
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

    def test_parse_link(self):
        """ parse a full link header with previous and next """
        link_header = ("<https://sentry.io/api/0/projects/tempo-automation/tem"
                       "pocom-prod/events/?&cursor=1489099048000:0:1>; rel=\"p"
                       "revious\"; results=\"true\"; cursor=\"1489099048000:0:"
                       "1\", <https://sentry.io/api/0/projects/tempo-automatio"
                       "n/tempocom-prod/events/?&cursor=1488932091000:0:0>; re"
                       "l=\"next\"; results=\"true\"; cursor=\"1488932091000:0"
                       ":0\"")
        next_link = SentryStats.parse_next_url(link_header)
        self.assertEqual(("https://sentry.io/api/0/projects/tempo-automation/"
                          "tempocom-prod/events/?&cursor=1488932091000:0:0"),
                         next_link)

    def test_parse_no_prev(self):
        """ parse a header that just has next and no previous """
        link_header = ("<https://sentry.io/api/0/projects/tempo-automatio"
                       "n/tempocom-prod/events/?&cursor=1488932091000:0:0>; re"
                       "l=\"next\"; results=\"true\"; cursor=\"1488932091000:0"
                       ":0\"")
        next_link = SentryStats.parse_next_url(link_header)
        self.assertEqual(("https://sentry.io/api/0/projects/tempo-automation/"
                          "tempocom-prod/events/?&cursor=1488932091000:0:0"),
                         next_link)

    def test_parse_no_next(self):
        """ parse a header that just previous """
        link_header = ("<https://sentry.io/api/0/projects/tempo-automation/tem"
                       "pocom-prod/events/?&cursor=1489099048000:0:1>; rel=\"p"
                       "revious\"; results=\"true\"; cursor=\"1489099048000:0:"
                       "1\"")
        next_link = SentryStats.parse_next_url(link_header)
        self.assertIsNone(next_link)

    def test_parse_gibberish(self):
        """ parse a header that just previous """
        random_string = ''.join(choice(string.printable) for x in range(200))
        next_link = SentryStats.parse_next_url(random_string)
        self.assertIsNone(next_link)
