import os
import human_eval

# Find where the human_eval library is installed in your virtual environment
exec_file = os.path.join(os.path.dirname(human_eval.__file__), "execution.py")

with open(exec_file, "r", encoding="utf-8") as f:
    code = f.read()

# Comment out the Unix-only time limit commands and replace them with 'pass'
if "pass # signal.setitimer" not in code:
    code = code.replace("signal.setitimer", "pass # signal.setitimer")
    code = code.replace("signal.signal(signal.SIGALRM", "pass # signal.signal(signal.SIGALRM")
    
    with open(exec_file, "w", encoding="utf-8") as f:
        f.write(code)
    print("\n✅ OpenAI HumanEval library successfully patched for Windows!")
else:
    print("\n✅ Patch was already applied!")