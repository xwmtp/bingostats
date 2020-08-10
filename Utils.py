import datetime as dt
import pandas as pd
import math
import csv
import json
import requests
import logging


def readjson(url, text_only=False, tries=5):

    for i in range(tries):
        response = requests.get(url)
        status = response.status_code

        if status == 200:
            if text_only:
                return response.text
            else:
                return response.json()
        if status == 404:
            return

    logging.error("Error in accessing api:", status, "(after", tries, "tries)")


def readjson_file(file):
    return json.load(open(file))


def convert_to_dict(name, to_lower=False):
    dict = {}
    with open('./data/' + name, 'r+') as file:
        reader = csv.reader(file, delimiter=';')
        for row in reader:
            if row[1] == "-":
                row[1] = row[0]
            key = row[0]
            val = row[1]
            if to_lower:
                key = key.lower()
                val = val.lower()
            dict[key] = val
    return dict


def list_to_df(list):
    df = pd.DataFrame(columns=["time", "type", "seed", "row", "comment", "player"])
    i = 0
    for obj in list:
        df.loc[i] = pd.Series({"time" : obj.time, "type" : obj.type, "seed" : obj.seed, "row" : obj.row, "comment" : obj.comment, "player" : obj.player})
        i = i + 1


def extract_attr(races, attr, seconds = False):
        if attr == "time" and seconds:
            return [race.time.total_seconds() for race in races]
        else:
            return [getattr(race, attr) for race in races]



def convert_to_human_readable_time(time):

    h = int(math.floor(time / 3600))
    time = time % 3600
    m = int(math.floor(time / 60))
    s = int(time % 60)
    human_readable_time =  str(h) + ":" + str(m).zfill(2) + ":" + str(s).zfill(2)

    new_time = "2018-05-28 " + human_readable_time

    return new_time, human_readable_time

def parse_date(date_str):
    return dt.datetime.strptime(date_str, '%d-%m-%Y').date()



class Range:

    def __init__(self, start, end=None):
        from_year, from_month = self._extract_year_month(start)
        if end == None:
            to_year, to_month = from_year, from_month
        else:
            to_year, to_month = self._extract_year_month(end)

        self.start = dt.date(from_year + 2000, from_month, 1)
        self.end   = dt.date(to_year   + 2000, to_month, 27)
        if self.start > self.end:
            raise ValueError("Start date should not exceed end date.")

    def _extract_year_month(self, str):
        dates = []
        for symbol in ['-', "_", '.']:
            if symbol in str:
                dates = str.split(symbol)
                break
        if not dates:
            if len(str) == 4:
                dates = [str[:2], str[2:4]]
            else:
                raise ValueError("Supply a year and month in the form 'YY-MM'.")

        dates = sorted([int(x) for x in dates])
        if dates[1] > 2000:
            dates[1] = dates - 2000
        year, month = dates[1], dates[0]
        if year < month or year < 13 or year > 19 or month < 1 or month > 12:
            raise ValueError("Supply a year and month in the form 'YY-MM'.")
        return year, month
