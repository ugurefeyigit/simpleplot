import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from scipy.stats import linregress

class Questionnaire(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Data Input")

        ttk.Label(self, text="How many data points do you have?").grid(row=0, column=0, sticky="w")
        self.data_amount_entry = ttk.Entry(self)
        self.data_amount_entry.grid(row=0, column=1)

        ttk.Label(self, text="What is the data on the X-axis?").grid(row=1, column=0, sticky="w")
        self.x_data_name_entry = ttk.Entry(self)
        self.x_data_name_entry.grid(row=1, column=1)

        ttk.Label(self, text="What is the unit of the data on the X-axis?").grid(row=2, column=0, sticky="w")
        self.x_data_unit_entry = ttk.Entry(self)
        self.x_data_unit_entry.grid(row=2, column=1)

        ttk.Label(self, text="What is the data on the Y-axis?").grid(row=3, column=0, sticky="w")
        self.y_data_name_entry = ttk.Entry(self)
        self.y_data_name_entry.grid(row=3, column=1)

        ttk.Label(self, text="What is the unit of the data on the Y-axis?").grid(row=4, column=0, sticky="w")
        self.y_data_unit_entry = ttk.Entry(self)
        self.y_data_unit_entry.grid(row=4, column=1)

        ttk.Label(self, text="What is the plot name?").grid(row=5, column=0, sticky="w")
        self.plot_name_entry = ttk.Entry(self)
        self.plot_name_entry.grid(row=5, column=1)

        self.best_fit_line_var = tk.IntVar()
        ttk.Checkbutton(self, text="Create best fit line?", variable=self.best_fit_line_var).grid(row=6, column=0, columnspan=2)

        # Add submit button for questionnaire
        self.submit_button = ttk.Button(self, text="Submit", command=self.submit)
        self.submit_button.grid(row=7, column=0, columnspan=2)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        self.destroy()
        self.master.quit()

    def submit(self):
        try:
            # Hide the questionnaire section and its submit button
            for widget in self.winfo_children():
                widget.grid_remove()
            self.submit_button.grid_remove()

            # Add data entry fields for x and y axis
            self.x_data_entries = []
            self.y_data_entries = []
            for i in range(int(self.data_amount_entry.get())):
                ttk.Label(self, text=f"X-axis data {i+1}:").grid(row=8+i, column=0, sticky="w")
                x_data_entry = ttk.Entry(self)
                x_data_entry.grid(row=8+i, column=1)
                self.x_data_entries.append(x_data_entry)

                ttk.Label(self, text=f"Y-axis data {i+1}:").grid(row=8+i, column=2, sticky="w")
                y_data_entry = ttk.Entry(self)
                y_data_entry.grid(row=8+i, column=3)
                self.y_data_entries.append(y_data_entry)

            # Add submit button for entered data
            self.data_submit_button = ttk.Button(self, text="Submit Data", command=self.submit_data)
            self.data_submit_button.grid(row=9+i, column=0, columnspan=2)
        except ValueError:
            print("Please enter a valid number for the amount of data points.")

    def submit_data(self):
        try:
            # Check that all entries are filled
            if all(entry.get() for entry in self.x_data_entries) and all(entry.get() for entry in self.y_data_entries):
                # Collect data from entries and plot
                x_data = [float(entry.get()) for entry in self.x_data_entries]
                y_data = [float(entry.get()) for entry in self.y_data_entries]
                plt.plot(x_data, y_data, 'o', label=self.y_data_name_entry.get() + ' points')  # 'o' marker added here
                plt.plot(x_data, y_data, label=self.y_data_name_entry.get() + ' line')  # line plot added here
                plt.xlabel(self.x_data_name_entry.get() + " (" + self.x_data_unit_entry.get() + ")")
                plt.ylabel(self.y_data_name_entry.get() + " (" + self.y_data_unit_entry.get() + ")")
                plt.title(self.plot_name_entry.get())

                if self.best_fit_line_var.get() == 1:
                    slope, intercept, r_value, p_value, std_err = linregress(x_data, y_data)
                    plt.plot(x_data, [slope*x + intercept for x in x_data], label='Best fit line')

                plt.legend()
                plt.show()

                # Clear the data entries for new data
                for entry in self.x_data_entries + self.y_data_entries:
                    entry.delete(0, 'end')
            else:
                messagebox.showerror("Error", "Please fill all entries before submitting.")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for the data points.")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    Questionnaire()
    tk.mainloop()
