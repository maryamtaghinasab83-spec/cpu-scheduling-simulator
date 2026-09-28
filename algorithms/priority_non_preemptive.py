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

    # Step 1 - Sort processes by arrival time
    sorted_processes = sorted(processes, key=lambda x: x[1])

    # Step 2 - Initialize current_time and remaining processes list
    current_time = 0
    gantt_chart = []
    waiting_times = {}
    turnaround_times = {}
    completion_times = {}

    # لیست فرآیندهای باقی‌مانده
    remaining_processes = list(sorted_processes)

    # Step 3 - Process scheduling loop
    while remaining_processes:
        # پیدا کردن فرآیندهای رسیده تا زمان فعلی
        available_processes = [
            p for p in remaining_processes
            if p[1] <= current_time
        ]

        if not available_processes:
            # اگر هیچ فرآیندی نرسیده، به زمان اولین فرآیند برو
            next_arrival = min(p[1] for p in remaining_processes)
            idle_time = next_arrival - current_time
            if idle_time > 0:
                gantt_chart.append(('IDLE', current_time, next_arrival))
            current_time = next_arrival
            continue

        # انتخاب فرآیند با بالاترین اولویت
        # اگر اولویت مساوی بود، اول فرآیندی که زودتر رسیده انتخاب می‌شود
        selected_process = max(
            available_processes,
            key=lambda p: (priorities[p[0]], -p[1])  # اولویت بالاتر، زمان ورود کمتر
        )

        pid, arrival_time, burst_time = selected_process

        # حذف از لیست فرآیندهای باقی‌مانده
        remaining_processes.remove(selected_process)

        start_time = current_time
        end_time = start_time + burst_time
        current_time = end_time

        # افزودن به نمودار گانت
        gantt_chart.append((pid, start_time, end_time))

        # محاسبه زمان‌ها
        completion_times[pid] = end_time
        turnaround_times[pid] = end_time - arrival_time
        waiting_times[pid] = turnaround_times[pid] - burst_time

    # Step 4 - Return the results
    return gantt_chart, waiting_times, turnaround_times, completion_times