import json
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from MO import check
#  форма для обратной сзвязи
from forms import ContactForm

app = Flask(__name__)
app.config['SECRET_KEY'] = "12345"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class urls(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.Text, unique = True)
    date = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id

@app.route('/', methods=['GET', 'POST'])
def index():
    form = ContactForm()

    return render_template("index.html",
                           title="index page",
                           form=form)

@app.route('/newdata', methods  = ['GET'])
def new_data():
        data = urls.query.order_by(urls.date).all()
        return render_template("data.html", data=data)


@app.route('/update', methods = ['GET'])
def update():
    if request.method == 'GET':
        table = "<table border='1'>"
        for i in urls.query.order_by(urls.date).all():
            table+="<tr><td>{}</td><td>{}</td><td>{}</td></tr>".format(i.id, i.title, i.date)
        table+="</table>"
        return json.dumps({'success': 'true', 'msg': table})
    else:
        return json.dumps({'success': 'false', 'msg': 'Ошибка на сервере!'})

@app.route('/send', methods=['POST'])
def send():
    form = ContactForm()
    if request.method == "POST":
        if form.validate_on_submit():
            url = request.form.get('name')
            data = urls(title=url)
            db.session.add(data)
            db.session.commit()
            answer = "{} is {}".format(url, check(url) )
            return json.dumps({'success': 'true', 'msg': answer})
        else:
            return json.dumps({'success': 'false', 'msg': 'Ошибка на сервере!'})





if __name__ == '__main__':
    app.run(debug=True)