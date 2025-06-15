# Kompassi Event Management System

Formerly known as Turska and ConDB. Simple web app for managing (Tra)con stuff. Work in progress.


## Getting Started

### The Easy Way

Provided you have Docker and Docker Compose Plugin (Docker Desktop for Win/Mac provides these both), you should get up and running by simply executing

    docker compose up

Now open http://localhost:8000 in your browser. A superuser `mahti` with password `mahti` has been created for you.

When the dependencies change, you need to add `--build` to `docker compose up` to rebuild the Docker image.

On first start-up the `web` and `celery` containers may fail on start-up due to a race condition between them and the `postgres` container. To work around this, just stop all the containers by hitting `Ctrl+C` and run `docker-compose up` again.

#### Compiling internationalization files

Also on first start-up you may notice internalization is broken. This is because your working copy is bind-mounted into the container in order to facilitate code reload, and your working copy probably does not contain compiled translation files.

To fix this, and to update the translations when you change them (`django.po` files under `appname/locale`), run this in another terminal (with the app running under Docker Compose):

    docker-compose exec --user root web python manage.py kompassi_i18n -acv2

#### Running tests

    alias dc-test="docker compose -f docker-compose.test.yml up --build --abort-on-container-exit --exit-code-from test"
    dc-test

#### Running `manage.py makemigrations`

Kompassi uses the standard Django DB migration facility. However, due to the development environment running under `docker compose`, you need to hop through extra hoops to run the `manage.py makemigrations` command: namely, run it inside a container, and run it as `root` to be able to write migration files:

    docker compose exec --user=root web python manage.py makemigrations

### The Hard Way

**NOTE:** Python 3.13 or greater is required. Python 2.7 is not supported.

    python3.13 -m venv venv3-kompassi
    source venv3-kompassi/bin/activate
    git clone https://github.com/tracon/kompassi.git
    cd kompassi
    pip install -U pip setuptools wheel
    pip install -r requirements.txt
    ./manage.py setup
    ./manage.py runserver
    iexplore http://localhost:8000

`./manage.py setup --test` created a test user account `mahti` with password `mahti`.

## Docker

A Docker image is available as [tracon/kompassi](https://hub.docker.com/r/tracon/kompassi/). More info to follow.

## Kubernetes

### Cluster requirements

The following services are required:

* [kubernetes-secret-generator](https://github.com/mittwald/kubernetes-secret-generator)
* [ingress-nginx](https://github.com/kubernetes/ingress-nginx) or some other ingress controller
* [cert-manager](https://github.com/jetstack/cert-manager)

Getting these deployed (eg. Docker for Mac):

    kubernetes/setup_prerequisites.sh

The Kubernetes templates use [emrichen](https://github.com/con2/emrichen) for substituting variables and reducing repetition.

To deploy in a K8s cluster:

    kubectl create namespace kompassi
    emrichen kubernetes/template.in.yaml | kubectl apply -n kompassi -f -

For production, you may want to use an external PostgreSQL and Redis.

## Conventions

### The 8-8-8-8 Rule: Hostname, database, username, password

All the words _hostname_, _database_, _username_ and _password_ are 8 characters in length. They are often abbreviated in wildly different ways. In Kompassi we choose to always use the 8-character versions of them where we get to choose ourselves. Hence the _8-8-8-8_ rule.

| Correct | Incorrect |
|---------|-----------|
| `hostname` | `host` |
| `database` | `db`, `dbname` |
| `password` | `pass`, `passwd` |
| `username` | `user`, `login` |

## License

    The MIT License (MIT)

    Copyright © 2009–2025 Santtu Pajukanta
    Copyright © 2020–2024 Tuomas Puikkonen
    Copyright © 2019 Mikko Hänninen
    Copyright © 2018 Kalle Kivimaa
    Copyright © 2017 Tomi Simsiö
    Copyright © 2015–2017 Miika Ojamo
    Copyright © 2015–2016 Aarni Koskela, Santeri Hiltunen
    Copyright © 2014–2016 Jyrki Launonen
    Copyright © 2012–2018 Meeri Panula
    Copyright © 2009–2015 Jussi Sorjonen
    Copyright © 2014 Pekka Wallendahl
    Copyright © 2013 Esa Ollitervo
    Copyright © 2011 Petri Haikonen

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
