# Student Academic Performance Analyzer

A beginner-friendly Python project that analyzes student marks using **NumPy, Pandas, and Matplotlib**.

## Features
- Loads student records from a CSV file.
- Identifies missing or invalid marks.
- Calculates total, average, percentage, grade, and result.
- Finds subject averages, strongest/weakest subjects, and top/lowest performers.
- Generates three charts: subject averages, grade distribution, and student comparison.
- Saves the analyzed data and charts in the `outputs/` folder.

## Project structure
```text
student_performance_analyzer/
├── data/
│   └── students.csv
├── outputs/
├── student_performance.py
├── requirements.txt
└── README.md
```

## 1. Run in Google Colab
1. Upload `student_performance.py` and `data/students.csv` to Colab, or upload the ZIP and extract it.
2. Install libraries:
   ```python
   !pip install numpy pandas matplotlib
   ```
3. Run:
   ```python
   !python student_performance.py
   ```
4. Open the `outputs` folder to view the CSV results and charts.

## 2. Run in VS Code
1. Install Python and open this project folder in VS Code.
2. Open the terminal and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run:
   ```bash
   python student_performance.py
   ```

To analyze your own CSV:
```bash
python student_performance.py path/to/your_file.csv
```

## CSV format
Your CSV must contain these columns:
`Student_ID, Name, Math, Science, English, Computer`

Marks should be between 0 and 100. Blank or invalid marks are treated as missing. The sample CSV intentionally contains one missing mark to demonstrate missing-value detection.

## Grade scale used
| Percentage | Grade |
|---|---|
| 90–100 | A+ |
| 80–89.99 | A |
| 70–79.99 | B |
| 60–69.99 | C |
| 50–59.99 | D |
| 40–49.99 | E |
| Below 40 | F |

A student is marked **Pass** only when every subject has at least 40 marks. If a subject mark is missing, the record is marked **Incomplete**.

## Output files
- `outputs/student_analysis_results.csv`
- `outputs/subject_averages.png`
- `outputs/grade_distribution.png`
- `outputs/student_comparison.png`

## Tools and concepts
- **NumPy:** numerical handling and conditional result classification.
- **Pandas:** CSV loading, missing-value detection, averages, and tabular analysis.
- **Matplotlib:** visualizing subject averages, grade distribution, and student performance.

## Note
This is an educational demonstration using sample data. Replace the sample CSV with anonymized data when using real student records. Do not upload private student information publicly.
