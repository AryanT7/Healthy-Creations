from flask import Flask ,render_template,redirect,request,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,login_user,UserMixin

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = 'thisissecret'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(25), unique=True,nullable=False)
    password = db.Column(db.String(25), nullable=False)
    gender = db.Column(db.String(25), nullable=False)
    disease = db.Column(db.String(25), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about_us")
def about():
    return render_template("about.html")

@app.route("/contact_us")
def contact_us():
    return render_template("contact_us.html")

@app.route("/Sign_up", methods=['GET','POST'])   
def signup():
    if request.method=='POST':
        username = request.form['uname']   
        email = request.form['email']
        password = request.form['password']
        gender = request.form['gender']
        disease = request.form['disease']
        age = request.form['age']
        weight = request.form['weight']
        height = request.form['height']
        user = User(username=username,email=email,password=password,gender=gender,disease=disease,age=age,weight=weight,height=height)
        db.session.add(user)
        db.session.commit()
        flash('Successfully registered','success')
        return redirect('/Sign_in')
    return render_template("Sign_up.html")

@app.route("/Sign_in", methods=['GET','POST'])   
def signin():
    if request.method=='POST':
        username = request.form['uname']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and password==user.password:
            login_user(user)
            flash('Successfully logged in','success')
            return redirect(f'/main/{user.id}')
        else:
            flash('Invalid username or password','warning')
            return redirect('/Sign_in')
    return render_template("Sign_in.html")

@app.route("/main/<int:id>", methods=['GET','POST'])   
def main1(id):
    obj = User.query.filter_by(id=id).first()
    # return redirect('/result')
    return render_template("main.html",obj=obj)

@app.route("/result/<int:id>", methods=['GET','POST'])   
def result(id):
    obj = User.query.filter_by(id=id).first()
    ht = obj.height
    wt = obj.weight
    age = obj.age
    gender = obj.gender
    if(gender == "Male"):
        cal = (10*wt + 6.25*ht - 5*age + 5)*1.375
    else:
        cal = (10*wt + 6.25*ht - 5*age - 161)*1.375
    carb = 0.45*cal
    fats = 0.30*cal
    protein = 0.25*cal
    bmi = round(((wt/(ht*ht))*10000),3)
    return render_template("result.html",cal=cal,carb=carb,fats=fats,protein=protein,bmi=bmi)

@app.route("/videos")
def video():
    return render_template("video.html")

if __name__ == "__main__":
    app.run(debug = True)