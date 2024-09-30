from peewee import *

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

class NRD(Base):

    machine_associated = ForeignKeyField(model=Machine)
    last_collection_date = DateTimeField()
    has_conectivity = BooleanField(null=True)
    is_machine_change = BooleanField(null=True)
    is_unknown_reason = BooleanField(null=True)

class RemovedMachine(Base):
    serial = CharField()

class HelpDeskCase(Base):

    ticket = IntegerField()
    description = CharField()
    start_date = DateTimeField()
    end_date = DateTimeField()
    machine_associated = ForeignKeyField(model=Machine, null=True)
    site_associated = ForeignKeyField(model=Site, null=True)
    contact_associated = ForeignKeyField(model=Contact, null=True)

class ChannelCase(Base):

    n_case = IntegerField()
    work_order = CharField()
    machine_associated = ForeignKeyField(model=Machine, backref='channel_cases', null=True)
    helpdesk_case_associated = ForeignKeyField(model=HelpDeskCase, null=True)
    description = CharField(null=True)
    status = CharField()
    creation_date = DateTimeField()
    close_date = DateTimeField(null=True)

class MachineChange(Base):

    old_serial = CharField()
    new_serial = CharField()
    case_associated = ForeignKeyField(model=ChannelCase, null=True)
    site_associated = ForeignKeyField(model=Site, null=True)
    change_date = DateTimeField(null=True)
    msl_sent = BooleanField(null=True)
    dcc_updated = BooleanField(null=True)

class OSATASK(Base):

    n_case = IntegerField()
    description = CharField()
    creation_date = CharField()
    machine_associated = CharField()

class OSARR(Base):

    n_case = IntegerField()
    description = CharField()
    creation_date = CharField()
    machine_associated = CharField()

class OSAFOV(Base):

    n_case = IntegerField()
    description = CharField()
    creation_date = CharField()
    machine_associated = CharField()

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
db.create_tables([
    Machine, RemovedMachine, Site, Contact, ChannelCase, MachineChange, 
    HelpDeskCase, OSATASK, OSARR, OSAFOV, SupplyOrder, ConsumableLevel, NRD
])