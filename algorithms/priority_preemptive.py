def priority_non_preemptive(processes, priorities):
    """
    TODO: Implement Priority Non-Preemptive CPU scheduling algorithm

    Priority Non-Preemptive is a scheduling algorithm where processes are executed 
    based on their priority (higher priority first) without preemption.
    When multiple processes are available, the one with highest priority is selected.

    Args:
        processes: List of tuples where each tuple represents a process
                  Format: (process_id, arrival_time, burst_time)
        priorities: Dictionary mapping process_id to priority value
                   Format: {pid: priority}
                   Note: Higher value = Higher priority

    Returns:
        tuple: (gantt_chart, waiting_times, turnaround_times, completion_times)
        - gantt_chart: List of tuples (pid, start_time, end_time)
        - waiting_times: Dictionary {pid: waiting_time}
        - turnaround_times: Dictionary {pid: turnaround_time}
        - completion_times: Dictionary {pid: completion_time}
    """

    # TODO: Step 1 - Sort processes by arrival time
    # Sort processes by arrival time to handle them in arrival order
    sorted_processes = sorted(processes, key=lambda x: x[1])

    # TODO: Step 2 - Initialize current_time and remaining processes list
    current_time = 0
    gantt_chart = []
    waiting_times = {}
    turnaround_times = {}
    completion_times = {}

    # Create a list to track processes that haven't been executed yet
    remaining_processes = sorted_processes.copy()
    # Create a list for processes that have arrived but not executed
    ready_queue = []

    # TODO: Step 3 - Process scheduling loop
    while remaining_processes or ready_queue:
        # Move processes that have arrived by current_time to ready queue
        arrived_processes = []
        for process in remaining_processes[:]:  # Use copy for safe iteration
            if process[1] <= current_time:
                arrived_processes.append(process)
                remaining_processes.remove(process)

        ready_queue.extend(arrived_processes)

        # If ready queue is empty but there are still remaining processes,
        # jump to the arrival time of the next process
        if not ready_queue and remaining_processes:
            # Find the next arriving process
            next_process = min(remaining_processes, key=lambda x: x[1])
            current_time = next_process[1]
            continue

        # Select process with highest priority from ready queue
        # Higher priority value = higher priority
        selected_process = max(ready_queue, key=lambda p: priorities[p[0]])
        ready_queue.remove(selected_process)

        pid, arrival, burst = selected_process

        # Calculate start time (if process arrived after current_time, start at arrival time)
        start_time = max(current_time, arrival)
        end_time = start_time + burst

        # Add to Gantt chart
        gantt_chart.append((pid, start_time, end_time))

        # Update current_time
        current_time = end_time

        # Calculate completion time
        completion_times[pid] = end_time

        # Calculate turnaround time
        turnaround_times[pid] = end_time - arrival

        # Calculate waiting time
        waiting_times[pid] = turnaround_times[pid] - burst

    # TODO: Step 4 - Return the results
    return gantt_chart, waiting_times, turnaround_times, completion_times