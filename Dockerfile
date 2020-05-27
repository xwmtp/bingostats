FROM python:3.8-slim-buster

COPY ./ /etc/BingoStats

RUN pip install dash dash_core_components pandas requests

VOLUME ["/etc/BingoStats/logs"]

EXPOSE 80

WORKDIR /etc/BingoStats
CMD ["python", "Main.py"]