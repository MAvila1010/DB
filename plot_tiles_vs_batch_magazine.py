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

    # Extract batch number and magazine character from BARCODE
    df['Batch'] = df['BARCODE'].str[7:11]  # Extracting the batch number
    df['Magazine'] = df['BARCODE'].str[11]  # Extracting the magazine character

    # Group by batch and magazine, count number of tiles in each group
    batch_magazine_counts = df.groupby(['Batch', 'Magazine']).size().unstack(fill_value=0)

    # Plot number of tiles by batch, with breakdown by magazines
    ax = batch_magazine_counts.plot(kind='bar', stacked=True, figsize=(12, 6))
    plt.xlabel('Batch')
    plt.ylabel('Number of Tiles')
    plt.title('Number of Tiles by Batch (Breakdown by Magazines)')
    plt.legend(title='Magazine', bbox_to_anchor=(1, 1))
    plt.xticks(rotation=0)  # Set x-axis labels to be horizontal
    plt.tight_layout()

    # Create a mapping from the x-coordinate to the batch label
    x_labels = batch_magazine_counts.index
    x_mapping = {i: label for i, label in enumerate(x_labels)}

    # Initialize cumulative heights dictionary using batch labels as keys
    cumulative_heights = {label: 0 for label in x_labels}

    for p in ax.patches:
        height = p.get_height()
        if height > 0:
            # Extract the batch index from the patch and map it to the batch label
            x_index = int(p.get_x() + p.get_width() / 2)
            batch_label = x_mapping.get(x_index, None)
            if batch_label is not None:
                y = cumulative_heights[batch_label] + height / 2
                ax.annotate(str(int(height)), (p.get_x() + p.get_width() / 2., y),
                            ha='center', va='center', xytext=(0, 5), textcoords='offset points')
                cumulative_heights[batch_label] += height  # Update cumulative height for this batch

    plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 plot_tiles.py <csv_file>")
        sys.exit(1)

    csv_file = sys.argv[1]
    plot_tiles(csv_file)
