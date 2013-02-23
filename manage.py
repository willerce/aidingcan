from flask.ext.script import Manager, Server
from canku.config import DefaultConfig, ProductionConfig
from canku.extensions import db
from canku import create_app


manager = Manager(create_app(config=DefaultConfig()))

@manager.command
def drop_create():
    #Creates database tables
    db.drop_all()

    #Creates database tables
    db.create_all()


@manager.command
def createall():
    """Creates database tables"""
    db.create_all()


@manager.command
def dropall():
    """Creates database tables"""
    db.drop_all()

manager.add_command("runserver", Server())
if __name__ == "__main__":
    manager.run()
