from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=16)
    password = models.CharField(max_length=16)

class Images(models.Model):
    username = models.CharField(max_length=16)
    imagesource = models.TextField()
    fractype = models.CharField(max_length=16)
    rowres = models.IntegerField(default=0)
    colres = models.IntegerField(default=0)
    xmin = models.FloatField(default=0)
    xmax = models.FloatField(default=0)
    ymin = models.FloatField(default=0)
    ymax = models.FloatField(default=0)
    cr = models.FloatField(default=0)
    ci = models.FloatField(default=0)



'''
 check if user exist
 @:param username: the user name
 @:true if user exists, else false
 '''
def is_user_exist(username):
    query_set = User.objects.filter(username = username)
    return len(query_set) != 0

'''
 user log in
 @:param username: the user name
 @:param password: the password
 @:true if there is the user and password matches, else false
 '''
def log_in(username, password):
    if not is_user_exist(username):
        return False
    query_set = User.objects.filter(username = username)
    cur_user = query_set[0]
    return cur_user.password == password

'''
 user sign up
 @:param username: the user name
 @:true if added, else false
 '''
def sign_up(username, password):
    if is_user_exist(username):
        return False
    cur_user = User(username = username, password = password)
    cur_user.save()
    return True

'''
add img
 @:post_obj: the post object
 @:true
 '''
def add_img(post_obj):
    username = str(post_obj['username'])
    imagesource = str(post_obj['img_src'])
    fractype = ""
    if "fractype" in post_obj:
        fractype = str(post_obj['fractype'])
    elif "noisetype" in post_obj:
        fractype = str(post_obj['noisetype'])
    cur_img = Images(username = username, imagesource = imagesource, fractype = fractype)
    cur_img.save()
    return True

'''
get img
Get the saved img of the given user
 @:param username: the user name
 @:return: list of image source
 '''
def get_img(username):
    query_set = Images.objects.filter(username = username)
    res = []
    type_list = []
    for i in query_set:
        cur = {}
        cur['img_src'] = i.imagesource
        cur['img_type'] = i.fractype
        res.append(cur)
    return res
