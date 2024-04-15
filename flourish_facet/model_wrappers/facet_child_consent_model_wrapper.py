
from django.apps import apps as django_apps
from django.conf import settings
from edc_model_wrapper import ModelWrapper
from edc_base.utils import age, get_utcnow


class FacetChildConsentModelWrapper(ModelWrapper):
    model = 'flourish_facet.motherchildconsent'
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'facet_child_listboard_url')
    next_url_attrs = []

    @property
    def age_in_months(self):

        if hasattr(self.object, 'child_dob'):
            today = get_utcnow().date()
            child_age = age(self.object.child_dob, today)
            return (child_age.years * 12) + child_age.months
