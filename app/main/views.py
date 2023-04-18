from datetime import datetime
from app import db,login_manager
from . import main
from .forms import UserForm,LoginForm,CarsForm,VehiclesForm,ContactForm,AddToBookingForm,CheckoutForm,BookForm
from ..models import Users,Vehicles,Cars,Booking
from flask import Flask, render_template,flash,request,redirect,url_for,session,current_app
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin,login_user,LoginManager,login_required,logout_user,current_user




@main.route('/')
def index():
    return render_template("base_home.html")

@main.route('/mobile')
def mobile():
    return render_template("base_mobile.html")

@main.route('/menu_base')
def menu_base():
    vehicles = Vehicles.query.all()
    return render_template("menu_base.html",vehicles=vehicles)

@main.route('/user/<name>')
def user(name):
    return render_template("user.html",user_name=name)

@main.route('/about')
def about():
    form = ContactForm()
    if form.validate_on_submit():
        # handle form submission here
        pass
    return render_template("about.html", form=form)

@main.route('/contact')
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        # handle form submission here
        pass
    return render_template('contact.html', form=form)


@main.route('/terms')
def terms():
    return render_template("terms.html")

@main.route('/login',methods=['GET','POST']) #post method needed for page containing forms
def login():
    form = LoginForm()
    #validating form
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user:
            # checking the hash
            if check_password_hash(user.password_hash,form.password.data):
                login_user(user)
                flash("Login Successful!")
                return redirect(url_for('main.dashboard'))
                
            else:
                flash("Wrong password -- Try again")
                return render_template("login.html",form=form)
        else:
            flash("That user doesn't exist -- Try again")
            return render_template("login.html",form=form)
    else:
        return render_template("login.html",form=form)

@main.route('/dashboard', methods=["GET","POST"])
@login_required
def dashboard():
    vehicles = Vehicles.query.all()
    return render_template("dashboard.html", active_nav='dashboard', vehicles=vehicles)

@main.route('/logout', methods=["GET","POST"])
@login_required
def logout():
    logout_user()
    flash("You are logged out!")
    return render_template("index.html")



@main.route('/add-item', methods = ['POST','GET'])
@login_required
def add_item():
    form = CarsForm(request.form)
    if form.validate_on_submit():
        cart = Cars(name=form.name.data, size = form.size.data, price = form.price.data)
        db.session.add()
        db.session.commit()
        flash("Item added successfully")
        return redirect(url_for('main.add_item'))
    else:
        return render_template("add_item.html", form=form)
        
        
   
@main.route('/cars')
@login_required
def view_cars():
    cars = Cars.query.order_by(Cars.id)
    return render_template("cars.html",cars=cars)

@main.route('/item/<int:id>')
@login_required
def item_zoom(id):
    form = CarsForm()
    item = Cars.query.get_or_404(id)
    return render_template('item.html', item=item,form=form)


@main.route('/item/delete/<int:id>')
@login_required
def delete_item(id):
    item_to_delete = Cars.query.get_or_404(id)
    id = current_user.id
    if id == 1:
        try:
            db.session.delete(item_to_delete)
            db.session.commit()
            flash("Item was deleted")
            cars = Cars.query.order_by(Cars.date_posted)
            return render_template("cars.html",cars=cars)

        
        
        except:
            flash("There was a problem deleting item..try again")
            cars = Cars.query.order_by(Cars.id)
            return render_template("cars.html",cars=cars)

    else:
         flash("Unauthorized Access")
         cars = Cars.query.order_by(Cars.date_posted)
         return render_template("cars.html",cars=cars)



@main.route('/item/edit/<int:id>', methods = ["GET","POST"])
@login_required
def edit_item(id):
    item = Cars.query.get_or_404(id)
    form = CarsForm()
    if form.validate_on_submit():
        item.name = form.name.data
       # post.author = form.author.data
        item.size = form.size.data
        item.price = form.price.data
        db.session.add(item)
        db.session.commit()
        flash("Item has been updated!")
        return redirect(url_for('main.item',id=item.id))
    
    if current_user.id == 1:
        form.name.data = item.name
    # form.author.data = post.author
        form.size.data = item.size
        form.price.data = item.price
        return render_template('edit_item.html', form=form)

    else:
        flash("Unauthorized Access")
        cars = Cars.query.order_by(Cars.date_posted)
        return render_template("cars.html",cars=cars)




@main.route('/user/add', methods =['GET','POST'])
def add_user(): 
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            # Hash password first
            hash_pw = generate_password_hash(form.password_hash.data, "sha256")
            user = Users(name=form.name.data,email=form.email.data,phone=form.phone.data,password_hash=hash_pw)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.password_hash.data = ''
        flash("User Added Sucessfully")
    #To display user names on the page 
    our_users = Users.query.order_by(Users.date_added)   
    return render_template('add_user.html',form=form,name=name,our_users=our_users)

