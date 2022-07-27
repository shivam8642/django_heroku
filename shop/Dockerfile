FROM python:3.10.5-alpine

WORKDIR /Uers/lovet/Desktop/stripe/shop
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip 
# COPY ./requirements.txt /usr/src/app
# RUN pip install -r requirements.txt

# # copy project
# COPY . /usr/src/app

EXPOSE 8000


COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]