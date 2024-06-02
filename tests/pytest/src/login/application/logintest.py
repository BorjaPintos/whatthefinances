from src.login.application.login import Login
from src.login.domain.exceptions.unauthorizederror import UnauthorizedError
from tests.pytest.shared.environmentpytest import *
import unittest
from unittest.mock import Mock
from src.login.domain.user import User


class LoginTest(unittest.TestCase):

    def test_login_success(self):
        domain_object = User(id=1, name="admin",
                             encrypted_password="addd55c9db8c0d868e7a826df9c58c364dda0bbd25e151f9acfaf993e73c5fb1276d119d3a11c2931aeb72fc3131a71c61edfa291cf261347e8377108fa61c22")
        self.assertEqual(domain_object.is_authenticated(), False)
        mem_repo = Mock()
        mem_repo.get = Mock(return_value=domain_object)
        use_case = Login(user_repository=mem_repo)
        returned_user = use_case.execute("admin", "test")
        self.assertEqual(returned_user.is_authenticated(), True)

    def test_login_failure(self):
        domain_object = User(id=1, name="admin",
                             encrypted_password="asdfgh")
        self.assertEqual(domain_object.is_authenticated(), False)
        mem_repo = Mock()
        mem_repo.get = Mock(return_value=domain_object)
        use_case = Login(user_repository=mem_repo)
        with pytest.raises(UnauthorizedError) as e:
            use_case.execute("admin", "test")

    def test_login_invalid_user(self):
        mem_repo = Mock()
        mem_repo.get = Mock(return_value=None)
        use_case = Login(user_repository=mem_repo)
        returned_user = use_case.execute("blabla", "test")
        self.assertEqual(returned_user, None)
