import os
import argparse
import logging
import pyperclip
import shutil

S3_BUCKET = "magarimame"
AWS_PROFILE = "home"


def main():
    parser = argparse.ArgumentParser(
        description="""
    ファイルやフォルダをS3にアップします。
    """
    )

    parser.add_argument("path", help="アップロード対象のファイルパスやフォルダパス")
    parser.add_argument("-t", "--test", help="何か文字列を指定")
    parser.add_argument("-m", "--mode", help="モードを指定します",
                        choices=["mode1", "mode2"])

    args = parser.parse_args()

    # log設定
    formatter = "%(asctime)s : %(levelname)s : %(message)s"
    # ログレベルを DEBUG に変更
    logging.basicConfig(level=logging.DEBUG, format=formatter)

    if args.mode == "mode1":
        logging.info("mode1")
        # do_something(args.test)
    elif args.mode == "mode2":
        logging.info("mode2")
        # do_anything(args.test)
    else:
        upload(args.path)
        # parser.print_help()


def upload(path):
    # ディレクトリの場合、圧縮
    if os.path.isdir(path):
        logging.info("target is dir. zip start..")
        shutil.make_archive(path, 'zip', root_dir=path)
        path = path + ".zip"

    logging.info("{} -----> s3://{}".format(path, S3_BUCKET))
    basename = os.path.basename(path)

    # アップロード
    cmd = "aws s3 cp {} s3://{} --profile {}".format(
        path, S3_BUCKET, AWS_PROFILE)
    logging.info(cmd)
    os.system(cmd)

    # アップロード後の確認
    cmd = "aws s3 ls s3://{}/{} --recursive --human-readable --summarize --profile {}".format(
        S3_BUCKET, basename, AWS_PROFILE)
    logging.info(cmd)
    os.system(cmd)

    # s3パスをクリップボードへコピー
    logging.info("----------------------")
    result = "s3://{}/{}   ( copied to clipboad. )".format(
        S3_BUCKET, basename)
    logging.info(result)
    logging.info("----------------------")
    pyperclip.copy(result)


if __name__ == "__main__":
    main()
