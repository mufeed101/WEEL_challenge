# Flask Project

## Installation

To install the required dependencies for this Flask project:

```bash
pip install -r requirements.txt
```

## Set Environment variables
You need to set the following env variables before testing or running the application

### Windows
```bash
$env:host = "localhost"
$env:user = "root"
$env:password = "password"
```

### MAC
```bash
export host="localhost"
export user="root"
export password="password"
```

## Testing

To run tests written for this Flask project:

```bash
python -m pytest tests
```

## Running the Application

1. To run the application you need to set up the data base, run the following command:

```bash
python .\database\load_schema.py
```

2. Run Flask application:
```bash
python -m flask run
```