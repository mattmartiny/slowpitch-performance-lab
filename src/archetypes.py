import pandas as pd


def add_archetypes(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    #  Dynamic thresholds based on data
    ppa_75 = df["value_per_pa"].quantile(0.75)
    ppa_50 = df["value_per_pa"].quantile(0.50)
    ppa_25 = df["value_per_pa"].quantile(0.25)

    hit_75 = df["hit_rate"].quantile(0.75)
    xbh_75 = df["xbh_rate"].quantile(0.75)
    out_75 = df["out_rate"].quantile(0.75)

    def classify(row):
        pva = row["value_per_pa"]
        hit = row["hit_rate"]
        xbh = row["xbh_rate"]
        out = row["out_rate"]
        run_prod = row["run_production_per_pa"]

        # Elite = top performers
        if pva >= ppa_75 and hit >= hit_75:
            return "Elite"

        # Power = top XBH guys
        if xbh >= xbh_75:
            return "Power"

        # High floor = high hit, low outs
        if hit >= hit_75 and out < out_75:
            return "High Floor"

        # Run producer
        if run_prod >= df["run_production_per_pa"].quantile(0.75):
            return "Run Producer"

        # Boom/Bust = power + high outs
        if xbh >= xbh_75 and out >= out_75:
            return "Boom/Bust"

        if pva >= ppa_50:
            return "Above Average"


        # Low efficiency = bottom tier
        if pva <= ppa_25:
            return "Low Efficiency"

        return "Balanced"

    df["archetype"] = df.apply(classify, axis=1)

    return df