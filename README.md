# Tracon ConDB

Simple web app for managing (Tra)con stuff. Work in progress.

## Getting Started

    virtualenv venv-condb
    source venv-condb/bin/activate
    git clone https://github.com/mieleton/condb.git
    cd condb
    pip install -r requirements.txt
    pip install <db_adapter> (psycopg2 or similar)
    vim condb/settings.py
    ./manage.py syncdb
    ./manage.py migrate
    ./manage.py runserver
