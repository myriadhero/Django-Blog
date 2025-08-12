# Simple Django Blog :)

This started out as a blog concept, but is now slowly growing into an entertainment/pop-culture site.

## Running Django Server in Dev

- Download this repository
- Install [uv](https://docs.astral.sh/uv/getting-started/installation/)
- Navigate to root and run: `uv sync`
- Install [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Copy `example_settings/.env` file to root folder
- Edit root `.env` file:
  - Change `DJANGO_SECRET_KEY` to your own phrase
  - Change `POSTGRES_DB_PASSWORD` 
  - Change other parameters if needed
- To start dev DB docker container run: `docker compose -profile dev up`
- In a separate prompt
  - When starting Django for the first time run: 
    - `uv run backend/manage.py migrate`
    - `uv run backend/manage.py createsuperuser`
  - Start django server: `uv run backend/manage.py runserver`
- Go to http://localhost:8000/admin and have a look around :)
- Use `ctrl-c` to kill server and DB container

### Project structure

`backend/` folder contains Django and actually almost everything needed to run the server.

`frontend/` folder is a stub for if we ever need a more advanced standalone front end (like react), but for now it's mostly empty and is only used to optionally build some CSS. [NPM](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) is used build CSS/frontend.

Despite there being frontend folder which is responsible for building some CSS, the actual HTML Django templates are kept with the rest of Django in `backend/templates/` folder. CSS built in the frontend folder is also stored in `backend/static/css` folder for convenience of serving it. In the future i may want to make it a step in the docker build process instead.

Site settings and base urls live in `backend/blogsite/` - i didn't know to name it better at the time... 😅

Most of the site's logic lives in `backend/blog/` and some general site identity stuff in `backend/core/`.

Root folder contains docker, utils, and config files that build and run the server. `nginx` server is used in prod.

### Helpful tools for dev env

I use VScode with various extensions:
- Microsoft Python extensions that VScode should prompt you to install whenever opening a .py file
- [Ruff Formatter](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff)
- [djLint](https://marketplace.visualstudio.com/items?itemName=monosans.djlint) from monosans - code formatter for Django HTML templates
- [Django](https://marketplace.visualstudio.com/items?itemName=batisteo.vscode-django) snippets and syntax from Baptiste Darthenay
- [Prettier - Code formatter](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode) from Prettier

And also [iPython](https://ipython.org/) for python shell exploration stuff.

## Deploying in prod 
`(⚠may be out of date as of 17/11/2023)`

This app is deployed on a private virtual server - Ubuntu 22.04.
It is located behind another network proxy and CloudFlare,
so it only has to handle https requests on a specified port (8080).
Everything else (like redirect to https) is handled elsewhere and is locked down.

- Install Docker engine - https://docs.docker.com/engine/install/ubuntu/
  - Useful script/info in `utils/dockerinstall.sh`
  - Install rootless optionally - https://docs.docker.com/engine/security/rootless/
- Download the repo
- Copy `example_settings/.env` file to root folder, and change config for prod
- Copy `example_settings/default.conf` to `nginx/` folder
  - Change mysite.com occurences to your domain
- Create self-signed or get a trusted SSL certificate with key and put into `nginx/` folder
  - Useful script in `utils/selfsignedcert.sh`
- Run `docker compose --profile prod up -d` to build and run containers
- Run `docker compose --profile prod exec web python manage.py migrate --noinput`
- Run `docker compose --profile prod exec web python manage.py collectstatic --noinput`
- Run (optional) `docker compose --profile prod exec web python manage.py process_imagefields --no-parallel --all`
- Run `docker compose --profile prod exec web python manage.py createsuperuser --noinput --username <yourUsername> --password <yourPass>`

It should be good to go!💃

___


### Packages used in this project:

- [Python 🐍](https://www.python.org/downloads/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [Docker](https://www.docker.com/products/docker-desktop/)
- [Psycopg 3](https://www.psycopg.org/psycopg3/docs/) and [PostgreSQL](https://www.postgresql.org/) (via docker)
- [Gunicorn](https://gunicorn.org/)
- [Django](https://www.djangoproject.com/)
- [Django-taggit](https://django-taggit.readthedocs.io/en/latest/)
- [Django Debug Toolbar](https://github.com/jazzband/django-debug-toolbar)
- [Django-Select2](https://django-select2.readthedocs.io/en/latest/)
- [Django-Meta](https://github.com/nephila/django-meta)
- [Crispy Forms](https://django-crispy-forms.readthedocs.io/en/latest/)
- [Crispy Bulma](https://crispy-bulma.readthedocs.io/en/latest/)
- [HTMX](https://htmx.org/)
- [Bulma CSS](https://bulma.io/)
- [Swiper Carousel](https://swiperjs.com/)
- [lxml](https://lxml.de/)
- [Font Awesome](https://fontawesome.com/docs/web/use-with/python-django)
- [Cropper.js v1](https://github.com/fengyuanchen/cropperjs/blob/v1/README.md)
- [Django-imagefield](https://github.com/matthiask/django-imagefield/)
- [Django-ckeditor-5](https://github.com/hvlads/django-ckeditor-5)
