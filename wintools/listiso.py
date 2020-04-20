import os
import time
import glob
import pathlib
import datetime
import argparse


def print_fileinfo(file: str, drive_letter: str):
    p = pathlib.Path(file)
    p.resolve()

    # ファイルパス (ドライブレターは削除)
    file_path = str(p)
    file_path = file_path.replace("{}:\\".format(drive_letter), "")

    # ファイルサイズ
    file_size = os.path.getsize(file)

    # ファイル最終更新日付
    dt = datetime.datetime.fromtimestamp(p.stat().st_mtime)
    year = dt.strftime("%Y")
    month = dt.strftime("%m").lstrip("0")
    day = dt.strftime("%d").lstrip("0")
    file_update_time = year + "/" + month + "/" + day

    print("{},,,{},{}".format(file_path, file_size, file_update_time))


def print_files(iso_file: str):
    search_list = ["E", "F", "G", "H", "I"]

    files = []
    while len(files) <= 0:
        # 検索対象のドライブレターを決める（ない場合、次のドライブレターで試す）
        drive_letter = search_list.pop(0)

        # filesが取れない時があるので、ダミーアクセス
        test = os.path.join("{}:/".format(drive_letter), "dummy")

        files = glob.glob("{}:/*".format(drive_letter))
        time.sleep(1)

        # 検索対象のドライブレターがもうなければ終わり
        if len(search_list) == 0:
            break

    print("--------- ↓ [{}] ↓ --------".format(iso_file))
    for file in files:
        print_fileinfo(file, drive_letter)
    print("--------- ↑ [{}] ↑ --------".format(iso_file))


def mount(iso_file: str):
    # Pythonからpowershellを実行
    power_command = 'Mount-DiskImage -ImagePath "{}"'.format(iso_file)
    os.system("powershell -Command" + " " + power_command)


def unmount(iso_file: str):
    # Pythonからpowershellを実行
    power_command = 'DisMount-DiskImage -ImagePath "{}"'.format(iso_file)
    os.system("powershell -Command" + " " + power_command)


def list_iso(iso_file: str):
    mount(iso_file)
    print_files(iso_file)
    unmount(iso_file)


def main():
    parser = argparse.ArgumentParser(
        description="""
isoファイルの中身を表示します。

指定されたディレクトリにあるisoファイルをマウントして、その情報(サイズや更新日付)を表示します。
適当なドライブレター（E:からI:）に対してマウント→中身表示→アンマウントの流れで実行します。
マウントに失敗する場合はコードを直接変更してください。
表示された情報は、そのままマスター出図連絡票にコピー出来ます。
    """,
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument("target", help="isoファイルの格納ディレクトリ(フルパス)")
    args = parser.parse_args()

    isos = glob.glob("{}/*".format(args.target))
    for iso in isos:
        list_iso(iso)


# sample call
# python wintools\listiso.py c:\workspace\wintools E
if __name__ == "__main__":
    main()

# sample result
# <file>,,,<size>,<timestamp>
# C:\workspace\src_fm\intra_svn_all\trunk\FM_BUILDtool\@not_used\Tools\LockFile\LockFile.cpp,,,2108,2019/9/2
# C:\workspace\src_fm\intra_svn_all\trunk\FM_BUILDtool\@not_used\Tools\LockFile\LockFile.dsp,,,4153,2019/9/2
# C:\workspace\src_fm\intra_svn_all\trunk\FM_BUILDtool\@not_used\Tools\LockFile\LockFile.dsw,,,545,2019/9/2
# C:\workspace\src_fm\intra_svn_all\trunk\FM_BUILDtool\@not_used\Tools\LockFile\LockFile.h,,,1358,2019/9/2
# C:\workspace\src_fm\intra_svn_all\trunk\FM_BUILDtool\@not_used\Tools\LockFile\LockFile.rc,,,5238,2019/9/2
# C:\workspace\src_fm\intra_svn_all\trunk\FM_BUILDtool\@not_used\Tools\LockFile\LockFileDlg.cpp,,,4549,2019/9/2
# C:\workspace\src_fm\intra_svn_all\trunk\FM_BUILDtool\@not_used\Tools\LockFile\LockFileDlg.h,,,1502,2019/9/2
# C:\workspace\src_fm\intra_svn_all\trunk\FM_BUILDtool\@not_used\Tools\LockFile\ReadMe.txt,,,1557,2019/9/2
# C:\workspace\src_fm\intra_svn_all\trunk\FM_BUILDtool\@not_used\Tools\LockFile\res\LockFile.ico,,,1078,2019/9/2
# C:\workspace\src_fm\intra_svn_all\trunk\FM_BUILDtool\@not_used\Tools\LockFile\res\LockFile.rc2,,,435,2019/9/2
# C:\workspace\src_fm\intra_svn_all\trunk\FM_BUILDtool\@not_used\Tools\LockFile\Resource.h,,,824,2019/9/2
# C:\workspace\src_fm\intra_svn_all\trunk\FM_BUILDtool\@not_used\Tools\LockFile\StdAfx.cpp,,,226,2019/9/2
# C:\workspace\src_fm\intra_svn_all\trunk\FM_BUILDtool\@not_used\Tools\LockFile\StdAfx.h,,,1065,2019/9/2
