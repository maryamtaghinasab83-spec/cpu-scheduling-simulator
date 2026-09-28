# algorithms/fcfs.py

def fcfs(processes):
    """
    TODO: Implement First-Come, First-Served (FCFS) CPU scheduling algorithm

    FCFS is a non-preemptive scheduling algorithm where processes are executed 
    in the order of their arrival time.

    Args:
        processes: List of tuples where each tuple represents a process
                  Format: (process_id, arrival_time, burst_time)

    Returns:
        tuple: (gantt_chart, waiting_times, turnaround_times, completion_times)
        - gantt_chart: List of tuples (pid, start_time, end_time)
        - waiting_times: Dictionary {pid: waiting_time}
        - turnaround_times: Dictionary {pid: turnaround_time}
        - completion_times: Dictionary {pid: completion_time}
    """

    # TODO: 
    # Currently returning empty data - replace with your implementation

    gantt_chart = []
    waiting_times = {}
    turnaround_times = {}
    completion_times = {}

    # TODO: Step 1 - Sort processes by arrival time
    # اگر دو فرآیند همزمان برسند، بر اساس PID مرتب می‌کنیم
    sorted_processes = sorted(processes, key=lambda x: (x[1], x[0]))

    # TODO: Step 2 - Initialize current_time
    current_time = 0

    # TODO: Step 3 - Process each job in FCFS order
    for i, (pid, arrival_time, burst_time) in enumerate(sorted_processes):
        # اگر فرآیند هنوز نرسیده باشد
        if arrival_time > current_time:
            # زمان بیکاری CPU به نمودار گانت اضافه می‌شود
            gantt_chart.append(('IDLE', current_time, arrival_time))
            current_time = arrival_time

        start_time = current_time
        completion_time = start_time + burst_time
        current_time = completion_time

        # اضافه کردن اجرای فرآیند به نمودار گانت
        gantt_chart.append((pid, start_time, completion_time))

        # ذخیره زمان تکمیل
        completion_times[pid] = completion_time

        # محاسبه زمان چرخش (Turnaround Time)
        turnaround_time = completion_time - arrival_time
        turnaround_times[pid] = turnaround_time

        # محاسبه زمان انتظار (Waiting Time)
        waiting_time = turnaround_time - burst_time
        waiting_times[pid] = waiting_time

    # TODO: Step 4 - Return the results
    return gantt_chart, waiting_times, turnaround_times, completion_times