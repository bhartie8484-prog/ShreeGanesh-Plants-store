from flask import Flask, render_template, session, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'test_key_for_simple_app'

# Sample products with REAL online images (Unsplash CDN)
SAMPLE_PRODUCTS = [
    (
        1, 
        'Monstera Deliciosa', 
        'Beautiful Swiss Cheese Plant with large fenestrated leaves. Perfect for indoor decoration and air purification.',
        1299.00, 
        15, 
        'https://images.unsplash.com/photo-1614594975525-e45190c55d0b?w=800&h=800&fit=crop&q=80',
        'Indoor'
    ),
    (
        2, 
        'Snake Plant', 
        'Low maintenance air purifying plant perfect for beginners. Thrives in low light conditions.',
        499.00, 
        25, 
        'https://images.unsplash.com/photo-1593482892540-73c9abab5c1e?w=800&h=800&fit=crop&q=80',
        'Indoor'
    ),
    (
        3, 
        'Fiddle Leaf Fig', 
        'Trendy plant with large violin-shaped leaves. A statement piece for any room.',
        1899.00, 
        10, 
        'https://images.unsplash.com/photo-1590502593747-42a996133562?w=800&h=800&fit=crop&q=80',
        'Indoor'
    ),
    (
        4, 
        'Peace Lily', 
        'Elegant flowering plant that thrives in low light. Known for its air purifying qualities.',
        699.00, 
        20, 
        'https://images.unsplash.com/photo-1593482892920-42e0c0b4e390?w=800&h=800&fit=crop&q=80',
        'Indoor'
    ),
    (
        5, 
        'Pothos Golden', 
        'Easy-care trailing plant with heart-shaped leaves. Perfect for hanging baskets.',
        399.00, 
        30, 
        'https://images.unsplash.com/photo-1572688484384-9b7c4e59511e?w=800&h=800&fit=crop&q=80',
        'Indoor'
    ),
    (
        6, 
        'Aloe Vera', 
        'Medicinal succulent plant with healing properties. Great for skin care and burns.',
        349.00, 
        18, 
        'https://images.unsplash.com/photo-1596548438137-d51ea5c83ca5?w=800&h=800&fit=crop&q=80',
        'Succulent'
    ),
    (
        7, 
        'Rubber Plant', 
        'Glossy-leaved plant that purifies indoor air. Low maintenance and fast growing.',
        899.00, 
        12, 
        'https://images.unsplash.com/photo-1610757076685-89b0bb9c0d89?w=800&h=800&fit=crop&q=80',
        'Indoor'
    ),
    (
        8, 
        'ZZ Plant', 
        'Extremely hardy plant with shiny waxy leaves. Survives in low light and with minimal water.',
        799.00, 
        4, 
        'https://images.unsplash.com/photo-1632207691143-643e2de889f3?w=800&h=800&fit=crop&q=80',
        'Indoor'
    ),
]

@app.route('/')
def index():
    return render_template('index_with_images.html', products=SAMPLE_PRODUCTS)

@app.route('/products')
def products():
    return render_template('products_with_images.html', products=SAMPLE_PRODUCTS)

@app.route('/product/<int:id>')
def product_detail(id):
    product = next((p for p in SAMPLE_PRODUCTS if p[0] == id), None)
    if product:
        return render_template('product_detail_with_images.html', product=product)
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
    print('🌿 PlantStore with REAL Images!')
    print('='*60)
    print('✅ Using high-quality plant images from Unsplash')
    print('✅ No database required - demo mode')
    print('\n📌 Open browser: http://localhost:5000')
    print('📌 Press Ctrl+C to stop\n')
    print('='*60 + '\n')
    app.run(debug=True, port=5000)
