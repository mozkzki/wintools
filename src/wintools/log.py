import sys
import logging


def set_logger(logger):
    # 標準出力(コンソール)にログを出力するハンドラを生成する
    sh = logging.StreamHandler(sys.stdout)
    # エラーレベル設定(この指定以上のレベルのログレコードを出力)
    sh.setLevel(logging.WARNING)
    # フォーマッタを定義する
    # 第一引数: メッセージのフォーマット文字列
    # 第二引数: 日付時刻のフォーマット文字列
    fmt = logging.Formatter(
        "[%(asctime)s][%(name)s][%(levelname)s] %(message)s", "%Y-%m-%dT%H:%M:%S"
    )
    # フォーマッタをハンドラに紐づける
    sh.setFormatter(fmt)
    # ハンドラをロガーに紐づける
    logger.addHandler(sh)