#update database
@main.route('/update/<int:id>', methods =['GET','POST'])
@login_required
def update(id):
    form = UserForm()
    # Query the database to retrieve the existing user row
    user = Users.query.get(id)
    form.name.data = user.name
    form.email.data = user.email

    # If the form is being submitted
    if request.method == 'POST':

        # Modify the values of the retrieved user object
        user.name = request.form['name']
        user.email = request.form['email']

        # Hash the new password
        hashed_password = generate_password_hash(request.form['password_hash'], "sha256")
        user.password_hash = hashed_password

        # Commit the changes to the database
        db.session.commit()

        # Redirect to the dashboard page
        return redirect(url_for('main.dashboard'))

    # If the form is being displayed
    else:
        # Render the update template
        return render_template('update.html', user=user, form=form)

@main.route('/delete/<int:id>', methods =['GET','POST'])
@login_required
def delete(id):
    user = db.session.query(Users).get(id)
    form = UserForm(request.form)
    if request.method == "GET":
        db.session.delete(user)
        db.session.commit()
        flash("User Deleted Sucessfully")
        return render_template("add_user.html",form=form,user=user)
    
    else:
        return render_template("add_user.html",form=form,user=user)



@main.route('/menu')
@login_required
def menu():
    vehicles = Vehicles.query.all()
    return render_template('menu.html', vehicles=vehicles)


@main.route('/menu/<string:category>', methods=['GET','POST'])
@login_required
def menu_category(category):
    cars = Cars.query.filter_by(category=category).all()
    cart = [] 
    if request.method == 'POST':
        # get the item name and size from the request form
        item_name = request.form.get('item_name')
        item_size = request.form.get('item_size')

        # find the item in the list of cars
        for item in cars:
            if item.name == item_name and item.size == item_size:
                # add the item to the cart
                cart = request.form.get('cart', [])
                cart.append(item)

        # render the template with the updated cart
        return render_template('menu_category.html', cars=cars, cart=cart)


    return render_template("menu_category.html", cars=cars,cart=cart)

@main.route('/menu_base/<string:category>', methods=['GET','POST'])
def menu_category_base(category):
    cars = Cars.query.filter_by(category=category).all()
    return render_template("menu_category_base.html", cars=cars)

def get_duration_in_days(pickup_date_str, return_date_str):
    pickup_date = datetime.strptime(pickup_date_str, '%Y-%m-%d')
    return_date = datetime.strptime(return_date_str, '%Y-%m-%d')
    duration_in_days = (return_date - pickup_date).days
    return duration_in_days
    

@main.route('/add_to_cart/<int:id>', methods=['GET', 'POST'])
def add_to_cart(id):
    form = BookForm()
    item = Cars.query.get(id)
    cars = Cars.query.all()
    form.name.data = item.name

    if request.method == 'POST':
        user_id = current_user.id
        car_id = item.id
        car_price = item.price
        pickup_date = request.form.get('pickup_date')
        return_date = request.form.get('return_date')
        duration = get_duration_in_days(pickup_date_str = pickup_date , return_date_str = return_date)
        existing_booking = Booking.query.filter_by(user_id=user_id, car_id=car_id).first()

        if existing_booking:
            existing_booking.pickup_date = pickup_date
            existing_booking.return_date = return_date
            existing_booking.duration = duration  # Update duration in existing booking

        else:
            new_booking = Booking(pickup_date, return_date, duration, booking_id=user_id)
            db.session.add(new_booking)
            db.session.commit()
            print("done")
        return redirect(url_for('main.view_cart'))
    return render_template('add_to_cart.html', form=form, cars=cars, item=item)


from datetime import datetime

@main.route('/cart')
def view_cart():
    # Get all the bookings in the cart for the current user
    cart_bookings = Booking.query.filter_by(user_id=current_user.id).all()
    total = 0

    # Create a list of dictionaries that contain the name, price, and total
    # for each item in the cart
    cart_bookings_with_attributes = []
    for booking in cart_bookings:
        car = Cars.query.filter_by(id=booking.car_id).first()
        if car:
            booking_dict = {
                'name': car.name,
                'price': car.price,
                'pickup_date': booking.pickup_date,
                'return_date': booking.return_date,
                'duration': booking.duration,  # Calculate duration in days
                'total':  booking.duration * car.price
            }
            cart_bookings_with_attributes.append(booking_dict)

    return render_template('cart.html', cart=cart_bookings_with_attributes, total=total, active_nav='cart')


@main.route('/clear-cart')
def clear_cart():
  # Get all the cars in the cart for the current user
  cart_cars = Booking.query.filter_by(user_id=current_user.id).all()
  
  # Delete all the cars in the cart
  for item in cart_cars:
    db.session.delete(item)
  db.session.commit()
  
  return redirect(url_for('main.view_cart'))




@main.route("/checkout", methods=['GET','POST'])
def checkout():
    cart_cars = Booking.query.filter_by(user_id=current_user.id).all()
    total = 0
    total = calculate_total(cart_cars, total=total)
    form = CheckoutForm()

    if form.validate_on_submit():
        # Perform checkout logic here
        flash("Your order has been placed sucessfully!")
    return render_template('checkout.html', form=form, total=total)











