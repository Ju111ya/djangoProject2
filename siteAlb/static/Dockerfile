FROM python:3.10.6

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/projects/albSite

COPY ./req.txt  /usr/projects/albSite/req.txt
RUN pip install -r /usr/projects/albSite/req.txt

COPY . /usr/src/djangoProject2

EXPOSE 8000
CMD["python", "manage.py", "runserver", "0.0.0.0:8000"]