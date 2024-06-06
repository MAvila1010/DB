import tkinter as tk
from tkinter import messagebox
import csv
from datetime import datetime
import os

class ModuleAssemblyGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Module Assembly")

        # Configure root window to expand
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        
        # Frame for trapezoidal boxes
        self.squares_frame = tk.Frame(root)
        self.squares_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.squares_frame.rowconfigure(tuple(range(8)), weight=1)
        self.squares_frame.columnconfigure(tuple(range(8)), weight=1)
        
        self.squares = []
        for i in range(8):  # 8 rows
            row = []
            for j in range(8):  # 8 columns
                square = tk.Label(self.squares_frame, bg='red', width=4, height=2, relief="ridge", justify="center")
                square.grid(row=i, column=j, padx=5, pady=5, sticky="nsew")
                if j > 0:
                    square.lower()  # Lower the current widget to the bottom of the stacking order
                row.append(square)
            self.squares.append(row)
        
        # Frame for input boxes
        self.inputs_frame = tk.Frame(root)
        self.inputs_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        self.inputs_frame.rowconfigure(tuple(range(35)), weight=1)  # Add extra rows for titles and filename input
        self.inputs_frame.columnconfigure(0, weight=1)
        self.inputs_frame.columnconfigure(1, weight=1)
        
        # Title label for Tile Board
        self.title_label = tk.Label(self.inputs_frame, text="Tile Board")
        self.title_label.grid(row=0, column=0, columnspan=2, padx=5, pady=2)

        # Input box for filename
        self.filename_var = tk.StringVar()
        self.filename_var.trace_add('write', self.check_existing_file)
        self.filename_entry = tk.Entry(self.inputs_frame, textvariable=self.filename_var)
        self.filename_entry.grid(row=1, column=0, columnspan=2, padx=5, pady=2, sticky="ew")

        # Title label for Tiles
        self.tiles_label = tk.Label(self.inputs_frame, text="Tiles")
        self.tiles_label.grid(row=2, column=0, columnspan=2, padx=5, pady=2)

        self.input_vars = []
        self.inputs = []
        for i in range(64):
            var = tk.StringVar()
            var.trace_add('write', lambda name, index, mode, var=var, idx=i: self.update_square(var, idx))
            entry = tk.Entry(self.inputs_frame, textvariable=var)
            entry.grid(row=i % 32 + 3, column=i // 32, padx=5, pady=2, sticky="nsew")
            self.input_vars.append(var)
            self.inputs.append(entry)

            # Bind events to change square color on hover
            entry.bind("<Enter>", lambda event, idx=i: self.highlight_square(idx))
            entry.bind("<Leave>", lambda event, idx=i: self.reset_square(idx))
        
        # Preparation Date
        self.prep_date_label = tk.Label(root, text="Preparation Date")
        self.prep_date_label.grid(row=3, column=0, padx=5, pady=2, sticky="e")

        self.prep_date_var = tk.StringVar()
        self.prep_date_entry = tk.Entry(root, textvariable=self.prep_date_var)
        self.prep_date_entry.grid(row=3, column=1, padx=5, pady=2, sticky="w")

        self.prep_date_button = tk.Button(root, text="Set now", command=self.set_prep_date)
        self.prep_date_button.grid(row=3, column=2, padx=5, pady=2, sticky="w")

        # Assembly Date
        self.assembly_date_label = tk.Label(root, text="Assembly Date")
        self.assembly_date_label.grid(row=4, column=0, padx=5, pady=2, sticky="e")

        self.assembly_date_var = tk.StringVar()
        self.assembly_date_entry = tk.Entry(root, textvariable=self.assembly_date_var)
        self.assembly_date_entry.grid(row=4, column=1, padx=5, pady=2, sticky="w")

        self.assembly_date_button = tk.Button(root, text="Set now", command=self.set_assembly_date)
        self.assembly_date_button.grid(row=4, column=2, padx=5, pady=2, sticky="w")

        # Export button
        self.export_button = tk.Button(root, text="Export to CSV", command=self.export_to_csv)
        self.export_button.grid(row=5, column=1, pady=(10, 0), sticky="ew")

        # Clear Entries button
        self.clear_button = tk.Button(root, text="Clear Entries", command=self.clear_entries)
        self.clear_button.grid(row=5, column=0, pady=(10, 0), sticky="ew")

    def update_square(self, var, idx):
        row = idx // 8
        col = idx % 8
        text = var.get()
        if len(text) >= 15:
            formatted_text = f"{text[5:7]}\n{text[7:11]}\n{text[11]} {text[12:15]}"
            self.squares[row][col].config(text=formatted_text)
        else:
            self.squares[row][col].config(text=text)

        if text:
            self.squares[row][col]['bg'] = 'green'
        else:
            self.squares[row][col]['bg'] = 'red'

    def highlight_square(self, idx):
        row = idx // 8
        col = idx % 8
        self.squares[row][col]['bg'] = 'yellow'

    def reset_square(self, idx):
        row = idx // 8
        col = idx % 8
        if self.input_vars[idx].get():
            self.squares[row][col]['bg'] = 'green'
        else:
            self.squares[row][col]['bg'] = 'red'

    def set_prep_date(self):
        self.prep_date_var.set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def set_assembly_date(self):
        self.assembly_date_var.set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def export_to_csv(self):
        # Check if all input boxes are filled
        for var in self.input_vars:
            if not var.get():
                messagebox.showerror("Error", "Missing Tiles")
                return

        # Check if the preparation date is filled
        if not self.prep_date_var.get().strip():
            messagebox.showerror("Error", "Preparation date is missing.")
            return

        # Check for duplicate barcodes in other files
        duplicate_info = self.check_for_duplicate_barcodes()
        if duplicate_info:
            duplicate_barcode, filename = duplicate_info
            messagebox.showerror("Error", f"Duplicate barcode found: {duplicate_barcode} in file {filename}")
            return

        # Get the filename
        filename = self.filename_var.get().strip()
        if not filename:
            messagebox.showerror("Error", "Please enter a filename.")
            return

        # Tile Board Barcode
        tile_board_barcode = filename  # Assuming the barcode is the filename

        # Prepare data for CSV
        header = ["Tile_Board", "Tiles", "Preparation_Date", "Assembly_Date"]
        data = [header]

        # Add row with tile board, preparation date, and assembly date
        board_data = [
            tile_board_barcode,
            '',
            self.prep_date_var.get(),
            self.assembly_date_var.get()
        ]
        data.append(board_data)

        # Add rows with tile data
        for var in self.input_vars:
            tile = var.get()
            row = [
                '',
                tile,
                '',
                ''
            ]
            data.append(row)

        # Write data to CSV file
        csv_filename = filename + ".csv"
        with open(csv_filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)

        messagebox.showinfo("Export Successful", f"Data has been exported to {csv_filename}")

    def clear_entries(self):
        for var in self.input_vars:
            var.set("")
        self.filename_var.set("")
        self.prep_date_var.set("")
        self.assembly_date_var.set("")

    def check_existing_file(self, *args):
        filename = self.filename_var.get().strip()
        if not filename:
            return

        # Check if a file with the same name exists
        if os.path.exists(filename + ".csv"):
            # Read data from the existing CSV file and populate the input boxes
            with open(filename + ".csv", 'r', newline='') as file:
                reader = csv.reader(file)
                data = list(reader)
            if len(data) > 1:
                # Tile Board Barcode
                tile_board_barcode = data[1][0]
                self.filename_var.set(tile_board_barcode)
                
                # Tiles
                for i, row in enumerate(data[2:]):
                    if len(row) > 1:
                        self.input_vars[i].set(row[1])
                
                # Preparation Date
                prep_date = data[1][2]
                self.prep_date_var.set(prep_date)
                
                # Assembly Date
                assembly_date = data[1][3]
                self.assembly_date_var.set(assembly_date)

    def check_for_duplicate_barcodes(self):
        current_board = self.filename_var.get().strip() + ".csv"
        barcodes = set(var.get().strip() for var in self.input_vars)

        for file in os.listdir("."):
            if file.endswith(".csv") and file != current_board:
                with open(file, 'r', newline='') as f:
                    reader = csv.reader(f)
                    data = list(reader)
                    for row in data[2:]:
                        if len(row) > 1:
                            barcode = row[1].strip()
                            if barcode in barcodes:
                                return barcode, file
        return None

if __name__ == "__main__":
    root = tk.Tk()
    app = ModuleAssemblyGUI(root)
    root.mainloop()
