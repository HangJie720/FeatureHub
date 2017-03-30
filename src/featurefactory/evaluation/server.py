#!/usr/bin/env python3
"""
Evaluation server for Feature Factory user notebooks
"""

from functools import wraps
import json
import os
from urllib.parse import quote

from flask import Flask, redirect, request, Response

from jupyterhub.services.auth import HubAuth

class EvaluationResult:
    def __init__(self):
        pass

prefix = os.environ.get("JUPYTERHUB_SERVICE_PREFIX", "/")

auth = HubAuth(
    api_token=os.environ["JUPYTERHUB_API_TOKEN"],
    cookie_cache_max_age=60,
)

app = Flask(__name__)

def authenticated(f):
    """Decorator for authenticating with the Hub"""
    @wraps(f)
    def decorated(*args, **kwargs):
        cookie = request.cookies.get(auth.cookie_name)
        if cookie:
            user = auth.user_for_cookie(cookie)
        else:
            user = None
        if user:
            return f(user, *args, **kwargs)
        else:
            # redirect to login url on failed auth
            return redirect(auth.login_url + "?next=%s" % quote(request.path))
    return decorated

@app.route(prefix + "/evaluate", methods=["POST"])
@authenticated
def evaluate(user):
    # post elements
    code        = request.form["code"]
    description = request.form["description"]
    problem     = request.form["problem"]

    score = -1.0
    return Response(
        json.dumps(score, indent=1, sort_keys=True),
        mimetype="application/json",
        )

@app.route(prefix + '/')
@authenticated
def whoami(user):
    return Response(
        json.dumps(user, indent=1, sort_keys=True),
        mimetype='application/json',
        )

