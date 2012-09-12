import sqlite3
import re
import datetime
import hashlib
from bottle import route, run, debug, template, request, validate, static_file, error, app, redirect, post, get
from beaker.middleware import SessionMiddleware

session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 300,
    'session.data_dir': './data',
    'session.auto': True
}
mybeaker = SessionMiddleware(app(), session_opts)

def connectDB():
    conn = sqlite3.connect('boring.db')
    return conn

@route('/register', method=['GET','POST'])
def register():
    if 0('register','').strip():
        email = request.POST.get('email', '').strip()
        join_date = datetime.datetime.now().isoformat()
        last_login = False
        blog_name = re.search('([^@]+)', email).group(0)
        
        # check that email is valid
        if validateEmail(email) == False:
            return template('register.tpl', error = "bad_email")
        
        # check passwords match
        password = request.POST.get('password', '').strip()
        confirm = request.POST.get('confirm', '').strip()
        if password != confirm:
            return template('register.tpl', error = "pw_mismatch")
        password = hashlib.sha512(str.encode(password)).hexdigest()
        
        # connect to db
        conn = connectDB()
        c = conn.cursor()
        
        # check if email exists
        c.execute("SELECT * FROM user WHERE email=?", [email])
        if c.fetchall():
            return template('register.tpl', error = "email_exists")
            
        # check if blog title exists. if does, append int
        c.execute("SELECT * FROM user WHERE blog_name=?", [blog_name])
        if c.fetchall():
            blog_name_exists = True
        num = 0
        while blog_name_exists == True:
            num = num + 1
            blog_name = blog_name + str(num)
            c.execute("SELECT * FROM user WHERE blog_name=?", [blog_name])
            if c.fetchall():
                blog_name_exists = True
            else:
                blog_name_exists = False
            
        # add new user to db
        c.execute("INSERT INTO user (email, join_date, last_login, blog_name, password) VALUES (?,?,?,?,?)", (email, join_date, last_login, blog_name, password))
        new_id = c.lastrowid
        
        # commit to db and close
        conn.commit()
        c.close() 
    
        return '<p>Registration successful %s</p>' % new_id
    else:
        return template('register.tpl', error = False)
    
#@post('/login')
@route('/login', method=['GET','POST'])
def login():
    s = request.environ.get('beaker.session')
    if request.forms.get('login','').strip():
        email = request.forms.get('email', '').strip()
        password = request.forms.get('password', '').strip()
        password = hashlib.sha512(str.encode(password)).hexdigest()
        
        # connect to db
        conn = connectDB()
        c = conn.cursor()
        
        # attempt login
        c.execute("SELECT * FROM user WHERE email=? AND password=?", (email, password))
        fetched = c.fetchall()
        if fetched:
            s = request.environ.get('beaker.session')
            s['email'] = email
            s['last_login'] = datetime.datetime.now().isoformat()
            s['user_id'] = fetched[0][0]
            redirect("/dashboard")
        else: 
            return template('login.tpl', error = "bad_login") 
        
        c.close()
    elif 'email' in s:
         redirect("/dashboard")
    else:
        return template('login.tpl', error = False) 

#@route('/dashboard',  method='POST')
@route('/dashboard', method=['GET','POST'])
def dashboard():
    s = request.environ.get('beaker.session')
    
    if 'email' in s and request.POST.get('post','').strip():
    
        create_date = datetime.datetime.now().isoformat()
        
        # needs more processing, remove excess linebreaks etc.
        body = request.POST.get('post','').strip() 
        
        conn = connectDB()
        c = conn.cursor()
        c.execute("SELECT * FROM post WHERE user_id=?", (s['user_id'],))
        count = len(c.fetchall()) + 1
        
        c.execute("INSERT INTO post (user_id, create_date, edit_date, body, count) VALUES (?,?,?,?,?)", (s['user_id'], create_date, False, body, count))
        conn.commit()
        c.close()
        return template('dashboard', email = s['email'], user_id = s['user_id'])
        
    elif 'email' in s:
        conn = connectDB()
        c = conn.cursor()
        c.execute("UPDATE user SET last_login=? WHERE email=?", [s['last_login'], s['email']])
        conn.commit()
        c.close()
        return template('dashboard', email = s['email'], user_id = s['user_id'])
        
    else:
        return "you are not logged in"
    
@route('/bb/:blog_name')
def blog(blog_name):

    conn = connectDB()
    c = conn.cursor()
    
    c.execute("SELECT id FROM user WHERE blog_name=?", (blog_name,))
    id = c.fetchall()[0][0]
    
    c.execute("SELECT * FROM post WHERE user_id=?", (id,))
    fetched = c.fetchall()
    
    return template('blog', rows = fetched)
    
        
@route('/logout')
def logout():
    s = request.environ.get('beaker.session')
    s.delete()
    redirect("/login")
    

## source: http://code.activestate.com/recipes/65215/
def validateEmail(email):
    if len(email) > 7:
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
            return True
    return False
    
        
debug(True)
run(app=mybeaker)




