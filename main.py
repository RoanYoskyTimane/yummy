from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, FileField
from wtforms.validators import DataRequired, EqualTo
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import cloudinary
import cloudinary.uploader
#from cloudinary.utils import cloudinary_url
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///recipe.db"
app.config['SECRET_KEY'] = "1214"
app.config['UPLOAD_FOLDER'] = 'static/files'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    photoOfTheRecipe = db.Column(db.String(200))
    nameOfTheRecipe = db.Column(db.String(200))
    country = db.Column(db.String(25))
    teacher = db.Column(db.String(10))
    ingredient = db.Column(db.String(200))
    steps = db.Column(db.String(1000))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(320))
    password = db.Column(db.String(200))

    @property
    def password(self):
        raise AttributeError ('password is not readable attribute!')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)   


def init_db():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

cloudinary.config( 
    cloud_name = "dyyt08ixh", 
    api_key = "324699569726994", 
    api_secret = "MClHB7NDLNWGeeFi4RzF1QRmfng", 
    secure=True
)

@app.route('/')

def index():
    return render_template("index.html")

class SigninForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), EqualTo('password_hash2', message='Password must be equal')])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Sign-in")

@app.route('/signin', methods=['GET', 'POST'])

def signin():
    form = SigninForm()

    return render_template ("signin.html", form=form)

@app.route('/add_user', methods=['POST'])

def add_user():
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    hashed_password = ""

    if (password != confirm_password):
        print("The password don't match are different")
        return render_template("signin.html")
    else:
        print("This is the email", email)
        print("This the password", password)
        print("This the confirm password", confirm_password)
        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
        print("The hashed password", hashed_password)
        return render_template("index.html")

class RecipeForm(FlaskForm):
    #imageOfTheRecipe = FileField("Upload a photo")
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
    file = request.files['imageOfTheRecipe']
    image_url = ""

    if file:
        upload_result = cloudinary.uploader.upload(file)
        image_url = upload_result.get('url')
        print("The url of the image", image_url)    
        print('File successfully uploaded')
    
    nameOfTheRecipe = request.form['nameOfTheRecipe']
    print("The name of the recipe",nameOfTheRecipe)
    
    country = request.form['country']
    print("The name of the country", country)

    teacher = request.form['teacher']
    print("The name of the teacher",teacher)

    ingredient = request.form['allIngredients']
    print("The ingredients", ingredient)

    steps = request.form['theFinalRecipe']
    print("The recipe", steps)
    
    recipe = Recipe(photoOfTheRecipe=image_url, nameOfTheRecipe=nameOfTheRecipe, country=country, teacher=teacher, ingredient=ingredient, steps=steps)
    db.session.add(recipe)
    db.session.commit()
    return render_template("success.html")