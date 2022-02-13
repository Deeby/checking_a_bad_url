from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from MO import check
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class urls(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.Text, unique = True)
    date = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id

@app.route('/', methods= ['POST', 'GET'])
def main():
    if request.method == "POST":
        new_data = request.form["text"]
        data = urls(title=new_data)
        try:
            db.session.add(data)
            db.session.commit()
            note = check(new_data)
            flag = True
            return render_template("index.html", url = new_data, note = note, flag = flag)
        except:
            return "Ошибка"
    else:
        return render_template("index.html")

@app.route('/newdata')
def new_data():
    data = urls.query.order_by(urls.date).all()
    return render_template("data.html",data = data)
if __name__ == "__main__":
    app.run(debug=True)