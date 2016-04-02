# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms


class ImportCSVForm(forms.Form):
    csv_file = forms.FileField(label='CSV file')
