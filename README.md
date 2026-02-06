# PackVote ✈️

PackVote is a **constraint-aware group travel recommendation system**. It helps groups agree on a destination by aggregating preferences, filtering by real-world constraints (budget, weather, distance), and generating AI itineraries.

## 🌟 Key Features

*   **Group Coordination**: Create groups and invite friends via Email.
*   **Dynamic Filtering**: Backend filters places based on:
    *   **Weather**: Real-time forecast checks (Open-Meteo).
    *   **Distance**: Travel time from start city (Google Maps).
    *   **Seasonality**: "Best Time to Visit" logic.
*   **Smart Ranking**: Destinations are ranked by matching group preferences using TF-IDF/Cosine Similarity.
*   **AI Itinerary**: Generates day-wise trip plans for the winning destination using Gemini AI.
*   **Creative UI**: Modern, responsive frontend with "Glassmorphism" design.

## 🛠️ Tech Stack

*   **Backend**: FastAPI, SQLite (SQLAlchemy), Pydantic.
*   **Frontend**: Next.js 14, Tailwind CSS, Framer Motion, Lucide Icons.
*   **External APIs**:
    *   **Google Gemini**: Itinerary Generation.
    *   **Open-Meteo**: Weather Data.
    *   **Google Maps**: Distance Matrix.
    *   **SMTP (Gmail)**: Email Invitations.

## 🚀 Getting Started

### Prerequisites

*   Python 3.10+
*   Node.js 18+
*   Google Account (for App Password & API Keys)

### 1. Backend Setup

1.  Clone the repo and navigate to the project root.
2.  Create a virtual environment:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate  # Windows
    # source venv/bin/activate # Mac/Linux
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configuration**:
    *   Copy `.env.example` to `.env`.
    *   Fill in your API Keys:
        *   `SMTP_USERNAME` / `SMTP_PASSWORD`: Your Gmail & App Password (for sending invites).
        *   `GOOGLE_MAPS_API_KEY`: For distance calculations.
        *   `GEMINI_API_KEY`: For AI itineraries.
        *   `GOOGLE_FORM_LINK`: Link to your preference survey form.

5.  **Initialize Database & Load Data**:
    ```bash
    python scripts/load_places.py
    ```
    *(This creates the SQLite DB and loads destination data from `data/processed/`)*

6.  **Run Server**:
    ```bash
    uvicorn app.main:app --reload
    ```
    Backend will run at: `http://127.0.0.1:8000`

### 2. Frontend Setup

1.  Navigate to the frontend directory:
    ```bash
    cd frontend
    ```
2.  Install dependencies:
    ```bash
    npm install
    # or
    npm install --legacy-peer-deps
    ```
3.  **Run Development Server**:
    ```bash
    npm run dev
    ```
    Frontend will run at: `http://localhost:3000`

## 📂 Project Structure

```
PACKVOTE/
├── app/
│   ├── api/            # Route handlers (groups, participants, recommendations)
│   ├── models/         # Database models (SQLAlchemy)
│   ├── services/       # Logic (Email, Weather, Distance, AI, Recommendation)
│   ├── config.py       # Pydantic settings
│   └── main.py         # App entry point
├── frontend/
│   ├── app/            # Next.js App Router pages
│   ├── components/     # UI Components (Navbar, Cards)
│   └── ...
├── data/               # Raw and Processed JSON data
├── scripts/            # Utility scripts (loader, debuggers)
└── ...
```

## 🤝 Contribution

1.  Fork the repository.
2.  Create a feature branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your changes.
4.  Push to the branch.
5.  Open a Pull Request.

---
Made with ❤️ by the PackVote Team
