# ShreeGanesh-Plants-store

Ek modern aur professional plant store website jo **Nurserylive.com** se inspired hai. Yeh HTML, CSS, JavaScript, Python (Flask), aur MySQL use karti hai.

## 🎨 Design Features

- ✨ **Modern UI/UX** - Nurserylive jaisa clean aur professional design
- 🎯 **Hero Banner** with search functionality
- 🏆 **Trust Badges** section
- 📦 **Category Cards** with hover effects
- 💳 **Modern Product Cards** with quick view
- 🎁 **Promo Banners**
- 🌱 **Plant Care Tips** section
- 📱 **Fully Responsive** design

## Features

- 🌿 User Registration aur Login
- 🛒 Shopping Cart functionality
- 🌱 Product catalog with details
- 📧 Contact form
- 💳 Order management system
- 🔒 Secure password hashing
- 📱 Responsive design

## Folder Structure

```
plant-store/
│
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
│
├── database/             # Database files
│   └── schema.sql       # Database schema and sample data
│
├── static/              # Static files
│   ├── css/
│   │   └── style.css   # Main stylesheet
│   ├── js/
│   │   └── main.js     # JavaScript functionality
│   └── uploads/        # Product images
│       └── placeholder.jpg
│
├── templates/           # HTML templates
│   ├── base.html       # Base template
│   ├── index.html      # Home page
│   ├── products.html   # Products listing
│   ├── product_detail.html
│   ├── cart.html       # Shopping cart
│   ├── login.html      # Login page
│   ├── register.html   # Registration page
│   └── contact.html    # Contact page
│
├── images/             # Additional images
├── config/             # Configuration files
└── uploads/            # User uploaded files

```

## Installation Steps

### 1. Python aur Dependencies Install karo

```bash
# Virtual environment banao (optional but recommended)
python -m venv venv

# Virtual environment activate karo
# Windows:
venv\Scripts\activate

# Python packages install karo
pip install -r requirements.txt
```

### 2. MySQL Database Setup

```bash
# MySQL mein login karo
mysql -u root -p

# Database create karo aur schema load karo
source database/schema.sql

# Ya phir direct command se:
mysql -u root -p < database/schema.sql
```

### 3. Configuration

`app.py` file mein apne MySQL credentials update karo:

```python
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'your_password'
app.config['MYSQL_DB'] = 'plant_store'
```

### 4. Plant Images Add karo

`static/uploads/` folder mein apne plant images add karo. Sample data mein ye image names use kiye gaye hain:

- monstera.jpg
- snake-plant.jpg
- fiddle-leaf.jpg
- peace-lily.jpg
- pothos.jpg
- aloe-vera.jpg
- rubber-plant.jpg
- zz-plant.jpg

### 5. Application Run karo

```bash
python app.py
```

Website `http://localhost:5000` par available hogi.

## Database Tables

1. **users** - User accounts
2. **products** - Plant products
3. **cart** - Shopping cart items
4. **orders** - Order history
5. **order_items** - Order details
6. **contacts** - Contact form submissions

## Default Admin/Test Data

Database schema automatically sample products insert karti hai. Aap khud users register kar sakte ho.

## Technologies Used

- **Frontend**: HTML5, CSS3, JavaScript
- **Backend**: Python Flask
- **Database**: MySQL
- **Libraries**: Flask-MySQLdb, Werkzeug

## Features Details

### User Management

- Registration with password hashing
- Secure login/logout
- Session management

### Product Management

- Product listing with images
- Product detail pages
- Category filtering
- Stock management

### Shopping Cart

- Add to cart functionality
- Quantity management
- Order summary
- Checkout process

### Responsive Design

- Mobile-friendly layout
- Tablet optimization
- Desktop experience

## Future Enhancements

- Payment gateway integration
- Order tracking
- Admin dashboard
- Product reviews
- Wishlist functionality
- Email notifications
- Search functionality
- Advanced filtering

## Troubleshooting

### MySQL Connection Error

- MySQL server running hai check karo
- Credentials correct hain verify karo
- Database exist karta hai confirm karo

### Images Not Loading

- Images `static/uploads/` folder mein hain check karo
- Image names database mein match karte hain verify karo

### Flask Import Error

- Virtual environment activate hai ensure karo
- `pip install -r requirements.txt` phir se run karo

## Support

Koi problem ho to:

1. Error message check karo
2. MySQL connection verify karo
3. Python dependencies install hain confirm karo

## License

This project is for educational purposes.

---

**Happy Coding! 🌿**

# ShreeGanesh-Plants-store
