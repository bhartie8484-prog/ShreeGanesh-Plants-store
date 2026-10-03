from flask import Flask, render_template, session, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'test_key_for_simple_app'

# Sample products WITH LOCAL IMAGES (from static/uploads folder)
# Download your specific images and save them in static/uploads/
SAMPLE_PRODUCTS = [
    (1, 'Monstera Deliciosa', 'Beautiful Swiss Cheese Plant with large fenestrated leaves', 1299.00, 15, 'monstera.jpg', 'Indoor'),
    (2, 'Snake Plant', 'Low maintenance air purifying plant perfect for beginners - Blue pot', 499.00, 25, 'snake-plant.jpg', 'Indoor'),
    (3, 'Fiddle Leaf Fig', 'Trendy plant with large violin-shaped leaves - White pot', 1899.00, 10, 'fiddle-leaf.jpg', 'Indoor'),
    (4, 'Peace Lily', 'Elegant flowering plant that thrives in low light', 699.00, 20, 'peace-lily.jpg', 'Indoor'),
    (5, 'Pothos Golden', 'Easy-care trailing plant with heart-shaped leaves', 399.00, 30, 'pothos.jpg', 'Indoor'),
    (6, 'Aloe Vera', 'Medicinal succulent plant with healing properties', 349.00, 18, 'aloe-vera.jpg', 'Succulent'),
    (7, 'Rubber Plant', 'Glossy-leaved plant that purifies indoor air', 899.00, 12, 'rubber-plant.jpg', 'Indoor'),
    (8, 'ZZ Plant', 'Extremely hardy plant with shiny waxy leaves', 799.00, 4, 'zz-plant.jpg', 'Indoor'),
]

@app.route('/')
def index():
    return render_template('index.html', products=SAMPLE_PRODUCTS)

@app.route('/products')
def products():
    return render_template('products.html', products=SAMPLE_PRODUCTS)

@app.route('/product/<int:id>')
def product_detail(id):
    product = next((p for p in SAMPLE_PRODUCTS if p[0] == id), None)
    if product:
        return render_template('product_detail.html', product=product)
    return redirect(url_for('products'))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template('contact.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/cart')
def cart():
    return render_template('cart.html', cart_items=[], total=0)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    flash('Product added to cart! (Demo mode - no actual cart)', 'success')
    return redirect(url_for('products'))

if __name__ == '__main__':
    print('\n' + '='*60)
    print('🌿 PlantStore with LOCAL Images')
    print('='*60)
    print('✅ Using images from static/uploads/ folder')
    print('✅ No database required - demo mode')
    print('\n📌 Download your images first:')
    print('   1. Snake Plant → static/uploads/snake-plant.jpg')
    print('   2. Fiddle Leaf Fig → static/uploads/fiddle-leaf.jpg')
    print('\n📌 Open browser: http://localhost:5000')
    print('📌 Press Ctrl+C to stop\n')
    print('='*60 + '\n')
    app.run(debug=True, port=5000)
