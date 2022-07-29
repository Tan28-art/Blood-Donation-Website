from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user,
    LoginManager,
)
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from matplot import save_graph, remove_file

app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SECRET_KEY"] = "secret_key"

# manages login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# class for users
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(
        db.String(20), nullable=False, unique=True
    )  # Ensures that every username is unique and cannot be null
    password = db.Column(db.String(80), nullable=False)


# creates the login form
class LoginForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[InputRequired(), Length(min=4, max=20)],
        render_kw={"placeholder": "Username"},
    )
    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=4, max=20)],
        render_kw={"placeholder": "Password"},
    )
    submit = SubmitField("Login")


# creates the register form
class RegisterForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[InputRequired(), Length(min=4, max=50)],
        render_kw={"placeholder": "Username"},
    )
    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=4)],
        render_kw={"placeholder": "Password"},
    )
    submit = SubmitField("Register")

    def validate_username(self, username):
        username = User.query.filter_by(username=username.data).first()
        if username:
            raise ValidationError("Username already exists. Please choose a different username.")


# Routes to default page
@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")


# Routes to login page
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=True)
                return redirect(url_for("info"))
        return redirect(url_for("login"))
    return render_template("login.html", form=form)


# Logs user out
@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    remove_file()
    logout_user()
    return redirect(url_for("login"))


# Routes to sign up page
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(
            form.password.data
        )  # For encrypting password
        new_user = User(username=form.username.data, password=hashed_pass)
        db.session.add(new_user)  # adds new user to db
        db.session.commit()
        return redirect(url_for("login"))  # redirects to login page after registering

    return render_template("register.html", form=form)


@app.route("/info", methods=["GET", "POST"])
@login_required
def info():
    return render_template("info.html")

