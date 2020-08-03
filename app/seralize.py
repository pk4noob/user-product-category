from flask import Flask
from extensions.extensions import db,ma
from app.model import User,Product,Category
from marshmallow import validate,fields

class UserSchema(ma.SQLAlchemyAutoSchema):
    name =fields.String(required=True,validate=[validate.Length(min=2,max=20)])
    surname =fields.String(required=True,validate=[validate.Length(min=2,max=20)])
    nickname =fields.String(required=True,validate=[validate.Length(min=2,max=20)])
    password =fields.String(required=True,validate=[validate.Length(min=8,max=40)])
    email=fields.Email(required=True)

    class Meta:
        model = User
        load_instance=True

class UpdateSchema(ma.Schema):
    name =fields.String()
    surname =fields.String()
    nickname =fields.String()
    password =fields.String()
    email=fields.Email()

class ProductSchema(ma.SQLAlchemyAutoSchema):
    name =fields.String(required=True,validate=[validate.Length(min=2,max=20)])
    # product_id=fields.String(required=True,validate=[validate.Length(min=2,max=20)])
    category_id=fields.Integer(required=True,validate=[validate.Range(min=0)])
    class Meta:
        model = Product
        inclufr_fk = True
        load_instance=True

class CategorySchema(ma.SQLAlchemyAutoSchema):
    name =fields.String(required=True,validate=[validate.Length(min=2,max=20)])
    class Meta:
        model = Category
        load_instance=True