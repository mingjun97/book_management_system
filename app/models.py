from datetime import datetime
from app import db
from flask_login import UserMixin


class Base():
    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}


class Book(db.Model, Base):
    __tablename__ = 'books'
    id = db.Column(db.String(5), primary_key=True, nullable=False)
    type = db.Column(db.String(256))
    name = db.Column(db.String(256))
    publisher = db.Column(db.String(256))
    year = db.Column(db.Integer, default=2010)
    author = db.Column(db.String(256))
    price = db.Column(db.Float)
    amount = db.Column(db.Integer)
    store = db.Column(db.Integer, default=amount)


class Reader(db.Model, Base):
    __tablename__ = 'readers'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(256))
    department = db.Column(db.String(256))
    type = db.Column(db.String(256))


class Admin(db.Model, UserMixin, Base):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    password = db.Column(db.String(256))
    name = db.Column(db.String(256))
    contact = db.Column(db.String(256))

    @staticmethod
    def get(userid):
        user = Admin.query.filter_by(id=userid).first()
        if user is None:
            return user
        else:
            return user


class Record(db.Model, Base):
    __tablename__ = 'records'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    reader_id = db.Column(db.Integer, db.ForeignKey('readers.id'))
    book_id = db.Column(db.String(5), db.ForeignKey('books.id'))
    borrow_date = db.Column(db.DateTime, default=datetime.now)
    receive_date = db.Column(db.DateTime, default=None, nullable=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admins.id'))


