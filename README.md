# Student Depression Analysis System

An interactive command-line Python application that analyzes student survey data to identify demographic, academic, socioeconomic, and lifestyle patterns associated with self-reported depression.

---

## Table of Contents
- [Project Overview](#project-overview)
- [Key Features](#key-features)
- [Dataset Details](#dataset-details)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Execution Instructions](#execution-instructions)
- [Menu Options & Capabilities](#menu-options--capabilities)
- [Sample Output](#sample-output)
- [Data & Methodology Notes](#data--methodology-notes)
- [Important Disclaimer](#important-disclaimer)

---

## Project Overview

The **Student Depression Analysis System** processes a dataset containing 4,464 survey responses from university students. The CLI tool cleanses and standardizes the records, segments the population across various demographic and lifestyle dimensions, computes statistical metrics (case counts and category percentages), and produces structured analytical summaries and comparative reports.

---

## Key Features

- **Interactive CLI Menu:** Fast, lightweight, terminal-based navigation through 9 distinct analysis modules.
- **Demographic & Environmental Categorization:**
  - Overall population statistics
  - Age brackets (`17-19`, `20-22`, `23-25`, `26-28`)
  - Gender comparison (`Female` vs. `Male`)
  - Academic progress by semester (`Semester 0` to `13`)
  - Socioeconomic status (`Lower Middle class`, `Middle class`, `Rich class`)
  - Relationship status (`Single`, `In a Relationship`, `Complicated`)
  - Living arrangements (`Bachelor` vs. `Family`)
  - Health condition assessment (`Good`, `Normal`, `Abnormal`, `Critical`)
- **Automated Statistical Insights:** Computes category-level percentages, case distribution counts, and percentage-point gap rankings.
- **Small-Sample Protection:** Warns when sub-cohorts have fewer than 30 samples (`MIN_GROUP_SIZE = 30`), marking them as unreliable to avoid statistical distortion.
- **Anomaly & Anomaly Split Detection:** Highlights potential data collection artifacts (e.g., 0% or 100% split responses).
- **Consolidated Summary Report:** Menu Option 9 executes an end-to-end report consolidating metrics across all 7 categorical dimensions.

---

## Dataset Details

The dataset is stored in `dataset/student_depression.csv` and contains **4,464 student survey responses** with 13 attributes:

| Column Name | Type | Description |
| :--- | :--- | :--- |
| `Gender` | Text | Gender of the student (`Male`, `Female`) |
| `Age` | Numeric | Age in years |
| `Family_background` | Text | Socioeconomic background (`Lower Middle class`, `Middle class`, `Rich class`) |
| `Relationship_status`| Text | Relationship status (`Single`, `In a Relationship`, `Complicated`) |
| `Marital_status` | Text | Marital status (`Unmarried`, `Married`) |
| `Living_style` | Text | Accommodation type (`Bachelor` / hostel / roommates, `Family`) |
| `Current_semester` | Numeric | Current semester enrolled (`0` to `13`) |
| `CGPA` | Numeric | Cumulative Grade Point Average |
| `friend_circle` | Text | Peer network availability (`Yes`, `No`) |
| `Health_condition` | Text | Physical/general health status (`Good`, `Normal`, `Abnormal`, `Critical`) |
| `Cost_without_study` | Numeric | Monthly living costs excluding academic tuition |
| `Home_division` | Text | Geographical home region / division |
| `Depression` | Text | Primary survey response (`Yes`, `No`) |

---

## Project Structure

```text
Student-Depression-Analysis/
├── dataset/
│   └── student_depression.csv   # Student survey dataset (4,464 records)
├── main.py                      # Main Python CLI application
├── requirements.txt             # Python dependencies (pandas, numpy)
└── README.md                    # Project documentation & execution guide
```

---

## Prerequisites

Before running the application, ensure you have the following installed:

- **Python 3.8+** (Python 3.9, 3.10, 3.11, or newer recommended)
- **pip** (Python package installer)
- **Git** (optional, for cloning)

To verify your Python and pip installation:
```bash
python --version
pip --version
```
*(On macOS/Linux, you may need to use `python3` and `pip3`)*

---

## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/SadhaSri697/Student-Depression-Analysis.git
cd Student-Depression-Analysis
```

### 2. (Recommended) Create a Virtual Environment
Isolating dependencies ensures a clean execution environment:

- **Windows (Command Prompt / PowerShell):**
  ```cmd
  python -m venv venv
  venv\Scripts\activate
  ```

- **macOS / Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 3. Install Dependencies
Install the required packages using `requirements.txt`:
```bash
pip install -r requirements.txt
```

Alternatively, you can install the dependencies directly:
```bash
pip install pandas numpy
```

---

## Execution Instructions

Run the main script from the root of the project directory:

```bash
python main.py
```
*(or `python3 main.py` on macOS/Linux)*

Upon launching, the interactive menu will appear in your terminal:

```text
STUDENT DEPRESSION ANALYSIS SYSTEM - MAIN MENU

 1. Overall Depression Analysis
 2. Age-wise Depression Analysis
 3. Gender-wise Depression Analysis
 4. Semester-wise Depression Analysis
 5. Family Background Analysis
 6. Relationship Status Analysis
 7. Living Arrangement Analysis
 8. Health Condition Analysis
 9. Complete Depression Report
10. Exit

Enter your choice:
```

### Navigating the System:
1. Enter the number corresponding to your chosen analysis (e.g., `1` for Overall Analysis, `9` for the Complete Report) and press **Enter**.
2. Review the generated table, statistical breakdown, and automated insights.
3. Press **Enter** to return to the main menu.
4. Enter `10` when you are ready to terminate the program.

---

## Menu Options & Capabilities

| Option | Title | Description |
| :---: | :--- | :--- |
| **1** | **Overall Depression Analysis** | Summarizes total population metrics and overall percentage of students reporting depression. |
| **2** | **Age-wise Depression Analysis** | Groups students into 4 standard age brackets (17-19, 20-22, 23-25, 26-28) and identifies highest/lowest incidence. |
| **3** | **Gender-wise Depression Analysis** | Directly contrasts female and male cohorts, reporting percentage point differences. |
| **4** | **Semester-wise Depression Analysis**| Tracks depression reporting across university semesters (Semesters 0 through 13). |
| **5** | **Family Background Analysis** | Examines variations among Lower Middle class, Middle class, and Rich class backgrounds. |
| **6** | **Relationship Status Analysis** | Evaluates Single, In a Relationship, and Complicated relationship statuses. |
| **7** | **Living Arrangement Analysis** | Compares students living independently/with roommates (`Bachelor`) vs. living with `Family`. |
| **8** | **Health Condition Analysis** | Analyzes correlations between general health state (`Good`, `Normal`, `Abnormal`, `Critical`) and depression. |
| **9** | **Complete Depression Report** | Generates an end-to-end report summarizing dataset statistics, all 7 categorical tables, ranked disparity gaps, and anomalies. |
| **10** | **Exit** | Gracefully closes the application. |

---

## Sample Output

Example execution of **Option 1 (Overall Depression Analysis)**:

```text
1. OVERALL DEPRESSION ANALYSIS

Total students                             : 4464
Students reporting depression (Yes)        : 1201
Students not reporting depression (No)     : 3263

Percentage of each group (out of all students):
  Reporting depression (Yes)    : 26.9%
  Not reporting depression (No) : 73.1%

Insight:
  About 27 out of every 100 students in this dataset answered 'Yes'.
  Most students answered 'No'.
  This is the overall figure. The next options compare the percentage
  inside each category, so you can see how it differs between groups.
  Note: these results describe patterns in survey responses.
  They are statistical associations only - not medical diagnoses
  and not proof that one factor causes another.
```

---

## Data & Methodology Notes

- **Data Cleaning:** During file ingestion, text values are stripped of whitespace and capitalized, numerical fields are coerced, non-positive ages are replaced with `NaN`, and records without explicit binary `Yes`/`No` depression values are filtered.
- **Percentage Calculation:** Category percentages are calculated relative to each group's individual size (`cases / group_total * 100`) rather than overall dataset size, providing an accurate basis for comparisons across unevenly-sized cohorts.
- **Reliability Threshold:** Subgroups containing fewer than 30 respondents are flagged with an asterisk (`*`) and excluded from highest/lowest percentage rankings to prevent small-sample bias.

---

## Important Disclaimer

> **Note:** The results generated by this tool describe statistical patterns and correlations observed within self-reported survey responses. They represent **statistical associations only** and must **not** be construed as clinical or medical diagnoses, nor as proof of causal relationships between demographic or lifestyle factors and depression.
