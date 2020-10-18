# DOFIS (Districts of Innovation Statute)

The code in this package analyzes the impact of the Texas Districts of Innovation statute. 

data_from_plans scrapes district websites for DOI plans and extracts laws. 

data_from_tea cleans district and school level data from the Texas education agency.

merge_and_clean combines the scraped data with TEA data.

analysis estimates the impact of the law.


To run appropriately, there needs to be a setup.py file that is sibling to this folder and contains the following:

    from setuptools import setup
    from setuptools import find_packages
    
    setup(name='dofis', version='1.0', packages=find_packages())

