def print_top_players(df, n=10):
    print("\nTOP PLAYERS")

    top = df.head(n)

    for i, row in enumerate(top.itertuples(), start=1):
        print(
            f"{i}. {row.PLAYER} — "
            f"OV: {row.offensive_value:.1f} | "
            f"OV/PA: {row.value_per_pa:.2f} | "
            f"Hit%: {row.hit_rate:.2f} | "
            f"Archetype: {row.archetype}"
        )


def print_batting_order(df):
    print("\n RECOMMENDED BATTING ORDER")

    for row in df.itertuples():
        print(
            f"{row.batting_order}. {row.PLAYER} — {row.batting_role} "
            f"(OV/PA: {row.value_per_pa:.2f})"
        )