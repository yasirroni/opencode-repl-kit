# exec() Workflow Template

# Write your Python code here, then execute in REPL:
# pty_write(data="exec(open('temp/this_file.py').read())\n")

def my_function(data):
    """Replace with your function."""
    return [x * 2 for x in data]

class MyProcessor:
    """Replace with your class."""
    def __init__(self, data):
        self.data = data

    def process(self):
        return my_function(self.data)
