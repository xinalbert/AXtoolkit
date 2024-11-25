import os

class ShellTools:
    def __init__(self):
        pass

    @staticmethod
    def para_fly_run(sh_file_path, threads_num, para_fly_path: str = "/data/soft/soft/Miniforge/bin/ParaFly"):
        """This function is used to run a shell script using ParaFly.
        Args:
            sh_file_path: The path of the shell script to be run.
            threads_num: The number of threads to be used.
            para_fly_path: The path of ParaFly. The default value is "/data/soft/soft/Miniforge/bin/ParaFly".
        Returns:
            None.
        Raises:
            None.
        Example:
            para_fly_run("test.sh", 4)
        """
        cmd = f"{para_fly_path} -c {sh_file_path} -CPU {threads_num}"
        os.system(cmd)
