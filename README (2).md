# The £895 Billion Question: Why Didn't QE Cause Inflation?

**Substack article by Vatsala Dagar** · [vatsaladagar.substack.com](https://substack.com/@vatsaladagar)

> *Britain spent over a decade pumping money into the economy. Prices barely moved. Here's what actually happened — and why the answer is more complicated than it looks.*

---

## Overview

This repository contains the data visualisation code and charts accompanying my Substack piece on quantitative easing and inflation transmission failures in the UK (2009–2020).

The article examines why the Bank of England's £895 billion asset purchase programme — spanning four rounds across eleven years — failed to generate the demand-driven inflation it was designed to produce. The analysis traces the breakdown through five transmission failures: the wealth channel reaching the wrong households, bank credit rotating into mortgages rather than productive investment, fiscal austerity pulling against monetary stimulus, persistent labour market slack, and the mechanical distinction between central bank reserves and real-economy money.

The cross-country comparison (US Fed, ECB) and the 2020 pandemic episode — where direct fiscal transfers produced rapid inflation that a decade of QE could not — anchor the empirical argument.

---

## Charts

All four charts are produced by `qe_charts.py` using publicly available ONS and Bank of England data.

| File | Title | Source Series |
|---|---|---|
| `graph1_cpi.png` | UK CPI Inflation, 2005–2020 | ONS D7G7 |
| `graph2_wages_cpi.png` | UK Nominal Wage Growth vs CPI Inflation, 2005–2020 | ONS KAC2 + D7G7 |
| `graph3_qe_purchases.png` | Bank of England Cumulative Asset Purchases, 2009–2020 | BoE APF statements |
| `graph4_savings_rate.png` | UK Household Saving Ratio, 2005–2020 | ONS DGD8 |

### Graph 1 — UK CPI Inflation, 2005–2020

![UK CPI Inflation](graph1_cpi.png)

CPI inflation tracked at or below the 2% target for most of the QE era. The two exceedances — 2011 (4.5%, VAT hike and energy spike) and 2017 (2.7%, post-Brexit sterling collapse) — were supply-side events, not demand-driven. Underlying inflation was persistently weak.

### Graph 2 — Nominal Wage Growth vs CPI Inflation, 2005–2020

![Wages vs CPI](graph2_wages_cpi.png)

Nominal wage growth collapsed during the GFC and spent most of the subsequent decade hovering around or below CPI. Real wages were effectively flat. In a genuinely demand-driven economy, wages should lead prices; here they trailed them.

### Graph 3 — BoE Cumulative Asset Purchases, 2009–2020

![QE Purchases](graph3_qe_purchases.png)

The step-chart structure tells its own story: each new QE round was not a sign of success but a response to continued failure. QE1 (£200bn, 2009), QE2 (£175bn, 2011–12), QE3 (£70bn, 2016), and the Covid-era QE4 (£450bn, 2020) together reached £895 billion without generating sustained above-target inflation.

### Graph 4 — UK Household Saving Ratio, 2005–2020

![Household Saving Ratio](graph4_savings_rate.png)

Post-crisis households deleveraged rather than spent. The saving ratio surged from a pre-crisis average of 6.6% to 10–11% by 2010 and remained elevated for most of the decade — direct evidence that the credit/spending channel failed. The spike to 16.6% in 2020 reflects pandemic-era forced saving.

---

## Reproducing the Charts

### Requirements

```
pandas
matplotlib
```

Install with:

```bash
pip install pandas matplotlib
```

### Data Downloads

The script requires three ONS time series CSVs. Download them directly from the ONS website:

| Series | Description | Download URL |
|---|---|---|
| D7G7 | CPI Annual Rate | [ONS — D7G7](https://www.ons.gov.uk/economy/inflationandpriceindices/timeseries/d7g7/mm23) |
| KAC2 | Average Weekly Earnings (full emp dataset) | [ONS — emp dataset](https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/datasets/averageweeklyearningsemp) |
| DGD8 | Household Saving Ratio (SA) | [ONS — DGD8](https://www.ons.gov.uk/economy/nationalaccounts/satelliteaccounts/timeseries/dgd8/ukea) |

Save all three CSVs in the same directory as `qe_charts.py`, then update the file path constants at the top of the script:

```python
CPI_CSV     = "series-XXXXXX.csv"   # D7G7 annual CPI
WAGES_CSV   = "emp.csv"             # full AWE dataset (KAC2 at column index 438)
SAVINGS_CSV = "series-XXXXXX.csv"   # DGD8 saving ratio SA
```

Graph 3 (BoE asset purchases) uses manually compiled annual stock figures sourced from Bank of England APF published statements — no additional download required.

### Running

```bash
python qe_charts.py
```

All four charts are saved as `.png` files in the directory specified by `OUTPUT_DIR` (defaults to the same folder as the script).

---

## Key Argument

The article does not claim QE was irrelevant. Academic estimates (Joyce, Tong and Woods, 2011) suggest QE1 alone raised UK GDP by 1.5–2% and added 0.75–1.5 percentage points to inflation relative to the counterfactual. Without it, a deflationary spiral on the Japanese model was plausible.

The claim is narrower: QE stabilised, but could not transform. Five structural constraints broke the transmission:

1. **Two circuits of money.** Central bank reserves cannot leave the interbank system. They become real-economy money only when commercial banks lend — which requires willing lenders and willing borrowers. Post-2008 UK had neither.
2. **The wealth channel reached the wrong households.** Asset prices rose, but financial assets are concentrated among high-wealth households with low marginal propensity to consume.
3. **Credit went to mortgages, not businesses.** The share of bank lending to residential mortgages rose from 39.7% (2008) to 54% post-crisis; lending to non-financial firms fell from 11.6% to 9.6%.
4. **Fiscal austerity pulled in the opposite direction.** The 2010 coalition programme was contractionary throughout the period QE was trying to stimulate demand.
5. **Labour market slack suppressed wage growth.** High underemployment and near-zero productivity growth meant employers could not afford — and employees could not demand — the wage increases that demand-driven inflation requires.

The 2020 comparison is the natural experiment: direct fiscal transfers bypassed the banking system entirely, created real-economy deposits immediately, and when that spending power met supply disruptions, inflation followed rapidly. Same country. Same central bank. Completely different transmission mechanism. Completely different outcome.

---

## Data Sources

- ONS Consumer Prices Index, series D7G7 (mm23 dataset)
- ONS Average Weekly Earnings, series KAC2 (emp dataset)
- ONS Household Saving Ratio (SA), series DGD8
- Bank of England Asset Purchase Facility published statements
- Bank of England APF Quarterly Report, Q1 2026
- Joyce, Tong and Woods (2011), *Bank of England Quarterly Bulletin*
- Broadbent (2015), Society of Business Economists speech
- Crafts (2017), *National Institute Economic Review*
- OBR Economic and Fiscal Outlooks (various)

---

## Author

**Vatsala Dagar** — MSc Economics & Policy, King's College London  
Substack: [vatsaladagar.substack.com](https://substack.com/@vatsaladagar)  
GitHub: [github.com/vatsaladagar](https://github.com/vatsaladagar)
