# 🎬 Movie Intelligence Aggregator

> Discover the **true Top Movies of any year** by combining ratings, reviews, popularity, and awards data from multiple trusted movie sources.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![AsyncIO](https://img.shields.io/badge/AsyncIO-Concurrent-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Active-success)

---

## 🌟 Overview

Most movie ranking websites provide only a single perspective. IMDb focuses heavily on user ratings, Rotten Tomatoes emphasizes critics, while TMDb measures popularity and engagement.

**Movie Intelligence Aggregator** combines data from multiple sources, removes duplicates, enriches metadata, and generates a weighted consensus ranking to identify the most impactful movies released in a given year.

The goal is simple:

> **Create a smarter movie ranking system than any individual source can provide.**

---

## ✨ Features

### 🔍 Multi-Source Aggregation

Collects movie information from multiple sources:

* IMDb
* TMDb
* OMDb
* Rotten Tomatoes *(optional)*
* Metacritic *(optional)*
* Wikipedia Awards Data

---

### 🧠 Intelligent Deduplication

Different platforms often list the same movie differently.

Example:

```text
The Batman (2022)
Batman, The (2022)
```

The system uses fuzzy matching and year validation to automatically merge duplicate entries into a single canonical movie record.

---

### 📊 Weighted Ranking Engine

Movies are ranked using multiple signals:

* Critic ratings
* Audience ratings
* Awards and nominations
* Review volume
* Popularity metrics
* Cross-platform consistency

Example scoring formula:

```text
Final Score =
35% Critics Score
30% Audience Score
20% Awards Score
15% Popularity Score
```

All weights are configurable.

---

### ⚡ High Performance

Built with modern asynchronous Python:

* Concurrent requests
* Connection pooling
* Retry mechanisms
* Exponential backoff
* Rate limiting
* Graceful degradation

If one source fails, the pipeline continues.

---

### 📦 Data Export

Results are automatically exported as:

| Format | Purpose                 |
| ------ | ----------------------- |
| TXT    | Human-readable report   |
| CSV    | Spreadsheet analysis    |
| JSON   | Machine learning & APIs |

---

## 🏗️ Architecture

```text
                ┌─────────────┐
                │    IMDb     │
                └──────┬──────┘
                       │
                ┌──────▼──────┐
                │    TMDb     │
                └──────┬──────┘
                       │
                ┌──────▼──────┐
                │    OMDb     │
                └──────┬──────┘
                       │
              ┌────────▼────────┐
              │ Movie Collector │
              └────────┬────────┘
                       │
              ┌────────▼────────┐
              │ Deduplicator    │
              └────────┬────────┘
                       │
              ┌────────▼────────┐
              │ Ranking Engine  │
              └────────┬────────┘
                       │
          ┌────────────┼────────────┐
          │            │            │
          ▼            ▼            ▼
        TXT           CSV         JSON
```

---

## 🚀 Quick Start

### Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/movie-intelligence-aggregator.git

cd movie-intelligence-aggregator
```

---

### Create Virtual Environment

```bash
python -m venv venv
```

Linux / macOS

```bash
source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Configure API Keys

Get free API keys from:

* TMDb
* OMDb

Linux/macOS:

```bash
export TMDB_API_KEY="YOUR_KEY"
export OMDB_API_KEY="YOUR_KEY"
```

Windows:

```cmd
set TMDB_API_KEY=YOUR_KEY
set OMDB_API_KEY=YOUR_KEY
```

---

### Run

```bash
python main.py 2014
```

or

```bash
python main.py
```

and enter the year when prompted.

---

## 📸 Example Output

```text
🏆 TOP MOVIES OF 2014

Rank  Movie                           Score
------------------------------------------------
1     Interstellar                    95.4
2     Whiplash                        94.1
3     The Grand Budapest Hotel        92.8
4     Gone Girl                       91.3
5     Nightcrawler                    90.9
6     Birdman                         90.4
7     Guardians of the Galaxy         89.8
8     Boyhood                         88.7
9     The Imitation Game              87.5
10    Edge of Tomorrow                86.9
```

---

## 📂 Project Structure

```text
movie_intelligence/
│
├── main.py
├── config.py
├── ranking_engine.py
│
├── scraper/
│   ├── base.py
│   ├── imdb.py
│   ├── tmdb.py
│   ├── omdb.py
│   ├── rotten_tomatoes.py
│   ├── metacritic.py
│   └── wikipedia.py
│
├── models/
│   └── movie.py
│
├── exporters/
│   ├── txt_exporter.py
│   ├── csv_exporter.py
│   └── json_exporter.py
│
├── cache/
├── datasets/
├── logs/
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Configuration

All project settings live inside:

```python
config.py
```

Available configuration options:

| Option                | Description                |
| --------------------- | -------------------------- |
| ACTIVE_SOURCES        | Enable/disable sources     |
| RANKING_WEIGHTS       | Ranking formula            |
| FUZZY_MATCH_THRESHOLD | Deduplication sensitivity  |
| CONCURRENT_REQUESTS   | Parallel request limit     |
| RETRY_ATTEMPTS        | Retry count                |
| RETRY_BACKOFF         | Exponential backoff factor |

---

## 🛠️ Tech Stack

### Core

* Python 3.9+
* AsyncIO
* aiohttp
* BeautifulSoup

### Data Processing

* RapidFuzz
* Dataclasses
* JSON
* CSV

### Engineering

* Logging
* Type Hints
* OOP
* SOLID Principles

---

## 📈 Future Improvements

* Letterboxd Integration
* Streamlit Dashboard
* Docker Support
* SQLite Cache Layer
* Unit Testing Suite
* REST API
* Machine Learning Recommendation Engine
* Movie Trend Analysis

---

## ⚠️ Limitations

* Some sources do not provide public APIs.
* Website structure changes may require scraper updates.
* Rankings depend on available data quality.
* Certain movies may have incomplete metadata.

---

## 📄 License

This project is licensed under the MIT License.

See the `LICENSE` file for details.

---
