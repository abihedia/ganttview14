# -*- coding: utf-8 -*-
from appdirs import unicode
from odoo import models, fields, api, _, tools
from odoo.exceptions import UserError, AccessError, ValidationError, RedirectWarning


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
                av_line += line.per_advance
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

    per_advance_note = fields.Float(string="% note", )
    categ_id = fields.Many2one(related="product_id.categ_id")
    project_id = fields.Many2one('project.task', string="Projet")
    per_advance = fields.Float(related="project_id.per_advance", string="% d'avancement", )


class Task(models.Model):
    _inherit = "project.task"
    _description = "Task"

    @api.constrains('per_advance')
    def _check_value(self):
        if self.per_advance > 1 or self.per_advance < 0:
            raise ValidationError(_('Avancement doit être entre 0-100.'))

    per_advance = fields.Float(string="% d'avancement", copy=True, )
