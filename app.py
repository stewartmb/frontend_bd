from flask import Flask, render_template, request, redirect, url_for, flash
from config import get_connection

app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/users', methods=['POST', 'GET'])
def users():
    if request.method == 'POST':
        user_id = request.form['nombre']
        try:
            result = get_user_by_id(user_id)
            return render_template('search.html', users=result)
        except Exception as e:
            print(e)
            flash('Ocurrió un problema al buscar')
            return redirect(url_for('users'))
    else:
        result = get_all_users()
        return render_template('users.html', users=result)

@app.route('/properties', methods=['POST', 'GET'])
def properties():
    if request.method == 'POST':
        min_price = request.form['min_price']
        max_price = request.form['max_price']
        try:
            result = get_properties_by_price(min_price, max_price)
            return render_template('properties.html', properties=result)
        except Exception as e:
            print(e)
            flash('Ocurrió un problema al buscar')
            return redirect(url_for('properties'))
    else:
        result = get_all_properties()
        return render_template('properties.html', properties=result)

@app.route('/add_booking', methods=['POST', 'GET'])
def add_booking():
    if request.method == 'POST':
        booking_id = request.form['booking_id']
        total_price = request.form['total_price']
        timestamp = request.form['timestamp']
        check_in_date = request.form['check_in_date']
        check_out_date = request.form['check_out_date']
        guest_user_id = request.form['guest_user_id']
        property_id = request.form['property_id']
        try:
            add_new_booking(booking_id, total_price, timestamp, check_in_date, check_out_date, guest_user_id, property_id)
            flash('Reserva añadida exitosamente')
        except Exception as e:
            print(e)
            flash('Ocurrió un problema al añadir la reserva')
        return redirect(url_for('add_booking'))
    return render_template('add_booking.html')

@app.route('/add_review', methods=['POST', 'GET'])
def add_review():
    if request.method == 'POST':
        review_id = request.form['review_id']
        booking_id = request.form['booking_id']
        comment = request.form['comment']
        rating = request.form['rating']
        try:
            add_new_review(review_id, booking_id, comment, rating)
            flash('Reseña añadida exitosamente')
        except Exception as e:
            print(e)
            flash('Ocurrió un problema al añadir la reseña')
        return redirect(url_for('add_review'))
    return render_template('add_review.html')

@app.route('/verify_triggers')
def verify_triggers():
    hosts = get_all_hosts()
    guests = get_all_guests()
    properties = get_all_properties()
    bookings = get_all_bookings()
    return render_template('verify_triggers.html', hosts=hosts, guests=guests, properties=properties, bookings=bookings)

def get_user_by_id(user_id):
    db, cur = get_connection()
    query = 'SELECT * FROM airbnb_bd."user" WHERE user_id = %s'
    cur.execute(query, (user_id,))
    return cur.fetchall()

def get_all_users():
    db, cur = get_connection()
    query = 'SELECT * FROM airbnb_bd."user"'
    cur.execute(query)
    return cur.fetchall()

def get_all_properties():
    db, cur = get_connection()
    query = 'SELECT * FROM airbnb_bd."property"'
    cur.execute(query)
    return cur.fetchall()

def get_properties_by_price(min_price, max_price):
    db, cur = get_connection()
    query = 'SELECT * FROM airbnb_bd."property" WHERE price BETWEEN %s AND %s ORDER BY price ASC'
    cur.execute(query, (min_price, max_price))
    return cur.fetchall()

def add_new_booking(booking_id, total_price, timestamp, check_in_date, check_out_date, guest_user_id, property_id):
    db, cur = get_connection()
    query = '''INSERT INTO airbnb_bd."booking" (booking_id, total_price, timestamp, check_in_date, check_out_date, guest_user_id, property_id) 
               VALUES (%s, %s, %s, %s, %s, %s, %s)'''
    cur.execute(query, (booking_id, total_price, timestamp, check_in_date, check_out_date, guest_user_id, property_id))
    db.commit()

def add_new_review(review_id, booking_id, comment, rating):
    db, cur = get_connection()
    query = '''INSERT INTO airbnb_bd."review" (review_id, booking_id, comment, rating) 
               VALUES (%s, %s, %s, %s)'''
    cur.execute(query, (review_id, booking_id, comment, rating))
    db.commit()

def get_all_hosts():
    db, cur = get_connection()
    query = 'SELECT * FROM airbnb_bd."host"'
    cur.execute(query)
    return cur.fetchall()

def get_all_guests():
    db, cur = get_connection()
    query = 'SELECT * FROM airbnb_bd."guest"'
    cur.execute(query)
    return cur.fetchall()

def get_all_bookings():
    db, cur = get_connection()
    query = 'SELECT * FROM airbnb_bd."booking"'
    cur.execute(query)
    return cur.fetchall()

if __name__ == '__main__':
    app.run(debug=True)
