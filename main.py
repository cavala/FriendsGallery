from urllib import response
import boto3
from logging import NullHandler
import requests
from bson.objectid import ObjectId
from flask import Flask, render_template, redirect, request, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

from helpers import is_access_token_valid, is_id_token_valid, config
from mxuser import mxUser

from user import User 
from post import *
from db import *

from werkzeug.utils import secure_filename

import key_config as key



app = Flask(__name__)
app.config.update({'SECRET_KEY': 'SomethingNotEntirelySecret'})

login_manager = LoginManager()
login_manager.init_app(app)


APP_STATE = 'ApplicationState'
NONCE = 'SampleNonce'




@login_manager.user_loader
def load_user(user_id):
    return mxUser.get(user_id)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login")
def login():
    # get request params
    query_params = {'client_id': config["client_id"],
                    'redirect_uri': config["redirect_uri"],
                    'scope': "openid email profile",
                    'state': APP_STATE,
                    'nonce': NONCE,
                    'response_type': 'code',
                    'response_mode': 'query'}

    # build request_uri
    request_uri = "{base_url}?{query_params}".format(
        base_url=config["auth_uri"],
        query_params=requests.compat.urlencode(query_params)
    )

    return redirect(request_uri)


@login_required
@app.route('/like<postId>/')
def like(postId):
    aDb = get_database()    
    usr = User(_id = current_user.id, email=current_user.email, name=current_user.name)
    usr.save()
    imgPost = ImagePost.objects.get(id = ObjectId(postId))
    imgPost.likes.append(usr.to_dbref())
    imgPost.save()
    return redirect(url_for('gallery'))

@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=current_user)

@app.route("/gallery" , methods=['post', 'get']) 
def gallery():
    aDb = get_database() 
    imgPosts = aDb.myFirstDatabase.post.find({'_cls': 'Post.ImagePost','visible': False})
    aImgDict = []
    for img in imgPosts:
        s3_client = boto3.client('s3',
                        aws_access_key_id = key.access_key,
                        aws_secret_access_key = key.secret_access_key) 

        imgSrc = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': key.s3_bucket_name,
                'Key': key.s3_folder_name +'/'+ img['imagename'] 
            },
            ExpiresIn=3600
        )        
         
        aCommentDict = []
        for comment in img['comments']:
            commentUsr = aDb.myFirstDatabase.user.find_one({'_id': comment['author']})            
            aCommentDict.append({'username':commentUsr['name'], 'comment':comment['content']})
        
        aLikesDict = []
        
        for like in img['likes']:           
            usrLike = aDb.myFirstDatabase.user.find_one({'_id': like})                         
            aLikesDict.append({'username': usrLike['name']})

        aImgDict.append(({'postId': img['_id'],
                          'imgSrc': imgSrc, 
                          'imgTitle': img['title'],
                          'comments': aCommentDict, 
                          'likes': aLikesDict 
                          })) 
    return render_template("gallery.html", user=current_user, imgDict = aImgDict)



@app.route("/uploadImage" , methods=['post', 'get'])
@login_required
def uploadImage():
    if request.method == 'POST':
        aDb = get_database() 
        imgPost = ImagePost(title = request.form.get("comments")) # img.filename
        usr = User(_id = current_user.id, email=current_user.email, name=current_user.name)       
       
        usr.save()
        imgPost.author = usr.to_dbref()
        
        s3_client = boto3.client('s3',
                        aws_access_key_id = key.access_key,
                        aws_secret_access_key = key.secret_access_key) 

        #img = request.form.get("myfile")
        
        img = request.files["myfile"]
        
        if img:
            filename = secure_filename(img.filename)
           
            img.save(filename)
            imgPost.imagename = filename

            s3_client.upload_file(filename, 
                            key.s3_bucket_name, 
                            key.s3_folder_name +'/'+ filename)

            msg = "Upload Done ! "                    
            imgPost.save()

            return render_template("uploadImage.html", user=current_user, msg =msg)
    return render_template("uploadImage.html", user=current_user )


@app.route("/authorization-code/callback")
def callback():
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    code = request.args.get("code")
    if not code:
        return "The code was not returned or is not accessible", 403
    query_params = {'grant_type': 'authorization_code',
                    'code': code,
                    'redirect_uri': request.base_url
                    }
    query_params = requests.compat.urlencode(query_params)
    exchange = requests.post(
        config["token_uri"],
        headers=headers,
        data=query_params,
        auth=(config["client_id"], config["client_secret"]),
    ).json()

    # Get tokens and validate
    if not exchange.get("token_type"):
        return "Unsupported token type. Should be 'Bearer'.", 403
    access_token = exchange["access_token"]
    id_token = exchange["id_token"]

    if not is_access_token_valid(access_token, config["issuer"]):
        return "Access token is invalid", 403

    if not is_id_token_valid(id_token, config["issuer"], config["client_id"], NONCE):
        return "ID token is invalid", 403

    # Authorization flow successful, get userinfo and login user
    userinfo_response = requests.get(config["userinfo_uri"],
                                     headers={'Authorization': f'Bearer {access_token}'}).json()

    unique_id = userinfo_response["sub"]
    user_email = userinfo_response["email"]
    user_name = userinfo_response["given_name"]

    xUser = mxUser(
        id_=unique_id, name=user_name, email=user_email
    )

    if not mxUser.get(unique_id):
        mxUser.create(unique_id, user_name, user_email)

    usr = User(_id = unique_id, email=user_email, name=user_name)
    
    if not User.get(_id = unique_id):
        User.create(unique_id, user_email, user_name)    
    
    login_user(xUser)
    #login_user(usr)

    return redirect(url_for("uploadImage"))


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(host="localhost", port=8080, debug=True)
    