# wintools

Windows関連ツール.

## Install

```sh
pip install git+https://github.com/mozkzki/wintools
# upgrade
pip install --upgrade git+https://github.com/mozkzki/wintools
# uninstall
pip uninstall wintools
```

## Usage

### S3

```sh
# download directory
wintools s3 download s3://mozkzki/wintools/sample/ ./out
# download file (save to current directory)
wintools s3 download s3://mozkzki/wintools/sample/LICENSE
```

### ISO

```sh
```

### File

```sh
```

## Develop

### Prepare

```sh
poetry install
poetry shell
```

### Run (Example)

```sh
./examples/example.sh
# or
make example
# or
make start # show help
```

### Unit Test

test all.

```sh
pytest
pytest -v # verbose
pytest -s # show standard output (same --capture=no)
pytest -ra # show summary (exclude passed test)
pytest -rA # show summary (include passed test)
```

with filter.

```sh
pytest -k app
pytest -k test_app.py
pytest -k my
```

specified marker.

```sh
pytest -m 'slow'
pytest -m 'not slow'
```

make coverage report.

```sh
pytest -v --capture=no --cov-config .coveragerc --cov=src --cov-report=xml --cov-report=term-missing .
# or
make ut
```

### Lint

```sh
flake8 --max-line-length=100 --ignore=E203,W503 ./src
# or
make lint
```

### Update dependency modules

dependabot (GitHub公式) がプルリクを挙げてくるので確認してマージする。

- dependabotは`pyproject.toml`と`poetry.lock`を更新してくれる
