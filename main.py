import polars as pl
import matplotlib.pyplot as plt

expected_years = [
    2005,
    2006,
    2007,
    2008,
    2009,
    2010,
    2011,
    2012,
    2013,
    2014,
    2015,
    2016,
    2017,
    2018,
    2019,
    2020,
    2021,
    2022,
    2023,
]


def load_dataset(dataset):
    """loads the data"""
    df = pl.read_csv(dataset)
    df = df.fill_null(0)
    df = df.fill_nan(0)
    return df


def get_summaries_per_country(dataset):
    yearly_data = dataset.group_by(["Country name"]).agg(
        pl.col("Healthy life expectancy at birth").mean().alias("Mean"),
        pl.col("Healthy life expectancy at birth").median().alias("Median"),
        pl.col("Healthy life expectancy at birth").std().alias("Std Deviation"),
        pl.col("Healthy life expectancy at birth").max().alias("Maximum"),
        pl.col("Healthy life expectancy at birth").min().alias("Minimum"),
    )
    return yearly_data.sort(by=["Country name"])


def get_summaries_per_year(dataset):
    yearly_data = dataset.group_by(["year"]).agg(
        pl.col("Healthy life expectancy at birth").mean().alias("Mean"),
        pl.col("Healthy life expectancy at birth").median().alias("Median"),
        pl.col("Healthy life expectancy at birth").std().alias("Std Deviation"),
        pl.col("Healthy life expectancy at birth").max().alias("Maximum"),
        pl.col("Healthy life expectancy at birth").min().alias("Minimum"),
    )
    return yearly_data.sort(by=["year"])


def get_average_per_year(dataset):
    yearly_data = dataset.group_by(["year"]).agg(
        pl.col("Healthy life expectancy at birth").mean().alias("Mean")
    )
    return yearly_data.sort(by=["year"])


# I wanted to use this to generate a line chart but the data was too many making the chart unreadable
# I'll look at other options later. Scatter too didn't help very much
def get_country_per_year(dataset):
    yearly_data = dataset.group_by(["year", "Country name"]).agg(
        pl.col("Healthy life expectancy at birth").sum()
    )

    countries = yearly_data["Country name"].unique().to_list()
    set_expected_years = set(expected_years)
    # Find the years missing
    plot_data = {
        country: (
            set_expected_years
            - set(
                yearly_data.filter(pl.col("Country name") == country)["year"].to_list()
            )
        )
        for country in countries
    }

    # Append the missing years to the dataframe giving it zero for Healthy life expectancy at birth
    for key in plot_data.keys():
        for year in plot_data[key]:
            new_row = pl.DataFrame(
                {
                    "year": [year],
                    "Country name": [key],
                    "Healthy life expectancy at birth": [0.0],
                },
                yearly_data.schema,
            )
            yearly_data = pl.concat([yearly_data, new_row])

    return pl.DataFrame(yearly_data.sort(by=["Country name", "year"]))


def save_plot():
    data = load_dataset("World_Happiness_Report_2024.csv")

    yearly_average = get_average_per_year(data)
    # Extract unique years and categories
    years = yearly_average["year"].unique().to_list()
    plt.figure(figsize=(14, 6))
    plt.bar(
        years,
        yearly_average["Mean"],
    )
    # Adding labels and title
    plt.xlabel("Year")
    plt.ylabel("Mean Healthy life expectancy at birth")
    plt.title("Yearly Mean Healthy life expectancy at birth")
    plt.xticks(years)  # Set x-axis to show all years

    plt.savefig("yearly_average.png")
