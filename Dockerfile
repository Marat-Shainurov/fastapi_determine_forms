FROM python:3.11-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code

RUN chmod +x /code/run_tests.sh
RUN chmod +x /code/run_app.sh

CMD ["/code/run_tests.sh"]