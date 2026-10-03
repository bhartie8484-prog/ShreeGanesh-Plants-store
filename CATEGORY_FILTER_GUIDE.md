# Category Filter Guide - Plant Store

## ✨ Feature Overview

Ab aapki Plant Store mein **category-wise filtering** ka feature add ho gaya hai! Users ab easily Indoor, Outdoor, aur Flowering plants ko filter kar sakte hain.

## 🎯 Categories Available

1. **Indoor Plants** 🏠
   - Air-purifying plants
   - Low-light friendly
   - Perfect for homes and offices

2. **Outdoor Plants** 🌳
   - Garden favorites
   - Medicinal herbs
   - Aromatic plants

3. **Flowering Plants** 🌺
   - Beautiful blooms
   - Colorful flowers
   - Fragrant varieties

## 🔧 How It Works

### Homepage (index.html)
- Teen category cards hain with icons
- Har card par click karoge to us category ke plants dikhengy
- "Explore" button click karein to products page with filter khulega

### Products Page (products.html)
- Top par filter buttons hain:
  - **All Plants** - Sab plants dikhayega
  - **Indoor Plants** - Sirf indoor plants
  - **Outdoor Plants** - Sirf outdoor plants
  - **Flowering Plants** - Sirf flowering plants
  
- Active filter button **dark green color** mein dikhai dega
- Hover karne par buttons animate honge

## 📝 Technical Details

### Changed Files:

1. **templates/index.html**
   - Category card links ab `?category=` parameter pass karti hain
   - Indoor, Outdoor, Flowering ke liye alag links

2. **templates/products.html**
   - Category filter buttons section added
   - Dynamic active class based on selected category
   - Icon-based navigation

3. **app.py**
   - Products route updated with category filtering
   - `request.args.get('category')` se category fetch hoti hai
   - SQL query conditional hai based on category

4. **static/css/style.css**
   - `.category-filter` styling
   - `.filter-btn` with hover and active states
   - Responsive design for mobile

5. **database/schema.sql**
   - Sample data updated with proper categories:
     - Indoor Plants (8 items)
     - Outdoor Plants (5 items)
     - Flowering Plants (5 items)

## 🚀 Usage

1. **Database Update** (important):
   ```sql
   -- Apne database mein schema.sql wali sample data insert karein
   -- Ya existing products ka category update karein
   UPDATE products SET category = 'Indoor' WHERE name IN ('Snake Plant', 'ZZ Plant', etc);
   UPDATE products SET category = 'Outdoor' WHERE name IN ('Neem Plant', 'Curry Leaf', etc);
   UPDATE products SET category = 'Flowering' WHERE name IN ('Rose Plant', 'Hibiscus', etc);
   ```

2. **Run the Application**:
   ```bash
   python app.py
   ```

3. **Test the Filters**:
   - Homepage pe category cards click karein
   - Ya directly: 
     - `http://localhost:5000/products` - All plants
     - `http://localhost:5000/products?category=Indoor` - Indoor plants
     - `http://localhost:5000/products?category=Outdoor` - Outdoor plants
     - `http://localhost:5000/products?category=Flowering` - Flowering plants

## 🎨 UI Features

- **Modern Design**: Clean and modern filter buttons
- **Active State**: Selected category clearly visible
- **Hover Effects**: Smooth animations on hover
- **Icons**: Font Awesome icons for visual appeal
- **Responsive**: Mobile-friendly layout
- **Color Coding**: Green theme matching your plant store

## 📱 Mobile Responsive

Mobile screens par filter buttons vertical stack ho jayengi full-width ke sath for easy clicking.

## 🔮 Future Enhancements (Optional)

- Add more categories (Succulents, Cacti, Herbs)
- Price range filter
- Search functionality within categories
- Sort by price/popularity
- Multiple category selection

---

**Happy Gardening! 🌱**
