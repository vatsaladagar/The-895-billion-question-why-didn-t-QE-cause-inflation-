"""
QE and Inflation Transmission Failures in the UK (2009-2020)
Charts for Substack article by Vatsala Dagar (https://substack.com/@vatsaladagar)

Data Sources:
- Graph 1: ONS CPI Annual Rate, series D7G7 (mm23 dataset)
- Graph 2: ONS Average Weekly Earnings, series KAC2 (emp dataset) + D7G7
- Graph 3: Bank of England Asset Purchase Facility (manually compiled from BoE published statements)
- Graph 4: ONS Households Saving Ratio (SA), series DGD8

Instructions:
- Download D7G7 from: https://www.ons.gov.uk/economy/inflationandpriceindices/timeseries/d7g7/mm23
- Download KAC2 (full emp dataset) from: https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/datasets/averageweeklyearningsemp
- Download DGD8 (saving ratio SA) from: https://www.ons.gov.uk/economy/nationalaccounts/satelliteaccounts/timeseries/dgd8/ukea
- Save all CSVs in the same folder as this script and update file paths below
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.patches as mpatches
import warnings
warnings.filterwarnings('ignore')

# ── File paths — update these to match your local CSV locations ───────────────
CPI_CSV     = "series-060626__2_.csv"   # D7G7 annual CPI
WAGES_CSV   = "emp.csv"                  # full AWE dataset (KAC2 at column 438)
SAVINGS_CSV = "series-060626.csv"        # DGD8 saving ratio SA

# ── Output folder — charts saved here ─────────────────────────────────────────
OUTPUT_DIR = ""   # leave empty to save in same folder, or set e.g. "charts/"

# ── Shared style ──────────────────────────────────────────────────────────────
NAVY   = "#1a1a2e"
ORANGE = "#e07b39"
GRAY   = "#7A7060"
BG     = "#F5ECD7"


def base_ax(fig, ax):
    """Apply consistent style — cream background, x/y axes only, no grid."""
    ax.set_facecolor(BG)
    fig.patch.set_facecolor(BG)
    for spine in ['top', 'right', 'left']:
        ax.spines[spine].set_visible(False)
    ax.spines['bottom'].set_color('#CCCCCC')
    ax.tick_params(colors=GRAY, labelsize=9.5)
    ax.grid(False)


def save(fig, name):
    path = OUTPUT_DIR + name
    fig.savefig(path, dpi=180, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"Saved: {path}")


# ══════════════════════════════════════════════════════════════════════════════
# GRAPH 1 — UK CPI Inflation 2005–2020 (annual, ONS D7G7)
# ══════════════════════════════════════════════════════════════════════════════

# Annual CPI values (%) — sourced from ONS D7G7
cpi_data = {
    2005: 2.1, 2006: 2.3, 2007: 2.3, 2008: 3.6, 2009: 2.2,
    2010: 3.3, 2011: 4.5, 2012: 2.8, 2013: 2.6, 2014: 1.5,
    2015: 0.0, 2016: 0.7, 2017: 2.7, 2018: 2.5, 2019: 1.8, 2020: 0.9
}

years_cpi = list(cpi_data.keys())
vals_cpi  = list(cpi_data.values())

fig, ax = plt.subplots(figsize=(10, 5.5))
base_ax(fig, ax)

ax.fill_between(years_cpi, vals_cpi, alpha=0.10, color=NAVY)
ax.plot(years_cpi, vals_cpi, color=NAVY, linewidth=2.5, marker='o', markersize=4)

# 2% target reference line
ax.axhline(2.0, color=ORANGE, linewidth=1.5, linestyle='--', alpha=0.8)
ax.text(2005.1, 2.18, '2% Target', fontsize=9, color=ORANGE)

# Annotate supply shock episodes
ax.annotate('VAT hike +\nenergy spike',
            xy=(2011, 4.5), xytext=(2011.4, 5.1),
            fontsize=8, color=GRAY,
            arrowprops=dict(arrowstyle='->', color=GRAY, lw=0.8))
ax.annotate('Sterling\ncollapse',
            xy=(2017, 2.7), xytext=(2017.4, 3.3),
            fontsize=8, color=GRAY,
            arrowprops=dict(arrowstyle='->', color=GRAY, lw=0.8))

ax.set_xlim(2004.5, 2020.5)
ax.set_ylim(-0.5, 5.8)
ax.set_xticks(years_cpi)
ax.set_xticklabels([str(y) for y in years_cpi], rotation=45, ha='right')
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:.1f}%"))
ax.set_title("UK CPI Inflation, 2009–2020",
             fontsize=13, color=ORANGE, fontweight='bold', pad=14, loc='center')
ax.text(0.99, -0.20,
        "Source: ONS Consumer Prices Index, series D7G7. "
        "Exceedances above 2% target driven by external supply shocks, not domestic demand.",
        transform=ax.transAxes, fontsize=8, color=GRAY, ha='right', style='italic')

save(fig, "graph1_cpi.png")


# ══════════════════════════════════════════════════════════════════════════════
# GRAPH 2 — Nominal Wage Growth vs CPI Inflation 2005–2020
#            Wages: ONS KAC2 (monthly), CPI: annual values from above
# ══════════════════════════════════════════════════════════════════════════════

# Load full AWE dataset and extract KAC2 (column index 438)
df_wages = pd.read_csv(WAGES_CSV, header=None, skiprows=7)
wages_raw = pd.DataFrame({
    'date': df_wages[0],
    'wage': pd.to_numeric(df_wages[438], errors='coerce')
})
wages_raw = wages_raw.dropna(subset=['wage'])

# Keep only monthly rows (format: "2009 JAN")
wages_raw = wages_raw[wages_raw['date'].astype(str).str.match(r'^\d{4} [A-Z]{3}$')]

month_map = {'JAN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4, 'MAY': 5, 'JUN': 6,
             'JUL': 7, 'AUG': 8, 'SEP': 9, 'OCT': 10, 'NOV': 11, 'DEC': 12}

wages_raw['year']     = wages_raw['date'].str[:4].astype(int)
wages_raw['month']    = wages_raw['date'].str[5:].map(month_map)
wages_raw['date_num'] = wages_raw['year'] + (wages_raw['month'] - 1) / 12

wages_m = wages_raw[
    (wages_raw['year'] >= 2005) & (wages_raw['year'] <= 2020)
].sort_values('date_num')

# Expand annual CPI to monthly for overlay
cpi_m_x, cpi_m_y = [], []
for y, v in cpi_data.items():
    for m in range(1, 13):
        cpi_m_x.append(y + (m - 1) / 12)
        cpi_m_y.append(v)

fig, ax = plt.subplots(figsize=(10, 5.5))
base_ax(fig, ax)

ax.plot(wages_m['date_num'], wages_m['wage'],
        color=NAVY, linewidth=2, label='Nominal wage growth (KAC2)', alpha=0.9)
ax.plot(cpi_m_x, cpi_m_y,
        color=ORANGE, linewidth=1.8, linestyle='--', label='CPI inflation (D7G7)', alpha=0.85)
ax.axhline(0, color='#CCCCCC', linewidth=0.8)

ax.set_xlim(2004.5, 2020.5)
ax.set_xticks(list(range(2005, 2021)))
ax.set_xticklabels([str(y) for y in range(2005, 2021)], rotation=45, ha='right')
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:.1f}%"))
ax.set_title("UK Nominal Wage Growth vs CPI Inflation, 2009–2020",
             fontsize=13, color=ORANGE, fontweight='bold', pad=14, loc='center')
ax.legend(fontsize=9.5, frameon=False, loc='upper right')
ax.text(0.99, -0.20,
        "Source: ONS Average Weekly Earnings series KAC2; ONS CPI series D7G7. "
        "Real wages were effectively flat for much of the decade.",
        transform=ax.transAxes, fontsize=8, color=GRAY, ha='right', style='italic')

save(fig, "graph2_wages_cpi.png")


# ══════════════════════════════════════════════════════════════════════════════
# GRAPH 3 — BoE Cumulative Asset Purchases by QE Round 2009–2020
#            Manually compiled from BoE published statements
# ══════════════════════════════════════════════════════════════════════════════

# Cumulative stock (£bn) at end of each year
# QE1: £200bn (Mar 2009 – Feb 2010)
# QE2: £175bn additional (Oct 2011 – Nov 2012) → total £375bn
# QE3: £70bn additional (Aug 2016 – Feb 2017) → total £445bn
# QE4: £450bn additional (Mar 2020 – Dec 2020) → total £895bn (partial year shown as £745bn)
annual_qe = {
    2009: 75,   # partial year QE1
    2010: 200,  # QE1 complete
    2011: 275,  # QE2 begins
    2012: 375,  # QE2 complete
    2013: 375,
    2014: 375,
    2015: 375,
    2016: 415,  # QE3 begins
    2017: 445,  # QE3 complete
    2018: 445,
    2019: 445,
    2020: 745   # QE4 partial (to Dec 2020)
}

xs = list(annual_qe.keys())
ys = [v / 1000 for v in annual_qe.values()]  # convert to £ trillions

fig, ax = plt.subplots(figsize=(10, 5.5))
base_ax(fig, ax)

ax.fill_between(xs, ys, alpha=0.12, color=NAVY, step='post')
ax.step(xs, ys, where='post', color=NAVY, linewidth=2.5)

# Annotate each QE round
annotations = [
    (2009.15, 0.04,  "QE1: £200bn\nMar 2009", 0.18),
    (2011.15, 0.22,  "QE2: £175bn\nOct 2011", 0.38),
    (2016.15, 0.36,  "QE3: £70bn\nAug 2016",  0.50),
    (2020.05, 0.58,  "QE4: £450bn\nMar 2020", 0.76),
]
for x, y_tip, label, y_txt in annotations:
    ax.annotate(label,
                xy=(x, y_tip), xytext=(x, y_txt),
                fontsize=8.5, color=NAVY,
                arrowprops=dict(arrowstyle='-', color='#CCCCCC', lw=1),
                bbox=dict(boxstyle='round,pad=0.3', fc=BG, ec='#CCCCCC', lw=0.8))

ax.set_xlim(2008.5, 2021)
ax.set_ylim(0, 0.95)
ax.set_xticks(range(2009, 2021))
ax.set_xticklabels([str(y) for y in range(2009, 2021)], rotation=45, ha='right')
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"£{x:.2f}tr"))
ax.set_title("Bank of England Cumulative Asset Purchases, 2009–2020",
             fontsize=13, color=ORANGE, fontweight='bold', pad=14, loc='center')
ax.text(0.99, -0.20,
        "Source: Bank of England Asset Purchase Facility published statements. "
        "Each new round reflected continued economic weakness, not success.",
        transform=ax.transAxes, fontsize=8, color=GRAY, ha='right', style='italic')

save(fig, "graph3_qe_purchases.png")


# ══════════════════════════════════════════════════════════════════════════════
# GRAPH 4 — UK Household Saving Ratio 2005–2020 (ONS DGD8, SA)
# ══════════════════════════════════════════════════════════════════════════════

savings_raw = pd.read_csv(SAVINGS_CSV, skiprows=8, header=None, names=['year', 'rate'])
savings_raw['year'] = pd.to_numeric(savings_raw['year'], errors='coerce')
savings_raw['rate'] = pd.to_numeric(savings_raw['rate'], errors='coerce')
savings = savings_raw.dropna().query("2005 <= year <= 2020").copy()

pre_avg  = savings.query("year <= 2007")['rate'].mean()
peak_row = savings.loc[savings['rate'].idxmax()]

fig, ax = plt.subplots(figsize=(10, 5.5))
base_ax(fig, ax)

ax.fill_between(savings['year'], savings['rate'], alpha=0.10, color=NAVY)
ax.plot(savings['year'], savings['rate'],
        color=NAVY, linewidth=2.5, marker='o', markersize=4)

# Shade GFC period
ax.axvspan(2008, 2009.5, alpha=0.07, color=ORANGE)

# Pre-crisis average reference line
ax.axhline(pre_avg, color=ORANGE, linewidth=1.3, linestyle='--', alpha=0.75)
ax.text(2005.1, pre_avg + 0.4, f"Pre-crisis avg: {pre_avg:.1f}%", fontsize=8.5, color=ORANGE)

# Annotate peak
ax.annotate(f"Peak: {peak_row['rate']:.1f}%\n({int(peak_row['year'])})",
            xy=(peak_row['year'], peak_row['rate']),
            xytext=(peak_row['year'] + 1.2, peak_row['rate'] + 0.8),
            fontsize=8.5, color=NAVY,
            arrowprops=dict(arrowstyle='->', color=GRAY, lw=0.9),
            bbox=dict(boxstyle='round,pad=0.3', fc=BG, ec='#CCCCCC', lw=0.8))

gfc_patch = mpatches.Patch(color=ORANGE, alpha=0.2, label='GFC 2008–09')
ax.legend(handles=[gfc_patch], fontsize=9, frameon=False, loc='upper right')

ax.set_xlim(2004.5, 2020.5)
ax.set_xticks(list(range(2005, 2021)))
ax.set_xticklabels([str(y) for y in range(2005, 2021)], rotation=45, ha='right')
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:.0f}%"))
ax.set_title("UK Household Saving Ratio, 2009–2020",
             fontsize=13, color=ORANGE, fontweight='bold', pad=14, loc='center')
ax.text(0.99, -0.20,
        "Source: ONS Households saving ratio (SA), series DGD8. "
        "Post-crisis savings surge reflects balance sheet repair, not confidence.",
        transform=ax.transAxes, fontsize=8, color=GRAY, ha='right', style='italic')

save(fig, "graph4_savings_rate.png")

print("\nAll 4 charts generated successfully.")
