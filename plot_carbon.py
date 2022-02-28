#imports
from matplotlib import patches as mpatches
from matplotlib import pyplot as plt
from datetime import datetime
import pandas as pd
import os

#function definitions
def trend_plot(df, path):
    plt.figtext(0.99, -.05, "Data extracted from ESRL/NOAA", horizontalalignment="right", fontsize="x-small")
    plt.xlabel("Date")
    plt.ylabel("CO\N{SUBSCRIPT TWO} (ppm)")
    plt.title("Trend and Cycle")

    date_list = pd.to_datetime(df[["year", "month", "day"]])

    plt.plot_date(date_list, df["smoothed"], "#3bbbbb")
    plt.plot_date(date_list, df["trend"], "#fa9a39")

    cyan_patch = mpatches.Patch(color="#3bbbbb", label="cycle")
    orange_patch = mpatches.Patch(color="#fa9a39", label="trend")

    plt.legend(handles=[cyan_patch, orange_patch], loc="upper left")

    plt.savefig(f"{path}IMAGE1.png", dpi=300, bbox_inches="tight", pad_inches=0.4)
    plt.clf()

def year_plot(df, path):
    plt.figtext(0.99, -.05, "Data extracted from ESRL/NOAA", horizontalalignment="right", fontsize="x-small")
    plt.xlabel("Day of Year")
    plt.ylabel("CO\N{SUBSCRIPT TWO} (ppm)")
    plt.title("Parsed by Year")

    years = df["year"].unique()
    df_list = [df[df["year"]==year] for year in years]

    for i in range(len(df_list)):
        days_of_year = [x.timetuple()[7] for x in pd.to_datetime(df_list[i][["year", "month", "day"]])]
        cycle_data = df_list[i]["smoothed"].tolist()
        plt.plot(days_of_year, cycle_data, "#3bbbbb")
        plt.annotate(years[i], (390, max(cycle_data) - 0.35), annotation_clip=False)

    plt.savefig(f"{path}IMAGE2.png", dpi=300, bbox_inches="tight", pad_inches=0.4)
    plt.clf()

def offset_year_plot(df, path):
    plt.figtext(0.99, -.05, "Data extracted from ESRL/NOAA", horizontalalignment="right", fontsize="x-small")
    plt.xlabel("Day of Year")
    plt.ylabel("CO\N{SUBSCRIPT TWO} (ppm)")

    years = df["year"].unique()
    df_list = [df[df["year"]==year] for year in years]
    size = len(df_list)

    plt.title(f"Comparison of {years[-1]} to Previous Decade")
    grey_patch = mpatches.Patch(color="#b3B3b3", label=f"{years[0]}-{years[-2]}")
    orange_patch = mpatches.Patch(color="#fa9a39", label=years[-1])
    plt.legend(handles=[grey_patch, orange_patch], loc="lower left")

    for i in range(size):
        days_of_year = [x.timetuple()[7] for x in pd.to_datetime(df_list[i][["year", "month", "day"]])]
        cycle_data = df_list[i]["smoothed"].tolist()
        offset_cycle_data = [x - cycle_data[0] for x in cycle_data]
        if i < size - 1:
            plt.plot(days_of_year, offset_cycle_data, "#b3B3b3", linestyle="-")
        else:
            plt.plot(days_of_year, offset_cycle_data, "#fa9a39", linewidth=5, alpha=0.5)

    plt.savefig(f"{path}IMAGE3.png", dpi=300, bbox_inches="tight", pad_inches=0.4)
    plt.clf()

def modification_history(df, path):
    tail = df.tail(1).squeeze().apply(int)
    date = datetime(tail["year"], tail["month"], tail["day"]).strftime("%-D")
    with open(f"{path}modifications.txt", "w") as date_file:
        date_file.write(f"Most recent datum: {date}")

def main():
    df = pd.read_csv("https://www.esrl.noaa.gov/gmd/webdata/ccgg/trends/co2/co2_trend_gl.csv", comment="#")
    OS_PATH = os.path.join(os.path.dirname(__file__), os.path.realpath("../../../"))
    RESOURCE_PATH = f"{OS_PATH}/public_html/resources/"

    trend_plot(df, RESOURCE_PATH)
    year_plot(df, RESOURCE_PATH)
    offset_year_plot(df, RESOURCE_PATH)
    modification_history(df, RESOURCE_PATH)

#function calls
if __name__=="__main__":
    main()
