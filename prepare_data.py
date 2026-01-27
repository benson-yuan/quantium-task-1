import pandas as pd
from pathlib import Path


data = Path("data")
output_path = data/"pink_morsel_sales.csv"

def main():
    csv_files = [
        f for f in data.glob("*.csv")
        if f.name != "pink_morsel_sales.csv"
    ]

    if not csv_files:
        raise FileNotFoundError("No CSV files found")

    frames = []
    for files in csv_files:
        df = pd.read_csv(files)

    df = df[df["product"] == "pink morsel"].copy()

    df["price"] = (
        df["price"]
        .str.replace("$", "", regex=False)
        .astype(float)
    )

    df["sales"] = df["price"] * df["quantity"]

    df = df[["sales", "date", "region"]]

    frames.append(df)
    result = pd.concat(frames, ignore_index=True)
    result.to_csv(output_path, index=False)

    print(f"Saved {len(result)} rows to {output_path}")

if __name__ == "__main__":
    main()
