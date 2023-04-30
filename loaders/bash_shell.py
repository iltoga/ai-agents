import subprocess
import traceback

class BashShell:
    def __init__(self):
        pass
        
    def run(self, command):
        try:
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
            if result.returncode == 0:
                return (result.returncode, result.stdout, None)
            else:
                return (result.returncode, None, result.stderr)
        except Exception as e:
            return (None, None, traceback.format_exc())
        
if __name__ == "__main__":
    cmd = BashShell()
    invalid_command = "echoz 'Hello, World!'"
    return_code, output, error = cmd.run(invalid_command)
    assert return_code != 0
    assert output is None
    assert error == '/bin/sh: echoz: command not found\n'        
    valid_command = "echo 'Hello, World!'"
    return_code, output, error = cmd.run(valid_command)
    assert return_code == 0
    assert output == "Hello, World!\n"
