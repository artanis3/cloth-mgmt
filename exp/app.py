from flask import Flask, jsonify, render_template, request, redirect, send_from_directory, url_for ,session, flash,request
from flask_mysqldb import MySQL
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
import os
from datetime import date, datetime
from sqlalchemy import create_engine
import pandas as pd
import stripe
import logging
import random
import requests



app = Flask(__name__)
logging.basicConfig(level=logging.ERROR)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'akshayg2003'
app.config['MYSQL_DB'] = 'cloths'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = 'static/uploads/'


if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


mysql = MySQL(app)



with app.app_context():
    cur = mysql.connection.cursor()


    cur.execute('''
         CREATE TABLE IF NOT EXISTS male_shirts (
             mshirt_id VARCHAR(20) PRIMARY KEY,
             image_url_l VARCHAR(255)
         )
     ''')
    
    cur.execute('''
         CREATE TABLE IF NOT EXISTS male_pants (
             mpant_id VARCHAR(20) PRIMARY KEY,
             image_url_l VARCHAR(255)
         )
     ''')
    
    cur.execute('''
         CREATE TABLE IF NOT EXISTS female_shirts (
             fshirt_id VARCHAR(20) PRIMARY KEY,
             image_url_l VARCHAR(255)
         )
     ''')
    
    cur.execute('''
         CREATE TABLE IF NOT EXISTS female_pants (
             fpant_id VARCHAR(20) PRIMARY KEY,
             image_url_l VARCHAR(255)
         )
     ''')
    


@app.route('/')
def login():
    return render_template('login.html')



@app.route('/main_menu')
def main_menu():
    return render_template('main_menu.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.route('/add_mshirt', methods=['GET', 'POST'])
def add_mshirt():
    if request.method == 'POST':
        mshirt_id = request.form['mshirt_id']

        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO male_shirts(mshirt_id, image_url_l) VALUES (%s, %s)", (mshirt_id, filename))  
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('main_menu'))
    return render_template('add_mshirt.html')



@app.route('/add_mpant', methods=['GET', 'POST'])
def add_mpant():
    if request.method == 'POST':
        mpant_id = request.form['mpant_id']

        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO male_pants(mpant_id, image_url_l) VALUES (%s, %s)", (mpant_id, filename))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('main_menu'))
    return render_template('add_mpant.html')


@app.route('/add_fshirt', methods=['GET', 'POST'])
def add_fshirt():
    if request.method == 'POST':
        fshirt_id = request.form['fshirt_id']

        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO female_shirts(fshirt_id, image_url_l) VALUES (%s, %s)", (fshirt_id, filename))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('main_menu'))
    return render_template('add_fshirt.html')

@app.route('/add_fpant', methods=['GET', 'POST'])
def add_fpant():
    if request.method == 'POST':
        fpant_id = request.form['fpant_id']

        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO female_pants(fpant_id, image_url_l) VALUES (%s, %s)", (fpant_id, filename))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('main_menu'))
    return render_template('add_fpant.html')



@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/display_mcloth')
def display_mcloth():
    cur = mysql.connection.cursor()
    cur.execute("SELECT image_url_l FROM male_shirts")
    mshirt_images = [row[0] for row in cur.fetchall()]
    cur.execute("SELECT image_url_l FROM male_pants")
    mpant_images = [row[0] for row in cur.fetchall()]
    return render_template('display_mcloth.html', mshirt_images=mshirt_images, mpant_images=mpant_images)

@app.route('/display_fcloth')
def display_fcloth():
    cur = mysql.connection.cursor()
    cur.execute("SELECT image_url_l FROM female_shirts")
    fshirt_images = [row[0] for row in cur.fetchall()]
    cur.execute("SELECT image_url_l FROM female_pants")
    fpant_images = [row[0] for row in cur.fetchall()]
    return render_template('display_fcloth.html', fshirt_images=fshirt_images, fpant_images=fpant_images)


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        item_id = request.form['item_id']
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM male_shirts WHERE mshirt_id = %s", [item_id])
        cur.execute("DELETE FROM male_pants WHERE mpant_id = %s", [item_id])
        cur.execute("DELETE FROM female_shirts WHERE fshirt_id = %s", [item_id])
        cur.execute("DELETE FROM female_pants WHERE fpant_id = %s", [item_id])
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('main_menu'))
    return render_template('delete.html')


import random

@app.route('/view_mcombination')
def view_mcombination():
    cur = mysql.connection.cursor()
    cur.execute("SELECT mshirt_id, image_url_l FROM male_shirts")
    mshirts = cur.fetchall()
    cur.execute("SELECT mpant_id, image_url_l FROM male_pants")
    mpants = cur.fetchall()
    mshirt = random.choice(mshirts)
    mpant = random.choice(mpants)
    return render_template('view_mcombination.html', mshirt=mshirt, mpant=mpant)

@app.route('/view_fcombination')
def view_fcombination():
    cur = mysql.connection.cursor()
    cur.execute("SELECT fshirt_id, image_url_l FROM female_shirts")
    fshirts = cur.fetchall()
    cur.execute("SELECT fpant_id, image_url_l FROM female_pants")
    fpants = cur.fetchall()
    fshirt = random.choice(fshirts)
    fpant = random.choice(fpants)
    return render_template('view_fcombination.html', fshirt=fshirt, fpant=fpant)


@app.route('/remove_bg', methods=['GET', 'POST'])
def remove_bg():
    if request.method == 'POST':
        image_id = request.form['image_id']
        table_name = request.form['table_name']
        cur = mysql.connection.cursor()
        cur.execute(f"SELECT image_url_l FROM {table_name} WHERE id = %s", [image_id])
        result = cur.fetchone()
        if result is None:
            return 'No image found with the provided ID.'
        image_url = result[0]
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_url)

        response = requests.post(
            'https://api.remove.bg/v1.0/removebg',
            files={'image_file': open(image_path, 'rb')},
            data={'size': 'auto'},
            headers={'X-Api-Key': 'INSERT-YOUR-API-KEY-HERE'},
        )
        if response.status_code == requests.codes.ok:
            with open('static/no-bg.png', 'wb') as out:
                out.write(response.content)
            return render_template('show_image.html')
        else:
            return 'Error removing background: {}'.format(response.text)

    return render_template('remove_bg.html')



if __name__ == '__main__':
    app.run(debug=True)






