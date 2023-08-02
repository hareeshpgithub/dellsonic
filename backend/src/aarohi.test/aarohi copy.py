import subprocess
import os
import shutil
import sys
import re
import time
import datetime
import yaml
import ansible.constants as C

ansible_version = C.__version__
python_version = sys.version.split()[0]

from datetime import datetime
from pymongo import MongoClient
from tzlocal import get_localzone

connection_url = "mongodb://localhost:27017/"
database_name = "Aarohi"

client = MongoClient(connection_url)

database = client[database_name]

device_info_collection = database["deviceInfo"]
device_backup_collection = database["deviceBackup"]

log_collection = database["logs"]

os.environ["TERM"] = "xterm-256color"
os.environ["ANSIBLE_FORCE_COLOR"] = "true"

collections_folder = "collections"
ansible_collections_folder = "ansible_collections"
aarohi_folder = "Aarohi"
yaml_folder = "yaml"
password = "AarohiSolutions@Bangalore"
license_key_command = "--vault-password-file=" + os.path.join(
    collections_folder,
    ansible_collections_folder,
    aarohi_folder,
    "license.key",
)
verbose = "-vvv"
output_folder = "output"
newline = "\n"
inventory = "[inventory]\n"
ansible_host = " ansible_host="
host_children = "[all:children]\ninventory"
ansible_user = "ansible_user="
ansible_password = " ansible_password="
log_file_name = "log.txt"
log_file_clean = r"\x1b\[[0-9;]*[mK]"
ansible_playbook = "ansible-playbook"
ansible_inventory_argument = "-i"
ansible_hosts_file = "hosts"
ansible_extra_vars = "--extra-vars"
ansible_device_information_yml = "get_device_info.yml"
ansible_device_backup_yml = "get_device_backup.yml"
ansible_device_deploy_yml = "setup_config.yml"
info_file = "info"
backup_file = "backup"
deploy_file = "deploy"
process_terminated = "Process Terminated\n"
system_timezone = get_localzone()

region = str(system_timezone)  # "Asia/Kolkata"
date_time_format = "%d-%b-%Y %H:%M:%S %p"
aarohi_version = "1.0.0"

debugging_mode = True
mongo_initializing = "Initializing"
mongo_completed = "Completed"
mongo_failed = "Failed"

# region Working Directory


def change_working_directory_sonicos4():
    os.chdir("../sonicos4")


# endregion

# region Licenst


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


def remove_license():
    # Remove License Key
    if os.path.exists(
        os.path.join(collections_folder, ansible_collections_folder, aarohi_folder)
    ):
        shutil.rmtree(
            os.path.join(collections_folder, ansible_collections_folder, aarohi_folder)
        )


# endregion

# region Create Hosts File


def create_hosts_file(hostname, ip_address):
    with open("hosts", "w") as hosts:
        hosts.write(inventory)
        hosts.write(f"{hostname} {ansible_host}{ip_address}\n\n")
        hosts.write(host_children)


# endregion

# region Mongo database Actions


def create_new_document(
    action,
    user,
    hostname,
    device_ip_address,
    device_user,
    device_password,
    exceution_start_time,
    ansible_command_string,
    input_yml,
):
    new_document = {
        "action": action,
        "user": user,
        "hostname": hostname,
        "host_ip_address": device_ip_address,
        "host_user": device_user,
        "host_password": device_password,
        "ansible_start_time": exceution_start_time.strftime(date_time_format),
        "ansible_start_unix_timestamp": int(time.time()),
        "command": ansible_command_string,
        "yml_configuration": input_yml,
        "status": mongo_initializing,
        "ansible_version": ansible_version,
        "python_version": python_version,
    }
    result = log_collection.insert_one(new_document)
    return result.inserted_id


