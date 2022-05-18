from flask import Blueprint, redirect, render_template, request, session, url_for, jsonify, abort
from . import db
from flask_login import login_required, current_user

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
        return redirect(redirect_uri + "/state=" + state +"&code=" + current_user.id + ":h1m5sjtRqo976Ka25EEPkGu9L&scope=read")
    else:
        session['url'] = request.url
        return redirect(url_for('auth.login'))


@main.route('/oauth/token', methods=['POST'])
def token_exchange():
    client_id = request.form.get("client_id")
    client_secret = request.form.get("client_secret")
    auth_code = request.form.get("code")
    grant_type = request.form.get("grant_type")

    if (client_id == "1234" and client_secret == "secret_4321"):
        data = {
            "token_type": "Bearer",
            "expires_at": 1562908002,
            "expires_in": 21600,
            "refresh_token": "0JBApdViXJL0J5SEDxHK7psmE",
            "access_token": "uRgpMWA7HvgNDTR77772ZZ2KQ",
        }
        return jsonify(data)
    abort(400, 'Not Valid Client Secret')