# 🚀 Saarthi AI

> An AI-powered multilingual career guidance platform that helps users discover career paths aligned with their interests, skills, abilities, and knowledge.

## 📖 Overview

Choosing the right career can be overwhelming, especially when students and job seekers have limited access to personalized guidance. Saarthi AI was developed to bridge this gap using data-driven career recommendations powered by machine learning and the U.S. Department of Labor's O*NET occupational database.

Unlike traditional career assessment tools that rely on simple rule-based matching, Saarthi AI uses a two-stage machine learning architecture to analyze a user's profile and recommend careers that closely align with their strengths and interests.

The platform supports multiple languages, making career guidance accessible to a broader audience.

---

## ✨ Key Features

* 🧠 AI-powered career recommendations
* 🌐 Multilingual support (English, Hindi, Kannada)
* 📊 66-question psychometric assessment
* 🎯 Personalized Top 5 career recommendations
* 📚 Powered by real-world O*NET occupational data
* ⚡ Fast and responsive React frontend
* 🔒 Secure backend powered by FastAPI and PostgreSQL
* 📈 Scalable architecture with API versioning

---

## 🏗️ System Architecture

### Frontend

Built using React 18 and Vite for a fast and modern user experience.

#### Features

* Dynamic career assessment engine
* Real-time score aggregation
* Responsive UI using Tailwind CSS
* Client-side routing with React Router
* Internationalization (i18n)

**Tech Stack**

* React 18
* Vite
* Tailwind CSS
* React Router DOM
* i18next

---

### Backend

Built using FastAPI to provide high-performance REST APIs.

#### Features

* Asynchronous request handling
* PostgreSQL integration
* SQLAlchemy ORM
* Alembic migrations
* Versioned API architecture

**Tech Stack**

* FastAPI
* Python 3.10+
* PostgreSQL
* SQLAlchemy
* Alembic

---

## 🧠 Machine Learning Engine

### Why V2?

Early versions attempted to map a small set of features directly to hundreds of occupations, resulting in poor accuracy.

To improve recommendation quality, Saarthi AI was redesigned using a two-stage prediction architecture.

---

### Dataset

The recommendation engine is trained using occupational datasets from O*NET, including:

* Abilities
* Knowledge Areas
* Essential Skills
* Career Interest Types

These datasets are processed and normalized into 30 meaningful career-related features covering:

* Interests
* Skills
* Abilities
* Knowledge Domains

The final training dataset contains over 9,000 generated career profiles mapped to 894 occupations.

---

### Stage 1: Career Domain Prediction

A Random Forest Classifier predicts the most relevant career domains from 23 major O*NET occupational groups.

Examples include:

* Computer & Mathematical
* Architecture & Engineering
* Healthcare
* Education
* Business & Finance

#### Model Performance

* Accuracy: 97.24%
* Precision: 0.97
* Recall: 0.97

---

### Stage 2: Career Recommendation

Once the top career domains are identified, Saarthi AI performs similarity matching using Cosine Similarity.

The user's profile is compared against official O*NET occupational vectors to identify careers with the closest alignment.

This approach produces highly personalized and mathematically robust career recommendations.

---

## 🔄 Recommendation Workflow

1. User completes the 66-question assessment.
2. Responses are converted into a 30-feature profile vector.
3. Random Forest predicts the most relevant career domains.
4. Cosine Similarity compares the profile against occupations in those domains.
5. Saarthi AI returns the Top 5 recommended careers.

---

## 🛠️ Local Development Setup

### Prerequisites

* Node.js 18+
* Python 3.10+
* PostgreSQL

---

### Backend Setup

```bash
# Activate virtual environment
.venv\Scripts\activate

# Install dependencies
cd backend
pip install -r requirements.txt

# Start FastAPI server
python -m uvicorn main:app --reload
```

Backend runs at:

```text
http://localhost:8000
```

---

### Frontend Setup

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend runs at:

```text
http://localhost:5173
```

---

## 📊 Project Impact

* 894 Occupations Covered
* 23 Career Domains
* 30 Career Features
* 9,000+ Training Profiles
* 97.24% Domain Classification Accuracy
* Multilingual Career Guidance

---

## 🔮 Future Enhancements

* AI-powered career roadmap generation
* Skill gap analysis
* Course recommendations
* Resume evaluation
* Job market trend insights
* Career mentorship matching

---

## 📜 License

This project is licensed under the MIT License.

See the LICENSE file for more information.
