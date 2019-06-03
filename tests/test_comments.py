import unittest
from app.models import Comments,User
from flask_login import current_user
from app import db
class TestComments(unittest.TestCase):

    def setUp(self):
        self.user_James = User(username = 'James',password = 'potato', email = 'james@ms.com')
        self.new_comment = Comments(pitches_id=12345,opinion='Review for movies',user_id=1,user = self.user_James )

    def tearDown(self):
        Comments.query.delete()
        User.query.delete()
    
    def test_instance(self):
        self.assertTrue(isinstance(self.new_comment,Comments))

    def test_check_instance_variables(self):
        self.assertEquals(self.new_comment.pitches_id,12345)
        self.assertEquals(self.new_comment.opinion,'Review for movies')
        self.assertEquals(self.new_comment.user_id,1)
        self.assertEquals(self.new_review.user,self.user_James)

    def test_save_comment(self):
        self.new_comment.save_comment()
        self.assertTrue(len(Comments.query.all())>0)


    def test_get_comment_by_id(self):

        self.new_comment.save_comment()
        got_comments = Comments.get_comments(12345)
        self.assertTrue(len(got_comments) == 1)
