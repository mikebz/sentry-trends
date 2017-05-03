"""small utility for dumping out Sentry event trends"""
import ConfigParser
from datetime import datetime
import sys
from dateutil import parser
import pytz
from sentry_stats import SentryStats


def deep_get(dictionary, *keys):
    """
    deep get for nested dictionaries, great for getting stuff from
    REST api_keys
    Courtesy of:
    http://stackoverflow.com/questions/25833613/python-safe-method-to-get-value-of-nested-dictionary  # noqa
    """
    return reduce(lambda d, key: d.get(key) if d else None, keys, dictionary)


def process_issues(sentry_key, organization, project):
    """process issues"""
    stats = SentryStats(sentry_key, organization)
    issues = stats.retrieve_issues(project)

    print "\n\nTitle, Links, hits, percent gain"
    for issue in issues:
        row = [
            issue["title"],
            issue["status"],
            issue["jiraLink"],
            str(issue["hitsPerIssue"]),
            str(issue["percentGain"])
        ]
        print ", ".join(row)


def process_events(sentry_key, organization, project, days):
    """process and output the events for this project"""

    stats = SentryStats(sentry_key, organization)
    events = stats.retrieve_events(project, days)

    end_date = pytz.utc.localize(datetime.utcnow())
    day_breakdown = dict.fromkeys(range(0, days), 0)

    print "\n\nDate Created, Date Received, User ID, Type, Message"
    for event in events:
        row = [
            event["dateCreated"],
            event["dateReceived"],
            deep_get(event, "user", "id") or "",
            event["type"],
            event["message"].strip()
        ]
        print ", ".join(row)

        date_created = parser.parse(event["dateCreated"])
        delta = end_date - date_created
        day_slot = days - delta.days - 1
        day_breakdown[day_slot] += 1

    print "\n\nTotal: " + str(len(events))

    print "\n\nDay,Events"
    for day, occurances in day_breakdown.iteritems():
        print str(day) + ", " + str(occurances)


def main(argv):
    """main command line entry point"""
    if len(argv) == 0 \
       or argv[0] in ['/?', '-?', 'help', '-h', '/h'] \
       or not argv[0] in ['issues', 'events']:
        print "main.py help - for help"
        print "main.py events - for event report"
        print "main.py issues - for issues"
        sys.exit()

    config_parser = ConfigParser.ConfigParser()
    config_parser.read("config.ini")
    sentry_key = config_parser.get("api_keys", "sentry")
    organization = config_parser.get("common_filters", "organization")
    project = config_parser.get("common_filters", "project")
    print "Sentry Key: " + sentry_key[0:5] + "..."
    print "Organization: " + organization
    print "Project: " + project

    command = argv[0]
    if command == 'issues':
        process_issues(sentry_key, organization, project)
    elif command == 'events':
        days = config_parser.getint("event_filters", "days")
        print "Days of data: " + str(days)
        process_events(sentry_key, organization, project, days)


if __name__ == "__main__":
    main(sys.argv[1:])
