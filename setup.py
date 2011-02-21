from distutils.core import setup

setup(
    name='django-fluidinfo',
    author='Nicholas Tollervey',
    author_email='dev@fluidinfo.com',
    version='0.2.0',
    packages=['django_fluidinfo'],
    url='http://fluidinfo.com/',
    license='LICENSE.txt',
    description='Provides a familiar interface for using Fluidinfo within Django projects',
    long_description=open('README.rst').read(),
    classifiers=['Development Status :: 3 - Alpha Development Status',
                 'Environment :: Web Environment', 
                 'Framework :: Django',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: BSD License',
                 'Operating System :: OS Independent', 
                 'Programming Language :: Python',
                 'Topic :: Utilities']
)
