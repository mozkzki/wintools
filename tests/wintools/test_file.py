from wintools import print_files_info, print_info


FILES = ["./tests/resources/test.iso"]


class TestFile:
    def test_print_files_info(self):
        print_files_info(FILES)

    def test_print_info(self):
        print_info("./tests")
