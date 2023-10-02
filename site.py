from flask import render_template, request, redirect, url_for, session


from app import app
from string import digits
from random import choice
from database import *
from base64 import b64encode

from sqlalchemy import desc, or_

from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

def generate_id():
    result = ""
    for _ in range(0, 5):
       result += choice(str(digits))
    return int(result)


login_manager = LoginManager(app)
login_manager.login_view = 'login'

class UserLogin(UserMixin):
    pass

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        admin = Admin.query.filter_by(name=username).first()
        if admin and admin.check_password(password):
            login_user(admin)
            return redirect(url_for('admin.index'))
    else:
        if current_user.is_authenticated:
            if current_user.is_admin():
                return redirect(url_for('admin.index'))
            else:
                return redirect('/')
    return render_template('admin_login.html')

@app.route("/admin_logout")
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route("/")
def passby():
    return redirect(url_for('home', lang='en'))

@app.route("/<lang>/")
def home(lang):
    if lang == "ua":
        categories = Category.query.all()
        last_items = Item.query.order_by(desc(Item.dateadded)).limit(6).all()
        return render_template('ua/home.html', categories=categories, items=last_items, b64encode=b64encode)
    if lang == "de":
        categories = Category.query.all()
        last_items = Item.query.order_by(desc(Item.dateadded)).limit(6).all()
        return render_template('de/home.html', categories=categories, items=last_items, b64encode=b64encode)

    if lang == "en":
        categories = Category.query.all()
        last_items = Item.query.order_by(desc(Item.dateadded)).limit(6).all()
        return render_template('en/home.html', categories=categories, items=last_items, b64encode=b64encode) 

    if lang == "ru":
        categories = Category.query.all()
        last_items = Item.query.order_by(desc(Item.dateadded)).limit(6).all()
        return render_template('ru/home.html', categories=categories, items=last_items, b64encode=b64encode)               
            
    else:
        return "wrong"


@app.route("/<lang>/all-products/", methods=["GET","POST"])
def items(lang):
    page = request.args.get('page', 1, type=int)

    query_categories = Category.query.all()

    if lang == "ua":
        if "q" in request.args:
            q = request.args["q"]
            print(q.capitalize())
            items = Item.query.filter(or_(Item.name_ua.contains(q.capitalize()), Item.name_ua.contains(q), Item.name_ua.contains(q.lower()))).order_by(desc(Item.dateadded)).paginate(page=page, per_page=9)

        else:
            items = Item.query.order_by(desc(Item.dateadded)).paginate(page=page, per_page=9)

        if request.method == "POST":
            q = request.form["search_request"]
            return redirect(url_for('items', q=q, lang=lang))

        return render_template("ua/items.html", items=items, categories=query_categories,b64encode=b64encode)
    
    if lang == "de":
        if "q" in request.args:
            q = request.args["q"]
            print(q.capitalize())
            items = Item.query.filter(or_(Item.name_ge.contains(q.capitalize()), Item.name_ge.contains(q), Item.name_ge.contains(q.lower()))).order_by(desc(Item.dateadded)).paginate(page=page, per_page=9)

        else:
            items = Item.query.order_by(desc(Item.dateadded)).paginate(page=page, per_page=9)

        if request.method == "POST":
            q = request.form["search_request"]
            return redirect(url_for('items', q=q, lang=lang))

        return render_template("de/items.html", items=items, categories=query_categories,b64encode=b64encode)

    if lang == "en":
        if "q" in request.args:
            q = request.args["q"]
            print(q.capitalize())
            items = Item.query.filter(or_(Item.name_en.contains(q.capitalize()), Item.name_en.contains(q), Item.name_en.contains(q.lower()))).order_by(desc(Item.dateadded)).paginate(page=page, per_page=9)

        else:
            items = Item.query.order_by(desc(Item.dateadded)).paginate(page=page, per_page=9)

        if request.method == "POST":
            q = request.form["search_request"]
            return redirect(url_for('items', q=q, lang=lang))

        return render_template("en/items.html", items=items, categories=query_categories,b64encode=b64encode) 

    if lang == "ru":
        if "q" in request.args:
            q = request.args["q"]
            items = Item.query.filter(or_(Item.name_ru.contains(q.capitalize()), Item.name_ru.contains(q), Item.name_ru.contains(q.lower()))).order_by(desc(Item.dateadded)).paginate(page=page, per_page=9)

        else:
            items = Item.query.order_by(desc(Item.dateadded)).paginate(page=page, per_page=9)

        if request.method == "POST":
            q = request.form["search_request"]
            return redirect(url_for('items', q=q, lang=lang))

        return render_template("ru/items.html", items=items, categories=query_categories,b64encode=b64encode)       

    else:
        return "wrong"

