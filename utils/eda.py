import pandas as pd
import plotly.express as px


def monthly_sales_trend(df):

    monthly = (
        df.groupby("Month")["Sales"]
        .sum()
        .reset_index()
    )

    fig = px.line(
        monthly,
        x="Month",
        y="Sales",
        title="Monthly Sales Trend"
    )

    return fig


def revenue_contribution(df):

    revenue = (
        df.groupby("Product")["Revenue"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        revenue,
        names="Product",
        values="Revenue",
        title="Revenue Contribution"
    )

    return fig


def top_products(df):

    top = (
        df.groupby("Product")["Sales"]
        .sum()
        .reset_index()
        .sort_values(
            by="Sales",
            ascending=False
        )
        .head(10)
    )

    fig = px.bar(
        top,
        x="Sales",
        y="Product",
        orientation="h",
        title="Top Selling Products"
    )

    return fig