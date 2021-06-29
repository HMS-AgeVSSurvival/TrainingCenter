import pandas as pd
import numpy as np


if __name__ == "__main__":
    heart_size = pd.read_csv("data/heart/HeartSize.csv").dropna().set_index("eid")
    folds = pd.read_csv("data/heart/All_eids.csv").set_index("eid")

    heart_size["fold"] = folds
    heart_size.set_index("id", inplace=True)
    demographics = pd.read_csv("data/heart/Demographics.csv").drop(columns=["eid"]).set_index("id")

    heart_size[demographics.columns] = demographics

    heart_size[["mortstat", "follow_up_time", "survival_type_alive", "survival_type_cancer","survival_type_cvd", "survival_type_other"]] = np.nan
    heart_size.reset_index().rename(columns={"id": "SEQN", "Age when attended assessment centre": "RIDAGEEX_extended; Best age in months at date of examination for individuals under 85 years of age at screening."}).to_feather("data/heart/HeartSize.feather")