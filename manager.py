# coding:utf-8
import os
from app import app_create, db
from app.models import User, SpiderLog
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

app = app_create(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, SpiderLog=SpiderLog)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()