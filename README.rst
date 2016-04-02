===================
Inline csv importer
===================

Inline csv importer is a simple Django app to import csv data in admin inlines.

Quick start
-----------

1. Add ``inline_csv_importer`` to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'inline_csv_importer',
    ]

2. Include the mixin in your ``ModelAdmin`` class and define ``csv_inline``::


    class AwardAdmin(UploadCSVAdminMixin, admin.ModelAdmin):
        csv_inline = (
            (
                'Person import', {
                    'fields': ('date', 'name', 'extra',),
                    'inline': AwardPersonInline,
                    'help_text': (
                        'CSV File should be in this format without headings: '
                        '<br> name, date, extra information.'
                    )
                }
            ),
        )

