from django.http import JsonResponse
from django.views import View
from django.apps import apps


class CallHistoryView(View):

    flourishcaregiver_label = "flourish_caregiver"

    def get(self, request, *args, **kwargs):

        sid = kwargs.get('subject_identifier')

        flourish_appts = self.get_appointments(sid)
        flourish_contacts = self.get_contact_entry(sid)

        appt_data = [{'appt_datetime': item.appt_datetime.strftime("%Y-%m-%d, %H:%M:%S"),
                      'appt_reason': item.appt_reason,
                      'appt_type': item.appt_type,
                      'source': 'flourish'} for item in flourish_appts]

        contact_entries = [{
            'report_datetime': item.report_datetime.strftime("%Y-%m-%d, %H:%M:%S"),
            'status': item.contact_success,
            'contact_type': item.contact_type,
            'outcome': item.contact_comment,
            'source': item.study_name} for item in flourish_contacts]

        data = {
            'appt': appt_data,
            'contact_entry': contact_entries,
        }

        return JsonResponse(data)

    def get_appointments(self, sid=None):
        flo_appt_model = apps.get_model('edc_appointment', 'appointment')

        flourish_appt_calls = flo_appt_model.objects.filter(
            subject_identifier=sid,
            appt_type="telephone",
            appt_status='new',
            appt_reason="scheduled").order_by('-appt_datetime')

        return flourish_appt_calls

    @property
    def contact_model(self):
        return apps.get_model(self.flourishcaregiver_label, "caregivercontact")

    def get_contact_entry(self, sid=None):
        contact_entry = self.contact_model.objects.filter(subject_identifier=sid,
                                                          contact_success='Yes').order_by('-report_datetime')

        return contact_entry
