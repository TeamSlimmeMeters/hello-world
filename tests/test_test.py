import unittest
import pytest


class TestRun(unittest.TestCase):

    def setUp(self) -> None:
        self.meter_id = 1

    def test_init(self):
        assert (2 < 5)
    