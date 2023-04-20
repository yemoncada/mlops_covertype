FROM python:3.9

RUN mkdir /dataset
WORKDIR /dataset
COPY . .

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8502
ENTRYPOINT ["uvicorn", "load_data:app", "--host", "0.0.0.0", "--port", "8502"]

