from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:1234@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y37kGcys&zP3B'


def title_error(blog_title):             #if blog title is blank return True
    if len(blog_title) > 0:              #to render error msg to user
        return False
    else:
        return True

def body_error(blog_body):               #if blog body is blank return True
    if len(blog_body) > 0:               #to render error msg to user
        return False
    else:
        return True

def password_error(password):
    space = False
    for char in password:
        if char.isspace() == True:
            space = True
    
    if 2<len(password)<20 and space == False:
        return False
    else:
        return True

def verify_error(verify, password):
    if verify == password:
        return False
    else:
        return True

def email_error(email):
    existing_user = User.query.filter_by(email=email).first()
    if "@" in email and "." in email and " " not in email and not existing_user and 2<len(email)<20 and email.count('@') == 1:
        return False
    else:
        return True

class Blog(db.Model):                   #create Blog object

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))                    #blog title
    body = db.Column(db.String(800))                    #blog body
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __init__(self, blog, blogbody, owner):
        self.name=blog
        self.body=blogbody
        self.owner=owner

class User(db.Model):                   #create User object

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, email, password):
        self.email=email
        self.password=password


@app.route('/index', methods=['POST', 'GET'])           #this is the main page display
def index():
    users = User.query.all()

    rows = Blog.query.count()
 
    return render_template('index.html', users=users)  #remove rows=rows

@app.route("/")                                         #setup to route '/' to the index page
def main():
    return render_template('index.html')

@app.before_request                                   #if not logged in, allow access to login, register,
def require_login():                                  #index and blogs pages
    
    # user_id = str(request.args.get('user'))
    # blog_id = str(request.args.get('id'))                                  

    allowed_routes = ['login', 'register', 'index', 'blogs']
    #, 'blogs?id=' + blog.id, 'blogs?user=' + user.id              add to allowed routes?

    if request.endpoint not in allowed_routes and 'email' not in session:  #redirect to index if user not logged in or 
        return redirect('/index')                                          #on an allowed routes page

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        login_error = ''
        if user and user.password == password:
            session['email']  =email
            return redirect('/index')
        else:
            login_error = "User password incorrect or user does not exist"
            return render_template('login.html', login_error=login_error)

    return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():

    if request.method == 'POST':
        password = request.form['password']
        verify = request.form['verify']
        email = request.form['email']

        pw_error = ''
        v_error = ''
        e_error = ''

        # 'escape' the user's input so that if they typed HTML, it doesn'
        password_escaped = cgi.escape(password, quote=True)
        verify_escaped = cgi.escape(verify, quote=True)
        email_escaped = cgi.escape(email, quote=True)

        if password_error(password):
            pw_error = "Please specify a password that is between 3 and 20 characters and contains no spaces."
            password = ''

        if verify_error(verify, password):
            v_error = "Passwords do not match."

        if email_error(email):
            e_error = "Please specify a valid email that is not already in use."
            email = ''

        existing_user = User.query.filter_by(email=email).first()

        if not existing_user and not password_error(password) and not verify_error(verify, password) and not email_error(email):  
            new_user = User(email, password)
            db.session.add(new_user)
            db.session.commit()
            session['email'] = email
            return redirect('/index')
        else:
            return render_template('register.html', password_error=pw_error, verify_password_error=v_error, email=email, email_error=e_error)

    else:
        return render_template('register.html')


@app.route('/logout')                        #redirect user to index page if logged out
def logout():
    del session['email']
    return redirect('/index')

@app.route('/blogs', methods=['POST', 'GET'])         #display blog posts filtered by user_id
def blogs_display():
    
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