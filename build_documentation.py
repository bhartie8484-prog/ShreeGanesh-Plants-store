from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.text import WD_BREAK
from pathlib import Path
from datetime import date

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "ShreeGanesh_Plants_Store_Documentation.docx"

NAVY = "173F35"
GREEN = "2F6B4F"
LIGHT_GREEN = "E8F2EC"
PALE = "F4F7F5"
GRAY = "5E6B66"
LIGHT_GRAY = "E6EAE8"
WHITE = "FFFFFF"
BLACK = "1F2522"
GOLD = "B8892D"
RED = "9B2C2C"


def set_cell_shading(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = tc_pr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        tc_pr.append(shd)
    shd.set(qn("w:fill"), fill)


def set_cell_margins(cell, top=100, start=120, bottom=100, end=120):
    tc = cell._tc
    tc_pr = tc.get_or_add_tcPr()
    tc_mar = tc_pr.first_child_found_in("w:tcMar")
    if tc_mar is None:
        tc_mar = OxmlElement("w:tcMar")
        tc_pr.append(tc_mar)
    for m, v in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        node = tc_mar.find(qn(f"w:{m}"))
        if node is None:
            node = OxmlElement(f"w:{m}")
            tc_mar.append(node)
        node.set(qn("w:w"), str(v))
        node.set(qn("w:type"), "dxa")


def set_table_geometry(table, widths_dxa, indent=120):
    table.autofit = False
    tbl_pr = table._tbl.tblPr
    tbl_w = tbl_pr.first_child_found_in("w:tblW")
    tbl_w.set(qn("w:w"), str(sum(widths_dxa)))
    tbl_w.set(qn("w:type"), "dxa")
    tbl_ind = tbl_pr.first_child_found_in("w:tblInd")
    if tbl_ind is None:
        tbl_ind = OxmlElement("w:tblInd")
        tbl_pr.append(tbl_ind)
    tbl_ind.set(qn("w:w"), str(indent))
    tbl_ind.set(qn("w:type"), "dxa")
    grid = table._tbl.tblGrid
    for child in list(grid):
        grid.remove(child)
    for width in widths_dxa:
        col = OxmlElement("w:gridCol")
        col.set(qn("w:w"), str(width))
        grid.append(col)
    for row in table.rows:
        for idx, cell in enumerate(row.cells):
            tc_pr = cell._tc.get_or_add_tcPr()
            tc_w = tc_pr.first_child_found_in("w:tcW")
            tc_w.set(qn("w:w"), str(widths_dxa[idx]))
            tc_w.set(qn("w:type"), "dxa")
            set_cell_margins(cell)
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER


def set_repeat_table_header(row):
    tr_pr = row._tr.get_or_add_trPr()
    tbl_header = OxmlElement("w:tblHeader")
    tbl_header.set(qn("w:val"), "true")
    tr_pr.append(tbl_header)


def set_run(run, size=None, bold=None, color=None, italic=None, font="Aptos"):
    run.font.name = font
    run._element.get_or_add_rPr().rFonts.set(qn("w:ascii"), font)
    run._element.get_or_add_rPr().rFonts.set(qn("w:hAnsi"), font)
    if size is not None:
        run.font.size = Pt(size)
    if bold is not None:
        run.bold = bold
    if italic is not None:
        run.italic = italic
    if color:
        run.font.color.rgb = RGBColor.from_string(color)


def add_page_field(paragraph):
    run = paragraph.add_run()
    fld_char1 = OxmlElement("w:fldChar")
    fld_char1.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = " PAGE "
    fld_char2 = OxmlElement("w:fldChar")
    fld_char2.set(qn("w:fldCharType"), "end")
    run._r.extend([fld_char1, instr, fld_char2])
    set_run(run, size=9, color=GRAY)


doc = Document()
sec = doc.sections[0]
sec.page_width = Inches(8.5)
sec.page_height = Inches(11)
sec.top_margin = Inches(1)
sec.bottom_margin = Inches(0.85)
sec.left_margin = Inches(1)
sec.right_margin = Inches(1)
sec.header_distance = Inches(0.492)
sec.footer_distance = Inches(0.492)

# compact_reference_guide token map
styles = doc.styles
normal = styles["Normal"]
normal.font.name = "Aptos"
normal._element.rPr.rFonts.set(qn("w:ascii"), "Aptos")
normal._element.rPr.rFonts.set(qn("w:hAnsi"), "Aptos")
normal.font.size = Pt(10.5)
normal.font.color.rgb = RGBColor.from_string(BLACK)
normal.paragraph_format.space_after = Pt(6)
normal.paragraph_format.line_spacing = 1.2

for name, size, before, after, color in [
    ("Heading 1", 16, 18, 10, GREEN),
    ("Heading 2", 13, 14, 7, GREEN),
    ("Heading 3", 11.5, 10, 5, NAVY),
]:
    st = styles[name]
    st.font.name = "Aptos Display"
    st._element.rPr.rFonts.set(qn("w:ascii"), "Aptos Display")
    st._element.rPr.rFonts.set(qn("w:hAnsi"), "Aptos Display")
    st.font.size = Pt(size)
    st.font.bold = True
    st.font.color.rgb = RGBColor.from_string(color)
    st.paragraph_format.space_before = Pt(before)
    st.paragraph_format.space_after = Pt(after)
    st.paragraph_format.keep_with_next = True

for list_style in ("List Bullet", "List Number"):
    st = styles[list_style]
    st.font.name = "Aptos"
    st.font.size = Pt(10.5)
    st.paragraph_format.left_indent = Inches(0.375)
    st.paragraph_format.first_line_indent = Inches(-0.188)
    st.paragraph_format.space_after = Pt(4)
    st.paragraph_format.line_spacing = 1.2

if "Code Block" not in styles:
    code_style = styles.add_style("Code Block", WD_STYLE_TYPE.PARAGRAPH)
else:
    code_style = styles["Code Block"]
code_style.font.name = "Consolas"
code_style._element.rPr.rFonts.set(qn("w:ascii"), "Consolas")
code_style._element.rPr.rFonts.set(qn("w:hAnsi"), "Consolas")
code_style.font.size = Pt(8.5)
code_style.font.color.rgb = RGBColor.from_string(NAVY)
code_style.paragraph_format.left_indent = Inches(0.22)
code_style.paragraph_format.right_indent = Inches(0.12)
code_style.paragraph_format.space_before = Pt(3)
code_style.paragraph_format.space_after = Pt(6)


def add_header_footer(section):
    hp = section.header.paragraphs[0]
    hp.text = "SHREEGANESH PLANTS-STORE  |  TECHNICAL & USER DOCUMENTATION"
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    set_run(hp.runs[0], size=8, bold=True, color=GRAY)
    fp = section.footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = fp.add_run("Project Documentation  |  Page ")
    set_run(r, size=9, color=GRAY)
    add_page_field(fp)


add_header_footer(sec)


def add_title(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(8)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(text)
    set_run(r, size=30, bold=True, color=NAVY, font="Aptos Display")
    return p


def add_kicker(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(15)
    r = p.add_run(text.upper())
    set_run(r, size=10, bold=True, color=GOLD)


def add_subtitle(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(24)
    r = p.add_run(text)
    set_run(r, size=14, color=GREEN, font="Aptos Display")


def add_body(text, bold_start=None):
    p = doc.add_paragraph()
    if bold_start and text.startswith(bold_start):
        r = p.add_run(bold_start)
        set_run(r, bold=True, color=NAVY)
        p.add_run(text[len(bold_start):])
    else:
        p.add_run(text)
    return p


def new_numbering(marker="decimal"):
    numbering = doc.part.numbering_part.element
    abstract_ids = [int(x.get(qn("w:abstractNumId"))) for x in numbering.findall(qn("w:abstractNum"))]
    num_ids = [int(x.get(qn("w:numId"))) for x in numbering.findall(qn("w:num"))]
    abstract_id = max(abstract_ids, default=0) + 1
    num_id = max(num_ids, default=0) + 1
    abstract = OxmlElement("w:abstractNum")
    abstract.set(qn("w:abstractNumId"), str(abstract_id))
    multi = OxmlElement("w:multiLevelType")
    multi.set(qn("w:val"), "singleLevel")
    abstract.append(multi)
    lvl = OxmlElement("w:lvl")
    lvl.set(qn("w:ilvl"), "0")
    start = OxmlElement("w:start")
    start.set(qn("w:val"), "1")
    num_fmt = OxmlElement("w:numFmt")
    num_fmt.set(qn("w:val"), marker)
    lvl_text = OxmlElement("w:lvlText")
    lvl_text.set(qn("w:val"), "%1." if marker == "decimal" else "•")
    suff = OxmlElement("w:suff")
    suff.set(qn("w:val"), "tab")
    p_pr = OxmlElement("w:pPr")
    tabs = OxmlElement("w:tabs")
    tab = OxmlElement("w:tab")
    tab.set(qn("w:val"), "num")
    tab.set(qn("w:pos"), "540")
    tabs.append(tab)
    ind = OxmlElement("w:ind")
    ind.set(qn("w:left"), "540")
    ind.set(qn("w:hanging"), "270")
    p_pr.extend([tabs, ind])
    lvl.extend([start, num_fmt, lvl_text, suff, p_pr])
    abstract.append(lvl)
    first_num = numbering.find(qn("w:num"))
    if first_num is None:
        numbering.append(abstract)
    else:
        numbering.insert(list(numbering).index(first_num), abstract)
    num = OxmlElement("w:num")
    num.set(qn("w:numId"), str(num_id))
    abstract_ref = OxmlElement("w:abstractNumId")
    abstract_ref.set(qn("w:val"), str(abstract_id))
    num.append(abstract_ref)
    numbering.append(num)
    return num_id


def add_bullets(items):
    num_id = new_numbering("bullet")
    for item in items:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.375)
        p.paragraph_format.first_line_indent = Inches(-0.188)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.2
        p_pr = p._p.get_or_add_pPr()
        num_pr = OxmlElement("w:numPr")
        ilvl = OxmlElement("w:ilvl")
        ilvl.set(qn("w:val"), "0")
        num_id_el = OxmlElement("w:numId")
        num_id_el.set(qn("w:val"), str(num_id))
        num_pr.extend([ilvl, num_id_el])
        p_pr.append(num_pr)
        p.add_run(item)


def add_steps(items):
    num_id = new_numbering("decimal")
    for item in items:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.375)
        p.paragraph_format.first_line_indent = Inches(-0.188)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.2
        p_pr = p._p.get_or_add_pPr()
        num_pr = OxmlElement("w:numPr")
        ilvl = OxmlElement("w:ilvl")
        ilvl.set(qn("w:val"), "0")
        num_id_el = OxmlElement("w:numId")
        num_id_el.set(qn("w:val"), str(num_id))
        num_pr.extend([ilvl, num_id_el])
        p_pr.append(num_pr)
        p.add_run(item)


def add_code(text):
    p = doc.add_paragraph(style="Code Block")
    p.add_run(text)
    p_pr = p._p.get_or_add_pPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), PALE)
    p_pr.append(shd)
    return p


