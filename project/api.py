from os import abort
from flask import Blueprint, request, abort, jsonify
import re
from . import db
from .models import User, UserAccessToken
import time

api = Blueprint('api', __name__)

@api.route('/api/get_profile')
def get_profile():
    auth_header = request.headers['Authorization']
    access_token = re.sub("^Bearer ", "", auth_header)
    user_access_token = UserAccessToken.query.filter_by(access_token=access_token).first()
    if (not user_access_token):
        abort(400, 'Invalid access token')

    # check if access token is expired
    token_expires_at = user_access_token.access_token_creation_time + user_access_token.access_token_expires_in
    current_time = int(time.time())
    if (current_time > token_expires_at):
        abort(400, 'Access token expired')
    
    user = User.query.filter_by(id=user_access_token.id).first()
    if (not user):
        abort(400, 'Invalid access token')

    data = {
        "user_id": user.id,
        "email": user.email,
        "name": user.name,
    }
    return jsonify(data)