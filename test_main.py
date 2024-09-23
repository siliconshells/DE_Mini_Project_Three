from main import load_dataset, get_summaries_per_year, get_summaries_per_country
from convert_to_markdown import save_summaries_to_markdown
import os
import polars as pl

dataset_path = "World_Happiness_Report_2024.csv"


def test_load_dataset():
    """Testing the loading of dataset"""
    dataset = load_dataset(dataset_path)
    assert dataset is not None
    assert dataset.shape == (2363, 11)
    return


def test_file_creation(cleanup=True):
    """Test file creation"""
    dataset = load_dataset(dataset_path)
    # Remove existing ones
    if os.path.exists("yearly_average.png"):
        os.remove("yearly_average.png")
    if os.path.exists("summary_statistics.md"):
        os.remove("summary_statistics.md")

    # Test and create new ones
    assert not os.path.exists("yearly_average.png")
    assert not os.path.exists("summary_statistics.md")

    # Create the files
    save_summaries_to_markdown(dataset)

    assert os.path.exists("yearly_average.png")
    assert os.path.exists("summary_statistics.md")

    # Clean up
    if cleanup:
        if os.path.exists("yearly_average.png"):
            os.remove("yearly_average.png")
        if os.path.exists("summary_statistics.md"):
            os.remove("summary_statistics.md")


def test_country_summaries():
    """Test country summaries"""
    dataset = load_dataset(dataset_path)
    summaries_per_country = get_summaries_per_country(dataset)

    # print(polars_summaries["statistic", "Healthy life expectancy at birth"])
    countries = dataset["Country name"].unique()
    for country in countries:
        country_data = dataset.filter(pl.col("Country name") == country)[
            "Healthy life expectancy at birth"
        ]

        # test mean
        assert (
            country_data.mean()
            == summaries_per_country.filter(pl.col("Country name") == country)["Mean"][
                0
            ]
        )

        # test median
        assert (
            country_data.median()
            == summaries_per_country.filter(pl.col("Country name") == country)[
                "Median"
            ][0]
        )

        # test max
        assert (
            country_data.max()
            == summaries_per_country.filter(pl.col("Country name") == country)[
                "Maximum"
            ][0]
        )

        # test min
        assert (
            country_data.min()
            == summaries_per_country.filter(pl.col("Country name") == country)[
                "Minimum"
            ][0]
        )

        # test standard deviation
        if country_data.std() is not None:
            assert round(country_data.std(), 11) == round(
                summaries_per_country.filter(pl.col("Country name") == country)[
                    "Std Deviation"
                ][0],
                11,
            )


def test_year_summaries():
    """Test year summaries"""
    dataset = load_dataset(dataset_path)
    summaries_per_year = get_summaries_per_year(dataset)

    # print(polars_summaries["statistic", "Healthy life expectancy at birth"])
    for year in range(2005, 2023):
        year_data = dataset.filter(pl.col("year") == year)[
            "Healthy life expectancy at birth"
        ]

        # test mean
        assert (
            year_data.mean()
            == summaries_per_year.filter(pl.col("year") == year)["Mean"][0]
        )

        # test median
        assert (
            year_data.median()
            == summaries_per_year.filter(pl.col("year") == year)["Median"][0]
        )

        # test max
        assert (
            year_data.max()
            == summaries_per_year.filter(pl.col("year") == year)["Maximum"][0]
        )

        # test min
        assert (
            year_data.min()
            == summaries_per_year.filter(pl.col("year") == year)["Minimum"][0]
        )

        # test standard deviation
        assert round(year_data.std(), 11) == round(
            summaries_per_year.filter(pl.col("year") == year)["Std Deviation"][0],
            11,
        )


if __name__ == "__main__":
    test_load_dataset()
    test_file_creation(False)
    test_year_summaries()
    test_country_summaries()
    print("Test completed successfully")
