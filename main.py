from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:1234@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y37kGcys&zP3B'


def title_error(blog_title):
    if len(blog_title) > 0:
        return False
    else:
        return True

def body_error(blog_body):
    if len(blog_body) > 0:
        return False
    else:
        return True


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    body = db.Column(db.String(800))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __init__(self, blog, blogbody, owner):
        self.name=blog
        self.body=blogbody
        self.owner=owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, email, password):
        self.email=email
        self.password=password

@app.route('/index', methods=['POST', 'GET'])
def home():

    users = User.query.all()

    return render_template('index.html', users=users)


@app.before_request
def require_login():
    allowed_routes = ['login', 'register', 'index', 'blogs']
    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect('/index') 

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            session['email']  =email
            flash("Logged in")
            return redirect('/index')
        else:
            flash("User password incorrect or user does not exist", 'error')

    return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']

        # TODO - validate user's data

        existing_user = User.query.filter_by(email=email).first()
        if not existing_user:
            new_user = User(email, password)
            db.session.add(new_user)
            db.session.commit()
            session['email'] = email
            return redirect('/index')
        else:
            # TODO - user better response messaging
            return '<h1>Duplicate user</h1>'

    return render_template('register.html')

@app.route('/logout')
def logout():
    del session['email']
    return redirect('/login')

@app.route('/blogs', methods=['POST', 'GET'])
def index():
    
    user_id = str(request.args.get('user'))
    owner = Blog.query.filter_by(id=user_id).first()

    blog_id = str(request.args.get('id'))
    blogs = Blog.query.filter_by(owner=owner).all()
    myblog = Blog.query.get(blog_id)

    return render_template('blogs.html', blogs=blogs, myblog=myblog)
  

@app.route('/newblog', methods=['POST', 'GET'])
def new_blog():
        
    if request.method == 'POST' :
        blog_title = request.form['blog']   
        blog_body = request.form['blogbody']
        title_error_msg = ''
        body_error_msg = ''
        

        if title_error(blog_title):
            title_error_msg = "Please input a title."
            return render_template('newblog.html', title_error=title_error_msg, body_error=body_error_msg, blog_body=blog_body)
        if body_error(blog_body):
            body_error_msg = "Please input blog content."
            return render_template('newblog.html', title_error=title_error_msg, body_error=body_error_msg, blog_title=blog_title)
                   
        else:
            owner = User.query.filter_by(email=session['email']).first()
            new_blog = Blog(blog_title, blog_body, owner)
            db.session.add(new_blog)
            db.session.commit()  
            return redirect('blogs?id=' + str(new_blog.id)) 
    else:
            return render_template('newblog.html')  
    


if __name__ == '__main__':
    app.run()