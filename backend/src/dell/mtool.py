import json
import os
import re
import shutil
import subprocess
import sys


ansible_playbook = "ansible-playbook"
ansible_inventory_argument = "-i"
ansible_hosts_file = "hosts"
ansible_extra_vars = "--extra-vars"
ansible_user = "ansible_user="
ansible_password = " ansible_password="
collections_folder = "collections"
ansible_collections_folder = "ansible_collections"
aarohi_folder = "Aarohi"
verbose = "-vvv"
output_folder = "output"
process_terminated = "Process Terminated\n"
inventory = "[inventory]\n"
ansible_host = " ansible_host="
host_children = "[all:children]\ninventory"

log_file_clean = r"\x1b\[[0-9;]*[mK]"

license_key_command = "--vault-password-file=" + os.path.join(
    collections_folder,
    ansible_collections_folder,
    aarohi_folder,
    "license.key",
)

ansible_cpu_yml = "setup_config.yml"
password = "AarohiSolutions@Bangalore"


def remove_license():
    # Remove License Key
    if os.path.exists(
        os.path.join(collections_folder, ansible_collections_folder, aarohi_folder)
    ):
        shutil.rmtree(
            os.path.join(collections_folder, ansible_collections_folder, aarohi_folder)
        )


def create_license():
    # Create the collections/ansible_collections/Aarohi directory & Create License Key
    os.makedirs(
        os.path.join(
            collections_folder,
            ansible_collections_folder,
            aarohi_folder,
        )
    )

    with open(
        os.path.join(
            collections_folder,
            ansible_collections_folder,
            aarohi_folder,
            "license.key",
        ),
        "w",
    ) as file:
        file.write(password)


def create_hosts_file(hostname, ip_address):
    with open("hosts", "w") as hosts:
        hosts.write(inventory)
        hosts.write(f"{hostname} {ansible_host}{ip_address}\n\n")
        hosts.write(host_children)


def change_working_directory():
    os.chdir("../sonicos4")


