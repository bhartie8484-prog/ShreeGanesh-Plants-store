from flask import Flask, render_template, request, redirect, url_for, session, flash, abort, g
import pymysql
import sqlite3
try:
    import psycopg
except ImportError:  # Local MySQL-only development can run without psycopg.
    psycopg = None
import os
import uuid
from datetime import datetime
from urllib.parse import urlparse, unquote, parse_qs
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from werkzeug.middleware.proxy_fix import ProxyFix
from catalog import CATEGORIES, db_products

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'development-only-change-me')
if os.environ.get('RENDER'):
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)
    app.config.update(
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax',
    )

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'plant_store'
app.config['MYSQL_PORT'] = 3306

# Machine-specific credentials live in an ignored local config file.
app.config.from_pyfile('config/local.py', silent=True)

# Production credentials are supplied by the hosting provider. DATABASE_URL
# takes priority, while individual MYSQL_* variables remain supported.
database_url = os.environ.get('DATABASE_URL')
parsed_candidate = urlparse(database_url) if database_url else None
if parsed_candidate and parsed_candidate.hostname in {'mysql_host', 'actual-hostname.provider.com'}:
    database_url = None

app.config['USE_SQLITE'] = bool(
    os.environ.get('DATABASE_BACKEND', '').lower() == 'sqlite'
    or (os.environ.get('RENDER') and not database_url)
)
app.config['SQLITE_PATH'] = os.environ.get(
    'SQLITE_PATH', '/tmp/plant_store.db' if os.environ.get('RENDER') else 'plant_store.db'
)
if database_url:
    parsed_db_url = urlparse(database_url)
    if parsed_db_url.scheme in ('postgres', 'postgresql'):
        app.config['USE_POSTGRES'] = True
        app.config['DATABASE_URL'] = database_url
    elif parsed_db_url.scheme in ('mysql', 'mysql+pymysql'):
        app.config['USE_POSTGRES'] = False
        app.config.update(
            MYSQL_HOST=parsed_db_url.hostname,
            MYSQL_PORT=parsed_db_url.port or 3306,
            MYSQL_USER=unquote(parsed_db_url.username or ''),
            MYSQL_PASSWORD=unquote(parsed_db_url.password or ''),
            MYSQL_DB=parsed_db_url.path.lstrip('/'),
        )
        database_query = parse_qs(parsed_db_url.query)
        app.config['MYSQL_SSL'] = (
            database_query.get('ssl-mode', [''])[0].lower() in ('required', 'verify_ca', 'verify_identity')
            or database_query.get('ssl', [''])[0].lower() in ('1', 'true', 'required')
        )
    else:
        raise RuntimeError('DATABASE_URL must use postgres://, postgresql://, mysql://, or mysql+pymysql://')
else:
    app.config['USE_POSTGRES'] = False
    app.config.update(
        MYSQL_HOST=os.environ.get('MYSQL_HOST', app.config['MYSQL_HOST']),
        MYSQL_PORT=int(os.environ.get('MYSQL_PORT', app.config['MYSQL_PORT'])),
        MYSQL_USER=os.environ.get('MYSQL_USER', app.config['MYSQL_USER']),
        MYSQL_PASSWORD=os.environ.get('MYSQL_PASSWORD', app.config['MYSQL_PASSWORD']),
        MYSQL_DB=os.environ.get('MYSQL_DB', app.config['MYSQL_DB']),
    )
    app.config['MYSQL_SSL'] = os.environ.get('MYSQL_SSL', '').lower() in ('1', 'true', 'required')

# Upload Configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class SQLiteCursorAdapter:
    def __init__(self, cursor):
        self.cursor = cursor

    def execute(self, query, params=()):
        query = query.replace('ORDER BY RAND()', 'ORDER BY RANDOM()').replace('%s', '?')
        query = query.replace(
            'ON DUPLICATE KEY UPDATE quantity = quantity + 1',
            'ON CONFLICT(user_id, product_id) DO UPDATE SET quantity = quantity + 1'
        )
        return self.cursor.execute(query, params)

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()

    @property
    def lastrowid(self):
        return self.cursor.lastrowid

    def close(self):
        self.cursor.close()

