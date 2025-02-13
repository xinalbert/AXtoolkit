from pathlib import Path
import subprocess
import psutil

class command_Error(Exception):
    pass

def get_free_cpus(threshold: int = 30) -> int:
        """
        This function returns the number of free CPUs on the system.
        Args:
            threshold: The threshold for CPU usage percentage, default is 30%.
        Returns:
            The number of free CPUs.
        """
        cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
        free_cpus = sum(1 for p in cpu_percent if p < threshold)
        return free_cpus


def run_cmd(cmd_str,checknum = [0]):
    """
    run a command in shell
    """
    try:
        process = subprocess.Popen(cmd_str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        if process.returncode in checknum:
            pass
        else:
            raise command_Error(f"Execution failed for command: command return code: {process.returncode}\nError: {err.decode()}")
    except Exception as e:
        raise command_Error(f"Execution failed for command: {cmd_str}\nError: {e}")


def cmd_check(work_dir, cmd_file_name, cmd_list, checknum = [0], parafly = None):
    """
    check if command has been executed before, if not, write\
     command to file and execute it.
    return True if command has been executed previously, \
    False if command is newly executed.

    Args:
        work_dir: working directory
        cmd_file_name: command file name
        cmd_list: list of commands to be executed
        checknum: check number of return code, default is [0]
        parafly: parallelization, default is None
    Returns:
        True if command has been executed, False if command has not been executed.
    must contain dirs: is work_dir/.cmd and work_dir/.cmd_ok
    """

    cmd_file = work_dir / ".cmd" / cmd_file_name
 
    cmd_file.parent.mkdir(parents=True, exist_ok=True, max_threads=20)
    with open(cmd_file, "w") as f:
        for cmd_str in cmd_list:
            # print(cmd_str)
            f.write(cmd_str + '\n')  # 写入命令到文件
    # 执行命令
    if parafly:
        num_threads = int(0.6 * get_free_cpus())
        if max_threads is not None:
            num_threads = min(num_threads, max_threads)
        if num_threads <= 0:
            num_threads = 1  # at least use one thread
        cmd_str = f"{parafly} -c {cmd_file} -CPU {num_threads} -failed_cmds {work_dir}/{cmd_file_name}_failed_cmds.sh"
        run_cmd(cmd_str, checknum = checknum)
    else:
        for cmd_str in cmd_list:
            # print(cmd_str)
            run_cmd(cmd_str, checknum = checknum)
    # 标记命令已执行

    print(f"Commands executed and file created : {cmd_file_name}")
    
    return True