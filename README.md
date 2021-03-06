# COVID Smart Alarm Clock

This project is designed to help make it easier for users to schedule when they get updates on key information during the COVID-19 pandemic. The package allows users to get the latest COVID stats, the weather and the headlines all in the same place. They can choose when they get an announcement, and whether or not news and weather updates accompany the latest stats. This can all be done from the users browser.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

This package relies on a number of other modules. The modules that must be installed are `pyttsx3`, `flask` and `uk_covid19`. This can be done with the following commands

```python
pip install pyttsx3
pip install flask
pip install uk-covid19
```

You will also want to have your AIP keys for www.api.openweathermap.org and www.newsapi.org respectively.

### Installing

To get the system running copy the packaging to the desired location. Then run `install.py` to initialise key values in the config file. Finally execute `main_flask.py` in `.../covid_alarm_clock_packaging/covid_alarm_clock/`.

## Running the tests

To test the API's and speech engine run `test.py` in the tests folder.

## Built With

- [Flask](https://flask.palletsprojects.com/en/1.1.x/) - The web framework used
- [uk_covid19](https://publichealthengland.github.io/coronavirus-dashboard-api-python-sdk/index.html) - COVID data API
- [pyttsx3](https://pypi.org/project/pyttsx3/) - text to speech engine

## Authors

- **Louis Alexander** -  [GitHub](https://github.com/louisalexander2001/covid_alarm_clock_packaging)

## License

This project is licensed under the MIT License - see the `LICENSE.md` file for details

## Location

This package can be found at https://github.com/louisalexander2001/covid_alarm_clock_packaging