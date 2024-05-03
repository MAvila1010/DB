import pandas as pd

# Read the original Excel file
df = pd.read_excel("Wrapped.xlsx")

# Drop empty rows
df = df.dropna(subset=['Number_of_Tiles', 'Vendor_Plate_Number'])

# Define a function to format the SERIAL_NUMBER
def format_serial(row):
    magazine_number = row['Magazine_Number']
    if isinstance(magazine_number, int):
        magazine_number = int(magazine_number)
    return [f"{int(row['Vendor_Plate_Number']):04d}-{str(magazine_number).split('.')[0]}-{str(i).zfill(3)}" for i in range(1, int(row['Number_of_Tiles']) + 1)]

# Apply formatting functions to create new columns
df['LABEL_TYPECODE'] = df['Tile_Size'].apply(lambda x: f"BC-{str(x).split('.')[0].zfill(2)}")
df['BATCH_NUMBER'] = df['Vendor_Plate_Number']
df['SERIAL_NUMBER'] = df.apply(lambda row: format_serial(row), axis=1)
df = df.explode('SERIAL_NUMBER')
df['BARCODE'] = '320BC' + df['SERIAL_NUMBER']
df['LOCATION'] = 'NIU'
df['INSTITUTION'] = 'NIU'
df['MANUFACTURER'] = 'NIU'
df['NAME_LABEL'] = df.apply(lambda row: f"Bare Cast Tile BH Ring {str(row['Tile_Size']).split('.')[0].zfill(2)} SN {row['SERIAL_NUMBER']}", axis=1)
df['PRODUCTION_DATE'] = df['Date_Produced'].dt.strftime('%Y-%m-%d')

# Select and reorder columns
df = df[['LABEL_TYPECODE', 'BATCH_NUMBER', 'SERIAL_NUMBER', 'BARCODE', 'LOCATION', 'INSTITUTION', 'MANUFACTURER', 'NAME_LABEL', 'PRODUCTION_DATE']]

# Write the transformed data to a new Excel file
df.to_excel("Bare_Updated.xlsx", index=False)



