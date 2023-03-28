import os
from app import create_app, db
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from config import Config

app = create_app()
app.config.from_object(Config)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()
