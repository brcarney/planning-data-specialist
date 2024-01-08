import pandas as pd
import numpy as np
from scipy import stats
from import_data import CRASH_POP_APPEND_DF, YEARS


def summary_stats(year: int):
    for year in YEARS:
        summary = CRASH_POP_APPEND_DF.loc[CRASH_POP_APPEND_DF["Crash Year"] == year]
        x = summary.agg(
            {
                "crashes_per_cap": ["mean", "median", "std"],
                "TOTAL CRASH": ["mean", "median", "std"],
            }
        )
        print(x)
        x.to_csv(
            "G:/My Drive/PlanningDataSpecialist/data-outputs/mcd_pd_summary_stats_{}.csv".format(
                year
            )
        )


summary_stats(YEARS)


def summary_stats_counties(year: int):
    for year in YEARS:
        summary = CRASH_POP_APPEND_DF.loc[CRASH_POP_APPEND_DF["Crash Year"] == year]
        x = summary.groupby("county").agg(
            {
                "crashes_per_cap": ["mean", "median", "std"],
                "TOTAL CRASH": ["sum", "mean", "median", "std"],
            }
        )
        x.to_csv(
            "G:/My Drive/PlanningDataSpecialist/data-outputs/county_summary_stats_{}.csv".format(
                year
            )
        )
        print(x)


summary_stats_counties(YEARS)


def pop_buckets(year: int):
    for year in YEARS:
        pct_10_df = CRASH_POP_APPEND_DF.loc[CRASH_POP_APPEND_DF["Crash Year"] == year]
        pct_10 = round(pct_10_df["pop_{}".format(year)].quantile(q=0.10), 1)
        print("The 10th percentile for population in {} is {}".format(year, pct_10))


pop_buckets(YEARS)

"""
def outlier_detection(year: int):
    df = CRASH_POP_APPEND_DF.loc[CRASH_POP_APPEND_DF["Crash Year"] == year]
    q1 = df["pop_{}".format(year)].quantile(0.25)
    q3 = df["pop_{}".format(year)].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - (1.5 * iqr)
    upper = q3 + (1.5 * iqr)
    upper_array = np.where(df["pop_{}".format(year)] >= upper)[0]
    lower_array = np.where(df["pop_{}".format(year)] <= lower)[0]
    df.drop(index=upper_array, inplace=True)
    df.drop(index=lower_array, inplace=True)
    high = df.loc[df["pop_{}".format(year)] >= upper]
    print(upper_array)
"""

APPENDED_DATA = []


def drop_outliers(year: int):
    for year in YEARS:
        df = CRASH_POP_APPEND_DF.loc[
            CRASH_POP_APPEND_DF["Crash Year".format(year)] == year
        ]
        print(len(df))
        z = np.abs(stats.zscore(df["crashes_per_cap"]))
        outliers = np.array(np.where(z > 3)[0])
        print(outliers)
        df.drop(index=outliers, inplace=True)
        no_outlier_df = pd.DataFrame(df)
        no_outlier_df.to_csv(
            "G:/My Drive/PlanningDataSpecialist/data-outputs/mcd_pd_crash_summary_{}_no_outliers.csv".format(
                year
            )
        )
        APPENDED_DATA.append(no_outlier_df)


drop_outliers(YEARS)
OUTLIER_APPEND_DF = pd.concat(APPENDED_DATA)
