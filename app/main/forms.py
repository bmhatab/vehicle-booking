from .. import main
from flask import Flask, render_template,flash,request,redirect,url_for
from flask_wtf import FlaskForm
from wtforms import Form,StringField,SubmitField,PasswordField,SelectField,IntegerField,TextAreaField,DateTimeField
from wtforms.validators import DataRequired,EqualTo,Length
from wtforms.widgets import TextArea




class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

class UserForm(FlaskForm):
    name = StringField("Name : ", validators=[DataRequired()])
    email = StringField("Email : ", validators=[DataRequired()])
    phone = IntegerField("Phone : ", validators=[DataRequired()])
    submit = SubmitField("Submit")
    password_hash = PasswordField("Password : ", validators=[DataRequired(),EqualTo('password_hash_v',message="Passwords must match!")])
    password_hash_v = PasswordField("Confirm Password : ", validators=[DataRequired()])

    
class CarsForm(FlaskForm):
    name = StringField("Item Name", validators=[DataRequired()])
    description = StringField("Size", validators=[DataRequired()], widget=TextArea())
    price = StringField("Price", validators=[DataRequired()])
    category = StringField("Item Name", validators=[DataRequired()])
    submit = SubmitField()




class BookForm(FlaskForm):
    name = StringField("Car Name", validators=[DataRequired()])
    pickup_date = DateTimeField('Pick-up Date',
                                format='%Y-%m-%d %H',
                                validators=[DataRequired()],
                                description='Select a date and time',
                                render_kw={'placeholder': 'YYYY-MM-DD HH'})
    
    return_date = DateTimeField('Return Date',
                                format='%Y-%m-%d %H',
                                validators=[DataRequired()],
                                description='Select a date and time',
                                render_kw={'placeholder': 'YYYY-MM-DD HH'})
    submit = SubmitField()


class VehiclesForm(FlaskForm):
    name = StringField("Product Name", validators=[DataRequired()])
    category = StringField("Category", validators=[DataRequired()], widget=TextArea())
    description = StringField("Description", validators=[DataRequired()])
    submit = SubmitField()

class AddToBookingForm(FlaskForm):
    name = SelectField('Item Name', choices=[], default='')
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Add to Cart')


class CheckoutForm(FlaskForm):
    name = StringField('Receipient Name', validators=[DataRequired(), Length(min=2, max=50)])
    phone = IntegerField('Phone Number', validators=[DataRequired()])
    address = StringField('Hostel Name', validators=[DataRequired(), Length(min=2, max=200)])
    room_number = IntegerField('Room Number', validators=[DataRequired()])
    student_id = IntegerField('Student ID (Discount Purchase)', validators=[DataRequired()])
    submit = SubmitField('Submit')

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send')