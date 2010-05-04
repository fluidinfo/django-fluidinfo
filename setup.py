from distutils.core import setup

setup(
    name='django-fluiddb',
    author='Nicholas Tollervey',
    author_email='dev@fluidinfo.com',
    version='0.1.0',
    packages=['django_fluiddb'],
    url='http://fluidinfo.com/',
    license='LICENSE.txt',
    description='Provides a familiar interface for using FluidDB within Django projects',
    long_description=open('README.txt').read(),
    classifiers=['Development Status :: 3 - Alpha Development Status',
                 'Environment :: Web Environment', 
                 'Framework :: Django',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: BSD License',
                 'Operating System :: OS Independent', 
                 'Programming Language :: Python',
                 'Topic :: Utilities']
)
