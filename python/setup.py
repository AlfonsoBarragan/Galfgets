from distutils.core import setup
setup(
  name = 'Galfgets',        
  packages = ['Galfgets'],   
  version = '0.1.6',      
  license='GNU General Public License v3 (GPLv3)',        
  description = 'Package with several util functions to evade the wasting of time', 
  author = 'Alfonso Barragan Carmona',           
  author_email = 'alfonso.barragan@uclm.es',      
  url = 'https://github.com/AlfonsoBarragan/Galfgets/tree/main/python/Galfgets',   
  download_url = 'https://github.com/AlfonsoBarragan/Galfgets/releases/download/0.1.4/Galfgets-0.1.4.tar.gz',    
  keywords = ['UTILS', 'LAMBDAS', 'REGULAR EXPRESIONS', 'FUNCTIONS'],   
  install_requires=[            
          'joblib',
          'numpy',
          'pandas',
          'seaborn',
          'matplotlib',
          'sklearn',

      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',   
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)
