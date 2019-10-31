# Build with:
# docker build --rm -t optimizer-baskend ./
# Run with:
# docker run --rm -p 8008:8000 -v $PWD:/opt/Optimizer-backend -ti optimizer-baskend:latest
FROM python:3.6-slim-buster
COPY requirements.txt ./
RUN pip install -r requirements.txt
WORKDIR /opt/Optimizer-backend
