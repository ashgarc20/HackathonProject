import webapp2
import jinja2
import os
import logging
import time
from google.appengine.ext import ndb
from models import Tree_Application
​
​
the_jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
    
class CoordsRequest(ndb.Model):
    lat = ndb.StringProperty(required = True)
    lon = ndb.StringProperty(required = True)
    timestamp = ndb.DateTimeProperty(auto_now_add = True)
​
class AddressRequest(ndb.Model):
    address = ndb.StringProperty(required = True)
    timestamp = ndb.DateTimeProperty(auto_now_add = True)
    
def run_query(location, o_name, a_name, o_email, a_email, o_phone_num, a_phone_num, tree_number, tree_species, date):
    user_info = Tree_Application(address = location, owner_name = o_name, applicant_name = a_name, owner_email = o_email, applicant_email = a_email, owner_phone_num = o_phone_num, applicant_phone_num = a_phone_num, num_of_trees = tree_number, tree_type = tree_species, date_submitted = date)
    info_key = user_info.put()
​
# class webapp2.RequestHandler(webapp2.webapp2.RequestHandler):
#     def dispatch(self):
#         # Get a request store for this request.
#         self.request_store = requests.get_store(request=self.request)
#         print("request loading %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
​
#         try:
#             # Dispatch the request.
#             webapp2.webapp2.RequestHandler.dispatch(self)
#         finally:
#             # Save all requests.
#             print("saving request $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
#             self.request_store.save_requests(self.response)
​
#     @webapp2.cached_property
#     def request(self):
#         # Returns a request using the default cookie key.
#         return self.request_store.get_request()    
​
class WelcomePageHandler(webapp2.RequestHandler):
    def get(self):
        welcome_template = the_jinja_env.get_template('design_pages/welcome.html')
        self.response.write(welcome_template.render())
        
class FormHandler(webapp2.RequestHandler):
    def get(self):
        personal_contact_template = the_jinja_env.get_template('form_pages/personal_contact.html')
        self.response.write(personal_contact_template.render())
​
# class SiteInfoHandler(webapp2.RequestHandler):
#     def get(self):
​
# <<<<<<< HEAD
​
#         self.request['ownname'] = self.request.get('ownname')
#         self.request['appliname'] = self.request.get('appliname')
#         self.request['ownemail'] = self.request.get('ownemail')
#         self.request['appliemail'] = self.request.get('appliemail')
#         self.request['ownphone'] = self.request.get('ownphone')
#         self.request['appliphone'] = self.request.get('appliphone')
#         self.request['submission'] = self.request.get('submission')
#         self.request['address'] = self.request.get('address')
   
#         site_info_template = the_jinja_env.get_template('form_pages/site_info.html')
#         self.response.write(site_info_template.render())
# =======
#         self.session['ownname'] = self.request.get('ownname')
#         self.session['appliname'] = self.request.get('appliname')
#         self.session['ownemail'] = self.request.get('ownemail')
#         self.session['appliemail'] = self.request.get('appliemail')
#         self.session['ownphone'] = self.request.get('ownphone')
#         self.session['appliphone'] = self.request.get('appliphone')
#         self.session['submission'] = self.request.get('submission')
        
#         myDict = {
#             'address_from_python_dict': '277 River Road'
#         }
​
#         site_info_template = the_jinja_env.get_template('form_pages/site_info.html')
#         self.response.write(site_info_template.render(myDict))
# >>>>>>> b9ec29afe5554df3029e3e9de5498755f6e01ddb
        
# class TermsAndConditionsHandler(webapp2.RequestHandler):
#     def get(self):
        
#         self.request['tree'] = self.request.get('tree')
#         self.request['quantity'] = self.request.get('quantity')
#         print("in terms and conditions handler: ", self.request.get('ownemail'))
       
#         terms_conditions_template = the_jinja_env.get_template('form_pages/terms_conditions.html')
#         self.response.write(terms_conditions_template.render())
        
class ViewApplicationHandler(webapp2.RequestHandler):
    def post(self):
        
        view_application_template = the_jinja_env.get_template('background_database/view_application.html')
        
        address = self.request.get('address')
        owner_name = self.request.get('ownname')
        applicant_name = self.request.get('appliname')
        owner_email = self.request.get('ownemail')
        applicant_email = self.request.get('appliemail')
        owner_phone_num = self.request.get('ownphone')
        applicant_phone_num = self.request.get('appliphone')
        num_of_trees = self.request.get('quantity')
        tree_type = self.request.get('tree')
        date_submitted = self.request.get('submission')
        
     
        run_query(address, owner_name, applicant_name, owner_email, applicant_email, owner_phone_num, applicant_phone_num, num_of_trees, tree_type, date_submitted)
        
        the_variable_dict = {
            "place": address,
            "own_name": owner_name,
            "app_name": applicant_name,
            "own_email": owner_email,
            "app_email": applicant_email,
            "own_phone": owner_phone_num,
            "app_phone": applicant_phone_num,
            "tree_amount": num_of_trees,
            "species_trees": tree_type,
            'time': date_submitted,
        }
        
        self.response.write(view_application_template.render(the_variable_dict))
        
        
class SubmitPageHandler(webapp2.RequestHandler):
    def get(self):
        submit_template = the_jinja_env.get_template('design_pages/submit.html')
        self.response.write(submit_template.render())
        
class ViewableDatabase(webapp2.RequestHandler):
    def get(self):
        all_data_template = the_jinja_env.get_template('background_database/viewable_database.html')
     
        all_data = Tree_Application.query().fetch()
        
        the_variable_dict = {
            'all_data': all_data
        }
        
        self.response.write(all_data_template.render(the_variable_dict))
​
​
app = webapp2.WSGIApplication([
    ('/', WelcomePageHandler),
    ('/form', FormHandler),
    ('/result', ViewApplicationHandler),
    ('/complete', SubmitPageHandler),
    ('/database', ViewableDatabase),
​
], debug=True)