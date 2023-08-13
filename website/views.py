from django.shortcuts import render,redirect
from django.contrib import messages
from users.models import User
import requests
import json
from django.http import HttpResponse
from users.serializers import UserSerializer
import json
from json import JSONEncoder
import datetime
    
# Create your views here.

def index(request):

    return render(request,"index.html")

def register(request):

    if request.method =="POST":
        #get user entries
        name=request.POST['name']
        password=request.POST['password']
        email=request.POST['email']

        #validation to ensure no field is empty
        if ((name=="") or (password=="") or (email=="")):
            messages.info(request,'Please fill all the fields to register..')
            return redirect('register')

        else:
            userDict = {
                "name": name,
                "email": email,
                "password":password
            }

            response = requests.post('http://127.0.0.1:8000/users/register', json=userDict)
            print(response.json())

            
        return render(request,'login.html')
    else:
        return render(request,'register.html')




def login(request):

    if request.method=='POST':
        #get email and password from the user
        email=request.POST['email']
        password=request.POST['password']

        #validation to ensure no field is empty
        if ((email=="") or (password=="")):
            messages.info(request,'Please fill all the fields to login..')
            return render(request,'login.html')

        else:
            userDict = {
                "email": email,
                "password":password
            }

            response = requests.post('http://127.0.0.1:8000/users/login', json=userDict) #the token
            #print(response.json())

            global userAuthStatus
            global userdetails

            if response.status_code != requests.codes.ok:
                
                if response.json()["detail"]=='User not found!' or response.json()["detail"]=='Incorrect password!':
                    
                    userAuthStatus = False

                    messages.info(request,'Unauthenticated..')
                    return render(request,'login.html')

            else:

                userAuthStatus = True

                userResponse = requests.get('http://127.0.0.1:8000/users/user',cookies=response.cookies)
                #print(userResponse.json())

                userdetails = userResponse.json()

                if userResponse.status_code != requests.codes.ok:


                    if userdetails["detail"]=='Unauthenticated!':
                    
                        userAuthStatus = False

                        messages.info(request,'Unauthenticated..')
                        return render(request,'login.html')

                if 'userAuthStatus' not in globals():
                    return render(request,'login.html')
                else:

                    context= {"authenticated":userAuthStatus, "name":userdetails["name"]}
                    #print(context)
            
                    return render(request,'index.html', context)

    else:
        return render(request,'login.html')
    
def logout(request):

    response = requests.post('http://127.0.0.1:8000/users/logout',request)
    print(response.json())

    userAuthStatus = False

    context= {"authenticated":userAuthStatus}

    return render(request,'index.html', context)

def post(request):

    if request.method=='POST':
            #get title and content from the user
            title=request.POST['title']
            content=request.POST['content']

            #validation to ensure no field is empty
            if ((title=="") or (content=="")):
                messages.info(request,'Please fill all the fields..')
                return redirect('post')

            else:

                if 'userAuthStatus' not in globals():
                    return render(request,'login.html')
                else:
        
                    postDict = {
                        "title": title,
                        "content": content,
                        "author":userdetails["id"],
                        "author_name":userdetails["name"]
                        #"author":   json.dumps(user, indent=4, cls=CustomEncoder)
                    }

                    response = requests.post('http://127.0.0.1:8000/posts/posts/', json=postDict) #the token
                    #print(response.json())
            
                    context= {"authenticated":userAuthStatus, "name":userdetails["name"]}

                    return render(request,'index.html', context)

    else:
        return render(request,'index.html')
    

def allposts(request):    

    response = requests.get('http://127.0.0.1:8000/posts/posts/') #the token
    #print(response.json())

    if response.json():
        postsExist=True

    if not response.json():
        postsExist=False

    postsList = response.json()

    allposts={
        "postsList":postsList,
        "postsExist":postsExist,
    }

    if 'userAuthStatus' not in globals():
        return render(request,'login.html')
    else:
        
        context= {"allposts":allposts,"authenticated":userAuthStatus, "name":userdetails["name"]}

        return render(request,'index.html', context)

def G_post(request):    
    
    postID=request.POST['id']

    #validation to ensure no field is empty
    if ((postID=="") or (postID==None)):
        messages.info(request,'Please fill all the fields..')
        return redirect('post')
    
    if 'userAuthStatus' not in globals():
        return render(request,'login.html')
    else:
        
        authorID = userdetails["id"]

        response = requests.get('http://127.0.0.1:8000/posts/posts/'+str(postID)+'/'+str(authorID)) #the token

        #print("responseuuuuuuuuuu", response, response.status_code)

        if response.status_code == requests.codes.ok:
            print ('OK!')
            get_post_details = {
                "id":response.json()["id"],
                "title":response.json()["title"],
                "content":response.json()["content"],
                "message":"success"
            }

            context= {"get_post_details":get_post_details,"authenticated":userAuthStatus, "name":userdetails["name"]}

            return render(request,'index.html', context)
        else:
            print ('Boo!')
                
            get_post_details = {
                "id":id,
                "message":"Either the post with ID=="+str(postID)+" is not exist or you are not the its author"
            }

            context= {"get_post_details":get_post_details,"authenticated":userAuthStatus, "name":userdetails["name"]}

            return render(request,'index.html', context)

    

def U_post(request):    
    
    postID=request.POST['id']
    title=request.POST['title']
    content=request.POST['content']

    #validation to ensure no field is empty
    if ((postID=="") or (postID==None) or (title=="") or (content=="")):
        messages.info(request,'Please fill all the fields..')
        return redirect('post')
    
    postDict = {
        "title": title,
        "content":content
    }
    
    if 'userAuthStatus' not in globals():
        return render(request,'login.html')
    else:
        
        authorID = userdetails["id"]

        response = requests.put('http://127.0.0.1:8000/posts/posts/'+str(postID)+'/'+str(authorID),json=postDict) #the token

        if response.status_code == requests.codes.ok:
            update_post_details = {
                "id":response.json()["id"],
                "title":response.json()["title"],
                "content":response.json()["content"],
                "message":"success"
            }

            context= {"update_post_details":update_post_details,"authenticated":userAuthStatus, "name":userdetails["name"]}

            return render(request,'index.html', context)
        
        else:
            update_post_details = {
                "id":id,
                "message":"Either the post with ID=="+str(postID)+" is not exist or you are not the its author"
            }
        
            context= {"update_post_details":update_post_details,"authenticated":userAuthStatus, "name":userdetails["name"]}

            return render(request,'index.html', context)

def D_post(request):    
    
    postID=request.POST['id']

    #validation to ensure no field is empty
    if ((postID=="") or (postID==None)):
        messages.info(request,'Please fill all the fields..')
        return redirect('post')
    
    if 'userAuthStatus' not in globals():
        return render(request,'login.html')
    else:
        
        authorID = userdetails["id"]

        response = requests.delete('http://127.0.0.1:8000/posts/posts/'+str(postID)+'/'+str(authorID)) #the token

        if response.status_code == 204:
            print ('OK!')

            context= {"deletemessage":"success..The post with ID=="+str(postID)+" deleted","authenticated":userAuthStatus, "name":userdetails["name"]}

            return render(request,'index.html', context)
        else:
            context= {"deletemessage":"Either the post with ID=="+str(postID)+" is not exist or you are not the its author","authenticated":userAuthStatus, "name":userdetails["name"]}

            return render(request,'index.html', context)


