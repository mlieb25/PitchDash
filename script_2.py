
# Create requirements.txt
requirements_content = """streamlit==1.28.0
pandas==2.1.0
numpy==1.24.3
plotly==5.17.0
python-dateutil==2.8.2
"""

with open(f'{base_dir}/requirements.txt', 'w') as f:
    f.write(requirements_content)

print("✓ Created requirements.txt")

# Create .streamlit/config.toml for custom styling
config_toml = """[theme]
primaryColor = "#0066CC"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[server]
headless = true
port = 8501
enableCORS = false
"""

with open(f'{base_dir}/.streamlit/config.toml', 'w') as f:
    f.write(config_toml)

print("✓ Created .streamlit/config.toml")