def monitoring_tool(
    action, user, hostname, device_ip_address, device_user, device_password, monitor
):
    log = ""
    change_working_directory()

    if monitor == "cpu":
        extra_vars = f"{ansible_user}{device_user} {ansible_password}{device_password} monitor_cpu=true"
    elif monitor == "memory":
        extra_vars = f"{ansible_user}{device_user} {ansible_password}{device_password} monitor_memory=true"
    elif monitor == "interface":
        extra_vars = f"{ansible_user}{device_user} {ansible_password}{device_password} monitor_interface=true"
    elif monitor == "fan":
        extra_vars = f"{ansible_user}{device_user} {ansible_password}{device_password} monitor_fan=true"
    elif monitor == "temperature":
        extra_vars = f"{ansible_user}{device_user} {ansible_password}{device_password} monitor_temperature=true"

    ansible_file = ansible_cpu_yml

    create_hosts_file(hostname, device_ip_address)

    remove_license()
    # Create License Key
    create_license()

    ansible_command = [
        ansible_playbook,
        ansible_inventory_argument,
        ansible_hosts_file,
        ansible_extra_vars,
        extra_vars,
        ansible_file,
        license_key_command,
        verbose,
    ]
    print(ansible_command)
    process = subprocess.Popen(
        ansible_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )

    try:
        for line in iter(process.stdout.readline, b""):
            decoded_line = line.decode().strip()
            cleaned_line = re.sub(log_file_clean, "", decoded_line)
            print(cleaned_line, flush=True)
            log += cleaned_line + "\n"
        process.wait()

        if process.returncode == 0:
            remove_license()

            # CPU File
            if monitor == "cpu":
                input_cpu_file_name = f"{hostname}.cpu.txt"
                input_cpu_file_path = os.path.join(output_folder, input_cpu_file_name)
                cpu_data = {}
                with open(input_cpu_file_path, "r") as device_content:
                    for line in device_content:
                        pattern = "CPU-"
                        if line.startswith(pattern):
                            print(line.strip())
                            parts = line.split()
                            if len(parts) >= 4:
                                cpu_name = parts[0]
                                values = {
                                    "KERNEL": int(parts[1]),
                                    "USER": int(parts[2]),
                                    "IDLE": int(parts[3]),
                                }
                                cpu_data[cpu_name] = values

                # Convert the dictionary to JSON
                json_data = json.dumps(cpu_data, indent=4)

                # Print or save the JSON data
                print(json_data)

            elif monitor == "memory":
                input_cpu_file_name = f"{hostname}.memory.txt"
                input_cpu_file_path = os.path.join(output_folder, input_cpu_file_name)
                memory_data = {}
                with open(input_cpu_file_path, "r") as device_content:
                    for line in device_content:
                        pattern_1 = "Total"
                        pattern_2 = "Used"
                        if line.startswith(pattern_1) or line.startswith(pattern_2):
                            print(line.strip())
                            parts = line.split(":")
                            if len(parts) >= 2:
                                memory_name = parts[0].strip()
                                values = {
                                    "Value/State": int(parts[1]),
                                }
                                memory_data[memory_name] = values
                # Convert the dictionary to JSON
                json_data = json.dumps(memory_data, indent=4)

                # Print or save the JSON data
                print(json_data)

            elif monitor == "interface":
                input_cpu_file_name = f"{hostname}.interface.txt"
                input_cpu_file_path = os.path.join(output_folder, input_cpu_file_name)
                interface_data = {}
                with open(input_cpu_file_path, "r") as device_content:
                    for line in device_content:
                        print(line.strip())
                        pattern_1 = "Eth"
                        pattern_2 = "PortChannel"
                        if line.startswith(pattern_1) or line.startswith(pattern_2):
                            parts = line.split()
                            if len(parts) >= 7:
                                interface_name = parts[0].strip()
                                values = {
                                    "Description": parts[1],
                                    "Oper": parts[2],
                                    "Reason": parts[3],
                                    "AutoNeg": parts[4],
                                    "Speed": parts[5],
                                    "MTU": parts[6],
                                    "Alternate Name": parts[7],
                                }
                                interface_data[interface_name] = values
                # Convert the dictionary to JSON
                json_data = json.dumps(interface_data, indent=4)

                # Print or save the JSON data
                print(json_data)

            elif monitor == "fan":
                input_cpu_file_name = f"{hostname}.fan.txt"
                input_cpu_file_path = os.path.join(output_folder, input_cpu_file_name)
                fan_data = {}
                with open(input_cpu_file_path, "r") as device_content:
                    for line in device_content:
                        print(line.strip())
                        pattern_1 = "FAN"
                        if line.startswith(pattern_1):
                            parts = line.split()
                            if len(parts) >= 4:
                                fan_name = parts[0] + parts[1]
                                values = {
                                    "Status": parts[2],
                                    "Speed (RPM)": parts[3],
                                    "Direction": parts[4],
                                }
                                fan_data[fan_name] = values
                # Convert the dictionary to JSON
                json_data = json.dumps(fan_data, indent=4)

                # Print or save the JSON data
                print(json_data)

            elif monitor == "temperature":
                input_cpu_file_name = f"{hostname}.temperature.txt"
                input_cpu_file_path = os.path.join(output_folder, input_cpu_file_name)
                temperature_data = {}
                with open(input_cpu_file_path, "r") as device_content:
                    for line in device_content:
                        print(line.strip())
                        pattern_1 = "Name"
                        if not line.startswith(pattern_1):
                            parts = line.split()
                            if len(parts) >= 8:
                                temperature_name = parts[0]
                                values = {
                                    "Temperature": parts[1],
                                    "High (TH)": parts[2],
                                    "Low (TH)": parts[3],
                                    "Critical High (TH)": parts[3],
                                    "Critical Low (TH)": parts[3],
                                    "Warning": parts[3],
                                }
                                temperature_data[temperature_name] = values

                # Convert the dictionary to JSON
                json_data = json.dumps(temperature_data, indent=4)

                # Print or save the JSON data
                print(json_data)

        if process.returncode != 0:
            remove_license()
            print("Failed")
            with open(os.path.join(output_folder, "error.log"), "w") as error_log:
                error_log.write(log)
    except KeyboardInterrupt:
        process.terminate()
        process.wait()
        remove_license()
        print("Terminated")
        log += process_terminated
        with open(os.path.join(output_folder, "error.log"), "w") as error_log:
            error_log.write(log)
    except Exception as e:
        log += str(e)
        remove_license()
        with open(os.path.join(output_folder, "error.log"), "w") as error_log:
            error_log.write(log)

    return process.returncode


if __name__ == "__main__":
    if len(sys.argv) < 1:
        print("Invalid command!")
        sys.exit(1000)
    action = sys.argv[1]
    user = sys.argv[2]
    host_name = sys.argv[3]
    ip = sys.argv[4]
    user_name = sys.argv[5]
    password = sys.argv[6]
    monitor = sys.argv[7]
    print(user)
    monitoring_tool(
        action,
        user,
        host_name,
        ip,
        user_name,
        password,
        monitor,
    )
# python3 mtool.py cpu dell test 192.168.2.216 admin YourPaSsWoRd
