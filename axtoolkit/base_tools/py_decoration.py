# 定义一个字典用于存储函数返回值
# cache_dic = {}
import functools
import datetime
import sys
import os
import file_tools
# sys.path.append('/share/nas2/zhushixin/python_script/python_bin')



class PyDecorator:
    def __init__(self):
        pass

    @staticmethod
    def cache_result(func):
        """decorator to store function return value in a dictionary, you must define 
            a dictionary named "cache_dic" before using this decorator. The last argument of the function 
            will be used as the key to store the result. If the key already exists in the dictionary, the value 
            will not be updated.
        Args:
            func: the function to be decorated
        Returns:
            wrapper: the decorated function
        Example:
            @cache_result
            def add(a, b):
                return a + b
            add(1, 2)  # 3
            add(3, 4)  # 7
            add(1, 2)  # 3
            add(2, 3)  # 5
            print(cache_dic)  # {1: 3, 2: 5, 3: 7, 4: 7}
        """
        def wrapper(*args, **kwargs):
            # 调用原始函数并获取结果
            result = func(*args, **kwargs)
            
            # 获取最后一个参数
            if args:
                key = args[-1]  # 从位置参数中获取最后一个参数
            elif kwargs:
                key = list(kwargs.values())[-1]  # 从关键字参数中获取最后一个参数
            else:
                raise ValueError("函数必须有至少一个参数")
            
            # 检查字典中是否已有该键，如果没有则添加
            if key not in cache_dic: # type: ignore
                cache_dic[key] = result # type: ignore
            else:
                print(f"键 {key} 已存在，未更新字典中的值。")
            
            return result
        return wrapper
    @staticmethod
    def timeit(func):
        """ Decorator to measure the runtime of a function.
        Args:
            func: the function to be decorated
        Returns:
            wrapper: the decorated function
        Example:
            @timeit
            def my_func(a, b):
                time.sleep(1)
                return a + b
            my_func(1, 2)  # 输出运行时间
            # Runtime of my_func: 0:00:01.000000
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = datetime.datetime.now()
            result = func(*args, **kwargs)
            end_time = datetime.datetime.now()
            file_get = file_tools.FileTools.replace_extension(sys.argv[0], new_extension = None)
            print(f"\nRuntime of {file_get}: {end_time - start_time}\n")
            return result
        return wrapper

    @staticmethod
    def plot_save(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            for exten in ['.png', '.pdf', '.svg']:
                new_args = []
                for arg in args:
                    # print(arg)
                    if isinstance(arg, str) and os.path.exists(arg):
                        path = arg.split('.')[0]
                        path = path + exten
                        print(path)
                        new_args.append(path)
                    else:
                        new_args.append(arg)
                        # print(new_args)
                # print(new_args)
                new_args = tuple(new_args)
                # print(new_args)
                func(*new_args, **kwargs)
            return None

        return inner