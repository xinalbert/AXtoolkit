import os
import subprocess

class Pipeliner:
    def __init__(self, verbose=False):
        self.commands = []  # store the commands and flags
        self.verbose = verbose

    def add_command(self, command, flag):
        """
        Add the command to commands list        
        """
        self.set_permissions(command)
        self.commands.append((command, flag))

    def set_permissions(self, file):
        """
        Set permissions for file to 777
        """
        if os.path.isfile(file):
            os.chmod(file, 0o777)
            if self.verbose:
                print(f"Permissions set for {file}")

    def run(self):
        """
        Run all commands in the commands list
        """
        for cmd, flag in self.commands:
            if os.path.exists(flag):
                if self.verbose:
                    print(f"Skipping: {cmd} (flag: {flag} already exists)")
                continue
            
            if self.verbose:
                print(f"Running: {cmd}")
            
            try:
                # 使用 /bin/sh 运行命令
                subprocess.run(cmd, shell=True, executable='/bin/sh', check=True)
                with open(flag, 'w') as f:
                    f.write("Command completed successfully.")
                if self.verbose:
                    print(f"Flag file created: {flag}")
            except subprocess.CalledProcessError as e:
                print(f"Error: Command failed with error: {e}")
                break

def execute_pipeline(commands, flag, verbose=False):
    """
    Args:
        commands: list of commands to be executed
        flag: flag file to be created after command execution
        verbose: whether to print verbose messages
    Example:
        >>> execute_pipeline(["echo hello", "echo world"], "example_flag.ok", verbose=True)
        Running: echo hello
        hello
        Running: echo world
        world
        Flag file created: example_flag.ok 
    """
    pipeliner = Pipeliner(verbose=verbose)
    for command in commands:
        pipeliner.add_command(command, flag)
    pipeliner.run()

def write_commands(file_path, command_list):
    """
    Args:
        file_path: path to the file to be written
        command_list: list of commands to be written to the file
    Example:
        >>> write_commands("example_commands.sh", ["echo hello", "echo world"])
        >>> cat example_commands.sh
        echo hello
        echo world 
    """
    with open(file_path, "w") as f:
        for cmd in command_list:
            f.write(f"{cmd}\n")

# Python 版本的 pipeline_qsub_commands 函数
def pipeline_qsub_commands(commands, flag, cpu, cmds_dir, flag_dir, verbose=False):
    """
    Args:
        commands: name of the file containing the commands to be executed
        flag: name of the flag file to be created after command execution
        cpu: number of CPUs to be used for each command
        cmds_dir: directory where the commands file is located
        flag_dir: directory where the flag file will be created
        verbose: whether to print verbose messages
    Example:
        >>> pipeline_qsub_commands("example_commands.sh", "example_flag.ok", 4, "/path/to/cmds", "/path/to/flags", verbose=True)
        Running: ssh cluster qsub-sge.pl --maxproc 4 --queue general.q --resource vf=2.5G --reqsub /path/to/cmds/example_commands.sh --Check --independent
        Flag file created: /path/to/flags/example_flag.ok 
    """
    pipeliner = Pipeliner(verbose=verbose)

    # 定义 qsub 命令
    cmd = (f"ssh cluster qsub-sge.pl --maxproc {cpu} --queue general.q "
           f"--resource vf=2.5G --reqsub {os.path.join(cmds_dir, commands)} --Check --independent")

    # 添加命令和 flag 文件
    pipeliner.add_command(cmd, os.path.join(flag_dir, flag))

    # 运行命令
    pipeliner.run()


def para_fly_run(sh_file_path, threads_num):
    """This function is used to run a shell script using ParaFly.
    Args:
        sh_file_path: The path of the shell script to be run.
        threads_num: The number of threads to be used.
    Returns:
        None.
    Raises:
        None.
    Example:
        para_fly_run("test.sh", 4)
    
    """
    import os
    parafly = "/data/soft/soft/Miniforge/bin/ParaFly"
    cmd = f"{parafly} -c {sh_file_path} -CPU {threads_num}"
    os.system(cmd)