def update_document(
    mongo_id, exceution_end_time, exceution_elapsed_time_seconds, output, log, exit_code
):
    elapsed_seconds = (
        exceution_elapsed_time_seconds.total_seconds()
        if hasattr(exceution_elapsed_time_seconds, "total_seconds")
        else (
            exceution_elapsed_time_seconds.microseconds / 1000000.0
            + exceution_elapsed_time_seconds.seconds
        )
    )

    minutes = int((elapsed_seconds // 60) % 60)
    seconds = int(elapsed_seconds % 60)
    milliseconds = int((elapsed_seconds % 1) * 1000)

    # Format minutes and seconds with appropriate pluralization
    minutes_label = "minute" if minutes == 1 else "minutes"
    seconds_label = "second" if seconds == 1 else "seconds"

    formatted_output = f"{minutes} {minutes_label} {seconds} {seconds_label} and {milliseconds} milliseconds"

    update_document = {
        "ansible_end_time": exceution_end_time.strftime(date_time_format),
        "ansible_end_unix_timestamp": int(time.time()),
        "ansible_execution_time": elapsed_seconds,
        "ansible_execution_human_readable": formatted_output,
        "output": output,
        "log": log,
        "exit_code": exit_code,
        "status": mongo_completed if exit_code == 0 else mongo_failed,
    }

    log_collection.update_one({"_id": mongo_id}, {"$set": update_document})


# endregion

# region Get Device Information / Get Device Backup


def device_safe_commands(
    action, user, hostname, device_ip_address, device_user, device_password, file_input
):
    log = ""
    output = None
    input_yml = None

    # Change working Directory
    change_working_directory_sonicos4()

    # Execution Start Date Time
    exceution_start_time = datetime.now()

    extra_vars = f"{ansible_user}{device_user} {ansible_password}{device_password}"
    if action == "get_device_information":
        ansible_file = ansible_device_information_yml
        log_file_extenstion = info_file
        action_name = "Get Device Information"
    elif action == "get_device_backup":
        ansible_file = ansible_device_backup_yml
        log_file_extenstion = backup_file
        action_name = "Get Device Backup"
    elif action == "deploy_configuration":
        file_input_path = os.path.join("../", "../", "uploads", file_input)
        file_ouput_name = f"{hostname}.yml"
        file_ouput_path = os.path.join("host_Vars", file_ouput_name)
        if os.path.exists(file_ouput_path):
            new_file_name = f"{hostname}.{int(time.time())}.yml"
            new_file_path = os.path.join("host_Vars", new_file_name)
            os.rename(file_ouput_path, new_file_path)

        shutil.copyfile(file_input_path, file_ouput_path)
        print(file_input_path, file_ouput_path)
        ansible_file = ansible_device_deploy_yml
        log_file_extenstion = deploy_file
        action_name = "Deploy Configuration"

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

    # Remove License Key from ansible_command (to save in mongodb)
    ansible_command_array = ansible_command.copy()
    ansible_command_array.remove(license_key_command)
    ansible_command_string = " ".join(ansible_command_array)

    # Replace ansible_password value with asterisks
    ansible_command_string = ansible_command_string.replace(
        f"ansible_password={device_password}", "ansible_password=****"
    )

    # Insert New Record into Mongo
    mongo_id = create_new_document(
        action_name,
        user,
        hostname,
        device_ip_address,
        device_user,
        device_password,
        exceution_start_time,
        ansible_command_string,
        input_yml,
    )

    if debugging_mode:
        print("action: ", action)
        print("ansible_command: ", ansible_command)
        print("ansible_command_string: ", ansible_command_string)
        print("mongo_id", mongo_id)

    # Create hosts file
    create_hosts_file(hostname, device_ip_address)

    # Remove Old License If Exists
    remove_license()

    # Create License Key
    create_license()

    # OutPut, Log Files
    output_file_name = f"{hostname}.aarohi.device.{log_file_extenstion}.txt"
    output_file_path = os.path.join(output_folder, output_file_name)

    # Rename Old OutPut
    if os.path.exists(output_file_path):
        new_file_name = (
            f"{hostname}.aarohi.device.{log_file_extenstion}.{int(time.time())}.txt"
        )
        new_file_path = os.path.join(output_folder, new_file_name)
        os.rename(output_file_path, new_file_path)

    # Command as a subprocess
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

        if process.returncode == 0 and action != "deploy_configuration":
            with open(output_file_path, "r") as device_content:
                output = device_content.read()

        # Remove License & Update Database
        remove_license()
        exceution_end_time = datetime.now()
        exceution_elapsed_time_seconds = exceution_end_time - exceution_start_time
        exit_code = process.returncode
        update_document(
            mongo_id,
            exceution_end_time,
            exceution_elapsed_time_seconds,
            output,
            log,
            exit_code,
        )

    except KeyboardInterrupt:
        process.terminate()
        process.wait()
        log += process_terminated

        # Remove License & Update Database
        remove_license()
        exceution_end_time = datetime.now()
        exceution_elapsed_time_seconds = exceution_end_time - exceution_start_time
        exit_code = process.returncode
        update_document(
            mongo_id,
            exceution_end_time,
            exceution_elapsed_time_seconds,
            output,
            log,
            exit_code,
        )

    except Exception as e:
        log += str(e)

        # Remove License & Update Database
        remove_license()
        exceution_end_time = datetime.now()
        exceution_elapsed_time_seconds = exceution_end_time - exceution_start_time
        exit_code = process.returncode
        update_document(
            mongo_id,
            exceution_end_time,
            exceution_elapsed_time_seconds,
            output,
            log,
            exit_code,
        )
    return process.returncode


# endregion


def create_yaml_folder():
    if not os.path.exists("../" + yaml_folder):
        os.makedirs("../" + yaml_folder)


def copyright_header(output_file, content_type):
    current_datetime = datetime.now()
    day = current_datetime.day
    suffix = (
        "th" if 11 <= day <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
    )
    formatted_datetime = current_datetime.strftime(f"%d{suffix} %b %Y %I:%M:%S %p")

    company = "Aarohi IT Solutions Private Limited"
    copyright_text = "All rights reserved by Aarohi IT Solutions Private Limited."
    legal_disclaimer = "This file contains confidential and proprietary information. Unauthorized use, reproduction, or distribution may result in legal penalties"
    software = "Created using Aarohi Property Software"
    yaml_content = {
        "Company": company,
        "Copyright": copyright_text,
        "Legal Disclaimer": legal_disclaimer,
        "Software": software,
    }
    with open(output_file, "w") as file:
        file.write(f"# Auto-generated {content_type} File" + newline)
        file.write("# Created by Aarohi Property Software" + newline)
        file.write("# Created Date and Time: " + formatted_datetime + newline)
        file.write("# Version: " + aarohi_version + newline + newline)
        yaml.dump(yaml_content, file, default_flow_style=False)


def management_ip(input_file, output_file):
    management_ip = ""
    management_ip_start = False
    with open(input_file, "r") as file:
        for line in file:
            if line.startswith("interface Management 0"):
                management_ip_start = True
            if management_ip_start == True:
                if line.strip().startswith("ip address"):
                    management_ip += line.strip().split()[2].split("/")[0]
                    break
    if management_ip_start == True:
        with open(output_file, "a") as file:
            file.write(newline + "# Management IP" + newline)
            yaml_content = {"management_ip": management_ip}
            yaml.dump(yaml_content, file, default_flow_style=False)
            print("Management IP Completed", flush=True)
            return True
    else:
        return False


def host_name(output_file):
    yaml_content = {"host_name": output_file.rsplit("/", 1)[-1].split(".")[0]}
    with open(output_file, "a") as file:
        file.write(newline + "# Host Name" + newline)
        yaml.dump(yaml_content, file, default_flow_style=False)
        print("Host Name Completed", flush=True)


def anycast_mac_address(input_file, output_file):
    anycast_mac_address = None
    with open(input_file, "r") as file:
        for line in file:
            if line.startswith("ip anycast-mac-address"):
                anycast_mac_address = line.strip().split()[-1]
                break
    if anycast_mac_address != None:
        with open(output_file, "a") as file:
            file.write(newline + "# Any Cast Mac Address" + newline)
            yaml_content = {"anycast_mac_address": anycast_mac_address}
            yaml.dump(yaml_content, file, default_flow_style=False)
            print("Any Cast Mac Address Completed", flush=True)


def time_zone(input_file, output_file):
    clock_timezone = None
    with open(input_file, "r") as file:
        for line in file:
            if line.startswith("clock timezone"):
                clock_timezone = line.strip().split()[-1]
                break

    if clock_timezone is not None:
        yaml_content = {"sonic_timezone": clock_timezone}
        with open(output_file, "a") as file:
            file.write(newline + "# Clock Timezone" + newline)
            yaml.dump(yaml_content, file, default_flow_style=False)
            print("Clock Timezone Completed", flush=True)


def vrf_management(input_file, output_file):
    ip_vrf_mgmt = None
    with open(input_file, "r") as file:
        for line in file:
            if line.startswith("ip vrf mgmt"):
                ip_vrf_mgmt = "mgmt"
                break

    if ip_vrf_mgmt is not None:
        yaml_content = {"sonic_vrf_name": ip_vrf_mgmt}
        with open(output_file, "a") as file:
            file.write(newline + "# VRF Management" + newline)
            yaml.dump(yaml_content, file, default_flow_style=False)
            print("VRF Management Completed", flush=True)


def logging_server(input_file, output_file):
    logging_server = None
    with open(input_file, "r") as file:
        for line in file:
            if line.startswith("logging server"):
                logging_server = line.strip()
                pattern = r"logging server (\S+) remote-port (\S+) source-interface (\S+) (\S+)"
                match = re.search(pattern, logging_server)
                if match:
                    ip_address = match.group(1)
                    remote_port = int(match.group(2))
                    source_interface = match.group(3) + " " + match.group(4)
                break
    if logging_server != None:
        yaml_content = {
            "sonic_logging_server": [
                {
                    "logging_server": ip_address,
                    "remote_port": remote_port,
                    "source_interface": source_interface,
                }
            ]
        }

        with open(output_file, "a") as file:
            file.write(newline + "# Logging Server" + newline)
            yaml.dump(yaml_content, file, Dumper=IndentDumper, default_flow_style=False)
            print("Logging Server Completed", flush=True)


def loopback_adapter(input_file, output_file):
    print(input_file, output_file)


class IndentDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super().increase_indent(flow, False)


if __name__ == "__main__":
    command_array = [
        "backuptoyml",
        "exceltoyml",
        "deviceinfo",
        "devicebackup",
        "deploy",
        "reset",
    ]
    if len(sys.argv) < 2:
        print("Invalid command!")
        sys.exit(1000)
    command = sys.argv[1]

    if command not in command_array:
        print("Invalid command! Argument")
        sys.exit(1001)

    if command == "deviceinfo" or command == "devicebackup" or command == "deploy":
        # Command Line Example's:
        # python3 aarohi.py deviceinfo   aarohi hareesh2 192.168.29.88 admin YourPaSsWoRd
        # python3 aarohi.py devicebackup aarohi hareesh2 192.168.29.88 admin YourPaSsWoRd
        # python3 aarohi.py deploy       aarohi hareesh2 192.168.29.88 admin YourPaSsWoRd HYD-NAR-F1-SR035-LEAF-BBPS-S5248F-SW1.yml

        user = sys.argv[2]
        hostname = sys.argv[3]
        device_ip_address = sys.argv[4]
        device_user = sys.argv[5]
        device_password = sys.argv[6]
        file_input = sys.argv[7] if len(sys.argv) > 7 else None
        action = (
            "deploy_configuration"
            if command == "deploy"
            else "get_device_information"
            if command == "deviceinfo"
            else "get_device_backup"
            if command == "devicebackup"
            else ""
        )

        exit_code = device_safe_commands(
            action,
            user,
            hostname,
            device_ip_address,
            device_user,
            device_password,
            file_input,
        )
        sys.exit(exit_code)

    elif command == "backuptoyml":
        create_yaml_folder()
        input_file = sys.argv[2]
        hostname = sys.argv[3] + ".yml"
        output_file = "../" + yaml_folder + "/" + hostname
        copyright_header(output_file, "YAML")
        management_ip(input_file, output_file)  # Pending assert
        host_name(output_file)
        anycast_mac_address(input_file, output_file)
        time_zone(input_file, output_file)
        vrf_management(input_file, output_file)
        logging_server(input_file, output_file)  # Pending multiple logging servers
