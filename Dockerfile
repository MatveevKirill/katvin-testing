FROM python:3.9

COPY source /source
COPY requirements.txt requirements.txt

RUN python3.9 -m pip install -r requirements.txt

WORKDIR /source

CMD ["python3.9", "pytest -v -s --alluredir=tmp/allure-report"]
CMD ["allure serve tmp/allure-report"]