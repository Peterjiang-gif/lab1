import tkinter as tk
def get_selected_items():
 # Get selected items from the first listbox
    selected_indices_1 = listbox1.curselection()
    selected_items_1 = [listbox1.get(i) for i in selected_indices_1]

    # Get selected items from the second listbox
    selected_indices_2 = listbox2.curselection()
    selected_items_2 = [listbox2.get(i) for i in selected_indices_2]

    # Print or process the selected items
    print("Selected from Listbox 1:", selected_items_1)
    print("Selected from Listbox 2:", selected_items_2)
    
    # Update a label to show the results in the GUI
    result_label.config(text=f"L1: {selected_items_1}\\nL2: {selected_items_2}")

# Create the main window
root = tk.Tk()
root.title("Listbox Input Example")
root.geometry("450x300")

# --- Listbox 1 ---
label1 = tk.Label(root, text="Select from List 1:")
label1.pack(pady=(10, 0))
listbox1 = tk.Listbox(root, selectmode=tk.MULTIPLE, exportselection=False) # exportselection=False allows selections in both listboxes simultaneously
for item in ["Apple", "Banana", "Cherry", "Date", "Elderberry"]:
    listbox1.insert(tk.END, item)
listbox1.pack(padx=10, pady=5, fill=tk.BOTH, expand=True, side=tk.LEFT)

# --- Listbox 2 ---
label2 = tk.Label(root, text="Select from List 2:")
label2.pack(pady=(10, 0))
listbox2 = tk.Listbox(root, selectmode=tk.MULTIPLE, exportselection=False)
for item in ["Red", "Green", "Blue", "Yellow", "Purple"]:
    listbox2.insert(tk.END, item)
listbox2.pack(padx=10, pady=5, fill=tk.BOTH, expand=True, side=tk.RIGHT)

# --- Button ---
# The 'command' attribute links the button click to the get_selected_items function
button = tk.Button(root, text="Get Selections", command=get_selected_items)
button.pack(pady=10)

# --- Result Label (optional, for GUI output) ---
result_label = tk.Label(root, text="Selections will appear here")
result_label.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()