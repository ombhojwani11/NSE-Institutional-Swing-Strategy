# NSE Institutional Swing Strategy

**AI-Assisted Full-Stack Swing Trading System for NSE F&O**  
*Detecting institutional footprints using delivery, futures & options data*

![Python](https://img.shields.io/badge/Python-3775A8?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![XlsxWriter](https://img.shields.io/badge/Excel%20Automation-21759B?style=for-the-badge&logo=microsoft-excel&logoColor=white)

### 🎯 What it does
Built a complete end-to-end Python pipeline that processes **full NSE historical data** (delivery + futures + options) and generates **professional institutional signal reports** every month.

- Automated data ingestion & cleaning from NSE zip files  
- Rolling statistics + Z-score anomaly detection  
- Multi-factor signal generation (Delivery + Futures OI/Volume + Institutional Options)  
- Professional Excel output with conditional formatting, embedded charts & summary dashboard  
- 2,500+ lines of clean, modular, production-grade code (developed with AI assistance)

### 🛠️ Tech Stack
- **Core**: Python 3, Pandas, NumPy  
- **Reporting**: XlsxWriter (custom formatting, charts, conditional coloring)  
- **Data Handling**: Zip extraction, date math, rolling windows, caching  
- **Analysis**: Rolling medians, Z-scores, multi-timeframe pattern detection  

### 📊 Sample Output
(Images in `/outputs` folder)

**Executive Summary Dashboard** | **Individual Symbol Deep-Dive Sheets** | **Z-Score Visuals**

### 🚀 Why this stands out
- Fully reproducible & auditable pipeline  
- Handles real institutional data flows (delivery + F&O)  
- Professional-grade reporting that looks like a quant desk tool  
- Demonstrates strong Python + data engineering skills applied to trading

**This is the backbone of my live swing trading strategy.**

---

### 📁 Project Structure
See folder layout above.

### 🛠️ Setup
```bash
git clone https://github.com/YOURUSERNAME/NSE-Institutional-Swing-Strategy.git
cd NSE-Institutional-Swing-Strategy
pip install -r requirements.txt
