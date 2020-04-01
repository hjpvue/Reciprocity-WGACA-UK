import anvil.microsoft.auth
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.facebook.auth
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import datetime

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#
@anvil.server.callable
def save_to_database(product_key, units, expiry_date, notes):
    """ Returns 'Duplicate' if product_key/expiry date row already exists"""
    product_key = " … ".join(product_key)
    user = anvil.users.get_user()
    if user is None:
        return
    existing_entry = app_tables.offers.get(product_key=product_key, expiry_date=expiry_date, user = user)
    if existing_entry:
        return "Duplicate"    
    app_tables.offers.add_row(status='New',product_key=product_key, notes = str(notes), expiry_date = expiry_date, units=units, user=user, date_posted=datetime.datetime.today().date())

@anvil.server.callable
def get_my_offers():
    user = anvil.users.get_user()
    if user is not None:
        return app_tables.offers.search(tables.order_by("product_key"), user = user)

@anvil.server.callable
def get_units_of_measure():
    return """grammes
kilogrammes
millilitres
centilitres
litres
bags (small)
bags (medium)
bags (large)
bottles (small)
bottles (medium)
bottles (large)
boxes (small)
boxes (medium)
boxes (large)
cans (small)
cans (medium)
cans (large)
items (small)
items (medium)
items (large)
packets (small)
packets (medium)
packets (large)
tins (small)
tins (medium)
tins (large)"""     
      
