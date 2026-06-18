# BigQuery Release Notes Dashboard

A high-fidelity, responsive web application that parses, structures, and presents the official Google BigQuery Release Notes feed in a modern visual dashboard. It features robust caching, real-time client-side text filtering, status classification tags, and dark/light modes.

Live Remote Repository: [Isaac-Udoetor-event-talks-app](https://github.com/Izik-Ipkiss/Isaac-Udoetor-event-talks-app)

---

## 🚀 Key Features

* **Advanced RSS Parser**: Splits multi-item daily release entries into separate, classified dashboard cards (e.g. *Features*, *Issues*, *Announcements*, *Deprecations*).
* **Dual-Tier Resilience Cache**: Serves responses in sub-milliseconds from an in-memory cache. If Google's feed is down, it serves cached logs as a fallback instead of failing.
* **Instant Client-Side Filtering**: Live-filters the timeline by keyword search and/or category badges without re-querying the backend.
* **Typographic & Visual Polish**: Custom UI layout built with the **Plus Jakarta Sans** and **JetBrains Mono** fonts, dynamic skeleton loaders, and a fluid dark/light theme switch.

---

## 🛠️ Tech Stack

* **Backend**: Python Flask (using standard libraries `urllib.request` and `xml.etree.ElementTree` for RSS parsing).
* **Frontend**: Vanilla HTML5, CSS3 Custom Properties (Variables), and Modern Vanilla JavaScript (ES6).

---

## 📁 Directory Structure

```text
├── templates/
│   └── index.html      # Main frontend HTML template, CSS styling, and JS application
├── .gitignore          # Standard repository ignore list
├── app.py              # Flask backend server, parser, and caching logic
└── README.md           # This project documentation file
```

---

## ⚙️ Setup & Local Installation

### Prerequisites
* Python 3.8 or higher installed on your system.

### 1. Clone the Repository
```bash
git clone https://github.com/Izik-Ipkiss/Isaac-Udoetor-event-talks-app.git
cd Isaac-Udoetor-event-talks-app
```

### 2. Install Dependencies
Install Flask in your global environment or virtual environment:
```bash
pip install Flask
```

### 3. Run the Development Server
```bash
python app.py
```

### 4. Access the Dashboard
Open your web browser and navigate to:
* **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 🔍 How the Caching Works
1. When a user requests `/api/releases`, the server checks the in-memory cache.
2. If the cache is **less than 5 minutes old**, it returns the cached data instantly.
3. If the cache is **expired**, the server fetches the XML feed from Google, parses it, updates the cache, and serves the new data.
4. If a network fetch fails, the server serves the stale cache with a warning metadata flag.
5. Users can bypass the cache by clicking the **"Refresh Feed"** button, which forces a live reload from Google.

---

## 📝 License
This project is open-source. Feel free to copy, modify, and distribute it as needed.
