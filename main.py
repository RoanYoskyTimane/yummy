from flask import Flask, render_template, flash, request, jsonify
import traceback
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, FileField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///recipe.db"
app.config['SECRET_KEY'] = "1214"
db = SQLAlchemy(app)


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    photoOfTheRecipe = db.Column(db.LargeBinary)
    nameOfTheRecipe = db.Column(db.String(200))
    country = db.Column(db.String(25))
    teacher = db.Column(db.String(10))
    steps = db.Column()
    

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Creates the database and tables
    app.run(debug=True)


@app.route('/')

def index():
    return render_template("index.html")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


@app.route('/login', methods=['GET', 'POST'])

def login():
    form = LoginForm()

    if form.validate_on_submit():
        # Handle form submission
        pass

    return render_template ("login.html", form=form)

class RecipeForm(FlaskForm):
    imageOfTheRecipe = FileField("Upload a photo")
    nameOfTheRecipe = StringField("Recipe name:", validators=[DataRequired()])
    country = SelectField("Country", choices=[
        ('Mozambique'),
        ('South Africa'),
        ('Italy')]) 

    teacher = SelectField("Who thought you:", choices=[
        ("Mother"),
        ("Grandmother"),
        ("Another person")
    ])   

    measurement = SelectField("Measurement:", choices=[
        ("Teaspoon(tsp)"),
        ("Tablespoon(tbsp)"),
        ("Cup(C)"),
        ("Pint(pt)"),
        ("Quart(qt)"),
        ("Gallon(gal)"),
        ("Ounce(oz)"),
        ("Fluid Ounce(fl oz)"),
        ("Pound(lb)")
    ])

    step = StringField("Steps")
    
@app.route('/add_recipe')

def recipe():
    form = RecipeForm()

    return render_template("recipe-menu.html", form=form)

@app.route('/submit', methods=['POST'])

def submit_recipe():
    if not request.is_json:
            return jsonify({
                'status': 'error',
                'message': 'Content-Type must be application/json'
            }), 400
        
    data = request.get_json()

    nameOfTheRecipe = data.get('nameOfTheRecipe')
    print("The name of the recipe",nameOfTheRecipe)
    country = data.get('country')
    print("The name of the country",country)
    teacher = data.get('teacher')
    print("The name of the teacher",teacher)
    ingredient = data.get('ingredient')
    print("The ingredients", ingredient)
    recipe = data.get('recipe')
    print("The recipe", recipe)

    response_message = f"The name of the recipe: {nameOfTheRecipe}, country:{country}, teacher: {teacher}, ingredient: {ingredient}, recipe: {recipe}"     
    return jsonify({"message": response_message}), 200
    
    

    
        