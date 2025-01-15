from pathlib import Path
import subprocess


class command_Error(Exception):
    pass

def run_cmd(cmd_str,checknum = 0):
    """
    run a command in shell
    """
    try:
        process = subprocess.Popen(cmd_str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        if process.returncode== checknum:
            pass
        else:
            raise command_Error(f"Execution failed for command: {cmd_str}\nError: {err.decode()}")
    except Exception as e:
        raise command_Error(f"Execution failed for command: {cmd_str}\nError: {e}")


def cmd_check(work_dir, cmd_file_name, cmd_list, checknum = 0):
    """
    check if command has been executed before, if not, write\
     command to file and execute it.
    return True if command has been executed previously, \
    False if command is newly executed.

    Args:
        work_dir: working directory
        cmd_file_name: command file name
        cmd_list: list of commands to be executed
        checknum: check number of return code
    Returns:
        True if command has been executed, False if command has not been executed.
    must contain dirs: is work_dir/.cmd and work_dir/.cmd_ok
    """

    cmd_file = work_dir / ".cmd" / cmd_file_name
 
    cmd_file.parent.mkdir(parents=True, exist_ok=True)
    with open(cmd_file, "w") as f:
        for cmd_str in cmd_list:
            # print(cmd_str)
            f.write(cmd_str + '\n')  # 写入命令到文件
    # 执行命令
    for cmd_str in cmd_list:
        # print(cmd_str)
        run_cmd(cmd_str, checknum = checknum)
    # 标记命令已执行

    print(f"Commands executed and file created : {cmd_file_name}")
    
    return True