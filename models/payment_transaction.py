from odoo import models
from odoo.addons.payment import utils as payment_utils
import hashlib
import requests


class PaymentTransaction(models.Model):
    """Inheriting model payment transaction"""
    _inherit = 'payment.transaction'

    def _get_specific_rendering_values(self, processing_values):
        """ Override of payment to return Payu-specific rendering values.
        Note: self.ensure_one() from `_get_processing_values`
        :param dict processing_values: The generic and specific processing
        values of the transaction
        :return: The dict of provider-specific processing values
        :rtype: dict
        """

        res = super()._get_specific_rendering_values(processing_values)
        if self.provider_code != 'payu':
            return res

        api_key = self.provider_id.payu_merchant_code
        txn_id = self.reference
        amount = self.amount
        product_info = self.reference
        first_name, last_name = payment_utils.split_partner_name(
            self.partner_id.name)
        email = self.partner_email
        salt = self.provider_id.payu_merchant_key
        surl = "https://4800-111-92-105-22.ngrok-free.app/payment/payu/return"
        furl = "https://4800-111-92-105-22.ngrok-free.app/payment/payu/return"
        hash_string = f"{api_key}|{txn_id}|{amount}|{product_info}|{first_name}|{email}|||||||||||{salt}"
        hash = hashlib.sha512(hash_string.encode()).hexdigest()
        print('hash', hash)

        url = 'https://test.payu.in/_payment'
        payload = {
            'key': api_key,
            'txnid': txn_id,
            'amount': amount,
            'productinfo': product_info,
            'firstname': first_name,
            'email': email,
            'phone': self.partner_phone,
            'surl': surl,
            'furl': furl,
            'hash': hash,
        }
        print('payu values with hash', payload)
        response = requests.post(url, data=payload)
        print('response text', response.text)
        return payload

    # def _get_tx_from_notification_data(self, provider_code, notification_data):
    #     print('get tx-find transaction', self)
    #
    #
    # def _process_notification_data(self, notification_data):
    #     print('process transaction', self)
