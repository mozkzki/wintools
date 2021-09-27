import os
import pathlib
import datetime
from typing import List


def print_info(target_path: str) -> None:

    target = pathlib.Path(target_path)
    target.resolve()
    if target.is_dir:
        children_dir = [p for p in target.iterdir() if p.is_dir()]
        for d in children_dir:
            print_info(str(d))
        children_file = [p for p in target.iterdir() if p.is_file()]
        for f in children_file:
            __print_file_info(str(f))
    elif target.is_file:
        __print_file_info(str(target))


def print_files_info(files: List[str]) -> None:
    for file in files:
        __print_file_info(file)


def __print_file_info(file: str) -> None:
    p = pathlib.Path(file)
    p.resolve()

    # ファイルパス
    file_path = str(p)
    # ファイルサイズ
    file_size = os.path.getsize(file)
    # ファイル最終更新日付
    dt = datetime.datetime.fromtimestamp(p.stat().st_mtime)
    year = dt.strftime("%Y")
    month = dt.strftime("%m").lstrip("0")
    day = dt.strftime("%d").lstrip("0")
    file_update_time = year + "/" + month + "/" + day

    print("{},{},{}".format(file_path, file_size, file_update_time))
