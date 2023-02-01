from flask import render_template, redirect, request, session

from flask_app import app

from flask_app.models.cookie_order import Customer


@app.route('/')
def index():
    return redirect('/cookies')

@app.route('/cookies')
def cookies_home():
    all_orders = Customer.get_all()
    print(all_orders)
    return render_template('cookie_orders.html', orders = all_orders)

@app.route('/cookies/new')
def add_new_order():
    return render_template('new_order.html')

@app.route('/cookies/add', methods=['POST'])
def adding_new():
    if not Customer.validate_user(request.form):
        return redirect('/cookies/new')
    data = {
        'name' : request.form['name'],
        'cookie_type' : request.form['cookie_type'],
        'num_of_boxes' : request.form['num_of_boxes']
    }
    Customer.save(data)
    return redirect('/cookies')

@app.route('/cookies/edit/<int:cookie_id>')
def edit(cookie_id):
    return render_template("edit_order.html", order_update = Customer.select_user(cookie_id))

@app.route('/cookies/update/<int:cookie_id>', methods=['POST'])
def update(cookie_id):
    if not Customer.validate_user(request.form):
        return redirect(f'/cookies/edit/{cookie_id}')
    Customer.update(request.form)
    return redirect('/')

@app.route('/cookies/remove/<int:id>')
def remove(id):
    data = {"id": id}
    Customer.remove(data)
    return redirect('/')