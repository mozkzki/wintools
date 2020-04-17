import os
import glob
import pathlib
import datetime
import argparse


def print_fileinfo(file: str):
    p = pathlib.Path(file)
    p.resolve()

    file_path = str(p)
    file_size = os.path.getsize(file)

    dt = datetime.datetime.fromtimestamp(p.stat().st_mtime)
    year = dt.strftime("%Y")
    month = dt.strftime("%m").lstrip("0")
    day = dt.strftime("%d").lstrip("0")
    file_update_time = year + "/" + month + "/" + day

    print("{},,,{},{}".format(file_path, file_size, file_update_time))


def print_files(drive_letter: str):
    files = glob.glob("{}:/*".format(drive_letter))
    print("-----------------------")
    for file in files:
        print_fileinfo(file)
    print("-----------------------")


def mount(iso_file: str):
    # Pythonからpowershellを実行
    power_command = 'Mount-DiskImage -ImagePath "{}"'.format(iso_file)
    os.system("powershell -Command" + " " + power_command)


def unmount(iso_file: str):
    # Pythonからpowershellを実行
    power_command = 'DisMount-DiskImage -ImagePath "{}"'.format(iso_file)
    os.system("powershell -Command" + " " + power_command)


def main():
    parser = argparse.ArgumentParser(
        description="""
isoファイルの中身を表示します。

指定されたisoファイルをマウントして、その情報(サイズや更新日付)を表示します。
マスター出図票を作成する際に、表示された情報をコピーします。
マウント→中身表示→アンマウントの流れで実行しますが、マウントされる
ドライブレターは環境依存なので予め試した上で指定してください。
    """,
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument("iso", help="isoファイルのフルパスを指定")
    parser.add_argument("drive", help="マウントされるドライブレターを指定(環境依存なので予め確かめること)")
    args = parser.parse_args()

    mount(args.iso)
    print_files(args.drive)
    unmount(args.iso)


# sample call
# python wintools\listiso.py c:\workspace\wintools\test.iso E
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
