import os
import datetime
import sys
import shutil


class FileTools:
    def __init__(self):
        pass
    def file2list(file_path):
        """Reads a file and returns a list of its lines without newline characters.
        Args:
            file_path (str): The path of the file to be read.
        Returns:
            list: A list containing the lines of the file, stripped of leading and trailing whitespace.
        Raises:
            IOError: If the file cannot be opened.
        Examples:
            >>> file2list('/path/to/file.txt')
            ['line1', 'line2', 'line3']
        """
        with open(file_path, 'r') as file:
            return [line.strip() for line in file]
        
    def get_files_with_pattern(directory, pattern, recursive=False):
        """This function returns a list of all files in a directory that match the given pattern.
        Args:
            directory (str): The directory path.
            pattern (str): The file pattern to match (e.g., '*.txt').
            recursive (bool): Whether to search recursively in subdirectories. Default is False.
        Returns:
            list: A list of matching file paths.
        Raises:
            ValueError: If the directory does not exist or is not a directory.
        Examples:
            >>> get_files_with_pattern('/path/to/directory', '*.txt')
            ['/path/to/directory/file1.txt', '/path/to/directory/file2.txt']
        """
        import glob
        if not os.path.isdir(directory):
            raise ValueError(f"The directory '{directory}' does not exist or is not a directory.")
        
        search_path = os.path.join(directory, '**', pattern) if recursive else os.path.join(directory, pattern)
        return glob.glob(search_path, recursive=recursive)


    def get_column(file_path, column_num=1, delimiter='\t'):
        """This function reads a file and yields values from the specified column.
        Args:
            file_path (str): The path of the file to be read.
            column_num (int): The number of the column to be returned (1-based index).
            delimiter (str): The delimiter used to split the file.
        Yields:
            str: Values from the specified column.
        Raises:
            ValueError: If column_num is less than 1.
            IndexError: If a line does not have enough columns.
            IOError: If the file cannot be opened.
        Examples:
            >>> for value in get_column('/path/to/file.txt', 2):
            >>>     print(value)
    
        """
        if column_num < 1:
            raise ValueError("column_num must be a positive integer starting from 1.")
        
        with open(file_path, 'r') as file:
            for line in file:
                parts = line.strip().split(delimiter)
                if len(parts) < column_num:
                    raise IndexError(f"Line does not have enough columns: {line.strip()}")
                yield parts[column_num - 1]
        

    # def replace_extension(file_path, new_extension):
    #     """This function replace the file extension to a new extension
    #     Args:
    #         file_path (str): The path of the file to be replaced.
    #         new_extension (str): The new extension to be added.
    #     Returns:
    #         str: The new file path with the new extension.
    #     Examples:
    #         >>> replace_extension('/path/to/file.txt', 'csv')
    #         '/path/to/file.csv'
    #     """
    #  
    #     return f"{os.path.splitext(file_path)[0]}.{new_extension}"

    def mkdir(file_path):
        """This function creates a directory if it does not exist.
        Args:
            file_path (str): The path of the directory to be created.
        Raises:
            OSError: If the directory cannot be created.
        Examples:
            >>> mkdir('/path/to/directory')
        """
        if not os.path.exists(file_path):
            os.makedirs(file_path, exist_ok=True)


    def pwd():
        """This function returns the current working directory.
        Returns:
            str: The current working directory.
        Examples:
            >>> print(pwd())
            '/path/to/directory'
        """
        return os.getcwd()  

    def ls(directory):
        """This function returns a list of all files and directories in a directory.
        Args:
            directory (str): The directory path.
        Returns:
            list: A list of all files and directories in the directory.
        Raises:
            ValueError: If the directory does not exist or is not a directory.
        Examples:
            >>> ls('/path/to/directory')
            ['file1.txt', 'file2.txt', 'directory1', 'directory2']
        """
        if not os.path.isdir(directory):
            raise ValueError(f"The directory '{directory}' does not exist or is not a directory.")
        return os.listdir(directory)

    def cp(src, dst):
        """This function copies a file or directory to a new location.
        Args:
            src (str): The path of the file or directory to be copied. 
            dst (str): The path of the new location.    
        Raises: 
            OSError: If the file or directory cannot be copied. 
        Examples:    
            >>> cp('/path/to/file.txt', '/path/to/new_directory')    
        """
        if os.path.isdir(src):
            shutil.copytree(src, dst)
        else:
            shutil.copy(src, dst) 

    def mv(src, dst):
        """This function moves a file or directory to a new location.
        Args:
            src (str): The path of the file or directory to be moved. 
            dst (str): The path of the new location.    
        Raises: 
            OSError: If the file or directory cannot be moved. 
        Examples:    
            >>> mv('/path/to/file.txt', '/path/to/new_directory')    
        """
        try:
            shutil.move(src, dst)
        except shutil.Error as e:
            print(f"Error: {e.args[0]}")
        
    def rm(file_path):
        """This function removes a file or directory.
        Args:
            file_path (str): The path of the file or directory to be removed.
        Raises:
            OSError: If the file or directory cannot be removed.
        Examples:
            >>> rm('/path/to/file.txt')
        """
        try:
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
            else:
                os.remove(file_path)
        except OSError as e:
            print(f"Error: {e.args[0]}")

    def replace_extension(file_path, new_extension = 'txt', base_name=False):
        """
        This function replace the file extension to a new extension
        
        ParametersL
        file_path: file path which you want to replace teh extension
        new_extension: new file extension, default is 'txt', if you want to remove the extension, set it to None.
        base_name: if True, only replace the base name of the file, not the extension. Default is False.

        Return:
        the replaced file path
        """
        if new_extension == None:
            new_extension = ""
            return os.path.basename(file_path)

        if base_name:
            return f"{os.path.splitext(file_path)[0]}"
        else:
            return f"{os.path.splitext(file_path)[0]}.{new_extension}"

    def get_dir_name(file_path):
        """
        This function returns the directory name of a file path.
        
        Args:
            - file_path: file path which you want to get the directory name.
        Return:
            - the directory name of the file path.
        Examples:
            >>> get_dir_name('/path/to/file.txt')
            '/path/to'
        """
        return os.path.dirname(file_path)

    def def_new_save_path(file_path, file_name=None):
        """
        This function returns the new save path of a file path with a new extension.

        Args:
            - file_path: file path which you want to replace the extension.
            - file_name: new file name, if None, the new file name will be 'new__file_YYYYMMDD_HHMMSS.txt'. Default is None.
        Return:
            - the new save path of the file path with a new extension.
        Examples:
            >>> def_new_save_path('/path/to/file.txt', 'new_file.csv')
            '/path/to/new_file.csv'
        """

        time_str = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        if file_path == None:
            pre_path = os.getcwd()
            print(f"Current working directory: {pre_path}")
        else:
            pre_path = FileTools.get_dir_name(file_path)
        
        if file_name == None:
            file_path = os.join(pre_path, f'new__file_{time_str}.txt')
            print(f"New file path: {file_path}")
            return file_path
        else:
            file_path = os.join(pre_path, f'{file_name}')
            return file_path

