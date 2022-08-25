# ecommerce-django
This is a sample application that demonstrates an e-commerce website using the Python Django. The application loads products from a PostgreSQL database and displays them. Users can select to display products in a single category. Users can register and login to website and, click on any product to get more information including pricing, reviews and rating. Users can select items and add them to their shopping cart,and complete their payment using Razor-pay or cod. They can view their order status, can download invoice and add review of product.
In admin side, admins can manage users,products,categories,discount coupons,orders etc...


## Live Demonstration

The E-commerce demo can be viewed online here: https://savebox.ae

Here is the screencast that show the E-commerce demo application in use: https://youtu.be/PEueuoEQ5S8


## Getting started
To get started you can simply clone this ecommerce-django repository and install the dependencies.

Clone the ecommerce-demo repository using git:
```python
git clone https://github.com/noufida/ecommerce-django.git
cd ecommerce-django
```
Create a virtual environment to install dependencies in and activate it:
```python
python3 -m venv env
source env/bin/activate
```

Then install the dependencies:
```python
(env)$ pip install -r requirement.txt
```
Note the ```(env)``` in front of the prompt. This indicates that this terminal session operates in a virtual environment set up by virtualenv2.

Once ```pip``` has finished downloading the dependencies:
```python
(env)$ cd ecommerce-django
(env)$ python3 manage.py runserver
```
And navigate to ```http://127.0.0.1:8000/```


## Tech Stack
  Python
  
  Django
  
  PostgreSQL
  
  Bootstrap
  
  Javascript
