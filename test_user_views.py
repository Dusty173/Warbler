"""User View tests"""

import os
from unittest import TestCase
from models import db, connect_db, User

os.environ["DATABASE_URL"] = "postgresql:///warbler-test"

from app import app, CURR_USER_KEY

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False

class UserViewTestCase(TestCase):
    """Tests views for user"""
    
    def setUp(self):
        """Set up"""
        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        self.user1 = User.signup(
            email = "testdude@mrguy.com",
            username= "testerguy",
            password = "password",
            image_url = None
        )

        self.user1_id = 73
        self.user1.id = self.user1_id

        self.user2 = User.signup(
            email = "testdude@mrguy.com",
            username= "testerguy",
            password = "password",
            image_url = None
        )

        self.user2_id = 23
        self.user2.id = self.user2_id


    def tearDown(self):
        """Teardown"""
        db.session.rollback()

    def test_users(self):
        """ensure users exist"""

        with self.client as c:
            res = c.get("/users")

            self.assertIn("user1", str(res.data))
            self.assertIn("user2", str(res.data))
    
    def test_user_show(self):
        """Check for specific user"""
        with self.client as c:
            res = c.get(f"/users/{self.user1_id}")

            self.assertEqual(res.status_code, 200)

            self.assertIn("user1", str(res.data))

