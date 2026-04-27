import pandas as pd


def recommend_top_lineup(df: pd.DataFrame, lineup_size: int = 4) -> pd.DataFrame:
    """
    Recommends the best lineup based on value per PA.
    """
    eligible = df.copy()

    # Avoid tiny-sample players dominating rankings
    eligible = eligible[eligible["PA"] >= 10]

    lineup = (
        eligible
        .sort_values(["value_per_pa", "offensive_value"], ascending=False)
        .head(lineup_size)
        .copy()
    )

    lineup["recommendation_rank"] = range(1, len(lineup) + 1)

    return lineup[
        [
            "recommendation_rank",
            "PLAYER",
            "PA",
            "offensive_value",
            "value_per_pa",
            "hit_rate",
            "out_rate",
            "xbh_rate",
            "archetype",
        ]
    ]