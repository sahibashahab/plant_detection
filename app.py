from flask import Flask, request, render_template, redirect, url_for
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os
app = Flask(__name__)


model = load_model('model\model.h5')


plant_info = {
   
    'aloevera': {
        'description': 'Aloe Vera is known for its soothing properties and is often used in skin care products.',
        'uses': ['Skin treatment', 'Burn relief', 'Digestive aid'],
        'benefits': ['Soothes skin irritations', 'Promotes healing', 'Aids in digestion']
    },
    'banana': {
        'description': 'Banana is a tropical fruit that is rich in potassium and is a great source of energy.',
        'uses': ['Food', 'Natural sweetener', 'Fiber source'],
        'benefits': ['High in potassium', 'Aids in digestion', 'Energy booster']
    },
    'bilimbi': {
        'description': 'Bilimbi is a tropical fruit known for its sour taste, often used in cooking and traditional medicine.',
        'uses': ['Culinary ingredient', 'Natural remedy for cough', 'Pickling'],
        'benefits': ['Rich in vitamin C', 'Anti-inflammatory properties', 'Aids in weight loss']
    },
    'cantaloupe': {
        'description': 'Cantaloupe is a refreshing melon with a sweet flavor, rich in vitamins and minerals.',
        'uses': ['Fruit salads', 'Smoothies', 'Desserts'],
        'benefits': ['High in vitamin A and C', 'Supports immune health', 'Hydration']
    },
    'cassava': {
        'description': 'Cassava is a starchy root vegetable that is a staple food in many tropical regions.',
        'uses': ['Staple food', 'Tapioca production', 'Gluten-free flour'],
        'benefits': ['Rich in carbohydrates', 'Gluten-free', 'Source of fiber']
    },
    'coconut': {
        'description': 'Coconut is a versatile fruit used for its water, milk, oil, and flesh.',
        'uses': ['Cooking', 'Beverage', 'Cosmetics'],
        'benefits': ['Hydrates and refreshes', 'Rich in healthy fats', 'Antioxidant properties']
    },
    'corn': {
        'description': 'Corn is a cereal grain that is a major food source worldwide, used in many culinary dishes.',
        'uses': ['Food', 'Cornmeal', 'Biofuel production'],
        'benefits': ['Rich in fiber', 'Contains essential vitamins', 'Provides energy']
    },
    'cucumber': {
        'description': 'Cucumber is a cool and refreshing vegetable often used in salads and skin care.',
        'uses': ['Salads', 'Skin care', 'Pickling'],
        'benefits': ['Hydrates the body', 'Promotes digestion', 'Anti-inflammatory']
    },
    'curcuma': {
        'description': 'Curcuma, also known as turmeric, is a spice with potent anti-inflammatory properties.',
        'uses': ['Spice in cooking', 'Natural dye', 'Traditional medicine'],
        'benefits': ['Anti-inflammatory', 'Antioxidant', 'Supports joint health']
    },
    'eggplant': {
        'description': 'Eggplant is a versatile vegetable used in various cuisines, known for its rich flavor and texture.',
        'uses': ['Culinary ingredient', 'Grilled dishes', 'Curries'],
        'benefits': ['Rich in fiber', 'Supports heart health', 'Low in calories']
    },
    'galangal': {
        'description': 'Galangal is a spice similar to ginger, used in Southeast Asian cooking for its pungent flavor.',
        'uses': ['Spice in cooking', 'Traditional medicine', 'Aromatherapy'],
        'benefits': ['Aids digestion', 'Anti-inflammatory', 'Boosts immunity']
    },
    'ginger': {
        'description': 'Ginger is a popular spice known for its medicinal properties, often used to treat nausea and inflammation.',
        'uses': ['Culinary ingredient', 'Herbal tea', 'Natural remedy'],
        'benefits': ['Relieves nausea', 'Anti-inflammatory', 'Boosts immunity']
    },
    'guava': {
        'description': 'Guava is a tropical fruit rich in dietary fiber, vitamin C, and antioxidants.',
        'uses': ['Fruit juice', 'Culinary ingredient', 'Natural remedy'],
        'benefits': ['Boosts immunity', 'Supports heart health', 'Rich in fiber']
    },
    'kale': {
        'description': 'Kale is a leafy green vegetable known for its high nutrient content, including vitamins A, C, and K.',
        'uses': ['Salads', 'Smoothies', 'Soups'],
        'benefits': ['Rich in vitamins', 'Supports bone health', 'Detoxifies the body']
    },
    'longbeans': {
        'description': 'Long beans are a type of legume known for their long, slender pods, used in various Asian dishes.',
        'uses': ['Stir-fries', 'Salads', 'Curries'],
        'benefits': ['Rich in fiber', 'Source of protein', 'Supports digestion']
    },
    'mango': {
        'description': 'Mango is a sweet tropical fruit known for its juicy flesh and vibrant flavor.',
        'uses': ['Fruit salads', 'Smoothies', 'Desserts'],
        'benefits': ['Rich in vitamin C', 'Supports eye health', 'Boosts immunity']
    },
    'melon': {
        'description': 'Melon is a refreshing fruit with a sweet flavor, often enjoyed in salads and as a dessert.',
        'uses': ['Fruit salads', 'Smoothies', 'Desserts'],
        'benefits': ['Hydrating', 'Rich in vitamins A and C', 'Supports digestion']
    },
    'orange': {
        'description': 'Orange is a citrus fruit known for its high vitamin C content and refreshing taste.',
        'uses': ['Juice', 'Culinary ingredient', 'Natural remedy'],
        'benefits': ['Boosts immunity', 'Rich in antioxidants', 'Promotes skin health']
    },
    'paddy': {
        'description': 'Paddy, or rice, is a staple food crop grown in flooded fields, known for its versatility in cooking.',
        'uses': ['Staple food', 'Rice flour', 'Culinary ingredient'],
        'benefits': ['Rich in carbohydrates', 'Gluten-free', 'Provides energy']
    },
    'papaya': {
        'description': 'Papaya is a tropical fruit known for its sweet taste and vibrant orange flesh, rich in enzymes.',
        'uses': ['Fruit salads', 'Smoothies', 'Natural remedy'],
        'benefits': ['Aids digestion', 'Rich in vitamin C', 'Supports skin health']
    },
    'peper chili': {
        'description': 'Pepper chili is a spicy fruit used in cooking for its heat and flavor, commonly found in various cuisines.',
        'uses': ['Spice in cooking', 'Sauces', 'Pickling'],
        'benefits': ['Boosts metabolism', 'Rich in vitamins A and C', 'Anti-inflammatory']
    },
    'pineapple': {
        'description': 'Pineapple is a tropical fruit known for its sweet and tangy flavor, often used in desserts and drinks.',
        'uses': ['Fruit salads', 'Smoothies', 'Culinary ingredient'],
        'benefits': ['Rich in vitamin C', 'Supports digestion', 'Anti-inflammatory']
    },
    'pomelo': {
        'description': 'Pomelo is a large citrus fruit with a sweet and tangy flavor, often enjoyed as a fresh fruit or in salads.',
        'uses': ['Fruit salads', 'Juice', 'Culinary ingredient'],
        'benefits': ['Rich in vitamin C', 'Supports digestion', 'Boosts immunity']
    },
    'shallot': {
        'description': 'Shallot is a type of onion known for its mild flavor, often used in gourmet cooking and salads.',
        'uses': ['Culinary ingredient', 'Salads', 'Pickling'],
        'benefits': ['Rich in antioxidants', 'Supports heart health', 'Anti-inflammatory']
    },
    'soybeans': {
        'description': 'Soybeans are a versatile legume used in various products like tofu, soy milk, and soy sauce.',
        'uses': ['Tofu production', 'Soy milk', 'Culinary ingredient'],
        'benefits': ['High in protein', 'Rich in fiber', 'Supports heart health']
    },
    'spinach': {
        'description': 'Spinach is a leafy green vegetable known for its high nutrient content, particularly iron and calcium.',
        'uses': ['Salads', 'Smoothies', 'Culinary ingredient'],
        'benefits': ['Rich in iron', 'Supports bone health', 'Antioxidant properties']
    },
    'sweet potatoes': {
        'description': 'Sweet potatoes are a starchy root vegetable known for their sweet taste and rich nutrient profile.',
        'uses': ['Baking', 'Culinary ingredient', 'Snacks'],
        'benefits': ['Rich in vitamins A and C', 'Supports eye health', 'Boosts immunity']
    },
    'tobacco': {
        'description': 'Tobacco is a plant whose leaves are used in the production of cigarettes and other tobacco products.',
        'uses': ['Cigarette production', 'Chewing tobacco', 'Traditional medicine'],
        'benefits': ['Used in traditional practices', 'Contains nicotine', 'Economic crop']
    },
    'waterapple': {
        'description': 'Water apple is a tropical fruit with a crisp texture and mildly sweet flavor, often eaten fresh.',
        'uses': ['Fresh fruit', 'Culinary ingredient', 'Salads'],
        'benefits': ['Hydrating', 'Rich in vitamins', 'Supports digestion']
    },
    'watermelon': {
        'description': 'Watermelon is a juicy and refreshing fruit with a high water content, perfect for hydration.',
        'uses': ['Fruit salads', 'Smoothies', 'Snacks'],
        'benefits': ['Hydrating', 'Rich in vitamins A and C', 'Supports heart health']
    }
}



plant_labels = ['aloevera', 'banana', 'bilimbi', 'cantaloupe', 'cassava', 'coconut', 'corn', 'cucumber', 'curcuma', 'eggplant', 'galangal', 'ginger', 'guava', 'kale', 'longbeans', 'mango', 'melon', 'orange', 'paddy', 'papaya', 'peper chili', 'pineapple', 'pomelo', 'shallot', 'soybeans', 'spinach', 'sweet potatoes', 'tobacco', 'waterapple', 'watermelon']

def load_and_prepare_image(img_path):
    img = image.load_img(img_path, target_size=(48, 48))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0
    return img_array

def predict_plant(img_path):
    img = load_and_prepare_image(img_path)
    prediction = model.predict(img)
    predicted_class = np.argmax(prediction[0])
    return plant_labels[predicted_class]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
      
        if not os.path.exists('uploads'):
            os.makedirs('uploads')

     
        file = request.files['image']
        if file:
          
            file_path = os.path.join('uploads', file.filename)
            file.save(file_path)

            
            plant_label = predict_plant(file_path)

            
            plant_details = plant_info.get(plant_label, None)

            return render_template('result.html', plant_label=plant_label, plant_details=plant_details)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)