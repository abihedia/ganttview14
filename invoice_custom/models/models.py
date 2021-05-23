# -*- coding: utf-8 -*-
from appdirs import unicode
from odoo import models, fields, api, _, tools
from decimal import Decimal


#
# class SectionNote(models.Model):
#     _inherit = "section.note"
#     _description = "Section Note"
#
#     type = fields.Selection([
#         ('section', 'Section'),
#         ('note', 'Note'),
#     ], default=False,)
#     section_name = fields.Char('nom section')
#     categ_id = fields.Many2one('product.category')
#     avdvanced_per_section = fields.Float('avancement par section')
#     move_line_id = fields.Many2one()


class AccountMove(models.Model):
    _inherit = "account.move"
    _description = "Journal Entry"

    # ajout champs amount_market dans le modele facturation
    amount_market = fields.Monetary(string='Montant Marché', readonly=True, compute='_get_amount_market_sale')
    advance = fields.Boolean(string="% site section", compute='_get_per_advance_categ', default=False)

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

    @api.depends('invoice_line_ids')
    def _get_per_advance_categ(self):
        """
        Calculer advance.
        """

        # *********************************
        av_line = 0.0
        comp_line = 0
        av_section = 0.0
        comp_section = 0
        # av_note = 0.0
        for line in self.invoice_line_ids:

            if line.display_type != 'line_section' and line.display_type != 'line_note':
                av_line += line.per_advance_product
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
                    line.write({'per_advance_product': av_note
                                })

        self.advance = True


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"
    _description = "Journal Item"

    per_advance_product = fields.Float(string="% site", )
    categ_id = fields.Many2one(related="product_id.categ_id")
