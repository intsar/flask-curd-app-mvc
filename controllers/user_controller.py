from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.database import get_db_connection

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', users=users)

@user_blueprint.route('/add', methods=['GET','POST'])
def add():
    if request.method == 'POST':
        name = request.form.get('name') or request.name
        email = request.form.get('email') or request.email
        phone = request.form.get('phone') or request.phone
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * from flask_curd.users where email = %s", (email,))
        emailExists = cursor.fetchone()
        if emailExists :
            error = "Email Id already exists"
            return render_template('add.html', error=error)
        
        cursor.execute("INSERT INTO flask_curd.users (name, email, phone) VALUES (%s, %s, %s)", (name, email, phone))
        conn.commit()
        cursor.close()
        return redirect(url_for('user.index'))
    return render_template('add.html');

@user_blueprint.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    db = get_db_connection()
    if request.method == 'GET':
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * from users where id = %s", (id,))
        user = cursor.fetchone()
        cursor.close()
        return render_template('edit.html', user = user)
    else :
        name = request.form.get('name') or request.name
        email = request.form.get('email') or request.email
        phone = request.form.get('phone') or request.phone
        cursor = db.cursor()
        cursor.execute(""" UPDATE flask_curd.users 
                       SET name =%s, email = %s, phone = %s 
                       WHERE id=%s 
                       """, (name, email, phone, id))
        db.commit()
        cursor.close()
        return redirect(url_for('user.index'))

@user_blueprint.route('/delete/<int:id>')
def delete(id): 
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM flask_curd.users where id = %s", (id,))
    db.commit()
    cursor.close()
    return redirect(url_for('user.index'))