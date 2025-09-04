import pandas as pd
import requests
import os


excel_file_path = 'items_data.xlsx'

sheet_name = 'Sheet1'  

download_folder = 'photos'

failed_log_file = "failed_photos.txt"


os.makedirs(download_folder, exist_ok=True)


df = pd.read_excel(excel_file_path, sheet_name=sheet_name)


links = df.iloc[:, 22].tolist()

barcodes = df.iloc[:, 4].tolist()

for index, (url, barcode) in enumerate(zip(links, barcodes)):
    try:
        response = requests.get(url)
        response.raise_for_status()

        
        barcode_str = str(barcode).rstrip('.0')

        
        content_type = response.headers.get('Content-Type')
        if 'image/png' in content_type:
            extension = 'png'
        elif 'image/jpeg' in content_type:
            extension = 'jpeg'
        elif 'image/jpg' in content_type:
            extension = 'jpg'            
        else:
            print(f'Unsupported image format for {url}. Skipping...')
            continue
        
        # Use the cleaned barcode as the filename
        filename = os.path.join(download_folder, f'{barcode_str}.{extension}')
        
        
        with open(filename, 'wb') as file:
            file.write(response.content)
        
        print(f'Downloaded: {filename}')
        print(f'{index}')
    except Exception as e:
        print(f'Failed to download {url}: {e}') 
        with open(failed_log_file, 'a') as f:
            f.write(f"{barcode} | {url} \n") 
        