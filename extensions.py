"""
extensions.py
=============
Flask extensions are instantiated here — WITHOUT the app object.
The app is bound later via init_app() inside create_app().
This breaks the circular import:  app → routes → models → app
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db           = SQLAlchemy()
login_manager = LoginManager()