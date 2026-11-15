import os

import numpy as np
import pandas as pd


BASE_FOLDER = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_FOLDER, "dataset", "student_depression.csv")

REQUIRED_COLUMNS = [
    "Gender", "Age", "Family_background", "Relationship_status",
    "Living_style", "Current_semester", "Health_condition", "Depression",
]
TEXT_COLUMNS = [
    "Gender", "Family_background", "Relationship_status",
    "Living_style", "Health_condition", "Depression",
]
NUMBER_COLUMNS = ["Age", "Current_semester"]

MIN_GROUP_SIZE = 30

AGE_GROUPS = [
    {"label": "17-19", "low": 17, "high": 19},
    {"label": "20-22", "low": 20, "high": 22},
    {"label": "23-25", "low": 23, "high": 25},
    {"label": "26-28", "low": 26, "high": 28},
]

CATEGORIES = [
    {"title": "Age group", "column": "Age_Group"},
    {"title": "Gender", "column": "Gender"},
    {"title": "Semester", "column": "Current_semester"},
    {"title": "Family background", "column": "Family_background"},
    {"title": "Relationship status", "column": "Relationship_status"},
    {"title": "Living arrangement", "column": "Living_style"},
    {"title": "Health condition", "column": "Health_condition"},
]

DISCLAIMER_LINES = [
    "Note: these results describe patterns in survey responses.",
    "They are statistical associations only - not medical diagnoses",
    "and not proof that one factor causes another.",
]


def load_data(path):
    """Read the CSV file into a Pandas DataFrame.
    Returns None (and prints a message) if the file cannot be found."""
    if not os.path.exists(path):
        print(f"Error: dataset file not found at:\n  {path}")
        print("Make sure student_depression.csv is inside the 'dataset' folder.")
        return None
    return pd.read_csv(path)


def check_required_columns(df):
    """Make sure every column the program needs is really in the file.
    Uses a LIST and a FOR loop to collect any missing column names."""
    missing = []
    for column in REQUIRED_COLUMNS:
        if column not in df.columns:
            missing.append(column)

    if len(missing) > 0:
        print("Error: these required columns are missing:", missing)
        return False
    return True


def clean_data(df):
    """Build a cleaned COPY of the data. The original DataFrame is never changed.
    Removes extra spaces, turns bad numbers into missing values (NaN) and
    keeps only rows with a clear Yes/No Depression answer."""
    cleaned = df.copy()

    for column in TEXT_COLUMNS:
        cleaned[column] = cleaned[column].str.strip()
    cleaned["Depression"] = cleaned["Depression"].str.capitalize()

    for column in NUMBER_COLUMNS:
        cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce")
    cleaned.loc[cleaned["Age"] <= 0, "Age"] = np.nan

    cleaned = cleaned[cleaned["Depression"].isin(["Yes", "No"])].copy()
    return cleaned


def calculate_percentage(part, whole):
    """Return part as a percentage of whole. Avoids dividing by zero."""
    if whole == 0:
        return 0.0
    return part / whole * 100


def count_reported(data):
    """Count students whose Depression answer is 'Yes' (NumPy sum of True values)."""
    return int(np.sum(data["Depression"] == "Yes"))


def format_label(value):
    """Show 5.0 as '5' so semesters look clean."""
    if isinstance(value, (float, np.floating)) and float(value).is_integer():
        return str(int(value))
    return str(value)


def find_age_group(age):
    """Return the label of the age group (17-19, 20-22, ...) that contains this age."""
    if pd.isna(age):
        return None
    for group in AGE_GROUPS:
        if group["low"] <= age <= group["high"]:
            return group["label"]
    return None


def add_age_group(data):
    """Return a COPY of the data with an extra 'Age_Group' column."""
    result = data.copy()
    result["Age_Group"] = result["Age"].apply(find_age_group)
    return result


def summarise_groups(data, column):
    """The core calculation used by every analysis.

    For each different value in 'column' (for example 'Male' and 'Female') it counts
    the students, the reported cases (answer 'Yes') and the percentage.
    Each group is stored in a DICTIONARY and all dictionaries are kept in a LIST.

    Percent = reported cases in the group / students in the SAME group x 100."""
    rows = []
    for value in sorted(data[column].dropna().unique()):
        subset = data[data[column] == value]
        students = len(subset)
        cases = count_reported(subset)
        rows.append({
            "Category": value,
            "Label": format_label(value),
            "Students": students,
            "Cases": cases,
            "NotReported": students - cases,
            "Percent": calculate_percentage(cases, students),
        })
    return rows


