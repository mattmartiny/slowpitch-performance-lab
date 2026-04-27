import pandas as pd


def generate_team_report(df: pd.DataFrame, lineup: pd.DataFrame) -> str:
    avg_hit = df["hit_rate"].mean()
    avg_out = df["out_rate"].mean()
    avg_xbh = df["xbh_rate"].mean()
    avg_pts = df["value_per_pa"].mean()

    report = []

    # 🔥 Strengths
    report.append("Strengths:")

    if avg_hit > 0.55:
        report.append("- Strong contact hitting across lineup")

    if avg_xbh > 0.20:
        report.append("- Solid extra-base hit power")

    if avg_pts > 1.6:
        report.append("- High overall offensive efficiency")

    # 🔻 Weaknesses
    report.append("\nWeaknesses:")

    if avg_out > 0.40:
        report.append("- Elevated out rate hurting consistency")

    if avg_xbh < 0.15:
        report.append("- Limited power production")

    bottom = lineup.tail(4)
    if bottom["value_per_pa"].mean() < avg_pts:
        report.append("- Bottom of lineup is a drop-off in production")

    # 🧠 Key decision
    report.append("\nKey Insight:")

    top = lineup.head(3)
    best = df.sort_values("value_per_pa", ascending=False).iloc[0]

    report.append(
        f"- {best['PLAYER']} is your most efficient hitter and should be placed in a high-impact spot (2–4)."
    )

    return "\n".join(report)