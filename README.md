# wintools

Utilityes for Windows.

## 必要な環境変数

特になし。

## インストール

```(sh)
pip install git+https://github.com/yukkun007/wintools
```

windowsの場合(pythonランチャーを使う場合)

```(sh)
py -m pip install git+https://github.com/yukkun007/wintools
```

## アップグレード

```(sh)
pip install -U git+https://github.com/yukkun007/wintools
```

windowsの場合(pythonランチャーを使う場合)

```(sh)
py -m pip install -U git+https://github.com/yukkun007/wintools
```

## 使い方 (コードからモジュールを利用)

[参照](#モジュールを利用)

## 使い方 (コマンドラインアプリ)

```(sh)
py -m wintools
```

## アンインストール

```(sh)
py -m pip uninstall wintools
```

## 開発フロー

### 環境構築

1. プロジェクトディレクトリに仮想環境を作成するために下記環境変数を追加

   - Linux

     ```(sh)
     export PIPENV_VENV_IN_PROJECT=true
     ```

   - Windows

     ```(sh)
     set PIPENV_VENV_IN_PROJECT=true
     ```

1. `py -m pip install pipenv`
1. `git clone git@github.com:yukkun007/wintools.git`
1. `cd wintools`
1. `py -m pipenv install --dev`

### install package

下記は編集可能モードでインストールされる。

```(sh)
py -m pipenv run pip install -e .
```

通常のインストールは下記だがソース編集の都度`upgrade package`が必要なので基本は`-e`をつける。

```(sh)
py -m pipenv run pip install .
```

### upgrade package

```(sh)
py -m pipenv run pip install --upgrade . (もしくは-U)
```

## 開発行為

### モジュールを利用

```(python)
$ python
or
$ py -m pipenv run python
>>> import wintools
>>> wintools.foo()
>>> wintools.hello("yutaka")
```

### コマンドラインアプリを実行

```(sh)
py -m pipenv run start (もしくはmyapp)
```

### unit test

```(sh)
py -m pipenv run ut
```

### lint

```(sh)
py -m pipenv run lint
```

### create api document (sphinx)

```(sh)
py -m pipenv run doc
```
