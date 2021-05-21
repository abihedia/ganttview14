# -*- coding: utf-8 -*-
from appdirs import unicode
from odoo import models, fields, api, _, tools


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
    per_advance_section = fields.Char(string="% site section", compute='_get_per_advance_categ')
    per_advance_note = fields.Char(string="% site note", compute='_get_per_advance_categ')

    def _get_amount_market_sale(self):
        """
        Calculer Montant Marché par client.
        """
        sale_ids = self.env['sale.order'].search([('partner_id', '=', self.partner_id.id)])
        amount_market = 0.0
        for par in sale_ids:
            amount_market += par.amount_total

        self.amount_market = amount_market
        self.amount_market = amount_market

    @api.depends('invoice_line_ids')
    def _get_per_advance_categ(self):
        """
        Calculer avancement par section.
        """
        # section
        data_section = []
        data_note = []
        section = ''
        note = ''
        for line in self.invoice_line_ids:
            st_section = self.env['product.category'].search([('id', '=', line.categ_id.id)])
            data_section.append(st_section.id)
        # supprimer les doublons data_section
        lwd = []
        for i in data_section:
            if i not in lwd: lwd.append(i)


        # note
        for line in self.invoice_line_ids:
            st_note = self.env['product.category'].search([('id', '=', line.categ_id.parent_id.id)])
            data_note.append(st_note.id)
        print("data_note",data_note)
        # supprimer les doublons data_note
        lwd_note = []
        for i in data_note:
            if i not in lwd_note: lwd_note.append(i)
        print("data note**********", lwd_note)
        for num in lwd:
            avance_per_section = 0.0
            avancement_section = 0.0
            compteur_section = 0
            section_name = ""
            note_id = 0
            note_name = ""



            for line in self.invoice_line_ids:

                if line.categ_id.id != num:
                    continue
                else:
                    avancement_section += line.per_advance_product
                    compteur_section += 1
                    section_name = line.categ_id.name
                    note_name = line.categ_id.parent_id.name
                    note_id = line.categ_id.parent_id.id
                    avance_per_section = avancement_section / compteur_section
            # self.env['section.note'].create({
            #         'type': 'section',
            #         'section_name': section_name,
            #         'categ_id': 'num',
            #         'avdvanced_per_section': avance_per_section,
            #     })
            # section += "section: " + section_name + " avancement: " + str("%.2f" % avance_per_section) + "\n"
            if section_name:
                section += "section: %s avancement: %8.2s \n" % (section_name , avance_per_section)
            avancement_note = 0.0
            compteur_note = 0
            for num_note in lwd_note:
                avance_per_note = 0

                print("note_id",note_id)
                print("num_note",num_note)

                if note_id != num_note:
                    continue
                # note_id==num_note
                else:
                    avancement_note += avance_per_section
                    compteur_note += 1
                    note_name = note_name
                    avance_per_note = avancement_note / compteur_note
                    print("avancement_note", avancement_note)
                    print("compteur_note", compteur_note)
                    print("note_name", note_name)
                    print("avance_per_note", avance_per_note)
                # note += "note: " + note_name + " avancement: " + str("%.2f" % avance_per_note) + "\n"

        self.per_advance_note = note

        self.per_advance_section = section



class AccountMoveLine(models.Model):
    _inherit = "account.move.line"
    _description = "Journal Item"

    per_advance_product = fields.Float(string="% site", )
    categ_id = fields.Many2one(related="product_id.categ_id")

