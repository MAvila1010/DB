import pandas as pd
from datetime import datetime

def convert_size(size):
    if size.startswith('HD'):
        return f'F{size[2]}'  # Handling F1, F2, F3 tiles
    else:
        parts = size.split('-')
        return f'{min(int(parts[0]), int(parts[1])):02d}'

def generate_files(excel_file):
    df = pd.read_excel(excel_file, header=4)

    # Group rows by batch number and size for processing
    grouped_df = df.groupby([df['BATCH'].str[1:5], df['SIZE']])  # Group by batch number (2nd to 5th chars) and size

    for (batch_number, size), batch_group in grouped_df:
        fabricated_data = []
        prod_qc_data = []

        # Process each row within the grouped batch and size
        for index, row in batch_group.iterrows():
            # Convert 'MADE' to string and format to 'YYYY-MM-DD'
            try:
                made_date = row['MADE'].strftime('%Y-%m-%d') if isinstance(row['MADE'], datetime) else datetime.strptime(str(row['MADE']), '%m/%d/%Y').strftime('%Y-%m-%d')
            except ValueError:
                made_date = datetime.strptime(str(row['MADE']), '%m/%d/%y').strftime('%Y-%m-%d')  # In case of a 2-digit year format

            magazine_label = row['BATCH'][6]  # Extract the 6th character (magazine label)
            fabricated_count = int(row['FABRICATED'])
            prod_qc_count = int(row['PROD-QC'])
            size_converted = convert_size(size)

            # Generate first file based on FABRICATED count
            for i in range(1, fabricated_count + 1):
                serial_number = f'{batch_number}-{magazine_label}-{i:03d}'
                barcode = f'320BC{size_converted}{batch_number}{magazine_label}{i:03d}'
                name_label = f'Bare Cast Tile BH Ring {size_converted} SN {serial_number}'
                fabricated_data.append([
                    f'BC-{size_converted}', batch_number, serial_number, barcode, 'NIU', 'NIU', 'NIU', name_label, made_date
                ])

            # Generate second file based on PROD-QC count
            for i in range(1, prod_qc_count + 1):
                serial_number = f'{batch_number}-{magazine_label}-{i:03d}'
                barcode = f'320TC{size_converted}{batch_number}{magazine_label}{i:03d}'
                name_label = f'Wrap Cast Tile BH Ring {size_converted} SN {serial_number}'
                made_from_typecode = f'BC-{size_converted}'
                made_from_sn = f'{batch_number}-{magazine_label}-{i:03d}'
                prod_qc_data.append([
                    f'TC-{size_converted}', batch_number, serial_number, barcode, 'NIU', 'NIU', 'NIU', name_label, made_date, made_from_typecode, made_from_sn
                ])

        # Keep the original naming scheme
        if fabricated_data:
            fabricated_file_name = f'{fabricated_data[0][3][:11]}.csv'  # Same naming scheme based on barcode
            fabricated_df = pd.DataFrame(fabricated_data, columns=['LABEL_TYPECODE', 'BATCH_NUMBER', 'SERIAL_NUMBER', 'BARCODE', 'LOCATION', 'INSTITUTION', 'MANUFACTURER', 'NAME_LABEL', 'PRODUCTION_DATE'])
            fabricated_df.to_csv(fabricated_file_name, index=False)

        if prod_qc_data:
            prod_qc_file_name = f'{prod_qc_data[0][3][:11]}.csv'  # Same naming scheme based on barcode
            prod_qc_df = pd.DataFrame(prod_qc_data, columns=['LABEL_TYPECODE', 'BATCH_NUMBER', 'SERIAL_NUMBER', 'BARCODE', 'LOCATION', 'INSTITUTION', 'MANUFACTURER', 'NAME_LABEL', 'PRODUCTION_DATE', 'MADE-FROM-TYPECODE[1]', 'MADE-FROM-SN[1]'])
            prod_qc_df.to_csv(prod_qc_file_name, index=False)

generate_files('Tiles.xlsx')
