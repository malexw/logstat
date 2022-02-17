import datetime
import pytest

from logstat import log_entry


def test_normal_parse_line():
    test_dt = datetime.datetime(2022, 4, 1, 13, 14, 15)
    # Trim the last 3 digits of the formatted time string because strftime writes out microseconds but the
    # logs only go to milliseconds
    test_dt_str = test_dt.strftime(log_entry.TS_FORMAT)[:-3]

    entry = log_entry.parse_line(f"{test_dt_str} INFO This is an info message")
    assert entry.time == test_dt
    assert entry.level is log_entry.Level.info
    assert entry.message == "This is an info message"


def test_parse_empty_log_line():
    with pytest.raises(log_entry.LogFormatException):
        entry = log_entry.parse_line("")


def test_parse_unknown_level():
    with pytest.raises(log_entry.LogFormatException):
        entry = log_entry.parse_line(
            f"{log_entry.TS_SAMPLE} DEBUG A debug level message"
        )
