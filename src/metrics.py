import pandas as pd


def safe_div(numerator, denominator):
    return numerator / denominator if denominator else 0


def add_player_metrics(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()


    df["offensive_value"] = (
    df["1B"] * 1.1
    + df["2B"] * 1.8
    + df["3B"] * 2.4
    + df["HR"] * 3.0
    + df["BB"] * 0.95
    + df["ROE"] * 1.0
    + df["R"] * 0.25
    + df["RBI"] * 0.25
    - df["OUT"] * 0.5
)

    df["value_per_pa"] = df.apply(lambda r: safe_div(r["offensive_value"], r["PA"]), axis=1)

    df["hit_rate"] = df.apply(
        lambda r: safe_div(r["1B"] + r["2B"] + r["3B"] + r["HR"], r["AB"]), axis=1
    )

    df["out_rate"] = df.apply(lambda r: safe_div(r["OUT"], r["AB"]), axis=1)

    df["xbh_rate"] = df.apply(
        lambda r: safe_div(r["2B"] + r["3B"] + r["HR"], r["AB"]), axis=1
    )

    df["hr_rate"] = df.apply(lambda r: safe_div(r["HR"], r["AB"]), axis=1)

    df["run_production_per_pa"] = df.apply(
        lambda r: safe_div(r["R"] + r["RBI"], r["PA"]), axis=1
    )

    return df