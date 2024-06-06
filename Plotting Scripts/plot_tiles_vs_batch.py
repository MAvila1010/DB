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

    # Extract batch number and number of tiles from SERIAL_NUMBER
    df['Batch_Number'] = df['SERIAL_NUMBER'].str.extract(r'^(\d+)')
    df['Number_of_Tiles'] = df['SERIAL_NUMBER'].str.extract(r'-(\d+)$').astype(int)

    # Count the number of tiles for each batch number and sort by batch number
    batch_counts = df['Batch_Number'].value_counts().sort_index()

    # Plot number of tiles by batch number
    plt.figure(figsize=(10, 6))
    ax = plt.bar(batch_counts.index, batch_counts.values)
    plt.xlabel('Batch Number')
    plt.ylabel('Number of Tiles')
    plt.title('Number of Tiles by Batch Number')
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