@app.route('/<lang>/categories/<int:cat_id>', methods=["GET","POST"])
def categories(lang,cat_id):
    page = request.args.get('page', 1, type=int)
    query_categories = Category.query.all()
    cat_id = int(cat_id)

    if lang == "ua":
        if "q" in request.args:
            q = request.args["q"]
            items = Item.query.filter(Item.category_id == cat_id, or_(Item.name_ua.contains(q.capitalize()), Item.name_ua.contains(q), Item.name_ua.contains(q.lower()))).order_by(desc(Item.dateadded)).paginate(page=page, per_page=9)
        else:
            items = Item.query.filter(Item.category_id == cat_id).order_by(desc(Item.dateadded)).paginate(page=page, per_page=9)
        
        if request.method == "POST":
            q = request.form["search_request"]
            return redirect(url_for(f'categories', lang='ua',cat_id=cat_id,q=q))
        return render_template("ua/items.html", items=items, categories=query_categories,b64encode=b64encode)

    if lang == "de":
        if "q" in request.args:
            q = request.args["q"]
            items = Item.query.filter(Item.category_id == cat_id, or_(Item.name_ge.contains(q.capitalize()), Item.name_ge.contains(q), Item.name_ge.contains(q.lower()))).order_by(desc(Item.dateadded)).paginate(page=page, per_page=9)
        else:
            items = Item.query.filter(Item.category_id == cat_id).order_by(desc(Item.dateadded)).paginate(page=page, per_page=9)
        
        if request.method == "POST":
            q = request.form["search_request"]
            return redirect(url_for(f'categories', lang='de',cat_id=cat_id,q=q))
        return render_template("de/items.html", items=items, categories=query_categories,b64encode=b64encode) 

    if lang == "en":
        if "q" in request.args:
            q = request.args["q"]
            items = Item.query.filter(Item.category_id == cat_id, or_(Item.name_en.contains(q.capitalize()), Item.name_en.contains(q), Item.name_en.contains(q.lower()))).order_by(desc(Item.dateadded)).paginate(page=page, per_page=9)
        else:
            items = Item.query.filter(Item.category_id == cat_id).order_by(desc(Item.dateadded)).paginate(page=page, per_page=9)
        
        if request.method == "POST":
            q = request.form["search_request"]
            return redirect(url_for(f'categories', lang='en',cat_id=cat_id,q=q))
        return render_template("en/items.html", items=items, categories=query_categories,b64encode=b64encode)    

    if lang == "ru":
        if "q" in request.args:
            q = request.args["q"]
            items = Item.query.filter(Item.category_id == cat_id, or_(Item.name_ru.contains(q.capitalize()), Item.name_ru.contains(q), Item.name_ru.contains(q.lower()))).order_by(desc(Item.dateadded)).paginate(page=page, per_page=9)
            

        else:
            items = Item.query.filter(Item.category_id == cat_id).order_by(desc(Item.dateadded)).paginate(page=page, per_page=9)
        
        if request.method == "POST":
            q = request.form["search_request"]
            return redirect(url_for(f'categories', lang='ru',cat_id=cat_id,q=q))
        return render_template("ru/items.html", items=items, categories=query_categories,b64encode=b64encode)                  


