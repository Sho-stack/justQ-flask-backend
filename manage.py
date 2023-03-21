import os
import click
from flask_migrate import Migrate, init, upgrade, downgrade, migrate as flask_migrate, init as flask_init
from app import create_app, db
from app.models import User, Question, Answer

app = create_app()
migrate = Migrate(app, db)

@app.cli.command("db_create")
def db_create():
    with app.app_context():
        db.create_all()
    print("Database created")

@app.cli.command("db_drop")
def db_drop():
    with app.app_context():
        db.drop_all()
    print("Database dropped")

@app.cli.command("db_init")
def db_init():
    migrations_dir = os.path.join(os.path.dirname(__file__), 'migrations')
    if not os.path.exists(migrations_dir):
        flask_init(directory='migrations')
        print("Migrations folder created")
    else:
        print("Migrations folder already exists")

@app.cli.command("db_migrate")
def db_migrate():
    with app.app_context():
        migrations_dir = os.path.join(os.path.dirname(__file__), 'migrations')
        Migrate(app, db, directory=migrations_dir)
    print("Migration created")

@app.cli.command("db_upgrade")
def db_upgrade():
    with app.app_context():
        upgrade()
    print("Database upgraded")

@app.cli.command("db_downgrade")
def db_downgrade():
    with app.app_context():
        downgrade()
    print("Database downgraded")

if __name__ == "__main__":
    app.cli()