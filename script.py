
# Create comprehensive Streamlit dashboard application structure
# This will generate a multi-page interactive investor pitch dashboard

import os
import json

# Create the app directory structure
app_structure = {
    'streamlit_investor_dashboard': {
        'app.py': None,  # Main entry point
        'pages': {
            '1_📊_Overview.py': None,
            '2_💰_ROI_Analysis.py': None,
            '3_📈_Financial_Projections.py': None,
            '4_🎯_Investment_Scenarios.py': None,
            '5_📑_Company_Details.py': None
        },
        'data': {},  # Will hold CSV files
        'utils': {
            '__init__.py': '',
            'calculations.py': None,
            'visualizations.py': None
        },
        'assets': {},
        'requirements.txt': None,
        'README.md': None,
        '.streamlit': {
            'config.toml': None
        }
    }
}

def create_directory_structure(base_path, structure):
    """Recursively create directory structure"""
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_directory_structure(path, content)
        else:
            # File to be created later
            pass

# Create base directory
base_dir = 'streamlit_investor_dashboard'
os.makedirs(base_dir, exist_ok=True)
os.makedirs(f'{base_dir}/pages', exist_ok=True)
os.makedirs(f'{base_dir}/data', exist_ok=True)
os.makedirs(f'{base_dir}/utils', exist_ok=True)
os.makedirs(f'{base_dir}/assets', exist_ok=True)
os.makedirs(f'{base_dir}/.streamlit', exist_ok=True)

print("✓ Created directory structure")
print(f"  - {base_dir}/")
print(f"  - {base_dir}/pages/")
print(f"  - {base_dir}/data/")
print(f"  - {base_dir}/utils/")
print(f"  - {base_dir}/assets/")
print(f"  - {base_dir}/.streamlit/")
