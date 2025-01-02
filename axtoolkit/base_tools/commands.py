from pathlib import Path
from .utils import run_cmd

def cmd_check(work_dir, cmd_file_name, cmd_list):
    """
    检查命令是否已执行，未执行则写入文件并执行。
    Args:
        work_dir (Path): 工作目录。
        cmd_file_name (str): 命令文件名。
        cmd_list (list): 要执行的命令列表。
    Returns:
        bool: True 表示命令已执行过，False 表示命令刚被执行。
    Raises:
        ValueError: 如果工作目录或命令文件名无效。
    """
    if not isinstance(work_dir, Path):
        raise ValueError("work_dir must be a Path object")
    if not cmd_file_name or not isinstance(cmd_file_name, str):
        raise ValueError("cmd_file_name must be a non-empty string")

    # 定义存储路径
    cmd_dir = work_dir / ".cmd"
    cmd_file = cmd_dir / cmd_file_name
    cmd_ok_dir = work_dir / ".cmd_ok"
    cmd_ran_file = cmd_ok_dir / f"{cmd_file_name}.done"

    # 如果命令已执行
    if cmd_ran_file.exists():
        print(f"Commands already executed: {cmd_file_name}")
        return True

    # 确保目录存在
    cmd_dir.mkdir(parents=True, exist_ok=True)
    cmd_ok_dir.mkdir(parents=True, exist_ok=True)

    # 写入命令到文件
    with cmd_file.open("w") as f:
        for cmd_str in cmd_list:
            f.write(cmd_str + "\n")

    # 执行命令
    for cmd_str in cmd_list:
        run_cmd(cmd_str)

    # 标记命令已执行
    cmd_ran_file.touch()
    print(f"Commands executed and file created: {cmd_file_name}")
    return False