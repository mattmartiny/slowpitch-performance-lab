import pandas as pd


def assign_batting_role(row):
    if row["value_per_pa"] >= 1.8 and row["xbh_rate"] >= 0.25:
        return "Middle-order run producer"

    if row["hit_rate"] >= 0.600 and row["out_rate"] <= 0.350:
        return "Table setter"

    if row["xbh_rate"] >= 0.200:
        return "Power bat"

    if row["out_rate"] <= 0.350:
        return "Contact bat"

    return "Bottom-order depth"


def recommend_batting_order(df: pd.DataFrame, lineup_size: int = 12) -> pd.DataFrame:
    eligible = df[df["PA"] >= 10].copy()

    eligible["batting_role"] = eligible.apply(assign_batting_role, axis=1)

    table_setters = eligible.sort_values(
        ["hit_rate", "value_per_pa"], ascending=False
    ).head(2)

    remaining = eligible[~eligible["player_key"].isin(table_setters["player_key"])]

    run_producers = remaining.sort_values(
        ["run_production_per_pa", "value_per_pa", "xbh_rate"],
        ascending=False,
    ).head(3)

    remaining = remaining[~remaining["player_key"].isin(run_producers["player_key"])]

    rest = remaining.sort_values(
        ["value_per_pa", "hit_rate", "out_rate"],
        ascending=[False, False, True],
    )

    lineup = pd.concat([table_setters, run_producers, rest]).head(lineup_size).copy()
    lineup["batting_order"] = range(1, len(lineup) + 1)

    return lineup[
        [
            "batting_order",
            "PLAYER",
            "PA",
            "offensive_value",
            "value_per_pa",
            "hit_rate",
            "out_rate",
            "xbh_rate",
            "run_production_per_pa",
            "archetype",
            "batting_role",
        ]
    ]