@app.route('/<lang>/product/<int:product_id>')
def viewproduct(lang,product_id):
    if lang == "ua":
        product = Item.query.filter(Item.id == int(product_id)).first()
        return render_template("ua/viewproduct.html", product=product, b64encode=b64encode, len=len)

    if lang == "de":
        product = Item.query.filter(Item.id == int(product_id)).first()
        return render_template("de/viewproduct.html", product=product, b64encode=b64encode, len=len)

    if lang == "en":
        product = Item.query.filter(Item.id == int(product_id)).first()
        return render_template("en/viewproduct.html", product=product, b64encode=b64encode, len=len)       

    if lang == "ru":
        product = Item.query.filter(Item.id == int(product_id)).first()
        return render_template("ru/viewproduct.html", product=product, b64encode=b64encode, len=len)                             


@app.route('/<lang>/support', methods=["GET", "POST"])
def support(lang):
    if request.method == "POST":
        email = request.form["email"]
        message = request.form["message"]

        if Message.query.filter(Message.email == email, Message.message == message).first() is None:
            new_msg = Message(email=email, message=message)
            db.session.add(new_msg)
            db.session.commit()

            return redirect(f'/{lang}/aftermessage')

        else:
            return redirect(f'/{lang}/support')

    if lang == "ua":
        return render_template("ua/support.html")
    if lang == "de":
        return render_template("de/support.html")
    if lang == "ru":
        return render_template("ru/support.html")
    if lang == "en":
        return render_template("en/support.html")


@app.route('/<lang>/aftermessage')
def aftermessage(lang):
    if lang == "ua":
        return render_template("ua/aftermessage.html")
    if lang == "de":
        return render_template("de/aftermessage.html")
    if lang == "ru":
        return render_template("ru/aftermessage.html")
    if lang == "en":
        return render_template("en/aftermessage.html")


@app.route('/<lang>/cart')
def cart(lang):
    if 'cart' not in session:
        session['cart'] = [] 

    items = []
    for item in session['cart']:
        items.append(Item.query.filter(Item.id==item).first())



    if lang == "ua":
        full_price = 0
        for item in items:
            full_price += item.price_ua
        return render_template("ua/order.html", items=items, b64encode=b64encode, full_price=full_price, len=len)   

    if lang == "de":
        full_price = 0
        for item in items:
            full_price += item.price_eur
        return render_template("de/order.html", items=items, b64encode=b64encode, full_price=full_price, len=len)

    if lang == "en":
        full_price = 0
        for item in items:
            full_price += item.price_eur
        return render_template("en/order.html", items=items, b64encode=b64encode, full_price=full_price, len=len)

    if lang == "ru":
        full_price = 0
        for item in items:
            full_price += item.price_ru
        return render_template("ru/order.html", items=items, b64encode=b64encode, full_price=full_price, len=len)   


@app.route('/<lang>/addtocart/<int:product_id>')
def addtocart(lang, product_id):
    if 'cart' not in session:
        session['cart'] = []  
    cart_list = session['cart']
    cart_list.append(product_id)
    session['cart'] = cart_list

    return redirect(url_for('cart', lang=lang))


@app.route('/delcast/<int:product_id>')
def delcast(product_id):
    lang = request.args.get('lang', 'de') 
    cart_list = session['cart']
    cart_list.remove(product_id)
    session['cart'] = cart_list
    return redirect(url_for('cart', lang=lang))

@app.route('/<lang>/clearcart')
def clearcart():
    try:
        session.pop('cart', None)
    except:
        pass

    return redirect(url_for('passby'))

with app.app_context():
    db.create_all()
    username = "admin"
    password = "admin"
    if Admin.query.filter(Admin.name == username).first() is None:
        new_admin = Admin(username, password)
        db.session.add(new_admin)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)