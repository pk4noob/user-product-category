from flask import Flask, request, jsonify
from app_init.app_factory import createAp
from flask import jsonify, current_app, request
from flask import Flask, jsonify, request
from http import HTTPStatus
import os
from werkzeug.security import generate_password_hash
import warnings
from app.seralize import ProductSchema, CategorySchema,UserSchema,UpdateSchema
from app.model import User,Product, Category
from http import HTTPStatus
from marshmallow import ValidationError
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)


warnings.simplefilter("ignore")
settings_name = os.getenv("settings")
app = createAp(settings_name)

@app.route("/user",methods=["POST"])
def createUser():
    data = request.get_json()
    try:
        x:User = UserSchema().load(data)
        x.set_password()
        x.savedb()
    except ValidationError as err:
        return jsonify(err.messages),HTTPStatus.BAD_REQUEST
    return UserSchema().jsonify(x),HTTPStatus.OK

@app.route("/category",methods=["POST"])
def createCategory():
    data = request.get_json()
    try:
        y = CategorySchema().load(data)
        y.savedb()
    except ValidationError as err:
        return jsonify(err.messages),HTTPStatus.BAD_REQUEST
    return CategorySchema().jsonify(y),HTTPStatus.OK

@app.route("/user/products",methods=["POST"])
@jwt_required
def createProduct():
    data = request.get_json()
    identtiy =  get_jwt_identity()
    try:
        user=User.query.get(identtiy)
        if user:
            z = ProductSchema().load(data)
            z.user_id = user.id
            z.savedb()
    except ValidationError as err:
        return jsonify(err.messages),HTTPStatus.BAD_REQUEST
    return ProductSchema().jsonify(z),HTTPStatus.OK



@app.route("/user",methods=["GET"])
@jwt_required
def UserGetMethods():
    identity=get_jwt_identity()
    data = User.query.filter_by(id = identity).first()
    if data:
        return UserSchema().jsonify(data),HTTPStatus.OK
    return jsonify(msg="error1"),HTTPStatus.BAD_REQUEST

@app.route("/category<int:id>",methods=["GET"])
def CategoryGetMethods(id):
    data = Category.query.filter_by(id=id).first()
    if data:
        return CategorySchema().jsonify(data),HTTPStatus.OK
    return jsonify(msg="error2"),HTTPStatus.BAD_REQUEST

@app.route("/user", methods=["GET"])
def UsercreateAll():
    dataAll = User.query.all()
    return UserSchema().jsonify(dataAll, many=True), HTTPStatus.OK

@app.route("/category", methods=["GET"])
def CategorycreateAll():
    dataAll = Category.query.all()
    return CategorySchema().jsonify(dataAll, many=True), HTTPStatus.OK

@app.route("/user", methods=["PUT"])
@jwt_required
def updateMethods():
    identity=get_jwt_identity()
    dataupdate = User.query.filter_by(id=identity).first()
    if dataupdate:
        dataa = request.get_json()
        dataupdate.update(**dataa)
        return UserSchema().jsonify(dataa), HTTPStatus.OK
    return jsonify(msg="error"), HTTPStatus.BAD_REQUEST

@app.route("/category/<int:id>",methods=["PUT"])
def UpdateCategory(id):
    dataUpdate = Category.query.filter_by(id=id).first()
    if dataUpdate:
        data = request.get_json()
        dataUpdate.update(**data)
        return CategorySchema().jsonify(data),HTTPStatus.OK
    return jsonify(mes="error"),HTTPStatus.BAD_REQUEST

@app.route("/user",methods=["DELETE"])
@jwt_required
def UserDelete():
    identity=get_jwt_identity()
    data = User.query.filter_by(id=identity).first()
    if data:
        data.deletedb()
        return jsonify(msg="silindi"),HTTPStatus.OK
    return jsonify(msg="Error"),HTTPStatus.BAD_REQUEST

@app.route("/category/<int:id>",methods=["DELETE"])
def CategoryDelete():
    data = Category.query.filter_by(id=id).first()
    if data:
        data.deletedb()
        return jsonify(msg="silindi"),HTTPStatus.OK
    return jsonify(msg="error"),HTTPStatus.BAD_REQUEST

@app.route("/user/products",methods=["GET"])
@jwt_required
def ProductGetMethods():
    identity=get_jwt_identity()
    data = Product.query.filter_by(identity()).first()
    if data:
        return ProductSchema().jsonify(data), HTTPStatus.OK
    return jsonify(msg="Error"), HTTPStatus.NOT_FOUND

@app.route("/user/products", methods=["GET"])
@jwt_required
def createAll():
    identity=get_jwt_identity()
    dataAll = Product.query.filter_by(id = identity).all()
    return ProductSchema().jsonify(dataAll, many=True), HTTPStatus.OK

@app.route("/user/products",methods=["PUT"])
@jwt_required
def ProductUpdateeMethods():
    identity=get_jwt_identity()
    dataUpdate = Product.query.filter_by(id = identity).first()
    if dataUpdate:
        data = request.get_json()
        dataUpdate.update(**data)
        return ProductSchema().jsonify(data),HTTPStatus.OK
    return jsonify(msg= "error"),HTTPStatus.BAD_REQUEST

@app.route("/user/products",methods=["DELETE"])
@jwt_required
def DeleteProductsMethodss():
    identity=get_jwt_identity()
    data = Product.query.filter_by(id= identity).first()
    if data:
        data.deletedb()
        return jsonify(msg=True),HTTPStatus.OK
    return jsonify(msg="errorrr"),HTTPStatus.BAD_REQUEST


@app.route("/user/login",methods=["POST"])
def UserLogin():
    if not request.get_json():
        return jsonify(msg="yanlis requiest"),HTTPStatus.NOT_FOUND
    email=request.json.get("email",None)
    password=request.json.get("password",None)
    if not email:
        return jsonify(msg="yanlis Email"),HTTPStatus.NOT_FOUND
    if not password:
        return jsonify(msg="yanlis password"),HTTPStatus.NOT_FOUND
    user = User.query.filter_by(email = email).first()
    if user:
        if user.check_password(password):
            access_token= create_access_token(identity=user.id)
            return jsonify (access_token=access_token),HTTPStatus.OK
    return jsonify(msg="User not found"),HTTPStatus.NOT_FOUND
        









