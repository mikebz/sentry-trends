# sentry-trends
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fmikebz%2Fsentry-trends.svg?type=shield)](https://app.fossa.io/projects/git%2Bgithub.com%2Fmikebz%2Fsentry-trends?ref=badge_shield)

A Python script that grabs Sentry events and outputs them as CSV

To use this cript:
* first you need to make a copy of the `config_example.ini` into `config.ini`.  Then you will need to populate the Sentry API key, your organization slug and your project slug.
* create a virtual environment
* pip install the requirements

The default timespan to grab the events into CSV is 7 days, but it's configurable.

There are tests you can run if you want to enhance or refactor this utility, but you will need to make sure your `config.ini` is properly set up because the tests make live calls to Sentry.

Sample usage:
```
python main.py 
```


## License
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fmikebz%2Fsentry-trends.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2Fmikebz%2Fsentry-trends?ref=badge_large)