import subprocess

command = "echo 'Hello, world!'"
result = subprocess.run(command, shell=True, stdout=subprocess.PIPE)
print(result.stdout)