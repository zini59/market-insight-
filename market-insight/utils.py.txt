def filter_region(df, region):
    if region == "전체":
        return df
    return df[df["region"] == region]