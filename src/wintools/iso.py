import os
import time
import glob
from typing import List
from wintools.file import print_files_info


def print_iso_files_info(iso_file: str) -> None:
    search_list = ["E", "F", "G", "H", "I"]

    files: List[str] = []
    while len(files) <= 0:
        # 検索対象のドライブレターを決める（ない場合、次のドライブレターで試す）
        drive_letter = search_list.pop(0)

        # filesが取れない時があるので、ダミーアクセス
        test = os.path.join("{}:/".format(drive_letter), "dummy")  # noqa F841

        files = glob.glob("{}:/*".format(drive_letter))
        time.sleep(1)

        # 検索対象のドライブレターがもうなければ終わり
        if len(search_list) == 0:
            break

    print("--------- ↓ [{}] ↓ --------".format(iso_file))
    print_files_info(files)
    print("--------- ↑ [{}] ↑ --------".format(iso_file))


def mount(iso_file: str) -> int:
    # Pythonからpowershellを実行
    power_command = 'Mount-DiskImage -ImagePath "{}"'.format(iso_file)
    return os.system("powershell -Command" + " " + power_command)


def unmount(iso_file: str) -> int:
    # Pythonからpowershellを実行
    power_command = 'DisMount-DiskImage -ImagePath "{}"'.format(iso_file)
    return os.system("powershell -Command" + " " + power_command)


def dump_iso(iso_file: str) -> None:
    mount(iso_file)
    print_iso_files_info(iso_file)
    unmount(iso_file)
