from tests.pytest.shared.environment import *
import unittest
from unittest.mock import Mock
from src.login.application.getuser import GetUser
from src.login.domain.user import User


class GetUserTest(unittest.TestCase):

    def test_get_user(self):
        domain_object = User(id=1, name="admin", encrypted_password="asdasd")
        mem_repo = Mock()
        mem_repo.get = Mock(return_value=domain_object)
        use_case = GetUser(user_repository=mem_repo)
        returned_user = use_case.execute(1)
        self.assertEqual(domain_object.get_id(), returned_user.get_id())
