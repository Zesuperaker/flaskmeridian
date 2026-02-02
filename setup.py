from setuptools import setup, find_packages

setup(
    name='flaskmeridian',
    version='0.1.0',
    description='Fast setup and automations CLI tool for Flask',
    author='Joaquim',
    author_email='joaquimdaltonpereira@gmail.com',
    url='https://github.com/Zesuperaker/flaskmeridian',
    py_modules=['cli'],
    packages=find_packages(),
    install_requires=[
        'click==8.3.1',
        'flask==3.1.2',
    ],
    entry_points={
        'console_scripts': [
            'flaskmeridian=cli:cli',
        ],
    },
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
    ],
)