class SQLiteConnectionAdapter:
    def __init__(self, path):
        self.connection = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread=False)
        self.connection.execute('PRAGMA foreign_keys = ON')

    def cursor(self):
        return SQLiteCursorAdapter(self.connection.cursor())

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def close(self):
        self.connection.close()

class PostgresCursorAdapter:
    def __init__(self, cursor):
        self.cursor = cursor
        self._lastrowid = None

    def execute(self, query, params=()):
        query = query.replace('ORDER BY RAND()', 'ORDER BY RANDOM()')
        query = query.replace('`key`', '"key"').replace('`value`', '"value"')
        query = query.replace(
            'ON DUPLICATE KEY UPDATE quantity = quantity + 1',
            'ON CONFLICT(user_id, product_id) DO UPDATE SET quantity = cart.quantity + 1'
        )
        query = query.replace(
            'REPLACE INTO app_meta ("key", "value") VALUES (\'catalog_version\', \'7\')',
            'INSERT INTO app_meta ("key", "value") VALUES (\'catalog_version\', \'7\') '
            'ON CONFLICT ("key") DO UPDATE SET "value" = EXCLUDED."value"'
        )
        if query.lstrip().upper().startswith('INSERT INTO ORDERS ') and ' RETURNING ' not in query.upper():
            query = f"{query} RETURNING id"
            self.cursor.execute(query, params)
            self._lastrowid = self.cursor.fetchone()[0]
            return None
        self._lastrowid = None
        return self.cursor.execute(query, params)

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()

    @property
    def lastrowid(self):
        return self._lastrowid

    def close(self):
        self.cursor.close()

class PostgresConnectionAdapter:
    def __init__(self, url):
        if psycopg is None:
            raise RuntimeError('psycopg is required for PostgreSQL DATABASE_URL')
        self.connection = psycopg.connect(url)

    def cursor(self):
        return PostgresCursorAdapter(self.connection.cursor())

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def close(self):
        self.connection.close()

def duplicate_record_errors():
    errors = [pymysql.err.IntegrityError, sqlite3.IntegrityError]
    if psycopg is not None:
        errors.append(psycopg.errors.UniqueViolation)
    return tuple(errors)

def database_errors():
    errors = [pymysql.MySQLError, sqlite3.Error]
    if psycopg is not None:
        errors.append(psycopg.Error)
    return tuple(errors)

