import os
from app import create_app, db
from flask_migrate import Migrate, init, migrate, upgrade
import sys
from config import Config

app = create_app()
app.config.from_object(Config)

def init_migrate_upgrade():
    with app.app_context():
        migrate_instance = Migrate(app, db)
        
        if not os.path.exists("migrations"):
            print("Initializing the migration repository...")
            init(directory="migrations")
            print("Migration repository initialized.")
        else:
            print("Migration repository already exists.")
        
        print("Creating a new migration script...")
        migrate(directory="migrations")

        print("Applying the migration script...")
        upgrade(directory="migrations")
        print("Success.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "init_migrate_upgrade":
        init_migrate_upgrade()
    else:
        print("Usage: python manage.py init_migrate_upgrade")