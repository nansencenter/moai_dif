from setuptools import setup, find_packages

setup(
    name='moai_dif',
    version='0.1',
    author='NERSC',
    description="DIF extension for MOAI",
    packages=find_packages(),
    entry_points= {
    'moai.content':[
        'dif=moai_dif.xml:XMLContent'
     ],
    'moai.format':[
         'dif=moai_dif.dif:DIF'
     ],
    },
    install_requires=[
        'pyoai==2.4.4',
        'MOAI>=2.0.0beta',
    ]
)


