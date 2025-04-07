# IVF Success Chance Calculator

This module creates a Django webserver that calculates IVF success chances according to the CDC's formulae as on [their ART page](https://www.cdc.gov/art/ivf-success-estimator/index.html). The homepage allows the user to provide inputs, and then shows the calculated value.

## installing dependencies

```python
pip install -r requirements.txt
```

## To collect static files:

```python
python manage.py collectstatic
```

## To run this application:

make sure to add the following in `.env` at root level
```
SECRET_KEY=not_empty
DEBUG=False

ALLOWED_HOSTS=*
```

Then run the next command from your terminal/command line

```python
python manage.py runserver <port>
```
and navigate to localhost:<port> in your browser
