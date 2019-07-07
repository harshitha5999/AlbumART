from flask import Flask,render_template,flash,redirect,url_for,session,request,logging
from flask_wtf import Form
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField,TextAreaField,PasswordField,validators,SubmitField, TextField
from passlib.hash import sha256_crypt
from functools import wraps
from flask_ckeditor import CKEditor, CKEditorField
from flask import flash

app=Flask(__name__)
#config MySQLapp
app.secret_key='i_am_very_goodgirl'
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:harshi5999@localhost/project'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db=SQLAlchemy(app)

id1=0


class Users(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(30))
    email=db.Column(db.String(100))
    username=db.Column(db.String(30))
    password=db.Column(db.String(200))
    registered_date=db.Column(db.DateTime)
    article_key=db.relationship('Articles', backref='users', lazy=True)
    def get_id(self):
        return self.id
       
class Articles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(100))
    body=db.Column(db.String(10000))
    user_key = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)

class Poems(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(300))
    body=db.Column(db.String(10000))
    user_key=db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)

class Stories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(100))
    body=db.Column(db.String(10000))
    user_key = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)


class RegisterForm(Form):
    name=TextField('name')
    email=TextField('email')
    username=TextField('username')
    password=PasswordField('password')
    confirm=PasswordField('confirm password')
    submit=SubmitField("Create new user")

class ArticleForm(Form):
    title=TextField('Title')
    body=CKEditorField('body')
    submit=SubmitField('Submit')

class StoryForm(Form):
    title=TextField('Title')
    body=CKEditorField('body')
    submit=SubmitField('Submit')

class PoemForm(Form):
    title=TextField('title')
    body=CKEditorField('body')
    submit=SubmitField('Submit')

class LoginForm(Form):
    username=TextField('username')
    password=PasswordField('password')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register',methods=['POST','GET'])
def register():
    form = RegisterForm()
    if request.method=='POST':
        form=request.form
        name=form['name']
        email=form['email']
        username=form['username']
        password=form['password']
        #create cursor
        insert_data = Users(name = name, email = email, username = username, password = password)
        save_to_database = db.session
        try:
            save_to_database.add(insert_data)
            save_to_database.commit()
            return redirect(url_for('login'))
        except:
            save_to_database.rollback()
            save_to_database.flush()
            return 'im in except'
    return render_template('register.html',form=form)

@app.route('/login/',methods=['GET','POST'])
def login():
    user=''
    if request.method=='POST':
        form=LoginForm(request.form)

        username=request.form['username']
        print(username)
        password=request.form['password']
        user = Users.query.filter_by(username=username).first()
        
        try:
            print('in login',user.username)
            print('in login ',user.password)
            print(password)
            if password==user.password:
                session['logged_in'] = True
                return redirect(url_for('dashboard',id=user.id))
            else:
                flash('please check again','danger')
        except:
            return 'usesrname not found'
        return render_template('login.html')

    return render_template('login.html')

