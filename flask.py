from flask import Flask,render_template,request,redirect  
import smtplib
from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy import create_engine
from datetime import datetime

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///databasehere.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/fdb'
print("debug2")
db = SQLAlchemy(app)
print("debug3")
print("debug4")
class Friends(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Names %r>' % self.id


@app.route('/')
def index():
    return(render_template('index.html'))

subscribers = []

@app.route('/about')
def about():
    me = ['my name is vijayadharshni','i am a student','i am from chennai']
    return(render_template('about.html',aboutme = me))

@app.route('/subscription')
def subscription():
    return(render_template('subscription.html'))

@app.route('/form', methods=['POST'])
def form():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    message = "You have successfully subscribed to our newsletter"
    #server = smtplib.SMTP("smtp.gmail.com", 587)
    #server.starttls()
    #server.login("bokahevi14@gmail.com", "karthik234")
    #server.sendmail("thisisdharshni@gmail.com",email,message)
    if not first_name or not last_name or not email:
        error_message = "All form fields are required"
        return render_template('subscription.html', error_message=error_message,first_name=first_name, last_name=last_name, email=email)
    else:
        subscribers.append(f"{first_name}, {last_name}, {email}")
        return render_template('form.html', subscribers=subscribers)

@app.route('/friends', methods=['POST', 'GET'])
def friends():
    if request.method == "POST":
        friend_name = request.form['name']
        new_friend = Friends(name=friend_name)
        try:
            db.session.add(new_friend)
            db.session.commit()
            return redirect('/friends')
        except:
            return "There was an error adding your friend"
    else:
        friends = Friends.query.order_by(Friends.date_created)
        return render_template('friends.html', friends=friends)  
@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    friend_to_update = Friends.query.get_or_404(id)
    if request.method == "POST":
        friend_to_update.name = request.form['name']
        try:
            db.session.commit()
            return redirect('/friends')
        except:
            return "There was an error updating your friend"
    else:
        return render_template('update.html',friend_to_update=friend_to_update)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    print("debug5")
    print("debug6")
    app.run(debug=True, port=8000)
    print("debug7")
