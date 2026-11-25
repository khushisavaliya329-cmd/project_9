
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os


class SalesDataAnalyzer:

    def __init__(self):
        self.data = None
        self.plots = []

    def __del__(self):
        plt.close("all")

    def load_data(self, path):
        try:
            self.data = pd.read_csv(path)
            print(self.data.head())
            print("Data loaded successfully.")
            return True
        except Exception as e:
            print("Error:", e)
            return False

    def ensure_data(self):
        if self.data is None:
            print("Data not loaded.")
            path = input("Enter CSV file path: ")
            return self.load_data(path)
        return True

    def explore_data(self):
        if not self.ensure_data():
            return

        print(self.data.head())
        print(self.data.tail())
        print(self.data.columns)
        print(self.data.dtypes)
        self.data.info()
        print(self.data.describe())

    def clean_data(self):
        if not self.ensure_data():
            return

        print(self.data[self.data.isnull().any(axis=1)])
        print("1. Fill with mean  2. Drop rows  3. Replace")
        choice = input("Enter choice: ")

        if choice == "1":
            for col in self.data.select_dtypes(include=np.number):
                self.data[col] = self.data[col].fillna(
                    self.data[col].mean()
                )

        elif choice == "2":
            self.data = self.data.dropna()

        elif choice == "3":
            value = input("Enter replacement value: ")
            self.data = self.data.fillna(value)

        else:
            print("Invalid choice.")

    def mathematical_operations(self):
        if not self.ensure_data():
            return

        col = input("Enter numeric column: ")

        if col not in self.data.select_dtypes(include=np.number).columns:
            print("Invalid column.")
            return

        n = float(input("Enter number: "))

        print("1.Add 2.Subtract 3.Multiply 4.Divide")
        ch = input("Choice: ")

        if ch == "1":
            print(self.data[col] + n)

        elif ch == "2":
            print(self.data[col] - n)

        elif ch == "3":
            print(self.data[col] * n)

        elif ch == "4" and n != 0:
            print(self.data[col] / n)

        else:
            print("Invalid operation.")

    def combine_data(self):
        if not self.ensure_data():
            return

        try:
            path = input("Enter second CSV path: ")
            other = pd.read_csv(path)

            combined = pd.concat(
                [self.data, other],
                ignore_index=True
            )

            print(combined)

        except Exception as e:
            print("Error:", e)

    def split_data(self):
        if not self.ensure_data():
            return

        col = input("Enter column: ")

        if col not in self.data.columns:
            print("Column not found.")
            return

        os.makedirs("Split_Data", exist_ok=True)

        for value, part in self.data.groupby(col):
            part.to_csv(
                "Split_Data/" + str(value) + ".csv",
                index=False
            )

        print("Data split successfully.")

    def search_sort_filter(self):
        if not self.ensure_data():
            return

        print("1.Search 2.Sort 3.Filter")
        ch = input("Choice: ")

        col = input("Enter column: ")

        if col not in self.data.columns:
            print("Column not found.")
            return

        if ch == "1":
            value = input("Search value: ")

            print(
                self.data[
                    self.data[col].astype(str).str.contains(
                        value, case=False, na=False
                    )
                ]
            )

        elif ch == "2":
            print(self.data.sort_values(col))

        elif ch == "3" and pd.api.types.is_numeric_dtype(
            self.data[col]
        ):
            n = float(input("Minimum value: "))
            print(self.data[self.data[col] >= n])

        else:
            print("Invalid choice.")

    def aggregate_functions(self):
        if not self.ensure_data():
            return

        numeric = self.data.select_dtypes(include=np.number)

        print(
            numeric.agg(["sum", "mean", "max", "min"])
        )

        if "Region" in self.data.columns and "Sales" in self.data.columns:
            print(
                self.data.groupby("Region")["Sales"].sum()
            )

            self.data["Average"] = (
                self.data.groupby("Region")["Sales"].transform("mean")
            )

    def statistical_analysis(self):
        if not self.ensure_data():
            return

        numeric = self.data.select_dtypes(include=np.number)

        print(numeric.describe())
        print(numeric.corr())

    def create_pivot_table(self):
        if not self.ensure_data():
            return

        if all(
            col in self.data.columns
            for col in ["Sales", "Region", "Product"]
        ):
            table = pd.pivot_table(
                self.data,
                values="Sales",
                index="Region",
                columns="Product",
                aggfunc="sum",
                fill_value=0
            )

            print("\nPivot Table:")
            print(table)

        else:
            print("Sales, Region or Product column is missing.")

    def numpy_operations(self):
        if not self.ensure_data():
            return

        col = input("Enter numeric column: ")

        if col not in self.data.select_dtypes(include=np.number).columns:
            print("Invalid column.")
            return

        arr = self.data[col].to_numpy()

        print(arr)
        print(arr[0])
        print(arr[:3])
        print(np.array_split(arr, 2))
        print(np.concatenate((arr, arr)))

    def visualize_data(self):
        if not self.ensure_data():
            return

        self.plots = []

        data = self.data
        numeric = data.select_dtypes(include=np.number)

        if numeric.empty:
            print("No numeric data available.")
            return

        # Bar Chart
        if "Product" in data.columns and "Sales" in data.columns:
            fig, ax = plt.subplots(figsize=(8, 5))

            sns.barplot(
                data=data,
                x="Product",
                y="Sales",
                estimator="sum",
                ax=ax
            )

            ax.set_title("Sales by Product")
            plt.tight_layout()
            self.plots.append(fig)

        # Pie Chart
        if "Region" in data.columns and "Sales" in data.columns:
            fig, ax = plt.subplots(figsize=(7, 7))

            data.groupby("Region")["Sales"].sum().plot.pie(
                autopct="%1.1f%%",
                ax=ax
            )

            ax.set_title("Sales by Region")
            ax.set_ylabel("")
            plt.tight_layout()
            self.plots.append(fig)

        # Line Chart
        if "Date" in data.columns and "Sales" in data.columns:
            fig, ax = plt.subplots(figsize=(9, 5))

            dates = pd.to_datetime(data["Date"], errors="coerce")
            temp = data.assign(Date=dates).dropna(subset=["Date"])
            temp = temp.sort_values("Date")

            sns.lineplot(
                data=temp,
                x="Date",
                y="Sales",
                marker="o",
                ax=ax
            )

            ax.set_title("Sales Over Time")
            plt.xticks(rotation=45)
            plt.tight_layout()
            self.plots.append(fig)

        # Scatter Chart
        if "Sales" in data.columns and "Profit" in data.columns:
            fig, ax = plt.subplots(figsize=(8, 5))

            sns.scatterplot(
                data=data,
                x="Sales",
                y="Profit",
                hue="Region" if "Region" in data.columns else None,
                s=100,
                ax=ax
            )

            ax.set_title("Sales vs Profit")
            plt.tight_layout()
            self.plots.append(fig)

        # Histogram
        if "Sales" in data.columns:
            fig, ax = plt.subplots(figsize=(8, 5))

            sns.histplot(
                data=data,
                x="Sales",
                bins=10,
                kde=True,
                ax=ax
            )

            ax.set_title("Sales Distribution")
            plt.tight_layout()
            self.plots.append(fig)

        # Heatmap
        if len(numeric.columns) >= 2:
            fig, ax = plt.subplots(figsize=(8, 6))

            sns.heatmap(
                numeric.corr(),
                annot=True,
                cmap="coolwarm",
                fmt=".2f",
                ax=ax
            )

            ax.set_title("Correlation Heatmap")
            plt.tight_layout()
            self.plots.append(fig)

        if not self.plots:
            print("No suitable charts found.")
            return

        print("Generating different types of charts...")

        for fig in self.plots:
            plt.show()

        print("All charts generated successfully.")
        print("Total charts:", len(self.plots))

    def save_visualization(self):
        if not self.plots:
            print("Create charts first using option 6.")
            return

        os.makedirs("Visualizations", exist_ok=True)

        for i, fig in enumerate(self.plots, start=1):
            fig.savefig(
                "Visualizations/Chart_" + str(i) + ".png"
            )

        print("All charts saved in Visualizations folder.")

    def save_results(self):
        if not self.ensure_data():
            return

        name = input("Enter CSV file name: ")

        if not name.endswith(".csv"):
            name += ".csv"

        self.data.to_csv(name, index=False)

        print("Data saved successfully.")


