import ast
import json
import os

class SecurityScanner(ast.NodeVisitor):
    def __init__(self):
        self.found_flaws = 0

    def visit_Call(self, node):
        # 1. Look for dangerous base functions like 'eval()'
        if isinstance(node.func, ast.Name):
            if node.func.id == 'eval':
                print(f"    🚨 ALERT: Found insecure '{node.func.id}()' on line {node.lineno}!")
                self.found_flaws += 1
                
        # 2. Look for dangerous module calls like 'os.system()' or 'cursor.execute()'
        elif isinstance(node.func, ast.Attribute):
            dangerous_methods = ['system', 'call', 'execute']
            if node.func.attr in dangerous_methods:
                print(f"    🚨 ALERT: Found potentially risky '{node.func.attr}()' execution on line {node.lineno}!")
                self.found_flaws += 1
                
        self.generic_visit(node)

def scan_dataset():
    file_path = "data/full_dataset.json"
    
    if not os.path.exists(file_path):
        print("Dataset not found! Run generate_data.py first.")
        return

    print("Opening the dataset and scanning for vulnerabilities...\n")
    
    with open(file_path, "r") as file:
        dataset = json.load(file)
        
    for index, entry in enumerate(dataset):
        print(f"Scanning Example {index + 1} ({entry['vulnerability_type']})...")
        
        bad_code = entry.get("bad_code", "")
        
        try:
            tree = ast.parse(bad_code)
            scanner = SecurityScanner()
            scanner.visit(tree)
            
            if scanner.found_flaws == 0:
                print("    ✅ No flagged functions found in this AST tree.")
                
        except SyntaxError:
            print("    ❌ AI generated invalid Python syntax. Skipping.")
            
        print("-" * 40)

if __name__ == "__main__":
    scan_dataset()