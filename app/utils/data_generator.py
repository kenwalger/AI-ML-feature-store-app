"""Mock data generator for features"""
import random
from typing import List
from app.models.schemas import FeatureCreate


# Sample product categories
CATEGORIES = [
    "Electronics", "Clothing", "Home & Garden", "Sports & Outdoors",
    "Books", "Toys & Games", "Health & Beauty", "Automotive",
    "Food & Beverages", "Office Supplies", "Pet Supplies", "Musical Instruments"
]

# Sample product names by category
PRODUCT_NAMES = {
    "Electronics": [
        "Wireless Bluetooth Headphones", "Smart Watch Pro", "4K Ultra HD Monitor",
        "Portable Power Bank", "USB-C Charging Cable", "Wireless Mouse",
        "Mechanical Keyboard", "Webcam HD", "Tablet Stand", "Laptop Cooling Pad"
    ],
    "Clothing": [
        "Cotton T-Shirt", "Denim Jeans", "Running Shoes", "Winter Jacket",
        "Baseball Cap", "Sunglasses", "Backpack", "Leather Belt",
        "Wool Sweater", "Athletic Shorts"
    ],
    "Home & Garden": [
        "Coffee Maker", "Air Purifier", "LED Desk Lamp", "Plant Pot Set",
        "Kitchen Knife Set", "Throw Pillows", "Wall Clock", "Storage Baskets",
        "Garden Tools", "Indoor Plants"
    ],
    "Sports & Outdoors": [
        "Yoga Mat", "Dumbbell Set", "Bicycle Helmet", "Camping Tent",
        "Water Bottle", "Running Watch", "Tennis Racket", "Basketball",
        "Hiking Boots", "Fitness Tracker"
    ],
    "Books": [
        "Science Fiction Novel", "Cookbook Collection", "History Textbook",
        "Mystery Thriller", "Biography", "Self-Help Guide", "Poetry Collection",
        "Children's Storybook", "Technical Manual", "Art Photography Book"
    ],
    "Toys & Games": [
        "Board Game Set", "Building Blocks", "Puzzle 1000 Pieces", "Action Figure",
        "Remote Control Car", "Card Game", "Educational Toy", "Doll House",
        "Musical Instrument Toy", "Science Kit"
    ],
    "Health & Beauty": [
        "Face Moisturizer", "Shampoo & Conditioner", "Toothbrush Set",
        "Yoga Mat", "Resistance Bands", "Skincare Serum", "Hair Dryer",
        "Electric Razor", "Massage Oil", "Vitamins Supplement"
    ],
    "Automotive": [
        "Car Phone Mount", "Dash Cam", "Car Charger", "Floor Mats",
        "Steering Wheel Cover", "Air Freshener", "Tire Pressure Gauge",
        "Jump Starter", "Car Vacuum", "LED Headlights"
    ],
    "Food & Beverages": [
        "Organic Coffee Beans", "Green Tea Collection", "Protein Bars",
        "Dark Chocolate", "Olive Oil", "Honey Jar", "Spice Set",
        "Granola Mix", "Dried Fruits", "Nuts Variety Pack"
    ],
    "Office Supplies": [
        "Desk Organizer", "Notebook Set", "Pen Collection", "Stapler",
        "File Folders", "Whiteboard", "Desk Calendar", "Paper Clips",
        "Highlighters", "Binder Clips"
    ],
    "Pet Supplies": [
        "Dog Leash", "Cat Scratching Post", "Pet Food Bowl", "Dog Toy",
        "Cat Litter Box", "Pet Bed", "Pet Grooming Brush", "Pet Carrier",
        "Dog Treats", "Fish Tank Filter"
    ],
    "Musical Instruments": [
        "Acoustic Guitar", "Digital Piano", "Violin", "Drum Set",
        "Microphone", "Amplifier", "Ukulele", "Harmonica",
        "Keyboard Stand", "Guitar Strings"
    ]
}

# Sample descriptions templates
DESCRIPTION_TEMPLATES = [
    "High-quality {name} perfect for everyday use. Durable construction and excellent value.",
    "Premium {name} designed for comfort and performance. Ideal for {category} enthusiasts.",
    "Stylish {name} that combines functionality with modern design. Great addition to any collection.",
    "Professional-grade {name} suitable for both beginners and experts. Built to last.",
    "Eco-friendly {name} made from sustainable materials. Perfect for the conscious consumer.",
    "Innovative {name} featuring the latest technology. Experience the difference quality makes.",
    "Versatile {name} that adapts to your needs. A must-have for any {category} collection.",
    "Classic {name} with timeless appeal. Crafted with attention to detail and quality.",
]


def generate_feature(category: str = None) -> FeatureCreate:
    """Generate a single random feature"""
    if category is None:
        category = random.choice(CATEGORIES)
    
    name = random.choice(PRODUCT_NAMES.get(category, ["Generic Product"]))
    description_template = random.choice(DESCRIPTION_TEMPLATES)
    description = description_template.format(name=name, category=category)
    
    # Generate realistic price based on category
    price_ranges = {
        "Electronics": (29.99, 499.99),
        "Clothing": (9.99, 199.99),
        "Home & Garden": (14.99, 299.99),
        "Sports & Outdoors": (19.99, 399.99),
        "Books": (4.99, 49.99),
        "Toys & Games": (9.99, 149.99),
        "Health & Beauty": (7.99, 99.99),
        "Automotive": (12.99, 199.99),
        "Food & Beverages": (5.99, 49.99),
        "Office Supplies": (3.99, 79.99),
        "Pet Supplies": (8.99, 149.99),
        "Musical Instruments": (49.99, 999.99),
    }
    
    min_price, max_price = price_ranges.get(category, (9.99, 99.99))
    price = round(random.uniform(min_price, max_price), 2)
    
    return FeatureCreate(
        name=name,
        description=description,
        category=category,
        price=price
    )


def generate_features(count: int, category: str = None) -> List[FeatureCreate]:
    """Generate multiple random features"""
    features = []
    for _ in range(count):
        features.append(generate_feature(category))
    return features

