# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unicodecsv as csv

from django.conf.urls import url
from django.contrib import messages
from django.forms.forms import pretty_name
from django.forms.models import inlineformset_factory, modelform_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.html import format_html

from .forms import ImportCSVForm


class UploadCSVAdminMixin(object):
    change_form_template = 'admin/inline_csv_importer/change_form.html'

    def get_urls(self):
        urls = super(UploadCSVAdminMixin, self).get_urls()
        my_urls = [
            url(
                r'^(\d+)/import-inline-csv/$',
                self.import_inline_csv,
                name='import-inline-csv'
            ),
        ]
        return my_urls + urls

    def format_csv_inline(self):
        """ Outputs formatted csv_inline. """

        csv_inline = {}
        for line in self.csv_inline:
            csv_inline['name'] = self.csv_inline[0][0]
            csv_inline.update(self.csv_inline[0][1])
        return csv_inline

    def do_checks(self):
        """
        Do some checks to make sure that defined tupe or lists is in the right format.
        """
        message = None

        if not hasattr(self, 'csv_inline'):
            message = format_html(
                'Please define <b>csv_inline</b> if you want import from csv.'
            )
        elif not isinstance(self.csv_inline[0], (list, tuple)):
            message = format_html(
                '{}.csv_inline must be list or tuple.'.format(self.__class__.__name__)
            )
        elif len(self.csv_inline) > 1:
            message = format_html(
                '{}.csv_inline can\'t be more than one set.'.format(self.__class__.__name__)
            )
        elif not self.csv_inline[0][1].get('inline'):
            message = format_html(
                '{}.csv_inline please define <b>inline</b>.'.format(self.__class__.__name__)
            )
        return message

    def get_inline_model_form(self):
        """ Build model form for inline model. """

        return modelform_factory(
            model=self.pretty_csv_inline['inline'].model,
            fields=self.pretty_csv_inline['fields']
        )

    def build_formset(self, model_form, extra=0):
        """ Build formset. """

        formset = inlineformset_factory(
            parent_model=self.model,
            model=self.pretty_csv_inline['inline'].model,
            form=model_form,
            extra=extra,
        )
        return formset

    def import_inline_csv(self, request, obj_id):

        form = None
        formset = None
        initial_data = []
        headers = []

        # Do checks on defined csv_inline fieldset.
        message = self.do_checks()
        if message:
            messages.error(request, message)
            return HttpResponseRedirect('../')

        self.pretty_csv_inline = self.format_csv_inline()

        opts = {
            'verbose_name': self.model._meta.verbose_name,
            'verbose_name_plural': self.model._meta.verbose_name_plural,
            'app_label': self.model._meta.app_label,
            'object_name': self.model._meta.model_name,
        }

        confirmed = request.POST.get('confirmed', False)

        if request.method == 'POST':
            # Build inline formset.
            model_form = self.get_inline_model_form()

            if request.FILES.get('csv_file'):

                csv_file = request.FILES['csv_file']
                csv_file = csv.reader(csv_file)

                # Skip headers
                next(csv_file, None)

                # Make headers pretty.
                headers = map(pretty_name, self.pretty_csv_inline['fields'])

                for row in csv_file:

                    # Zip values from csv row to defined fields in csv_inline
                    zipped_data = dict(zip(self.pretty_csv_inline['fields'], row))

                    initial_data.append(zipped_data)

                # Build formset.
                formset = self.build_formset(model_form, extra=len(initial_data))
                formset = formset(initial=initial_data)

            else:
                formset = self.build_formset(model_form)
                formset = formset(request.POST)
                if formset.is_valid():
                    obj = self.get_object(request, obj_id)
                    formset.instance = obj
                    formset.save()
                    messages.success(request, 'Imported successfully.')
                    return HttpResponseRedirect('../')
        else:
            form = ImportCSVForm()
            if self.pretty_csv_inline.get('help_text'):
                form['csv_file'].help_text = self.pretty_csv_inline['help_text']

        return render_to_response(
            'admin/inline_csv_importer/inline_csv_importer.html',
            {
                'title': 'Import data',
                'root_path': 'admin',
                'app_label': opts['app_label'],
                'opts': opts,
                'form': form,
                'confirmed': confirmed,
                'formset': formset,
                'headers': headers,
                'initial_data': initial_data,
            },
            RequestContext(request)
        )
