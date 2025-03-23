from flask import Flask, request, jsonify
import easyocr
import cv2
import re
import numpy as np
import os
import logging
from pymongo import MongoClient
from bson import ObjectId 
from flask_cors import CORS
app = Flask(__name__)
CORS(app) 
# MongoDB configuration
app.config['MONGO_URI'] = 'mongodb://localhost:27017/KINJALVOTINGSYSTEM'
client = MongoClient(app.config['MONGO_URI'])
db = client['KINJALVOTINGSYSTEM']
aadhaar_collection = db['aadhaar_records']

# Setup logging
# logging.basicConfig(level=logging.DEBUG)

def preprocess_image(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(10,8))
    enhanced = clahe.apply(gray)
    return enhanced

def score_name_candidate(name):
    score = 0
    if all(word.isalpha() for word in name.split()):
        score += 3
    if not any(c * 3 in name for c in name):
        score += 2
    common_endings = ['KUMAR', 'LAL', 'SINGH', 'RAJ', 'WARI', 'HARI']
    if any(name.endswith(end) for end in common_endings):
        score += 2
    unusual_combinations = ['HH', 'JJ', 'KK', 'XX', 'ZZ']
    if any(combo in name for combo in unusual_combinations):
        score -= 2
    return score

def extract_aadhar_info(image_path):
    reader = easyocr.Reader(['en'])
    processed_img = preprocess_image(image_path)
    results = reader.readtext(processed_img, detail=0, paragraph=False)
    full_text = ' '.join(results).upper()
    info = {"Name": None, "DOB": None, "Aadhaar Number": None}
    words = full_text.split()
    name_candidates = []
    for i in range(len(words) - 1):
        word1, word2 = words[i], words[i+1]
        if len(word1) >= 3 and len(word2) >= 3:
            replacements = {'1': 'I', '3': 'E', '4': 'A', '5': 'S', '7': 'T', '0': 'O', '$': 'S', '8': 'B'}
            clean_word1 = ''.join(replacements.get(c, c) for c in word1)
            clean_word2 = ''.join(replacements.get(c, c) for c in word2)
            common_words = {'GOVERNMENT', 'INDIA', 'MALE', 'FEMALE', 'ADDRESS', 'AADHAAR'}
            if clean_word1 not in common_words and clean_word2 not in common_words:
                candidate = f"{clean_word1} {clean_word2}"
                score = score_name_candidate(candidate)
                name_candidates.append((candidate, score))
    if name_candidates:
        name_candidates.sort(key=lambda x: x[1], reverse=True)
        info["Name"] = name_candidates[0][0].title()
    dob_match = re.search(r'DOB.*?(\d{2}/\d{2}/\d{4})', full_text)
    if dob_match:
        info["DOB"] = dob_match.group(1)
    aadhaar_match = re.search(r'\b(\d{4}\s?\d{4}\s?\d{4})\b', full_text)
    if aadhaar_match:
        raw_num = aadhaar_match.group(1).replace(' ', '')
        info["Aadhaar Number"] = f"{raw_num[:4]} {raw_num[4:8]} {raw_num[8:12]}"
    return info

@app.route('/extract-aadhaar', methods=['POST'])
def extract_aadhaar_api():
    # logging.debug("API called")
    if '' not in request.files:
        # logging.error("No file uploaded")
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files['']
    file_path = "temp.jpg"
    file.save(file_path)
    user_id = request.form['userId']
    user_id = ObjectId(user_id)
    # logging.debug(f"File saved to {file_path}")
    result = extract_aadhar_info(file_path)
    os.remove(file_path)
    # logging.debug(f"Extracted info: {result}")
    
    if result["Aadhaar Number"]:
        existing_record = aadhaar_collection.find_one({"aadhaar_number": result["Aadhaar Number"]})
        if existing_record:
            # logging.info("Aadhaar ID already registered")
            return jsonify({"message": "This Aadhaar ID is already registered.", "status": "exists"}), 201
        
        new_record = {
            "user_id": user_id,
            "aadhaar_number": result["Aadhaar Number"],
            "name": result["Name"],
            "dob": result["DOB"]
        }
        aadhaar_collection.insert_one(new_record)
        # logging.info("Aadhaar ID successfully registered")
        return jsonify({"message": "Aadhaar ID successfully registered.", "status": "success"}), 201
    
    # logging.error("Aadhaar number could not be extracted")
    return jsonify({"error": "Aadhaar number could not be extracted."}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 
