"""small utility for dumping out Sentry event trends"""
import ConfigParser
from datetime import datetime
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


def main():
    """main command line entry point"""
    config_parser = ConfigParser.ConfigParser()
    config_parser.read("config.ini")
    sentry_key = config_parser.get("api_keys", "sentry")
    organization = config_parser.get("event_filters", "organization")
    project = config_parser.get("event_filters", "project")
    days = config_parser.getint("event_filters", "days")
    print "Sentry Key: " + sentry_key[0:5] + "..."
    print "Organization: " + organization
    print "Project: " + project
    print "Days of data: " + str(days)

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


if __name__ == "__main__":
    main()
