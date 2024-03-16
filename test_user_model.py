"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)

    def test_repr_method(self):
        """Does repr method work?"""

        user= User(
            email = "testdude@mrguy.com",
            username= "testerguy",
            password = "password"
        )

        db.session.add(user)
        db.session.commit()

        self.assertEqual(repr(user), f"<User #{user.id}: testerguy, testdude@mrguy.com>")

    def test_is_following(self):
        """Testing is_following method"""

        user= User(
            email = "testdude@mrguy.com",
            username= "testerguy",
            password = "password"
        )

        user2= User(
            email = "testdude2@mrguy.com",
            username= "testerguy2",
            password = "password2"
        )

        db.session.add(user)
        db.session.add(user2)

        db.session.commit()

        # Create relationship on follows
        f = Follows(user_being_followed_id=user.id, user_following_id=user2.id)

        db.session.add(f)
        db.session.commit()

        # Test if user is_following user2
        self.assertEqual(user2.is_following(user), True)
        self.assertEqual(len(user2.following), 1)

        # Does is_following detect when user is not following user2?
        self.assertEqual(user.is_following(user2), False)

    def test_is_followed_by(self):
        """Test is_followed_by method"""

        user= User(
            email = "testdude@mrguy.com",
            username= "testerguy",
            password = "password"
        )

        user2= User(
            email = "testdude2@mrguy.com",
            username= "testerguy2",
            password = "password2"
        )

        db.session.add(user)
        db.session.add(user2)

        db.session.commit()

        # User is following User2 relationship
        f = Follows(user_being_followed_id = user2.id, user_following_id = user.id)
        
        db.session.add(f)
        db.session.commit()

        self.asserEqual(user2.is_followed_by(user), True)
        self.assertEqual(user.is_followed_by(user2), False)

    def test_create_user(self):
        """Test if user is created"""

        user= User(
            email = "testdude@mrguy.com",
            username= "testerguy",
            password = "password",
            image_url = None
        )

        db.session.add(user)
        db.session.commit()

        user_count = User.query.count()

        self.assertEqual(user_count, 1)
    
    def test_user_authentication(self):
        """Test user authentication"""

        user= User(
            email = "testdude@mrguy.com",
            username= "testerguy",
            password = "password",
            image_url = None
        )

        db.session.add(user)
        db.session.commit()

        authed_user = User.authenticate("testerguy", "password")
        unauth_user = User.authenticate("testerguy", "not_the_password")

        self.assertTrue(authed_user)
        self.assertFalse(unauth_user)