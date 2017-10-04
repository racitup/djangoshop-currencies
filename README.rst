djangoshop-currencies
=====================

Django-SHOP integration with `django-currencies <https://github.com/panosl/django-currencies>`__

Introduction
------------

This module allows Django-SHOP implementations to integrate live
currency feeds. This will allow you to offer your shop product prices
in the user's chosen currency.

The module is currently compatible with Django v1.10.7. This
documentation assumes a working knowledge of Django and
`Django-SHOP <http://django-shop.readthedocs.io/en/latest/>`__.

Release History
~~~~~~~~~~~~~~~

- 0.2.x - `Django-SHOP <https://github.com/awesto/django-shop>`__ v0.11.x compatibility
- 0.1.x - `Django-SHOP <https://github.com/awesto/django-shop>`__ v0.10.2 compatibility

TODO
~~~~

Please let me know of you have any feature suggestions, or wish to
implement any of the below:

-  Fix for the db initialisation warning below.
-  Tests.
-  Continuous build integration including compatibility testing with
   various python, Django and Django-SHOP versions.

Configuration
-------------

Follow the Readme for `django-currencies <https://github.com/panosl/django-currencies>`__.
Install this module through pip: ``pip install djangoshop-currencies``.

The Django-SHOP Money system has been extended to use django-currencies as a currency conversion backend.
To enable this functionality your currencies configuration must satisfy the following requirements:

1. ISO4217Exponent and symbol populating using ``./manage.py currencies iso``
   (This automatically imports the currencies set in the ``SHOP_CURRENCIES`` setting)
2. Currency factors populating using ``./manage.py updatecurrencies yahoo``
   (This also sets the base currency to ``SHOP_DEFAULT_CURRENCY``)
3. Some currencies set to active in the admin interface

.. topic:: Warning

    The *currencies* database table **must** be initialised before any Django app can import the included money types.
    Unfortunately the ``./manage.py`` command will automatically import a lot of modules when they are configured in
    INSTALLED_APPS causing an error which prevents you from running ``./manage.py migrate``, etc.

    As a workaround before a permanent solution is found:

    1. Create a minimal settings file which will be used temporarily to allow the currencies table of your database to be populated. As an example, `one is included here <shop_currencies/min_settings.py>`_.
    2. Run ``python manage.py migrate --settings shop_currencies.min_settings`` (or use your minimal settings file)
    3. Satisfy requirements 1. & 2. above & append ``--settings <min_settings>`` to the commands
    4. Run ``python manage.py migrate``
    5. Run ``python manage.py createsuperuser`` to create an admin user
    6. Satisfy requirement 3. above

    Once created, I recommend dumping your base currency as a fixture for subsequent use when initialising databases:

    .. code-block:: shell

        python manage.py dumpdata --indent 2 --output fixtures/currency.json --pks 1 currencies.currency
        python manage.py loaddata --settings shop_currencies.min_settings fixtures/currency.json

Usage
~~~~~

Replace the ``DefaultCartModifier`` with the provided ``CurrencyCartModifier``
in your shop settings:

.. code-block:: python

    SHOP_CART_MODIFIERS = (
        # provides the default cart lines
        'shop_currencies.modifiers.CurrencyCartModifier',
        ...

Use the Money conversion extension which provides the ``to(code)`` function as below.
The additional ``base`` argument is used by the cart modifier.

.. code-block:: python

    from django.db import models
    from currencies.utils import get_currency_code
    from shop_currencies.money.fields import MoneyField

    class MyModel(models.Model):
        unit_price = MoneyField()
        ...

        def get_price(self, request, base=False):
            if base:
                return self.unit_price
            else:
                session_currency_code = get_currency_code(request)
                return self.unit_price.to(session_currency_code)
