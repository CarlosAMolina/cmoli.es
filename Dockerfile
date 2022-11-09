# syntax=docker/dockerfile:1
FROM python:latest
RUN mkdir /volume
ENTRYPOINT ["/bin/bash", "volume/create-pandoc-script"]
#ENTRYPOINT ["tail", "-f", "/dev/null"]
