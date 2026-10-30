# tasky

A tiny command-line task tracker written in plain Python (no dependencies).

## Usage

```sh
python -m tasky add Buy milk
python -m tasky list
python -m tasky done 1
python -m tasky rm 1
```

Tasks are stored in `~/.tasky.json` (override with `--file PATH`).

## Tests

```sh
python -m unittest -v
```