def get_db():
    if 'db' not in g:
        if app.config['USE_SQLITE']:
            g.db = SQLiteConnectionAdapter(app.config['SQLITE_PATH'])
            return g.db
        if app.config.get('USE_POSTGRES'):
            g.db = PostgresConnectionAdapter(app.config['DATABASE_URL'])
            return g.db
        connection_options = dict(
            host=app.config['MYSQL_HOST'],
            port=app.config['MYSQL_PORT'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            database=app.config['MYSQL_DB'],
            charset='utf8mb4',
            autocommit=False,
            connect_timeout=10,
        )
        if app.config.get('MYSQL_SSL'):
            connection_options['ssl'] = {'check_hostname': True}
        g.db = pymysql.connect(**connection_options)
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
    if not version or version[0] != '7':
        # Add newly curated products without deleting products referenced by orders.
        if version and version[0] == '4':
            indoor_renames = {
                'Monstera Deliciosa': 'Aloe Vera Plant',
                'Golden Pothos': 'Golden Money Plant',
                'Rubber Plant Indoor': 'Rubber Plant',
                'Areca Palm': 'Money Plant',
            }
            for old_name, new_name in indoor_renames.items():
                cursor.execute(
                    "UPDATE products SET name = %s WHERE name = %s AND category = 'Indoor'",
                    (new_name, old_name)
                )
        if version and version[0] == '5':
            outdoor_renames = {
                'Bougainvillea Outdoor': 'Caladium Plant',
                'Neem Tree': 'Coral Bells Plant',
                'Hibiscus Outdoor': 'Curry Leaf Plant',
                'Jasmine Outdoor': 'Fern Plant',
                'Rose Outdoor': 'Hosta Plant',
                'Aloe Vera Outdoor': 'Lungwort Plant',
                'Cactus Plant': 'Mint Plant',
                'Jade Plant': 'Neem Plant',
            }
            for old_name, new_name in outdoor_renames.items():
                cursor.execute(
                    "UPDATE products SET name = %s WHERE name = %s AND category = 'Outdoor'",
                    (new_name, old_name)
                )
        if version and version[0] == '6':
            tool_renames = {
                'Gardening Pruner': 'Pruner',
                'Garden Spade': 'Spade',
                'Gardening Axe': 'Axe',
                'Gardening Hoe': 'Hoe',
                'Garden Rake': 'Rake',
                'Gardening Watering Can': 'Watering Can',
                'Gardening Scissor': 'Scissor',
                'Gardening Gloves': 'Gloves',
            }
            for old_name, new_name in tool_renames.items():
                cursor.execute(
                    "UPDATE products SET name = %s WHERE name = %s AND category = 'Gardening Tools'",
                    (new_name, old_name)
                )
        for product in db_products():
            cursor.execute(
                "SELECT id FROM products WHERE name = %s AND category = %s LIMIT 1",
                (product[0], product[5])
            )
            existing = cursor.fetchone()
            if existing:
                cursor.execute(
                    "UPDATE products SET description=%s, price=%s, stock=%s, image=%s WHERE id=%s",
                    (product[1], product[2], product[3], product[4], existing[0])
                )
            else:
                cursor.execute(
                    "INSERT INTO products (name, description, price, stock, image, category) VALUES (%s, %s, %s, %s, %s, %s)",
                    product
                )
        cursor.execute("REPLACE INTO app_meta (`key`, `value`) VALUES ('catalog_version', '7')")
        db.commit()
    cursor.close()
    catalog_ready = True

def ensure_store_schema():
    global store_schema_ready
    if store_schema_ready:
        return
    db = get_db()
    if app.config.get('USE_POSTGRES'):
        cursor = db.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                description TEXT,
                price NUMERIC(10,2) NOT NULL,
                stock INTEGER DEFAULT 0,
                image VARCHAR(255),
                category VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cart (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
                quantity INTEGER DEFAULT 1,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, product_id)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                total_amount NUMERIC(10,2) NOT NULL,
                status VARCHAR(50) DEFAULT 'pending',
                order_number VARCHAR(32) UNIQUE,
                payment_method VARCHAR(30),
                payment_status VARCHAR(30) DEFAULT 'pending',
                shipping_name VARCHAR(100),
                shipping_phone VARCHAR(20),
                shipping_address TEXT,
                shipping_city VARCHAR(80),
                shipping_state VARCHAR(80),
                shipping_pincode VARCHAR(10),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS order_items (
                id SERIAL PRIMARY KEY,
                order_id INTEGER NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
                product_id INTEGER REFERENCES products(id),
                quantity INTEGER NOT NULL,
                price NUMERIC(10,2) NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL,
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS payments (
                id SERIAL PRIMARY KEY,
                order_id INTEGER NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
                transaction_id VARCHAR(50) UNIQUE NOT NULL,
                method VARCHAR(30) NOT NULL,
                amount NUMERIC(10,2) NOT NULL,
                status VARCHAR(30) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        db.commit()
        cursor.close()
        store_schema_ready = True
        return
    if app.config['USE_SQLITE']:
        db.connection.executescript("""
            CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT UNIQUE NOT NULL, password TEXT NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
            CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, description TEXT, price REAL NOT NULL, stock INTEGER DEFAULT 0, image TEXT, category TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
            CREATE TABLE IF NOT EXISTS cart (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, product_id INTEGER NOT NULL, quantity INTEGER DEFAULT 1, added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, UNIQUE(user_id, product_id), FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE, FOREIGN KEY(product_id) REFERENCES products(id) ON DELETE CASCADE);
            CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, total_amount REAL NOT NULL, status TEXT DEFAULT 'pending', created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, order_number TEXT UNIQUE, payment_method TEXT, payment_status TEXT DEFAULT 'pending', shipping_name TEXT, shipping_phone TEXT, shipping_address TEXT, shipping_city TEXT, shipping_state TEXT, shipping_pincode TEXT, FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE);
            CREATE TABLE IF NOT EXISTS payments (id INTEGER PRIMARY KEY AUTOINCREMENT, order_id INTEGER NOT NULL, transaction_id TEXT UNIQUE NOT NULL, method TEXT NOT NULL, amount REAL NOT NULL, status TEXT NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY(order_id) REFERENCES orders(id) ON DELETE CASCADE);
            CREATE TABLE IF NOT EXISTS order_items (id INTEGER PRIMARY KEY AUTOINCREMENT, order_id INTEGER NOT NULL, product_id INTEGER NOT NULL, quantity INTEGER NOT NULL, price REAL NOT NULL, FOREIGN KEY(order_id) REFERENCES orders(id) ON DELETE CASCADE, FOREIGN KEY(product_id) REFERENCES products(id));
            CREATE TABLE IF NOT EXISTS contacts (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT NOT NULL, message TEXT NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
        """)
        db.commit()
        store_schema_ready = True
        return
    cursor = db.cursor()
    # A fresh production database is initialized automatically. All statements
    # are idempotent, so they are also safe for existing installations.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            description TEXT,
            price DECIMAL(10,2) NOT NULL,
            stock INT DEFAULT 0,
            image VARCHAR(255),
            category VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cart (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            product_id INT NOT NULL,
            quantity INT DEFAULT 1,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE KEY unique_user_product (user_id, product_id),
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            total_amount DECIMAL(10,2) NOT NULL,
            status VARCHAR(50) DEFAULT 'pending',
            order_number VARCHAR(32) UNIQUE,
            payment_method VARCHAR(30),
            payment_status VARCHAR(30) DEFAULT 'pending',
            shipping_name VARCHAR(100),
            shipping_phone VARCHAR(20),
            shipping_address TEXT,
            shipping_city VARCHAR(80),
            shipping_state VARCHAR(80),
            shipping_pincode VARCHAR(10),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            id INT AUTO_INCREMENT PRIMARY KEY,
            order_id INT NOT NULL,
            product_id INT NOT NULL,
            quantity INT NOT NULL,
            price DECIMAL(10,2) NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
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
    # Static assets and the platform health check must remain available even
    # when the database is temporarily unavailable.
    if request.endpoint in ('static', 'health', 'favicon'):
        return
    ensure_store_schema()
    ensure_catalog()

@app.route('/health')
def health():
    try:
        cursor = get_db().cursor()
        cursor.execute('SELECT 1')
        cursor.close()
        return {'status': 'ok', 'database': 'connected'}, 200
    except database_errors():
        app.logger.exception('Database health check failed')
        return {'status': 'error', 'database': 'unavailable'}, 503

@app.route('/favicon.ico')
def favicon():
    return '', 204

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
    
    if category == 'Flowering':
        cursor.execute(
            """SELECT * FROM products
               WHERE stock > 0 AND category = %s
               AND name NOT IN (%s, %s, %s)""",
            (category, 'Bougainvillea', 'Chrysanthemum', 'Dahlia Plant')
        )
    elif category:
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
        except duplicate_record_errors():
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
