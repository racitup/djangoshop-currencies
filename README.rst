djangoshop-currencies
=====================

Django-SHOP integration with `django-currencies <https://github.com/panosl/django-currencies>`__

Introduction
------------

This module allows Django-SHOP implementations to integrate live
currency feeds. This will allow you to offer your shop product prices
in the user's chosen currency.
The module is currently compatible with Django v1.10.7 and
`Django-SHOP <https://github.com/awesto/django-shop>`__ v0.10.2. This
documentation assumes a working knowledge of Django and
`Django-SHOP <http://django-shop.readthedocs.io/en/latest/>`__.

TODO
----

Please let us know of you have any feature suggestions, or wish to
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

1. ISO4217Exponent and symbol populating using ``manage.py currencies iso``
   (This automatically imports the currencies set in the ``SHOP_CURRENCIES`` setting)
2. Currency factors populating using ``manage.py updatecurrencies <source>``
   (This also sets the base currency to ``SHOP_DEFAULT_CURRENCY``)
3. Some currencies set to active in the admin interface

.. warning::

    The currencies database table **must** be initialised before any Django app can import the included money types.
    If initialising a new database after shop project development, follow these steps:

    1. In the settings ``INSTALLED_APPS`` comment out entries starting with ``cmsplugin_cascade`` and ``shop`` plus your shop implementation
    2. Comment out ``ROOT_URLCONF``
    3. In ``MIDDLEWARE_CLASSES`` comment out ``shop`` entries
    4. Run ``python manage.py migrate``
    5. Satisfy requirements 1 & 2 above
    6. Run ``python manage.py createsuperuser`` to create an admin user
    7. Restore your settings
    8. Migrate again
    9. Satisfy requirement 3 above

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
