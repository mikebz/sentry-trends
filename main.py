"""
small utility for dumping out Sentry event trends
"""
import ConfigParser


def main():
    """main command line entry point"""
    parser = ConfigParser.ConfigParser()
    parser.read("config.ini")
    sentry_key = parser.get("api_keys", "sentry")
    print "Sentry Key: " + sentry_key[0:5] + "..."


if __name__ == "__main__":
    main()
