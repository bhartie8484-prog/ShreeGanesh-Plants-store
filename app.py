from flask import Flask, render_template, request, redirect, url_for, session, flash, abort, g
import pymysql
import os
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from catalog import CATEGORIES, db_products

app = Flask(__name__)
app.secret_key = 'development-only-change-me'

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'plant_store'

# Machine-specific credentials live in an ignored local config file.
app.config.from_pyfile('config/local.py', silent=True)

# Upload Configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            database=app.config['MYSQL_DB'],
            charset='utf8mb4',
            autocommit=False,
        )
    return g.db

@app.teardown_appcontext
def close_db(error=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

catalog_ready = False
store_schema_ready = False

def ensure_catalog():
    """Install the curated catalogue once for existing MySQL databases."""
    global catalog_ready
    if catalog_ready:
        return
    db = get_db()
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS app_meta (`key` VARCHAR(50) PRIMARY KEY, `value` VARCHAR(50) NOT NULL)")
    cursor.execute("SELECT value FROM app_meta WHERE `key` = 'catalog_version'")
    version = cursor.fetchone()
    if not version or version[0] != '3':
        cursor.execute("DELETE FROM products")
        cursor.executemany(
            "INSERT INTO products (name, description, price, stock, image, category) VALUES (%s, %s, %s, %s, %s, %s)",
            db_products()
        )
        cursor.execute("REPLACE INTO app_meta (`key`, `value`) VALUES ('catalog_version', '3')")
        db.commit()
    cursor.close()
    catalog_ready = True

def ensure_store_schema():
    global store_schema_ready
    if store_schema_ready:
        return
    db = get_db()
    cursor = db.cursor()
    additions = [
        "ADD COLUMN order_number VARCHAR(32) UNIQUE",
        "ADD COLUMN payment_method VARCHAR(30)",
        "ADD COLUMN payment_status VARCHAR(30) DEFAULT 'pending'",
        "ADD COLUMN shipping_name VARCHAR(100)",
        "ADD COLUMN shipping_phone VARCHAR(20)",
        "ADD COLUMN shipping_address TEXT",
        "ADD COLUMN shipping_city VARCHAR(80)",
        "ADD COLUMN shipping_state VARCHAR(80)",
        "ADD COLUMN shipping_pincode VARCHAR(10)",
    ]
    for addition in additions:
        try:
            cursor.execute(f"ALTER TABLE orders {addition}")
        except pymysql.err.OperationalError as exc:
            if exc.args[0] != 1060:
                raise
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            id INT AUTO_INCREMENT PRIMARY KEY,
            order_id INT NOT NULL,
            transaction_id VARCHAR(50) UNIQUE NOT NULL,
            method VARCHAR(30) NOT NULL,
            amount DECIMAL(10,2) NOT NULL,
            status VARCHAR(30) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
        )
    """)
    db.commit()
    cursor.close()
    store_schema_ready = True

@app.before_request
def prepare_catalog():
    ensure_catalog()
    ensure_store_schema()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM products WHERE stock > 0 ORDER BY RAND()")
    all_products = cursor.fetchall()
    products = []
    used_ids = set()
    for category in CATEGORIES:
        match = next((item for item in all_products if item[6] == category), None)
        if match:
            products.append(match)
            used_ids.add(match[0])
    products.extend(item for item in all_products if item[0] not in used_ids)
    products = products[:12]
    cursor.close()
    return render_template('index.html', products=products)

@app.route('/products')
def products():
    category = request.args.get('category', None)
    cursor = get_db().cursor()
    
    if category:
        cursor.execute("SELECT * FROM products WHERE stock > 0 AND category = %s", (category,))
    else:
        cursor.execute("SELECT * FROM products WHERE stock > 0")
    
    all_products = cursor.fetchall()
    
    cursor.close()
    
    return render_template('products.html', products=all_products, categories=CATEGORIES, selected_category=category)

@app.route('/product/<int:id>')
def product_detail(id):
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM products WHERE id = %s", (id,))
    product = cursor.fetchone()
    cursor.close()
    if not product:
        abort(404)
    return render_template('product_detail.html', product=product)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                           (name, email, password))
        except pymysql.err.IntegrityError:
            db.rollback()
            cursor.close()
            flash('An account with this email already exists.', 'error')
            return render_template('register.html')
        db.commit()
        cursor.close()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        cursor = get_db().cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        
        if user and check_password_hash(user[3], password):
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials!', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/cart')
def cart():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    cursor = get_db().cursor()
    cursor.execute("""
        SELECT c.id, p.name, p.price, c.quantity, p.image 
        FROM cart c 
        JOIN products p ON c.product_id = p.id 
        WHERE c.user_id = %s
    """, (session['user_id'],))
    cart_items = cursor.fetchall()
    cursor.close()
    
    total = sum(item[2] * item[3] for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/cart/update/<int:cart_id>', methods=['POST'])
def update_cart(cart_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    try:
        quantity = int(request.form.get('quantity', ''))
    except ValueError:
        flash('Please enter a valid quantity.', 'error')
        return redirect(url_for('cart'))

    if quantity < 1:
        flash('Quantity must be at least 1.', 'error')
        return redirect(url_for('cart'))

    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "UPDATE cart SET quantity = %s WHERE id = %s AND user_id = %s",
        (quantity, cart_id, session['user_id'])
    )
    db.commit()
    cursor.close()
    flash('Cart updated.', 'success')
    return redirect(url_for('cart'))

@app.route('/cart/remove/<int:cart_id>', methods=['POST'])
def remove_from_cart(cart_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "DELETE FROM cart WHERE id = %s AND user_id = %s",
        (cart_id, session['user_id'])
    )
    db.commit()
    cursor.close()
    flash('Item removed from your cart.', 'success')
    return redirect(url_for('cart'))

@app.route('/add_to_cart/<int:product_id>', methods=['GET', 'POST'])
def add_to_cart(product_id):
    if 'user_id' not in session:
        flash('Please login to add items to cart.', 'error')
        return redirect(url_for('login'))
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO cart (user_id, product_id, quantity) 
        VALUES (%s, %s, 1)
        ON DUPLICATE KEY UPDATE quantity = quantity + 1
    """, (session['user_id'], product_id))
    db.commit()
    cursor.close()
    
    flash('Product added to cart! 🛒', 'success')
    return redirect(url_for('cart'))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        
        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s)", 
                      (name, email, message))
        db.commit()
        cursor.close()
        
        flash('Message sent successfully!', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html')

def cart_rows(user_id):
    cursor = get_db().cursor()
    cursor.execute("""
        SELECT c.id, p.id, p.name, p.price, c.quantity, p.image, p.stock
        FROM cart c JOIN products p ON c.product_id = p.id
        WHERE c.user_id = %s
    """, (user_id,))
    rows = cursor.fetchall()
    cursor.close()
    return rows

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if 'user_id' not in session:
        flash('Please login to checkout.', 'error')
        return redirect(url_for('login'))
    items = cart_rows(session['user_id'])
    if not items:
        flash('Your cart is empty.', 'error')
        return redirect(url_for('cart'))
    subtotal = sum(item[3] * item[4] for item in items)
    shipping = 0 if subtotal > 999 else 50
    if request.method == 'POST':
        required = ['name', 'phone', 'address', 'city', 'state', 'pincode', 'payment_method']
        if any(not request.form.get(field, '').strip() for field in required):
            flash('Please complete all checkout fields.', 'error')
            return render_template('checkout.html', items=items, subtotal=subtotal, shipping=shipping)
        if not request.form['pincode'].isdigit() or len(request.form['pincode']) != 6:
            flash('Please enter a valid 6-digit PIN code.', 'error')
            return render_template('checkout.html', items=items, subtotal=subtotal, shipping=shipping)
        session['checkout'] = {field: request.form[field].strip() for field in required}
        return redirect(url_for('payment'))
    return render_template('checkout.html', items=items, subtotal=subtotal, shipping=shipping)

@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if 'user_id' not in session or 'checkout' not in session:
        return redirect(url_for('checkout'))
    items = cart_rows(session['user_id'])
    if not items:
        return redirect(url_for('cart'))
    subtotal = sum(item[3] * item[4] for item in items)
    total = subtotal + (0 if subtotal > 999 else 50)
    checkout_data = session['checkout']
    if request.method == 'POST':
        if request.form.get('demo_result') == 'failed':
            flash('Demo payment declined. No money was charged.', 'error')
            return render_template('payment.html', total=total, method=checkout_data['payment_method'])
        for item in items:
            if item[4] > item[6]:
                flash(f'Only {item[6]} units of {item[2]} are available.', 'error')
                return redirect(url_for('cart'))
        db = get_db()
        cursor = db.cursor()
        order_number = 'PS' + datetime.now().strftime('%y%m%d') + uuid.uuid4().hex[:6].upper()
        method = checkout_data['payment_method']
        payment_status = 'pending' if method == 'cod' else 'paid'
        cursor.execute("""
            INSERT INTO orders (user_id, total_amount, status, order_number, payment_method,
                payment_status, shipping_name, shipping_phone, shipping_address,
                shipping_city, shipping_state, shipping_pincode)
            VALUES (%s,%s,'confirmed',%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (session['user_id'], total, order_number, method, payment_status,
              checkout_data['name'], checkout_data['phone'], checkout_data['address'],
              checkout_data['city'], checkout_data['state'], checkout_data['pincode']))
        order_id = cursor.lastrowid
        for item in items:
            cursor.execute("INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (%s,%s,%s,%s)",
                           (order_id, item[1], item[4], item[3]))
            cursor.execute("UPDATE products SET stock = stock - %s WHERE id = %s", (item[4], item[1]))
        transaction_id = 'TXN' + uuid.uuid4().hex[:12].upper()
        cursor.execute("INSERT INTO payments (order_id, transaction_id, method, amount, status) VALUES (%s,%s,%s,%s,%s)",
                       (order_id, transaction_id, method, total, payment_status))
        cursor.execute("DELETE FROM cart WHERE user_id = %s", (session['user_id'],))
        db.commit()
        cursor.close()
        session.pop('checkout', None)
        return redirect(url_for('order_success', order_number=order_number))
    return render_template('payment.html', total=total, method=checkout_data['payment_method'])

@app.route('/order-success/<order_number>')
def order_success(order_number):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM orders WHERE order_number=%s AND user_id=%s", (order_number, session['user_id']))
    order = cursor.fetchone()
    cursor.close()
    if not order:
        abort(404)
    return render_template('order_success.html', order=order)

@app.route('/orders')
def orders():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM orders WHERE user_id=%s ORDER BY created_at DESC", (session['user_id'],))
    rows = cursor.fetchall()
    cursor.close()
    return render_template('orders.html', orders=rows)

@app.route('/track-order', methods=['GET', 'POST'])
def track_order():
    order = None
    if request.method == 'POST':
        number = request.form.get('order_number', '').strip().upper()
        cursor = get_db().cursor()
        cursor.execute("SELECT order_number, status, payment_status, created_at, shipping_city FROM orders WHERE order_number=%s", (number,))
        order = cursor.fetchone()
        cursor.close()
        if not order:
            flash('Order number not found.', 'error')
    return render_template('track_order.html', order=order)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

POLICY_PAGES = {
    'shipping-policy': ('Shipping Policy', 'We dispatch healthy plants within 2–4 business days. Delivery usually takes 3–7 business days after dispatch. Live-plant orders may be held during extreme weather for plant safety.'),
    'return-policy': ('Returns & Refunds', 'Report damaged or incorrect items within 24 hours of delivery with clear photos and an unboxing video. Approved refunds are processed to the original payment method within 5–7 business days.'),
    'privacy-policy': ('Privacy Policy', 'We collect only the information needed to process orders, provide support, and improve your experience. We do not sell personal information. Demo payment details are never stored.'),
    'terms': ('Terms & Conditions', 'By using PlantStore, you agree to provide accurate order information and use the service lawfully. Product appearance may vary naturally. This demonstration store does not process real payments.'),
}

@app.route('/policy/<slug>')
def policy(slug):
    page = POLICY_PAGES.get(slug)
    if not page:
        abort(404)
    return render_template('policy.html', title=page[0], content=page[1])

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', code=404, title='Page not found', message='The page you requested does not exist.'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('error.html', code=500, title='Something went wrong', message='Please try again in a moment.'), 500

if __name__ == '__main__':
    app.run(debug=False)
