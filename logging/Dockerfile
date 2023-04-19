FROM python:3.9

RUN mkdir /log
WORKDIR /log
COPY . .

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8505
ENTRYPOINT ["uvicorn", "logger_inference:app", "--host", "0.0.0.0", "--port", "8505"]
