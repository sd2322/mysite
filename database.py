from flask_sqlalchemy import SQLAlchemy

from flask_login import UserMixin

from sqlalchemy.orm import backref

from werkzeug.security import generate_password_hash, check_password_hash

from app import app

from datetime import datetime

db = SQLAlchemy(app)

class Admin(db.Model, UserMixin):
	__tablename__ = 'admins'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(40))
	password_hash = db.Column(db.Text)

	def __init__(self, name, password):
		self.name = name 
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def is_admin(self):
		return True

class Message(db.Model):
	__tablename__ = 'messages'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(60))
	message = db.Column(db.Text)
	date = db.Column(db.DateTime, default=datetime.now)

	def __init__(self, email,message):
		self.email = email
		self.message = message


class Category(db.Model):
	__tablename__ = 'categories'
	id = db.Column(db.Integer, primary_key=True)
	name_ua = db.Column(db.String(40), unique=True)
	name_en = db.Column(db.String(40), unique=True)
	name_ru = db.Column(db.String(40), unique=True)
	name_ge = db.Column(db.String(40), unique=True)
	items = db.relationship("Item", backref="category")


	def __init__(self, name_ua, name_en, name_ru, name_ge):
		self.name_ua = name_ua
		self.name_en = name_en
		self.name_ru = name_ru
		self.name_ge = name_ge


class Item(db.Model):
	__tablename__ = 'items'
	id = db.Column(db.Integer, primary_key=True)
	name_ua = db.Column(db.String(80))
	name_en = db.Column(db.String(80))
	name_ru = db.Column(db.String(80))
	name_ge = db.Column(db.String(80))
	price_ua = db.Column(db.Integer, default=100)
	price_eur = db.Column(db.Integer, default=100)
	price_ru = db.Column(db.Integer, default=100)
	desc_ua = db.Column(db.Text)
	desc_en = db.Column(db.Text)
	desc_ru = db.Column(db.Text)
	desc_ge = db.Column(db.Text)
	dateadded = db.Column(db.DateTime, default=datetime.now)
	category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))	


	def __init__(self, name_ua, name_en, name_ru, name_ge,
		price_ua, price_ru, price_eur,  
		desc_ua, desc_en, desc_ru, desc_ge, category_id):
		self.name_ua = name_ua
		self.name_en = name_en
		self.name_ru = name_ru
		self.name_ge = name_ge
		self.price_ua = price_ua
		self.price_eur = price_eur
		self.price_ru = price_ru
		self.desc_ua = desc_ua
		self.desc_ru = desc_ru
		self.desc_en = desc_en
		self.desc_ge = desc_ge
		self.category_id = category_id


	def get_title_img(self):
		return ItemImage.query.filter(ItemImage.item_id == self.id).first()

	def has_many_images(self):
		if len(ItemImage.query.filter(ItemImage.item_id == self.id).all()) > 1:
			return True
		else:
			return False

	def get_all_images(self):
		images = ItemImage.query.filter(ItemImage.item_id == self.id).all()
		if self.get_title_img() in images:
			images.remove(self.get_title_img())
		else:
			pass
		return images

	def get_category(self):
		return Category.query.filter(Category.id == self.id).first()
		

class ItemImage(db.Model):
	__tablename__ = "item_images"
	id = db.Column(db.Integer, primary_key=True)
	item_id = db.Column(db.Integer)
	filename = db.Column(db.Text)
	data = db.Column(db.LargeBinary)

	def __init__(self, item_id, filename, data):
		self.filename = filename
		self.data = data
		self.item_id = item_id