def reliable_rows(rows):
    """Keep only groups with at least MIN_GROUP_SIZE students.
    A group of 1 or 2 students can easily show 0% or 100% by chance."""
    reliable = []
    for row in rows:
        if row["Students"] >= MIN_GROUP_SIZE:
            reliable.append(row)
    if len(reliable) == 0:
        return rows
    return reliable


def find_most_cases(rows):
    """Group with the largest NUMBER of reported cases (NumPy argmax gives its position)."""
    cases = np.array([row["Cases"] for row in rows])
    return rows[int(np.argmax(cases))]


def find_highest_percent(rows):
    """Group with the highest PERCENTAGE of reported cases (reliable groups only)."""
    reliable = reliable_rows(rows)
    percents = np.array([row["Percent"] for row in reliable])
    return reliable[int(np.argmax(percents))]


def find_lowest_percent(rows):
    """Group with the lowest PERCENTAGE of reported cases (reliable groups only)."""
    reliable = reliable_rows(rows)
    percents = np.array([row["Percent"] for row in reliable])
    return reliable[int(np.argmin(percents))]


def has_small_group(rows):
    """True if any group has fewer than MIN_GROUP_SIZE students."""
    for row in rows:
        if row["Students"] < MIN_GROUP_SIZE:
            return True
    return False


def has_perfect_split(rows):
    """True if a reliable group (30+ students) has exactly 0% or 100% reported cases."""
    for row in rows:
        if row["Students"] >= MIN_GROUP_SIZE and (row["Percent"] == 0 or row["Percent"] == 100):
            return True
    return False


def print_perfect_split_caution(title):
    """Warn that a perfect 0% / 100% split is unusual and may not be a real survey pattern."""
    print("\nCaution:")
    print(f"  At least one {title.lower()} category has 0% or 100% reported cases.")
    print("  Survey answers rarely split this perfectly, so this column may be closely")
    print("  tied to how the Depression column was created in the dataset. Treat these")
    print("  numbers with extra care and do not read them as one factor causing another.")


def print_heading(title):
    """Print a section title with blank lines around it."""
    print()
    print(title)
    print()


def print_group_table(rows, title):
    """Print the list of group dictionaries as a neat table."""
    print(f"{title:<20}{'Students':>9}{'Reported cases':>15}{'Not reported':>13}{'% within category':>19}")
    for row in rows:
        mark = ""
        if row["Students"] < MIN_GROUP_SIZE:
            mark = " *"
        print(f"{row['Label']:<20}{row['Students']:>9}{row['Cases']:>15}{row['NotReported']:>13}"
              f"{row['Percent']:>18.1f}%{mark}")
    if has_small_group(rows):
        print(f"* fewer than {MIN_GROUP_SIZE} students - the percentage is unreliable.")


def print_reading_note():
    """Explain the difference between the two main numbers in every table."""
    print("\nHow to read the table:")
    print("  Reported cases    = the NUMBER of students who answered 'Yes'.")
    print("  % within category = reported cases / students in that same category x 100.")


def print_disclaimer():
    """Print the reminder that results are associations, not diagnoses."""
    for line in DISCLAIMER_LINES:
        print("  " + line)


def print_insights(rows):
    """Automatically write the key findings for a table of groups."""
    most = find_most_cases(rows)
    highest = find_highest_percent(rows)
    lowest = find_lowest_percent(rows)

    print("\nInsight:")
    print(f"  Most reported cases : {most['Label']} "
          f"({most['Cases']} cases among {most['Students']} students)")
    print(f"  Highest percentage  : {highest['Label']} "
          f"({highest['Percent']:.1f}% of its {highest['Students']} students)")
    print(f"  Lowest percentage   : {lowest['Label']} "
          f"({lowest['Percent']:.1f}% of its {lowest['Students']} students)")

    if highest["Category"] != lowest["Category"]:
        gap = highest["Percent"] - lowest["Percent"]
        print(f"  The highest and lowest percentages are {gap:.1f} percentage points apart.")

    if len(rows) > 1:
        if most["Category"] != highest["Category"]:
            print("  The category with the most cases is not the one with the highest percentage.")
            print("  Case counts depend on how many students each category has, so the")
            print("  percentage is the fairer way to compare categories of different sizes.")
        else:
            print("  The same category has both the most cases and the highest percentage.")

    if has_small_group(rows):
        print(f"  Categories with fewer than {MIN_GROUP_SIZE} students (marked *) are left out of")
        print("  the highest/lowest percentage because their percentages are unreliable.")
    print_disclaimer()


