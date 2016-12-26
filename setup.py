from setuptools import setup

setup(
    name = 'habitican_curse',
    packages = ['habitican_curse'],
    version = '2.2',
    description = 'Linux Terminal Application for Habitica',
    author = 'Rohan Bavishi',
    author_email = 'rohan.bavishi95@gmail.com',
    url = 'https://github.com/rbavishi/Habitican-Curse',
    license = 'MIT',
    scripts = ['habitican-curse'],
    install_requires=[
        'python-dateutil',
        'requests',
    ],
)
