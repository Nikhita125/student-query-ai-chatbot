# Student Query AI Chatbot System

An AI-powered chatbot that helps students get answers to common college-related questions using Natural Language Processing and Machine Learning.

## Key Highlights

- AI-powered student query classification
- NLP-based text processing
- TF-IDF feature extraction
- Logistic Regression machine learning model
- Confidence-based response handling
- Student login and registration
- Secure password hashing
- SQLite database integration
- Chat history tracking
- Admin dashboard
- FAQ management
- Admin-only access control

## Features

- Student Registration and Login
- AI-based Question Classification
- TF-IDF Text Vectorization
- Logistic Regression
- FAQ Management
- Chat History
- Admin Dashboard
- SQLite Database

## Technologies Used

- Python
- Flask
- Machine Learning
- NLP
- HTML
- CSS
- JavaScript
- SQLite
- Scikit-learn

## Key Highlights

- Uses Machine Learning for student question classification
- Uses TF-IDF for text feature extraction
- Uses Logistic Regression for intent prediction
- Stores users and chat history using SQLite
- Provides FAQ management for administrators
- Provides an Admin Dashboard to monitor student queries
- Supports multiple college-related student queries

## Project Architecture

Student
↓
Web Interface
↓
Flask Backend
↓
NLP Processing
↓
TF-IDF Vectorization
↓
Logistic Regression
↓
Intent Detection
↓
FAQ / Database
↓
Answer to Student

## Project Structure

- `app.py` – Flask application and web routes
- `train_model.py` – Trains the machine learning model
- `chatbot.py` – Chatbot prediction and responses
- `database.py` – SQLite database setup
- `dataset/` – Training dataset
- `model/` – Trained ML model
- `templates/` – HTML pages
- `static/` – CSS and JavaScript files

## How AI Works

Student Question
↓
TF-IDF
↓
Logistic Regression
↓
Intent Detection
↓
Answer

## Main Queries

- Exams
- Courses
- College Timing
- Library
- Hostel
- Fees
- Attendance
- Placements

## How to Run

Install the required packages:

```bash
pip install -r requirements.txt