def print_two_category_comparison(rows, title):
    """If a category has exactly two groups (e.g. Male and Female), compare them directly."""
    if len(rows) != 2:
        return
    first = rows[0]
    second = rows[1]

    print(f"\nComparison between the two {title.lower()} categories:")
    for row in rows:
        print(f"  {row['Label']}: {row['Cases']} reported cases, "
              f"{row['Percent']:.1f}% within the category ({row['Students']} students)")

    gap = first["Percent"] - second["Percent"]
    if gap > 0:
        print(f"  {first['Label']} has the higher percentage, by {gap:.1f} percentage points.")
    elif gap < 0:
        print(f"  {second['Label']} has the higher percentage, by {abs(gap):.1f} percentage points.")
    else:
        print("  Both categories have the same percentage.")

    if first["Cases"] > second["Cases"]:
        more_cases = first
    else:
        more_cases = second
    if gap > 0:
        higher_percent = first
    else:
        higher_percent = second
    if more_cases["Category"] != higher_percent["Category"]:
        print(f"  {more_cases['Label']} has more reported cases, but {higher_percent['Label']} has the "
              f"higher percentage.")
        print("  This is because the two categories have different numbers of students.")


def run_category_analysis(data, column, title):
    """Generic analysis used by menu options 2 to 8: table, reading note and insights."""
    rows = summarise_groups(data, column)
    print(f"Total students analysed: {len(data)}\n")
    print_group_table(rows, title)
    print_reading_note()
    print_insights(rows)
    return rows


def wait_for_enter():
    """Pause so the user can read the results before the menu appears again."""
    input("\nPress Enter to return to the main menu...")


def show_overall_analysis(data):
    """Menu 1: how many students answered Yes and No, overall."""
    print_heading("1. OVERALL DEPRESSION ANALYSIS")

    total = len(data)
    yes_count = count_reported(data)
    no_count = total - yes_count
    yes_percent = calculate_percentage(yes_count, total)
    no_percent = calculate_percentage(no_count, total)

    print(f"Total students                             : {total}")
    print(f"Students reporting depression (Yes)        : {yes_count}")
    print(f"Students not reporting depression (No)     : {no_count}")
    print()
    print("Percentage of each group (out of all students):")
    responses = {"Reporting depression (Yes)": yes_percent, "Not reporting depression (No)": no_percent}
    for answer, percent in responses.items():
        print(f"  {answer:<30}: {percent:.1f}%")

    print("\nInsight:")
    print(f"  About {yes_percent:.0f} out of every 100 students in this dataset answered 'Yes'.")
    if yes_percent > no_percent:
        print("  Most students answered 'Yes'.")
    else:
        print("  Most students answered 'No'.")
    print("  This is the overall figure. The next options compare the percentage")
    print("  inside each category, so you can see how it differs between groups.")
    print_disclaimer()


def show_age_analysis(data):
    """Menu 2: reported cases and percentages for each age group."""
    print_heading("2. AGE-WISE DEPRESSION ANALYSIS")
    data = add_age_group(data)
    outside = int(data["Age_Group"].isna().sum())

    run_category_analysis(data, "Age_Group", "Age group")
    if outside > 0:
        print(f"\n{outside} students are outside the age groups 17-28 and were not counted above.")


def show_gender_analysis(data):
    """Menu 3: reported cases and percentages for each gender."""
    print_heading("3. GENDER-WISE DEPRESSION ANALYSIS")
    rows = run_category_analysis(data, "Gender", "Gender")

    print()
    for row in rows:
        print(f"Total {row['Label'].lower()} students: {row['Students']}")
    print_two_category_comparison(rows, "gender")


def show_semester_analysis(data):
    """Menu 4: reported cases and percentages for each Current_semester value."""
    print_heading("4. SEMESTER-WISE DEPRESSION ANALYSIS")
    run_category_analysis(data, "Current_semester", "Semester")
    print("\nSemester values are shown exactly as recorded in the file")
    print("(including any 0 or unusually high values; the file does not explain them).")


def show_family_analysis(data):
    """Menu 5: reported cases and percentages for each family background."""
    print_heading("5. FAMILY BACKGROUND ANALYSIS")
    run_category_analysis(data, "Family_background", "Family background")


def show_relationship_analysis(data):
    """Menu 6: reported cases and percentages for each relationship status."""
    print_heading("6. RELATIONSHIP STATUS ANALYSIS")
    run_category_analysis(data, "Relationship_status", "Relationship status")


def show_living_analysis(data):
    """Menu 7: reported cases and percentages for each living arrangement."""
    print_heading("7. LIVING ARRANGEMENT ANALYSIS")
    rows = run_category_analysis(data, "Living_style", "Living arrangement")
    print_two_category_comparison(rows, "living arrangement")


