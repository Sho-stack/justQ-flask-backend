# Project Name

[Short project description]

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

* Python 3.x
* virtualenv (optional)

### Installation

1. Clone the repository:

>git clone https://github.com/Sho-stack/justQ-flask-backend-.git

>cd project-name

2. Create and activate a virtual environment (optional):

On Windows:

> python -m venv venv

> venv\Scripts\activate

On Unix/MacOS:

>python3 -m venv venv

>source venv/bin/activate


3. Install the dependencies:

>pip install -r requirements.txt

4. Set up the database:

>python manage.py db_init

>python manage.py db_migrate

>python manage.py db_upgrade

### Usage

Run the application:

>flask run

You can now access the application at [http://localhost:5000/](http://localhost:5000/).

