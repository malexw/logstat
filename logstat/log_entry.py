import datetime
from enum import Enum
import sys


TS_SAMPLE = "2021-04-01 13:14:15.678"
TS_LENGTH = len(TS_SAMPLE)
TS_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
LEVEL_INDEX = TS_LENGTH + 1


class Level(Enum):
    info = "INFO"
    warning = "WARNING"
    error = "ERROR"
    unknown = "UNKNOWN"


class LogFormatException(Exception):
    pass


class LogEntry(object):
    def __init__(self, time, level, message):
        self.time = time
        self.level = level
        self.message = message


def parse_line(line):
    # XXX(AW): There is a lot more error checking we can be doing here, but for now I'm fine with having the
    # script die if it encounters something unexpected.
    if len(line) < LEVEL_INDEX:
        raise LogFormatException("Log line is malformed")

    line_time = datetime.datetime.strptime(line[:TS_LENGTH], TS_FORMAT)
    line_level = Level.unknown
    message_index = 0

    if line.find(Level.info.value) == LEVEL_INDEX:
        line_level = Level.info
        message_index = LEVEL_INDEX + len(Level.info.value) + 1
    elif line.find(Level.warning.value) == LEVEL_INDEX:
        line_level = Level.warning
        message_index = LEVEL_INDEX + len(Level.warning.value) + 1
    elif line.find(Level.error.value) == LEVEL_INDEX:
        line_level = Level.error
        message_index = LEVEL_INDEX + len(Level.error.value) + 1
    else:
        raise LogFormatException("Unable to determine log level")

    return LogEntry(line_time, line_level, line[message_index:].strip())


def read_logs(source=sys.stdin, limit=2000):
    entries = []
    for line in source:
        if len(entries) == limit:
            break

        try:
            entry = parse_line(line)
        except LogFormatException:
            entry_count = len(entries)
            print(f"Failed to parse line {entry_count}: {line}")

        entries.append(entry)

    return entries