def show_health_analysis(data):
    """Menu 8: reported cases and percentages for each health condition."""
    print_heading("8. HEALTH CONDITION ANALYSIS")
    rows = run_category_analysis(data, "Health_condition", "Health condition")

    if has_perfect_split(rows):
        print_perfect_split_caution("health-condition")


def get_gap(finding):
    """Return the gap stored in one finding (used to sort the findings)."""
    return finding["Gap"]


def show_complete_report(data):
    """Menu 9: combine the major findings from every analysis in one report."""
    print_heading("9. COMPLETE DEPRESSION REPORT")

    print("Dataset summary")
    print(f"  Student records : {len(data)}")
    print(f"  Columns         : {data.shape[1]}")
    print(f"  Missing values  : {int(data.isna().sum().sum())}")
    print(f"  Duplicate rows  : {int(data.duplicated().sum())}")

    total = len(data)
    yes_count = count_reported(data)
    print("\nOverall")
    print(f"  Reporting depression (Yes)    : {yes_count} students "
          f"({calculate_percentage(yes_count, total):.1f}% of all students)")
    print(f"  Not reporting depression (No) : {total - yes_count} students "
          f"({calculate_percentage(total - yes_count, total):.1f}% of all students)")

    print_reading_note()

    work = add_age_group(data)
    findings = []
    caution_titles = []
    number = 1
    for category in CATEGORIES:
        rows = summarise_groups(work, category["column"])
        most = find_most_cases(rows)
        highest = find_highest_percent(rows)
        lowest = find_lowest_percent(rows)

        print(f"\n{number}. {category['title']}\n")
        print_group_table(rows, category["title"])
        print(f"\n  Most reported cases : {most['Label']} ({most['Cases']})")
        print(f"  Highest percentage  : {highest['Label']} ({highest['Percent']:.1f}%)")
        print(f"  Lowest percentage   : {lowest['Label']} ({lowest['Percent']:.1f}%)")

        if has_perfect_split(rows):
            caution_titles.append(category["title"])

        findings.append({
            "Title": category["title"],
            "Highest": highest,
            "Lowest": lowest,
            "Gap": highest["Percent"] - lowest["Percent"],
        })
        number = number + 1

    findings.sort(key=get_gap, reverse=True)
    print("\nCategories ranked by the gap between their highest and lowest percentage")
    print("(groups with fewer than 30 students are ignored)\n")
    for finding in findings:
        print(f"  {finding['Title']:<20} {finding['Gap']:>5.1f} points   "
              f"({finding['Highest']['Label']} {finding['Highest']['Percent']:.1f}% "
              f"vs {finding['Lowest']['Label']} {finding['Lowest']['Percent']:.1f}%)")

    for title in caution_titles:
        print_perfect_split_caution(title)

    print("\nSummary:")
    print("  A larger gap means the reported percentage varies more between the groups of")
    print("  that category in this dataset. It does not show why the groups differ.")
    print("  Reported cases (counts) and percentages within a category answer different")
    print("  questions, so always read them together.")
    print_disclaimer()


def print_menu():
    """Show the main menu."""
    print()
    print("STUDENT DEPRESSION ANALYSIS SYSTEM - MAIN MENU")
    print()
    print(" 1. Overall Depression Analysis")
    print(" 2. Age-wise Depression Analysis")
    print(" 3. Gender-wise Depression Analysis")
    print(" 4. Semester-wise Depression Analysis")
    print(" 5. Family Background Analysis")
    print(" 6. Relationship Status Analysis")
    print(" 7. Living Arrangement Analysis")
    print(" 8. Health Condition Analysis")
    print(" 9. Complete Depression Report")
    print("10. Exit")
    print()


def main():
    """Load and clean the data, then keep showing the menu until the user exits."""
    raw_data = load_data(DATA_FILE)
    if raw_data is None:
        return
    if not check_required_columns(raw_data):
        return

    data = clean_data(raw_data)

    actions = {
        "1": show_overall_analysis,
        "2": show_age_analysis,
        "3": show_gender_analysis,
        "4": show_semester_analysis,
        "5": show_family_analysis,
        "6": show_relationship_analysis,
        "7": show_living_analysis,
        "8": show_health_analysis,
        "9": show_complete_report,
    }

    while True:
        print_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "10":
            print("\nThank you for using the Student Depression Analysis System.")
            print("Remember: these are survey statistics, not medical advice or diagnoses.")
            print("Goodbye!")
            break
        elif choice in actions:
            actions[choice](data)
            wait_for_enter()
        else:
            print("\nInvalid choice. Please enter a number from 1 to 10.")


if __name__ == "__main__":
    main()