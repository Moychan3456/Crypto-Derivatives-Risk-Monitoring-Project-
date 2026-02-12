import pandas as pd
import os

script_name = os.path.dirname(os.path.abspath(__file__))
file_path_risk = os.path.join(script_name, 'daily_risk_report.csv')
risk_df = pd.read_csv(file_path_risk)

severity_levels = []

for _, row in risk_df.iterrows():

    if row["Margin_Utilization"] > 0.85 or row["Liquidation_Distance"] < 0.05:
        severity = "CRITICAL"

    elif row["Margin_Utilization"] > 0.70:
        severity = "WARNING"

    elif row["Leverage_Flag"] == "BREACH":
        severity = "WARNING"

    else:
        severity = "NORMAL"

    severity_levels.append(severity)

risk_df["Risk_Severity"] = severity_levels

risk_df.to_csv("daily_risk_report_with_severity.csv", index=False)

print(risk_df[["Trader","Asset","Margin_Utilization","Risk_Severity"]])
