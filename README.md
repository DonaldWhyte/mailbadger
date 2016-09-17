![mailbadger](content/logo.png)

mailbadger is a script that tries to find the name fo 

You give mailbadger the full name of the employee you want to contact and the domain of the company's mail server.  mailbadger then outputs email addresses from the company.

**NOTE:** mailbadger is Python 3 only!

## Installation

Use pip:

```
pip install mailbadger
```

Or clone this repository and manually run installation:

```
cd mailbadger
python setup.py install
```

## Usage

```
python mailbadger.py <firstName> <lastName> <email
```

Example output:

```
> python mailbadger.py donald whyte devcorp.com
dwhyte@devcorp.com
donaldwhyte3@devcorp.com
donaldw@devcorp.com
```

## TODO

## Running Tests

Unit tests can be executed by running:

```
python setup.py test
```

## Limitations

TODO
