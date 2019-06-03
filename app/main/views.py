
from flask import render_template, request, redirect, url_for, abort
from . import main
from ..models import User,Post,Comments,Category,Votes,PhotoProfile
from .. import db
from . forms import PostForm, CommentForm, CategoryForm, UpdateProfile
from flask_login import login_required,current_user
from .. import db,photos
from ..requests import get_quotes

#display categories on the landing page
@main.route('/')
def index():
    """ View root page function that returns index page """

    category = Category.get_categories()

    title = 'Home- Welcome'
    random_quotes = get_quotes()
    print('=====================')
    print([c.author for c in random_quotes])

    return render_template('index.html', title = title, categories=category,quotes=random_quotes)



#Route for adding a new pitch
@main.route('/category/new-post/<int:id>', methods=['GET', 'POST'])
@login_required
def new_post(id):
    ''' Function to check Pitches form and fetch data from the fields '''
    form = PostForm()
    category = Category.query.filter_by(id=id).first()

    if category is None:
        abort(404)

    if form.validate_on_submit():
        content = form.content.data
        new_post= Post(content=content,category_id= category.id,user_id=current_user.id)
        new_post.save_post()
        return redirect(url_for('.category', id=category.id))

    return render_template('new_pitch.html', post_form=form, category=category)

@main.route('/categories/<int:id>')
def category(id):
    category = Category.query.get(id)
    if category is None:
        abort(404)

    posts=Post.get_posts(id)
    return render_template('category.html', posts=posts, category=category)

@main.route('/add/category', methods=['GET','POST'])
@login_required
def new_category():
    '''
    View new group route function that returns a page with a form to create a category
    '''
    form = CategoryForm()

    if form.validate_on_submit():
        name = form.name.data
        new_category = Category(name=name)
        new_category.save_category()

        return redirect(url_for('.index'))

    title = 'New category'
    return render_template('new_category.html', category_form = form,title=title)


#view single pitch alongside its comments
@main.route('/view-post/<int:id>', methods=['GET', 'POST'])
@login_required
def view_post(id):
    '''
    Function the returns a single pitch for comment to be added
    '''
    print(id)
    posts = Post.query.get(id)
    # pitches = Pitch.query.filter_by(id=id).all()

    if posts is None:
        abort(404)
    #
    comment = Comments.get_comments(id)
    return render_template('view-pitch.html', posts=posts, comment=comment, category_id=id)


#adding a comment
@main.route('/write_comment/<int:id>', methods=['GET', 'POST'])
@login_required
def post_comment(id):
    ''' function to post comments '''
    form = CommentForm()
    title = 'post comment'
    posts = Post.query.filter_by(id=id).first()

    if postss is None:
         abort(404)

    if form.validate_on_submit():
        opinion = form.opinion.data
        new_comment = Comments(opinion=opinion, user_id=current_user.id, posts_id=posts.id)
        new_comment.save_comment()
        return redirect(url_for('.view_post', id=posts.id))

    return render_template('post_comment.html', comment_form=form, title=title)

#Routes upvoting/downvoting pitches
@main.route('/post/upvote/<int:id>')
@login_required
def upvote(id):
    '''
    View function that add one to the vote_number column in the votes table
    '''
    post_id = Post.query.filter_by(id=id).first()

    if post_id is None:
         abort(404)

    new_vote = Votes(vote=int(1), user_id=current_user.id, posts_id=posts_id.id)
    new_vote.save_vote()
    return redirect(url_for('.view_post', id=id))



@main.route('/post/downvote/<int:id>')
@login_required
def downvote(id):

    '''
    View function that add one to the vote_number column in the votes table
    '''
    post_id = Post.query.filter_by(id=id).first()

    if post_id is None:
         abort(404)

    new_vote = Votes(vote=int(2), user_id=current_user.id, posts_id=post_id.id)
    new_vote.save_vote()
    return redirect(url_for('.view_post', id=id))

@main.route('/post/downvote/<int:id>')
def vote_count(id):
    '''
    View function to return the total vote count per pitch
    '''
    votes = Votes.query.filter_by(user_id=user_id, line_id=line_id).all()

    total_votes = votes.count()

    return total_votes


@main.route('/user/<uname>')

def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)


@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():

        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)


@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        user_photo = PhotoProfile(pic_path = path,user = user)
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))
