from django.contrib import admin
from ...models import InfantBehaviourQuestionnaire
from ...forms import InfantBehaviourQuestionnaireForm
from ...admin_site import flourish_facet_admin
from edc_model_admin import audit_fieldset_tuple, audit_fields
from ..modeladmin_mixins import CrfModelAdminMixin


@admin.register(InfantBehaviourQuestionnaire, site=flourish_facet_admin)
class InfantBehaviourQuestionnaireAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = InfantBehaviourQuestionnaireForm

    fieldsets = (
        (None, {
            'fields': (
                'facet_visit',
                'report_datetime',
                'dob',
                'child_age',
                'dressed_squirm',
                'tossed_laugh',
                'tired_distress',
                'unfamilar_adult_cling',
                'enjoy_read',
                'play_toy',
                'move_towards_objects',
                'water_laugh',
                'nap_whimper',
                'after_sleep_cry',
                'feeding_get_away',
                'sing_soothe',
                'put_on_back',
                'peackaboo_laugh',
                'lookup_telephone',
                'angry_crib',
                'startle_body_position',
                'enjoy_words',
                'look_books',
                'visit_exicited',
                'toy_laugh',
                'exciting_day_tearful',
                'protest_confinement',
                'held_enjoy',
                'look_at_soothe',
                'hair_wash_vocalize',
                'airplane_sound',
                'unfamilar_adult_refuse',
                'activity_often_cry',
                'enyoy_swaying',
                'stare_picture',
                'wanted_upset',
                'unfamilar_adult_cling_again',
                'enyoy_rocking',
                'rubbing_soothe',
                'take_outside',
                'talking_sound',
                'blanket_squirm',
                'comment',
            )
        }), audit_fieldset_tuple
    )

    radio_fields = {
        'dressed_squirm': admin.HORIZONTAL,
        'tossed_laugh': admin.HORIZONTAL,
        'tired_distress': admin.HORIZONTAL,
        'unfamilar_adult_cling': admin.HORIZONTAL,
        'enjoy_read': admin.HORIZONTAL,
        'play_toy': admin.HORIZONTAL,
        'move_towards_objects': admin.HORIZONTAL,
        'water_laugh': admin.HORIZONTAL,
        'nap_whimper': admin.HORIZONTAL,
        'after_sleep_cry': admin.HORIZONTAL,
        'feeding_get_away': admin.HORIZONTAL,
        'sing_soothe': admin.HORIZONTAL,
        'put_on_back': admin.HORIZONTAL,
        'peackaboo_laugh': admin.HORIZONTAL,
        'lookup_telephone': admin.HORIZONTAL,
        'angry_crib': admin.HORIZONTAL,
        'startle_body_position': admin.HORIZONTAL,
        'enjoy_words': admin.HORIZONTAL,
        'look_books': admin.HORIZONTAL,
        'visit_exicited': admin.HORIZONTAL,
        'toy_laugh': admin.HORIZONTAL,
        'exciting_day_tearful': admin.HORIZONTAL,
        'protest_confinement': admin.HORIZONTAL,
        'held_enjoy': admin.HORIZONTAL,
        'look_at_soothe': admin.HORIZONTAL,
        'hair_wash_vocalize': admin.HORIZONTAL,
        'airplane_sound': admin.HORIZONTAL,
        'unfamilar_adult_refuse': admin.HORIZONTAL,
        'activity_often_cry': admin.HORIZONTAL,
        'enyoy_swaying': admin.HORIZONTAL,
        'stare_picture': admin.HORIZONTAL,
        'wanted_upset': admin.HORIZONTAL,
        'unfamilar_adult_cling_again': admin.HORIZONTAL,
        'enyoy_rocking': admin.HORIZONTAL,
        'rubbing_soothe': admin.HORIZONTAL,
        'take_outside': admin.HORIZONTAL,
        'talking_sound': admin.HORIZONTAL,
        'blanket_squirm': admin.HORIZONTAL,
    }

    def get_readonly_fields(self, request, obj=None):
        return (super().get_readonly_fields(request, obj=obj) + audit_fields +
                ('child_age',))
