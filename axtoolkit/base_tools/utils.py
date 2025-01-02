import subprocess
from .exceptions import CommandError

def run_cmd(cmd_str):
    """
    在 shell 中运行命令。
    Args:
        cmd_str (str): 要执行的命令字符串。
    Raises:
        CommandError: 如果命令执行失败。
    """
    try:
        subprocess.run(cmd_str, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        raise CommandError(f"Command failed: {cmd_str}\nError: {e}")