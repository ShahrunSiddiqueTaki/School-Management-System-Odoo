# -*- coding: utf-8 -*-
from odoo import api, fields, models, http
from datetime import datetime

class SchoolManagement(models.Model):
    _name = 'school.management'
    _description = 'School Management'

    name = fields.Char(string='Name')
    phone = fields.Char(string='Phone')
    mail = fields.Char(string='Email')
    age = fields.Char(string='Age')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], string='Gender')
    dateOfBirth = fields.Date(string='Date Of Birth')
    class_id = fields.Many2one(comodel_name='s.class', string='Class')

    address = fields.Char(string='Address')
    state = fields.Char(string='State')
    city = fields.Char(string='City')
    zip = fields.Char(string='Zip')

    uid = fields.Integer()
    total_invoice = fields.Integer(compute='_compute_total_invoice')

    states = fields.Selection([('draft', 'Draft'), ('finish', 'Finish'), ('cancel', '')], default='draft')

    def action_draft(self):
        self.states = 'draft'

    # def action_cancellation(self):
    #     self.states = 'cancellation'

    def action_finish(self):
        data = {
            'name': self.name,
            'phone': self.phone,
            'mail': self.mail,
            'age': self.age,
            'gender': self.gender,
            'dateOfBirth': self.dateOfBirth,
            'address': self.address,
            'state': self.state,
            'city': self.city,
            'class_id': int(self.class_id),
            'zip': self.zip,
            'uid': self.uid,
        }
        http.request.env['s.finish'].create(data)
        self.states = 'finish'

    # def action_cancel(self):
    #     self.states = 'draft'

    def action_invoices(self):
        return {
            'name': 'Invoices',
            'view_mode': 'list,form',
            'res_model': 'account.move',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'domain': [('partner_id', '=', self.env['res.users'].search([('id', '=', int(self.uid))]).read(['partner_id'])[0]['partner_id'][0])],
            'context': {'default_partner_id': self.env['res.users'].search([('id', '=', int(self.uid))]).read(['partner_id'])[0]['partner_id'][0]}
        }

    def _compute_total_invoice(self):
        self.total_invoice = self.env['account.move'].search_count([('partner_id', '=', self.env['res.users'].search([('id', '=', int(self.uid))]).read(['partner_id'])[0]['partner_id'][0])])

class SFinish(models.Model):
    _name = 's.finish'
    _description = 'School Management'

    name = fields.Char(string='Name')
    phone = fields.Char(string='Phone')
    mail = fields.Char(string='Email')
    age = fields.Char(string='Age')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], string='Gender')
    dateOfBirth = fields.Date(string='Date Of Birth')
    class_id = fields.Many2one(comodel_name='s.class', string='Class')

    address = fields.Char(string='Address')
    state = fields.Char(string='State')
    city = fields.Char(string='City')
    zip = fields.Char(string='Zip')

    uid = fields.Integer()
    total_invoice = fields.Integer(compute='_compute_total_invoice')

    def action_invoices(self):
        return {
            'name': 'Invoices',
            'view_mode': 'list,form',
            'res_model': 'account.move',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'domain': [('partner_id', '=', self.env['res.users'].search([('id', '=', int(self.uid))]).read(['partner_id'])[0]['partner_id'][0])],
            'context': {'default_partner_id': self.env['res.users'].search([('id', '=', int(self.uid))]).read(['partner_id'])[0]['partner_id'][0]}
        }

    def _compute_total_invoice(self):
        self.total_invoice = self.env['account.move'].search_count([('partner_id', '=', self.env['res.users'].search([('id', '=', int(self.uid))]).read(['partner_id'])[0]['partner_id'][0])])


class STeacher(models.Model):
    _name = 's.teacher'
    _description = 'Teacher'

    name = fields.Char(string='Name')
    phone = fields.Char(string='Phone')
    mail = fields.Char(string='Email')
    subject = fields.Char(string='Subject')
    age = fields.Char(string='Age')
    gender = fields.Selection([
            ('male', 'Male'),
            ('female', 'Female'),
        ],string='Gender')

    total_student = fields.Integer(compute='_compute_total_student')

    def action_student(self):
        return {
            'name': 'Students',
            'view_mode': 'list,form',
            'res_model': 'school.management',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'domain': [('class_id', '=', tuple([int(x) for x in list(self.env['s.class'].search([('teacher_id', '=', self.id)]))]))],
            'context': {'default_class_id': tuple([int(x) for x in list(self.env['s.class'].search([('teacher_id', '=', self.id)]))])}
        }

    def _compute_total_student(self):
        # self.total_student = self.env['school.management'].search_count([('class_id', '=', )])
        self.total_student = self.env['school.management'].search_count([('class_id', '=', tuple([int(x) for x in list(self.env['s.class'].search([('teacher_id', '=', self.id)]))]))])
        # print(self.env['s.class'].search([('teacher_id', '=', self.id)]))
        # print(tuple([int(x) for x in list(self.env['s.class'].search([('teacher_id', '=', self.id)]))]))
        # self.total_student = self.env['school.management'].search_count([('class_id', '=', self.id)])
        # self.total_student = 0

        print(self.env['school.management'].search([('class_id', '=', tuple([int(x) for x in list(self.env['s.class'].search([('teacher_id', '=', self.id)]))]))]))

