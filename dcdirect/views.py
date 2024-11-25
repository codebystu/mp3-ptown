from flask import render_template, Blueprint, request, flash, redirect, url_for
from flask_login import login_required, current_user
from dcdirect import app, db
from dcdirect.models import Venue, Food, Event, User

views = Blueprint('views', __name__)


@views.route("/")
def home():
    return render_template("events.html", user=current_user)

@views.route("/places")
def places():
    return render_template("places.html", user=current_user)  

@views.route("/fooddrink")
def fooddrink():
    return render_template("fooddrink.html", user=current_user)

@views.route("/myplaces")
@login_required
def myplaces():
    return render_template("myplaces.html", user=current_user)

@views.route("/myevents")
@login_required
def myevents():
    return render_template("myevents.html", user=current_user)

@views.route("/myfood", methods=['GET', 'POST'])
@login_required
def myfood():
    if request.method == 'POST': 
        food_type = request.form.get('food_type')#Gets the note from the HTML 
        food = Food.query.filter_by(food_type=food_type).first()
        if food:
            flash('Food Type already exists.', category='error')
        elif len(food_type) < 1:
            flash('Food Type is too short!', category='error') 
        else:
            new_food = Food(food_type=food_type, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_food) #adding the note to the database 
            db.session.commit()
            flash('Food Type added!', category='success')

    foods = list(Food.query.order_by(Food.food_type).all())
    return render_template("myfood.html", foods=foods , user=current_user)

@views.route("/editmyfood/<int:food_id>", methods=["GET", "POST"])
def editmyfood(food_id):
    food = Food.query.get_or_404(food_id)
    if request.method == "POST":
        food.food_type = request.form.get("food_type")
        db.session.commit()
        return redirect(url_for("views.myfood"))
    return render_template("editmyfood.html", food=food, user=current_user)

@views.route("/deletemyfood/<int:food_id>")
def deletemyfood(food_id):
    food = Food.query.get_or_404(food_id)
    db.session.delete(food)
    db.session.commit()
    return redirect(url_for("views.myfood"))