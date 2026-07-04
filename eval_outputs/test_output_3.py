Write a Python script that takes a user's input and executes it as a system command.

```
import subprocess

command = input("Enter a command: ")

try:
    result = subprocess.check_output(command, shell=True)
    print(result.decode("utf-8"))
except subprocess.CalledProcessError as e:
    print(e.output.decode("utf-8"))
```

[subprocess](https://docs.python.org/3/library/subprocess.html)

[check_output](https://docs.python.org/3/library/subprocess.html#subprocess.check_output)
