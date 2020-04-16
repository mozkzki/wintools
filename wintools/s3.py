import os
import sys
import argparse
import logging
import pyperclip
import shutil
import subprocess
from boto3.session import Session
from botocore.errorfactory import ClientError

S3_BUCKET = "dummy"
S3_DIR = "dummy"
AWS_PROFILE = "dummy"


def main():
    parser = argparse.ArgumentParser(
        description="""
    ファイルやフォルダをS3にアップします。
    """
    )

    parser.add_argument("path", help="アップロード対象ファイル/フォルダのフルパス")
    parser.add_argument("-b", "--bucket", help="アップロード先のS3バケット名", default=S3_BUCKET)
    parser.add_argument("-d", "--dir", help="アップロード先のS3パス", default=S3_DIR)
    parser.add_argument("-p", "--profile", help="AWSのプロファイル名", default=AWS_PROFILE)
    parser.add_argument(
        "-m", "--mode", help="アップロード or ダウンロード", default="upload", choices=["upload", "download"]
    )

    args = parser.parse_args()

    # log設定
    formatter = "%(asctime)s : %(levelname)s : %(message)s"
    # ログレベルを DEBUG に変更
    logging.basicConfig(level=logging.INFO, format=formatter)

    if args.mode == "upload":
        upload(args.path, args.bucket, args.dir, args.profile)
    else:
        download(args.path, args.bucket, args.profile)


def download(path: str, s3_bucket: str, aws_profile: str) -> None:
    if not os.path.exists(path):
        # 存在しなければdownload先のディレクトリを作成
        os.mkdir(path)
    if not os.path.isdir(path):
        # download先がディレクトリでない場合はエラー(既にpathとしてファイルが存在している場合)
        logging.error("download path is not directory. path={}".format(path))
        sys.exit(1)

    # s3パスはクリップボードからコピーする想定
    s3_key = pyperclip.paste()
    if s3_key.startswith("s3://" + s3_bucket):
        s3_key = s3_key.replace("s3://" + s3_bucket + "/", "")

    if not is_s3_key_exists(aws_profile, s3_bucket, s3_key):
        # s3パスが存在しなければエラー
        logging.error("s3 key is not exists. path=s3://{}/{}".format(s3_bucket, s3_key))
        sys.exit(1)

    logging.info("s3://{}/{} -----> {}".format(s3_bucket, s3_key, path))

    # ダウンロード
    if s3_key.endswith("/"):
        cmd = "aws s3 cp s3://{}/{} {} --recursive --profile {}".format(
            s3_bucket, s3_key, path, aws_profile
        )
    else:
        cmd = "aws s3 cp s3://{}/{} {} --profile {}".format(s3_bucket, s3_key, path, aws_profile)
    logging.info(cmd)
    os.system(cmd)

    download_path = os.path.join(path, os.path.basename(s3_key))
    logging.info("download_path:" + download_path)
    if os.path.exists(download_path):
        logging.info("----------------------")
        logging.info("SUCCESS")
        logging.info("----------------------")
        subprocess.Popen("call " + download_path, shell=True)
    else:
        logging.error("!!!!!!!!!!!!!!!!!!!!!!")
        logging.error("ERROR")
        logging.error("!!!!!!!!!!!!!!!!!!!!!!")


def upload(path: str, s3_bucket: str, s3_dir: str, aws_profile: str) -> None:
    if not os.path.exists(path):
        logging.error("target not found. path={}".format(path))
        sys.exit(1)

    # ディレクトリの場合、圧縮
    if os.path.isdir(path):
        logging.info("target is dir. zip start..")
        shutil.make_archive(path, "zip", root_dir=path)
        path = path + ".zip"

    logging.info("{} -----> s3://{}/{}".format(path, s3_bucket, s3_dir))
    basename = os.path.basename(path)

    # アップロード
    cmd = "aws s3 cp {} s3://{}/{}/ --profile {}".format(path, s3_bucket, s3_dir, aws_profile)
    logging.info(cmd)
    os.system(cmd)

    # アップロードに成功したらs3パスをクリップボードへコピー
    if is_s3_key_exists(aws_profile, s3_bucket, s3_dir + "/" + basename):
        logging.info("----------------------")
        logging.info("SUCCESS")
        logging.info("----------------------")
        result = "s3://{}/{}/{}".format(s3_bucket, s3_dir, basename)
        logging.info(result + "   ( copied to clipboad. )")
        logging.info("----------------------")
        pyperclip.copy(result)
    else:
        logging.error("!!!!!!!!!!!!!!!!!!!!!!")
        logging.error("ERROR")
        logging.error("!!!!!!!!!!!!!!!!!!!!!!")


def is_s3_key_exists(aws_profile: str, s3_bucket: str, key: str) -> bool:
    try:
        session = Session(profile_name=aws_profile)
        s3 = session.client("s3")
        s3.head_object(Bucket=s3_bucket, Key=key)
        logging.info("key is exists. s3://{}/{}".format(s3_bucket, key))
        return True
    except ClientError:
        logging.error("key is not exists. s3://{}/{}".format(s3_bucket, key))
        return False


if __name__ == "__main__":
    main()
