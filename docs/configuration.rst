=============
Configuration
=============

In order to use django-fluiddb you need indicate your FluidDB instance and 
credentials in the settings.py file. 

To use the main instance of FluidDB you would add something like this::

    from fom.session import Fluid

    fdb = Fluid() # defaults to http://fluiddb.fluidinfo.com/
    fdb.login('username', 'password')
    fdb.bind()

For the purposes of testing you might want to use the sandbox version of
FluidDB like this::


    from fom.session import Fluid

    fdb = Fluid('http://sandbox.fluidinfo.com') # sandbox's URL 
    fdb.login('username', 'password')
    fdb.bind()

Each time you start your application a FluidDB session is created with the
appropriate credentials. It is these credentials that are also used by the
management command ``syncfluiddb``.
