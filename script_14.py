
# Create a ZIP file of the entire dashboard for easy download
import zipfile
import os

zip_filename = 'streamlit_investor_dashboard.zip'

def zipdir(path, ziph):
    """Zip directory recursively"""
    for root, dirs, files in os.walk(path):
        # Skip __pycache__ directories
        dirs[:] = [d for d in dirs if d != '__pycache__']
        
        for file in files:
            file_path = os.path.join(root, file)
            arcname = os.path.relpath(file_path, os.path.dirname(path))
            ziph.write(file_path, arcname)

# Create ZIP file
with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipdir(base_dir, zipf)

zip_size = os.path.getsize(zip_filename) / 1024  # Size in KB

print(f"\n✅ Created {zip_filename} ({zip_size:.1f} KB)")
print(f"\nThis ZIP file contains the complete Streamlit dashboard package.")
print(f"You can download it and extract it to deploy the dashboard.")
