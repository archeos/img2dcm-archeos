#!/usr/bin/env python

from distutils.core import setup

setup(name='img2dcm',
	version='0.1.0',
	description='Convert bmp, tif, png, jpg, vti to dcm',
	author='Thiago Franco de Moraes',
	author_email='invesalius@cti.gov.br',
	url='https://bitbucket.org/tfmoraes/img2dcm',
	maintainer="Romain Janvier",
	maintainer_email="romain.janvier@hotmail.fr",
	py_modules=['ivDicom'],
	scripts=['img2dcm'],
	licence='GPL2',
	requires=['vtk (>=0.4.67)', 'gdcm (>=2.2.0)', 'vtkgdcm (>=2.2.0)'],
     )
