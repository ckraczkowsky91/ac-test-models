from application import db
from sqlalchemy import func

# create our database models
class Access(db.Model):
    id = db.Column(db.CHAR(255), primary_key=True)
    access_type = db.Column(db.String)
    access_value = db.Column(db.String)
    location = db.Column(db.String)
    direct_access = db.Column(db.Boolean)
    opportunities_id = db.Column(db.String, db.ForeignKey('services.id'))
    date_created = db.Column(db.DateTime)
    date_updated = db.Column(db.DateTime)
    meta_data = db.Column(db.Text)

class Address(db.Model):
    id = db.Column(db.CHAR(255), primary_key=True)
    street_number = db.Column(db.Integer)
    street_number_suffix = db.Column(db.String)
    street_name = db.Column(db.String)
    street_type = db.Column(db.String)
    street_direction = db.Column(db.String)
    address_type = db.Column(db.String)
    address_type_id = db.Column(db.String)
    minor_municipality = db.Column(db.String)
    major_municipality = db.Column(db.String)
    governing_district = db.Column(db.String)
    postal_area = db.Column(db.String)
    iso3_code = db.Column(db.CHAR(3))

    entities = db.relationship('Entity', backref='address', lazy=True)

class AsylumSeeker(db.Model):
    id = db.Column(db.CHAR(255), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)

    def __init__(self, id, user_id, first_name, last_name):
        self.id = id
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name

class Attachement(db.Model):
    id = db.Column(db.CHAR(255), primary_key=True)
    entity_id = db.Column(db.CHAR(255), db.ForeignKey('entity.id'))
    image = db.Column(db.Boolean)
    name = db.Column(db.String)
    date_uploaded = db.Column(db.DateTime)

    entities = db.relationship('Entity', backref='attachement', lazy=True)

