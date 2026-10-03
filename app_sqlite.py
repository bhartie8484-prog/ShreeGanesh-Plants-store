from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from catalog import CATEGORIES, db_products

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# SQLite Configuration
DATABASE = 'plant_store.db'

# Upload Configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            stock INTEGER DEFAULT 0,
            image TEXT,
            category TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cart (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER DEFAULT 1,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
            UNIQUE(user_id, product_id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Check if products exist
    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0:
        # Insert sample products
        products = [
            # Indoor Plants
            ('Monstera Deliciosa', 'Beautiful Swiss Cheese Plant with large fenestrated leaves', 1299.00, 15, 'monstera.jpg', 'Indoor'),
            ('Snake Plant', 'Low maintenance air purifying plant perfect for beginners', 499.00, 25, 'snake-plant.jpg', 'Indoor'),
            ('Fiddle Leaf Fig', 'Trendy plant with large violin-shaped leaves', 1899.00, 10, 'fiddle-leaf.jpg', 'Indoor'),
            ('Peace Lily', 'Elegant flowering plant that thrives in low light', 699.00, 20, 'peace-lily.jpg', 'Indoor'),
            ('Golden Pothos', 'Easy-care trailing plant with heart-shaped leaves', 399.00, 30, 'golden-pothos-1.jpg', 'Indoor'),
            ('Rubber Plant', 'Glossy-leaved plant that purifies indoor air', 899.00, 12, 'rubber-plant.jpg', 'Indoor'),
            ('ZZ Plant', 'Extremely hardy plant with shiny waxy leaves', 799.00, 22, 'zz-plant.jpg', 'Indoor'),
            ('Aloe Vera', 'Medicinal succulent plant with healing properties', 349.00, 18, 'aloe-vera.jpg', 'Indoor'),
            
            # Outdoor Plants
            ('Neem Plant', 'Medicinal outdoor plant with air purifying qualities', 599.00, 15, 'neem-plant.jpg', 'Outdoor'),
            ('Curry Leaf Plant', 'Aromatic herb plant perfect for Indian cooking', 299.00, 25, 'curry-leaf.jpg', 'Outdoor'),
            ('Tulsi Plant', 'Holy Basil plant with medicinal and spiritual significance', 199.00, 30, 'tulsi-plant.jpg', 'Outdoor'),
            ('Mint Plant', 'Fresh aromatic herb perfect for drinks and cooking', 149.00, 28, 'mint-plant.jpg', 'Outdoor'),
            ('Bougainvillea', 'Vibrant colorful climber for outdoor gardens', 899.00, 12, 'bougainvillea-1.jpg', 'Outdoor'),
            
            # Flowering Plants
            ('Rose Plant', 'Classic beautiful flowering plant with fragrant blooms', 499.00, 20, 'rose-plant.jpg', 'Flowering'),
            ('Hibiscus Flower Plant', 'Tropical flowering plant with large colorful blooms', 399.00, 18, 'hibiscus-flower.jpg', 'Flowering'),
            ('Jasmine Flower Plant', 'Fragrant white flowers perfect for gardens', 349.00, 22, 'jasmine-flower.jpg', 'Flowering'),
            ('Periwinkle Plant', 'Continuous blooming small flowering plant', 249.00, 25, 'periwinkle-plant.jpg', 'Flowering'),
            ('Marigold Plant', 'Bright orange and yellow flowering plant', 199.00, 30, 'marigold-plant.jpg', 'Flowering'),
        ]
        
        cursor.executemany(
            "INSERT INTO products (name, description, price, stock, image, category) VALUES (?, ?, ?, ?, ?, ?)",
            products
        )
    
    cursor.execute('CREATE TABLE IF NOT EXISTS app_meta (key TEXT PRIMARY KEY, value TEXT NOT NULL)')
    version = cursor.execute("SELECT value FROM app_meta WHERE key = 'catalog_version'").fetchone()
    if not version or version[0] != '3':
        cursor.execute("DELETE FROM products")
        cursor.executemany(
            "INSERT INTO products (name, description, price, stock, image, category) VALUES (?, ?, ?, ?, ?, ?)",
            db_products()
        )
        cursor.execute(
            "INSERT OR REPLACE INTO app_meta (key, value) VALUES ('catalog_version', '3')"
        )

    conn.commit()
    conn.close()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE stock > 0 ORDER BY RANDOM()")
    all_products = cursor.fetchall()
    products = []
    used_ids = set()
    for category in CATEGORIES:
        match = next((item for item in all_products if item['category'] == category), None)
        if match:
            products.append(match)
            used_ids.add(match['id'])
    products.extend(item for item in all_products if item['id'] not in used_ids)
    products = products[:12]
    conn.close()
    return render_template('index.html', products=products)

@app.route('/products')
def products():
    category = request.args.get('category', None)
    conn = get_db()
    cursor = conn.cursor()
    
    if category:
        cursor.execute("SELECT * FROM products WHERE stock > 0 AND category = ?", (category,))
    else:
        cursor.execute("SELECT * FROM products WHERE stock > 0")
    
    all_products = cursor.fetchall()
    
    conn.close()
    
    return render_template('products.html', products=all_products, categories=CATEGORIES, selected_category=category)

@app.route('/product/<int:id>')
def product_detail(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE id = ?", (id,))
    product = cursor.fetchone()
    conn.close()
    return render_template('product_detail.html', product=product)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        
        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", 
                          (name, email, password))
            conn.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Email already registered!', 'error')
        finally:
            conn.close()
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['user_name'] = user['name']
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
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.id, p.name, p.price, c.quantity, p.image 
        FROM cart c 
        JOIN products p ON c.product_id = p.id 
        WHERE c.user_id = ?
    """, (session['user_id'],))
    cart_items = cursor.fetchall()
    conn.close()
    
    total = sum(item['price'] * item['quantity'] for item in cart_items)
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

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE cart SET quantity = ? WHERE id = ? AND user_id = ?",
        (quantity, cart_id, session['user_id'])
    )
    conn.commit()
    conn.close()
    flash('Cart updated.', 'success')
    return redirect(url_for('cart'))

@app.route('/cart/remove/<int:cart_id>', methods=['POST'])
def remove_from_cart(cart_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM cart WHERE id = ? AND user_id = ?",
        (cart_id, session['user_id'])
    )
    conn.commit()
    conn.close()
    flash('Item removed from your cart.', 'success')
    return redirect(url_for('cart'))

@app.route('/add_to_cart/<int:product_id>', methods=['GET', 'POST'])
def add_to_cart(product_id):
    if 'user_id' not in session:
        flash('Please login to add items to cart.', 'error')
        return redirect(url_for('login'))
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Check if item already in cart
    cursor.execute("SELECT * FROM cart WHERE user_id = ? AND product_id = ?", 
                   (session['user_id'], product_id))
    existing = cursor.fetchone()
    
    if existing:
        cursor.execute("UPDATE cart SET quantity = quantity + 1 WHERE user_id = ? AND product_id = ?",
                      (session['user_id'], product_id))
    else:
        cursor.execute("INSERT INTO cart (user_id, product_id, quantity) VALUES (?, ?, 1)", 
                      (session['user_id'], product_id))
    
    conn.commit()
    conn.close()
    
    flash('Product added to cart! 🛒', 'success')
    return redirect(url_for('cart'))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)", 
                      (name, email, message))
        conn.commit()
        conn.close()
        
        flash('Message sent successfully!', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html')

if __name__ == '__main__':
    init_db()
    print("\n🌱 Plant Store Server Starting...")
    print("📍 Visit: http://localhost:5000")
    print("✨ Categories available: Indoor, Outdoor, Flowering")
    print("\n")
    app.run(debug=True)
