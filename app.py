import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

DATA_PATH = "data/pink_morsel_sales.csv"
PRICE_CHANGE_DATE = "2021-01-15"

# ---- Load and prepare data ----
df = pd.read_csv(DATA_PATH)

# Ensure correct types
df["sales"] = pd.to_numeric(df["sales"], errors="coerce")
df = df.dropna(subset=["sales"])

df["date"] = pd.to_datetime(df["date"], errors="coerce")
df = df.dropna(subset=["date"])

df = df.sort_values("date")

# Total sales per day (all regions)
daily = df.groupby("date", as_index=False)["sales"].sum()

# ---- Dash app ----
app = Dash(__name__)
server = app.server

app.layout = html.Div(
    style={"maxWidth": "1000px", "margin": "40px auto", "fontFamily": "Arial"},
    children=[
        html.H1("Pink Morsel Sales Visualiser", style={"textAlign": "center"}),

        html.P(
            f"Line chart of daily sales for Pink Morsels (sorted by date). "
            f"The dashed red line marks the price increase on {PRICE_CHANGE_DATE}.",
            style={"textAlign": "center"}
        ),

        dcc.Dropdown(
            id="view",
            options=[
                {"label": "Total sales per day (all regions)", "value": "total"},
                {"label": "Sales per day by region", "value": "by_region"},
            ],
            value="total",
            clearable=False,
            style={"marginBottom": "16px"},
        ),

        dcc.Graph(id="sales_chart"),
        html.Div(id="answer", style={"marginTop": "10px", "fontWeight": "bold"})
    ],
)

@app.callback(
    Output("sales_chart", "figure"),
    Output("answer", "children"),
    Input("view", "value"),
)
def update_chart(view):
    cutoff = pd.to_datetime(PRICE_CHANGE_DATE)

    if view == "by_region":
        by_region = df.groupby(["date", "region"], as_index=False)["sales"].sum()
        fig = px.line(
            by_region,
            x="date",
            y="sales",
            color="region",
            labels={"date": "Date", "sales": "Sales ($)"},
            title="Daily Pink Morsel Sales by Region",
        )
    else:
        fig = px.line(
            daily,
            x="date",
            y="sales",
            labels={"date": "Date", "sales": "Sales ($)"},
            title="Total Daily Pink Morsel Sales (All Regions)",
        )

    # --- Draw the price-change marker robustly (avoids add_vline annotation bugs) ---
    fig.add_shape(
        type="line",
        x0=cutoff,
        x1=cutoff,
        y0=0,
        y1=1,
        xref="x",
        yref="paper",
        line=dict(dash="dash", width=2, color="red"),
    )

    fig.add_annotation(
        x=cutoff,
        y=1,
        xref="x",
        yref="paper",
        text=f"Price increase ({PRICE_CHANGE_DATE})",
        showarrow=False,
        yanchor="bottom",
    )

    # --- Answer text (before vs after) ---
    before_data = daily[daily["date"] < cutoff]["sales"]
    after_data = daily[daily["date"] >= cutoff]["sales"]

    if before_data.empty or after_data.empty:
        answer = (
            f"Insufficient data on one side of {PRICE_CHANGE_DATE} to compare average daily sales."
        )
    else:
        before = before_data.mean()
        after = after_data.mean()
        answer = (
            f"Average daily sales BEFORE {cutoff.date()}: ${before:,.2f} | "
            f"AFTER: ${after:,.2f} → "
            + ("Higher AFTER" if after > before else "Higher BEFORE")
        )

    return fig, answer


if __name__ == "__main__":
    app.run(debug=True)
