# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.title = request.application
response.subtitle = T('customize me!')

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Your Name <you@example.com>'
response.meta.description = 'a cool new app'
response.meta.keywords = 'web2py, python, framework'
response.meta.generator = 'Web2py Web Framework'
response.meta.copyright = 'Copyright 2011'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

response.menu = [
    (T('H2read'), True, URL('default','index'), [(T('Records Captured'), True, URL('default','meterreadingform')),(T('Meter Reader'), True, URL('default','meteruserform'))]),
    (T('H2flow'), False, URL('default','index'), [(T('Captured Tap Status'), True, URL('default','problemstatusform')),(T('Tap Monitor'), True, URL('default','tapmonitorform')),(T('Areas'), True, URL('default','areasform')),(T('Monitors'), True, URL('default','monitorform'))])
    ]
