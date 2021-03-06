# Social Security data API wrapper for Python

This API provides a standardized interface for accessing social security data.

The API currently provides one endpoint, `/dmf`, which checks a Social Security Death Master File for a record associated with a particular Social Security number.

The goal of the API is to provide SSN validation functions without leaking unnecessary data to client applications.

The API comes with a backend for [Veris](http://veris-ssn.com/), which can be swapped out for other backends as necessary.

## Installation

0. Install [`pipenv`](https://docs.pipenv.org/) ('pip3 install pipenv' might be enough, on Debian)
1. Run `pipenv install`
2. Set an environment variable `DMF_CONFIG` pointing to the absolute path of `config.py` (your configuration file, which you should create based on `config.py.tmpl`).
3. Run `pipenv shell`
4. Start the server: `python serve.py`
5. The API is now available at `http://localhost:5001`
