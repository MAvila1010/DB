import tkinter as tk
from tkinter import messagebox
import csv
from datetime import datetime
import os

class ModuleAssemblyGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Module Assembly")
        self.root.geometry("1000x800")  # Initial size of the window

        # Configure root window to expand
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)

        # Initialize grid type
        self.current_grid = '8x8'

        # Navigation buttons
        self.nav_frame = tk.Frame(root)
        self.nav_frame.grid(row=2, column=0, columnspan=2, pady=5, sticky="ew")
        self.nav_frame.grid_columnconfigure(0, weight=1)
        self.nav_frame.grid_columnconfigure(1, weight=1)

        self.prev_button = tk.Button(self.nav_frame, text="<", command=self.show_prev_grid)
        self.prev_button.grid(row=0, column=0, padx=5, sticky="w")

        self.next_button = tk.Button(self.nav_frame, text=">", command=self.show_next_grid)
        self.next_button.grid(row=0, column=1, padx=5, sticky="e")

        # Initialize frames and variables for grids
        self.frames = {}
        self.init_grid('8x8', 8, 8)
        self.init_grid('A5F', 5, 8, [
            [1, 1, 1, 1, '1*', '1*', '1*', 1],
            [1, 1, 1, 1, '1*', '1*', '1*', 1],
            ['1*', 1, 1, 1, 1, 1, 1, '1*'],
            [1, 1, 1, 1, 1, 1, 1, 1],
            ['1*', 1, 1, 1, 1, 1, 1, '1*']
        ])
        self.init_grid('C5F', 5, 8, [
            [1, 1, '1*', '1*', 1, 1, 1, 1],
            [1, 1, '1*', '1*', '1*', 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            ['1*', 1, 1, 1, 1, 1, 1, '1*']
        ])
        self.init_grid('A6F', 6, 8, [
            [1, 1, 1, 1, '1*', '1*', '1*', 1],
            [1, 1, 1, 1, '1*', '1*', '1*', 1],
            ['1*', 1, 1, 1, 1, 1, 1, '1*'],
            [1, 1, 1, 1, 1, 1, 1, 1],
            ['1*', 1, 1, 1, 1, 1, 1, '1*'],
            [1, 1, 1, 1, 1, 1, 1, 1]
        ])
        self.init_grid('D8F', 8, 8, [
            [1, 1, 1, 1, 1, 1, '1*', '1*'],
            [1, 1, 1, 1, 1, 1, '1*', '1*'],
            [1, '1*', 1, 1, '1*', 1, '1*', 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, '1*', 1, 1, 1, 1, '1*', 1]
        ])
        self.init_grid('B11', 11, 8, [
            [1, 1, '1*', '1*', 1, 1, 1, 1],
            [1, 1, '1*', '1*', 1, 1, '1*', 1],
            [1, '1*', 1, 1, '1*', 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, '1*', 1, 1, 1, 1, 1, '1*']
        ])
        self.init_grid('B12', 12, 8, [
            [1, 1, '1*', '1*', 1, 1, 1, 1],
            [1, 1, '1*', '1*', 1, 1, '1*', 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, '1*', 1, 1, 1, 1, 1, '1*'],
            [1, 1, 1, 1, 1, 1, 1, 1]
        ])
        self.init_grid('E8F', 8, 8, [
            ['1*', '1*', '1*', '1*', '1*', '1*', '1*', 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, '1*', 1, 1, '1*', 1, 1, '1*'],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, '1*', 1, 1, '1*', 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1]
        ])
        self.init_grid('G3F', 3, 8, [
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, '1*', 1, 1, '1*', 1, '1*', 1],
            ['1*', '1*', '1*', '1*', '1*', '1*', '1*', 1]
        ])
        self.init_grid('G3L', 3, 7, [
            [1, 1, 1, 1, 1, 1, 1],
            ['1*', 1, 1, '1*', 1, '1*', 1],
            ['1*', '1*', '1*', '1*', '1*', '1*', 1]
        ])
        self.init_grid('G3R', 3, 7, [
            [1, 1, 1, 1, 1, 1, 1],
            [1, '1*', 1, 1, '1*', 1, '1*'],
            ['1*', '1*', '1*', '1*', '1*', '1*', '1*', '1*']
        ])
        self.init_grid('G5F', 5, 8, [
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, '1*', 1, 1, 1, 1, '1*', 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, '1*', 1, 1, '1*', 1, 1, '1*'],
            ['1*', '1*', '1*', '1*', '1*', '1*', '1*', 1]
        ])
        self.init_grid('G5L', 5, 8, [
            [0, 1, 1, 1, 1, 1, 1, 1],
            [0, '1*', 1, 1, 1, 1, '1*', 1],
            [0, 1, 1, 1, 1, 1, 1, 1],
            [1, '1*', 1, 1, '1*', 1, 1, '1*'],
            ['1*', '1*', '1*', '1*', '1*', '1*', '1*', 1]
        ])
        self.init_grid('G5R', 5, 8, [
            [1, 1, 1, 1, 1, 1, 1, 0],
            [1, '1*', 1, 1, 1, 1, '1*', 0],
            [1, 1, 1, 1, 1, 1, 1, 0],
            [1, '1*', 1, 1, '1*', 1, 1, '1*'],
            ['1*', '1*', '1*', '1*', '1*', '1*', '1*', 1]
        ])
        self.init_grid('G7F', 7, 8, [
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, '1*', 1, 1, 1, 1, '1*', 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, '1*', 1, 1, '1*', 1, 1, '1*'],
            ['1*', '1*', '1*', '1*', '1*', '1*', '1*', 1]
        ])
        self.init_grid('G7L', 7, 8, [
            [0, 1, 1, 1, 1, 1, 1, 1],
            [0, '1*', 1, 1, 1, 1, '1*', 1],
            [0, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, '1*', 1, 1, '1*', 1, 1, '1*'],
            ['1*', '1*', '1*', '1*', '1*', '1*', '1*', 1]
        ])
        self.init_grid('G7R', 7, 8, [
            [1, 1, 1, 1, 1, 1, 1, 0],
            [1, '1*', 1, 1, 1, 1, '1*', 0],
            [1, 1, 1, 1, 1, 1, 1, 0],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, '1*', 1, 1, '1*', 1, 1, '1*'],
            ['1*', '1*', '1*', '1*', '1*', '1*', '1*', 1]
        ])
        self.init_grid('G8F', 8, 8, [
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, '1*', 1, 1, 1, 1, '1*', 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, '1*', 1, 1, '1*', 1, 1, '1*'],
            ['1*', '1*', '1*', '1*', '1*', '1*', '1*', 1]
        ])
        self.init_grid('G8L', 8, 8, [
            [0, 1, 1, 1, 1, 1, 1, 1],
            [0, 1, 1, 1, 1, 1, 1, 1],
            [1, '1*', 1, 1, 1, 1, '1*', 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, '1*', 1, 1, '1*', 1, 1, '1*'],
            ['1*', '1*', '1*', '1*', '1*', '1*', '1*', 1]
        ])
        self.init_grid('G8R', 8, 8, [
            [1, 1, 1, 1, 1, 1, 1, 0],
            [1, 1, 1, 1, 1, 1, 1, 0],
            [1, '1*', 1, 1, 1, 1, '1*', 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, '1*', 1, 1, '1*', 1, 1, '1*'],
            ['1*', '1*', '1*', '1*', '1*', '1*', '1*', 1]
        ])

        # Preparation Date
        self.prep_date_label = tk.Label(root, text="Preparation Date:")
        self.prep_date_label.grid(row=3, column=1, padx=5, pady=2, sticky="w")

        self.prep_date_var = tk.StringVar()
        self.prep_date_entry = tk.Entry(root, textvariable=self.prep_date_var)
        self.prep_date_entry.grid(row=3, column=1, padx=5, pady=2, sticky="s")

        self.prep_date_button = tk.Button(root, text="Set now", command=self.set_prep_date)
        self.prep_date_button.grid(row=3, column=1, padx=5, pady=2, sticky="e")

        # Assembly Date
        self.assembly_date_label = tk.Label(root, text="Assembly Date:")
        self.assembly_date_label.grid(row=4, column=1, padx=5, pady=2, sticky="w")

        self.assembly_date_var = tk.StringVar()
        self.assembly_date_entry = tk.Entry(root, textvariable=self.assembly_date_var)
        self.assembly_date_entry.grid(row=4, column=1, padx=5, pady=2, sticky="s")

        self.assembly_date_button = tk.Button(root, text="Set now", command=self.set_assembly_date)
        self.assembly_date_button.grid(row=4, column=1, padx=5, pady=2, sticky="e")

        # Export button
        self.export_button = tk.Button(root, text="Export to CSV", command=self.export_to_csv)
        self.export_button.grid(row=3, column=0, pady=5, sticky="ew")

        # Clear Entries button
        self.clear_button = tk.Button(root, text="Clear Entries", command=self.confirm_clear_entries)
        self.clear_button.grid(row=4, column=0, pady=5, sticky="ew")

        self.show_grid('8x8')

    def init_grid(self, grid_type, rows, cols, layout=None):
        squares_frame = tk.Frame(self.root)
        squares_frame.rowconfigure(tuple(range(rows)), weight=1)
        squares_frame.columnconfigure(tuple(range(cols)), weight=1)

        squares = []
        for i in range(rows):
            row = []
            for j in range(cols):
                square = tk.Label(squares_frame, bg='red', width=4, height=2, relief="ridge", justify="center")
                if layout and i < len(layout) and j < len(layout[i]):
                    value = layout[i][j]
                    if value == 0:
                        square.grid_forget()
                    elif value == 1:
                        square.grid(row=i, column=j, padx=5, pady=5, sticky="nsew")
                    elif value == '1*':
                        square.config(bg='blue')
                        square.grid(row=i, column=j, padx=5, pady=5, sticky="nsew")
                else:
                    square.grid(row=i, column=j, padx=5, pady=5, sticky="nsew")
                row.append(square)
            squares.append(row)

        inputs_frame = tk.Frame(self.root)
        inputs_frame.rowconfigure(tuple(range(max(35, rows * cols // 2))), weight=1)  # Adjust row configuration
        inputs_frame.columnconfigure(0, weight=1)
        inputs_frame.columnconfigure(1, weight=1)

        filename_var = tk.StringVar()
        filename_var.trace_add('write', self.check_existing_file)
        filename_entry = tk.Entry(inputs_frame, textvariable=filename_var)
        filename_entry.grid(row=1, column=0, columnspan=2, padx=5, pady=2, sticky="ew")

        tiles_label = tk.Label(inputs_frame, text=f"Tiles ({grid_type})")
        tiles_label.grid(row=2, column=0, columnspan=2, padx=5, pady=2)

        input_vars = []
        inputs = []
        total_inputs = rows * cols
        inputs_per_col = total_inputs // 2 + (total_inputs % 2)
        for i in range(total_inputs):
            var = tk.StringVar()
            var.trace_add('write', lambda name, index, mode, var=var, idx=i, g=grid_type: self.update_square(var, idx, g))
            entry = tk.Entry(inputs_frame, textvariable=var)
            entry.grid(row=i % inputs_per_col + 3, column=i // inputs_per_col, padx=5, pady=2, sticky="nsew")
            input_vars.append(var)
            inputs.append(entry)

            # Bind events to change square color on hover
            entry.bind("<Enter>", lambda event, idx=i, g=grid_type: self.hover_square(idx, g))
            entry.bind("<Leave>", lambda event, idx=i, g=grid_type: self.reset_square(idx, g))
            entry.bind("<FocusIn>", lambda event, idx=i, g=grid_type: self.highlight_square(idx, g))

        self.frames[grid_type] = {
            'squares_frame': squares_frame,
            'inputs_frame': inputs_frame,
            'squares': squares,
            'filename_var': filename_var,
            'input_vars': input_vars,
        }

    def update_square(self, var, idx, grid_type):
        frame = self.frames[grid_type]
        rows = len(frame['squares'])
        cols = len(frame['squares'][0])
        row = idx // cols
        col = idx % cols
        square = frame['squares'][row][col]
        
        text = var.get()
        if len(text) >= 15:
            formatted_text = f"{text[5:7]}\n{text[7:11]}\n{text[11]} {text[12:15]}"
            square.config(text=formatted_text)
        else:
            square.config(text=text)

        square['bg'] = 'green' if text else 'red'


    def hover_square(self, idx, grid_type):
        frame = self.frames[grid_type]
        rows = len(frame['squares'])
        cols = len(frame['squares'][0])
        row = idx // cols
        col = idx % cols
        square = frame['squares'][row][col]

        # Remember the original background color
        if square['bg'] == 'blue':
            square.original_bg = 'blue'

        # Change the background color to yellow on hover
        if square['bg'] != 'green':  # Only change color if not filled (green)
            square['bg'] = 'yellow'

    def reset_square(self, idx, grid_type):
        frame = self.frames[grid_type]
        rows = len(frame['squares'])
        cols = len(frame['squares'][0])
        row = idx // cols
        col = idx % cols
        square = frame['squares'][row][col]
        var = frame['input_vars'][idx]

        # Reset to original background color
        if hasattr(square, 'original_bg'):
            if square.original_bg == 'blue': # Set it back to blue if originally blue
                square['bg'] = 'blue'
            else:
                square['bg'] = 'red' # Normal tile remains red when empty
        elif var.get():
            square['bg'] = 'green' # Filled input turns green
        else:
            square['bg'] = 'red' # Normal tile remains red when empty

    def highlight_square(self, idx, grid_type):
        self.hover_square(idx, grid_type)

    def set_prep_date(self):
        self.prep_date_var.set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def set_assembly_date(self):
        self.assembly_date_var.set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def show_grid(self, grid_type):
        for frame in self.frames.values():
            frame['squares_frame'].grid_forget()
            frame['inputs_frame'].grid_forget()

        self.frames[grid_type]['squares_frame'].grid(row=0, column=0, rowspan=2, padx=5, pady=5, sticky="nsew")
        self.frames[grid_type]['inputs_frame'].grid(row=0, column=1, rowspan=2, padx=5, pady=5, sticky="nsew")

    def show_prev_grid(self):
        grids = list(self.frames.keys())
        current_index = grids.index(self.current_grid)
        prev_index = (current_index - 1) % len(grids)
        self.show_grid(grids[prev_index])
        self.current_grid = grids[prev_index]

    def show_next_grid(self):
        grids = list(self.frames.keys())
        current_index = grids.index(self.current_grid)
        next_index = (current_index + 1) % len(grids)
        self.show_grid(grids[next_index])
        self.current_grid = grids[next_index]

    def check_existing_file(self, *args):
        filename = self.frames[self.current_grid]['filename_var'].get()
        if os.path.exists(filename):
            messagebox.showwarning("File Exists", "A file with this name already exists!")

    def set_prep_date(self):
        self.prep_date_var.set(datetime.now().strftime("%Y-%m-%d"))

    def set_assembly_date(self):
        self.assembly_date_var.set(datetime.now().strftime("%Y-%m-%d"))
            
    def export_to_csv(self):
        data = {
            'Preparation Date': self.prep_date_var.get(),
            'Assembly Date': self.assembly_date_var.get(),
            'Grid Type': self.current_grid
        }

        filename = f"module_assembly_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
        file_path = os.path.join(os.getcwd(), filename)
        
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=data.keys())
            writer.writeheader()
            writer.writerow(data)
        
        messagebox.showinfo("Export", f"Data exported to {filename}")


    def confirm_clear_entries(self):
        if messagebox.askyesno("Clear Entries", "Are you sure you want to clear all entries?"):
            for var in self.frames[self.current_grid]['input_vars']:
                var.set("")

if __name__ == "__main__":
    root = tk.Tk()
    app = ModuleAssemblyGUI(root)
    root.mainloop()
