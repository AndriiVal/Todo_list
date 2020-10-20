import unittest
from webapp import app, db
from webapp.models import Users, Tasks,Projects
from datetime import datetime

class UserModelCase(unittest.TestCase):
	def setUp(self):
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()

	def test_password_hashing(self):
		u = Users(username='Marat')
		u.set_password('gimmegimme')
		self.assertFalse(u.check_password('notgimme'))
		self.assertTrue(u.check_password('gimmegimme'))

	def test_check_name(self):
		u = Projects(project_name='Marat')
		self.assertFalse(u.if_name_is_empty())
		self.assertTrue(u.if_name_is_valid())

	def test_task_date(self):
		t = Tasks(task_name='Idont know unittest',date=datetime.utcnow())
		self.assertFalse(t.date_time_now())

if __name__ == '__main__':
	unittest.main(verbosity=2)
	