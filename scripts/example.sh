#!/bin/sh

# ------
# S3
# ------
# download directory
wintools s3 download s3://mozkzki/wintools/sample/ ./out
# download file
wintools s3 download s3://mozkzki/wintools/sample/LICENSE ./out

# ------
# ISO
# ------
# dump iso
wintools iso dump ./tests/resources/
# mount
wintools iso mount ./tests/resources/test.iso
# unmount
wintools iso unmount ./tests/resources/test.iso

# ------
# File
# ------
wintools file dump ./tests
