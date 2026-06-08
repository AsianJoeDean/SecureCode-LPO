import ast

# 1. This is the "dummy" code we want the AST to scan
dummy_bad_code = """
def run_user_code(user_input):
    print("Running your command...")
    
    # This is a massive security flaw
    result = eval(user_input) 
    
    return result
"""

# 2. We build a custom scanner that looks at every piece of the code
class SecurityScanner(ast.NodeVisitor):
    
    # This built-in method automatically triggers every time the scanner sees a function call
    def visit_Call(self, node):
        
        # Check if the function being called has a standard name
        if isinstance(node.func, ast.Name):
            
            # If the function is exactly the word 'eval', flag it!
            if node.func.id == 'eval':
                print(f"🚨 ALERT: Found insecure '{node.func.id}()' function on line {node.lineno}!")
        
        # Tell the scanner to keep moving through the rest of the file
        self.generic_visit(node)


def scan_code():
    print("Scanning code for vulnerabilities...")
    
    # 3. Turn the plain text code into an Abstract Syntax Tree (AST)
    tree = ast.parse(dummy_bad_code)
    
    # 4. Run our custom scanner over the tree
    scanner = SecurityScanner()
    scanner.visit(tree)
    
    print("Scan complete.")

if __name__ == "__main__":
    scan_code()