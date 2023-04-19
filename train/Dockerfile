FROM python:3.9

RUN mkdir /train
WORKDIR /train
COPY . .

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8503
ENTRYPOINT ["uvicorn", "train:app", "--host", "0.0.0.0", "--port", "8503"]
