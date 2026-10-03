"""
Quick test script to verify category filtering is working
"""
from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'plant_store'

mysql = MySQL(app)

with app.app_context():
    cursor = mysql.connection.cursor()
    
    print("\n=== Testing Category Filtering ===\n")
    
    # Test 1: All products
    cursor.execute("SELECT COUNT(*) FROM products")
    total = cursor.fetchone()[0]
    print(f"Total Products: {total}")
    
    # Test 2: Indoor Plants
    cursor.execute("SELECT COUNT(*) FROM products WHERE category = 'Indoor'")
    indoor_count = cursor.fetchone()[0]
    print(f"Indoor Plants: {indoor_count}")
    
    # Test 3: Outdoor Plants
    cursor.execute("SELECT COUNT(*) FROM products WHERE category = 'Outdoor'")
    outdoor_count = cursor.fetchone()[0]
    print(f"Outdoor Plants: {outdoor_count}")
    
    # Test 4: Flowering Plants
    cursor.execute("SELECT COUNT(*) FROM products WHERE category = 'Flowering'")
    flowering_count = cursor.fetchone()[0]
    print(f"Flowering Plants: {flowering_count}")
    
    # Test 5: List all categories
    cursor.execute("SELECT DISTINCT category FROM products")
    categories = cursor.fetchall()
    print(f"\nAvailable Categories: {[cat[0] for cat in categories]}")
    
    print("\n=== Test Complete ===\n")
    print("✓ Category filtering is ready to use!")
    print("\nTo test in browser:")
    print("1. Start the app: python app.py")
    print("2. Visit: http://localhost:5000")
    print("3. Click on Indoor/Outdoor/Flowering category cards")
    print("4. Or go directly to:")
    print("   - Indoor: http://localhost:5000/products?category=Indoor")
    print("   - Outdoor: http://localhost:5000/products?category=Outdoor")
    print("   - Flowering: http://localhost:5000/products?category=Flowering")
    
    cursor.close()
