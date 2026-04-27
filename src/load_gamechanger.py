import pandas as pd


def normalize_name(name: str) -> str:
    if pd.isna(name):
        return ""
    return str(name).strip().lower()


def load_gamechanger_csv(path: str, league: str) -> pd.DataFrame:
    raw = pd.read_csv(path)

    # Remove GameChanger header row
    data = raw.iloc[1:].copy()

    # Pull batting columns by position from the export
    df = pd.DataFrame({
        "NUMBER": data.iloc[:, 0],
        "LAST": data.iloc[:, 1],
        "FIRST": data.iloc[:, 2],
        "PA": data.iloc[:, 4],
        "AB": data.iloc[:, 5],
        "1B": data.iloc[:, 11],
        "2B": data.iloc[:, 12],
        "3B": data.iloc[:, 13],
        "HR": data.iloc[:, 14],
        "RBI": data.iloc[:, 15],
        "R": data.iloc[:, 16],
        "BB": data.iloc[:, 17],
        "ROE": data.iloc[:, 23],
    })

    df["PLAYER"] = df["FIRST"].astype(str).str.strip() + " " + df["LAST"].astype(str).str.strip()
    df["player_key"] = df["PLAYER"].apply(normalize_name)

    stat_cols = ["PA", "AB", "1B", "2B", "3B", "HR", "RBI", "R", "BB", "ROE"]

    for col in stat_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    df["OUT"] = df["AB"] - (df["1B"] + df["2B"] + df["3B"] + df["HR"])
    df["league"] = league

    return df[
        ["PLAYER", "player_key", "league", "PA", "AB", "1B", "2B", "3B", "HR", "RBI", "R", "BB", "ROE", "OUT"]
    ]