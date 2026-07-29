# ⚽ Football Analytics Platform

> End-to-end football analytics platform built on StatsBomb Open Data.
>
> Transform raw football event JSON into a fully normalized relational database and perform advanced SQL analytics, visualization and machine learning.

---

## Features

- ⚡ Modular ETL pipeline
- 🗄 47-table normalized SQLite database
- 🔗 Referential integrity using primary & foreign keys
- 📊 Built for SQL analytics
- 📈 Ready for visualization
- 🤖 Machine learning ready

---

## Architecture

<p align="center">
<img src="docs/images/architecture.png" width="900">
</p>

---

## Database ER Diagram

<p align="center">
<img src="docs/images/ERD.png" width="100%">
</p>

---

## Current Status

| Module | Status |
|---------|--------|
| Extraction | ✅ |
| Transformation | ✅ |
| Database Design | ✅ |
| Database Validation | ✅ |
| SQL Analytics | 🚧 |
| Dashboard | 🚧 |
| Machine Learning | 🚧 |

---

## Project Structure

```text
football-analytics/

├── data/
├── database/
├── docs/
├── src/
├── notebooks/
├── tests/
├── README.md
└── requirements.txt
```

---

## Tech Stack

- Python
- SQLite
- Pandas
- Git
- StatsBomb Open Data

---

## Roadmap

- [x] Data Extraction
- [x] Data Transformation
- [x] Database Design
- [x] SQLite ETL
- [ ] SQL Analytics
- [ ] Exploratory Data Analysis
- [ ] Dashboard
- [ ] Machine Learning

---

## Documentation

| Document | Description |
|-----------|-------------|
| ER Diagram | Database relationships |
| ETL Pipeline | Data processing workflow |
| Database Design | Schema documentation |

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.