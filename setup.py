#!/usr/bin/env python

from distutils.core import setup

setup(name='cpbpsim',
      version='1.1.5',
      description='A Persistent Memory-Aware Buffer Pool Manager Simulator for Multi-Tenant Cloud Databases.',
      author='Taras Basiuk',
      author_email='BasiukTV@gmail.com',
      url='https://github.com/BasiukTV/cpbpsim',
      packages=[
        'cpbpsim',
        'cpbpsim.data_admission_policy',
        'cpbpsim.data_eviction_policy',
        'cpbpsim.data_migration_policy',
        'cpbpsim.monitoring',
        'cpbpsim.page_access_sequence_generator',
        'cpbpsim.slas']
     )
