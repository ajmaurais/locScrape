
from setuptools import setup, find_packages

setup(name='protein_scrape',
      version='1.0',
      description='Given a .tsv file with a column containing Uniprot protein IDs, scrape annotations for subcellular location from Uniprot.org',
      author='Aaron Maurais',
      url='https://github.com/ajmaurais/protein_scrape',
      classifiers=['Development Status :: 4 - Beta',
        'Intended Audience :: SCIENCE/RESEARCH',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        ],
      packages=find_packages(),
      package_dir={'protein_scrape':'protein_scrape'},
      python_requires='>=3.6.*',
      install_requires=['tqdm>=4.31.1', 'lxml>=4.9.1', 'requests>=2.21.0'],
      entry_points={'console_scripts': ['scrape_locs=protein_scrape:scrape_locs']},
)

