import pandas as pd


def generate_team_report(df: pd.DataFrame, lineup: pd.DataFrame) -> str:
    avg_hit = df["hit_rate"].mean()
    avg_out = df["out_rate"].mean()
    avg_xbh = df["xbh_rate"].mean()
    avg_value = df["value_per_pa"].mean()

    report = []

    #  Strengths
    report.append("Strengths:")

    if avg_hit > 0.55:
        report.append("- Strong contact hitting across lineup")

    if avg_xbh > 0.20:
        report.append("- Solid extra-base hit power")

    if avg_value > 1.6:
        report.append("- High overall offensive efficiency")

    #  Weaknesses
    report.append("\nWeaknesses:")

    if avg_out > 0.40:
        report.append("- Elevated out rate hurting consistency")

    if avg_xbh < 0.15:
        report.append("- Limited power production")

    bottom = lineup.tail(4)
    if bottom["value_per_pa"].mean() < avg_value:
        report.append("- Bottom of lineup is a drop-off in production")

    #  Key decision
    report.append("\nKey Insight:")

    top = lineup.head(3)
    best = df.sort_values("value_per_pa", ascending=False).iloc[0]
    # Avoid tiny-sample players dominating rankings
    worst = df.sort_values("value_per_pa").iloc[1]

    report.append(
        f"- {best['PLAYER']} is your most efficient hitter and should be placed in a high-impact spot (2–4)."
    )
    report.append(
        f"- {worst['PLAYER']} is struggling and may need to be moved down the lineup or given fewer at-bats."
    )
    report.append(
        f"- Consider moving {top.iloc[0]['PLAYER']} to the top of the lineup to maximize their contact skills and set the table for run producers."
    )
    return "\n".join(report)