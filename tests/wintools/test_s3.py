import pytest
import os
import shutil

from wintools import download_from_s3, upload_to_s3, sepalate_s3_key


class TestS3:
    def test_download_and_upload(self):
        download_from_s3("./out", "s3://mozkzki/wintools/sample/")
        upload_to_s3("./out", "s3://mozkzki/wintools/sample/")

    @pytest.mark.parametrize(
        "s3_key, expected_bucket, expected_path",
        [
            ("s3://mozkzki/wintools/sample/", "mozkzki", "wintools/sample/"),
            ("s3://mozkzki/wintools/sample", "mozkzki", "wintools/sample"),
            ("mozkzki/wintools/sample/", "mozkzki", "wintools/sample/"),
            ("mozkzki/wintools/sample", "mozkzki", "wintools/sample"),
        ],
    )
    def test_sepalate_s3_key_1(self, s3_key, expected_bucket, expected_path):
        bucket, path = sepalate_s3_key(s3_key)
        assert bucket == expected_bucket
        assert path == expected_path

    def test_download(self):
        if os.path.exists("./out"):
            shutil.rmtree("./out")

        download_from_s3(
            save_path="./out", s3_uri="s3://mozkzki/wintools/sample/", aws_profile="default"
        )
        assert os.path.exists("./out/coverage.xml") is True
        assert os.path.exists("./out/LICENSE") is True
