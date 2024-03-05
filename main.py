import random
import tkinter as tk
from datetime import datetime
from tkinter import filedialog
from tkinter import ttk

import pandas as pd


class RandomDataGeneratorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Random Data Generator")

        self.columns = []
        self.column_mapping = {}

        # UI elements
        self.num_rows_label = ttk.Label(self.master, text="Number of Rows:")
        self.num_rows_entry = ttk.Entry(self.master)
        self.num_rows_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.num_rows_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        self.column_label = ttk.Label(self.master, text="Column Name:")
        self.column_entry = ttk.Entry(self.master)
        self.column_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.column_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        self.data_type_label = ttk.Label(self.master, text="Data Type:")
        self.data_type_var = tk.StringVar()
        self.data_type_combobox = ttk.Combobox(self.master, textvariable=self.data_type_var,
                                               values=["Source", "Range", "Inline"])
        self.data_type_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.data_type_combobox.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.data_type_combobox.bind("<<ComboboxSelected>>", self.update_options)

        self.options_frame = ttk.Frame(self.master)
        self.options_frame.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="w")

        self.output_file_label = ttk.Label(self.master, text="Output File:")
        self.output_file_entry = ttk.Entry(self.master)
        self.output_file_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.output_file_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")
        self.output_file_entry.insert(tk.END, f"dataset_{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx")

        self.add_column_button = ttk.Button(self.master, text="Add Column", command=self.add_column)
        self.generate_button = ttk.Button(self.master, text="Generate Excel", command=self.generate_excel)
        self.add_column_button.grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.generate_button.grid(row=5, column=1, padx=5, pady=5, sticky="e")

        self.column_details_label = ttk.Label(self.master, text="Column Details:")
        self.column_details_text = tk.Text(self.master, height=10, width=40)
        self.column_details_label.grid(row=6, column=0, padx=5, pady=5, sticky="w")
        self.column_details_text.grid(row=6, column=1, padx=5, pady=5, sticky="w")

    def update_options(self, event):
        data_type = self.data_type_var.get()
        for widget in self.options_frame.winfo_children():
            widget.destroy()

        if data_type == "Source":
            self.file_path_label = ttk.Label(self.options_frame, text="Data File Path:")
            self.file_path_entry = ttk.Entry(self.options_frame)
            self.file_path_button = ttk.Button(self.options_frame, text="Browse", command=self.browse_file)
            self.file_path_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
            self.file_path_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
            self.file_path_button.grid(row=0, column=2, padx=5, pady=5, sticky="w")
        elif data_type == "Range":
            self.range_label = ttk.Label(self.options_frame, text="Range (e.g., -10,10):")
            self.range_entry = ttk.Entry(self.options_frame)
            self.order_var = tk.StringVar(value="Random")
            self.order_random_radio = ttk.Radiobutton(self.options_frame, text="Random", variable=self.order_var,
                                                      value="Random")
            self.order_in_order_radio = ttk.Radiobutton(self.options_frame, text="In Order", variable=self.order_var,
                                                        value="In Order")
            self.range_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
            self.range_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
            self.order_random_radio.grid(row=1, column=0, padx=5, pady=5, sticky="w")
            self.order_in_order_radio.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        elif data_type == "Inline":
            self.inline_label = ttk.Label(self.options_frame, text="Inline Data (comma-separated):")
            self.inline_entry = ttk.Entry(self.options_frame)
            self.inline_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
            self.inline_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    def browse_file(self):
        file_path = filedialog.askopenfilename()
        self.file_path_entry.delete(0, tk.END)
        self.file_path_entry.insert(0, file_path)

    def add_column(self):
        column_name = self.column_entry.get()
        data_type = self.data_type_var.get()

        if not column_name:
            return

        if data_type == "Source":
            file_path = self.file_path_entry.get()
            self.column_mapping[column_name] = {"type": data_type, "file_path": file_path}
        elif data_type == "Range":
            range_str = self.range_entry.get()
            in_order = True if self.order_var.get() == "In Order" else False
            self.column_mapping[column_name] = {"type": data_type, "range": range_str, "in_order": in_order}
        elif data_type == "Inline":
            inline_data = self.inline_entry.get()
            self.column_mapping[column_name] = {"type": data_type, "inline_data": inline_data}

        self.columns.append(column_name)
        self.column_entry.delete(0, tk.END)
        self.update_column_details()

    def update_column_details(self):
        details_text = ""
        for column in self.columns:
            details_text += f"Column: {column}\n"
            details_text += f"Type: {self.column_mapping[column]['type']}\n"
            if self.column_mapping[column]['type'] == "Source":
                details_text += f"File Path: {self.column_mapping[column]['file_path']}\n"
            elif self.column_mapping[column]['type'] == "Range":
                details_text += f"Range: {self.column_mapping[column]['range']}\n"
                details_text += f"In Order: {self.column_mapping[column]['in_order']}\n"
            elif self.column_mapping[column]['type'] == "Inline":
                details_text += f"Inline Data: {self.column_mapping[column]['inline_data']}\n"
            details_text += "\n"

        self.column_details_text.delete(1.0, tk.END)
        self.column_details_text.insert(tk.END, details_text)

    def generate_excel(self):
        try:
            rows = int(self.num_rows_entry.get())
        except ValueError:
            print("Invalid number of rows.")
            return

        data = {}
        for column, mapping in self.column_mapping.items():
            data_type = mapping["type"]
            if data_type == "Source":
                with open(mapping["file_path"], 'r') as file:
                    data_list = [line.strip() for line in file.readlines()]
                data[column] = [random.choice(data_list) for _ in range(rows)]
            elif data_type == "Range":
                range_str = mapping["range"]
                in_order = mapping.get("in_order", False)
                values = list(map(int, range_str.split(',')))
                if not in_order:
                    random.shuffle(values)
                data[column] = values * (rows // len(values)) + values[:rows % len(values)]
            elif data_type == "Inline":
                inline_data = mapping["inline_data"]
                data[column] = [random.choice(inline_data.split(',')) for _ in range(rows)]

        output_file = self.output_file_entry.get()
        df = pd.DataFrame(data)
        df.to_excel(output_file, index=False)

        print(f"Random dataset with {rows} rows and {len(self.columns)} columns saved to {output_file}.")


if __name__ == "__main__":
    root = tk.Tk()
    app = RandomDataGeneratorApp(root)
    root.mainloop()
