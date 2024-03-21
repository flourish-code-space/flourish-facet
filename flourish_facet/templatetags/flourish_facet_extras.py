from datetime import datetime
from urllib.parse import unquote, urlencode

from django import template
from django.conf import settings
from django.utils.safestring import mark_safe
from edc_base.utils import age, get_utcnow
from edc_visit_schedule.models import SubjectScheduleHistory
from dateutil.relativedelta import relativedelta

register = template.Library()


@register.filter
def get_item(dictionary, key):
    if dictionary is not None:

        return dictionary.get(key)


@register.inclusion_tag('flourish_facet/buttons/consent_button.html')
def consent_button(model_wrapper):

    return dict(
        title='title',
        model_wrapper=model_wrapper)


@register.inclusion_tag('flourish_facet/buttons/listboard_button.html')
def listboard_button(title, href, exists):

    return dict(
        href=href,
        title=title,
        exists=exists)


@register.inclusion_tag('flourish_facet/buttons/qualitative_scheduling_button.html')
def qualitative_scheduling_button(model_wrapper):
    title = ['Qualitative Interview Scheduling']
    return dict(
        add_qualitative_scheduling_href=model_wrapper.qualitative_interview_scheduling.href,
        subject_identifier=model_wrapper.object.subject_identifier,
        qualitative_interview_scheduling_model_obj=model_wrapper.qualitative_interview_scheduling_model_obj,
        title=' '.join(title),)


@register.inclusion_tag('flourish_facet/buttons/qualitative_audio_upload_button.html')
def qualitative_audio_button(model_wrapper):
    title = ['Qualitative Interview Audio Upload']
    return dict(
        add_qualitative_audio_upload_href=model_wrapper.qualitative_interview_audio_upload.href,
        subject_identifier=model_wrapper.object.subject_identifier,
        qualitative_interview_audio_upload_model_obj=model_wrapper.qualitative_interview_audio_upload_model_obj,
        title=' '.join(title),)


@register.inclusion_tag('flourish_facet/buttons/qualitative_transcription_translation_button.html')
def qualitative_translation_transcription_button(model_wrapper):
    title = ['Qualitative Interview T & T']
    return dict(
        add_qualitative_transcription_translation_href=model_wrapper.qualitative_interview_transcription_translation.href,
        subject_identifier=model_wrapper.object.subject_identifier,
        qualitative_interview_transcription_translation_model_obj=model_wrapper.qualitative_interview_transcription_translation_model_obj,
        title=' '.join(title),)


@register.inclusion_tag('flourish_facet/buttons/edit_interview_button.html')
def edit_interview_button(model_wrapper):
    title = ['Edit Focus Group Interview form.']
    return dict(
        group_identifier=model_wrapper.object.group_identifier,
        href=model_wrapper.href,
        title=' '.join(title))


@register.inclusion_tag('flourish_facet/buttons/focus_group_transcription_translation_button.html')
def focus_group_translation_transcription_button(model_wrapper):
    title = ['Focus Group Interview T & T']
    return dict(
        add_focus_group_transcription_translation_href=model_wrapper.focus_group_interview_transcription_translation.href,
        group_identifier=model_wrapper.object.group_identifier,
        focus_group_interview_transcription_translation_model_obj=model_wrapper.focus_group_interview_transcription_translation_model_obj,
        title=' '.join(title),)


@register.inclusion_tag('flourish_facet/buttons/facet_contact_button.html')
def facet_contact_button(model_wrapper):
    title = ['Facet Contact.']
    return dict(
        subject_identifier=model_wrapper.object.subject_identifier,
        add_facetcontact_href=model_wrapper.facet_contact.href,
        title=' '.join(title),
    )
