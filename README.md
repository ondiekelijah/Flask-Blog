# Teksade-Blog

[![GitHub issues](https://img.shields.io/github/issues/Dev-Elie/Search-Weather-Wordnet-Location-Web-App)](https://github.com/Dev-Elie/Search-Weather-Wordnet-Location-Web-App/issues)
[![GitHub forks](https://img.shields.io/github/forks/Dev-Elie/Search-Weather-Wordnet-Location-Web-App)](https://github.com/Dev-Elie/Search-Weather-Wordnet-Location-Web-App/network)
[![Twitter](https://img.shields.io/twitter/url?style=social&url=https%3A%2F%2Ftwitter.com%2F)](https://twitter.com/intent/tweet?text=Wow:&url=https%3A%2F%2Fgithub.com%2FDev-Elie%2FSearch-Weather-Wordnet-Location-Web-App)

# Description
A fully functional blog website with CRUD capabilities. Developed using Python Flask framework and MySQL. 
#### Enables a user to:
* Create an account
* Login
* Update Account info
* Comment to posts
* Reply to comments on posts
#### Admin can;
* Add new posts
* Add new users
* Delete Posts
* Delete and Edit User info
* Delete, moderate and Edit comments

**NB:** Commands issued are for a linux environment,however no one is limited.
# Issues
> When executing the migrate commands to create a new database and when insering user roles,often a **Circular import error is raised**.
> To fix or avoid this,check on the app.py file and do the following
  * Do an inverse operation like this,comment line **1-75**
  * Uncomment lines **78-103**
> Next,check the models.py,do the following
  * Comment line **1**
  * Uncomment line **11**
  Proceed with the steps as shown below from installation
  
  **NB:** After the database migration and after inserting the user roles. Reverse the actions performed above before launching the application

# Installation
1. Create a new folder for the project and navigate into it
```
$ mkdir my_project
$ cd my_project
```
2.Inside the newly created folder create a virtual environment
```
 $ Python3.9 -m venv < env name>
```
3. Create another folder,name it "main",navigate to it and clone to it the applicatons files.
```
mkdir main
cd main
$ git clone https://github.com/Dev-Elie/Teksade-Blog.git
```
# Usage
1. Activate the virtual environment
```
$. venv/bin/activate
OR
$ source venv/bin/activate
``` 
2. Navigate into the "main" folder and install the requirements.
```
$ pip install -r requirements.txt
```
3. Use Migrate to create a new database
```
$ flask db init
$ flask db migrate -m "Initial migration."
$ flask db upgrade
```
4. Insert User Roles
```
$ from app import create_app
$ app = create_app()
$ app.app_context().push()
$ from models import Role
$ from app import db
$ Role.insert_roles()
$ Role.query.all()
```

6. Make the run file an executable
```
$ chmod 777 run
```
6. Launch the application
```
$ ./run
```
# Preview
![Home](https://github.com/Dev-Elie/Portfolio/blob/main/images/projects/blog.png)

Liked this project ? Let's tweet about it [![Twitter](https://img.shields.io/twitter/url?style=social&url=https%3A%2F%2Ftwitter.com%2F)](https://twitter.com/intent/tweet?text=Wow:&url=https%3A%2F%2Fgithub.com%2FDev-Elie%2FSearch-Weather-Wordnet-Location-Web-App)
