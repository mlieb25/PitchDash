
# Copy all existing CSV data files to the data directory
import shutil

csv_files = [
    'income_statement.csv',
    'balance_sheet.csv',
    'cash_flow_statement.csv',
    'key_metrics.csv',
    'operational_metrics.csv',
    'financial_summary.csv',
    'funding_rounds_overview.csv',
    'investor_roi_summary.csv',
    'financial_projections_2015_2030.csv',
    'series_b_exit_scenarios.csv',
    'series_c_exit_scenarios.csv',
    'ownership_evolution.csv'
]

for csv_file in csv_files:
    if os.path.exists(csv_file):
        shutil.copy(csv_file, f'{base_dir}/data/{csv_file}')
        print(f"✓ Copied {csv_file}")

# Also copy the JSON file
if os.path.exists('investor_pitch_summary.json'):
    shutil.copy('investor_pitch_summary.json', f'{base_dir}/data/investor_pitch_summary.json')
    print(f"✓ Copied investor_pitch_summary.json")

print(f"\n✓ All data files copied to {base_dir}/data/")
