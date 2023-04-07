# Simple Django Blog :)

## Running Django Server

- Install Python 3.11
- run `pip install pipenv`
- Download this repository
- Navigate to root and run: `pipenv install`
- Install docker desktop
- Copy `settings/blogsite/settings.py` file to `backend/blogsite/` folder
- Edit `backend/blogsite/settings.py` file:
  - Change `SECRET_KEY` to your own phrase
  - Change `DATABASES` - `PASSWORD` and other parameters if needed
- Copy docker files to root from settings folder
  - Change the root's `docker-compose.yml` file's `POSTGRES_PASSWORD` and other variables if needed
  - Should correspond to `backend/blogsite/settings.py`
- To start DB run: `pipenv run db`
- When starting Django for the first time run: `pipenv run migrate`
- In a separate prompt start django server: `pipenv run django`
- Use `ctrl-c` to kill it


