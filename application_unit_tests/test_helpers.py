from unittest import TestCase
import CLI_helpers


class TestCliHelpers(TestCase):
    def test_G92_A0_B0(self):
        # should not raise exception
        printtime = CLI_helpers.printing_time('G92 A0 B0')

