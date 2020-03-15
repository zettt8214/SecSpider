import os
from app import create_app,db
from app.models import User,Role,Info
from flask_migrate import Migrate


app=create_app('development')
migrate=Migrate(app,db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db,User=User,Role=Role,Info=Info)


if __name__ == '__main__':
    app.run("0.0.0.0")

