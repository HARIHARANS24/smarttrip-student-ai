# ✈️ AI-Powered Student Travel Planner

<div align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.11+-blue.svg" />
  <img alt="Streamlit" src="https://img.shields.io/badge/Streamlit-1.31.0-FF4B4B.svg" />
  <img alt="Google Gemini" src="https://img.shields.io/badge/Google%20Gemini-AI-orange.svg" />
  <img alt="SQLAlchemy" src="https://img.shields.io/badge/SQLAlchemy-2.0.25-red.svg" />
  <img alt="Docker" src="https://img.shields.io/badge/Docker-Supported-2496ED.svg" />
</div>

<br/>

**AI-Powered Student Travel Planner** is a comprehensive, production-ready web application designed specifically for students. It leverages the power of **Google Gemini AI** to curate affordable, personalized, and highly detailed travel itineraries, recommendations, and budgets based on individual academic schedules, preferences, and financial constraints.

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Project Architecture](#-project-architecture)
- [Prerequisites](#-prerequisites)
- [Installation & Setup](#-installation--setup)
- [Docker Deployment](#-docker-deployment)
- [Usage Guide](#-usage-guide)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🔍 Overview

Planning a trip as a student often involves balancing tight budgets, academic schedules, and the desire for memorable experiences. This platform simplifies the process by integrating an AI-driven approach. From selecting a destination to managing daily expenses, the application provides an end-to-end travel planning ecosystem.

## ✨ Key Features

- 🔐 **User Authentication**: Secure signup and login mechanisms using `bcrypt` password hashing.
- 👤 **Student Profiles**: Manage personal information, academic calendars, and granular travel preferences.
- 🎯 **Preference Assessment**: An interactive questionnaire to tailor the AI's understanding of your travel style.
- 🌍 **AI Destination Recommender**: Intelligent suggestions based on budget constraints, seasonal factors, and travel styles.
- 🗺️ **AI Trip Planner**: Auto-generated, detailed day-by-day itineraries encompassing activities, transport, and estimated costs.
- 💰 **AI Budget Planner**: Granular budget breakdowns across various expense categories (accommodation, food, transport, leisure).
- 🧾 **Expense Tracker**: Keep a real-time log of your spending during the trip.
- 📈 **Analytics Dashboard**: Visual representations (via Plotly) comparing planned budgets against actual expenditures.
- 🤖 **AI Travel Chatbot**: A conversational AI assistant to answer on-the-go travel queries and provide localized tips.
- 📄 **PDF Report Generation**: Export your finalized travel plans, itineraries, and budgets as cleanly formatted PDF documents.

---

## 🛠️ Tech Stack

- **Frontend & UI Framework**: [Streamlit](https://streamlit.io/)
- **Programming Language**: Python 3.11+
- **AI & LLM Integration**: Google Generative AI (Gemini)
- **Database & ORM**: SQLite, SQLAlchemy
- **Data Visualization**: Pandas, Plotly
- **Authentication**: Bcrypt
- **Document Generation**: FPDF2
- **Containerization**: Docker

---

## 📁 Project Architecture

```text
AI-Powered Student Travel Planner/
├── app.py                      # Main application entry point
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker configuration
├── .env.example                # Example environment variables
├── database/                   # DB connection & models
├── pages/                      # Streamlit application pages
│   ├── analytics.py            # Budget & expense charts
│   ├── assessment.py           # Travel preference questionnaire
│   ├── budget.py               # AI budget generation
│   ├── chatbot.py              # Gemini conversational agent
│   ├── dashboard.py            # User summary dashboard
│   ├── destinations.py         # AI destination recommendations
│   ├── expenses.py             # Expense tracking
│   ├── profile.py              # User profile management
│   └── trip_planner.py         # AI day-by-day itinerary planner
├── reports/                    # Generated PDF reports storage
├── services/                   # Business logic (Auth, AI APIs)
└── utils/                      # Helper functions and UI components
```

---

## ⚙️ Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.11** or higher
- **Git** (for version control)
- **Docker** (optional, for containerized deployment)
- A valid **Google Gemini API Key** (Get one [here](https://aistudio.google.com/app/apikey))

---

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/student-travel-planner.git
cd student-travel-planner
```

### 2. Set Up a Virtual Environment

It's highly recommended to use a virtual environment to manage dependencies.

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the example environment file and add your sensitive credentials.

```bash
cp .env.example .env
```

Open the `.env` file and insert your **Google Gemini API Key**:
```env
GEMINI_API_KEY=your_actual_api_key_here
```

### 5. Run the Application

Launch the Streamlit server:

```bash
streamlit run app.py
```

The application will automatically open in your default web browser at `http://localhost:8501`.

---

## 🐳 Docker Deployment

For a consistent and isolated environment, you can run the application using Docker.

### 1. Build the Docker Image

```bash
docker build -t student-travel-planner .
```

### 2. Run the Container

Execute the container, ensuring you pass the `.env` file for API key access:

```bash
docker run -p 8501:8501 --env-file .env student-travel-planner
```
Access the application at `http://localhost:8501`.

---

## 📖 Usage Guide

1. **Sign Up/Login**: Create an account or log in to your existing profile.
2. **Setup Profile**: Fill out your academic schedule and basic preferences in the **Profile** tab.
3. **Take the Assessment**: Use the **Assessment** tab to let the AI learn about your travel style (e.g., adventurer, foodie, relaxer).
4. **Discover Destinations**: Head to the **Destinations** tab to get AI-curated spots that fit your budget and dates.
5. **Plan the Trip**: Generate a comprehensive itinerary via the **Trip Planner**.
6. **Set a Budget**: Use the **Budget** tool to allocate funds.
7. **Track & Analyze**: During your trip, log your costs in **Expenses** and visualize your financial health in **Analytics**.
8. **Export**: Download your plans via PDF for offline viewing.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

---

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

---
*Built with ❤️ and AI for students exploring the world.*
