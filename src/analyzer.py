import math
from src.load_gamechanger import load_gamechanger_csv
from src.metrics import add_player_metrics
from src.archetypes import add_archetypes
from src.team_optimizer import recommend_batting_order
from src.report import generate_team_report
from src.simulator import simulate_many


def clean_for_json(value):
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return None

    if isinstance(value, dict):
        return {k: clean_for_json(v) for k, v in value.items()}

    if isinstance(value, list):
        return [clean_for_json(v) for v in value]

    return value


def prepare_team(df):
    df = add_player_metrics(df)
    df = add_archetypes(df)

    df = df[
        df["PLAYER"].notna()
        & (df["PLAYER"].astype(str).str.lower() != "nan")
        & (df["PA"] > 0)
    ]

    return df.sort_values("offensive_value", ascending=False)


def analyze_team(csv_path: str, league_name: str, league_code: str):
    raw = load_gamechanger_csv(csv_path, league=league_code)
    leaderboard = prepare_team(raw)

    batting_order = recommend_batting_order(leaderboard, lineup_size=12)
    report = generate_team_report(leaderboard, batting_order)

    lineup_names = batting_order["PLAYER"].tolist()

    simulation_lineup = (
        leaderboard[leaderboard["PLAYER"].isin(lineup_names)]
        .set_index("PLAYER")
        .loc[lineup_names]
        .reset_index()
        .to_dict(orient="records")
    )
    result = {
        "league": league_name,
    "leaderboard": leaderboard[
        [
            "PLAYER",
            "PA",
            "AB",
            "1B",
            "2B",
            "3B",
            "HR",
            "BB",
            "OUT",
            "offensive_value",
            "value_per_pa",
            "hit_rate",
            "out_rate",
            "xbh_rate",
            "hr_rate",
            "run_production_per_pa",
            "archetype",
        ]
    ].to_dict(orient="records"),
        "batting_order": batting_order.to_dict(orient="records"),
        "report": report,
        "simulation_results": simulate_many(simulation_lineup),
    }

    return clean_for_json(result)