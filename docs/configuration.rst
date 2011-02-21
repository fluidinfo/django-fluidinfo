=============
Configuration
=============

In order to use django-fluidinfo you need indicate your Fluidinfo instance and
credentials in the settings.py file.

To use the main instance of Fluidinfo you would add something like this::

    from fom.session import Fluid

    fdb = Fluid() # defaults to http://fluiddb.fluidinfo.com/
    fdb.login('username', 'password')
    fdb.bind()

For the purposes of testing you might want to use the sandbox version of
Fluidinfo like this::


    from fom.session import Fluid

    fdb = Fluid('http://sandbox.fluidinfo.com') # sandbox's URL
    fdb.login('username', 'password')
    fdb.bind()

Each time you start your application a Fluidinfo session is created with the
appropriate credentials. It is these credentials that are also used by the
management command ``syncfluidinfo``.
