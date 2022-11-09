# syntax=docker/dockerfile:1
FROM python:latest
RUN mkdir /volume
ENTRYPOINT ["/bin/bash", "volume/create-pandoc-script-for-files"]
#ENTRYPOINT ["tail", "-f", "/dev/null"]