def is_logged_in(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            flash('unauthorised,please login','danger')
            return redirect(url_for('login'))
    return wrap
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/logout/')
def logout():
    session.clear()
    flash('you are now logged out','success')
    return redirect(url_for('login'))

id1=0
@app.route('/dashboard/')
@is_logged_in
def dashboard():
    global id1
    if (id1):
        print('in dashboard',id1)
        user=Users.query.filter_by(id=id1).first()

        lst=[]
        lst=Articles.query.filter_by(user_key=id1).all()
        lst1=[]
        lst1=Stories.query.filter_by(user_key=id1).all()
        lst2=[]
        lst2=Poems.query.filter_by(user_key=id1).all()
    
        msg='in dashboard'
        return render_template('dashboard.html',msg=msg,user=user,articles=lst,stories=lst1,poems=lst2)
    else:
        id1= request.args.get('id')
        print('in dashboard',id1)
        user=Users.query.filter_by(id=id1).first()

        lst=[]
        lst=Articles.query.filter_by(user_key=id1).all()
        lst1=[]
        lst1=Stories.query.filter_by(user_key=id1).all()
        lst2=[]
        lst2=Poems.query.filter_by(user_key=id1).all()
    
        msg='in dashboard'
        return render_template('dashboard.html',msg=msg,user=user,articles=lst,stories=lst1,poems=lst2)


id1=0
@app.route('/addarticle/',methods=['POST','GET'])
@is_logged_in
def addarticle():
    form=ArticleForm()
    global id1
    print(id1)
    if request.method=='POST':
        form=request.form
        poems=[]
        stories=[]
        title1=form['title'] 
        body1=form['body']
        print('user id is')
        print(id1)
        print('before print')
        id1=int(id1)
        insert_data = Articles(title = title1, body = body1, user_key=id1)
        save_to_database = db.session
       
        lst=[]
        lst=Articles.query.filter_by(user_key=id1)
        user=Users.query.filter_by(id=id1)
        try:
            save_to_database.add(insert_data)
            save_to_database.commit()
            msg="Succesfully createdyour article"
            poems=Poems.query.filter_by(user_key=id1).all()
            articles=Articles.query.filter_by(user_key=id1).all()
            stories=Stories.query.filter_by(user_key=id1).all()
            print('im adding article')
            return render_template('dashboard.html',user=user,poems=poems,articles=articles,stories=stories)

        except Exception as ex:
            save_to_database.rollback()
            save_to_database.flush()
            return str(ex)    
    return render_template('addarticle.html',form=form,id=id)

id1=0
@app.route('/addstory/',methods=['POST','GET'])
@is_logged_in
def addstory():
    form=StoryForm()
    global id1
    print(id1)
    if request.method=='POST':
        form=request.form
        title1=form['title'] 
        body1=form['body']
        print('user id is')
        print(id1)
        print('before print')
        id1=int(id1)
        insert_data = Stories(title = title1, body = body1, user_key=id1)
        save_to_database = db.session
       
  
        stories=Stories.query.filter_by(user_key=id1)
        user=Users.query.filter_by(id=id1)
        try:
            save_to_database.add(insert_data)
            save_to_database.commit()
            msg="Succesfully createdyour article"
            articles=Articles.query.filter_by(user_key=id1).all()
            print('im printing articles')
            print(articles)
            poems=Poems.query.filter_by(user_key=id1).all()
            stories=Stories.query.filter_by(user_key=id1).all()
            print('imhere')
            return render_template('dashboard.html',user=user,stories=stories,msg=msg,poems=poems,articles=articles)

        except Exception as ex:
            save_to_database.rollback()
            save_to_database.flush()
            return str(ex)    
    return render_template('addstory.html',form=form,id=id)


@app.route('/articles')
@is_logged_in
def articles():
    article=Articles.query.filter_by().all()
    return render_template('articles.html',article=article)

@app.route('/article/<int:id>')
@is_logged_in
def article(id):
    article=Articles.query.filter_by(id=id).first()
    return render_template('article.html',article=article)

@app.route('/story/<int:id>')
@is_logged_in
def story(id):
    story=Stories.query.filter_by(id=id).first()
    return render_template('story.html',story=story)

@app.route('/poem/<int:id>')
@is_logged_in
def poem(id):
    poem=Poems.query.filter_by(id=id).first()
    return render_template('poem.html',poem=poem)

@app.route('/stories')
@is_logged_in
def stories():
    story=Stories.query.filter_by().all()
    return render_template('stories.html',story=story)

@app.route('/poems')
@is_logged_in
def poems():
    poem=Poems.query.filter_by().all()
    return render_template('poems.html',poem=poem)


id1=0
@app.route('/deletearticle/<int:id>/',methods=['POST','GET'])
@is_logged_in
def deletearticle(id):
    global id1
    print(id1)
    id1=int(id1)
    lst=[]
    article=Articles.query.filter(id==id).first()
    print('article to be deleted is ',article.title)
    db.session.delete(article)
    db.session.commit()
    lst=Articles.query.filter_by(user_key=id1).all()
    user=Users.query.filter_by(id=id1).first()
    poems=Poems.query.filter_by(id=id1).all()
    stories=Stories.query.filter_by(id=id1).all()
    print(user)
    print('list is',lst)
    print('list is',lst)
    return render_template('dashboard.html',user=user,articles=lst,poems=poems,stories=stories)

id1=0
@app.route('/editarticle/<int:id>',methods=['POST','GET'])
@is_logged_in
def edit_article(id):
    article=''
    article=Articles.query.filter_by(id=id).first()
    
    form=ArticleForm()
    global id1
    # print(id1)
    id1=int(id1)
    # print(id)
    #Popular article form fields
    form.title.data=article.title
    form.body.data=article.body
    user=Users.query.filter_by(id=id1).first()
    lst=[]
    lst=Articles.query.filter_by(user_key=id1).all()
    # print('form .title is ',form.title.data)
    if request.method=='POST':
        print('hi')
        form=request.form
        title1=form['title']
        body1=form['body']

        id1=int(id1)
        # insert_data = Articles(title = title1, body = body1, user_key=id1)
        article.title=title1
        article.body=body1
        print(article.body)

        
        try:
            # save_to_database.add(insert_data)
            save_to_database = db.session
            save_to_database.commit()
            print('before loading')
            poems=Poems.query.filter_by(user_key=id1).all()
            print('before loading stories')
            stories=Stories.query.filter_by(user_key=id1).all()
            print('before loading poems')
            articles=Articles.query.filter_by(user_key=id1).all()
            print('before loading poems')
            return render_template('dashboard.html',user=user,articles=articles,stories=stories,poems=poems)


        except Exception as ex:
            save_to_database.rollback()
            save_to_database.flush()
            return str(ex)    
    return render_template('editarticle.html',form=form,id=id)

id1=0
@app.route('/deletestory/<int:id>/',methods=['POST','GET'])
@is_logged_in
def deletestory(id):
    global id1
    print(id1)
    id1=int(id1)
    lst=[]
    story=Stories.query.filter(id==id).first()
    print('article to be deleted is ',story.title)
    db.session.delete(story)
    db.session.commit()
    lst=Stories.query.filter_by(user_key=id1).all()
    user=Users.query.filter_by(id=id1).first()
    print(user)
    print('list is',lst)
    print('list is',lst)

    articles=Articles.query.filter_by(user_key=id1).all()
    poems=Poems.query.filter_by(user_key=id1).all()
    return render_template('dashboard.html',user=user,stories=lst,articles=articles,poems=poems)
    
@app.route('/viewall',methods=['POST','GET'])
def viewall():
    artilce=Articles.quert
    return render_template('viewall.html')



id1=0
@app.route('/editstory/<int:id>',methods=['POST','GET'])
@is_logged_in
def edit_story(id):
    story=''

    story=Stories.query.filter_by(id=id).first()
    form=StoryForm()
    global id1
    # print(id1)
    id1=int(id1)
    form.title.data=story.title
    form.body.data=story.body
    user=Users.query.filter_by(id=id1).first()
    if request.method=='POST':
        print('hi')
        form=request.form
        title1=form['title']
        body1=form['body']

        id1=int(id1)
        story.title=title1
        story.body=body1
        print(story.body)

        save_to_database = db.session
        try:
            # save_to_database.add(insert_data)
            save_to_database.commit()
            stories=Stories.query.filter_by(user_key=id1).all()
            articles=Articles.query.filter_by(user_key=id1).all()
            poems=Poems.query.filter_by(user_key=id1).all()
            print('im editing stories')
            return render_template('dashboard.html',user=user,stories=stories,articles=articles,poems=poems)

        except Exception as ex:
            save_to_database.rollback()
            save_to_database.flush()
            return str(ex)    
    return render_template('editstory.html',form=form,id=id)

#ADD POEM
id1=0
@app.route('/addpoem/',methods=['POST','GET'])
def addpoem():
    form=PoemForm()
    global id1
    print(id1)
    if request.method=='POST':
        form=request.form
        title=form['title']
        body=form['body']
        print('user id is')
        print(id1)
        print('before print')
        id1=int(id1)
        insert_data = Poems(title=title, body=body, user_key=id1)
        save_to_database = db.session
       
        lst=[]
        articles=[]
        
        user=Users.query.filter_by(id=id1)
        try:
            save_to_database.add(insert_data)
            save_to_database.commit()
            msg="Succesfully createdyour article"
            lst=Poems.query.filter_by(user_key=id1).all()
            articles=Articles.query.filter_by(user_key=id1).all()
            stories=Stories.query.filter_by(user_key=id1).all()
            return render_template('dashboard.html',user=user,poems=lst,msg=msg,articles=articles,stories=stories)
        except Exception as ex:
            save_to_database.rollback()
            save_to_database.flush()
            return str(ex)    
    return render_template('addpoem.html',form=form,id=id)


#DELETE POEM
@app.route('/deletepoem/<int:id>/',methods=['POST','GET'])
def deletepoem(id):
    global id1
    print(id1)
    id1=int(id1)
    lst=[]
    print('im in delete poem')
    poem=Poems.query.filter(id==id).first()
    print('poem to be deleted is ',poem.title)
    db.session.delete(poem)
    db.session.commit()
    articles=[]
    lst=Poems.query.filter_by(user_key=id1).all()
    articles=Articles.query.filter_by(user_key=id1).all()
    user=Users.query.filter_by(id=id1).first()
    print(user)
    print('list is',lst)
    stories=Stories.query.filter_by(user_key=id1).all()
    print('list is',lst)
    return render_template('dashboard.html',user=user,poems=lst,articles=articles,stories=stories)
    

id1=0
@app.route('/editpoem/<int:id>',methods=['POST','GET'])
def edit_poem(id):
    poem=''
    print(' i entered edit poem')
    poem=Poems.query.filter_by(id=id).first()
    form=PoemForm()
    global id1
    print(id1)
    id1=int(id1)
    print(id)
    print('im here')
    #Popular article form fields
    form.title.data=poem.title
    form.body.data=poem.body
    
    user=Users.query.filter_by(id=id1).first()
    lst=[]
    lst=Poems.query.filter_by(user_key=id1).all()
    if request.method=='POST':
        print('hi')
        form=request.form
        title=form['title']
        body=form['body']
        print('no prob with form')
        id1=int(id1)
        # insert_data = Articles(title = title1, body = body1, user_key=id1)
        poem.title=title
        poem.body=body
        print(poem.body)
        print('no problem with poem')
        save_to_database = db.session
        try:
            # save_to_database.add(insert_data)
            save_to_database.commit()
            print('im in try')
            poems=Poems.query.filter_by(user_key=id1).all()
            articles=Articles.query.filter_by(user_key=id1).all()
            stories=Stories.query.filter_by(user_key=id1).all()
            return render_template('dashboard.html',user=user,poems=poems,articles=articles,stories=stories)

        except Exception as ex:
            save_to_database.rollback()
            save_to_database.flush()
            return str(ex)    
    return render_template('editpoem.html',form=form,id=id)


if __name__=="__main__":
    db.create_all()
    app.run(debug=True, port = 8000)
