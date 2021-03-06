# -*- coding: utf-8 -*-
from appdirs import unicode
from odoo import models, fields, api, _, tools
from decimal import Decimal


class AccountMove(models.Model):
    _inherit = "account.move"
    _description = "Journal Entry"

    # ajout champs amount_market dans le modele facturation
    amount_market = fields.Monetary(string='Montant Marché', readonly=True, compute='_get_amount_market_sale')
    advance = fields.Boolean(string="% site section", compute='_get_per_advance_categ', default=False)
    subtotal = fields.Boolean(string="subtotal section", compute='_get_per_subtotal', default=False)
    def _get_amount_market_sale(self):
        """
        Calculer Montant Marché par client.
        """
        sale_ids = self.env['sale.order'].search([('partner_id', '=', self.partner_id.id), ('state', '=', 'sale')])
        amount_market = 0.0
        for par in sale_ids:
            amount_market += par.amount_total

        self.amount_market = amount_market
        self.amount_market = amount_market
        
# @api.depends('invoice_line_ids')
    def _get_per_subtotal(self):
        """
        Calculer subtotal.
        """
        # *********************************
        for rec in self:
            subtotal = False
            tot_line = 0.0
            comp_line = 0
            tot_section = 0.0
            comp_section = 0
            # av_note = 0.0

            for line in reversed(self.invoice_line_ids):

                if line.display_type != 'line_section' and line.display_type != 'line_note':
                    # av_line += line.per_advance_product
                    tot_line += line.x_studio_subtotal
                    comp_line += 1
                if line.display_type == 'line_section':
                    if comp_line != 0:
                        tot_section += tot_line
                        tot_line -= tot_line
                        comp_line = 0
                        comp_section += 1

                if line.display_type == 'line_note':
                    if comp_section != 0:
                        tot_note = tot_section
                        tot_section -= tot_section
                        comp_section = 0
                        line.x_studio_subtotal = tot_note

            rec.subtotal = True
            
    # @api.depends('invoice_line_ids')
    def _get_per_advance_categ(self):
        """
        Calculer advance.
        """

        # *********************************
        self.advance = False
        av_line = 0.0
        comp_line = 0
        av_section = 0.0
        comp_section = 0
        # av_note = 0.0

        for line in reversed(self.invoice_line_ids):

            if line.display_type != 'line_section' and line.display_type != 'line_note':
                # av_line += line.per_advance_product
                av_line += line.x_studio_pourcentage_situation
                comp_line += 1
            if line.display_type == 'line_section':
                if comp_line != 0:
                    av_section += av_line / comp_line
                    av_line -= av_line
                    comp_line = 0
                    comp_section += 1

            if line.display_type == 'line_note':
                if comp_section != 0:
                    av_note = av_section / comp_section
                    av_section -= av_section
                    comp_section = 0
                    line.write({'per_advance_note': av_note
                                })

        self.advance = True


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"
    _description = "Journal Item"

    per_advance_note = fields.Float(string="% site", )
    categ_id = fields.Many2one(related="product_id.categ_id")
