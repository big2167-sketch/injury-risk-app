import pandas as pd
def load_and_process_data(file_path):
    df = pd.read_csv(file_path)
    # Remove football because ball movement is not player movement
    df_players = df[df["displayName"] != "football"].copy()
     # Convert speed from yards/second to miles/hour
    df_players["speed_mph"] = df_players["s"] * 2.045
     # Remove unrealistic player speeds
    df_players = df_players[df_players["speed_mph"] <= 25].copy()
    # Create speed categories
    df_players["speed_category"] = pd.cut(
        df_players["speed_mph"],
        bins=[0, 5, 12, 18, 25],
        labels=[
            "Low (0–5 mph)",
            "Moderate (5–12 mph)",
            "High (12–18 mph)",
            "Sprint (18–25 mph)"
        ],
        include_lowest=True
    )
    # Create acceleration categories
    df_players["accel_category"] = pd.cut(
        df_players["a"],
        bins=[0, 1, 2.5, 10],
        labels=[
            "Low (0–1)",
            "Moderate (1–2.5)",
            "High (2.5+)"
        ],
        include_lowest=True
    )
    # Create movement intensity feature
    df_players["movement_intensity"] = df_players["speed_mph"] * df_players["a"]

    q75 = df_players["movement_intensity"].quantile(0.75)
    q90 = df_players["movement_intensity"].quantile(0.90)

    def label_risk(value):
        if value >= q90:
            return "High Risk Proxy (Top 10%)"
        elif value >= q75:
            return "Elevated (75–90%)"
        else:
            return "Normal (Bottom 75%)"

    df_players["risk_category"] = df_players["movement_intensity"].apply(label_risk)

    return df_players, q75, q90
