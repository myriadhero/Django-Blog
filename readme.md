# Simple Django Blog :)

This started out as a blog concept, but is now slowly growing into an entertainment/pop-culture site.

## Running Django Server in Dev

- Install [Python 3.11](https://www.python.org/downloads/)
- Run `pip install pipenv`
- Download this repository
- Navigate to root and run: `pipenv sync --dev` _or_ `pipenv install --dev` (the latter may install updated packages that could differ from current prod)
- Install [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Copy `example_settings/.env` file to root folder
- Edit root `.env` file:
  - Change `DJANGO_SECRET_KEY` to your own phrase
  - Change `POSTGRES_DB_PASSWORD` 
  - Change other parameters if needed
- To start dev DB docker container run: `pipenv run devdb`
- In a separate prompt
  - When starting Django for the first time run: 
    - `pipenv run migrate`
    - `pipenv run createsuperuser`
  - Start django server: `pipenv run django`
- Go to http://localhost/admin and have a look around :)
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
- [Black Formatter](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter) from Microsoft - python code formatter 👍
- [isort](https://marketplace.visualstudio.com/items?itemName=ms-python.isort) from Microsoft - sorts the imports at the top of the .py files
- [djLint](https://marketplace.visualstudio.com/items?itemName=monosans.djlint) from monosans - code formatter for Django HTML templates
- [Django](https://marketplace.visualstudio.com/items?itemName=batisteo.vscode-django) snippets and syntax from Baptiste Darthenay
- [Prettier - Code formatter](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode) from Prettier

Probably, for collab, I would recommend having all of the above installed.

Black, isort, djLint, and Prettier are activated in VScode by going into Preferences, `Open User Settings (JSON)` and adding this to the config:
```json
"[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter",
    "editor.formatOnSave": true,
    "editor.formatOnType": true,
    "editor.codeActionsOnSave": {
      "source.organizeImports": true
    }
  },
  "isort.args": ["--profile", "black"],
  "[javascript][scss][css]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[django-html][handlebars][hbs][mustache][jinja][jinja-html][nj][njk][nunjucks][twig]": {
    "editor.defaultFormatter": "monosans.djlint"
  },
  "djlint.useVenv": false,
  "djlint.pythonPath": "C:\\Users\\Kirill\\.local\\pipx\\venvs\\djlint\\Scripts\\python",
  "emmet.includeLanguages": {
    "django-html": "html"
  },
```

Also chatgpt and github copilot are great 👍

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
- Run `docker compose --profile prod exec web python manage.py createsuperuser --noinput --username <yourUsername> --password <yourPass>`

It should be good to go!💃

___


### Packages and programs used in this project:

- [Python 🐍](https://www.python.org/downloads/)
- [Pipenv](https://pipenv.pypa.io/en/latest/)
- [Docker](https://www.docker.com/products/docker-desktop/)
- [Psycopg 3](https://www.psycopg.org/psycopg3/docs/) and [PostgreSQL](https://www.postgresql.org/) (via docker)
- [Gunicorn](https://gunicorn.org/)
- [Django](https://www.djangoproject.com/)
- [Django-ckeditor](https://django-ckeditor.readthedocs.io/en/latest/)
- [Django-taggit](https://django-taggit.readthedocs.io/en/latest/)
- [Django Debug Toolbar](https://github.com/jazzband/django-debug-toolbar)
- [Django-imagekit](https://django-imagekit.readthedocs.io/en/latest/) and [Pillow](https://pypi.org/project/Pillow/)
- [Django-Select2](https://django-select2.readthedocs.io/en/latest/)
- [Django-Meta](https://github.com/nephila/django-meta)
- [Crispy Forms](https://django-crispy-forms.readthedocs.io/en/latest/)
- [Crispy Bulma](https://crispy-bulma.readthedocs.io/en/latest/)
- [HTMX](https://htmx.org/)
- [Bulma CSS](https://bulma.io/)
- [Swiper Carousel](https://swiperjs.com/)
- [lxml](https://lxml.de/)
- [Font Awesome](https://fontawesome.com/docs/web/use-with/python-django)