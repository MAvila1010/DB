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

    # Extract tile size from BARCODE
    df['Tile_Size'] = df['BARCODE'].str[5:7]

    # Count the number of tiles for each tile size
    tile_counts = df['Tile_Size'].value_counts().sort_index()

    # Plot number of tiles by tile size
    plt.figure(figsize=(10, 6))
    ax = tile_counts.plot(kind='bar')
    plt.xlabel('Tile Size')
    plt.ylabel('Number of Tiles')
    plt.title('Number of Tiles by Tile Size')
    plt.grid(True, axis='y')  # only horizontal grid lines
    plt.xticks(rotation=0)  # horizontal x-axis labels

    # Add totals on top of each bar
    for p in ax.patches:
        height = p.get_height()
        ax.annotate(str(int(height)), (p.get_x() + p.get_width() / 2., height),
                    ha='center', va='center', xytext=(0, 5), textcoords='offset points')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 plot_tiles.py <csv_file>")
        sys.exit(1)

    csv_file = sys.argv[1]
    plot_tiles(csv_file)
