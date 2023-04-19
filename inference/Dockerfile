FROM python:3.9

RUN mkdir /inference
WORKDIR /inference
COPY . .

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8504
ENTRYPOINT ["uvicorn", "inference:app", "--host", "0.0.0.0", "--port", "8504"]
