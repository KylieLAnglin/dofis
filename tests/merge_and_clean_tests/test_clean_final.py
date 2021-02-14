from dofis.merge_and_clean.library import clean_final
import pandas as pd
import numpy as np
import datetime
import pytest

test_data = pd.DataFrame()
test_data["distname"] = ["A", "B", "C"]
test_data["term_year"] = [2017, 2018, np.nan]
test_data["term_month"] = ["January", np.nan, ""]

test_data["finalize_year"] = [2018, 2019, 2019]
test_data["finalize_month"] = ["February", "September", "October"]


def test_prioritize_term_date():
    dates = clean_final.prioritize_term_date(test_data)
    dates = dates.set_index("distname")

    assert dates.loc["A"]["doi_date"] == pd.Timestamp("2017-01-01 00:00:00")
    assert dates.loc["B"]["doi_date"] == pd.Timestamp("2018-08-01 00:00:00")
    assert dates.loc["C"]["doi_date"] == pd.Timestamp("2019-10-01 00:00:00")
    assert isinstance(dates, pd.DataFrame)


def test_next_month():
    assert 2017 == clean_final.next_month(
        pd.Timestamp("2017-01-01 00:00:00"), month=3, day=1
    )
    assert 2018 == clean_final.next_month(
        pd.Timestamp("2017-03-02 00:00:00"), month=3, day=1
    )
    assert 2018 == clean_final.next_month(
        pd.Timestamp("2017-03-01 00:00:00"), month=3, day=1
    )


test_scores_df = pd.DataFrame()
test_scores_df["id"] = [1, 1, 2, 2, 1, 1, 2, 2, 3]
test_scores_df["year"] = [2013, 2014, 2013, 2014, 2013, 2014, 2013, 2014, 2014]
test_scores_df["outcome"] = [
    "math",
    "math",
    "math",
    "math",
    "reading",
    "reading",
    "reading",
    "reading",
    "reading",
]
test_scores_df["score"] = [1, 2, 2, 4, 15, 30, 25, 45, 12]
test_scores_df["meaningless_columns"] = [100, 2, 43, 5, 100, 2, 43, 5, 7]


def test_standardize_scores_within_year():

    test_scores_df["score_std"] = clean_final.standardize_scores_within_year(
        data=test_scores_df,
        score_column="score",
        year_column="year",
        test_column="outcome",
    )

    assert test_scores_df[test_scores_df.outcome == "math"].score_std.mean() == 0

    test_scores_df["score_std2"] = clean_final.standardize_scores_within_year(
        data=test_scores_df, score_column="score", year_column="year"
    )

    assert (
        test_scores_df[
            (test_scores_df.outcome == "math") & (test_scores_df.year == 2013)
        ].score_std2.mean()
        != 0
    )

    test_scores_df["score_std3"] = clean_final.standardize_scores_within_year(
        data=test_scores_df,
        score_column="score",
        year_column="year",
        test_column="outcome",
        standardization_year=2013,
    )

    assert (
        test_scores_df[
            (test_scores_df.id == 2)
            & (test_scores_df.outcome == "math")
            & (test_scores_df.year == 2014)
        ].score_std3.mean()
        == 5
    )
