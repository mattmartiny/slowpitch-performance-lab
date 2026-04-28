from load_gamechanger import load_gamechanger_csv
from metrics import add_player_metrics
from archetypes import add_archetypes
from team_optimizer import recommend_batting_order
from report import generate_team_report
from pretty_print import print_top_players, print_batting_order
from charts import plot_value_vs_hit_rate


print("\n Slowpitch Performance Lab\n")


def prepare_team(df):
    df = add_player_metrics(df)
    df = add_archetypes(df)
    return df.sort_values("offensive_value", ascending=False)


def print_team_report(df, league_name):
    leaderboard = prepare_team(df)
    batting_order = recommend_batting_order(leaderboard, lineup_size=12)

    report = generate_team_report(leaderboard, batting_order)

    print("\n==============================")
    print(f" {league_name} TEAM REPORT")
    print("==============================")

    print_top_players(leaderboard, n=12)
    print_batting_order(batting_order)

    print("\n TEAM ANALYSIS")
    print(report)
    plot_value_vs_hit_rate(leaderboard, league_name)

def main():
    monday = load_gamechanger_csv("data/raw/monday.csv", league="MON")
    friday = load_gamechanger_csv("data/raw/friday.csv", league="FRI")

    print_team_report(monday, "MONDAY")
    print_team_report(friday, "FRIDAY")
    

if __name__ == "__main__":
    main()