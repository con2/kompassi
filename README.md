# Turska, the Tracon Convention Management System

Simple web app for managing (Tra)con stuff. Work in progress.

## Getting Started

    virtualenv venv-turska
    source venv-turska/bin/activate
    git clone https://github.com/mieleton/turska.git
    cd turska
    pip install -r requirements.txt
    ./manage.py setup --test
    ./manage.py runserver
    iexplore http://localhost:8000

`./manage.py setup_core --test` created a test user account `mahti` with password `mahti`.

## Important terms

**Signup Extra** - A signup extra model is a ...

**Event Meta** - An event meta model is a ...

## Running tests

    bundle install
    ./manage.py runserver
    bundle exec rake cucumber

## Developing on Windows - Caveats

It is mostly possible to develop Turska on Microsoft(R) Windows(R) (tested: 8.1, 7). GitHub for Windows is recommended. The Getting Started procedure in Git Shell (PowerShell) is as follows:

    virtualenv venv-turska
    venv-turska\Scripts\activate.ps1
    git clone https://github.com/mieleton/turska.git
    cd turska
    pip install -r requirements.txt
    python manage.py setup --test
    python manage.py runserver
    iexplore http://localhost:8000

**Caveat:** Anything that uses `datetime.strftime` instead of the Django date formatting stuff will show stuff in UTC instead of the intended time zone. This includes `labour.WorkPeriod.__unicode__` which is shown to users in some places. Wontfix, as Windows is only supported as a development platform - all production deployments should run Linux.