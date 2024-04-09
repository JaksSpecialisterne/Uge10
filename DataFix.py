import sys
import os
import pandas as pd


def FixMissingEntries(Filename: str):
    pass


def fix_faa_id(flights: pd.DataFrame) -> pd.DataFrame:
    df_letters = pd.read_csv("Data/L_AIRPORT.csv").dropna()
    df_numbers = pd.read_csv("Data/L_AIRPORT_ID.csv").dropna()

    df = pd.merge(df_letters, df_numbers, on="Description", how="left").dropna()

    df.columns = ["IATA", "Description", "FAA"]

    df["FAA"] = df["FAA"].astype(int)

    flights = map_faa_to_iata(flights, "ORIGIN_AIRPORT", df)
    flights = map_faa_to_iata(flights, "DESTINATION_AIRPORT", df)

    return flights


def map_faa_to_iata(df: pd.DataFrame, column: str, mapping: pd.DataFrame):
    mapping = mapping.drop_duplicates("FAA")

    # Extracting the mapping for the specific value
    mapping_dict = dict(zip(mapping["FAA"], mapping["IATA"]))

    # Replace values in the column using the mapping dictionary
    df[column] = df[column].map(mapping_dict).fillna(df[column])

    return df


def fix_timestamp(time):
    try:
        time = int(time)
        time = str(time).zfill(4)
        time = f"{time[:2]}:{time[2:]}"
        if time == "24:00":
            time = "00:00"
    except ValueError:
        pass
    return time


def fix_time(flights: pd.DataFrame) -> pd.DataFrame:
    timestamps = [
        "SCHEDULED_DEPARTURE",
        "DEPARTURE_TIME",
        "WHEELS_OFF",
        "WHEELS_ON",
        "SCHEDULED_ARRIVAL",
        "ARRIVAL_TIME",
    ]

    for i in timestamps:
        flights[i] = flights[i].apply(fix_timestamp)

    return flights


if __name__ == "__main__":
    data = pd.read_csv("Data/flights.csv")
    data = fix_time(data)
    data = fix_faa_id(data)
    data.to_csv("Data/flights.csv")
