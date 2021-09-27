import glob
from fire import Fire

from wintools import dump_iso, mount, unmount, download_from_s3, upload_to_s3, print_info


class Iso:
    """iso utils."""

    def mount(self, iso_file: str):
        """mount iso file.

        Parameters
        ----------
        iso_file : str
            iso file path
        """
        mount(iso_file)

    def unmount(self, iso_file: str):
        """unmount iso file.

        Parameters
        ----------
        iso_file : str
            iso file path
        """
        unmount(iso_file)

    def dump(self, target_dir: str):
        """mount iso files to windows drive and print file infomation include iso.

        指定されたディレクトリにあるisoファイルをマウントして、その情報(サイズや更新日付)を表示します。
        適当なドライブレター（E:からI:）に対してマウント→中身表示→アンマウントの流れで実行します。

        Parameters
        ----------
        target_dir : str
            directory path include iso files
        """
        isos = glob.glob("{}/*".format(target_dir))
        for iso in isos:
            dump_iso(iso)


class S3:
    """s3 utils."""

    def download(self, s3_uri: str, save_path: str = ".", aws_profile: str = "default"):
        """download file or directory from s3.

        Parameters
        ----------
        s3_uri : str
            s3 uri
        save_path : str, optional
            download and save path (local), by default "."
        aws_profile : str, optional
            aws profile name, by default "default"
        """
        download_from_s3(save_path, s3_uri, aws_profile)

    def upload(self, target_path: str, s3_uri: str, aws_profile: str = "default"):
        """upload file or directory to s3.

        Parameters
        ----------
        target_path : str
            file or directory path to upload (local)
        s3_uri : str
            s3 uri
        aws_profile : str, optional
            aws profile name, by default "default"
        """
        upload_to_s3(target_path, s3_uri, aws_profile)


class File:
    """file utils."""

    def dump(self, target_path: str):
        """dump file or directory

        Parameters
        ----------
        target_path : str
            file or directory path
        """
        print_info(target_path)


class Command:
    """mozkzki's windows tool."""

    iso = Iso()
    s3 = S3()
    file = File()


def run():
    Fire(Command())
