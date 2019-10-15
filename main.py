from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:1234@localhost:8889/build-a-blog'
db = SQLAlchemy(app)
app.secret_key = 'y37kGcys&zP3B'


class Blog(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    blog = db.Column(db.String(120))
    published = db.Column(db.Boolean)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, name, owner):
        self.blog=blog
        self.published=False
        self.owner = owner






@app.route('/', methods=['POST', 'GET'])
def index():

    owner = User.query.filter_by(email=session['email']).first()

    if request.method == 'POST':
        blog_name = request.form['blog']        
        new_blog = Blog(blog_name, owner)
        db.session.add(new_blog)
        db.session.commit()

    blogs = Task.query.filter_by(published=False,owner=owner).all()
    published_blogs = Task.query.filter_by(published=True,owner=owner).all()
    return render_template('blogs.html',title="Build-A-Blog!", 
        blogs=blogs, published_blogs=published_blogs)








if __name__ == '__main__':
    app.run()