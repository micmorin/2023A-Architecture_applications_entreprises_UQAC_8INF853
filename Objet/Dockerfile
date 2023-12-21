FROM python:3-slim
WORKDIR /app

RUN python -m pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8000
CMD [ "python", "run.py"]