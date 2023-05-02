# Simple Django Blog :)

## Running Django Server

- Install Python 3.11
- run `pip install pipenv`
- Download this repository
- Navigate to root and run: `pipenv install`
- Install docker desktop
- Copy `settings/.env` file to root folder
- Edit root `.env` file:
  - Change `DJANGO_SECRET_KEY` to your own phrase
  - Change `DJANGO_DB_PASSWORD` and other parameters if needed
- Copy docker files to root from settings folder
  - Change the root's `docker-compose.yml` file's `POSTGRES_PASSWORD` and other variables if needed
  - Should correspond to `.env`
- To start DB run: `pipenv run db`
- In a separate prompt
  - When starting Django for the first time run: 
    - `pipenv run migrate`
    - `pipenv run createsuperuser`
  - Start django server: `pipenv run django`
- Use `ctrl-c` to kill both server and DB container


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