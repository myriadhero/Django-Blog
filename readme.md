# Simple Django Blog :)

## Running Django Server in Dev:

- Install Python 3.11
- run `pip install pipenv`
- Download this repository
- Navigate to root and run: `pipenv sync` or `pipenv install` (the latter may install updated packages)
- Install docker desktop
- Copy `example_settings/.env` file to root folder
- Edit root `.env` file:
  - Change `DJANGO_SECRET_KEY` to your own phrase
  - Change `DJANGO_DB_PASSWORD` and other parameters if needed
  - Change others as required, especially Allowed hosts and Debug for prod deploy
- Change the root's `docker-compose.yml` file's `POSTGRES_PASSWORD` and other variables if needed
- Should correspond to `.env`
- To start DB run: `pipenv run devdb`
- In a separate prompt
  - When starting Django for the first time run: 
    - `pipenv run migrate`
    - `pipenv run createsuperuser`
  - Start django server: `pipenv run django`
- Use `ctrl-c` to kill both server and DB container

## Deploying in prod

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
- [Django](https://www.djangoproject.com/)
- [Django-ckeditor](https://django-ckeditor.readthedocs.io/en/latest/)
- [Django-taggit](https://django-taggit.readthedocs.io/en/latest/)
- [Django-imagekit](https://django-imagekit.readthedocs.io/en/latest/)
- [HTMX](https://htmx.org/)
- [Bulma CSS](https://bulma.io/)
- [Swiper Carousel](https://swiperjs.com/)
- [lxml](https://lxml.de/)
- [Pipenv](https://pipenv.pypa.io/en/latest/)
- [Docker](https://www.docker.com/products/docker-desktop/)
- [Font Awesome](https://fontawesome.com/docs/web/use-with/python-django)
- [Crispy Forms](https://django-crispy-forms.readthedocs.io/en/latest/)
- [Crispy Bulma](https://crispy-bulma.readthedocs.io/en/latest/)