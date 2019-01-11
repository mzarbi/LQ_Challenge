# project/server/main/views.py
import ast
import json

import redis
import requests
from rq import Queue, Connection
from flask import Blueprint, jsonify, \
    request, current_app
from werkzeug.utils import redirect

from project.server.main.models import Task

main_blueprint = Blueprint('main', __name__,)

@main_blueprint.route('/', methods=['GET'])
def index():
   """
    This is the index route
   """
   return '''
        <html>
            <body>
                <h1 style="color: #5e9ca0;">LeadIQ <span style="color:#2b2301;">challenge</span></h1>
                <form action="/echo" method="POST">
                    <input name="client_id" value="63bbb2cd9f0bf7c">
                    <input type="submit" value="Redirect">
                </form>
            </body>
        </html>'''

@main_blueprint.route("/echo", methods=['POST'])
def echo():
    """
    This route will take the client id entered in '/' and then will redirect to the imgur Authorization url
    """
    return redirect("https://api.imgur.com/oauth2/authorize?client_id=" + request.form['client_id'] + "&response_type=token&state=sssss", code=302)


@main_blueprint.route('/oauth2/callback/', methods=['GET', 'POST'])
def callback():
    """
    This route is the auth2 callback route, it will parse the client side in order to get the access token and then it will send them to /app_response_token
    """
    return '''
        <script type="text/javascript">
            var loc = window.location.toString() ;
            var res = loc.replace("#", "&");
            res = res.replace('http://localhost:5004/oauth2/callback/?','') ;

            var req = new XMLHttpRequest();  

            var params = res;
            //alert(res)
            var url = 'http://localhost:5004/' + 'app_response_token?'
            req.open('POST', url, true);

            req.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

            req.onreadystatechange = function() {//Call a function when the state changes.
                if(http.readyState == 4 && http.status == 200) {
                    alert(http.responseText);
                }
            }
            req.send(params);
            //alert('http://' + window.location.host + '/app_response_token?' + res)
        </script>
        Access Token Acquired
'''


@main_blueprint.route('/app_response_token', methods=['POST'])
def app_response_token():
    """
    this route serves as a mean to store the credentials in the redis server
    """
    tokens = {
        "access_token": request.form["access_token"],
        "refresh_token": request.form["refresh_token"],
        "token_type": request.form["token_type"],
        "account_username": request.form["account_username"],
        "expires_in": request.form["expires_in"],
        "account_id": request.form["account_id"]
    }

    # add credentials to the redis server
    rd = redis.from_url(current_app.config['REDIS_URL'])
    rd.set("credentials",str(tokens))

    return jsonify({"status" : "Ok"}), 202


@main_blueprint.route('/v1/images/upload', methods=['POST'])
def image_upload():
    """
    The image upload route
    """
    urls = request.json['urls']

    # get credentials from the redis server
    rd = redis.from_url(current_app.config['REDIS_URL'])
    try:
        credentials = rd.get("credentials")
    except:
        response_object = {'status': "error, no access token is found, without it you can no longer upload image files."}
        return jsonify(response_object)

    # create new Task
    tsk = Task()
    tsk.initialize(urls,credentials)

    # create and add Job
    with Connection(redis.from_url(current_app.config['REDIS_URL'])):
        q = Queue()
        task = q.enqueue('project.server.main.works.long_work', tsk)
    if task:
        response_object = {'jobId': task.get_id()}
    else:
        response_object = {
            'status': "error, could start job, this may mean that there are no workers running, or the redis server is down"}

    return jsonify(response_object), 202

@main_blueprint.route('/v1/images/upload/<jobId>', methods=['GET'])
def job_status(jobId):
    """
    The job status route
    """
    # fetch job by his id
    with Connection(redis.from_url(current_app.config['REDIS_URL'])):
        q = Queue()
        task = q.fetch_job(jobId)
    if task:
        # return job progress
        try:
            response_object = task.meta["progress"]
        except:
            response_object = {'status': 'error, could not fetch status'}
    else:
        response_object = {'status': 'error, could not resolve jobId'}
    return jsonify(response_object)

@main_blueprint.route('/v1/images', methods=['GET', 'POST'])
def image_links():
    """
    the images route
    """
    # get credentials from the redis server
    rd = redis.from_url(current_app.config['REDIS_URL'])
    try:
        cred = rd.get("credentials")
    except:
        response_object = {
            'status': "error, no access token is found, without it you can no longer fetch image files."}
        return jsonify(response_object)


    try:
        clean = str(cred).replace('b\"', '').replace('\"', '').replace("'", '"')
        clean_dict = ast.literal_eval(clean)
        token = clean_dict["access_token"]
        refresh_token = clean_dict["refresh_token"]
        account_username = clean_dict["account_username"]
        authentication = {'Authorization': 'Bearer {0}'.format(token)}

    except:
        response_object = {
            'status': "error, no access token is found, without it you can no longer fetch image files."}
        return jsonify(response_object)

    # get al uploaded images from imgur
    resp = requests.get("https://api.imgur.com/3/account/" + account_username + "/images/", {},
                        headers=authentication,
                        verify=True)
    # generate response
    uploaded = []
    for i in json.loads(resp.content)["data"]:
        uploaded.append(i["link"])

    response_object = {"uploaded": uploaded}
    return jsonify(response_object)