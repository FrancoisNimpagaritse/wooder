from src.models import User
from werkzeug.security import generate_password_hash, check_password_hash


# test user creation
def test_can_create_user():
    user = User()
    user.firstname = 'testo'
    user.lastname = 'test'
    user.email = 'test@test.com'
    user.password = generate_password_hash('test123')

    assert user.firstname == 'testo'
    assert user.password != 'test123'

# test user edition
# test user deletion
# test project creation
# test project edition
# test project deletion
# test project list