class SClass(models.Model):
    _name = 's.class'
    _description = 'Class'

    name = fields.Char(string='Name')
    room = fields.Char(string='Room No.')
    capecity = fields.Char(string='Capecity')
    teacher_id = fields.Many2one(comodel_name='s.teacher', string='Teacher')

    total_student = fields.Integer(compute='_compute_total_student')

    admission_fee = fields.Many2one(comodel_name='product.template', string='Admission Fee', domain="[('school_ok', '=', True)]")
    tuition_fees = fields.Many2one(comodel_name='product.template', string='Tuition Fees', domain="[('school_ok', '=', True)]")
    # print(product_template)
    # admission_fee = fields.Many2one(comodel_name='product.product', string='Admission Fee', domain="[('product_tmpl_id', '=', product_template.id)]")

    # x = http.request.env['s.application']

    # for x in admission_fee:
    #     print(x)
    # admission_fee = fields.Many2one(comodel_name='product.product', string='Admission Fee', domain="[('product_tmpl_id', '=', 9)]")

    # admission_fee = fields.Many2one(comodel_name='product.product', string='Admission Fee', compute='_compute_admission_fee')
    # admission_fee = fields.Many2one(comodel_name='product.product', string='Admission Fee', domain="[('product_tmpl_id', '=', http.request.env['product.template'].search([('school_ok', '=', True)]))]")
    # tuition_fees = fields.Many2one(comodel_name='product.product', string='Tuition Fees')

    # @api.depends('admission_fee')
    # @api.one
    # @api.onchange('admission_fee')
    # def _get_admission_fee(self):
    #     print(self)
    #     self.admission_fee = self.env['product.product'].search([('product_tmpl_id', '=', 9)])
        # return {'domain': {'admission_fee': [('product_tmpl_id', '=', 9)]}}
        # return {'domain': {'admission_fee': [('product_tmpl_id', '=', [x.id for x in self.venue_id.facility_lines])]}}

    # def _compute_admission_fee(self):
    #     print(self.env['product.product'].search([('product_tmpl_id', '=', self.env['product.template'].search([('school_ok', '=', True)]))]))
    #
    #     self.admission_fee = self.env['product.product'].search([('product_tmpl_id', '=', self.env['product.template'].search([('school_ok', '=', True)]))])

    def action_student(self):
        return {
            'name': 'Students',
            'view_mode': 'list,form',
            'res_model': 'school.management',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'domain': [('class_id', '=', self.id)],
            'context': {'default_class_id': self.id}
        }

    def _compute_total_student(self):
        self.total_student = self.env['school.management'].search_count([('class_id', '=', self.id)])

