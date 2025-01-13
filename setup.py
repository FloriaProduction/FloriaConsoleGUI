from setuptools import setup, find_packages

def readme():
    with open('README.md', 'r', encoding='utf-8') as f:
        return f.read()

setup(
    name='FloriaConsoleGUI',
    version='1.0.6',
    author='FloriaProduction',
    author_email='FloriaProduction@yandex.ru',
    description='Framework for console GUI apps',
    long_description=readme(),
    long_description_content_type='text/markdown',
    license='Apache-2.0',
    project_urls={
        "Documentation": 'https://FloriaConsoleGUI.github.io',
        "Source": 'https://github.com/FloriaProduction/FloriaConsoleGUI',
    },
    packages=find_packages(),
    install_requires=['readchar'],
    classifiers=[
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: Apache Software License',
        'Environment :: Console',
        "Intended Audience :: Developers",
        "Typing :: Typed"
    ],
    keywords='python console gui ui ux',
    zip_safe=True,
    python_requires='>=3.12'
)