def add_callout(label, text, fill=LIGHT_GREEN, color=NAVY):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_geometry(table, [9360], 120)
    cell = table.cell(0, 0)
    set_cell_shading(cell, fill)
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run(label + ": ")
    set_run(r, bold=True, color=color)
    r2 = p.add_run(text)
    set_run(r2, color=BLACK)
    doc.add_paragraph().paragraph_format.space_after = Pt(1)


def add_table(headers, rows, widths):
    table = doc.add_table(rows=1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = "Table Grid"
    set_table_geometry(table, widths, 120)
    hdr = table.rows[0]
    set_repeat_table_header(hdr)
    for i, h in enumerate(headers):
        set_cell_shading(hdr.cells[i], GREEN)
        p = hdr.cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r = p.add_run(str(h))
        set_run(r, size=9.5, bold=True, color=WHITE)
    for row in rows:
        cells = table.add_row().cells
        for i, value in enumerate(row):
            if len(table.rows) % 2 == 0:
                set_cell_shading(cells[i], PALE)
            p = cells[i].paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(str(value))
            set_run(r, size=9.2, color=BLACK)
    doc.add_paragraph().paragraph_format.space_after = Pt(1)
    return table


def page_break():
    doc.add_page_break()


# Cover - editorial_cover
for _ in range(5):
    doc.add_paragraph().paragraph_format.space_after = Pt(12)
add_kicker("Complete Website Documentation")
add_title("ShreeGanesh Plants-store")
add_subtitle("User Manual, Functional Specification & Technical Reference")
add_callout("Document scope", "Flask + MySQL e-commerce website ka verified functional aur technical documentation. Current source code snapshot ke anusar taiyar kiya gaya.")
doc.add_paragraph().paragraph_format.space_after = Pt(35)
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Version 1.0  |  03 October 2026")
set_run(r, size=11, bold=True, color=GRAY)
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Prepared for project handover, maintenance, demonstration and future development")
set_run(r, size=9.5, italic=True, color=GRAY)

page_break()
doc.add_heading("Document Control", level=1)
add_table(["Field", "Detail"], [
    ("Project", "ShreeGanesh Plants-store"),
    ("Application type", "Responsive plant and gardening e-commerce web application"),
    ("Backend", "Python Flask 2.3.0"),
    ("Database", "MySQL through PyMySQL 1.1.2"),
    ("Frontend", "HTML5, Jinja2, CSS3, JavaScript, Font Awesome"),
    ("Primary entry point", "app.py"),
    ("Catalog baseline", "73 curated products across 9 categories"),
    ("Document status", "Current implementation reference"),
    ("Repository", "github.com/bhartie8484-prog/ShreeGanesh-Plants-store"),
], [2300, 7060])

doc.add_heading("How to Use This Document", level=2)
add_bullets([
    "End users: Sections 3 to 7 explain browsing, account, cart, checkout, orders and support pages.",
    "Developers: Sections 8 to 15 cover architecture, routes, database, catalog, configuration and maintenance.",
    "Evaluators: Sections 1, 2 and 16 summarize scope, completed features, known constraints and future roadmap.",
])
add_callout("Important", "The checkout and payment screens are demonstration flows. They do not connect to a real payment gateway and do not charge money.", fill="FFF5DF", color=GOLD)

doc.add_heading("Contents", level=1)
contents = [
    "Executive Summary", "Scope and Feature Inventory", "Website Navigation and Public Pages",
    "Account and Authentication", "Product Discovery and Catalog", "Cart, Checkout and Payment",
    "Orders, Tracking and Customer Support", "System Architecture", "Application Routes",
    "Database Design", "Catalog and Image Management", "Frontend Design and JavaScript",
    "Installation and Local Setup", "Configuration and Security", "Testing and Troubleshooting",
    "Known Limitations and Roadmap", "Appendix A. Folder Structure", "Appendix B. Operational Checklist",
]
add_steps(contents)
doc.add_heading("1. Executive Summary", level=1)
add_body("ShreeGanesh Plants-store ek full-stack educational e-commerce website hai jo plants, gardening tools aur related products ko browse aur order karne ka responsive experience deti hai. Application server-side rendering ke liye Flask/Jinja2, persistent data ke liye MySQL, aur interaction/design ke liye CSS aur vanilla JavaScript use karti hai.")
add_body("Current system mein public catalog browsing, nine-category filtering, product detail pages, user registration/login, persistent shopping cart, address collection, demo payment outcomes, stock validation, order creation, order history, public order tracking, contact storage, policies, FAQ aur custom error pages implemented hain.")
add_callout("Current baseline", "Catalog code 73 products supply karta hai: Outdoor 9 items; baaki Indoor, Flowering, Herbal, Fruit, Vegetable, Decorative, Hanging aur Gardening Tools mein 8-8 items. Price range Rs.149 se Rs.1,899 hai.")

doc.add_heading("Primary Objectives", level=2)
add_bullets([
    "Customers ko category-wise plants aur tools discover karne dena.",
    "Secure password hashing aur session-based login ke saath customer account dena.",
    "Cart se checkout, simulated payment aur confirmed order tak complete shopping journey dikhana.",
    "Local product images, responsive layouts aur mobile navigation ke saath polished storefront banana.",
    "MySQL-based order, payment, stock aur contact data persistence demonstrate karna.",
])

page_break()
doc.add_heading("2. Scope and Feature Inventory", level=1)
add_table(["Module", "Implemented capability", "Status"], [
    ("Storefront", "Hero, featured products, category navigation, promotions, trust messaging", "Complete"),
    ("Catalog", "All products, nine filters, product detail, local/remote image support", "Complete"),
    ("Authentication", "Registration, login, logout, hashed passwords, sessions", "Complete"),
    ("Cart", "Add, increment duplicate item, update quantity, remove, totals", "Complete"),
    ("Checkout", "Delivery details, PIN validation, shipping fee rules", "Complete"),
    ("Payment", "UPI/card/COD selection and simulated success/failure", "Demo only"),
    ("Orders", "Order number, items, payment record, stock deduction, history", "Complete"),
    ("Support", "Contact form, FAQ, about, policies, order tracking", "Complete"),
    ("Administration", "Admin dashboard and UI-based product/order management", "Not included"),
], [1800, 5700, 1860])

page_break()
doc.add_heading("3. Website Navigation and Public Pages", level=1)
doc.add_heading("3.1 Global Layout", level=2)
add_body("base.html common navigation, flash messages, footer links, responsive menu aur shared CSS/JavaScript load karta hai. Logged-in state ke basis par cart, logout aur orders links dikhte hain; guest state mein login aur register links milte hain.")
add_bullets([
    "Main navigation: Home, All Plants, About, Contact.",
    "Authenticated navigation: Cart, Orders and Logout.",
    "Footer shop links: Flowering, Herbal, Fruit and Gardening Tools.",
    "Footer help links: Shipping Policy, Return Policy, FAQ and Track Order.",
    "Legal links: Privacy and Terms.",
])

doc.add_heading("3.2 Home Page (/)", level=2)
add_body("Home page available in-stock products ko random order mein load karti hai. System pehle har category se ek representative item choose karta hai, phir remaining products add karke maximum 12 featured products show karta hai. Is approach se home page par category diversity maintain hoti hai.")
add_bullets([
    "Premium hero section aur primary shop call-to-action.",
    "Visual category navigation for all nine categories.",
    "Featured/best-selling style product cards with image, category, price and stock cues.",
    "Direct product details aur add-to-cart actions.",
    "Promotional and plant-care content sections.",
])

doc.add_heading("3.3 Informational Pages", level=2)
add_table(["Page", "URL", "Purpose"], [
    ("About", "/about", "Brand story, healthy plants, expert support and responsible choices."),
    ("FAQ", "/faq", "Frequently asked questions for ordering and plant purchase support."),
    ("Contact", "/contact", "Name, email and message collect karke contacts table mein store karta hai."),
    ("Policies", "/policy/<slug>", "Shipping, returns, privacy and terms content."),
    ("Error", "404 / 500", "Friendly error page with home navigation."),
], [1500, 2100, 5760])

page_break()
doc.add_heading("4. Account and Authentication", level=1)
doc.add_heading("4.1 Registration", level=2)
add_steps([
    "User /register page par full name, unique email aur password submit karta hai.",
    "Backend Werkzeug generate_password_hash() se password ka hash banata hai.",
    "users table mein name, email aur hashed password insert hota hai.",
    "Duplicate email par transaction rollback hota hai aur readable error flash hota hai.",
    "Successful registration user ko login page par redirect karti hai.",
])

doc.add_heading("4.2 Login and Session", level=2)
add_body("Login email se user record fetch karta hai aur check_password_hash() se password verify karta hai. Success par session mein user_id aur user_name save hote hain. Logout poori session clear karta hai.")
add_callout("Access control", "Cart, checkout, payment, order success aur order history routes logged-in user require karte hain. Unauthorized access ko login/checkout ki taraf redirect kiya jata hai.")

doc.add_heading("4.3 Authentication Data Flow", level=2)
add_table(["Input", "Processing", "Persistent/session result"], [
    ("Registration form", "Validation + password hashing", "New users row"),
    ("Login form", "Email lookup + hash comparison", "user_id and user_name session keys"),
    ("Logout request", "session.clear()", "Authenticated state removed"),
], [2200, 3400, 3760])

doc.add_heading("Security Notes", level=2)
add_bullets([
    "Passwords plaintext mein store nahi hote; Werkzeug hashing use hoti hai.",
    "SQL statements parameterized placeholders use karte hain, jo SQL injection risk reduce karte hain.",
    "Current forms mein CSRF tokens implemented nahi hain; production se pehle Flask-WTF/CSRF protection add karna chahiye.",
    "Session secret local configuration/environment se strong random value hona chahiye; development fallback production ke liye unsuitable hai.",
])

page_break()
doc.add_heading("5. Product Discovery and Catalog", level=1)
doc.add_heading("5.1 Supported Categories", level=2)
add_table(["Category", "Catalog count", "Typical products"], [
    ("Indoor", "8", "Aloe Vera, Snake Plant, Money Plant, ZZ Plant"),
    ("Outdoor", "9", "Caladium, Coral Bells, Curry Leaf, Fern, Neem"),
    ("Flowering", "8", "Rose, Hibiscus, Jasmine, Marigold"),
    ("Herbal", "8", "Tulsi, Mint, Ashwagandha, Lemongrass"),
    ("Fruit", "8", "Lemon, Mango, Guava, Papaya"),
    ("Vegetable", "8", "Tomato, Chilli, Brinjal, Cucumber"),
    ("Decorative", "8", "Aglaonema, Croton, Ficus, Lucky Bamboo"),
    ("Hanging", "8", "Golden Money Plant, Spider Plant, Philodendron"),
    ("Gardening Tools", "8", "Pruner, spade, rake, gloves, watering can"),
], [1900, 1500, 5960])

doc.add_heading("5.2 Product Listing", level=2)
add_body("/products bina query parameter ke sab in-stock items load karta hai. category query parameter dene par exact category match ke saath filter hota hai. Template active filter ko visually highlight karta hai aur empty-result state bhi provide karta hai.")
add_code("/products\n/products?category=Indoor\n/products?category=Gardening%20Tools")

doc.add_heading("5.3 Product Detail", level=2)
add_body("/product/<id> selected product ka complete record dikhata hai. Missing ID par custom 404 return hota hai. Page product image, name, category, description, current price, stock indication, care/value details aur add-to-cart action provide karti hai.")

doc.add_heading("5.4 Catalog Synchronization", level=2)
add_body("Har request se pehle ensure_catalog() curated catalog ko database ke saath synchronize karta hai. app_meta table catalog_version track karti hai. Version mismatch par existing products update hote hain aur missing products insert hote hain; referenced records ko wholesale delete nahi kiya jata.")
add_callout("Catalog version", "Current code catalog_version = 6 use karta hai. Purane version 4 aur 5 se specific Indoor/Outdoor product rename migrations bhi included hain.")

page_break()
doc.add_heading("6. Cart, Checkout and Payment", level=1)
doc.add_heading("6.1 Shopping Cart", level=2)
add_body("Cart database-backed hai, isliye authenticated user ke items requests ke beech persistent rehte hain. users aur products ke combination par unique constraint duplicate row ko रोकता hai; same product dobara add karne par quantity increment hoti hai.")
add_table(["Action", "Route", "Behavior"], [
    ("View cart", "GET /cart", "Joined product rows aur calculated total show karta hai."),
    ("Add product", "GET/POST /add_to_cart/<id>", "New row insert ya existing quantity +1."),
    ("Update quantity", "POST /cart/update/<id>", "Minimum 1 validate karke owned row update."),
    ("Remove item", "POST /cart/remove/<id>", "Owned cart row delete."),
], [1800, 3100, 4460])

doc.add_heading("6.2 Checkout Rules", level=2)
add_bullets([
    "Empty cart checkout nahi kar sakta.",
    "Required fields: full name, phone, address, city, state, six-digit PIN and payment method.",
    "Subtotal Rs.999 se greater hone par shipping free; otherwise Rs.50.",
    "Checkout form values temporary session['checkout'] structure mein store hote hain.",
    "Available methods: UPI, card and cash on delivery (COD).",
])

doc.add_heading("6.3 Demo Payment and Order Transaction", level=2)
add_steps([
    "Payment page current cart se total dobara calculate karti hai.",
    "User simulated success ya failure choose karta hai; failure par koi order/charge nahi banta.",
    "Success se pehle requested quantity ko current product stock ke against validate kiya jata hai.",
    "Unique order number PS + date + random suffix se generate hota hai.",
    "orders row confirmed status ke saath create hota hai; COD payment pending, other methods paid hote hain.",
    "Har cart item order_items mein snapshot price aur quantity ke saath insert hota hai.",
    "Product stock deduct hota hai aur payments row transaction ID ke saath create hota hai.",
    "User cart clear hota hai, database commit hota hai aur success page open hoti hai.",
])
add_callout("Payment disclaimer", "Payment screen sirf end-to-end workflow testing ke liye fake gateway hai. Card/UPI credentials collect ya store nahi kiye jate.", fill="FFF5DF", color=GOLD)

page_break()
doc.add_heading("7. Orders, Tracking and Customer Support", level=1)
doc.add_heading("7.1 Order Confirmation and History", level=2)
add_body("Successful payment ke baad /order-success/<order_number> sirf authenticated owning user ko order dikhata hai. /orders logged-in user ke orders newest-first list karta hai, including total, payment state aur order state.")

doc.add_heading("7.2 Public Order Tracking", level=2)
add_body("/track-order par order number uppercase/trim karke lookup hota hai. Match hone par order status, payment status, created date context aur destination city show hoti hai. Invalid number par flash error milta hai.")
add_callout("Privacy observation", "Current tracking lookup order number janne wale visitor ko limited order status aur city dikhata hai. Production mein registered email/phone verification ya signed tracking token add karna recommended hai.")

doc.add_heading("7.3 Contact and Policy Support", level=2)
add_bullets([
    "Contact submissions contacts table mein timestamp ke saath persist hote hain.",
    "Shipping policy dispatch 2-4 business days aur delivery 3-7 business days ka guidance deti hai.",
    "Returns content damaged/incorrect items ko 24 hours mein photos aur unboxing video ke saath report karne ko kehta hai.",
    "Privacy page order/support purposes ke liye minimal data collection explain karti hai.",
    "Terms page natural product variation aur demo-payment nature clarify karti hai.",
])

doc.add_heading("Customer Journey Summary", level=2)
add_table(["Stage", "Customer action", "System outcome"], [
    ("Discover", "Home/category browse", "In-stock product cards"),
    ("Evaluate", "Open detail page", "Description, price, stock and image"),
    ("Account", "Register/login", "Authenticated session"),
    ("Purchase", "Cart + checkout", "Validated delivery/payment selection"),
    ("Confirm", "Simulate payment", "Order, payment and stock transaction"),
    ("After-sales", "Orders/track/contact", "Status visibility and support capture"),
], [1600, 3200, 4560])

page_break()
doc.add_heading("8. System Architecture", level=1)
add_body("Application traditional server-rendered three-layer structure follow karti hai. Browser request Flask route tak jati hai; route MySQL data read/write karke Jinja2 template render karta hai; CSS/JavaScript presentation aur client-side interaction enhance karte hain.")
add_table(["Layer", "Components", "Responsibility"], [
    ("Presentation", "templates/*.html, static/css/style.css, static/js/main.js", "Responsive UI, forms, navigation, cards, feedback and search filtering."),
    ("Application", "app.py", "Routing, sessions, validation, business rules, checkout and error handling."),
    ("Catalog", "catalog.py", "Categories and curated product dataset for synchronization."),
    ("Persistence", "MySQL plant_store", "Users, products, carts, orders, payments, contacts and metadata."),
    ("Configuration", "config/local.py (ignored)", "Machine-specific database and secret settings."),
    ("Media", "static/uploads", "Locally served product and marketing images."),
], [1700, 3400, 4260])

doc.add_heading("Request Lifecycle", level=2)
add_steps([
    "Browser Flask route request bhejta hai.",
    "before_request hook catalog aur evolving order/payment schema ensure karta hai.",
    "get_db() request context mein lazy MySQL connection create/reuse karta hai.",
    "Route parameterized SQL aur business validation execute karta hai.",
    "Jinja2 HTML generate karta hai; static assets browser load karta hai.",
    "teardown_appcontext request ke end par connection close karta hai.",
])

doc.add_heading("Runtime Characteristics", level=2)
add_bullets([
    "MySQL connection utf8mb4 charset aur autocommit=False ke saath create hota hai.",
    "Write flows explicit commit/rollback use karte hain.",
    "Catalog/schema readiness process globals se repeated work reduce karti hai.",
    "Application production entry point par debug=False se run hoti hai.",
])

page_break()
doc.add_heading("9. Application Routes", level=1)
routes = [
    ("GET", "/", "Home/featured products", "Public"),
    ("GET", "/products", "All/category product listing", "Public"),
    ("GET", "/product/<id>", "Product detail", "Public"),
    ("GET/POST", "/register", "Create user account", "Public"),
    ("GET/POST", "/login", "Authenticate user", "Public"),
    ("GET", "/logout", "Clear session", "Logged-in"),
    ("GET", "/cart", "View cart", "Logged-in"),
    ("POST", "/cart/update/<id>", "Change quantity", "Logged-in"),
    ("POST", "/cart/remove/<id>", "Remove cart item", "Logged-in"),
    ("GET/POST", "/add_to_cart/<id>", "Add/increment product", "Logged-in"),
    ("GET/POST", "/checkout", "Delivery and payment selection", "Logged-in"),
    ("GET/POST", "/payment", "Demo payment completion", "Logged-in"),
    ("GET", "/order-success/<number>", "Owned order confirmation", "Logged-in"),
    ("GET", "/orders", "Owned order history", "Logged-in"),
    ("GET/POST", "/track-order", "Lookup order number", "Public"),
    ("GET/POST", "/contact", "Contact message", "Public"),
    ("GET", "/about", "Brand information", "Public"),
    ("GET", "/faq", "Frequently asked questions", "Public"),
    ("GET", "/policy/<slug>", "Policy content", "Public"),
]
add_table(["Method", "Route", "Purpose", "Access"], routes, [1250, 3000, 3550, 1560])

page_break()
doc.add_heading("10. Database Design", level=1)
add_table(["Table", "Purpose", "Important relationships/constraints"], [
    ("users", "Customer identity and password hash", "Unique email; parent of cart/orders"),
    ("products", "Catalog content, price, stock, image, category", "Referenced by cart/order_items"),
    ("cart", "Per-user active basket", "Unique user_id + product_id; cascade delete"),
    ("orders", "Order header, totals, delivery and status", "Belongs to user; unique order_number"),
    ("order_items", "Purchased product line snapshot", "Belongs to order and product"),
    ("payments", "Demo transaction ledger", "Belongs to order; unique transaction_id"),
    ("contacts", "Customer support messages", "Independent timestamped records"),
    ("app_meta", "Catalog migration/version state", "String key/value primary key"),
], [1750, 3450, 4160])

doc.add_heading("10.1 Relationship Model", level=2)
add_bullets([
    "One user can have many cart rows and many orders.",
    "One product can appear in many carts and order items.",
    "One order contains many order items and one or more payment records by schema capability (current flow creates one).",
    "Deleting a user cascades their cart and orders; deleting an order cascades order items and payments.",
    "order_items product foreign key intentionally preserves product reference rules without ON DELETE CASCADE.",
])

doc.add_heading("10.2 Runtime Schema Migration", level=2)
add_body("ensure_store_schema() existing orders table mein order number, payment, shipping fields add karne ka प्रयास करता है. MySQL duplicate-column error 1060 ignore hota hai. payments table absent ho to create hoti hai. Ye lightweight compatibility mechanism hai, full migration framework nahi.")
add_callout("Recommended", "Production growth ke liye Flask-Migrate/Alembic jaisa versioned migration system use karein. Runtime ALTER TABLE ko startup deployment step se replace karein.")

page_break()
doc.add_heading("10.3 Key Business Data", level=2)
add_table(["Field", "Rule"], [
    ("products.stock", "Successful order ke waqt ordered quantity se decrease."),
    ("orders.status", "Current successful flow mein confirmed."),
    ("orders.payment_status", "COD = pending; UPI/card demo success = paid."),
    ("orders.order_number", "PS + YYMMDD + six uppercase random hex characters."),
    ("payments.transaction_id", "TXN + twelve uppercase random hex characters."),
], [2800, 6560])
doc.add_heading("11. Catalog and Image Management", level=1)
doc.add_heading("11.1 Product Record Shape", level=2)
add_body("catalog.py ke db_products() records database insert order follow karte hain: name, description, price, stock, image filename aur category. Database query results templates mein positional indexes se consumed hote hain.")
add_code("(name, description, price, stock, image, category)")

doc.add_heading("11.2 Adding a Product", level=2)
add_steps([
    "Optimized product image static/uploads folder mein copy karein.",
    "catalog.py ke appropriate category group mein unique product tuple add karein.",
    "Catalog version number increment karein taaki existing database synchronize ho.",
    "Application restart karke products page aur product detail image verify karein.",
    "Cart, checkout aur stock deduction path test karein.",
])

doc.add_heading("11.3 Image Resolution", level=2)
add_body("Templates image string http se start hone par remote URL directly use karte hain; otherwise static/uploads/<filename> build karte hain. Current project majorly local curated image assets use karta hai.")
add_bullets([
    "Recommended web formats: WebP/JPEG for photos, PNG only where transparency needed.",
    "Consistent aspect ratio and compressed files page stability/performance improve karte hain.",
    "Filename database/catalog value se exact match hona chahiye.",
    "Missing images ke liye placeholder strategy maintain karein.",
])

doc.add_heading("11.4 Upload Support", level=2)
add_body("app.py allowed file extensions png, jpg, jpeg aur gif define karta hai aur UPLOAD_FOLDER static/uploads set karta hai. Current main application mein admin/user upload route implemented nahi hai; configuration future upload feature ke liye prepared hai.")

page_break()
doc.add_heading("12. Frontend Design and JavaScript", level=1)
doc.add_heading("12.1 Design System", level=2)
add_body("style.css green botanical visual language, responsive containers, card grids, rounded controls, hover states, commerce layouts, status pills, flash messages aur mobile navigation implement karta hai. Templates Font Awesome icons use karte hain.")
add_bullets([
    "Desktop and mobile navigation with hamburger control.",
    "Responsive product/category grids and commerce cards.",
    "Accessible labels/required attributes on core forms.",
    "Visual feedback through flash messages and notification behavior.",
    "Lazy-loaded imagery in major catalog/category sections where specified.",
])

doc.add_heading("12.2 main.js Responsibilities", level=2)
add_table(["Area", "Behavior"], [
    ("Navigation", "Mobile menu toggle, Escape close, resize cleanup and link-close behavior."),
    ("Search", "Hero/product search navigation and client-side product card filtering."),
    ("Product UI", "Card hover interactions and safe click behavior."),
    ("Forms", "Focus/blur styling and submission feedback."),
    ("Images", "Load/error handling and visual state management."),
    ("Notifications", "Dynamic flash container and dismissible notification helper."),
    ("Scroll", "Header/scroll-dependent interface behavior."),
    ("Currency", "Indian currency formatting helper."),
], [2200, 7160])

doc.add_heading("12.3 Template Inheritance", level=2)
add_body("base.html master layout hai. Page templates Jinja2 extends/block pattern se title aur main content supply karte hain. url_for() static files aur application routes ke URLs generate karta hai, जिससे deployment path changes ke against links maintainable rehte hain.")

page_break()
doc.add_heading("13. Installation and Local Setup", level=1)
doc.add_heading("13.1 Prerequisites", level=2)
add_bullets([
    "Python 3.8 or newer (project guidance); Python 3.10+ recommended.",
    "MySQL Server and optional MySQL Workbench.",
    "Git for source control.",
    "Modern browser such as Chrome, Edge or Firefox.",
])

doc.add_heading("13.2 Setup Procedure (Windows PowerShell)", level=2)
add_steps([
    "Repository folder open karein.",
    "Virtual environment create aur activate karein.",
    "requirements.txt dependencies install karein.",
    "database/schema.sql MySQL mein execute karein.",
    "Ignored config/local.py mein database settings aur strong secret configure karein.",
    "python app.py se server start karein.",
    "Browser mein http://localhost:5000 open karein.",
])
add_code("cd C:\\Users\\ujaga\\OneDrive\\Desktop\\plant-store\npython -m venv venv\n.\\venv\\Scripts\\Activate.ps1\npip install -r requirements.txt\npython app.py")

doc.add_heading("13.3 Database Initialization", level=2)
add_code("mysql -u root -p < database/schema.sql")
add_body("MySQL Workbench alternative: File > Open SQL Script se database/schema.sql open karke complete script execute karein. Script database aur core tables create karta hai. Main app later catalog version synchronization aur payments/schema additions ensure karti hai.")

doc.add_heading("13.4 Dependencies", level=2)
add_table(["Package", "Version/range", "Purpose"], [
    ("Flask", "2.3.0", "Web framework, routing, templates, session and request handling"),
    ("PyMySQL", "1.1.2", "MySQL database client"),
    ("cryptography", ">=43.0.0", "Secure cryptographic support used by dependency stack"),
    ("Werkzeug", "2.3.0", "Password hashing and Flask utilities"),
], [2100, 1800, 5460])

page_break()
doc.add_heading("14. Configuration and Security", level=1)
doc.add_heading("14.1 Configuration Strategy", level=2)
add_body("app.py development defaults define karta hai aur config/local.py ko silent load karta hai. local.py .gitignore se excluded hai, isliye machine-specific database password aur secret Git repository mein commit nahi hone chahiye.")
add_code("MYSQL_HOST = 'localhost'\nMYSQL_USER = '<database-user>'\nMYSQL_PASSWORD = '<strong-password>'\nMYSQL_DB = 'plant_store'\nSECRET_KEY = '<long-random-secret>'")
add_callout("Credential safety", "Documentation real local credentials intentionally include nahi karti. Agar koi secret kabhi public repository/log mein expose hua ho to usse rotate karna chahiye.", fill="FDECEC", color=RED)

doc.add_heading("14.2 Production Hardening Checklist", level=2)
add_bullets([
    "SECRET_KEY environment/secret manager se load karein; development fallback remove karein.",
    "Database user ko least-privilege grants dein; root account use na karein.",
    "CSRF protection, secure cookies (Secure, HttpOnly, SameSite) aur HTTPS enforce karein.",
    "Registration/login rate limiting aur stronger password policy add karein.",
    "Server-side validation phone/address lengths aur allowed payment method whitelist kare.",
    "Stock update ko atomic conditional UPDATE/transaction locking se race-safe banayein.",
    "Real payment gateway use karte waqt server-side signature/webhook verification implement karein.",
    "Public tracking endpoint par additional identity proof aur throttling add karein.",
    "Production WSGI server (Waitress/Gunicorn equivalent) aur reverse proxy use karein.",
    "Centralized logging, backups, monitoring and error reporting configure karein.",
])

doc.add_heading("14.3 Data Handling", level=2)
add_body("Application personal data mein name, email, phone aur delivery address store karti hai. Production operator ko access control, retention/deletion policy, encrypted backups, privacy notice accuracy aur applicable Indian data-protection obligations review karne chahiye.")

page_break()
doc.add_heading("15. Testing and Troubleshooting", level=1)
doc.add_heading("15.1 Recommended Functional Test", level=2)
add_steps([
    "Home page load karein aur nine category links verify karein.",
    "Each category filter mein expected product cards aur images check karein.",
    "New unique email register karke logout/login test karein.",
    "Same product twice add karke quantity increment verify karein.",
    "Quantity update/remove aur cart total verify karein.",
    "Rs.999 threshold ke below/above shipping calculation test karein.",
    "Invalid PIN and missing checkout fields reject hone chahiye.",
    "Demo failed payment par order/stock/cart unchanged verify karein.",
    "Demo successful UPI/card and COD flows separately test karein.",
    "Order history, success page, tracking number and contact form verify karein.",
    "Invalid product/policy/order success paths par 404 behavior check karein.",
    "Mobile viewport mein navigation, filters, forms and cart layout inspect karein.",
])

doc.add_heading("15.2 Troubleshooting Matrix", level=2)
add_table(["Problem", "Likely cause", "Resolution"], [
    ("Cannot connect to MySQL", "Service stopped, wrong credentials/database", "Start MySQL; verify local.py and plant_store schema."),
    ("Module not found", "Environment inactive/dependencies missing", "Activate venv and run pip install -r requirements.txt."),
    ("Image missing", "Filename/path mismatch", "Check static/uploads and catalog/database image value."),
    ("Port 5000 busy", "Another server process", "Stop process or configure a different app.run port."),
    ("Duplicate products", "schema sample data rerun", "Inspect products rows; use catalog sync as canonical source."),
    ("Checkout redirects", "Not logged in, empty cart or missing session checkout", "Login, add item and restart checkout."),
    ("Order not found", "Incorrect number/case or missing committed order", "Copy confirmation number; verify orders table."),
    ("500 error", "Database/schema/runtime exception", "Review terminal logs and confirm schema permissions."),
], [2200, 3200, 3960])

doc.add_heading("15.3 Existing Automated Check", level=2)
add_body("test_categories.py category/catalog behavior check karne ke liye repository mein present hai. Broader automated coverage ke liye pytest fixtures, test database, Flask test client aur transaction rollback-based isolated tests add karne chahiye.")

page_break()
doc.add_heading("16. Known Limitations and Roadmap", level=1)
add_table(["Priority", "Current limitation", "Recommended enhancement"], [
    ("High", "Demo-only payment", "Razorpay/Stripe/PayU sandbox integration with verified webhooks."),
    ("High", "No CSRF protection", "Flask-WTF and CSRF tokens across all state-changing forms."),
    ("High", "Stock race possible", "Atomic inventory update and transaction locking."),
    ("High", "No admin console", "Role-based product, inventory, order and contact management."),
    ("Medium", "Simple client-side search", "Server search, sort, price filter and pagination."),
    ("Medium", "No password reset/email verification", "Token-based email lifecycle."),
    ("Medium", "Public tracking uses order number only", "Email/phone confirmation and rate limiting."),
    ("Medium", "Runtime schema changes", "Alembic/Flask-Migrate versioned migrations."),
    ("Low", "No wishlist/reviews", "Customer engagement features with moderation."),
    ("Low", "Limited SEO/analytics", "Metadata, sitemap, structured data and privacy-aware analytics."),
], [1200, 3500, 4660])

doc.add_heading("Recommended Delivery Phases", level=2)
add_steps([
    "Stabilize: tests, CSRF, secrets, atomic stock, validation and migrations.",
    "Operate: admin dashboard, order states, email notifications, logging and backups.",
    "Transact: real gateway sandbox, webhook reconciliation, refunds and invoice generation.",
    "Grow: search/filter/pagination, wishlist, reviews, SEO and performance optimization.",
])

doc.add_heading("Project Strengths", level=2)
add_bullets([
    "Complete customer shopping journey already demonstrated end-to-end.",
    "Clear separation of templates, static assets, application logic and curated catalog.",
    "Parameterized SQL, password hashing and per-user cart/order ownership checks.",
    "Broad category catalog with local image coverage and responsive storefront.",
    "Catalog/version and schema compatibility logic supports iterative development.",
])

page_break()
doc.add_heading("Appendix A. Folder Structure", level=1)
add_code("plant-store/\n  app.py                    Main Flask application\n  catalog.py                Categories and curated catalog\n  requirements.txt          Python dependencies\n  config/local.py           Local secrets (ignored by Git)\n  database/schema.sql       MySQL schema and seed data\n  templates/                Jinja2 page templates\n  static/css/style.css      Main responsive stylesheet\n  static/js/main.js         Browser interactions/search\n  static/uploads/           Product and marketing images\n  images/                   Source/reference image collection\n  test_categories.py        Catalog/category check\n  README.md                 Project overview\n  SETUP_GUIDE.md            Local setup guidance")

doc.add_heading("Template Inventory", level=2)
add_table(["Template group", "Files"], [
    ("Shared", "base.html, error.html"),
    ("Storefront", "index.html, products.html, product_detail.html"),
    ("Account", "login.html, register.html"),
    ("Commerce", "cart.html, checkout.html, payment.html, order_success.html, orders.html, track_order.html"),
    ("Content/support", "about.html, contact.html, faq.html, policy.html"),
], [2200, 7160])

doc.add_heading("Appendix B. Operational Checklist", level=1)
add_bullets([
    "[ ] MySQL service running and plant_store accessible.",
    "[ ] Local configuration exists and is excluded from Git.",
    "[ ] Strong secret and least-privilege database user configured.",
    "[ ] Dependencies installed in active virtual environment.",
    "[ ] Catalog synchronization completes without errors.",
    "[ ] Product images render without broken links.",
    "[ ] Registration, login, cart and checkout smoke test passes.",
    "[ ] Payment disclaimer remains visible until real gateway is integrated.",
    "[ ] Database backup and restore procedure tested before production changes.",
    "[ ] Debug mode disabled and HTTPS/reverse proxy configured for deployment.",
])

# Prevent widows and keep headings with following content.
for paragraph in doc.paragraphs:
    p_pr = paragraph._p.get_or_add_pPr()
    widow = OxmlElement("w:widowControl")
    p_pr.append(widow)

doc.core_properties.title = "ShreeGanesh Plants-store - Complete Website Documentation"
doc.core_properties.subject = "User manual, functional specification and technical reference"
doc.core_properties.author = "ShreeGanesh Plants-store Project"
doc.core_properties.keywords = "Flask, MySQL, plant store, documentation, e-commerce"
doc.save(OUT)
print(OUT)
