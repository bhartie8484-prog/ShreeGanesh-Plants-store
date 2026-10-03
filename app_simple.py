from flask import Flask, render_template, request, session, redirect, url_for, flash
from catalog import CATEGORIES, db_products

app = Flask(__name__)
app.secret_key = 'test_key_for_simple_app'

# Sample products data - kept for the legacy demo categories.
LEGACY_PRODUCTS = [
    # Indoor Plants
    (1, 'Monstera Deliciosa', 'Beautiful Swiss Cheese Plant with large fenestrated leaves', 1299.00, 15, 'monstera.jpg', 'Indoor'),
    (2, 'Snake Plant', 'Low maintenance air purifying plant perfect for beginners', 499.00, 25, 'snake-plant.jpg', 'Indoor'),
    (3, 'Fiddle Leaf Fig', 'Trendy plant with large violin-shaped leaves', 1899.00, 10, 'fiddle-leaf.jpg', 'Indoor'),
    (4, 'Peace Lily', 'Elegant flowering plant that thrives in low light', 699.00, 20, 'peace-lily.jpg', 'Indoor'),
    (5, 'Pothos Golden', 'Easy-care trailing plant with heart-shaped leaves', 399.00, 30, 'pothos.jpg', 'Indoor'),
    (6, 'Aloe Vera', 'Medicinal succulent plant with healing properties', 349.00, 18, 'aloe-vera.jpg', 'Succulent'),
    (7, 'Rubber Plant', 'Glossy-leaved plant that purifies indoor air', 899.00, 12, 'rubber-plant.jpg', 'Indoor'),
    (8, 'ZZ Plant', 'Extremely hardy plant with shiny waxy leaves', 799.00, 4, 'zz-plant.jpg', 'Indoor'),
    
    # Outdoor Plants
    (9, 'Curry Leaf Plant', 'Fresh aromatic leaves for cooking - Essential kitchen plant', 599.00, 20, 'curry-leaf.jpg', 'Outdoor'),
    (10, 'Mint Plant', 'Refreshing herb perfect for tea and cooking', 299.00, 35, 'mint-plant.jpg', 'Outdoor'),
    (11, 'Neem Plant', 'Medicinal plant with multiple health benefits', 899.00, 15, 'neem-plant.jpg', 'Outdoor'),
    (12, 'Tulsi Plant', 'Holy Basil - Sacred plant with medicinal properties', 399.00, 28, 'tulsi-plant.jpg', 'Outdoor'),
    
    # Flowering Plants - NEW!
    (13, 'Hibiscus Flower', 'Beautiful tropical flowers in vibrant colors', 799.00, 18, 'hibiscus-flower.jpg', 'Flowering'),
    (14, 'Jasmine Flower', 'Fragrant white flowers perfect for gardens', 699.00, 22, 'jasmine-flower.jpg', 'Flowering'),
    (15, 'Periwinkle Flower', 'Colorful blooms that thrive in all seasons', 449.00, 30, 'periwinkle-flower.jpg', 'Flowering'),
    (16, 'Rose Plant', 'Classic beautiful roses - Queen of flowers', 999.00, 12, 'rose-flower.jpg', 'Flowering'),
    (17, 'Tulsi Plant', 'Medicinal holy basil for tea and daily wellness', 199.00, 30, 'tulsi-plant.jpg', 'Herbal'),
    (18, 'Aloe Vera', 'Easy-care herbal plant with soothing gel', 349.00, 18, 'aloe-vera.jpg', 'Herbal'),
    (19, 'Lemon Plant', 'Productive citrus plant for a sunny garden', 649.00, 14, 'neem-plant.jpg', 'Fruit'),
    (20, 'Strawberry Plant', 'Compact fruit plant for pots and balconies', 399.00, 20, 'rose-flower.jpg', 'Fruit'),
    (21, 'Tomato Plant', 'Kitchen garden tomato plant for a sunny spot', 199.00, 25, 'curry-leaf.jpg', 'Vegetable'),
    (22, 'Chilli Plant', 'Compact green chilli plant for home gardens', 179.00, 25, 'mint-plant.jpg', 'Vegetable'),
    (23, 'Bonsai Plant', 'Sculptural living decor for desks and tabletops', 999.00, 12, 'bonsai-plant-1.jpg', 'Decorative'),
    (24, 'Areca Palm', 'Graceful decorative palm for indoor spaces', 799.00, 16, 'areca-palm-1.jpg', 'Decorative'),
    (25, 'Hanging Pothos', 'Trailing foliage for hanging display', 449.00, 22, 'pothos-hanging-1.jpg', 'Hanging'),
    (26, 'Hanging Planter', 'Decorative hanging planter for balconies', 549.00, 18, 'plant-pot-planter-1.jpg', 'Hanging'),
    (27, 'Gardening Tool Set', 'Essential hand tools for planting', 699.00, 20, 'plant-seeds-1.jpg', 'Gardening Tools'),
]

SAMPLE_PRODUCTS = [
    (index, *product) for index, product in enumerate(db_products(), start=1)
]

@app.route('/')
def index():
    # Interleave categories so the home page always shows a mixed collection.
    mixed = [next(p for p in SAMPLE_PRODUCTS if p[6] == category) for category in CATEGORIES]
    mixed.extend(SAMPLE_PRODUCTS[:5])
    return render_template('index.html', products=mixed)

@app.route('/products')
def products():
    # Get category filter from query parameter
    category = request.args.get('category', None)
    
    if category:
        # Filter products by category
        filtered_products = [p for p in SAMPLE_PRODUCTS if p[6] == category]
        return render_template('products.html', products=filtered_products, categories=CATEGORIES, selected_category=category)
    else:
        # Show all products
        return render_template('products.html', products=SAMPLE_PRODUCTS, categories=CATEGORIES, selected_category=None)

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
    print('🌿 PlantStore Simple Test Server')
    print('='*60)
    print('✅ No database required - using sample data')
    print('✅ Testing modern UI design')
    print('\n📌 Open browser: http://localhost:5000')
    print('📌 Press Ctrl+C to stop\n')
    print('='*60 + '\n')
    app.run(debug=True, port=5000)
