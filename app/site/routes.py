from flask import Blueprint, render_template

site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/')
def home():
    return render_template('index.html')

@site.route('/profile')
def profile():
    return render_template('profile.html')

@site.route("/ourcars")
def ourcars():
    return render_template("cars.html")

@site.route("/contactus")
def contactus():
    return render_template("contactus.html")