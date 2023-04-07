FROM python:3.11-alpine

# Set the working directory
WORKDIR /dockertest

# Install pipenv
RUN pip install --upgrade pip pipenv

# Copy the Pipfile and Pipfile.lock
COPY Pipfile* .

# Install the dependencies
RUN pipenv install --deploy

# Copy the rest of the code
COPY dockertest/ .

RUN ls /

# Collect the static files
# RUN pipenv run ./dockertest/manage.py collectstatic --noinput

# Run the command to start the server
# CMD ["pipenv", "run", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["inf_loop.py"]
