from flask import Blueprint, redirect, render_template, request, session, url_for, jsonify, abort
from . import db
from flask_login import login_required, current_user
from .models import User, UserAuthCode, UserAccessToken
import secrets
import time

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)
    
@main.route('/oauth/authorize')
def authorize():
    client_id = request.args.get("client_id")
    response_type = request.args.get("response_type")
    redirect_uri = request.args.get("redirect_uri")
    state = request.args.get("state")
    if current_user.is_authenticated:
        auth_code = secrets.token_urlsafe(32)

        # store auth code in db
        user_auth_code = UserAuthCode.query.filter_by(id=current_user.id).first()
        if (user_auth_code):
            user_auth_code.auth_code = auth_code
        else:
            user_auth_code = UserAuthCode(id=current_user.id, auth_code=auth_code)
        db.session.add(user_auth_code)
        db.session.commit()
        return redirect(redirect_uri + "?state=" + state +"&code=" + auth_code + "&scope=read")
    else:
        session['url'] = request.url
        return redirect(url_for('auth.login'))


@main.route('/oauth/token', methods=['POST'])
def token_exchange():
    client_id = request.form.get("client_id")
    client_secret = request.form.get("client_secret")
    auth_code = request.form.get("code")
    grant_type = request.form.get("grant_type")

    # check if auth code is valid and derive the user_id
    user_auth_code = UserAuthCode.query.filter_by(auth_code=auth_code).first()
    if (not user_auth_code):
        abort(400, 'Not a valid auth code')

    # assign a new user_auth code since it is allowed to be use only ones

    user_auth_code.auth_code = secrets.token_urlsafe(32)
    db.session.add(user_auth_code)
    db.session.commit()

    user = User.query.filter_by(id=user_auth_code.id).first()
    if (not user):
        abort(400, 'Not a valid auth code (user)')
    access_token = secrets.token_urlsafe(16)
    refresh_token = secrets.token_urlsafe(16)
    access_token_creation_time = int(time.time())
    access_token_expires_in = 10
    user_access_token = UserAccessToken.query.filter_by(id=user_auth_code.id).first()
    if (not user_access_token):
        user_access_token = UserAccessToken(
            id=user.id, 
            access_token=access_token, 
            access_token_creation_time=access_token_creation_time,
            access_token_expires_in=access_token_expires_in,
            refresh_token=refresh_token)
    else:
        user_access_token.access_token = access_token
        user_access_token.access_token_creation_time = access_token_creation_time
        user_access_token.access_token_expires_in = access_token_expires_in
        user_access_token.refresh_token = refresh_token

    db.session.add(user_access_token)
    db.session.commit()

    data = {
        "token_type": "Bearer",
        "expires_in": access_token_expires_in,
        "refresh_token": refresh_token,
        "access_token": access_token,
    }
    return jsonify(data)
