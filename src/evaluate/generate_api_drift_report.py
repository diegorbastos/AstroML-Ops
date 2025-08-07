import pandas as pd
from evidently import Report
from evidently.presets import DataDriftPreset

reference_path = "data/processed/neo_data_balanced.csv"
current_path = "monitoring/logs/inferences.csv"
report_output = "monitoring/reports/api_drift_report.html"

df_reference = pd.read_csv(reference_path)
df_current = pd.read_csv(current_path)

common_cols = df_reference.columns.intersection(df_current.columns)
df_reference = df_reference[common_cols]
df_current = df_current[common_cols]

df_current = df_current.drop(columns=["timestamp"], errors="ignore")

report = Report([DataDriftPreset()])
report = report.run(df_reference, df_current)

report.save_html(report_output)

print(f"Relatório de drift salvo em: {report_output}")