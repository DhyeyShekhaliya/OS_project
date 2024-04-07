import streamlit as st
#from streamlit_option_menu import option_menu
#import plotly.graph_objects as go
import pandas as pd
#import streamlit_shadcn_ui as ui

class Process:
    def __init__(self):
        self.pos = 0
        self.AT = 0
        self.BT = 0
        self.ST = [0] * 20
        self.WT = 0
        self.FT = 0
        self.TAT = 0
        
def SCAN(arr, head, direction):
    seek_count = 0
    distance, cur_track = 0, 0
    left = []
    right = []
    seek_sequence = []

    disk_size = len(arr)  # Calculate the size of the request array

    if direction == "left":
        left.append(0)
    elif direction == "right":
        right.append(disk_size - 1)

    for i in range(len(arr)):  # Iterate over the length of the request array
        if arr[i] < head:
            left.append(arr[i])
        if arr[i] > head:
            right.append(arr[i])

    left.sort()
    right.sort()

    run = 2
    while run != 0:
        if direction == "left":
            for i in range(len(left) - 1, -1, -1):
                cur_track = left[i]
                seek_sequence.append(cur_track)
                distance = abs(cur_track - head)
                seek_count += distance
                head = cur_track
            
            direction = "right"
    
        elif direction == "right":
            for i in range(len(right)):
                cur_track = right[i]
                seek_sequence.append(cur_track)
                distance = abs(cur_track - head)
                seek_count += distance
                head = cur_track
            
            direction = "left"
        
        run -= 1

    return seek_count, seek_sequence

def mru_page_replacement(reference_string, frames):
    hit = 0
    fault_count = 0
    page = [9999] * frames
    mru = [9999] * len(reference_string)

    for i in range(len(reference_string)):
        hit = 0
        for j in range(frames):
            if page[j] == reference_string[i]:
                hit = 1
                fault_count += 1
                break

        if hit == 0:
            for j in range(frames):
                page_get = page[j]
                for j2 in range(i, len(reference_string)):
                    if page_get == reference_string[j2]:
                        mru[j] = j2
                        cap = 1
                        break
                    else:
                        cap = 0
                if cap == 0:
                    mru[j] = 9999

            maximum = -9999
            for j in range(frames):
                if mru[j] > maximum:
                    maximum = mru[j]
                    repeat = j
            page[repeat] = reference_string[i]

    return fault_count, len(reference_string) - fault_count

