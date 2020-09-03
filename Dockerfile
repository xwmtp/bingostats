FROM python:3.8-slim-buster

RUN pip install dash dash_core_components pandas requests isodate

VOLUME ["/etc/BingoStats/logs", "/etc/BingoStats/BingoBoards/Versions"]

EXPOSE 80

COPY ./ /etc/BingoStats

WORKDIR /etc/BingoStats
CMD ["python", "Main.py", "0.0.0.0", "False"]
