# logstat

logstat is a minimalist set of tooling for graphing data obtained from server logs. logstat reads logs provided via stdin and produces a set of graphs as `output.png` in the project root directory. Lines are read until either 2000 lines have been read, or an EOF in encountered, after which the output file is generated and the script terminates.

## Dependencies

logstat uses poetry for managing python package dependencies. A requirements.txt file is provided for those who want to run the project without installing poetry, but this hasn't been tested.

```shell
$ poetry install
```

## Running

A natural way to provide logs to the script is through a pipe:

```shell
$ cat sample_log.txt | poetry run logstat
```

## Development

Tests run with pytest and can be initiated with poetry

```shell
$ poetry run pytest
```

Source files should be formatted with Black

```shell
$ poetry run black logstat/unformatted_file.py
```

