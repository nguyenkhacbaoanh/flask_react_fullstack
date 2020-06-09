from flask_script import Manager
from project import create_app, db
import unittest
from project.api.models import User

app = create_app()
manager = Manager(create_app)

@manager.command
def run(host="0.0.0.0"):
    app.run(host=host)

@manager.command
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@manager.command
def seed_db():
    db.session.add(User(username='anh', email='anh.nguyen@gmail.com'))
    db.session.add(User(username='trinh', email='trinh.nguyen@gmail.com'))
    db.session.commit()

@manager.command
def test():
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

import coverage

COV = coverage.coverage(
    branch=True,
    include='project/*',
    omit=[
        'project/tests/*',
        'project/config.py',
    ]
)

COV.start()

@manager.command
def cov():
    tests = unittest.TestLoader().discover('project/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    return 1


if __name__ == '__main__':
    manager.run()
