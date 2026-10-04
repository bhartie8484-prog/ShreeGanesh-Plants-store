"""Curated product catalogue for every shop category."""

CATEGORIES = [
    'Indoor', 'Outdoor', 'Flowering', 'Herbal', 'Fruit', 'Vegetable',
    'Decorative', 'Hanging', 'Gardening Tools'
]

# name, description, price, stock, local image, category, Wikipedia image lookup
CATALOG_PRODUCTS = [
    ('Aloe Vera Plant', 'Easy-care succulent for a bright indoor window', 349, 18, 'indoor-aloe-vera.jpg', 'Indoor', 'Aloe vera'),
    ('Fiddle Leaf Fig', 'Statement foliage plant for bright indoor corners', 1899, 10, 'indoor-fiddle-leaf.webp', 'Indoor', 'Ficus lyrata'),
    ('Golden Money Plant', 'Golden trailing foliage for shelves and tabletops', 449, 24, 'indoor-golden-money.webp', 'Indoor', 'Epipremnum aureum'),
    ('Money Plant', 'Easy-growing green foliage for indoor rooms', 399, 30, 'indoor-money-plant.jpg', 'Indoor', 'Epipremnum aureum'),
    ('Peace Lily', 'Elegant white blooms for softly lit indoor spaces', 699, 20, 'indoor-peace-lily.jpg', 'Indoor', 'Spathiphyllum'),
    ('Rubber Plant', 'Glossy broad leaves for bright indirect light', 899, 12, 'indoor-rubber.jpeg', 'Indoor', 'Ficus elastica'),
    ('Snake Plant', 'Hardy air-purifying plant for low-light interiors', 499, 25, 'indoor-snake.jpg', 'Indoor', 'Dracaena trifasciata'),
    ('ZZ Plant', 'Glossy low-maintenance foliage for indoor rooms', 799, 22, 'indoor-zz.webp', 'Indoor', 'Zamioculcas'),

    ('Caladium Plant', 'Colourful heart-shaped foliage for shaded outdoor spaces', 549, 18, 'outdoor-caladium.webp', 'Outdoor', 'Caladium'),
    ('Coral Bells Plant', 'Decorative foliage plant for cool garden borders', 599, 16, 'outdoor-coral-bells.jpg', 'Outdoor', 'Heuchera'),
    ('Curry Leaf Plant', 'Aromatic curry leaves for a sunny home garden', 299, 25, 'outdoor-curry-leaf.jpeg', 'Outdoor', 'Murraya koenigii'),
    ('Fern Plant', 'Lush green fronds for shaded patios and gardens', 449, 20, 'outdoor-fern.jpg', 'Outdoor', 'Fern'),
    ('Hosta Plant', 'Broad ornamental leaves for shaded garden beds', 649, 14, 'outdoor-hosta.jpg', 'Outdoor', 'Hosta'),
    ('Lungwort Plant', 'Spotted foliage and delicate blooms for cool shade', 599, 15, 'outdoor-lungwort.jpg', 'Outdoor', 'Pulmonaria'),
    ('Mint Plant', 'Refreshing aromatic herb for outdoor pots', 149, 28, 'outdoor-mint.jpeg', 'Outdoor', 'Mentha spicata'),
    ('Neem Plant', 'Hardy traditional tree for spacious outdoor gardens', 599, 15, 'outdoor-neem.jpeg', 'Outdoor', 'Azadirachta indica'),
    ('Tulsi Plant', 'Sacred aromatic basil for balconies and courtyards', 199, 30, 'outdoor-tulsi.jpeg', 'Outdoor', 'Ocimum tenuiflorum'),

    ('Rose Plant', 'Fragrant classic rose plant for sunny balconies and gardens', 499, 20, 'user-flowering-rose.jpeg', 'Flowering', 'Rose'),
    ('Hibiscus Flower Plant', 'Tropical China rose with large colourful flowers', 399, 18, 'user-flowering-hibiscus.jpeg', 'Flowering', 'Hibiscus rosa-sinensis'),
    ('Jasmine Flower Plant', 'Mogra plant with highly fragrant white flowers', 349, 22, 'user-flowering-jasmine.jpeg', 'Flowering', 'Jasminum sambac'),
    ('African Marigold', 'Bright golden blooms ideal for borders and pots', 199, 30, 'catalog-marigold.jpg', 'Flowering', 'Tagetes erecta'),
    ('Periwinkle Plant', 'Heat-loving plant with long-lasting colourful blooms', 249, 25, 'user-flowering-periwinkle.jpeg', 'Flowering', 'Catharanthus roseus'),
    ('Bougainvillea', 'Sun-loving climber with vibrant papery bracts', 899, 12, 'catalog-bougainvillea.jpg', 'Flowering', 'Bougainvillea'),
    ('Chrysanthemum', 'Seasonal flowering plant with full daisy-like blooms', 299, 20, 'catalog-chrysanthemum.jpg', 'Flowering', 'Chrysanthemum indicum'),
    ('Dahlia Plant', 'Showy garden plant producing large layered flowers', 449, 16, 'catalog-dahlia.jpg', 'Flowering', 'Dahlia'),

    ('Tulsi Plant', 'Holy basil traditionally grown in Indian homes', 199, 30, 'user-herbal-tulsi.jpeg', 'Herbal', 'Ocimum tenuiflorum'),
    ('Mint Plant', 'Refreshing mint for drinks, chutneys and tea', 149, 28, 'user-herbal-mint.jpeg', 'Herbal', 'Mentha spicata'),
    ('Neem Plant', 'Traditional medicinal tree for outdoor gardens', 449, 18, 'user-herbal-neem.jpeg', 'Herbal', 'Azadirachta indica'),
    ('Lemongrass Plant', 'Citrus-scented culinary herb for tea and cooking', 249, 24, 'user-herbal-lemongrass.jpeg', 'Herbal', 'Cymbopogon citratus'),
    ('Oregano Plant', 'Aromatic culinary herb for seasoning', 399, 18, 'user-herbal-oregano.jpeg', 'Herbal', 'Oregano'),
    ('Curry Leaf Plant', 'Fresh aromatic curry leaves for Indian cooking', 299, 25, 'user-herbal-curry-leaf.jpeg', 'Herbal', 'Murraya koenigii'),
    ('Giloy Plant', 'Traditional climbing herbal plant for home gardens', 249, 20, 'user-herbal-giloy.jpeg', 'Herbal', 'Tinospora cordifolia'),
    ('Ashwagandha Plant', 'Traditional Indian medicinal herb for warm climates', 299, 15, 'user-herbal-ashwagandha.jpeg', 'Herbal', 'Withania somnifera'),

    ('Blueberry Fruit Plant', 'Compact berry plant suited to containers', 799, 12, 'user-fruit-blueberry.jpeg', 'Fruit', 'Blueberry'),
    ('Chiku Plant', 'Sapota fruit plant supplied with a grow bag', 699, 15, 'user-fruit-chiku.webp', 'Fruit', 'Manilkara zapota'),
    ('Guava Plant', 'Tropical fruit plant producing aromatic guavas', 699, 15, 'user-fruit-guava.webp', 'Fruit', 'Guava'),
    ('Kesar Mango Plant', 'Popular grafted mango variety for sunny gardens', 999, 10, 'user-fruit-kesar-mango.webp', 'Fruit', 'Mangifera indica'),
    ('Lemon Plant', 'Productive citrus plant supplied with a grow bag', 649, 14, 'user-fruit-lemon.webp', 'Fruit', 'Lemon'),
    ('Orange Fruit Plant', 'Citrus plant for a sunny balcony or garden', 749, 12, 'user-fruit-orange.jpeg', 'Fruit', 'Orange'),
    ('Papaya Fruit Plant', 'Fast-growing tropical plant producing sweet fruit', 499, 18, 'user-fruit-papaya.jpeg', 'Fruit', 'Papaya'),
    ('Pomegranate Plant', 'Sun-loving shrub supplied with a grow bag', 749, 12, 'user-fruit-pomegranate.webp', 'Fruit', 'Pomegranate'),

    ('Tomato Plant', 'Kitchen garden plant producing juicy tomatoes', 199, 25, 'user-vegetable-tomato.jpeg', 'Vegetable', 'Tomato'),
    ('Green Chilli Plant', 'Compact chilli plant for pots and grow bags', 179, 25, 'user-vegetable-chilli.jpeg', 'Vegetable', 'Chili pepper'),
    ('Brinjal Plant', 'Warm-season eggplant for home kitchen gardens', 199, 22, 'user-vegetable-brinjal.jpeg', 'Vegetable', 'Eggplant'),
    ('Okra Plant', 'Productive bhindi plant for sunny warm spaces', 179, 24, 'catalog-okra.jpg', 'Vegetable', 'Okra'),
    ('Cucumber Plant', 'Fast-growing vegetable vine for a support trellis', 199, 20, 'catalog-cucumber.jpg', 'Vegetable', 'Cucumber'),
    ('Capsicum Plant', 'Sweet bell pepper plant for pots and grow bags', 249, 18, 'catalog-capsicum.jpg', 'Vegetable', 'Bell pepper'),
    ('Bitter Gourd Plant', 'Climbing karela vine for a sunny terrace', 199, 20, 'catalog-bitter-gourd.jpg', 'Vegetable', 'Momordica charantia'),
    ('Spinach Plant', 'Quick-growing leafy green for regular harvesting', 149, 30, 'catalog-spinach.jpg', 'Vegetable', 'Spinach'),

    ('Aglaonema Butterfly Plant', 'Colourful low-care foliage for indoor decor', 749, 15, 'user-decorative-aglaonema-butterfly.webp', 'Decorative', 'Aglaonema'),
    ('Aglaonema Ice Plant', 'Silver-green decorative indoor foliage', 799, 14, 'user-decorative-aglaonema-ice.webp', 'Decorative', 'Aglaonema'),
    ('Aglaonema Manila Beauty', 'Large patterned foliage statement plant', 999, 10, 'user-decorative-aglaonema-manila.webp', 'Decorative', 'Aglaonema'),
    ('Croton Plant', 'Colourful decorative foliage in green, yellow and red', 599, 18, 'user-decorative-croton.jpeg', 'Decorative', 'Codiaeum variegatum'),
    ('Ficus Plant', 'Elegant evergreen foliage for bright interiors', 899, 12, 'user-decorative-ficus.jpeg', 'Decorative', 'Ficus'),
    ('Lucky Bamboo 2 Layer', 'Compact two-layer lucky bamboo arrangement', 499, 20, 'user-decorative-bamboo-2-layer.webp', 'Decorative', 'Dracaena sanderiana'),
    ('Lucky Bamboo Pyramid', 'Decorative pyramid-style bamboo arrangement', 699, 16, 'user-decorative-bamboo-pyramid.webp', 'Decorative', 'Dracaena sanderiana'),
    ('Rubber Plant', 'Glossy broad-leaved plant for indoor decor', 899, 12, 'user-decorative-rubber.jpeg', 'Decorative', 'Ficus elastica'),

    ('Boston Fern Hanging Plant', 'Full feathery fronds supplied in a hanging pot', 549, 18, 'user-hanging-boston-fern.jpeg', 'Hanging', 'Nephrolepis exaltata'),
    ('Golden Money Plant', 'Cascading golden leaves for hanging baskets', 399, 30, 'user-hanging-money-golden.webp', 'Hanging', 'Epipremnum aureum'),
    ('Variegated Money Plant', 'Patterned trailing foliage for hanging display', 449, 22, 'user-hanging-money-variegated.webp', 'Hanging', 'Epipremnum aureum'),
    ('Philodendron Broken Heart', 'Split-leaf philodendron supplied in a hanging pot', 649, 14, 'user-hanging-philodendron-broken-heart.webp', 'Hanging', 'Monstera adansonii'),
    ('Philodendron Brasil', 'Striped heart-shaped foliage in a hanging pot', 549, 18, 'user-hanging-philodendron-brasil.webp', 'Hanging', 'Philodendron hederaceum'),
    ('Philodendron Golden', 'Bright golden trailing foliage in a hanging pot', 549, 18, 'user-hanging-philodendron-golden.webp', 'Hanging', 'Philodendron hederaceum'),
    ('Philodendron Hanging Plant', 'Easy-care trailing greenery for indoor spaces', 499, 20, 'user-hanging-philodendron.webp', 'Hanging', 'Philodendron'),
    ('Spider Plant Hanging Pot', 'Arching striped foliage with baby plants', 349, 24, 'user-hanging-spider.jpeg', 'Hanging', 'Chlorophytum comosum'),

    ('Pruner', 'Sharp hand pruner for clean stem cutting', 599, 20, 'user-tool-pruner.jpeg', 'Gardening Tools', 'Pruning shears'),
    ('Spade', 'Sturdy digging spade for beds and borders', 799, 15, 'user-tool-spade.jpeg', 'Gardening Tools', 'Spade'),
    ('Axe', 'Strong garden axe for woody branches', 899, 12, 'user-tool-axe.jpeg', 'Gardening Tools', 'Axe'),
    ('Hoe', 'Reliable hoe for loosening soil and weeding', 649, 18, 'user-tool-hoe.jpeg', 'Gardening Tools', 'Hoe (tool)'),
    ('Rake', 'Durable rake for levelling soil and clearing leaves', 749, 14, 'user-tool-rake.jpeg', 'Gardening Tools', 'Rake (tool)'),
    ('Watering Can', 'Balanced watering can for pots and garden beds', 499, 24, 'user-tool-watering-can.jpeg', 'Gardening Tools', 'Watering can'),
    ('Scissor', 'Handy garden scissor for light trimming', 399, 22, 'user-tool-scissor.jpeg', 'Gardening Tools', 'Pruning shears'),
    ('Gloves', 'Protective reusable gloves for soil and plant care', 249, 35, 'user-tool-gloves.jpeg', 'Gardening Tools', 'Garden glove'),
    ('Sickle', 'Curved hand tool for cutting grass and light harvesting', 449, 18, 'user-tool-sickle.jpeg', 'Gardening Tools', 'Sickle'),
    ('Trowel', 'Compact hand trowel for potting and transplanting', 299, 28, 'user-tool-trowel.jpeg', 'Gardening Tools', 'Trowel'),
    ('Hedge Shears', 'Long-blade shears for shaping hedges and shrubs', 999, 10, 'user-tool-hedge-shears.jpeg', 'Gardening Tools', 'Hedge shears'),
]

def db_products():
    """Return the six database fields used by the products table."""
    return [product[:6] for product in CATALOG_PRODUCTS]
