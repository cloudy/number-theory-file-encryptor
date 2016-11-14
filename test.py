import os
import math
import itertools
from fractions import gcd
from random import randint
import binascii
import struct

from flask import Flask, render_template, flash, request, url_for
from flask.ext.wtf import Form
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from wtforms.validators import Required



DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
 

class ReusableForm(Form):
    str_encrypt = TextField('Number to encrypt:')
    str_decrypt = TextField('Encrypted text   :')
    str_key     = TextField('Key of Encrypted :')


@app.route("/", methods=['GET', 'POST'])
def main():
    form = ReusableForm(request.form)
 
    print(form.errors)
    if request.method == 'POST':
        if (request.form['str_encrypt']):
            str_encrypt=request.form['str_encrypt']
            print(str_encrypt)
     
            if form.validate():
                # Save the comment here.
                encrypted_data = encryptor(int(str_encrypt))
                flash('Encrypted Text: '+str(encrypted_data[0]))
                flash('Key:            '+str(encrypted_data[1]))
            else:
                flash('All the form fields are required. ')
        elif(request.form['str_decrypt'] != None):
            str_decrypt=request.form['str_decrypt']
            str_key = request.form['str_key']
            print(str_decrypt)
     
            if form.validate():
                # Save the comment here.
                decrypted_data = decryptor(int(str_decrypt), int(str_key))
                flash('Decrypted Text: '+str(decrypted_data))
            else:
                flash('All the form fields are required. ')             
 
    return render_template('index.html', form=form)

def is_prime(num):
    if num > 1:
        for i in range(2,num):
            if (num % i) == 0:
                return False;
                break
        else:
            return True;
    else:
        return False;

#Extended euclidean algorithm from:
# https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm

def xgcd(b, n):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while n != 0:
        q, b, n = b // n, n, b % n
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return  b, x0, y0

def encryptor(m):
    p = 2**31-1
    q = 2**61-1
    n = p * q
    phi = (p-1)*(q-1)
    
    e = randint(0,phi)
    while gcd(e, phi) != 1:
        e = randint(0,phi)
    
    bezout = xgcd(e, phi)
    
    d = bezout[1]%phi
    
    #words = 'sda'
    #print("ORIGINAL STRING: ", words)
    #m = toBinary(words)
    #print("WORDS TO BINARY: ", m)    
    #decword = toString(m)
    #print("DECWORD  DECODE: ",decword)
    #print("WORDS TO BINARY: ",m)
    print("ORIGINAL BEFR: ", m)
    #m = int(input("enter an int: "))

    c = pow(m,e,n)
    print("CIPHERTEXT ENC : ", c)
    return c, e

def decryptor(c, e):
    p = 2**31-1
    q = 2**61-1
    n = p * q
    phi = (p-1)*(q-1)
    
    bezout = xgcd(e, phi)
    
    d = bezout[1]%phi
    
    #words = 'sda'
    #print("ORIGINAL STRING: ", words)
    #m = toBinary(words)
    #print("WORDS TO BINARY: ", m)    
    #decword = toString(m)
    #print("DECWORD  DECODE: ",decword)
    #print("WORDS TO BINARY: ",m)
    #m = int(input("enter an int: "))

    decode = pow(c,d,n)
    print("ORIGINAL TEXT IN: ", decode)
    return decode


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=12345, debug=True)