@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    if request.method == "POST":
        blood_type = request.form.get("blood-info", None)
        if blood_type == "O+":
            stats_1 = "38.67%"
            stats_2 = "O+ A+ B+ and AB+"
            stats_3 = "O+ and O-"
            stats_4 = "O"
            info = """O+ blood is the most common blood type in the world and while it is not quite as universal as O- blood (O+ can be given to all Rh positive types but not the Rh negative types), it is still the most used blood, according to the American Red Cross. Additionally, Rh positive blood types are much more common than Rh negative blood types, which is another reason why O+ blood is always needed and important.

While O+ blood can be given to anyone with Rh positive blood types, individuals can only receive blood from O+ and O- donors. When it comes to plasma, O blood, both positive and negative, is not so universal and they can only give plasma to other O types. However, O blood types can be given plasma from anyone."""
            did_you_know = """Although both O+ and O- blood are used most often when an individual’s blood type is unknown, during traumas hospitals prefer to transfuse O+ blood over O- because the risk of reaction is much lower in ongoing blood loss situations and because hospitals have more O+ blood than O-. """

        elif blood_type == "A+":
            stats_1 = "27.42%"
            stats_2 = "A+ and AB+"
            stats_3 = "A+ A- O+ and O-"
            stats_4 = "O and A"
            info = r"""A+ blood is the second most common blood type just behind O+. About 27.42% of the world’s population has A+ blood, so donations from people with this blood type are always welcome so that the less common blood types can be saved for the those with rarer blood types and emergencies. While it is common, A+ blood can only be given to others with A+ or AB+ blood. Those with A+ blood can receive blood from Rh negative and positive A and O types.  """
            did_you_know = r"""According to the American Red Cross, the platelets from A+ blood are in high demand for patients undergoing chemotherapy treatments. """

        elif blood_type == "B+":
            stats_1 = "22.02%"
            stats_2 = "B+ and AB+"
            stats_3 = "B+ B- O+ and O-"
            stats_4 = "O and B"
            info = r"""While B- blood is very rare, B+ blood is fairly common as over 22% of the world’s population has this blood type. B+ blood is more restrictive than B- blood and can only be given to others with B+ or AB+ blood. Patients with B+ blood can only receive blood from B and O, both negative and positive types. """
            did_you_know = r"""Although B+ is not necessarily in high demand, it is important because it is often used to treat individuals with sickle cell sickle cell disease and thalassemia who need regular transfusions. """

        elif blood_type == "AB+":
            stats_1 = "5.88%"
            stats_2 = "AB+"
            stats_3 = "All blood types"
            stats_4 = "All blood types"
            info = r"""On the opposite end of the O- blood’s universal donor status is AB+, which is the universal recipient. Since AB+ blood can only be donated to others with AB+ blood, but can receive from any blood type, AB+ blood donations are not in high demand. This is a relatively good thing since AB+ blood is fairly rare with less 6% of the world’s population having this type. """
            did_you_know = r"""While demand for AB+ blood is low, AB plasma, both Rh negative and positive, is always wanted because AB blood is the universal plasma donor. According to the UK’s National Health Service (NHS), fresh frozen plasma can only be produced from male donors because plasma from female donors can develop harmful antibodies. """

        elif blood_type == "O-":
            stats_1 = "2.55%"
            stats_2 = "All blood types"
            stats_3 = "O-"
            stats_4 = "O"
            info = r"""As the “universal donor,” O- blood is perhaps the most valuable blood in the world as it can be given to nearly any blood type (except when the person has some rare antigen outside of the main ones). O- blood is used often in transfusions when the recipient’s blood type is unknown, like during trauma or emergency situations.

Unfortunately, O- blood is pretty uncommon and because of how important the blood is, donors are in very high demand around the world. According to the American Red Cross, O- blood is the always the first to run out during a blood shortage due to its universality. """
            did_you_know = r"""Although O- blood is already very special, O- donors who are CMV (Cytomegalovirus) negative are extra special because their blood is safe to give to babies. CMV is a flu-like virus that most adults have been exposed to at some time in their life and while CMV antibodies, which remain in the blood forever like all viruses, are safe for adults, they can be fatal to babies. """

        elif blood_type == "A-":
            stats_1 = "1.99%"
            stats_2 = "A- A+ AB- and AB+"
            stats_3 = "A- and O-"
            stats_4 = "O and A"
            info = r"""Of the A blood types, A- is much rarer than A+, which is actually pretty common. Less than 2% of the world’s population has A- blood. Similar to B- blood, A- blood can be donated to anyone with A or AB regardless of the positive or negative. On the other hand, those with A- blood can only get blood from A- and the universal donor O-. """
            did_you_know = r"""While people with A- blood can’t donate blood and plasma to just anyone, A- blood is valuable because it is the universal platelet donor and A- platelets can be given to anyone of any blood type. """

        elif blood_type == "B-":
            stats_1 = "1.11%"
            stats_2 = "B- B+ AB- and AB+"
            stats_3 = "B- and O-"
            stats_4 = "O and B"
            info = r"""B- is very rare among the world’s population, comprising only about 1.11% of the total population’s known blood types. Since B- blood lacks the A antibody in the red cells, it can only receive blood from B- and O- (the universal donor). Unlike B+ blood, B- blood can be given to both types of B and AB blood. """ 
            did_you_know = r"""According to various sources, only about 1 in 50 or so blood donors is B-, so B- donors are always in high demand to ensure that the supply is stable. """

        elif blood_type == "AB-":
            stats_1 = "0.36%"
            stats_2 = "AB- and AB+"
            stats_3 = "AB- A- B- and O-"
            stats_4 = "All blood types"
            info = r"""Of the eight basic blood types, AB- is the rarest with less than 1% (about 0.36%) of the world’s population sharing this type. While AB- can receive blood from all other Rh negative types, it can only donate to others with AB blood, both Rh negative and positive. AB- has both A and B antigens on its red cells which is why its compatible with all the other main Rh negative blood types. """
            did_you_know = r"""Since AB blood, both Rh positive and negative, contains no A or B antibodies it is the universal plasma donor and anyone from any blood group can receive plasma from AB blood. """

        save_graph() #saves graph to Assets folder to display on the dashboard

        return render_template(
            "dashboard.html",
            blood_type=blood_type,
            stats_1=stats_1,
            stats_2=stats_2,
            stats_3=stats_3,
            stats_4=stats_4,
            info=info,
            did_you_know=did_you_know
        )
        
    else:   
        return render_template("dashboard.html")

if __name__ == "__main__":
    app.run(debug=True)
