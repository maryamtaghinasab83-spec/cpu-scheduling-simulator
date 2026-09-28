def srtf(processes):
    """
    TODO: Implement Shortest Remaining Time First (SRTF) CPU scheduling algorithm

    SRTF is a preemptive version of SJF where the process with the smallest
    remaining burst time is selected for execution at every time unit.
    A running process can be preempted if a new process arrives with shorter remaining time.

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

    # TODO: Step 1 - Initialize data structures
    # Sort processes by arrival time
    sorted_processes = sorted(processes, key=lambda x: x[1])

    # Initialize remaining burst times
    remaining_burst = {pid: burst for pid, arrival, burst in sorted_processes}

    # Initialize waiting times and arrival times
    arrival_times = {pid: arrival for pid, arrival, burst in sorted_processes}

    for pid, arrival, burst in sorted_processes:
        waiting_times[pid] = 0
        completion_times[pid] = 0

    # Create list for processes that haven't arrived yet
    remaining_processes = sorted_processes.copy()

    # Track current process and time
    current_time = 0
    current_pid = None
    current_start_time = 0

    # TODO: Step 2 - Main scheduling loop
    while any(remaining_burst[pid] > 0 for pid in remaining_burst) or remaining_processes:
        # Add processes that have arrived by current_time
        arrived_processes = []
        for process in remaining_processes[:]:
            pid, arrival, burst = process
            if arrival <= current_time:
                arrived_processes.append(pid)
                remaining_processes.remove(process)

        # If there are processes ready to execute
        ready_pids = [pid for pid in remaining_burst if remaining_burst[pid] > 0
                      and arrival_times[pid] <= current_time]

        if ready_pids:
            # Select process with shortest remaining time
            # In case of tie, choose the one that arrived first
            selected_pid = min(ready_pids,
                               key=lambda pid: (remaining_burst[pid], arrival_times[pid]))

            # If process changes, record the previous one in Gantt chart
            if selected_pid != current_pid:
                if current_pid is not None:
                    gantt_chart.append((current_pid, current_start_time, current_time))
                current_pid = selected_pid
                current_start_time = current_time

            # Execute the selected process for 1 time unit
            remaining_burst[selected_pid] -= 1
            current_time += 1

            # Update waiting times for other ready processes
            for pid in ready_pids:
                if pid != selected_pid:
                    waiting_times[pid] += 1

            # If process is completed
            if remaining_burst[selected_pid] == 0:
                completion_times[selected_pid] = current_time
                if selected_pid == current_pid:
                    gantt_chart.append((current_pid, current_start_time, current_time))
                    current_pid = None
        else:
            # No process is ready, advance time to next arrival
            if remaining_processes:
                next_arrival = min(remaining_processes, key=lambda x: x[1])[1]
                current_time = next_arrival
            else:
                current_time += 1

    # TODO: Step 3 - Convert gantt_chart to tuples and return results
    # Calculate turnaround times
    for pid in arrival_times:
        turnaround_times[pid] = completion_times[pid] - arrival_times[pid]

    return gantt_chart, waiting_times, turnaround_times, completion_times