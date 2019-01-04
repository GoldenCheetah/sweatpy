from setuptools import setup, find_packages

setup(
    name = 'sweat',
    packages = find_packages(),
    version = '0.4.0',
    description = 'Workout analysis',
    author='Aart Goossens',
    author_email='aart@goossens.me',
    url='https://github.com/GoldenCheetah/sweatpy',
    install_requires=[
        'fitparse',
        'goldencheetahlib',
        'lmfit',
        'scipy',
        'pandas',
        'requests',
    ],
    tests_require=[
        'pytest',
        'vcrpy',
    ],
    setup_requires=[
        "pytest-runner",
    ],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
    ]
)
