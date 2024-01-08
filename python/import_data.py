import pandas as pd
import numpy as np
import re
from sqlalchemy import create_engine
from settings import pg_pw

ENGINE = create_engine(
    "postgresql://bcarney:{}@postgres.dvrpc.org:5432/bcarney".format(pg_pw)
)


CRASH_SUM_URL = "https://catalog.dvrpc.org/dataset/916c9fc4-c0c9-4d70-98f6-bd7f76e594b1/resource/ce75c010-3a79-4a67-b7b6-0e16fb83edaf/download/crash_summary_08_20.csv"
POP_URL = "https://catalog.dvrpc.org/dataset/8f75dffc-69d0-4e20-899b-271cf4ff9095/resource/d62075e7-6141-4dd4-9f23-02ffa9c4d43c/download/mcdpopforecast2050.1.csv"


YEARS = [2015, 2020]

APPENDED_DATA = []


def crash_pop_join(year: int):
    for year in YEARS:
        x = pd.read_csv(CRASH_SUM_URL, usecols=["GEOID10", "Crash Year", "TOTAL CRASH"])
        x = x.loc[x["Crash Year"] == year]
        y = pd.read_csv(
            POP_URL,
            usecols=[
                "mun_dist_id",
                "county",
                "municipality_district",
                "pop_{}".format(year),
            ],
        )
        y["pop_{}".format(year)] = y["pop_{}".format(year)].str.replace(
            ",", "", regex=True
        )
        y["pop_{}".format(year)] = pd.to_numeric(
            y["pop_{}".format(year)], errors="raise"
        )
        CRASH_POP_DF = pd.merge(y, x, left_on="mun_dist_id", right_on="GEOID10")
        CRASH_POP_DF["crashes_per_cap"] = round(
            CRASH_POP_DF["TOTAL CRASH"] / (CRASH_POP_DF["pop_{}".format(year)]), 3
        )
        CRASH_POP_DF.to_csv(
            "G:/My Drive/PlanningDataSpecialist/data-outputs/crashes_per_capita_{}.csv".format(
                year
            )
        )
        APPENDED_DATA.append(CRASH_POP_DF)


crash_pop_join(YEARS)
CRASH_POP_APPEND_DF = pd.concat(APPENDED_DATA)
