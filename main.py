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
    completed = db.Column(db.Boolean)


    def __init__(self, blog, blogbody):
        self.name=blog
        self.blogbody=blogbody
        self.completed=False


@app.route('/', methods=['POST', 'GET'])
def index():

 
    blogs = Blog.query.filter_by(completed=False).all()
    completed_blogs = Blog.query.filter_by(completed=True).all()
    return render_template('blogs.html',title="Build-A-Blog!", 
        completed_blogs=completed_blogs)


# @app.route('/delete-blog', methods=['POST'])
# def delete_blog():

#     blog_id = int(request.form['blog-id'])
#     blog = Blog.query.get(blog_id)
#     blog.completed = True
#     db.session.add(blog)
#     db.session.commit()

#     return redirect('/')

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