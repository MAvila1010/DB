import sys
import pandas as pd
import matplotlib.pyplot as plt

def plot_tiles(csv_file):
    # Read CSV file
    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        print("File not found.")
        return
    except Exception as e:
        print("An error occurred while reading the CSV file:", e)
        return

    # Extract magazine character and number of tiles from SERIAL_NUMBER
    df['Magazine_Character'] = df['SERIAL_NUMBER'].str.extract(r'-(\w)-')
    df['Number_of_Tiles'] = df['SERIAL_NUMBER'].str.extract(r'-(\d+)$').astype(int)

    # Plot number of tiles by magazine characters
    plt.figure(figsize=(10, 6))
    plate_counts = df['Magazine_Character'].value_counts()
    ax = plt.bar(plate_counts.index, plate_counts.values)
    plt.xlabel('Magazine Character')
    plt.ylabel('Number of Tiles')
    plt.title('Number of Tiles by Magazine Character')
    plt.grid(axis='y')  # Only horizontal grid lines
    plt.xticks(rotation=0)  # Horizontal x-axis labels

    # Add totals on top of each bar
    for p in ax:
        height = p.get_height()
        plt.annotate(str(int(height)), (p.get_x() + p.get_width() / 2., height),
                     ha='center', va='center', xytext=(0, 5), textcoords='offset points')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 plot_tiles.py <csv_file>")
        sys.exit(1)

    csv_file = sys.argv[1]
    plot_tiles(csv_file)
