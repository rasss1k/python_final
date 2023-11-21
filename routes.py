from flask import Flask, render_template, url_for, redirect, request
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from werkzeug.utils import secure_filename
from models import db, bcrypt, User, Item

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'
db.init_app(app)
app.app_context().push()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class SearchForm(FlaskForm):
    search = StringField("Searched")
    submit = SubmitField("Submit")

class RegisterForm(FlaskForm):
    username = StringField(validators= [InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators= [InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError("That username already exists. Please choose a different one.")


class LoginForm(FlaskForm):
    username = StringField(validators= [InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators= [InputRequired() , Length(
        min=4, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField("Login")


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/index')
@login_required
def index():
    item = Item.query.order_by(Item.id).all()
    return render_template('index.html', item=item)

@app.route("/index/<int:id>")
def post_editor(id):
    item = Item.query.get(id) 
    return render_template("post_editor.html", item = item)

@app.route("/index/buy/<int:id>")
def buy(id):
    item = Item.query.get(id) 
    return render_template("buy.html", item = item)

@app.route("/index/buy/<int:id>/visa")
def visa(id):
    item = Item.query.get(id) 
    return render_template("visa.html", item = item)

@app.route("/index/buy/<int:id>/kaspi")
def kaspi(id):
    item = Item.query.get(id) 
    return render_template("kaspi.html", item = item)

@app.route('/index/<int:id>/del')
@login_required
def post_delete(id):
    item = Item.query.get_or_404(id)
    if item.author != current_user:
        return redirect ("/abort")
    try:
        db.session.delete(item)
        db.session.commit()
        return redirect("/index")
    except:
        return "Error while deleting"
    

@app.route('/index/<int:id>/update', methods=['POST', 'GET'])
@login_required
def update(id):
    item = Item.query.get(id)
    if item.author != current_user:
        return redirect ("/abort")

    if request.method == 'POST':
        item.title = request.form['title']          
        item.text = request.form['text']       
        item.price = request.form['price']

        try:
            db.session.commit()
            return redirect('/index')
        except:
            return "Error while updating"
    else:
        return render_template("update.html", item=item)

@app.route('/abort')
def abort():
    return render_template('abort.html')

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

@app.route('/goal')
def goal():
    return render_template('goal.html')

@app.route("/create", methods=['POST', 'GET'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']        
        text = request.form['text']
        price = request.form['price']
        img = request.files['img']
        if img:
            img.save(f"static/uploads/{secure_filename(img.filename)}")
        item = Item(title=title, price=price, text = text, author=current_user, img=secure_filename(img.filename))
        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/index')
        except:
            return "Error"
    return render_template("create.html")

if __name__ == '__main__':
    app.run(debug=True)
