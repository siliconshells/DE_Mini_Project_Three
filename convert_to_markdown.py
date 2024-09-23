from main import (
    get_summaries_per_country,
    get_summaries_per_year,
    save_plot,
    load_dataset,
)


# saving markdown
def save_summaries_to_markdown(data) -> str:
    save_plot()
    with open("summary_statistics.md", "w", encoding="utf-8") as file:
        file.write("# Summary Statistics Grouped By Year\n")
        file.write(get_summaries_per_year(data).to_pandas().to_markdown())
        file.write("\n\n")
        file.write("# Summary Statistics Grouped By Country\n")
        file.write(get_summaries_per_country(data).to_pandas().to_markdown())
        # file.write("# Country Values Per Year\n")
        # file.write(get_country_per_year(data).to_pandas().to_markdown())
        file.write("\n\n")
        file.write("# yearly_average")
        file.write("\n\n")
        file.write("![yearly_average](yearly_average.png)")
    return "Markdown written successfully"


if __name__ == "__main__":
    save_summaries_to_markdown(load_dataset("World_Happiness_Report_2024.csv"))
    print("Test completed successfully")
