import matplotlib.pyplot as plt


def plot_value_vs_hit_rate(df, league_name):
    df = df[(df["PLAYER"].notna()) & (df["PA"] > 0)]
    plt.figure()

    plt.scatter(df["hit_rate"], df["value_per_pa"])

    for _, row in df.iterrows():
        plt.text(row["hit_rate"], row["value_per_pa"], row["PLAYER"], fontsize=6)

    plt.xlabel("Hit Rate")
    plt.ylabel("Value Per PA")
    plt.title(f"{league_name} Player Performance")

    plt.savefig(f"output/{league_name.lower()}_scatter.png")
    plt.close()