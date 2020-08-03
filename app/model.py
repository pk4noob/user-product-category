from flask import Flask
from extensions.extensions import db,ma
from werkzeug.security import check_password_hash ,generate_password_hash

class User(db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer(),primary_key=True)
    name = db.Column(db.String(),nullable=False)
    surname = db.Column(db.String(),nullable=False)
    nickname = db.Column(db.String(),nullable=False)
    password = db.Column(db.String(),nullable=False)
    email = db.Column(db.String(),unique=True,nullable=False)

    def set_password(self):
        self.password = generate_password_hash(self.password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def savedb(self):
        db.session.add(self)
        db.session.commit()
    def deletedb(self):
        db.session.delete(self)
        db.session.commit()
    def update(self,**kwargs):
        for key,value in kwargs.items():
            setattr(self,key,value)
        self.savedb() 

class Product(db.Model):
    __tablename__ = 'PRoduct'
    id = db.Column(db.Integer(),primary_key=True)
    name = db.Column(db.String(),nullable=False)
    user_id= db.Column(db.Integer(), db.ForeignKey(
        'User.id'), nullable=False)
    category_id = db.Column(db.Integer(),db.ForeignKey('Category.id'), nullable=False)

    def savedb(self):
        db.session.add(self)
        db.session.commit()

    def deletedb(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.savedb()

class Category(db.Model):
    __tablename__ = "Category"
    id = db.Column(db.Integer(),primary_key=True)
    name = db.Column(db.String(),nullable=False)
    
    def savedb(self):
        db.session.add(self)
        db.session.commit()
    def deletedb(self):
        db.session.delete(self)
        db.session.commit()
    def update(self,**kwargs):
        for key,value in kwargs.items():
            setattr(self,key,value)
        self.savedb()
