# Flask and MySQL Blog

[![GitHub issues](https://img.shields.io/github/issues/Dev-Elie/Search-Weather-Wordnet-Location-Web-App)](https://github.com/Dev-Elie/Search-Weather-Wordnet-Location-Web-App/issues)
[![GitHub forks](https://img.shields.io/github/forks/Dev-Elie/Search-Weather-Wordnet-Location-Web-App)](https://github.com/Dev-Elie/Search-Weather-Wordnet-Location-Web-App/network)
[![Twitter](https://img.shields.io/twitter/url?style=social&url=https%3A%2F%2Ftwitter.com%2F)](https://twitter.com/intent/tweet?text=Wow:&url=https%3A%2F%2Fgithub.com%2FDev-Elie%2FSearch-Weather-Wordnet-Location-Web-App)

### Requirements ,Packages used and Installation
Download and install Python, for this tutorial I'll be using Python 3.8.5, make sure to check the box Add Python to PATH on the installation setup screen
 
### Installation
          
Navigate to your current project directory for this case it will be **Truck-Hiring-Web-App**. <br>
          
### 1 .Clone the git repo and create an environment 
          
Depending on your operating system,make a virtual environment to avoid messing with your machine's primary dependencies
          
**Windows**
          
```
git clone https://github.com/Dev-Elie/Teksade-Blog.git
cd Teksade-Blog
py -3 -m venv venv

```
          
**macOS/Linux**
          
```
git clone https://github.com/Dev-Elie/Teksade-Blog.git
cd Teksade-Blog
python3 -m venv venv

```

### 2 .Activate the environment
          
**Windows** 

```venv\Scripts\activate```
          
**macOS/Linux**

```. venv/bin/activate```
or
```source venv/bin/activate```

### 3 .Install the requirements

Applies for windows/macOS/Linux

```pip install -r requirements.txt```

### 4 .Migrate/Create a database

Applies for windows/macOS/Linux

```python manage.py```

### 5. Run the application 

**For linux and macOS**
Make the run file executable by running the code

```chmod 777 run```

Then start the application by executing the run file

```./run```

**On windows**
```
set FLASK_APP=main
flask run

```
The run file incase missing,create a new file name it **run** then add the following;

```FLASK_APP=main.py FLASK_DEBUG=1 FLASK_ENV=development flask run```


Liked this project ? Let's tweet about it [![Twitter](https://img.shields.io/twitter/url?style=social&url=https%3A%2F%2Ftwitter.com%2F)](https://twitter.com/intent/tweet?text=Wow:&url=https%3A%2F%2Fgithub.com%2FDev-Elie%2FSearch-Weather-Wordnet-Location-Web-App)
