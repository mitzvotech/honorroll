# Capital Pro Bono Honor Roll

As part of the 2011 National Celebration of Pro Bono, the D.C. Access to Justice Commission and the D.C. Bar Pro Bono Program assisted the D.C. Courts to establish the Capital Pro Bono Honor Roll; and it has continued annually since then to celebrate the pro bono contributions made by member of the DC Bar. The Honor Roll, which is jointly sponsored by the District of Columbia Court of Appeals and the Superior Court of D.C., recognizes attorneys who provide 50 or more hours of pro bono services (or 100 or more hours of service for a higher recognition category) per year. To be included in the Honor Roll, D.C. Bar members and others who are authorized to perform pro bono work in the District of Columbia should submit the online application form, which includes a declaration that they have provided the prerequisite number of hours of pro bono work in the calendar year. Registration for the Honor Roll honoring pro bono contributions made during calendar year 2015 ends on January 31, 2016. Participating attorneys are recognized on the Courts' website and elsewhere.

This application is the data collection and publication engine for the Honor Roll.

## Installation

`honorroll` is a Flask application and is built for Python 3. To install, clone this repo, then `cd` into it. Set up your preferred virtual environment.

You'll need to set the following environmental variables: `MONGOLAB_DB`, `MONGOLAB_URI`, `SECRET_KEY`, and `SMTP_USER_PWD`. The application uses Mandrill, so you'll need to get an API key, and that will be your `SMTP_USER_PWD`. When developing, I also set `ENV_DEBUG=True` and `PYTHONPATH=app`.

Once you've set your environmental variables, the application can be run using `python app/app.py`.

## Testing

`honorroll` uses py.test.

## License

MIT
