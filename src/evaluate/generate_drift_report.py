import pandas as pd
import os
from evidently import Report
from evidently.presets import DataDriftPreset

def gerar_drift_report(
    reference_path = "data/processed/neo_data_balanced.csv",
    current_path = "data/processed/neo_data.csv",
    report_path = "monitoring/reports/drift_report.html"
):

    df_reference = pd.read_csv(reference_path)
    df_current = pd.read_csv(current_path)

    report = Report([DataDriftPreset(),])

    report = report.run(df_reference, df_current)

    report.save_html(report_path)

    print(f"Report salvo em {report_path}")

if __name__ == "__main__":
    gerar_drift_report()