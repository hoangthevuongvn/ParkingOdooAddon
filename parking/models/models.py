# -*- coding: utf-8 -*-

from odoo import models, fields, api
from pickle import TRUE


class ParkingUser(models.Model):
    _name = 'parking.user'
    _description = 'Parking User'
    # _rec_name = 'rfid_number'
 
    
    name = fields.Char(string='Full name', required=True)
    gender = fields.Selection(string='Gender', selection=[('male', 'Male'),
                                                        ('female', 'Female')])
    dob = fields.Date(string='Date of birth', required=True)
    address = fields.Char(string='Address')
    company = fields.Char(string='Company', requied = True)
    vehicle = fields.One2many('parking.vehicle','vehicle_owner', string='Vehicle')
    membership = fields.Boolean(string='Membership')
    user_rel = fields.One2many('parking.rfid','rfid_rel', string='RFID', store=True, readonly=True)
    rfid_number = fields.Integer(string = 'RFIDS', compute='onchange_rfid_number')
    
    @api.depends("user_rel")
    def onchange_rfid_number(self):
        for record in self:
            record.rfid_number = record.user_rel.id_number
            

class ParkingRFID(models.Model):
    _name = 'parking.rfid'
    _description = 'Parking RFID'
    _rec_name = 'id_number' #hien thi ten record la gia tri cua truong id_number 
    
    rfid_rel = fields.Many2one('parking.user', string='RFID user')
    id_number = fields.Integer(string='TAG ID')
    monthly = fields.Boolean(string='Monthly')
    rfid_check_rel = fields.One2many('parking.checktagid','check_tag_rel', String = 'RFID Check Tag Rel')
    status = fields.Boolean('Status', default=False)
    count = fields.Integer()
    _sql_constraints = [('id_number_unique', 'unique(id_number)', "id number be unique!")]


class ParkingVehicle(models.Model):
    _name = 'parking.vehicle'
    _description = 'Vehicle'
    
    vehicle_owner = fields.Many2one('parking.user',string='Owner', readonly=True) 
    type = fields.Char(string='Vehicle type', required=True)
    color = fields.Selection(string='Color', selection=[('red', 'Red'),('black', 'Black'),
                                                       ('white','White'),('yellow', 'Yellow')])
    license_plate = fields.Char(string='License plate', required=True)
    _sql_constraints = [('license_plate_unique', 'unique(license_plate)', "Licence be unique!")]
    
class CheckTagID(models.Model):
    _name = 'parking.checktagid'
    _description = 'Check Tag Id'
    
    check_tag_rel = fields.Many2one('parking.rfid', String='Check TagID Rel')
    count_status = fields.Integer(related='check_tag_rel.count')
    time_in = fields.Datetime('Time in')
    time_out = fields.Datetime('Time out')
    total_time = fields.Datetime('Total time')
    
        
    