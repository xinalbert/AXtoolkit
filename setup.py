""" setup.py """
from setuptools import setup, find_packages

def parse_requirements(file):
    """
    This function parses requirements from a file and returns a list of strings.
    """
    with open(file, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name='axtoolkit',
    version='0.1.31',
    description='A toolkit for analyzing and processing data',
    author='AlbertXin',
    author_email='<albert_xin@qq.com>',
    url='',
    packages=find_packages(),
    package_data={
        'my_package': ['utlscript/*.py'],  # 包含 scripts 目录下的所有 Python 脚本
    },
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',],
    # install_requires=parse_requirements('requirements.txt'),
    python_requires='>=3.6',
    entry_points={
    'console_scripts': [
        'svg2pngpdf = axtoolkit.utlscript.svg2pngpdf:main',  # 假设有 main 函数
        'sge_submit = axtoolkit.utlscript.terminal_command_manager_tools:pipeline_qsub_commands'  # 指定正确的可调用函数
    ]
}
)
# End of setup.pypyth