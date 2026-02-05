# 🎬 Cinematrix

Cinematrix is a **full-stack movie and TV show catalog platform** integrated with an **interaction-driven machine learning recommendation system**. The project focuses on delivering **efficient, scalable, and personalized movie recommendations** while maintaining a modern, production-grade web application architecture.

---

## 📌 Project Overview

Cinematrix allows users to:

* Browse a large catalog of **movies and TV shows**
* Search and view detailed information (cast, genres, overview, runtime, etc.)
* Maintain a **watchlist** and **rating history**
* Receive **personalized movie recommendations** based on their interactions

While cataloging and user management form the foundation, the **core highlight** of Cinematrix is its **machine learning–based recommendation engine**, designed with a strong emphasis on **efficiency and real-world scalability**.

---

## 🧠 Recommendation System – Core Idea

Cinematrix uses a **content-based recommendation system** powered by **cosine similarity**. Instead of running recommendations continuously, the system is designed to **compute recommendations only when necessary**, reducing redundant computation and improving performance.

### User Interaction Tracking

Each user interaction contributes to an accumulated interaction weight:

| Interaction Type | Weight Formula      |
| ---------------- | ------------------- |
| Click            | 0.5                 |
| Add to Watchlist | 1.0                 |
| Rate Movie       | 2.5 × (rating / 10) |

Once a user’s total interaction weight **exceeds 5**, the backend triggers the recommendation engine.

---

## ⚙️ Recommendation Workflow

1. User interactions are stored in the database.
2. Interaction weights are accumulated per user.
3. When the threshold (>5) is crossed:

   * Backend calls the **ML Recommendation API**
   * User interactions are fetched
   * A **user preference vector** is generated
4. Cosine similarity is computed against precomputed movie vectors.
5. Top-N recommendations are generated and stored in the database.
6. The frontend simply fetches stored recommendations (no recomputation).

This design ensures **high efficiency** and **low latency** during normal application usage.

---

## 🎥 Movie Representation & Feature Engineering

The recommendation system considers only the **top 5,000 most popular movies** (out of ~25,000) to:

* Reduce computational cost
* Improve recommendation relevance

### Features Used

* Cast
* Director
* Genre
* Keywords
* Overview
* Tagline
* Runtime
* Release Year

### Vectorization Strategy

* **Categorical features** → One-hot encoding
* **Textual features** → TF-IDF vectorization
* **Numerical features** → Scaled values

All feature vectors are **concatenated into a single combined movie vector**.

➡️ These vectors are **precomputed offline** and stored as sparse matrices to avoid repeated computation during runtime.

---

## 👤 User Vector Construction

* Only the **most recent 50 interactions** are considered
* For movies with multiple interactions, the **highest-priority interaction** is used:

  * Rated > Watchlist > Click
* Each movie vector is weighted based on interaction type
* Final user vector is a **normalized weighted average** of interacted movie vectors

---

## 🧊 Cold Start Handling

* New users receive **popular movies** instead of personalized recommendations
* Personalized recommendations begin only after sufficient interaction data is collected
* Recommendation quality improves progressively as users interact more

---

## 📊 Evaluation Strategy

Formal quantitative evaluation (precision, recall, etc.) was **out of scope** due to the absence of real user feedback data.

Instead, the system was **qualitatively evaluated** through:

* Demo user accounts
* Controlled interactions with known movie genres
* Manual verification of recommendation relevance

This approach ensured correctness and logical validity of the recommendation pipeline.

---

## 🧩 Application Architecture

### Application Stack

* **Language**: TypeScript
* **Framework**: Next.js (App Router, full-stack)
* **Frontend**: React + Tailwind CSS
* **Backend**: Node.js (Next.js API routes)
* **Authentication**: BetterAuth (Email + Google OAuth)
* **ORM**: Prisma
* **Database**: PostgreSQL

### Machine Learning Stack

* **Language**: Python
* **ML Framework**: Scikit-learn
* **Data Processing**: Pandas, NumPy
* **API Framework**: FastAPI
* **Similarity Metric**: Cosine Similarity

---

## 🗄️ Data Sources & Processing

* Dataset sourced from **Kaggle** (derived from TMDB)
* Initial dataset contained ~1.36M movies and TV shows
* Filtered to:

  * 25,000 popular movies
  * 5,000 popular TV shows

### Additional Data Enrichment

* Cast and director/creator data fetched using **TMDB API**
* Multiple Python notebooks used for:

  * Data cleaning and filtering
  * Feature extraction
  * Database normalization
  * Vector precomputation

The final database schema is **fully normalized**, consisting of ~43 tables.

---

## 🚀 Deployment

* **Frontend & Backend (Next.js)**: Vercel
* **Database (PostgreSQL)**: Supabase
* **ML Recommendation API (FastAPI)**: Render

The ML service is deployed as a **secure microservice**, accessible only via a custom API secret.

---

## 🔐 Security

* Recommendation API protected using a **custom API key middleware**
* Prevents unauthorized access to the ML service

---

## 🧭 Future Improvements

* Separate recommendation system for TV shows
* Hybrid recommendation (content + collaborative filtering)
* Online learning with continuous user feedback
* Formal evaluation using real user interaction data
* Caching and batching strategies for large-scale users

---

## 🏁 Conclusion

Cinematrix demonstrates how **modern full-stack development** can be effectively combined with **machine learning systems** to create scalable, efficient, and user-centric applications. The project emphasizes **smart architectural decisions**, **precomputation strategies**, and **clean system separation**, making it both practical and extensible.

---

📌 *Cinematrix — Efficient recommendations, thoughtfully engineered.*
