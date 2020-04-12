import os
import sys
import argparse
import logging
import pyperclip
import shutil
from boto3.session import Session
from botocore.errorfactory import ClientError

S3_BUCKET = "magarimame"
AWS_PROFILE = "home"


def main():
    parser = argparse.ArgumentParser(
        description="""
    ファイルやフォルダをS3にアップします。
    """
    )

    parser.add_argument("path", help="アップロード対象のファイルパスやフォルダパス")

    args = parser.parse_args()

    # log設定
    formatter = "%(asctime)s : %(levelname)s : %(message)s"
    # ログレベルを DEBUG に変更
    logging.basicConfig(level=logging.INFO, format=formatter)

    upload(args.path)


def upload(path: str) -> None:
    if not os.path.exists(path):
        logging.error("target not found. path={}".format(path))
        sys.exit(1)

    # ディレクトリの場合、圧縮
    if os.path.isdir(path):
        logging.info("target is dir. zip start..")
        shutil.make_archive(path, "zip", root_dir=path)
        path = path + ".zip"

    logging.info("{} -----> s3://{}".format(path, S3_BUCKET))
    basename = os.path.basename(path)

    # アップロード
    cmd = "aws s3 cp {} s3://{} --profile {}".format(path, S3_BUCKET, AWS_PROFILE)
    logging.info(cmd)
    os.system(cmd)

    # アップロードに成功したらs3パスをクリップボードへコピー
    if is_s3_key_exists(basename):
        logging.info("----------------------")
        logging.info("SUCCESS")
        logging.info("----------------------")
        result = "s3://{}/{}   ( copied to clipboad. )".format(S3_BUCKET, basename)
        logging.info(result)
        logging.info("----------------------")
        pyperclip.copy(result)
    else:
        logging.error("!!!!!!!!!!!!!!!!!!!!!!")
        logging.error("ERROR")
        logging.error("!!!!!!!!!!!!!!!!!!!!!!")


def is_s3_key_exists(key: str) -> bool:
    try:
        session = Session(profile_name=AWS_PROFILE)
        s3 = session.client("s3")
        s3.head_object(Bucket=S3_BUCKET, Key=key)
        logging.info("key is exists. s3://{}/{}".format(S3_BUCKET, key))
        return True
    except ClientError:
        logging.error("key is not exists. s3://{}/{}".format(S3_BUCKET, key))
        return False


if __name__ == "__main__":
    main()