def main():
  
    gannt_chart = []
    st.set_page_config(layout="wide")

   
    selected = option_menu(
        menu_title=None,
        options=["Round Robin", "Banker's Algorithm", "Scan-Disk Scheduling", "Most Recently Used [MRU] Page Repelacment"],
        orientation="horizontal",
    )

    
    st.write("""
        Welcome to the OS Simulator! Choose the algorithms from the left sidebar to learn more and run simulations.
    """)

    if selected == "Round Robin":
        st.title("Round Robin Scheduling Simulator")

        col1, col2, col3 = st.columns([1, 1, 2])  # Adjust column widths as needed

        n = col1.number_input("Enter the no. of processes:", min_value=1, step=1, value=1)
        quant = col2.number_input("Enter the quantum:", min_value=1, step=1, value=1)

        col3.write("Enter process details:")
        p = [Process() for _ in range(n)]
        for i in range(n):
            p[i].pos = col3.number_input(f"Process {i+1} number:", min_value=1, step=1, value=1)
            p[i].AT = col3.number_input(f"Arrival time of Process {i+1}:", min_value=0, step=1, value=0)
            p[i].BT = col3.number_input(f"Burst time of Process {i+1}:", min_value=1, step=1, value=1)

        c = n
        time = 0
        index = -1
        s = [[-1] * 20 for _ in range(n)]
        b = [p[i].BT for i in range(n)]
        a = [p[i].AT for i in range(n)]
        tot_wt = 0
        tot_tat = 0

        gantt_data = []  # Data for Gantt chart

        while c != 0:
            mini = float("inf")
            flag = False

            for i in range(n):
                pTime = time + 0.1
                if a[i] <= pTime and b[i] > 0:
                    if mini > a[i]:
                        index = i
                        mini = a[i]
                        flag = True

            if not flag:
                time += 1
                continue

            j = 0
            while s[index][j] != -1:
                j += 1

            if s[index][j] == -1:
                s[index][j] = time
                p[index].ST[j] = time

            if b[index] <= quant:
                time += b[index]
                b[index] = 0
            else:
                time += quant
                b[index] -= quant

            if b[index] > 0:
                a[index] = time + 0.1

            if b[index] == 0:
                c -= 1
                p[index].FT = time
                p[index].WT = p[index].FT - p[index].AT - p[index].BT
                tot_wt += p[index].WT
                p[index].TAT = p[index].BT + p[index].WT
                tot_tat += p[index].TAT

            # Append data for Gantt chart
            gantt_data.append({
                'Process': f'P{p[index].pos}',
                'Start': p[index].ST[j],
                'End': time
            })

        st.header("Gantt Chart")
        plot_gantt_chart(gantt_data)

        # Display results and averages
        st.header("Results")
        df_results = pd.DataFrame(columns=["Process Number", "Arrival Time", "Burst Time", "Waiting Time", "Turnaround Time"])
        for i in range(n):
            df_results.loc[i] = [p[i].pos, p[i].AT, p[i].BT, p[i].WT, p[i].TAT]
        st.table(df_results)

        avg_wt = tot_wt / n
        avg_tat = tot_tat / n

        st.write(f"The average wait time is : {avg_wt}")
        st.write(f"The average TurnAround time is : {avg_tat}")

    elif selected == "Banker's Algorithm":
         
        st.title("BANKER'S ALGORITHM")

   
        st.header("RESOURCES")

       
        resourcesNumber = st.number_input("Please enter the number of resources:", min_value=1, step=1, value=1)

       
        if resourcesNumber < 0:
            st.error("Don't try and be a smartass. Enter a positive integer.")

      
        resources_values = []
        cols = st.columns(resourcesNumber)  
        for i in range(resourcesNumber):
            with cols[i]:
                quantity = st.number_input(f"Quantity of resource {chr(65 + i)} available:", min_value=0, step=1, value=0, key=f"resource_{i}")
                resources_values.append(quantity)

       
        resources_labels = [chr(65 + i) for i in range(resourcesNumber)]
        resources_table = pd.DataFrame({"Resources": resources_labels, "Total Available": resources_values})

       
        st.table(resources_table.T)  

       
        st.header("PROCESSES")

        
        processesNumber = st.number_input("Please enter the number of processes:", min_value=1, step=1, value=1)

       
        process_names = []
        cols = st.columns(processesNumber) 
        for i in range(processesNumber):
            with cols[i]:
                process_name = st.text_input(f"Enter the name of process {i + 1}:")
                process_names.append(process_name)

        
        st.header("ALLOCATION")

       
        available_resources = resources_values.copy()

      
        allocation_table = pd.DataFrame(index=process_names, columns=resources_labels)

        for i, process in enumerate(process_names):
            st.subheader(f"Allocation for Process {process}")
            cols = st.columns(resourcesNumber)  
            allocation_values = []
            for j, resource in enumerate(allocation_table.columns):
                with cols[j]:
                    allocation_value = st.number_input(f"Enter allocation for {resource}:", min_value=0, step=1, value=0, key=f"allocation_{i}_{j}")
                    allocation_values.append(allocation_value)
                    if allocation_value > available_resources[j]:
                        st.error(f"Not enough {resource} resources available for allocation.")
                    allocation_table.at[process, resource] = allocation_value

         
            available_resources = [available - allocated for available, allocated in zip(available_resources, allocation_values)]

      
        total_resources_allocated = allocation_table.sum().tolist()

       
        allocation_table.loc["Total"] = total_resources_allocated

  
        if all(available >= 0 for available in available_resources):
            st.table(allocation_table)
        else:
            st.error("Invalid allocation. Please ensure allocated resources do not exceed available resources.")

        
        available = [resources_values[i] - total_resources_allocated[i] for i in range(resourcesNumber)]

        available_resources_table = pd.DataFrame({"Resources": resources_labels, "Available": available})
        st.header("AVAILABLE RESOURCES")
        st.table(available_resources_table)

        
        st.header("MAXIMUM NEED")

     
        max_need_table = pd.DataFrame(index=process_names, columns=resources_labels)

     
        for i, process in enumerate(process_names):
            st.subheader(f"Maximum need for Process {process}")
            cols = st.columns(resourcesNumber)  
            for j, resource in enumerate(resources_labels):
                with cols[j]:
                    max_need_value = st.number_input(f"Enter maximum need for {resource}:", min_value=0, step=1, value=0, key=f"max_need_{i}_{j}")
                    max_need_table.at[process, resource] = max_need_value

       
        st.table(max_need_table)

       
        remaining_need = [[max_need_table.iloc[i, j] - allocation_table.iloc[i, j] for j in range(resourcesNumber)] for i in range(processesNumber)]

        st.header("REMAINING NEED")
        remaining_need_table = pd.DataFrame(data=remaining_need, index=process_names, columns=resources_labels)
        st.table(remaining_need_table)

    
        count = 0
        j = 0
        for k in range(len(remaining_need) - count):
            for i in range(len(remaining_need)):
                if j + 2 < len(available) and available[j] >= remaining_need[i][j] and available[j + 1] >= remaining_need[i][j + 1] and available[j + 2] >= remaining_need[i][j + 2]:
                    st.write(process_names[i])
                    available[0] += allocation_table.iloc[i, 0]
                    available[1] += allocation_table.iloc[i, 1]
                    available[2] += allocation_table.iloc[i, 2]
                    st.write(f"Available: {available[0]} {available[1]} {available[2]}")
                    remaining_need[i][j] = float('inf')
                    remaining_need[i][j + 1] = float('inf')
                    remaining_need[i][j + 2] = float('inf')
                    count += 1
        if count < len(remaining_need) - 1:
            st.write("Deadlock has occurred")
        
        else:
            st.write("The above is a safe sequence")


    elif selected == "Scan-Disk Scheduling":


        st.title("SCAN Disk Scheduling Algorithm")

        st.header("Input Parameters")
        arr_input = st.text_input("Enter the request array (comma-separated values):")
        if arr_input:
            arr = [int(x.strip()) for x in arr_input.split(",")]
        else:
            arr = []
        head = st.number_input("Enter the initial head position:", value=0, step=1)
        direction = st.selectbox("Select the initial direction:", ("left", "right"))

        # Execute SCAN algorithm
        if st.button("Run SCAN Algorithm") and arr:
            seek_count, seek_sequence = SCAN(arr, head, direction)
            st.success(f"Total number of seek operations = {seek_count}")
            st.header("Seek Sequence")
            for i in range(len(seek_sequence)):
                st.write(seek_sequence[i])     
            plot_scan_disk(seek_sequence, head)    
            
    elif selected == "Most Recently Used [MRU] Page Repelacment":

       st.title("Most Recently Used (MRU) Page Replacement Algorithm")

    frames = st.number_input("Number of Frames:", min_value=1, step=1)
    references = st.number_input("Number of References:", min_value=1, step=1)

    reference_string = []
    for i in range(references):
        reference = st.number_input(f"Reference String {i+1}:", step=1)
        reference_string.append(reference)

    if st.button("Simulate"):
        fault_count, hit_count = mru_page_replacement(reference_string, frames)
        st.write(f"Total Page Faults: {fault_count}")
        st.write(f"Total Page Hits: {hit_count}")
        
