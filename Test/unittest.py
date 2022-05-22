import unittest,os
from app import app,db
from app.models import User,gameRecord

class UserModelTest(unittest.TestCase):
    def setUp(self) -> None:
        basedir = os.path.abspath(os.path.dirname(__file__))
        self.app = app.test_client()
        db.create_all()
        u1 = User(id='00000',username='Test_User1',email='000@000.com')
        u2 = User(id='11111',username='Test_User2',email='111@111.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User.query.get("00000")
        u.set_password('test1')
        self.assertFalse(u.check_password('test'))
        self.assertTrue(u.check_password('test1'))
        print('111')

    def test_is_commited(self):
        u = User.query.get('00000')
        self.assertFalse(u.is_committed())
        gR = gameRecord(id=User.id,user_name=User.username)
        db.session.add(gR)
        db.session.flush()
        u.id = gR.id
        db.session.commit()
        self.assertTrue(u.is_committed())


if __name__ == "__main__":
    unittest.main()