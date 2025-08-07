import pandas as pd
import os
from evidently import Report
from evidently.presets import DataDriftPreset

reference_path = "data/processed/neo_data_balanced.csv"
current_path = "data/processed/neo_data.csv"
report_path = "monitoring/reports/drift_report.html"

df_reference = pd.read_csv(reference_path)
df_current = pd.read_csv(current_path)

report = Report([DataDriftPreset(),])

report = report.run(df_reference, df_current)

os.makedirs("reports", exist_ok=True)
report.save_html(report_path)

print(f"Report salvo em {report_path}")