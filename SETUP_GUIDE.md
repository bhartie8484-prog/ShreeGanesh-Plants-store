# Setup Guide - Plant Store Website 🌿

## Quick Start (Step by Step)

### 1️⃣ Python Install karein
- Python 3.8+ download karein: https://www.python.org/downloads/
- Installation ke time "Add Python to PATH" checkbox check karein

### 2️⃣ MySQL Install karein
- MySQL download karein: https://dev.mysql.com/downloads/installer/
- MySQL Workbench bhi install karein (recommended)
- Root password set karein installation ke time

### 3️⃣ Dependencies Install karein

```bash
# Project folder mein jaayein
cd c:\Users\ujaga\OneDrive\Desktop\plant-store

# Virtual environment banayein (optional but recommended)
python -m venv venv

# Virtual environment activate karein
venv\Scripts\activate

# Dependencies install karein
pip install -r requirements.txt
```

### 4️⃣ Database Setup

**Option 1: MySQL Workbench se (Easy)**
1. MySQL Workbench open karein
2. New Connection banayein (localhost, root user)
3. File > Open SQL Script
4. `database/schema.sql` file select karein
5. Execute button (⚡) click karein

**Option 2: Command Line se**
```bash
# MySQL mein login karein
mysql -u root -p

# Password enter karein, phir:
source c:/Users/ujaga/OneDrive/Desktop/plant-store/database/schema.sql
```

### 5️⃣ Configuration Update karein

`app.py` file ko open karein aur MySQL password update karein:

```python
app.config['MYSQL_PASSWORD'] = 'your_mysql_password'
```

### 6️⃣ Plant Images Add karein (Optional)

`static/uploads/` folder mein plant images add karein with these names:
- monstera.jpg
- snake-plant.jpg
- fiddle-leaf.jpg
- peace-lily.jpg
- pothos.jpg
- aloe-vera.jpg
- rubber-plant.jpg
- zz-plant.jpg

Ya phir koi bhi images add kar sakte ho aur database mein update kar sakte ho.

### 7️⃣ Application Run karein

```bash
python app.py
```

### 8️⃣ Browser mein open karein

```
http://localhost:5000
```

---

## 🎨 New Modern UI Features

### Home Page
- ✅ Hero banner with search bar
- ✅ Trust badges (Free Shipping, 100% Guarantee, etc.)
- ✅ Category cards (Indoor, Outdoor, Seeds, etc.)
- ✅ Best sellers section with modern product cards
- ✅ Promo banner with special offers
- ✅ Plant care tips section
- ✅ Why choose us section

### Product Cards
- ✅ Hover effects with smooth animations
- ✅ Quick view on hover
- ✅ Rating display
- ✅ Original price strike-through
- ✅ Bestseller badges
- ✅ Low stock warnings
- ✅ Add to cart icon button

### Design Elements
- ✅ Modern color scheme (Green theme inspired by Nurserylive)
- ✅ Clean navigation with white background
- ✅ Rounded corners and soft shadows
- ✅ Professional typography
- ✅ Smooth transitions and animations
- ✅ Responsive grid layouts

---

## 🔧 Troubleshooting

### MySQL Connection Error
```
Error: (2003, "Can't connect to MySQL server")
```
**Solution:**
- MySQL server running hai check karein (Services > MySQL)
- Username/password correct hai verify karein
- Port 3306 available hai check karein

### Module Not Found Error
```
ModuleNotFoundError: No module named 'flask'
```
**Solution:**
```bash
pip install -r requirements.txt
```

### Images Not Loading
- Images `static/uploads/` folder mein hai check karein
- Database mein image names match karte hain verify karein
- Browser cache clear karein (Ctrl + Shift + R)

### Port Already in Use
```
OSError: [Errno 48] Address already in use
```
**Solution:**
```bash
# Different port use karein
# app.py ke end mein change karein:
if __name__ == '__main__':
    app.run(debug=True, port=5001)
```

---

## 📱 Features Checklist

### Frontend
- ✅ Modern hero section with search
- ✅ Trust badges
- ✅ Category cards
- ✅ Product grid/carousel
- ✅ Product detail pages
- ✅ Shopping cart
- ✅ User authentication (Login/Register)
- ✅ Contact form
- ✅ Responsive design
- ✅ Flash messages
- ✅ Promo banners

### Backend
- ✅ Flask application
- ✅ MySQL database
- ✅ User authentication
- ✅ Session management
- ✅ Cart functionality
- ✅ Product management
- ✅ Order system (basic)
- ✅ Contact form handling

### Database
- ✅ Users table
- ✅ Products table with sample data
- ✅ Cart table
- ✅ Orders table
- ✅ Order items table
- ✅ Contacts table

---

## 🚀 Next Steps (Future Enhancements)

1. **Admin Panel**
   - Add/Edit/Delete products
   - Manage orders
   - View customer messages

2. **Payment Integration**
   - Razorpay/PayU integration
   - Order confirmation emails

3. **Advanced Features**
   - Product search & filters
   - Product reviews & ratings
   - Wishlist functionality
   - Order tracking
   - Email notifications

4. **Optimization**
   - Image optimization
   - Caching
   - CDN integration
   - SEO optimization

---

## 📞 Support

Koi problem ho to:
1. Error message carefully padhein
2. MySQL aur Python properly installed hain verify karein
3. Database credentials correct hain check karein
4. Browser console errors check karein (F12)

---

**Made with ❤️ for Plant Lovers**

Website ab ready hai! Enjoy coding! 🌱