def plot_gantt_chart(gantt_chart):
    df = pd.DataFrame(gantt_chart, columns=['Process', 'Start', 'End'])
    fig = go.Figure()
    for i, row in df.iterrows():
        fig.add_trace(go.Bar(x=[row['Start'], row['End']], y=[row['Process'], row['Process']],
                             orientation='h', name=f'Process {row["Process"]}'))
    fig.update_layout(barmode='relative', title='Gantt Chart', xaxis_title='Time', yaxis_title='Process')
    st.plotly_chart(fig)

def plot_scan_disk(seek_sequence, head):
    fig = go.Figure()

    # Add initial head position as a marker
    fig.add_trace(go.Scatter(x=[head], y=[0], mode='markers', name='Initial Head Position', marker=dict(color='red', size=10)))

    # Add disk seek sequence as line segments
    for i in range(len(seek_sequence) - 1):
        fig.add_trace(go.Scatter(x=[seek_sequence[i], seek_sequence[i + 1]], y=[0, 0], mode='lines+markers', name=f'Seek {i + 1}'))

    # Set layout and display the figure
    fig.update_layout(title='SCAN Disk Scheduling', xaxis_title='Disk Track', yaxis_title='Seek Operations', showlegend=True)
    st.plotly_chart(fig)

if __name__ == '__main__':
    main()
