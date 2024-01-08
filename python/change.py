import pandas as pd
from import_data import CRASH_POP_APPEND_DF


def pct_chg(fyear: int, lyear: int):
    fyear_df = CRASH_POP_APPEND_DF.loc[CRASH_POP_APPEND_DF["Crash Year"] == fyear]
    fyear_df = fyear_df[
        ["GEOID10", "municipality_district", "TOTAL CRASH", "crashes_per_cap"]
    ]
    lyear_df = CRASH_POP_APPEND_DF.loc[CRASH_POP_APPEND_DF["Crash Year"] == lyear]
    lyear_df = lyear_df[
        ["GEOID10", "municipality_district", "TOTAL CRASH", "crashes_per_cap"]
    ]
    combined_df = pd.merge(
        fyear_df,
        lyear_df,
        on=["GEOID10", "municipality_district"],
        suffixes=("_{}".format(fyear), "_{}".format(lyear)),
    )
    combined_df["crashes_per_cap_chg"] = round(
        (
            combined_df["crashes_per_cap_{}".format(lyear)]
            - combined_df["crashes_per_cap_{}".format(fyear)]
        )
        / combined_df["crashes_per_cap_{}".format(fyear)],
        3,
    )
    combined_df["TOTAL_CRASH_CHG"] = (
        combined_df["TOTAL CRASH_{}".format(lyear)]
        - combined_df["TOTAL CRASH_{}".format(fyear)]
    )
    print(combined_df)
    combined_df.to_csv(
        "G:/My Drive/PlanningDataSpecialist/data-outputs/crash_summary_chg_{}_to_{}.csv".format(
            fyear, lyear
        )
    )


pct_chg(2015, 2020)
