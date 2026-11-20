from app import db
from app.users.models import User
from tests.base import BaseTestCase


class ViewsTests(BaseTestCase):
    """Перевірка коректного завантаження сторінок."""

    def test_register_page_loads(self):
        response = self.client.get('/users/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Реєстрація', response.get_data(as_text=True))

    def test_login_page_loads(self):
        response = self.client.get('/users/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Вхід', response.get_data(as_text=True))

    def test_account_requires_login(self):
        response = self.client.get('/users/account')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/users/login', response.headers['Location'])

    def test_users_list_requires_login(self):
        response = self.client.get('/users/list')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/users/login', response.headers['Location'])


class RegistrationTests(BaseTestCase):
    """Збереження користувача в БД при реєстрації."""

    def test_register_saves_user_with_hashed_password(self):
        response = self.client.post('/users/register', data={
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'secret123',
            'confirm_password': 'secret123',
        })
        self.assertEqual(response.status_code, 302)

        with self.app.app_context():
            saved = db.session.scalar(
                db.select(User).where(User.email == 'new@example.com')
            )
            self.assertIsNotNone(saved)
            self.assertEqual(saved.username, 'newuser')
            self.assertNotEqual(saved.password, 'secret123')
            self.assertTrue(saved.password.startswith('$2b$'))
            self.assertTrue(saved.check_password('secret123'))

    def test_register_duplicate_email(self):
        self.create_user()
        response = self.client.post('/users/register', data={
            'username': 'another',
            'email': 'test@example.com',
            'password': 'secret123',
            'confirm_password': 'secret123',
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('вже існує', response.get_data(as_text=True))
        with self.app.app_context():
            self.assertEqual(len(db.session.scalars(db.select(User)).all()), 1)

    def test_register_duplicate_username(self):
        self.create_user()
        response = self.client.post('/users/register', data={
            'username': 'testuser',
            'email': 'other@example.com',
            'password': 'secret123',
            'confirm_password': 'secret123',
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('вже існує', response.get_data(as_text=True))

    def test_register_password_mismatch(self):
        response = self.client.post('/users/register', data={
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'secret123',
            'confirm_password': 'different',
        })
        self.assertEqual(response.status_code, 200)
        with self.app.app_context():
            self.assertIsNone(db.session.scalar(db.select(User)))


class LoginLogoutTests(BaseTestCase):
    """Вхід і вихід користувача."""

    def test_login_success(self):
        self.create_user()
        response = self.login(follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Welcome, testuser!', response.get_data(as_text=True))

    def test_login_wrong_password(self):
        self.create_user()
        response = self.login(password='wrongpass')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Invalid email or password',
                      response.get_data(as_text=True))

    def test_login_unknown_email(self):
        response = self.login(email='nobody@example.com')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Invalid email or password',
                      response.get_data(as_text=True))

    def test_logout(self):
        self.create_user()
        self.login()
        response = self.client.post('/users/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('successfully logged out',
                      response.get_data(as_text=True))

        response = self.client.get('/users/account')
        self.assertEqual(response.status_code, 302)

    def test_navbar_changes_after_login(self):
        self.create_user()
        guest_page = self.client.get('/users/login').get_data(as_text=True)
        self.assertIn('Реєстрація', guest_page)

        self.login()
        auth_page = self.client.get('/users/account').get_data(as_text=True)
        self.assertIn('Вихід', auth_page)
        self.assertNotIn('Реєстрація', auth_page)