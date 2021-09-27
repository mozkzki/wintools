from wintools import mount, unmount, print_iso_files_info, dump_iso


ISO_FILE = "./tests/resources/test.iso"


class TestIso:
    def test_mount(self):
        assert mount(ISO_FILE) == 0

    def test_umount(self):
        assert unmount(ISO_FILE) == 0

    def test_print_iso_files_info(self):
        print_iso_files_info(ISO_FILE)

    def test_dump_iso(self):
        dump_iso(ISO_FILE)
