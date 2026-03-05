
# ~Personal goal optimization and Accountability System

a goal-tracking and reflection system designed to help users **set goals**, **track daily/weekly execution**, and **monitor long-term consistency** (monthly → yearly).

This project focuses on **behavioral feedback** over time — not just checking tasks.


## Why this exists

Most trackers answer: “Did you do the task?”

This project answers:
- Are you consistent over time?
- Which life domains are neglected?
- Are you on track for long-term goals (monthly/quarter/semester/yearly)?
- Where do you need to adjust your behavior to reach your objectives?


## Features

- **Goal Setup**: create goals with a category + frequency  
  Daily, Weekly, Monthly, Quarterly, Semester, Yearly
- **Tracking Board**
- **Reports**
  - Daily consistency timeline 
  - Weekly consistency table 
  - Long-term strategic health 

## Tech Stack

- **Frontend**: Streamlit
- **Database**: Neon (PostgreSQL)
- **Data**: Pandas
- **Charts**: Plotly
- **Auth**: simple email/password (MVP)


## Project Structure

```
~Personal-goal-optimization-and-Accountability-System/
├── app.py
├── core_logic.py
├── db_utils.py
├── requirements.txt
├── packages.txt
├── .gitignore
├── README.md
├── .streamlit/
│   ├── config.toml
│   └── secrets.toml        # local only (never commit)
└── screenshots/

````


## Getting Started 
###  Install dependencies

```bash
pip install -r requirements.txt
```


## Configure Neon (PostgreSQL)

This project reads the Neon connection string from **Streamlit secrets**.

### 1) Create `.streamlit/secrets.toml`

Create this file locally:

```bash
mkdir -p .streamlit
touch .streamlit/secrets.toml
```

Add your Neon connection string inside:

```toml
DATABASE_URL="postgresql://<user>:<password>@<host>/<dbname>?sslmode=require"
```

### 2) Ensure `secrets.toml` is ignored by git

Your `.gitignore` should include:

```gitignore
.streamlit/secrets.toml
```


## Run the app

```bash
streamlit run app.py
```