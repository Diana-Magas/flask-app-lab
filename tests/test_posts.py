import unittest
from datetime import datetime

from app import create_app, db
from app.posts.models import Post


class PostTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def make_post(self, title="Test title", content="Test content",
                  category="tech", is_active=True):
        post = Post(title=title, content=content,
                    category=category, is_active=is_active)
        db.session.add(post)
        db.session.commit()
        return post

    def get_by_title(self, title):
        return db.session.scalar(db.select(Post).where(Post.title == title))

    def count_posts(self):
        return len(db.session.scalars(db.select(Post)).all())


    def test_create_post(self):
        response = self.client.post("/post/create", data={
            "title": "My first post",
            "content": "This is TDD!",
            "is_active": "y",
            "publish_date": "2026-11-07T12:00",
            "category": "tech",
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"has been added", response.data)

        post = self.get_by_title("My first post")
        self.assertIsNotNone(post)
        self.assertEqual(post.content, "This is TDD!")
        self.assertEqual(post.category, "tech")
        self.assertEqual(post.posted, datetime(2026, 11, 7, 12, 0))

    def test_create_post_form_page(self):
        response = self.client.get("/post/create")
        self.assertEqual(response.status_code, 200)

    def test_create_post_invalid(self):
        response = self.client.post("/post/create", data={
            "title": "",
            "content": "",
            "publish_date": "2026-11-07T12:00",
            "category": "tech",
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.count_posts(), 0)

    def test_list_posts(self):
        self.make_post(title="First post")
        self.make_post(title="Second post")

        response = self.client.get("/post")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"First post", response.data)
        self.assertIn(b"Second post", response.data)

    def test_list_hides_inactive_posts(self):
        self.make_post(title="Visible post")
        self.make_post(title="Hidden post", is_active=False)

        response = self.client.get("/post")
        self.assertIn(b"Visible post", response.data)
        self.assertNotIn(b"Hidden post", response.data)

    def test_view_post_detail(self):
        post = self.make_post(title="Detail title", content="Detail content")

        response = self.client.get(f"/post/{post.id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Detail title", response.data)
        self.assertIn(b"Detail content", response.data)

    def test_update_form_prefilled(self):
        post = self.make_post(title="Old title")

        response = self.client.get(f"/post/{post.id}/update")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Old title", response.data)

    def test_update_post(self):
        post = self.make_post(title="Old title", content="Old content")
        post_id = post.id

        response = self.client.post(f"/post/{post_id}/update", data={
            "title": "New title",
            "content": "New content",
            "is_active": "y",
            "publish_date": "2026-11-08T10:30",
            "category": "news",
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"updated", response.data)

        db.session.expire_all()
        updated = db.session.get(Post, post_id)
        self.assertEqual(updated.title, "New title")
        self.assertEqual(updated.content, "New content")
        self.assertEqual(updated.category, "news")

    def test_delete_confirm_page(self):
        post = self.make_post(title="To delete")

        response = self.client.get(f"/post/{post.id}/delete")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"To delete", response.data)
        self.assertEqual(self.count_posts(), 1)   

    def test_delete_post(self):
        post = self.make_post(title="To delete")
        post_id = post.id

        response = self.client.post(f"/post/{post_id}/delete",
                                    follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"deleted", response.data)

        db.session.expire_all()
        self.assertIsNone(db.session.get(Post, post_id))

    def test_404_not_found(self):
        response = self.client.get("/post/999")
        self.assertEqual(response.status_code, 404)

    def test_404_unknown_url(self):
        response = self.client.get("/no-such-page")
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"404", response.data)


if __name__ == "__main__":
    unittest.main()