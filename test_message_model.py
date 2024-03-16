"""Message Model tests"""

from app import app

import os
from unittest import TestCase
from models import db, Message, User, Follows, Likes

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

db.drop_all()
db.create_all()

class MessageTestCase(TestCase):
    """Tests Message Model"""

    def setUp(self):
        """Setup"""
        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        user1= User.signup(
            email = "testdude@mrguy.com",
            username= "testerguy",
            password = "password",
            image_url = None
        )

        msg = Message(
            text = "Hello World",
            user_id = user1.id
        )

        db.session.add(user1)
        db.session.commit()
        db.session.add(msg)
        db.session.commit()

    def tearDown(self):
        """Tear down"""
        db.session.rollback()
    
    def test_message_model(self):
        """Ensure Message exists for user"""
        user1 = User.query.get(self.user1.id)
        self.assertEqual(len(user1.messages), 1)    