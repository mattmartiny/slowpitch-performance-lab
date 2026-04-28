from load_gamechanger import load_gamechanger_csv
from metrics import add_player_metrics
from archetypes import add_archetypes
from team_optimizer import recommend_batting_order
from report import generate_team_report
from pretty_print import print_top_players, print_batting_order
from charts import plot_value_vs_hit_rate
from analyzer import analyze_team

print("\n Slowpitch Performance Lab\n")


def prepare_team(df):
    df = add_player_metrics(df)
    df = add_archetypes(df)
    return df.sort_values("value_per_pa", ascending=False)

def print_report(result):
    print(f"\n==============================")
    print(f"{result['league']} TEAM REPORT")
    print("==============================")

    print("\nTOP PLAYERS")
    for i, row in enumerate(result["leaderboard"][:12], start=1):
        print(
            f"{i}. {row['PLAYER']} — "
            f"OV: {row['offensive_value']:.1f} | "
            f"OV/PA: {row['value_per_pa']:.2f} | "
            f"Archetype: {row['archetype']}"
        )

    print("\nRECOMMENDED BATTING ORDER")
    for row in result["batting_order"]:
        print(
            f"{row['batting_order']}. {row['PLAYER']} — "
            f"{row['batting_role']} "
            f"(OV/PA: {row['value_per_pa']:.2f})"
        )

    print("\nTEAM ANALYSIS")
    print(result["report"])


def main():
    monday = analyze_team("data/raw/monday.csv", "MONDAY", "MON")
    friday = analyze_team("data/raw/friday.csv", "FRIDAY", "FRI")

    print_report(monday)
    print_report(friday)


if __name__ == "__main__":
    main()