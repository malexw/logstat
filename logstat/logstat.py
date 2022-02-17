import re

import matplotlib as mpl
import matplotlib.pyplot as plt

from .log_entry import Level, read_logs


def plot_entries(entries):
    # These tuples provide configuration for different plots to draw and has the following form:
    # (internal chart name, chart title, a function to determine if a log entry should be included in this plot)
    plots = [
        (Level.info.name, Level.info.value, lambda e: e.level is Level.info),
        (Level.warning.name, Level.warning.value, lambda e: e.level is Level.warning),
        (Level.error.name, Level.error.value, lambda e: e.level is Level.error),
        ("feature1", "Feature 1 errors", lambda e: re.match(r"Feature 1", e.message)),
        ("feature2", "Feature 2 errors", lambda e: re.match(r"Feature 2", e.message)),
        ("feature3", "Feature 3 errors", lambda e: re.match(r"Feature 3", e.message)),
    ]

    fig, axs = plt.subplot_mosaic([[plot[0]] for plot in plots], layout="tight")
    fig.set_size_inches(6, len(plots) * 1.75)
    all_entry_times = [entry.time for entry in entries]
    entry_range = (min(all_entry_times), max(all_entry_times))

    for plot in plots:
        axs[plot[0]].set_title(plot[1])
        axs[plot[0]].hist(
            [entry.time for entry in entries if plot[2](entry)],
            bins=100,
            range=entry_range,
        )

    plt.savefig("output.png")


def start():
    entries = read_logs()
    times = [entry.time for entry in entries if entry.level is Level.info]
    plot_entries(entries)


if __name__ == "__main__":
    start()
