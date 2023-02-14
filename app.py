from flask import Flask, redirect, request, render_template, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_db, db, User, Post, PostTag, Tag, default_img

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'murder'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


connect_db(app)


#User routes

@app.route('/', methods=['GET'])
def show_users():
    """Show home page which is users listing"""
    users = User.query.all()

    return render_template('base.html', users=users)


@app.route('/users/new')
def show_user_form():
    """Show user form"""
    return render_template('new_user_form.html')


@app.route('/users/new', methods=['POST'])
def add_new_user():
    """adding new user data to db and adding it to the html"""

    #getting data from forms
    first = request.form['first']
    last = request.form['last']
    img = request.form['url']
    # if url for img is not provided, use the default
    if not img:
        img = default_img

    #adding the data in db
    new_user = User(first_name=first, last_name=last, image_url=img)

    db.session.add(new_user)
    db.session.commit()

    return redirect('/')


@app.route('/users/<int:user_id>/')
def show_user_details(user_id):
    """Show user details"""
    user = User.query.get_or_404(user_id)

    return render_template('user_detail.html', user=user)



@app.route('/users/<int:user_id>/edit')
def show_edit_page(user_id):
    user = User.query.get_or_404(user_id)

    return render_template('edit_user.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def update_user(user_id):
    """Update user information"""
    user = User.query.get_or_404(user_id)

    user.first_name = request.form['first']
    user.last_name = request.form['last']
    user.url = request.form['url']
    if not user.url:
        user.url = default_img

    db.session.commit()
    return redirect(f'/users/{user.id}')


@app.route('/users/<int:user_id>/delete')
def delete_user(user_id):
    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect('/')


############################################
#Post routes

@app.route('/posts/<int:user_id>/posts/new', methods=['GET'])
def show_post_form(user_id):
    """Show form to add a new post"""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    

    return render_template('new_post.html', user=user, tags=tags)



@app.route('/posts/<int:user_id>/posts/new', methods=['POST'])
def show_post(user_id):
    """Show post page"""
    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    new_post = Post(title=request.form['title'], 
                    content=request.form['comment'], 
                    user_id=user.id)
    
    db.session.add(new_post)
    db.session.commit()
    # flash(f"Post '{new_post.title}' added!")

    return redirect(f"/users/{user.id}")



@app.route('/posts/<int:post_id>')
def show_post_detail(post_id):
    """Show post details"""

    post = Post.query.get_or_404(post_id)

    return render_template('post_detail.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def show_edit_post(post_id):
    """Show page for editing the post"""
    
    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(post.user_id)
    tags = Tag.query.all()

    return render_template('edit_post.html', post=post, user=user, tags=tags)


@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def update_post(post_id):
    """Update post"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['comment']

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()

    return redirect(f'/posts/{post.id}')


@app.route('/posts/<int:post_id>/delete')
def delete_post(post_id):
    """Delete post"""

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()
    return redirect(f'/users/{post.user_id}')



###################################################
#Tags route

@app.route('/tags')
def show_tags():
    """Show tags page"""
    tags = Tag.query.all()
    
    return render_template('tags.html', tags=tags)



@app.route('/tags/<int:tag_id>')
def show_tag_details(tag_id):
    """Show tag details"""
    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
   
    return render_template('tag_details.html', tag=tag, posts=posts)



@app.route('/tags/new')
def add_tag():
    """show form for adding a new tag"""
    return render_template('create_tag.html')



@app.route('/tags/new', methods=['POST'])
def get_tag_details():
    """Get tag details from form and add them to db"""

    new_tag = Tag(name=request.form['tagname']) 

    db.session.add(new_tag)
    db.session.commit()

    return redirect('/tags')



@app.route('/tags/<int:tag_id>/edit')
def edit_tag(tag_id):
    """Show form to edit tag"""

    tag = Tag.query.get_or_404(tag_id)

    return render_template('edit_tag.html', tag=tag)



@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def update_tag(tag_id):
    """Update tag"""

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['tagname']
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()
    

    return redirect("/tags")


@app.route('/tags/<int:tag_id>/delete')
def delete_tag(tag_id):
    """Delete tag"""

    tag = Tag.query.get_or_404(tag_id)

    db.session.delete(tag)
    db.session.commit()
    flash(f"Tag {tag.name} deleted.")

    return redirect('/tags')

    
    