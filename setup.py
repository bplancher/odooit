#!/usr/bin/python
# -*- coding: utf-8 -*-

from distutils.core import setup
setup(
  name='odooit',
  packages=['odooit'],  # this must be the same as the name above
  version='0.1',
  description='Tools to interact with an Odoo instance using XML-RPC protocol',
  author='Bruno PLANCHER',
  author_email='bruno.plancher@gmail.com',
  url='https://github.com/bplancher/odooit.git',  # use the URL to the github repo
  download_url='https://github.com/bplancher/odooit.git/0.1',  # I'll explain this in a second
  keywords=['odoo', 'xmlrpc', 'odoorpc'],  # arbitrary keywords
  classifiers=[],
)
