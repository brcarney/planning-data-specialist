import pandas as pd
import numpy as np
import re
from sqlalchemy import create_engine
from settings import pg_pw

engine = create_engine(
    "postgresql://bcarney:{}@postgres.dvrpc.org:5432/bcarney".format(pg_pw)
)


CRASH_SUM_URL = "https://catalog.dvrpc.org/dataset/916c9fc4-c0c9-4d70-98f6-bd7f76e594b1/resource/ce75c010-3a79-4a67-b7b6-0e16fb83edaf/download/crash_summary_08_20.csv"
POP_URL = "https://catalog.dvrpc.org/dataset/8f75dffc-69d0-4e20-899b-271cf4ff9095/resource/d62075e7-6141-4dd4-9f23-02ffa9c4d43c/download/mcdpopforecast2050.1.csv"


years = [2015, 2020]


def crash_years_summary(year):
    for year in years:
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
        crash_pop_df = pd.merge(y, x, left_on="mun_dist_id", right_on="GEOID10")
        crash_pop_df["crashes_per_cap"] = round(
            crash_pop_df["TOTAL CRASH"] / (crash_pop_df["pop_{}".format(year)]), 3
        )
        crash_pop_df.to_csv(
            "G:/My Drive/PlanningDataSpecialist/data-outputs/crashes_per_capita_{}.csv".format(
                year
            )
        )


crash_years_summary(years)

"""crash_pop_df["crashes_per_cap"] = round(
            crash_pop_df["TOTAL CRASH"] / (crash_pop_df["pop_{}".format(year)]), 3
        )"""

CRASH_SUMMARY = pd.read_csv(
    CRASH_SUM_URL,
    usecols=["GEOID10", "Crash Year", "TOTAL CRASH"],
)

CRASH_SUMMARY = CRASH_SUMMARY.loc[
    (CRASH_SUMMARY["Crash Year"] == 2015) | (CRASH_SUMMARY["Crash Year"] == 2020)
]

# CRASH_SUMMARY.to_sql("crash_summary", engine, schema="oss", if_exists="replace")


POP = pd.read_csv(
    POP_URL,
    usecols=["mun_dist_id", "county", "municipality_district", "pop_2015", "pop_2020"],
)

# Join Population and Crash Data
CRASH_POP_JOIN = pd.merge(POP, CRASH_SUMMARY, left_on="mun_dist_id", right_on="GEOID10")

"""
crash_pop_df["crashes_per_cap"] = round(
            crash_pop_df["TOTAL CRASH"] / (crash_pop_df["pop_{}".format(year)]), 3
        )
        """
