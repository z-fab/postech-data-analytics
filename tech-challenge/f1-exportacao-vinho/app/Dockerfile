# app/Dockerfile

FROM python:3.9-slim

EXPOSE 8501

WORKDIR /app

COPY . .

RUN apt-get update
RUN pip3 install -U pip setuptools wheel
RUN pip3 install -r requirements.txt


ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.enableCORS=false", "--server.enableXsrfProtection=false", "--server.baseUrlPath=tc-f1", "--theme.primaryColor=#794A9E"]