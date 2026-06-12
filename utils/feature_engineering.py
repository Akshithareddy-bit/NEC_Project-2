def create_features(df):

    if "Date" not in df.columns:
        return df

    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    df["Day"] = df["Date"].dt.day
    df["Quarter"] = df["Date"].dt.quarter
    df["Weekday"] = df["Date"].dt.day_name()

    if "Sales" in df.columns:

        df["Lag_1"] = df["Sales"].shift(1)

        df["Lag_7"] = df["Sales"].shift(7)

        df["Rolling_Avg"] = (
            df["Sales"]
            .rolling(window=7)
            .mean()
        )

    return df