Getting Started
===============
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

Prerequisites
-------------

This package relies on a number of other modules. The modules that must be installed are ``pyttsx3``, ``flask`` and ``uk_covid19``. This can be done with the following commands

```python
pip install pyttsx3
pip install flask
pip install uk-covid19
```

You will also want to have your AIP keys for http://api.openweathermap.org and http://newsapi.org respectively.

Installing
----------

To get the system running copy the packaging to the desired location. Then run ``install.py`` to initialise key values in the config file. Finally execute ``main_flask.py`` in ``.../covid_alarm_clock_packaging/covid_alarm_clock/``.
