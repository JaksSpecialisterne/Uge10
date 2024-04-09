import sys
import os
import pandas as pd


def FixMissingEntries(Filename: str):
    pass


def fix_faa_id():
    df_letters = pd.read_csv("Data/L_AIRPORT.csv").dropna()
    df_numbers = pd.read_csv("Data/L_AIRPORT_ID.csv").dropna()
    flights = pd.read_csv("Data/flights.csv")

    df = pd.merge(df_letters, df_numbers, on="Description", how="left").dropna()

    df.columns = ["IATA", "Description", "FAA"]

    df["FAA"] = df["FAA"].astype(int)
    df["FAA"] = df["FAA"].astype(str)

    flights = map_faa_to_iata(flights, "ORIGIN_AIRPORT", df)
    flights = map_faa_to_iata(flights, "DESTINATION_AIRPORT", df)

    flights.to_csv("Data/flights.csv")


def map_faa_to_iata(df: pd.DataFrame, column: str, mapping: pd.DataFrame):
    mapping = mapping.drop_duplicates("FAA")

    # Extracting the mapping for the specific value
    mapping_dict = dict(zip(mapping["FAA"], mapping["IATA"]))

    # Replace values in the column using the mapping dictionary
    df[column] = df[column].map(mapping_dict).fillna(df[column])

    return df


if __name__ == "__main__":
    fix_faa_id()
