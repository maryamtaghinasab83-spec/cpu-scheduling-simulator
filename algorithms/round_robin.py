from collections import deque


def round_robin(processes, time_quantum):
    """
    TODO: Implement Round Robin CPU scheduling algorithm

    Round Robin is a preemptive scheduling algorithm where each process 
    gets a fixed time quantum for execution. If a process doesn't complete
    within its time quantum, it's preempted and moved to the back of the ready queue.

    Args:
        processes: List of tuples where each tuple represents a process
                  Format: (process_id, arrival_time, burst_time)
        time_quantum: Integer representing the fixed time slice for each process

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
    # Sort processes by arrival time
    sorted_processes = sorted(processes, key=lambda x: x[1])

    # TODO: Step 2 - Initialize data structures
    # Initialize remaining burst times
    remaining_burst = {pid: burst for pid, arrival, burst in sorted_processes}

    # Initialize waiting times for all processes
    for pid, arrival, burst in sorted_processes:
        waiting_times[pid] = 0

    # Create queue for ready processes
    ready_queue = deque()

    # Track processes that haven't arrived yet
    remaining_processes = sorted_processes.copy()

    # Initialize current time
    current_time = 0

    # Track last time each process was executed (for calculating waiting time)
    last_execution_time = {}

    # TODO: Step 3 - Main scheduling loop
    # Add initial processes that arrive at time 0
    while remaining_processes and remaining_processes[0][1] <= current_time:
        pid, arrival, burst = remaining_processes.pop(0)
        ready_queue.append(pid)
        last_execution_time[pid] = arrival

    while ready_queue or remaining_processes:
        # If no process is ready but some are still pending
        if not ready_queue:
            # Jump to arrival time of next process
            next_arrival = remaining_processes[0][1]
            current_time = next_arrival

            # Add all processes that arrive at this time
            while remaining_processes and remaining_processes[0][1] <= current_time:
                pid, arrival, burst = remaining_processes.pop(0)
                ready_queue.append(pid)
                last_execution_time[pid] = arrival
            continue

        # Get next process from ready queue
        current_pid = ready_queue.popleft()

        # Calculate execution time for this quantum
        execution_time = min(remaining_burst[current_pid], time_quantum)

        # Calculate start time
        start_time = current_time

        # Update waiting time for this process
        if current_pid in last_execution_time:
            waiting_times[current_pid] += (start_time - last_execution_time[current_pid])

        # Execute the process
        current_time += execution_time
        remaining_burst[current_pid] -= execution_time

        # Add processes that arrived during this execution
        while remaining_processes and remaining_processes[0][1] <= current_time:
            pid, arrival, burst = remaining_processes.pop(0)
            ready_queue.append(pid)
            last_execution_time[pid] = arrival

        # Record in Gantt chart
        gantt_chart.append((current_pid, start_time, current_time))

        # Update last execution time
        last_execution_time[current_pid] = current_time

        # If process still has remaining burst time, add it back to queue
        if remaining_burst[current_pid] > 0:
            ready_queue.append(current_pid)
        else:
            # Process completed
            completion_times[current_pid] = current_time

    # TODO: Step 4 - Return the results
    # Calculate turnaround times for all processes
    for pid, arrival, burst in processes:
        turnaround_times[pid] = completion_times[pid] - arrival

    return gantt_chart, waiting_times, turnaround_times, completion_times