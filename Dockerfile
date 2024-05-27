# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /usr/src/app

# Install dependencies
COPY requirements.txt /usr/src/app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY . /usr/src/app/

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose the port the app runs on
EXPOSE 8666

# Run the application
CMD ["gunicorn", "project_name.wsgi:application", "--bind", "0.0.0.0:8000"]
