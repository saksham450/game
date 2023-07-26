import tkinter as tk


def draw_line(event):
    global x2, y2
    # Get the current position of the mouse
    x1, y1 = event.x, event.y
    # Create a line from the current position to the previous position
    canvas.create_line(x1, y1, x2, y2)
    # Update the previous position
    x2, y2 = x1, y1


def draw_rectangle():
    global x2, y2
    # Get the current position of the mouse
    x1, y1 = canvas.winfo_pointerx() - root.winfo_rootx(), canvas.winfo_pointery() - root.winfo_rooty()
    # Create a rectangle from the current position to the previous position
    canvas.create_rectangle(x1, y1, x2, y2)


def draw_oval():
    global x2, y2
    # Get the current position of the mouse
    x1, y1 = canvas.winfo_pointerx() - root.winfo_rootx(), canvas.winfo_pointery() - root.winfo_rooty()
    # Create an oval from the current position to the previous position
    canvas.create_oval(x1, y1, x2, y2)


# Create the main window
root = tk.Tk()


# Create the toolbar
toolbar = tk.Frame(root, bg="blue")

# Add buttons to the toolbar
btn_line = tk.Button(toolbar, text="Line", command=lambda: draw_line)
btn_rect = tk.Button(toolbar, text="Rectangle", command=draw_rectangle)
btn_oval = tk.Button(toolbar, text="Oval", command=draw_oval)

# Pack the buttons into the toolbar
btn_line.pack(side="left")
btn_rect.pack(side="left")
btn_oval.pack(side="left")

# Pack the toolbar into the main window
toolbar.pack(side="top", fill="x")

# Create the canvas
canvas = tk.Canvas(root, width=500, height=500)
canvas.pack()

# Bind the mouse events to the canvas
canvas.bind("<B1-Motion>", draw_line)

# Initialize the previous position variables
x2, y2 = 0, 0

# Start the main loop
root.mainloop()
