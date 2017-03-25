"""small utility for dumping out Sentry event trends"""
import ConfigParser
from .sentry_stats import SentryStats


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
    parser = ConfigParser.ConfigParser()
    parser.read("config.ini")
    sentry_key = parser.get("api_keys", "sentry")
    organization = parser.get("event_filters", "organization")
    project = parser.get("event_filters", "project")

    print "Sentry Key: " + sentry_key[0:5] + "..."
    print "Organization: " + organization
    print "Project: " + project

    stats = SentryStats(sentry_key, organization)
    events = stats.retrieve_events_raw(project)

    print "\n\nDate Created, Date Received, User ID, Type, Message"
    for event in events:
        row = [
            event["dateCreated"],
            event["dateReceived"],
            deep_get(event, "user", "id") or "",
            event["type"],
            event["message"]
        ]
        print ", ".join(row)


if __name__ == "__main__":
    main()
