# syntax=docker/dockerfile:1
FROM python:latest
RUN mkdir /web-content
ENTRYPOINT ["tail", "-f", "/dev/null"]
