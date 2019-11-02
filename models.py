from google.appengine.ext import ndb

class Tree_Application(ndb.Model):
    address = ndb.StringProperty(required=True)
    owner_name = ndb.StringProperty(required=True)
    applicant_name = ndb.StringProperty(required=True)
    owner_email = ndb.StringProperty(required=True)
    applicant_email = ndb.StringProperty(required=True)
    owner_phone_num = ndb.StringProperty(required=True)
    applicant_phone_num = ndb.StringProperty(required=True)
    num_of_trees = ndb.StringProperty(required=True)
    tree_type = ndb.StringProperty(required=True)
    date_submitted = ndb.StringProperty(required=True)