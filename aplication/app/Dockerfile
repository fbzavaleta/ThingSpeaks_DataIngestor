FROM tiangolo/uwsgi-nginx-flask:python3.6

RUN apt-get update -y 

COPY  requirements.txt .
COPY  finalized_model.sav .
RUN pip3 install -r requirements.txt

WORKDIR ./app/
COPY  . .

CMD ["python", "./main.py"]
