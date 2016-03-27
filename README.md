# Kompassi Event Management System

Formerly known as Turska and ConDB. Simple web app for managing (Tra)con stuff. Work in progress.

## Getting Started

    virtualenv venv-kompassi
    source venv-kompassi/bin/activate
    git clone https://github.com/tracon/kompassi.git
    cd kompassi
    pip install -r requirements.txt
    ./manage.py setup
    ./manage.py runserver
    iexplore http://localhost:8000

`./manage.py setup --test` created a test user account `mahti` with password `mahti`.

## License

    The MIT License (MIT)

    Copyright © 2009-2016 Santtu Pajukanta
    Copyright © 2009–2015 Jussi Sorjonen
    Copyright © 2011 Petri Haikonen
    Copyright © 2012-2015 Meeri Panula
    Copyright © 2013 Esa Ollitervo
    Copyright © 2014 Pekka Wallendahl
    Copyright © 2014-2016 Jyrki Launonen
    Copyright © 2015 Miika Ojamo
    Copyright © 2015-2016 Aarni Koskela, Santeri Hiltunen

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

For third-party component licenses, see [LICENSE](https://github.com/tracon/kompassi/blob/master/LICENSE.md).
