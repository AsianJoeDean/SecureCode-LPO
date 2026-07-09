import subprocess
import sys

# WARNING: This script can be a security risk if the user input is not validated!
# Only execute commands that are safe and expected.

# Get the user's input
command = input("Enter a command: ")

# Validate the input
if command not in ["safe_command1", "safe_command2"]:
    print("Invalid command. Only safe commands are allowed.")
    sys.exit(1)

# Execute the command
result = subprocess.run(command.split(), capture_output=True)

# Print the output
print(result.stdout.decode())
```

It's important to note that this script should only execute safe and expected commands, as running arbitrary user input as a system command can be a security risk.