from setuptools import setup, find_packages

setup(
    name='axtoolkit',
    version='0.1.2',
    description='A toolkit for analyzing and processing data',
    author='AlbertXin',
    author_email='<albert_xin@qq.com>',
    url='',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',],
    install_requires=[
        'numpy',
        'matplotlib',
        'pandas',
        'psutil'
        ],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'svg2pngpdf = axtoolkit.utlscript.svg2pngpdf:main',
            'sge_submit = axtoolkit.utlscript.terminal_command_manager:pipeline_qsub_commands'
            ],
            }
    

)