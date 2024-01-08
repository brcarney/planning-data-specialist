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