@anvil.server.callable
def get_product_heirarchy():
    return """Drink | Water | Mineral Water (sparkling)
Drink | Water | Mineral Water (still)
Drink | Fruit Juice | Apple Juice
Drink | Fruit Juice | Orange Juice
Drink | Fruit Juice | Other
Drink | Carbonated | Coca Cola, Pepsi etc.
Drink | Carbonated | Tango, Fanta etc.
Drink | Carbonated | Ginger Beer
Drink | Carbonated | Red Bull, Monster etc.
Drink | Milk | Skimmed / Semi-skimmed
Drink | Milk | Half-fat / Full-fat
Drink | Milk | Flavoured Milk
Drink | Milk | Coconut / Soya etc.
Drink | Milk | Iced Coffee
Food | Vegetables | Asparagus
Food | Vegetables | Aubergine
Food | Vegetables | Broccoli
Food | Vegetables | Carrots
Food | Vegetables | Cauliflower
Food | Vegetables | Celery
Food | Vegetables | Courgette
Food | Vegetables | Cucumbers
Food | Vegetables | Lettuce / Greens
Food | Vegetables | Mushrooms
Food | Vegetables | Onions
Food | Vegetables | Peppers
Food | Vegetables | Plantain
Food | Vegetables | Potatoes
Food | Vegetables | Spinach
Food | Vegetables | Squash
Food | Vegetables | Sweetcorn
Food | Vegetables | Tomatoes
Food | Fruits | Apples
Food | Fruits | Avocados
Food | Fruits | Bananas
Food | Fruits | Blueberries
Food | Fruits | Cherries
Food | Fruits | Grapefruit
Food | Fruits | Grapes
Food | Fruits | Kiwis
Food | Fruits | Lemons / Limes
Food | Fruits | Melon
Food | Fruits | Nectarines
Food | Fruits | Oranges
Food | Fruits | Peaches
Food | Fruits | Pears
Food | Fruits | Plums
Food | Fruits | Raspberries
Food | Fruits | Strawberries
Food | Dairy | Butter
Food | Dairy | Margarine
Food | Dairy | Milk - Skimmed
Food | Dairy | Milk - Semi Skimmed
Food | Dairy | Milk - Full Fat
Food | Dairy | Milk - Almond
Food | Dairy | Milk - Coconut
Food | Dairy | Milk - Oat
Food | Dairy | Milk - Soya
Food | Dairy | Single Cream
Food | Dairy | Double Cream
Food | Dairy | Sour Cream
Food | Dairy | Whipped Cream
Food | Dairy | Yogurt
Food | Cheese | Soft e.g. Brie, Camembert
Food | Cheese | Hard e.g. Cheddar, Red Leicester
Food | Cheese | Spreadable e.g. Cottage Cheese, Cream Cheese
Food | Cheese | Goat
Food | Cheese | Sandwich Slices
Food | Cheese | Veined e.g. Stilton
Food | Cheese | Other
Food | Meat | Bacon
Food | Meat | Beef - Minced
Food | Meat | Beef - Diced
Food | Meat | Beef - Joint
Food | Meat | Beef - Steak
Food | Meat | Chicken - Breast
Food | Meat | Chicken - Thighs
Food | Meat | Chicken - Wings
Food | Meat | Chicken - Diced
Food | Meat | Ham - Sliced
Food | Meat | Ham - Gammon Joint
Food | Meat | Lamb - Minced
Food | Meat | Lamb - Diced
Food | Meat | Lamb - Chops
Food | Meat | Lamb - Joint
Food | Meat | Pork - Diced
Food | Meat | Pork - Chops
Food | Meat | Pork - Joint
Food | Meat | Sausages
Food | Meat | Hot Dogs
Food | Seafood | Crab
Food | Seafood | Lobster
Food | Seafood | Mackerel
Food | Seafood | Mussels
Food | Seafood | Oysters
Food | Seafood | Salmon
Food | Seafood | Seabass
Food | Seafood | Shrimp/Prawns
Food | Seafood | Trout
Food | Seafood | Tuna - Steak
Food | Seafood | Tuna - Tinned
Food | Frozen | Ice-Cream
Food | Frozen | Peas
Food | Frozen | Carrots
Food | Frozen | Sweetcorn
Food | Frozen | Mushrooms
Food | Frozen | Cauliflower
Food | Frozen | Broccoli
Food | Frozen | Mixed Veg
Food | Frozen | Pizza
Food | Bread | White Sliced
Food | Bread | Brown Sliced
Food | Bread | Seeded Sliced
Food | Bread | Granary Sliced
Food | Bread | Wholemeal Sliced
Food | Bread | White 
Food | Bread | Wholemeal
Food | Bread | Granary
Food | Bread | Seeded  
Food | Bread | Brown  
Food | Bread | Tiger Loaf
Food | Bread | Giraffe Loaf
Food | Bread | Bagels
Food | Bread | Crumpets
Food | Bread | English Muffins
Food | Bread | Pastries
Food | Bread | Cake
Food | Bread | Pitta Bread
Food | Bread | Tortilla Wraps
Food | Bread | Hot Cross Buns
Food | Bread | Malt Loaf
Food | Bread | Waffles
Food | Bread | Rolls
Food | Pantry | Tinned Tomatoes
Food | Pantry | Tinned Sweetcorn
Food | Pantry | Tinned Carrots
Food | Pantry | Tinned Potatoes
Food | Pantry | Tinned Kidney Beans
Food | Pantry | Baked Beans
Food | Pantry | Soup
Food | Pantry | Bouillon Cubes
Food | Pantry | Cereal
Food | Pantry | Coffee / Filters
Food | Pantry | Instant Potatoes
Food | Pantry | Lemon / Lime Juice
Food | Pantry | Gravy Granules
Food | Pantry | Olive Oil
Food | Pantry | Pasta
Food | Pantry | Peanut Butter
Food | Pantry | Jam
Food | Pantry | Marmalade
Food | Pantry | Marmite
Food | Pantry | Pickle
Food | Pantry | Rice
Food | Pantry | Tea
Food | Pantry | Vegetable Oil
Food | Pantry | Vinegar
Food | Pantry | Tinned Corn Beef
Food | Pantry | Tinned Pies
Food | Pantry | Sauces - Tomato
Food | Pantry | Sauces - Mayonaise
Food | Pantry | Sauces - Mustard
Food | Pantry | Sauces - Hot Sauce
Food | Pantry | Sauces - Soy
Food | Pantry | Sauces - Pasta
Food | Pantry | Sauces - Pesto
Food | Pantry | Sauces Worcestershire
Food | Pantry | Sauces - Salsa
Food | Pantry | Sauces - Curry
Food | Pantry | Self- Raising Flour
Food | Pantry | Plain Flour
Food | Pantry | Corn Flour
Food | Pantry | Yeast
Food | Pantry | Strong Bread Flour
Food | Pantry | Baking Powder
Food | Pantry | Bicarbonate Of Soda
Food | Pantry | Sugar - Castor
Food | Pantry | Sugar - Granulated
Food | Pantry | Sugar - Golden
Food | Pantry | Sugar - Dark Muscovado
Food | Pantry | Crisps
Food | Pantry | Basil
Food | Pantry | Black Pepper
Food | Pantry | Cinnamon
Food | Pantry | Garlic
Food | Pantry | Ginger
Food | Pantry | Mint
Food | Pantry | Mixed Spice
Food | Pantry | Oregano
Food | Pantry | Paprika
Food | Pantry | Parsley
Food | Pantry | Turmeric
Food | Pantry | Salt
Food | Pantry | Vanilla Extract
Food | Pantry | Aluminum Foil
Food | Pantry | Napkins
Food | Pantry | Non-Stick Spray
Food | Pantry | Paper Towels
Food | Pantry | Plastic Wrap
Food | Pantry | Sandwich / Freezer Bags
Food | Pantry | Wax Paper
Pets | Store | Cat Food / Treats
Pets | Store | Cat Litter
Pets | Store | Dog Food / Treats
Pets | Store | Flea Treatment
Household | Personal Care | Antiperspirant / Deodorant
Household | Personal Care | Bath Soap / Hand Soap
Household | Personal Care | Condoms / Other B.C.
Household | Personal Care | Cosmetics
Household | Personal Care | Cotton Swabs / Balls
Household | Personal Care | Facial Cleanser
Household | Personal Care | Facial Tissue
Household | Personal Care | Feminine Products
Household | Personal Care | Floss
Household | Personal Care | Hair Gel / Spray
Household | Personal Care | Lip Balm
Household | Personal Care | Moisturizing Lotion
Household | Personal Care | Mouthwash
Household | Personal Care | Razors / Shaving Cream
Household | Personal Care | Shampoo / Conditioner
Household | Personal Care | Sunblock
Household | Personal Care | Toilet Paper
Household | Personal Care | Toothpaste
Household | Personal Care | Vitamins / Supplements
Household | Baby | Nappies
Household | Baby | Nappy Bags
Household | Baby | Formula
Household | Baby | Baby Lotion
Household | Baby | Baby Wipes
Household | Baby | Baby Oil
Household | Baby | Shampoo  
Household | Baby | Cotton Wool
Household | Baby | Cotton Buds
Household | Cleaning Products | Air Freshener
Household | Cleaning Products | Bathroom Cleaner
Household | Cleaning Products | Bleach / Detergent
Household | Cleaning Products | Dettol
Household | Cleaning Products | Dish / Dishwasher Soap
Household | Cleaning Products | Garbage Bags
Household | Cleaning Products | Glass Cleaner
Household | Cleaning Products | Kitchen Cleaner
Household | Cleaning Products | Mop Head / Vacuum Bags
Household | Cleaning Products | Sponges / Scrubbers
Household | Cleaning Products | Toilet Cleaner
Household | Cleaning Products | Washing - Powder
Household | Cleaning Products | Washing  - Liquid
Household | Cleaning Products | Fabric Softner
Medicine | Allergy
Medicine | Antidiarrheal
Medicine | Antiseptic Cream
Medicine | Aspirin
Medicine | Antacid
Medicine | Cold / Flu / Sinus
Medicine | Ibuprofen
Medicine | Paracetamol
Medicine | Paracetamol - Soluble
Medicine | Plasters"""