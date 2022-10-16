import pandas as pd
from typing import BinaryIO, List
from pandas.errors import ParserError
import httpx
from datetime import datetime


TOTAL_PROFIT_LIMIT = 1000
TOTAL_COST_LIMIT = 5000000
FIRST_APT_SERVICE = "https://api.example.com/"
SECOUND_API_SERVICE = "https://api-priority.example.com/"


def read_file(file_data: BinaryIO) -> pd.DataFrame:
    try:
        return pd.read_excel(file_data)
    except ValueError as ex:
        return pd.read_csv(file_data)


def validate_dataset(dataset: pd.DataFrame) -> List[str]:
    errors = list()
    for _, row in dataset.iterrows():
        try:
            r = httpx.get(
                FIRST_APT_SERVICE
                + "MasterData/Country/1"
                + f"?countryName={row['Country']}"
            )

            if r.json()[0]["region"] != row["Region"]:
                errors.append(
                    f"order {row['Order ID']} -> region {row['Region']} is incorrect"
                )
        except Exception as ex:
            errors.append(
                f"order {row['Order ID']} -> region {row['Region']} is incorrect"
            )
        try:
            r = httpx.get(
                SECOUND_API_SERVICE + f"?priorityCode={row['Order Priority']}"
            )
            if r.json() == 0:
                errors.append(
                    f"order {row['Order ID']} -> priority code {row['Order Priority']} is incorrect"
                )
        except Exception as ex:
            errors.append(
                f"order {row['Order ID']} -> priority code {row['Order Priority']} is incorrect"
            )

        if row["Total Profit"] < TOTAL_PROFIT_LIMIT:
            errors.append(
                f"order {row['Order ID']} -> total profit should not be less than {TOTAL_PROFIT_LIMIT}"
            )
        if row["Total Cost"] > TOTAL_COST_LIMIT:
            errors.append(
                f"order {row['Order ID']} -> total cost should not be greater than {TOTAL_COST_LIMIT}"
            )

        order_date = datetime.strptime(row["Order Date"], "%m/%d/%Y")
        ship_date = datetime.strptime(row["Ship Date"], "%m/%d/%Y")
        if not order_date < ship_date:
            errors.append(
                f"order {row['Order ID']} -> order date {row['Order Date']} should not be greater than {row['Ship Date']}"
            )
        if not round(row["Units Sold"] * row["Unit Price"], 2) == row["Total Revenue"]:
            errors.append(
                f"order {row['Order ID']} -> total revenue {row['Total Revenue']} is not equal to {row['Unit Price'] * row['Units Sold'] }"
            )
        if not round(row["Units Sold"] * row["Unit Cost"], 2) == row["Total Cost"]:
            errors.append(
                f"order {row['Order ID']} -> total cost {row['Total Cost']} is not equal to {row['Units Sold'] * row['Unit Cost'] }"
            )
    return errors


if __name__ == "__main__":
    with open("test.csv", "rb") as file:
        data_frame = read_file(file)
        print(validate_dataset(data_frame))
