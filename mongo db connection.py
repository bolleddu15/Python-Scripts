import pydicom
from pymongo import MongoClient
import os

# Establish connection with MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['cancer_chest_db']
collection = db['dicom_files']

# Load DICOM file with the corrected path
dicom_file_path = r'C:\vscode folders\Chest_cancer deployment\0007d316f756b3fa0baea2ff514ce945.dicom'
dicom_data = pydicom.dcmread(dicom_file_path)

# Save DICOM file to local file system (adjust path as needed)
save_path = r'C:\vscode folders\dicom_storage'
if not os.path.exists(save_path):
    os.makedirs(save_path)
dicom_file_name = os.path.basename(dicom_file_path)
dicom_save_path = os.path.join(save_path, dicom_file_name)
dicom_data.save_as(dicom_save_path)

# Store only the file reference in MongoDB
document = {
    'file_path': dicom_save_path
}

collection.insert_one(document)

print(f"DICOM file stored at: {dicom_save_path}")
