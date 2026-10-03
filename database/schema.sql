-- Plant Store Database Schema

CREATE DATABASE IF NOT EXISTS plant_store;
USE plant_store;

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Products Table
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    stock INT DEFAULT 0,
    image VARCHAR(255),
    category VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Cart Table
CREATE TABLE IF NOT EXISTS cart (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT DEFAULT 1,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_product (user_id, product_id)
);

-- Orders Table
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
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
);

CREATE TABLE IF NOT EXISTS payments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    transaction_id VARCHAR(50) UNIQUE NOT NULL,
    method VARCHAR(30) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(30) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
);

-- Order Items Table
CREATE TABLE IF NOT EXISTS order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- Contacts Table
CREATE TABLE IF NOT EXISTS contacts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Sample Products Data
INSERT INTO products (name, description, price, stock, image, category) VALUES
-- Indoor Plants
('Monstera Deliciosa', 'Beautiful Swiss Cheese Plant with large fenestrated leaves', 1299.00, 15, 'monstera.jpg', 'Indoor'),
('Snake Plant', 'Low maintenance air purifying plant perfect for beginners', 499.00, 25, 'snake-plant.jpg', 'Indoor'),
('Fiddle Leaf Fig', 'Trendy plant with large violin-shaped leaves', 1899.00, 10, 'fiddle-leaf.jpg', 'Indoor'),
('Peace Lily', 'Elegant flowering plant that thrives in low light', 699.00, 20, 'peace-lily.jpg', 'Indoor'),
('Pothos Golden', 'Easy-care trailing plant with heart-shaped leaves', 399.00, 30, 'pothos.jpg', 'Indoor'),
('Rubber Plant', 'Glossy-leaved plant that purifies indoor air', 899.00, 12, 'rubber-plant.jpg', 'Indoor'),
('ZZ Plant', 'Extremely hardy plant with shiny waxy leaves', 799.00, 22, 'zz-plant.jpg', 'Indoor'),
('Aloe Vera', 'Medicinal succulent plant with healing properties', 349.00, 18, 'aloe-vera.jpg', 'Indoor'),

-- Outdoor Plants
('Neem Plant', 'Medicinal outdoor plant with air purifying qualities', 599.00, 15, 'neem-plant.jpg', 'Outdoor'),
('Curry Leaf Plant', 'Aromatic herb plant perfect for Indian cooking', 299.00, 25, 'curry-leaf.jpg', 'Outdoor'),
('Tulsi Plant', 'Holy Basil plant with medicinal and spiritual significance', 199.00, 30, 'tulsi-plant.jpg', 'Outdoor'),
('Mint Plant', 'Fresh aromatic herb perfect for drinks and cooking', 149.00, 28, 'mint-plant.jpg', 'Outdoor'),
('Bougainvillea', 'Vibrant colorful climber for outdoor gardens', 899.00, 12, 'bougainvillea.jpg', 'Outdoor'),

-- Flowering Plants
('Rose Plant', 'Classic beautiful flowering plant with fragrant blooms', 499.00, 20, 'rose-plant.jpg', 'Flowering'),
('Hibiscus Flower Plant', 'Tropical flowering plant with large colorful blooms', 399.00, 18, 'hibiscus-flower.jpg', 'Flowering'),
('Jasmine Flower Plant', 'Fragrant white flowers perfect for gardens', 349.00, 22, 'jasmine-flower.jpg', 'Flowering'),
('Periwinkle Plant', 'Continuous blooming small flowering plant', 249.00, 25, 'periwinkle-plant.jpg', 'Flowering'),
('Marigold Plant', 'Bright orange and yellow flowering plant', 199.00, 30, 'marigold-plant.jpg', 'Flowering');

-- Expanded shop categories
INSERT INTO products (name, description, price, stock, image, category) VALUES
('Tulsi Plant', 'Medicinal holy basil for tea and daily wellness', 199.00, 30, 'tulsi-plant.jpg', 'Herbal'),
('Mint Plant', 'Fresh aromatic herb for drinks and cooking', 149.00, 28, 'mint-plant.jpg', 'Herbal'),
('Aloe Vera', 'Easy-care herbal plant with soothing gel', 349.00, 18, 'aloe-vera.jpg', 'Herbal'),
('Lemon Plant', 'Productive citrus plant for sunny gardens', 649.00, 14, 'neem-plant.jpg', 'Fruit'),
('Strawberry Plant', 'Compact fruit plant for pots and balconies', 399.00, 20, 'rose-flower.jpg', 'Fruit'),
('Tomato Plant', 'Kitchen garden tomato plant for a sunny spot', 199.00, 25, 'curry-leaf.jpg', 'Vegetable'),
('Chilli Plant', 'Compact green chilli plant for home gardens', 179.00, 25, 'mint-plant.jpg', 'Vegetable'),
('Bonsai Plant', 'Sculptural living decor for desks and tabletops', 999.00, 12, 'bonsai-plant-1.jpg', 'Decorative'),
('Areca Palm', 'Graceful decorative palm for indoor spaces', 799.00, 16, 'areca-palm-1.jpg', 'Decorative'),
('Hanging Pothos', 'Trailing foliage plant for hanging display', 449.00, 22, 'pothos-hanging-1.jpg', 'Hanging'),
('Hanging Planter', 'Decorative hanging planter for balconies', 549.00, 18, 'plant-pot-planter-1.jpg', 'Hanging'),
('Gardening Tool Set', 'Essential hand tools for planting', 699.00, 20, 'plant-seeds-1.jpg', 'Gardening Tools'),
('Organic Potting Mix', 'Ready-to-use growing mix for healthy plants', 299.00, 35, 'fertilizer-soil-compost-1.jpg', 'Gardening Tools');