a = SalesDataAnalyzer()

while True:

    print("\n========== SALES DATA ANALYZER ==========")

    print("1. Load Data")
    print("2. Explore Data")
    print("3. DataFrame Operations")
    print("4. Clean Data")
    print("5. Statistics")
    print("6. Visualization")
    print("7. Save Charts")
    print("8. Save Results")
    print("9. Pivot Table")
    print("10. NumPy Operations")
    print("11. Exit")

    ch = input("\nEnter choice: ")

    if ch == "1":
        path = input("Enter CSV path: ")
        a.load_data(path)

    elif ch == "2":
        a.explore_data()

    elif ch == "3":
        print("\n1. Mathematical Operations")
        print("2. Combine Data")
        print("3. Split Data")
        print("4. Search / Sort / Filter")

        op = input("Enter choice: ")

        if op == "1":
            a.mathematical_operations()

        elif op == "2":
            a.combine_data()

        elif op == "3":
            a.split_data()

        elif op == "4":
            a.search_sort_filter()

        else:
            print("Invalid choice.")

    elif ch == "4":
        a.clean_data()

    elif ch == "5":
        a.aggregate_functions()
        a.statistical_analysis()

    elif ch == "6":
        a.visualize_data()

    elif ch == "7":
        a.save_visualization()

    elif ch == "8":
        a.save_results()

    elif ch == "9":
        a.create_pivot_table()

    elif ch == "10":
        a.numpy_operations()

    elif ch == "11":
        print("Thank you for using Sales Data Analyzer!")
        break

    else:
        print("Invalid choice.")