class SApplication(models.Model):
    _name = 's.application'
    _description = 'Online Application'

    name = fields.Char(string='Name')
    phone = fields.Char(string='Phone')
    mail = fields.Char(string='Email')
    age = fields.Char(string='Age')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], string='Gender')
    dateOfBirth = fields.Date(string='Date Of Birth')
    class_id = fields.Many2one(comodel_name='s.class', string='Class')

    address = fields.Char(string='Address')
    state = fields.Char(string='State')
    city = fields.Char(string='City')
    zip = fields.Char(string='Zip')

    uid = fields.Integer()
    states = fields.Selection([('draft', 'Draft'), ('admission', 'Admission Test'), ('assign', 'Assign Class')], default='draft')

    total_invoice = fields.Integer(compute='_compute_total_invoice')

    date = fields.Date(default=datetime.today())

    def action_draft(self):
        self.states = 'draft'

    def action_admission(self):

        self.env.ref('school_management.mail_template_1').send_mail(self.id)
        # print(self.date.year)
        # indata = {
        #     'move_type': 'out_invoice',
        #     'state': 'draft',
        #     'partner_id': self.env['res.users'].search([('id', '=', int(self.uid))]).read(['partner_id'])[0]['partner_id'][0],
        # }
        # self.env['account.move'].create(indata)
        # template.send_mail(self.id, force_send=True)
        sequence_prefix = "INV/" + str(self.date.year) + "/"
        sequence_number = max([x['sequence_number'] for x in self.env['account.move'].search([('sequence_prefix', '=', sequence_prefix)]).read(['sequence_number'])]) + 100001
        invoice_name = sequence_prefix + str(sequence_number)[1:]
        product_template_id = self.env['s.class'].search([('id', '=', int(self.class_id.id))]).read(['admission_fee'])[0]['admission_fee'][0]
        product_product = self.env['product.product'].search([('product_tmpl_id', '=', int(product_template_id))])
        product_template = self.env['product.template'].search([('id', '=', int(product_template_id))])

        invoice = {
            'name': invoice_name,
            'move_type': 'out_invoice',
            'state': 'draft',
            'invoice_date': self.date,
            'partner_id': self.env['res.users'].search([('id', '=', int(self.uid))]).read(['partner_id'])[0]['partner_id'][0],
            'invoice_line_ids': [0, 0, {
                'product_id': product_product.id,
                'quantity': 1.0,
                'price_unit': product_template.list_price,
            }]
        }
        self.env['account.move'].create(invoice)
        self.env['account.move'].search([('name', '=', invoice_name)]).write({'state': 'posted'})
        self.states = 'admission'

    def action_assign(self):
        self.env.ref('school_management.mail_template_2').send_mail(self.id)
        # indata = {
        #     'move_type': 'out_invoice',
        #     'state': 'draft',
        #     'partner_id': self.env['res.users'].search([('id', '=', int(self.uid))]).read(['partner_id'])[0]['partner_id'][0],
        # }
        # self.env['account.move'].create(indata)
        data = {
            'name': self.name,
            'phone': self.phone,
            'mail': self.mail,
            'age': self.age,
            'gender': self.gender,
            'dateOfBirth': self.dateOfBirth,
            'address': self.address,
            'state': self.state,
            'city': self.city,
            'class_id': int(self.class_id),
            'zip': self.zip,
            'uid': self.uid,
            'states': 'draft'
        }
        http.request.env['school.management'].create(data)
        # self.env["s.application"].sudo().search([('id', '=', self.id)]).unlink()

        sequence_prefix = "INV/" + str(self.date.year) + "/"
        sequence_number = max([x['sequence_number'] for x in self.env['account.move'].search([('sequence_prefix', '=', sequence_prefix)]).read(['sequence_number'])]) + 100001
        invoice_name = sequence_prefix + str(sequence_number)[1:]
        product_template_id = self.env['s.class'].search([('id', '=', int(self.class_id.id))]).read(['tuition_fees'])[0]['tuition_fees'][0]
        product_product = self.env['product.product'].search([('product_tmpl_id', '=', int(product_template_id))])
        product_template = self.env['product.template'].search([('id', '=', int(product_template_id))])

        invoice = {
            'name': invoice_name,
            'move_type': 'out_invoice',
            'state': 'draft',
            'invoice_date': self.date,
            'partner_id': self.env['res.users'].search([('id', '=', int(self.uid))]).read(['partner_id'])[0]['partner_id'][0],
            'invoice_line_ids': [0, 0, {
                'product_id': product_product.id,
                'quantity': 1.0,
                'price_unit': product_template.list_price,
            }]
        }
        self.env['account.move'].create(invoice)
        self.env['account.move'].search([('name', '=', invoice_name)]).write({'state': 'posted'})
        self.states = 'assign'

    def action_invoices(self):
        return {
            'name': 'Invoices',
            'view_mode': 'list,form',
            'res_model': 'account.move',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'domain': [('partner_id', '=', self.env['res.users'].search([('id', '=', int(self.uid))]).read(['partner_id'])[0]['partner_id'][0])],
            'context': {'default_partner_id': self.env['res.users'].search([('id', '=', int(self.uid))]).read(['partner_id'])[0]['partner_id'][0]}
        }

    def _compute_total_invoice(self):
        self.total_invoice = self.env['account.move'].search_count([('partner_id', '=', self.env['res.users'].search([('id', '=', int(self.uid))]).read(['partner_id'])[0]['partner_id'][0])])

class ProductProduct(models.Model):
    _inherit = "product.template"

    school_ok = fields.Boolean('School', default=False)
    purchase_ok = fields.Boolean('Can be Purchased', default=False)
