# 🆔 Aadhaar Data Extraction System

A **Flask and React-based** system for **Aadhaar card data extraction and validation** using **OCR (EasyOCR)** and **MongoDB** for data storage.

---

## 🚀 Features

✅ **Aadhaar Data Extraction** - Extracts **Name, DOB, and Aadhaar Number** using OCR.  
✅ **Preprocessing** - Uses **CLAHE** for image enhancement to improve OCR accuracy.  
✅ **Duplicate Detection** - Prevents duplicate Aadhaar registration using **MongoDB**.  
✅ **REST API** - Exposes a **Flask API** for Aadhaar extraction and validation.  
✅ **React Frontend** - User-friendly interface for uploading Aadhaar images.  
✅ **CORS Enabled** - Allows communication between React frontend and Flask backend.  

---

## 🛠️ Technologies Used

### 📌 Backend (Flask)
- **Flask** - Python web framework  
- **EasyOCR** - Optical Character Recognition (OCR)  
- **OpenCV (cv2)** - Image preprocessing  
- **Pymongo** - MongoDB integration  
- **Regex (re)** - Data extraction patterns  
- **Flask-CORS** - Handles CORS for frontend-backend communication  

### 📌 Frontend (React)
- **React.js** - UI for Aadhaar verification  
- **Axios** - API requests  
- **Bootstrap / Tailwind (Optional)** - Styling  
- **File Upload Handling** - Allows users to submit Aadhaar images  

### 📌 Database
- **MongoDB** - Stores Aadhaar records  

---


