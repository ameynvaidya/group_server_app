from flask import Blueprint,  render_template, session

from flask_login import login_required, current_user


main = Blueprint('main', __name__)

@main.route('/')
def index():
    session.clear()
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)
    

