# School Students managment API (Basic CRUD server)

### Description
A CRUD server for viewing and editing a student database.
JWT is implemented for authorization


Using the API you can:
* get all students
* get specific student
* add student (admins only)
* get all students in a specific class (admins only)

## Quick start
First of all you need to have a .env file with this variable:
```
secret=yoursecret
```
It will be used to generate jwt tokens

Install dependencies
```bash
pip install -r requirements.txt
```
Run the server using `uvicorn`
```bash
uvicorn server:app --reload
```

If you want to run the tests
```bash
python -m pytest
```

## Demo
There is a .json database with sample users.
To test admin privliges, sign in using the following user:

username: tarek

password: t123

For normal guest user, sign-up or use this user:

username: rami

password: r123

## Authentication
It's basically checking that the user is indead the person they claim they are.
This is done by checking the provided credintials (username/password) against what we have in our database.
Of course the password would be stored in an encrypted form using encryption tools like bcrypt.


## Authorization
### For authorization we will use **JWT**
A tool used to help us with authorization AFTER the user has already signed-in and authenticated.
JWT would "sign" a piece of information about the user (such as their roles) and generate a token accordingly.
Then the user would keep using that same token while they communicate with our API or service.
So, when JWT is used, the user does not have to keep providing their username and password with every request.
AKA we get Single Sign On feature!

## Main points of failure of the server
- Manual id creation: This would cause failure when trying to accedently create a new user using and existing id. it must be automaticaly created using a uuid creation tool.
- Data in the database is stored as a list of dictionaries. This is great for filtering and sorting the data, but it has a time complexity of O(n) when you try to get or delete a specific student by id. So incase of huge data sets, it would be slow.
- Highlt coupled with some jwt authorization library: in future it may be a problem if I decide to use a different tool for authorization.

### TODO backlog
Some improvements that needs to be done:
- Increment id automatically when new student is added