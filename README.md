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

## License

    The MIT License (MIT)

    Copyright (c) 2009-2014 Santtu Pajukanta, Jussi Sorjonen
    Copyright (c) 2011 Petri Haikonen
    Copyright (c) 2012-2014 Meeri Panula
    Copyright (c) 2014 Jyrki Launonen, Pekka Wallendahl

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.
