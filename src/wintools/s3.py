import os
import sys
import logging
from typing import Tuple
import pyperclip
import shutil
import subprocess
from boto3.session import Session
from botocore.errorfactory import ClientError
from wintools.log import set_logger

logger = logging.getLogger(__name__)
set_logger(logger)


def download_from_s3(save_path: str, s3_uri: str = "", aws_profile: str = "default") -> None:
    if not os.path.exists(save_path):
        # 存在しなければdownload先のディレクトリを作成
        os.mkdir(save_path)
    if not os.path.isdir(save_path):
        # download先がディレクトリでない場合はエラー(既にpathとしてファイルが存在している場合)
        logger.error("download path is not directory. path={}".format(save_path))
        sys.exit(1)

    # s3 uriが未指定ならクリップボードからコピーする
    if s3_uri == "":
        s3_uri = pyperclip.paste()

    if not __is_s3_key_exists(s3_uri, aws_profile):
        # s3パスが存在しなければエラー
        sys.exit(1)

    logger.info("{} -----> {}".format(s3_uri, save_path))

    # ダウンロード
    if s3_uri.endswith("/"):
        cmd = "aws s3 cp {} {} --recursive --profile {}".format(s3_uri, save_path, aws_profile)
    else:
        cmd = "aws s3 cp {} {} --profile {}".format(s3_uri, save_path, aws_profile)

    logger.info(cmd)
    os.system(cmd)

    download_path = os.path.join(save_path, os.path.basename(s3_uri))
    logger.info("download_path: " + download_path)
    if os.path.exists(download_path):
        logger.info("----------------------")
        logger.info("SUCCESS")
        logger.info("----------------------")
        subprocess.Popen("call " + download_path, shell=True)
    else:
        logger.error("!!!!!!!!!!!!!!!!!!!!!!")
        logger.error("ERROR")
        logger.error("!!!!!!!!!!!!!!!!!!!!!!")


def upload_to_s3(target_path: str, s3_uri: str, aws_profile: str = "default") -> None:
    if not os.path.exists(target_path):
        logger.error("target path is not found. path={}".format(target_path))
        sys.exit(1)

    # ディレクトリの場合、圧縮
    if os.path.isdir(target_path):
        logger.info("target is dir. zip start..")
        shutil.make_archive(target_path, "zip", root_dir=target_path)
        target_path = target_path + ".zip"

    if not (s3_uri.startswith("s3://")):
        s3_uri = "s3://" + s3_uri
    if not (s3_uri.endswith("/")):
        s3_uri = s3_uri + "/"
    basename = os.path.basename(target_path)
    s3_uri_up_dir = s3_uri
    s3_uri_up_path = s3_uri + basename

    logger.info("{} -----> {}".format(target_path, s3_uri_up_path))

    # アップロード
    cmd = "aws s3 cp {} {} --profile {}".format(target_path, s3_uri_up_dir, aws_profile)
    logger.info(cmd)
    os.system(cmd)

    # アップロードに成功したらs3パスをクリップボードへコピー
    if __is_s3_key_exists(s3_uri_up_path, aws_profile):
        logger.info("----------------------")
        logger.info("SUCCESS")
        logger.info("----------------------")
        logger.info("{}   ( copied to clipboad. )".format(s3_uri_up_path))
        logger.info("----------------------")
        pyperclip.copy(s3_uri_up_path)
    else:
        logger.error("!!!!!!!!!!!!!!!!!!!!!!")
        logger.error("ERROR")
        logger.error("!!!!!!!!!!!!!!!!!!!!!!")


def __is_s3_key_exists(s3_uri: str, aws_profile: str = "default") -> bool:
    try:
        session = Session(profile_name=aws_profile)
        s3 = session.client("s3")
        bucket, key = sepalate_s3_key(s3_uri)
        s3.head_object(Bucket=bucket, Key=key)
        logger.info("specified s3 uri is exists. uri=s3://{}/{}".format(bucket, key))
        return True
    except ClientError:
        logger.error("specified s3 uri is not exists! uri=s3://{}/{}".format(bucket, key))
        logger.error("s3 'directory' must end with '/'")
        return False


def sepalate_s3_key(s3_key: str) -> Tuple[str, str]:
    """与えられたS3のkeyをバケットとパスに分割

    Parameters
    ----------
    s3_key : str
        S3 Key (s3://から始まった場合はトリム)

    Returns
    -------
    Tuple[str, str]
        Tuple(バケット, パス)
    """
    s3_key = s3_key.replace("s3://", "")
    splitted_s3_key = s3_key.split("/", 1)
    bucket = splitted_s3_key[0]
    path = splitted_s3_key[1]
    return (bucket, path)
