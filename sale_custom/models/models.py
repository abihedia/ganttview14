# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"
    _description = "Sales Order"

    @api.depends('partner_id', 'amount_total')
    def _get_amount_market(self):
        """
        Calculer Montant Marché par client.
        """
        sale_ids = self.env['sale.order'].search([('partner_id', '=', self.partner_id.id),('state','=','sale')])
        amount_market = 0.0
        for par in sale_ids:
            amount_market += par.amount_total

        self.amount_market = amount_market

    amount_market = fields.Monetary(string='Montant Marché', readonly=True, compute='_get_amount_market')
