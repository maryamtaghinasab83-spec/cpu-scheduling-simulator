import tkinter as tk
from tkinter import ttk, messagebox
from algorithms.fcfs import fcfs
from algorithms.round_robin import round_robin
from algorithms.sjf import sjf
from algorithms.srtf import srtf
from algorithms.priority_non_preemptive import priority_non_preemptive
from algorithms.priority_preemptive import priority_preemptive

def run_gui():
    root = tk.Tk()
    root.title("CPU Scheduling Simulator")

    root.geometry("900x700")
    root.minsize(900, 700)  # Minimum size to ensure proper layout
    root.resizable(False, False)

    process_entries = []
    output_widgets = []  # Track output widgets for clearing

    # --- Step 1: Number of processes ---
    tk.Label(root, text="Number of Processes:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10)
    num_processes_var = tk.StringVar()
    tk.Entry(root, textvariable=num_processes_var).grid(row=0, column=1, padx=10)

    # --- Step 2: Algorithm selection ---
    tk.Label(root, text="Select Algorithm:", font=("Arial", 12)).grid(row=1, column=0, padx=10)
    algo_var = tk.StringVar(value="FCFS")
    algo_menu = ttk.Combobox(root, textvariable=algo_var, values=[
        "FCFS",
        "Round Robin",
        "SJF",
        "SRTF",
        "Priority Non-preemptive",
        "Priority Preemptive"
    ], state="readonly")
    algo_menu.grid(row=1, column=1, padx=10)
    
    # Fix for hover blue background in combobox
    style = ttk.Style()
    style.map('TCombobox', fieldbackground=[('readonly', 'white')])
    style.map('TCombobox', selectbackground=[('readonly', 'white')])
    style.map('TCombobox', selectforeground=[('readonly', 'black')])

    # --- Step 3: Extra input (Time Quantum) ---
    extra_label = tk.Label(root, text="Time Quantum:", font=("Arial", 12))
    extra_var = tk.StringVar()
    extra_entry = tk.Entry(root, textvariable=extra_var)

    def update_extra_input(*args):
        # Remove previous widgets
        extra_label.grid_forget()
        extra_entry.grid_forget()
        if algo_var.get() == "Round Robin":
            extra_label.config(text="Time Quantum:")
            extra_label.grid(row=2, column=0, padx=10)
            extra_entry.grid(row=2, column=1, padx=10)

    algo_var.trace_add("write", update_extra_input)
    update_extra_input()

    # --- Generate process input form ---
    def generate_form():
        for w in output_widgets:
            w.destroy()
        output_widgets.clear()
        for widget in root.grid_slaves():
            if int(widget.grid_info()["row"]) >= 3:
                widget.destroy()
        process_entries.clear()

        try:
            n = int(num_processes_var.get())
            if n <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Enter a positive integer for number of processes")
            return

        # Table header
        tk.Label(root, text="PID").grid(row=3, column=0, padx=5)
        tk.Label(root, text="Arrival Time").grid(row=3, column=1, padx=5)
        tk.Label(root, text="Burst Time").grid(row=3, column=2, padx=5)
        if "Priority" in algo_var.get():
            tk.Label(root, text="Priority").grid(row=3, column=3, padx=5)

        # Process entries
        for i in range(n):
            pid_var = tk.StringVar(value=str(i+1))
            at_var = tk.StringVar()
            bt_var = tk.StringVar()
            pid_entry = tk.Entry(root, textvariable=pid_var, width=5)
            pid_entry.grid(row=i+4, column=0)
            at_entry = tk.Entry(root, textvariable=at_var, width=5)
            at_entry.grid(row=i+4, column=1)
            bt_entry = tk.Entry(root, textvariable=bt_var, width=5)
            bt_entry.grid(row=i+4, column=2)
            if "Priority" in algo_var.get():
                pr_var = tk.StringVar()
                pr_entry = tk.Entry(root, textvariable=pr_var, width=5)
                pr_entry.grid(row=i+4, column=3)
                process_entries.append((pid_var, at_var, bt_var, pr_var))
            else:
                process_entries.append((pid_var, at_var, bt_var))

        tk.Button(root, text="Run Algorithm", command=run_algorithm).grid(row=n+4, column=0, columnspan=5, pady=10)

    # --- Run selected algorithm ---
    def run_algorithm():
        for w in output_widgets:
            w.destroy()
        output_widgets.clear()

        processes = []
        priorities = {}
        for entry in process_entries:
            try:
                pid = int(entry[0].get())
                at = int(entry[1].get())
                bt = int(entry[2].get())
                if len(entry) == 4:
                    pr = int(entry[3].get())
                    priorities[pid] = pr
                processes.append((pid, at, bt))
            except ValueError:
                messagebox.showerror("Error", "All fields must be integers")
                return

        algo = algo_var.get()
        extra = extra_var.get()

        try:
            if algo == "FCFS":
                gantt, wt, tat, ct = fcfs(processes)
            elif algo == "Round Robin":
                tq = int(extra)
                if tq <= 0:
                    raise ValueError
                gantt, wt, tat, ct = round_robin(processes, tq)
            elif algo == "SJF":
                gantt, wt, tat, ct = sjf(processes)
            elif algo == "SRTF":
                gantt, wt, tat, ct = srtf(processes)
            elif algo == "Priority Non-preemptive":
                gantt, wt, tat, ct = priority_non_preemptive(processes, priorities)
            elif algo == "Priority Preemptive":
                gantt, wt, tat, ct = priority_preemptive(processes, priorities)
            else:
                messagebox.showerror("Error", "Unsupported algorithm")
                return
        except Exception as e:
            messagebox.showerror("Error", f"Error running algorithm: {str(e)}")
            return

        show_results(gantt, processes, wt, tat, ct, priorities if "Priority" in algo else None)

    # --- Display results ---
    def show_results(gantt_chart, processes, waiting_times, turnaround_times, completion_times, priorities=None):
        # --- Gantt chart ---
        canvas_width = 800
        canvas_height = 120  # Increased height to accommodate labels
        canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")
        canvas.grid(row=len(process_entries)+5, column=0, columnspan=5, pady=10, padx=10)  # Added padx for margin
        output_widgets.append(canvas)

        total_time = max(end for _, _, end in gantt_chart)
        # Add padding to prevent sticking to margins
        padding = 20  # pixels of padding on each side
        available_width = canvas_width - 2 * padding
        scale = max(1, available_width / (total_time + 1))
        colors = ["skyblue", "lightgreen", "salmon", "orange", "plum", "lightyellow", "lightcoral", "lightseagreen"]

        for i, (pid, start, end) in enumerate(gantt_chart):
            x1 = padding + start * scale
            x2 = padding + end * scale
            y1 = 40  # Moved down to make space for labels
            y2 = 80
            color = colors[i % len(colors)]
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black", width=2)
            canvas.create_text((x1+x2)/2, (y1+y2)/2, text=f"P{pid}", font=("Arial", 10, "bold"))
            
            # Draw time labels below the chart
            if i == 0:  # First process - show start time
                canvas.create_text(x1, y2+15, text=str(start), font=("Arial", 9))
            
            # Always show end time for each process
            canvas.create_text(x2, y2+15, text=str(end), font=("Arial", 9))

        # --- Stats table ---
        columns = ["PID", "Arrival", "Burst"]
        if priorities:
            columns.append("Priority")
        columns += ["Completion", "Waiting", "Turnaround"]

        tree = ttk.Treeview(root, columns=columns, show="headings", height=10)
        tree.grid(row=len(process_entries)+6, column=0, columnspan=5, pady=10, padx=10)
        output_widgets.append(tree)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=100)

        for pid, at, bt in processes:
            values = [pid, at, bt]
            if priorities:
                values.append(priorities[pid])
            values += [completion_times[pid], waiting_times[pid], turnaround_times[pid]]
            tree.insert("", tk.END, values=values)
            
        # Calculate and display averages
        avg_waiting = sum(waiting_times.values()) / len(waiting_times)
        avg_turnaround = sum(turnaround_times.values()) / len(turnaround_times)
        
        avg_label = tk.Label(root, text=f"Average Waiting Time: {avg_waiting:.2f} | Average Turnaround Time: {avg_turnaround:.2f}", 
                            font=("Arial", 12, "bold"))
        avg_label.grid(row=len(process_entries)+7, column=0, columnspan=5, pady=5)
        output_widgets.append(avg_label)

    tk.Button(root, text="Generate Process Form", command=generate_form).grid(row=0, column=2, padx=10)

    root.mainloop()
