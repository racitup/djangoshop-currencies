# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from shop.serializers.cart import ExtraCartRow
from shop.modifiers.base import BaseCartModifier
from .money import AbstractMoney, Money


class CurrencyCartModifier(BaseCartModifier):
    """Use this instead of DefaultCartModifier for all basic line item calculations"""
    # Empty carts are shown in base currency
    _foreigncurrency = False
    def process_cart_item(self, cart_item, request):
        cart_item.unit_price = cart_item.product.get_price(request, base=True)
        cart_item.line_total = cart_item.unit_price * cart_item.quantity

        # add extra row for local currency info
        local_price = cart_item.product.get_price(request)
        if local_price._currency_code != cart_item.unit_price._currency_code:
            self._foreigncurrency = True
            cart_item.extra_rows[self.identifier] = ExtraCartRow({
                'label': local_price,
                'amount': local_price * cart_item.quantity
            })
        else:
            self._foreigncurrency = False
        return super().process_cart_item(cart_item, request)

    def process_cart(self, cart, request):
        if not isinstance(cart.subtotal, AbstractMoney):
            # if we don't know the currency, use the default
            cart.subtotal = Money(cart.subtotal)
        cart.total = cart.subtotal
        if self._foreigncurrency:
            cart.extra_rows[self.identifier] = ExtraCartRow({
                'label': _("All payments are in {}".format(cart.total._currency_code))
            })
        return super().process_cart(cart, request)