class Comments(db.Model):
    id = db.Column(db.CHAR(255), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    entity_id = db.Column(db.CHAR(255), db.ForeignKey('entity.id'))
    date_created = db.Column(db.DateTime)
    date_updated = db.Column(db.DateTime)
    flagged = db.Column(db.Boolean)
    comment = db.Column(db.Text)

class Day(db.Model):
    id = db.Column(db.CHAR(255), primary_key=True)
    day = db.Column(db.Integer)

    daytimes = db.relationship('DayTime', backref='day', lazy=True)

class DayTime(db.Model):
    id = db.Column(db.CHAR(255), primary_key=True)
    time_id = db.Column(db.CHAR(255), db.ForeignKey('time_block.id'))
    day_id = db.Column(db.CHAR(255), db.ForeignKey('day.id'))

class Email(db.Model):
    id = db.Column(db.CHAR(255), primary_key=True)
    email = db.Column(db.String(255))
    entity_id = db.Column(db.CHAR(255), db.ForeignKey('entity.id'))

    def __init__(self, email):
        self.email = email

class Entity(db.Model):
    id = db.Column(db.CHAR(255), primary_key=True)
    name = db.Column(db.String)
    is_searchable = db.Column(db.Boolean)
    marked_deleted = db.Column(db.Boolean)
    date_created = db.Column(db.DateTime)
    date_updated_ac = db.Column(db.DateTime, server_default=func.now())
    date_updated_org = db.Column(db.DateTime, server_default=func.now())
    is_verified = db.Column(db.Boolean)
    last_verified = db.Column(db.DateTime)
    rating = db.Column(db.REAL)
    is_closed = db.Column(db.Boolean)
    phone = db.Column(db.String)
    user_id = db.Column(db.String)
    website = db.Column(db.String)
    lat = db.Column(db.REAL)
    lon = db.Column(db.REAL)
    address_id = db.Column(db.CHAR(255), db.ForeignKey('address.id'))

    attachements = db.relationship('Attachement', backref='entity', lazy=True)
    comments = db.relationship('Comments', backref='entity', lazy=True)
    emails = db.relationship('Email', backref='entity', lazy=True)
    entity_languages = db.relationship('EntityLanguage', backref='entity', lazy=True)
    entity_properties = db.relationship('EntityProperty', backref='entity', lazy=True)
    entity_tags = db.relationship('EntityTag', backref='entity', lazy=True)
    service_providers = db.relationship('ServiceProvider', backref='entity', lazy=True)
    user_favorites = db.relationship('UserFavorites', backref='entity', lazy=True)

class EntityLanguage(db.Model):
    entity_id = db.Column(db.CHAR(255), db.ForeignKey('entity.id'))
    id = db.Column(db.CHAR(255), primary_key=True)
    description = db.Column(db.Text)
    notes = db.Column(db.Text)

class EntityProperty(db.Model):
    property_id = db.Column(db.CHAR(255), db.ForeignKey('property.id'))
    id = db.Column(db.CHAR(255), primary_key=True)
    entity_id = db.Column(db.CHAR(255), db.ForeignKey('entity.id'))

class EntityTag(db.Model):
    id = db.Column(db.CHAR(255), primary_key=True)
    entity_id = db.Column(db.CHAR(255), db.ForeignKey('entity.id'))
    tag_id = db.Column(db.CHAR(255), db.ForeignKey('tags.id'))

class Organization(db.Model):
    id = db.Column(db.CHAR(255), primary_key=True)
    entity_id = db.Column(db.CHAR(255), db.ForeignKey('entity.id'))

    services = db.relationship('Services', backref='organization', lazy=True)

class Property(db.Model):
    id = db.Column(db.CHAR(255), primary_key=True)
    name = db.Column(db.String)
    definition = db.Column(db.Text)
    value = db.Column(db.String)

    entity_properties = db.relationship('EntityProperty', backref='property', lazy=True)

class Schedule(db.Model):
    id = db.Column(db.CHAR(255), primary_key=True)
    entity_id = db.Column(db.CHAR(255), db.ForeignKey('entity.id'))
    day_time_id = db.Column(db.CHAR(255), db.ForeignKey('day_time.id'))

    entities = db.relationship('Entity', backref='schedules', lazy=True)
    day_times = db.relationship('DayTime', backref='schedules', lazy=True)

class ServiceProvider(db.Model):
    id = db.Column(db.CHAR(255), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    type = db.Column(db.String)
    description = db.Column(db.String)
    organization_name = db.Column(db.String)
    about = db.Column(db.String)
    phone = db.Column(db.String)
    website = db.Column(db.String)
    cost = db.Column(db.String)
    appointment_needed = db.Column(db.Boolean)
    languages_spoken = db.Column(db.String)
    who_we_serve = db.Column(db.String)
    verified = db.Column(db.Boolean)
    entity_id = db.Column(db.CHAR(255), db.ForeignKey('entity.id'))

class Services(db.Model):
    id = db.Column(db.CHAR(255), primary_key=True)
    entity_id = db.Column(db.CHAR(255), db.ForeignKey('entity.id'))
    parent_organization = db.Column(db.CHAR(255), db.ForeignKey('organization.id'))
    appointment = db.Column(db.Boolean)

    access = db.relationship('Access', backref='service', lazy=True)

class Tags(db.Model):
    id = db.Column(db.CHAR(255), primary_key=True)
    name = db.Column(db.String)
    parent_tag = db.Column(db.String, db.ForeignKey('tags.id'))

    entity_tags = db.relationship('EntityTag', backref='tag', lazy=True)

class TimeBlock(db.Model):
    id = db.Column(db.CHAR(255), primary_key=True)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)

    daytimes = db.relationship('DayTime', backref='timeblock', lazy=True)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    user_type = db.Column(db.String)
    hashed_password = db.Column(db.String)
    salt = db.Column(db.String)
    created_at = db.Column(db.DateTime)
    iso3_code = db.Column(db.CHAR(3))
    active = db.Column(db.Boolean)
    prefered_language = db.Column(db.CHAR(3))

    comments = db.relationship('Comments', backref='user', lazy=True)
    user_favorites = db.relationship('UserFavorites', backref='user', lazy=True)
    asylum_seekers = db.relationship('AsylumSeeker', backref='user', lazy=True)
    service_providers = db.relationship('ServiceProvider', backref='user', lazy=True)

    def __init__(self, id, email, preferred_language):
        self.id = id
        self.email = email
        self.preferred_language = preferred_language

class UserFavorites(db.Model):
    id = db.Column(db.CHAR(255), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    entity_id = db.Column(db.CHAR(255), db.ForeignKey('entity.id'))
