from app import signup
from app import loginpage

def test_signup_missing_firstname(client):
    data = {
        'LastName': 'Bjering',
        'Email': 'oscar.bjering@gmail.com',
        'Password': 'Potatis'
    }
    