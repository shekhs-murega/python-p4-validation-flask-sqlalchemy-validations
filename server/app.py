from flask import Flask
from flask_migrate import Migrate
import sqlalchemy

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import validates

from models import db, EmailAddress

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)
base = declarative_base()  # Add this line to define the base

@app.route('/')
def index():
    return 'Validations lab'

class EmailAddress(base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True)
    email = Column(String)

    @validates('email')
    def validate_email(self, key, address):
        if '@' not in address:
            raise ValueError("failed simple email validation")
        return address

Session = sessionmaker(db)
session = Session()

base.metadata.create_all(db)

email = EmailAddress(email='banana')
session.add(email)

try:
    session.commit()
except sqlalchemy.exc.IntegrityError as e:
    print("Integrity violation blocked!")
    session.rollback()

if __name__ == '__main__':
    app.run(port=5555, debug=True)
