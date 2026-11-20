import unittest

from app import create_app, db
from app.users.models import User


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def create_user(self, username='testuser', email='test@example.com',
                    password='secret123'):
        with self.app.app_context():
            user = User(
                username=username,
                email=email,
                password=User.hash_password(password),
            )
            db.session.add(user)
            db.session.commit()

    def login(self, email='test@example.com', password='secret123',
              follow_redirects=False):
        return self.client.post(
            '/users/login',
            data={'email': email, 'password': password},
            follow_redirects=follow_redirects,
        )