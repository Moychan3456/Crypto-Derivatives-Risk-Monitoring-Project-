import pandas as pd
import os

# Load data
script_name = os.path.dirname(os.path.abspath(__file__))
file_path_pos = os.path.join(script_name, 'simulated_positions.csv')
file_path_btc = os.path.join(script_name, 'btc_prices.csv')
file_path_eth = os.path.join(script_name, 'eth_prices.csv')
positions = pd.read_csv(file_path_pos)
btc = pd.read_csv(file_path_btc)
eth = pd.read_csv(file_path_eth)

# Convert numeric columns
positions["Position_Size"] = pd.to_numeric(positions["Position_Size"], errors="coerce")
positions["Leverage"] = pd.to_numeric(positions["Leverage"], errors="coerce")

btc["Close"] = pd.to_numeric(btc["Close"], errors="coerce")
eth["Close"] = pd.to_numeric(eth["Close"], errors="coerce")

# Get latest prices
btc_price = btc["Close"].iloc[-1]
eth_price = eth["Close"].iloc[-1]

price_map = {"BTC": btc_price, "ETH": eth_price}

# Assumptions (institutional policy)
initial_margin_rate = 0.10
maintenance_margin_rate = 0.05
account_equity = 100000   # per trader simulated

results = []

for _, row in positions.iterrows():

    asset_price = price_map[row["Asset"]]
    notional = row["Position_Size"] * asset_price

    initial_margin = notional * initial_margin_rate
    maintenance_margin = notional * maintenance_margin_rate

    margin_utilization = initial_margin / account_equity

    # liquidation distance approximation
    #liquidation_distance = (initial_margin - maintenance_margin) / notional
    entry_price = asset_price
    leverage = row["Leverage"]

    if row["Side"] == "Long":
        liq_price = entry_price * (1 - 1/leverage)
    else:
        liq_price = entry_price * (1 + 1/leverage)

    liquidation_distance = abs(asset_price - liq_price) / asset_price


    # risk flags
    leverage_flag = "BREACH" if row["Leverage"] > 10 else "OK"
    margin_flag = "WARNING" if margin_utilization > 0.70 else "OK"

    results.append([
        row["Trader"],
        row["Asset"],
        row["Side"],
        notional,
        initial_margin,
        margin_utilization,
        liquidation_distance,
        leverage_flag,
        margin_flag
    ])

risk_df = pd.DataFrame(results, columns=[
    "Trader",
    "Asset",
    "Side",
    "Notional_Exposure",
    "Initial_Margin",
    "Margin_Utilization",
    "Liquidation_Distance",
    "Leverage_Flag",
    "Margin_Flag"
])

# ---- Desk VaR Calculation (simple historical proxy) ----
portfolio_volatility = 0.04   # assumed daily volatility proxy (4%)
confidence_multiplier = 1.65  # 95% VaR

total_exposure = risk_df["Notional_Exposure"].sum()
desk_var = confidence_multiplier * portfolio_volatility * total_exposure

print(f"Desk 95% VaR: ${desk_var:,.2f}")
with open(os.path.join(script_name, "desk_var.txt"), "w") as f:
    f.write(str(desk_var))


reports_dir = os.path.join(script_name, "reports")
os.makedirs(reports_dir, exist_ok=True)

output_file = os.path.join(reports_dir, "daily_risk_report.csv")
risk_df.to_csv(output_file, index=False)

risk_df.to_csv("daily_risk_report.csv", index=False)


print(risk_df)
