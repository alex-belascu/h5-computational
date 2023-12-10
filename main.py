import tkinter as tk
from tkinter import ttk
from math import atan2
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

def orientation(p, q, r):
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0:
        return 0
    return 1 if val > 0 else 2

def graham_scan(points):
    n = len(points)
    if n < 3:
        return points

    pivot = min(points, key=lambda p: (p[1], p[0]))
    sorted_points = sorted(points, key=lambda p: (atan2(p[1] - pivot[1], p[0] - pivot[0]), p))
    hull = [pivot, sorted_points[0], sorted_points[1]]

    for i in range(2, n):
        while len(hull) > 1 and orientation(hull[-2], hull[-1], sorted_points[i]) != 2:
            hull.pop()
        hull.append(sorted_points[i])

    return hull

def plot_convex_hull(points, convex_hull):
    fig, ax = plt.subplots(figsize=(6, 6))
    x, y = zip(*points)
    hull_x, hull_y = zip(*convex_hull)

    ax.scatter(x, y, marker='o', label='Points')
    ax.plot(hull_x + (hull_x[0],), hull_y + (hull_y[0],), marker='o', color='r', label='Convex Hull')
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_title('Convex Hull and Points')
    ax.legend()

    return fig

def points_on_convex_hull_border(points, convex_hull):
    border_points = set(convex_hull)
    for point in points:
        if point not in border_points:
            for i in range(len(convex_hull) - 1):
                if orientation(convex_hull[i], point, convex_hull[i + 1]) == 0:
                    border_points.add(point)
                    break
    return len(border_points)

class ConvexHullApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Convex Hull Visualization")

        self.lambda_label = ttk.Label(self.root, text="Enter Lambda:")
        self.lambda_entry = ttk.Entry(self.root)
        self.lambda_entry.insert(0, "1.5")

        self.plot_button = ttk.Button(self.root, text="Plot Convex Hull", command=self.plot_convex_hull)

        self.lambda_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.E)
        self.lambda_entry.grid(row=0, column=1, padx=10, pady=10)
        self.plot_button.grid(row=1, column=0, columnspan=2, pady=10)

    def plot_convex_hull(self):
        lambda_value = float(self.lambda_entry.get())
        points = [(3, -3), (3, 3), (-3, -3), (-3, 3), (-2 + lambda_value, 3 - lambda_value)]
        convex_hull = graham_scan(points)
        fig = plot_convex_hull(points, convex_hull)

        # Embed Matplotlib figure in Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=2, column=0, columnspan=2)

        # Count points on the border of the convex hull
        num_points_on_border = points_on_convex_hull_border(points, convex_hull)
        result_label = ttk.Label(self.root, text=f"Number of points on the border: {num_points_on_border}")
        result_label.grid(row=3, column=0, columnspan=2, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = ConvexHullApp(root)
    root.mainloop()
