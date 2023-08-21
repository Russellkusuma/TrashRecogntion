FROM python:3.11-slim-bullseye
RUN pip install --upgrade pip
COPY ./app.py /deploy/
COPY ./requirements.txt /deploy/
COPY ./ResNetPT_April17_TS_Compost_CPU.pt /deploy/
WORKDIR /deploy/
RUN pip install -r requirements.txt
EXPOSE 80
ENTRYPOINT ["python", "app.py"]