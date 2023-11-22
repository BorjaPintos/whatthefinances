import unittest

from src.version.application.getversion import GetVersion
from src.version.domain.version import Version


class GetVersionTest(unittest.TestCase):

    def test_get_version(self):
        domain_object = Version()
        use_case = GetVersion()
        returned_value = use_case.execute()
        self.assertEqual(domain_object.get_version(), returned_value.get_version())
