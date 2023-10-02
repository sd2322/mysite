from flask import Flask, request

from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose

from flask_login import current_user

from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import desc
from base64 import b64encode
from deep_translator import GoogleTranslator


app = Flask(__name__, static_folder='static')
app.config.from_pyfile('config.py')    


from database import db, Category, Item, ItemImage

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.is_admin()
        else:
            return False

class AddCategoryView(BaseView):
    @expose('/', methods=["GET","POST"])
    def index(self):
        if request.method == "POST":
            category_ua = request.form["category_ua"]
            category_en = request.form["category_en"]
            category_ru = request.form["category_ru"]
            category_ge = request.form["category_ge"]
            if Category.query.filter_by(name_ua=category_ua, name_en=category_en).first() is None:
                new_category = Category(name_ua=category_ua, name_en=category_en, name_ru=category_ru, name_ge=category_ge)
                db.session.add(new_category)
                db.session.commit()
            else:
                print("ERROR")
        return self.render('admin/addcategory.html')


"""
class DelGirlView(BaseView):
    @expose('/', methods=["GET", "POST"])
    def index(self):
        if request.method == "GET":
            try: 
                girl_id = request.args['id']
                q_girl = Girl.query.filter(Girl.id == girl_id).first()
                if q_girl:
                    db.session.delete(q_girl)
                    db.session.commit()
            except Exception as e:
                print(e)
        #id = request.args.get('page', "", type=int)
        girls = Girl.query.order_by(desc(Girl.dateadded)).all()
        return self.render('admin/delgirl.html', girls=girls, b64encode=b64encode)"""


class AddItemView(BaseView):
    @expose('/', methods=["GET", "POST"])
    def index(self):
        categories = Category.query.all()
        if request.method == "POST":
            name_ua = request.form["name_ua"]
            
            name_ge = GoogleTranslator(source='uk', target='de').translate(name_ua)
            name_ru = GoogleTranslator(source='uk', target='ru').translate(name_ua)
            name_eng = GoogleTranslator(source='uk', target='en').translate(name_ua)

            price_ua = request.form["price_ua"]
            price_ru = request.form["price_ru"]
            price_eur = request.form["price_eur"]

            desc_ua = request.form["desc"]
            desc_ge = GoogleTranslator(source='uk', target='de').translate(desc_ua)
            desc_ru = GoogleTranslator(source='uk', target='ru').translate(desc_ua)
            desc_eng = GoogleTranslator(source='uk', target='en').translate(desc_ua)


            item_cat_id = request.form["obj_type"]
            files = request.files.getlist("form_file")

            errors = []
            retry = False

            if len(files) > 3:
                errors.append("Максимальна кількість фото: 3")
                retry = True

            
            new_item = Item(name_ua=name_ua, name_en=name_eng, name_ru=name_ru, name_ge=name_ge,
                price_ua=price_ua, price_ru=price_ru, price_eur=price_eur,  
                desc_ua=desc_ua, desc_en=desc_eng, desc_ru=desc_ru, desc_ge=desc_ge, category_id=item_cat_id) 
            db.session.add(new_item)
            query_item = Item.query.filter_by(name_ua=name_ua, price_ua=price_ua, category_id=item_cat_id).first()

            for file in files:
                new_file = ItemImage(item_id=query_item.id, filename=file.filename, data=file.read())
                db.session.add(new_file)

            db.session.commit()
        return self.render('admin/additem.html', categories=categories)

admin = Admin(app, name='Admin', template_mode='bootstrap4',index_view=MyAdminIndexView())

admin.add_view(ModelView(Category, db.session, category='Категорії'))
admin.add_view(ModelView(Item, db.session))
admin.add_view(AddCategoryView('', endpoint='addcategory'))
admin.add_view(AddItemView('', endpoint='additem'))
