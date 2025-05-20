from users.serializers import UserSerializer
# from .factory import UserFactory, SuperUserFactory

import pytest

@pytest.mark.django_db
class TestUser(object):

    @pytest.mark.parametrize('email', ['a', '', None])
    def test_create_user_not_email_raise_validation_error(self, email):
        serialiser = UserSerializer(
            data={
                'email': email,
                'password': 'Password123'
            })
        assert not serialiser.is_valid()

    @pytest.mark.parametrize('password', ['', None])
    def test_create_user_not_password_raise(self, password):
        serialiser = UserSerializer(
            data={
                'email': 'test@example.com',
                'password': password
            })
        assert not serialiser.is_valid()

    def test_create(self):
        serialiser = UserSerializer(
            data={
                'email': 'test@example.com',
                'password': 'Password123',
                'role': 'PM',
            }
        )
        assert serialiser.is_valid()
        user = serialiser.save()
        assert user.role == 'ACC'
