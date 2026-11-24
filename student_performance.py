"""
Student Academic Performance Analyzer
Uses Pandas, NumPy, and Matplotlib to analyze student marks.
Run: python student_performance.py
Optional: python student_performance.py data/your_students.csv
CSV columns expected: Student_ID, Name, Math, Science, English, Computer
"""

from pathlib import Path
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

SUBJECTS = ["Math", "Science", "English", "Computer"]
PASS_MARK = 40


def load_data(csv_path: str) -> pd.DataFrame:
    """Load a CSV file and validate the required columns."""
    df = pd.read_csv(csv_path)
    required = ["Student_ID", "Name", *SUBJECTS]
    missing_columns = [col for col in required if col not in df.columns]
    if missing_columns:
        raise ValueError(f"CSV is missing required columns: {missing_columns}")

    for subject in SUBJECTS:
        df[subject] = pd.to_numeric(df[subject], errors="coerce")
        # Treat marks outside 0–100 as invalid/missing.
        df.loc[~df[subject].between(0, 100), subject] = np.nan
    return df


def assign_grade(percentage: float) -> str:
    if pd.isna(percentage):
        return "N/A"
    if percentage >= 90:
        return "A+"
    if percentage >= 80:
        return "A"
    if percentage >= 70:
        return "B"
    if percentage >= 60:
        return "C"
    if percentage >= 50:
        return "D"
    if percentage >= PASS_MARK:
        return "E"
    return "F"


def analyze_data(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate totals, averages, percentages, grades, and pass status."""
    result = df.copy()
    result["Total"] = result[SUBJECTS].sum(axis=1, min_count=1)
    result["Average"] = result[SUBJECTS].mean(axis=1)
    result["Percentage"] = result[SUBJECTS].mean(axis=1)
    result["Grade"] = result["Percentage"].apply(assign_grade)
    result["Result"] = np.where(
        result[SUBJECTS].isna().any(axis=1),
        "Incomplete",
        np.where((result[SUBJECTS] >= PASS_MARK).all(axis=1), "Pass", "Needs Improvement")
    )
    return result


def create_charts(df: pd.DataFrame, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. Average mark in each subject
    subject_averages = df[SUBJECTS].mean()
    plt.figure(figsize=(8, 5))
    subject_averages.plot(kind="bar")
    plt.title("Average Marks by Subject")
    plt.xlabel("Subject")
    plt.ylabel("Average Marks")
    plt.ylim(0, 100)
    plt.tight_layout()
    plt.savefig(output_dir / "subject_averages.png", dpi=150)
    plt.close()

    # 2. Grade distribution
    grade_order = ["A+", "A", "B", "C", "D", "E", "F", "N/A"]
    grade_counts = df["Grade"].value_counts().reindex(grade_order, fill_value=0)
    plt.figure(figsize=(8, 5))
    grade_counts.plot(kind="bar")
    plt.title("Student Grade Distribution")
    plt.xlabel("Grade")
    plt.ylabel("Number of Students")
    plt.tight_layout()
    plt.savefig(output_dir / "grade_distribution.png", dpi=150)
    plt.close()

    # 3. Student percentage comparison
    plot_df = df.dropna(subset=["Percentage"]).sort_values("Percentage", ascending=False)
    plt.figure(figsize=(10, 5))
    plt.bar(plot_df["Name"].astype(str), plot_df["Percentage"])
    plt.title("Student Performance Comparison")
    plt.xlabel("Student")
    plt.ylabel("Percentage")
    plt.ylim(0, 100)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(output_dir / "student_comparison.png", dpi=150)
    plt.close()


def print_summary(df: pd.DataFrame) -> None:
    complete = df.dropna(subset=SUBJECTS)
    print("\n========== ACADEMIC PERFORMANCE SUMMARY ==========")
    print(f"Total students: {len(df)}")
    print(f"Complete records: {len(complete)}")
    print(f"Records with missing/invalid marks: {df[SUBJECTS].isna().any(axis=1).sum()}")
    print("\nMissing values by subject:")
    print(df[SUBJECTS].isna().sum().to_string())

    print("\nAverage marks by subject:")
    print(df[SUBJECTS].mean().round(2).to_string())

    if not complete.empty:
        overall = complete["Percentage"].mean()
        pass_count = (complete["Result"] == "Pass").sum()
        print(f"\nAverage student percentage (complete records): {overall:.2f}%")
        print(f"Students passing every subject: {pass_count}/{len(complete)}")

        top = complete.loc[complete["Percentage"].idxmax()]
        low = complete.loc[complete["Percentage"].idxmin()]
        print(f"Top performer: {top['Name']} ({top['Percentage']:.2f}%)")
        print(f"Lowest complete-record performer: {low['Name']} ({low['Percentage']:.2f}%)")

    weakest_subject = df[SUBJECTS].mean().idxmin()
    strongest_subject = df[SUBJECTS].mean().idxmax()
    print(f"Strongest subject by average: {strongest_subject}")
    print(f"Subject needing most attention by average: {weakest_subject}")
    print("===================================================\n")


def main():
    default_csv = Path(__file__).parent / "data" / "students.csv"
    csv_path = Path(sys.argv[1]) if len(sys.argv) > 1 else default_csv
    output_dir = Path(__file__).parent / "outputs"

    try:
        raw_df = load_data(str(csv_path))
        analyzed_df = analyze_data(raw_df)
        print_summary(analyzed_df)

        output_dir.mkdir(exist_ok=True)
        analyzed_df.to_csv(output_dir / "student_analysis_results.csv", index=False)
        create_charts(analyzed_df, output_dir)
        print(f"Analysis complete. Results and charts saved in: {output_dir.resolve()}")
    except (FileNotFoundError, pd.errors.EmptyDataError, ValueError) as error:
        print(f"Error: {error}")
        print("Check that the CSV path and required columns are correct.")


if __name__ == "__main__":
    main()
