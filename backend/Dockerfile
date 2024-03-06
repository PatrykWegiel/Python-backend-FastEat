FROM python:3.10-buster

WORKDIR /code
COPY . /code

RUN chmod +x *.sh
RUN ./install.sh packages && ./install.sh pip
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

