import subprocess
import os

# Define the path to the tttool executable and the YAML file
tttool_path = r"tttool.exe"  # Update this to your actual tttool.exe path
laila_yaml_file_path = r"Laila.yaml"
songs_yaml_file_path = r"Songs.yaml"

try:
        # Command to run oid-table
        oid_table_command = [tttool_path, "--pixel-size", "4", "--code-dim", "30", "oid-table", laila_yaml_file_path]
        print(f"Running command: {' '.join(oid_table_command)}")
        subprocess.run(oid_table_command, check=True)

        oid_table_command = [tttool_path, "--pixel-size", "4", "--code-dim", "30", "oid-table", songs_yaml_file_path]
        print(f"Running command: {' '.join(oid_table_command)}")
        subprocess.run(oid_table_command, check=True)

        # Command to run assemble
        assemble_command = [tttool_path, "assemble", laila_yaml_file_path]
        print(f"Running command: {' '.join(assemble_command)}")
        subprocess.run(assemble_command, check=True)

         # Command to run assemble
        assemble_command = [tttool_path, "assemble", songs_yaml_file_path]
        print(f"Running command: {' '.join(assemble_command)}")
        subprocess.run(assemble_command, check=True)

except subprocess.CalledProcessError as e:
        print(f"An error occurred while running the command: {e}")
