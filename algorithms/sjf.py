def sjf(processes):
    """
    TODO: Implement Shortest Job First (SJF) CPU scheduling algorithm

    SJF is a non-preemptive scheduling algorithm where the process with 
    the smallest burst time is selected for execution next.
    When multiple processes are available, the one with shortest burst time runs first.

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

    # TODO: Step 1 - Sort processes by arrival time (and burst time for ties)
    # Sort processes by arrival time first, then burst time for processes with same arrival
    sorted_processes = sorted(processes, key=lambda x: (x[1], x[2]))

    # TODO: Step 2 - Initialize variables
    current_time = 0
    remaining_processes = sorted_processes.copy()
    ready_queue = []

    # Initialize waiting times for all processes
    for pid, arrival, burst in processes:
        waiting_times[pid] = 0
        turnaround_times[pid] = 0
        completion_times[pid] = 0

    # TODO: Step 3 - Main scheduling loop
    while remaining_processes or ready_queue:
        # Add processes that have arrived by current_time to ready queue
        arrived_processes = []
        for process in remaining_processes[:]:
            pid, arrival, burst = process
            if arrival <= current_time:
                arrived_processes.append(process)
                remaining_processes.remove(process)

        ready_queue.extend(arrived_processes)

        # If ready queue is empty but processes remain, jump to next arrival
        if not ready_queue and remaining_processes:
            next_process = min(remaining_processes, key=lambda x: x[1])
            current_time = next_process[1]
            continue

        # Select process with shortest burst time from ready queue
        if ready_queue:
            # Sort ready queue by burst time (shortest first)
            ready_queue.sort(key=lambda x: x[2])
            selected_process = ready_queue.pop(0)

            pid, arrival, burst = selected_process

            # Calculate start time
            start_time = max(current_time, arrival)
            end_time = start_time + burst

            # Update current time
            current_time = end_time

            # Add to Gantt chart
            gantt_chart.append((pid, start_time, end_time))

            # Calculate completion time
            completion_times[pid] = end_time

            # Calculate turnaround time
            turnaround_times[pid] = end_time - arrival

            # Calculate waiting time
            waiting_times[pid] = turnaround_times[pid] - burst

    # TODO: Step 4 - Return the results
    return gantt_chart, waiting_times, turnaround_times, completion_times