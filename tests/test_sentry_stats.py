import unittest
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

    def test1(self):
        """
        placeholder test
        """
        self.assertEqual("True", str(True))

    def test_get_projects(self):
        """
        basic test that the raw project json can be retrieved
        """
        stats = SentryStats(self.sentry_key, "tempo-automation")
        projects = stats.retrieve_projects_raw()
        self.assertIsNotNone(projects)
