from setuptools import setup

setup(
    name='pluma',
    version='0.1.0',
    description='A low-level interface to data collected with the pluma urban data acquisition system',
    url='https://github.com/emotional-cities/pluma-analysis',
    author='NeuroGEARS Ltd',
    author_email='contact@neurogears.org',
    license='MIT',
    packages=['pluma'],
    install_requires=['numpy'],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
    ],
)