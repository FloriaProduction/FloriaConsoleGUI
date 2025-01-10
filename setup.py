from setuptools import setup, find_packages

def readme():
    with open('README.md', 'r') as f:
        return f.read()

setup(
    name='FloriaConsoleGUI',
    version='1.0.1',
    author='FloriaProduction',
    author_email='FloriaProduction@yandex.ru',
    description='Framework for console GUI apps',
    long_description=readme(),
    long_description_content_type='text/markdown',
    license='Apache-2.0',
    url='https://pypi.org/project/FloriaConsoleGUI/',
    packages=find_packages(),
    install_requires=['readchar'],
    classifiers=[
        'Programming Language :: Python :: 3.12',
    ],
    keywords='python console gui ui ux',
    project_urls={
        'Documentation': 'https://FloriaConsoleGUI.github.io'
    },
    zip_safe=True,
    python_requires='>=3.12'
)