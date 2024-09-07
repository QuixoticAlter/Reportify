from peewee import *
import subprocess

db = SqliteDatabase("fasa.db")

class Base(Model):
    class Meta:
        database = db

class Site(Base):

    name = CharField()
    building = CharField()
    physical_address = CharField()
    city = CharField()

class Contact(Base):

    name = CharField()
    phone = CharField()
    mail = CharField()

class Machine(Base):

    serial = CharField()
    asset = CharField()
    sku = CharField()
    model = CharField()
    ip_addr = CharField()
    hostname = CharField()
    subnet_mask = CharField(null=True)
    gateway = CharField(null=True)
    mac_addr = CharField(null=True)
    site = ForeignKeyField(model=Site, null=True, backref='machines')
    contact = ForeignKeyField(model=Contact, null=True, backref='machines')
    status = CharField()
    collection_method = CharField()

class RemovedMachine(Base):
    serial = CharField()

class HelpDeskCase(Base):

    n_case = IntegerField()
    description = CharField()
    start_date = CharField()
    end_date = CharField()
    machine_associated = ForeignKeyField(model=Machine)
    site_associated = ForeignKeyField(model=Site)
    contact_associated = ForeignKeyField(model=Contact)

class ChanelCase(Base):

    n_case = IntegerField()
    machine_associated = ForeignKeyField(model=Machine)
    helpdesk_case_associated = ForeignKeyField(model=HelpDeskCase)
    description = CharField()
    category = CharField()
    response_time = CharField()

class SupplyOrder(Base):

    n_order = IntegerField()
    machine = ForeignKeyField(model=Machine, null=True)
    removed_machine = ForeignKeyField(model=RemovedMachine, null=True)
    cyan_cartridge = CharField(null=True)
    magenta_cartridge = CharField(null=True)
    yellow_cartridge = CharField(null=True)
    black_cartridge = CharField(null=True)
    creation_date = DateTimeField()
    arrival_date = DateTimeField(null=True)
    close_date = DateTimeField(null=True)

class ConsumableLevel(Base):

    machine = ForeignKeyField(model=Machine, null=True, backref='consumable_levels')
    removed_machine = ForeignKeyField(model=RemovedMachine, null=True)
    detection_date = DateTimeField()
    magenta_level = IntegerField()
    cyan_level = IntegerField()
    yellow_level = IntegerField()
    black_level = IntegerField()
    
db.connect()
db.create_tables([Machine, RemovedMachine, Site, Contact, ChanelCase, HelpDeskCase, ChanelCase, SupplyOrder, ConsumableLevel])