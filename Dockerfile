# syntax=docker/dockerfile:1
FROM python:latest
ENTRYPOINT ["/bin/bash", "volume-pandoc/create-pandoc-script-for-files"]
#ENTRYPOINT ["tail", "-f", "/dev/null"]
