import webapp2
import jinja2
import os
from models import Tree_Application
from webapp2_extras import sessions

the_jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
    
def run_query(location, o_name, a_name, o_email, a_email, o_phone_num, a_phone_num, tree_number, tree_species, date):
    user_info = Tree_Application(address = location, owner_name = o_name, applicant_name = a_name, owner_email = o_email, applicant_email = a_email, owner_phone_num = o_phone_num, applicant_phone_num = a_phone_num, num_of_trees = tree_number, tree_type = tree_species, date_submitted = date)
    info_key = user_info.put()

class BaseHandler(webapp2.RequestHandler):
    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()    

class WelcomePageHandler(BaseHandler):
    def get(self):
        welcome_template = the_jinja_env.get_template('design_pages/welcome.html')
        self.response.write(welcome_template.render())
        
class PersonalContactHandler(BaseHandler):
    def get(self):
        personal_contact_template = the_jinja_env.get_template('form_pages/personal_contact.html')
        self.response.write(personal_contact_template.render())

class SiteInfoHandler(BaseHandler):
    def get(self):

        self.session['ownname'] = self.request.get('ownname')
        self.session['appliname'] = self.request.get('appliname')
        self.session['ownemail'] = self.request.get('ownemail')
        self.session['appliemail'] = self.request.get('appliemail')
        self.session['ownphone'] = self.request.get('ownphone')
        self.session['appliphone'] = self.request.get('appliphone')
        self.session['submission'] = self.request.get('submission')

        site_info_template = the_jinja_env.get_template('form_pages/site_info.html')
        self.response.write(site_info_template.render())
        
class TermsAndConditionsHandler(BaseHandler):
    def get(self):
        
        self.session['tree'] = self.request.get('tree')
        self.session['quantity'] = self.request.get('quantity')
       
        terms_conditions_template = the_jinja_env.get_template('form_pages/terms_conditions.html')
        self.response.write(terms_conditions_template.render())
        
class ViewApplicationHandler(BaseHandler):
    def post(self):
        
        view_application_template = the_jinja_env.get_template('background_database/view_application.html')
        
        address = self.session.get('address')
        owner_name = self.session.get('ownname')
        applicant_name = self.session.get('appliname')
        owner_email = self.session.get('ownemail')
        applicant_email = self.session.get('appliemail')
        owner_phone_num = self.session.get('ownphone')
        applicant_phone_num = self.session.get('appliphone')
        num_of_trees = self.session.get('quantity')
        tree_type = self.session.get('tree')
        date_submitted = self.session.get('submission')
     
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
        
        
class SubmitPageHandler(BaseHandler):
    def get(self):
        submit_template = the_jinja_env.get_template('welcome_submit_pages/submit.html')
        self.response.write(submit_template.render())
        
class ViewableDatabase(BaseHandler):
    def get(self):
        all_data_template = the_jinja_env.get_template('background_database/viewable_database.html')
     
        all_data = Tree_Application.query().fetch()
        
        the_variable_dict = {
            'all_data': all_data
        }
        
        self.response.write(all_data_template.render(the_variable_dict))

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'my-super-secret-key',
}

app = webapp2.WSGIApplication([
    ('/', WelcomePageHandler),
    ('/form1', PersonalContactHandler),
    ('/form2', SiteInfoHandler),
    ('/form3', TermsAndConditionsHandler),
    ('/result', ViewApplicationHandler),
    ('/complete', SubmitPageHandler),
    ('/database', ViewableDatabase),

], debug=True, config=config)