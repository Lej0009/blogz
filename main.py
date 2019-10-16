from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:1234@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y37kGcys&zP3B'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    body = db.Column(db.String(800))



    def __init__(self, blog, blogbody):
        self.name=blog
        self.body=blogbody

@app.route('/', methods=['POST', 'GET'])
def index():

 
    blogs = Blog.query.all()
    
    return render_template('blogs.html',title="Build-A-Blog!", 
        blogs=blogs)



@app.route('/newblog', methods=['POST', 'GET'])
def new_blog():

    if request.method == 'POST':
        blog_title = request.form['blog']   
        blog_body = request.form['blogbody']     
        new_blog = Blog(blog_title, blog_body)
        db.session.add(new_blog)
        db.session.commit()

        return redirect('/')
    else:
        return render_template('newblog.html')

if __name__ == '__main__':
    app.run()