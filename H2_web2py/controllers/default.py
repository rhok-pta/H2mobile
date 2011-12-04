# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

import couchdb

@auth.requires_login()
def getDb():
    couch = couchdb.Server("http://41.79.111.110:5984/")
    db = couch['h2mobile']
    return db

@auth.requires_login()
def getDocs(viewname, **options):
    db = getDb() 
    docs = [doc for doc in db.view(viewname,**options)]
    return docs

@auth.requires_login()
def getDocsByMap(map_fun):
    db = getDb()
    docs = [doc for doc in db.query(map_fun)]
    return docs

@auth.requires_login()
def index():
    return dict()

@auth.requires_login()
def renderDocs(docs,fields,caption={}):
    r = "<tr>"+"\n".join(["<th>"+caption.get(f,f).title()+"</th>" for f in fields]) + "</tr>"
    
    for d in docs:
        r+="<tr>"+"\n".join(["<td>"+str(d.value[f]) +"</td>" for f in fields])+"</tr>"
    return XML(r)

@auth.requires_login()
def renderCSV(docs,fields,caption={}):
    r = "<tr><th>"+",".join([caption.get(f,f).title() for f in fields]) + "</th></tr>"
    
    for d in docs:
        r+="<tr><td>"+",".join([str(d.value[f]) for f in fields])+"</td></tr>"
    return XML(r)                

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs bust be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())

@auth.requires_login()
def meterreadingform():
    form=FORM(TABLE(TR("Start date:",INPUT(_type="text",_name="startdate",value=request.vars.get('startdate','2011-01-01'))),
                    TR("End date:",INPUT(_type="text",_name="enddate",value=request.vars.get('enddate','2012-01-01'))),
                    TR("Meter Number:",INPUT(_type="text",_name="meterno",value=request.vars.get('meterno','*'))),
                    TR("As CSV:",INPUT(_type="checkbox",_name="csv",value=request.vars.get('csv',False))),
                    TR("",INPUT(_type="submit",_value="SUBMIT"))))
    if form.accepts(request,session):
        response.flash="form accepted"
        meternofilter = ""
        if(request.vars.get('meterno','*') != "*"): meternofilter =  " && doc.meterno=='" +request.vars.get('meterno','*')+ "'"
        map_fun = '''function(doc) {
                       if (doc.type == 'meterreading' %s && doc.readingdate>='%s' && doc.readingdate<='%s'){
                         emit([doc.readingdate, doc.meterno], doc);
                      }
                  }''' % (meternofilter,request.vars['startdate'],request.vars['enddate'])
        if(request.vars.get('csv',False)): 
            form =XML(form) + XML( "<table class='imagetable'>"+(renderCSV(getDocsByMap(map_fun),["meterno","meterreading","readingdate"]))+"</table>")
        else:
            form =XML(form) + XML( "<table class='imagetable'>"+(renderDocs(getDocsByMap(map_fun),["meterno","meterreading","readingdate"]))+"</table>")

    elif form.errors:
        response.flash="form is invalid"
    else:
        response.flash="please fill the form"
    return dict(form=XML(form))


@auth.requires_login()
def meteruserform():
    meternofilter = ""
    userfilter = ""

    form=FORM(TABLE(TR("Reader:",INPUT(_type="text",_name="reader",value=request.vars.get('reader','*'))),
                    TR("Meter Number:",INPUT(_type="text",_name="meterno",value=request.vars.get('meterno','*'))),
                    TR("As CSV:",INPUT(_type="checkbox",_name="csv",value=request.vars.get('csv',False))),
                    TR("",INPUT(_type="submit",_value="SUBMIT"))))

    if form.accepts(request,session):
        response.flash="form accepted"
        if(request.vars.get('reader','*')!='*'): userfilter=" && doc.username=='" + request.vars['reader']+"'"
        if(request.vars.get('meterno','*')!='*'): userfilter=" && doc.meterno=='" + request.vars['meterno']+"'"

        map_fun = '''function(doc) {
                       if (doc.type == 'meteruser' %s %s){
                         emit([doc.username,doc.meterno], doc);
                      }
                  }''' % (meternofilter, userfilter)
        if(request.vars.get('csv',False)): 
            form =XML(form) + XML( "<table class='imagetable'>"+(renderCSV(getDocsByMap(map_fun),["username","meterno"]))+"</table>")
        else:
            form =XML(form) + XML( "<table class='imagetable'>"+(renderDocs(getDocsByMap(map_fun),["username","meterno"]))+"</table>")

    elif form.errors:
        response.flash="form is invalid"
    else:
        response.flash="please fill the form"
    return dict(form=XML(form))



@auth.requires_login()
def areasform():
    defarea = ""
    if request.vars.get('action','') == '':
        if(request.vars.get('area','')!=''):
            response.flash="form accepted"
            areas = getDocs('usertap/taparea', key=request.vars['area'])
            if(len(areas) != 0):
                response.flash="Duplicate area"    
            else: 
                doc = {'areaname':request.vars['area'], 'type':'taparea'}
                getDb().create(doc)
                response.flash="Area added"    
    else: 
       response.flash="Area deleted" 
       areas = getDocs('usertap/taparea', key=request.vars['areaname'])
       for a in areas:
            getDb().delete(a.value)       
       defarea = request.vars['areaname']
           
    form=FORM(TABLE(TR("Area:",INPUT(_type="text",_name="area",value=defarea)),
                    TR("",INPUT(_type="submit",_value="Add"))))
       
    docs =getDocs("usertap/taparea")
    
    r = "<tr><th>Area Name</th><th>Action</th></tr>"
    for d in docs:
        r+="<tr><td>"+str(d.value['areaname']) +"</td><td>"+str(FORM(INPUT(_type="hidden",_name="areaname", _value=str(d.value['areaname'])),INPUT(_type="hidden",_name="action", _value="delete"),INPUT(_type="submit",_value="Delete"))) + "</td></tr>"
    form =  XML( "<table class='imagetable'>"+(XML(r))+"</table>") +BR()+ XML(form)

    return dict(form=XML(form))



@auth.requires_login()
def monitorform():
    defmonitor = ""
    if request.vars.get('action','') == '':
        if(request.vars.get('monitor','')!=''):
            response.flash="form accepted"
            monitors = getDocs('usertap/tapmonitor', key=request.vars['monitor'])
            if(len(monitors) != 0):
                response.flash="Duplicate monitor"    
            else: 
                doc = {'username':request.vars['monitor'], 'type':'tapmonitor'}
                getDb().create(doc)
                response.flash="Monitor added"    
    else: 
       response.flash="Monitor deleted" 
       areas = getDocs('usertap/tapmonitor', key=request.vars['monitor'])
       for a in areas:
            getDb().delete(a.value)       
       defmonitor = request.vars['monitor']
           
    form=FORM(TABLE(TR("Monitor:",INPUT(_type="text",_name="monitor",value=defmonitor)),
                    TR("",INPUT(_type="submit",_value="Add"))))
       
    docs =getDocs("usertap/tapmonitor")
    
    r = "<tr><th>Monitor Name</th><th>Action</th></tr>"
    for d in docs:
        r+="<tr><td>"+str(d.value['username']) +"</td><td>"+str(FORM(INPUT(_type="hidden",_name="monitor", _value=str(d.value['username'])),INPUT(_type="hidden",_name="action", _value="delete"),INPUT(_type="submit",_value="Delete"))) + "</td></tr>"
    form =  XML( "<table class='imagetable'>"+(XML(r))+"</table>") +BR()+ XML(form)

    return dict(form=XML(form))


@auth.requires_login()
def tapmonitorform():
    defmonitor = ""
    defarea = ""
    deftap ="" 
    key=request.vars.get('monitor','')+","+request.vars.get('area','')+","+request.vars.get('tap','')
    if request.vars.get('action','') == '':
        if(request.vars.get('monitor','')!=''):
            response.flash="form accepted"
            monitors = getDocs('usertap/usertapbykey', key=key)
            if(len(monitors) != 0):
                response.flash="Duplicate record"    
            else: 
                doc = {'username':request.vars['monitor'], 'type':'usertap', 'area':request.vars['area'], 'tapid':request.vars['tap']}
                getDb().create(doc)
                response.flash="Record added"    
    else: 
       response.flash="Record deleted" 
       records = getDocs('usertap/usertapbykey', key=key)
       for a in records:
            getDb().delete(a.value)       
       defmonitor = request.vars['monitor']
       defarea = request.vars['area']
       deftap = request.vars['tap']
           
    monitors = [d.value['username'] for d in getDocs('usertap/tapmonitor')]
    areas = [d.value['areaname'] for d in getDocs('usertap/taparea')]
    
    form=FORM(TABLE(TR("Monitor:",SELECT(monitors,_name="monitor",value=defmonitor)),
                    TR("Area:",SELECT(areas,_name="area",value=defmonitor)),
                    TR("Tap:",INPUT(_type="text",_name="tap",value=deftap)),
                    TR("",INPUT(_type="submit",_value="Add"))))
       
    docs =getDocs("usertap/usertapbykey")
    
    r = "<tr><th>Monitor Name</th><th>Area</th><th>Tap</th><th>Action</th></tr>"
    for d in docs:
        r+="<tr>"+"<td>"+str(d.value['username']) +"</td>"
        r+="<td>"+str(d.value['area']) +"</td>"
        r+="<td>"+str(d.value['tapid']) +"</td>"
        r+="<td>"+str(FORM(INPUT(_type="hidden",_name="monitor", _value=d.value['username']),
                     INPUT(_type="hidden",_name="area", _value=d.value['area']),
                     INPUT(_type="hidden",_name="tap", _value=d.value['tapid']),
                     INPUT(_type="hidden",_name="action", _value="delete"),
                     INPUT(_type="submit",_value="Delete"))) + "</td></tr>"
    form =  XML( "<table class='imagetable'>"+(XML(r))+"</table>") +BR()+ XML(form)

    return dict(form=XML(form))


@auth.requires_login()
def problemstatusform():
    monitors = [d.value['username'] for d in getDocs('usertap/tapmonitor')]
    monitors.append('*')
    areas = [d.value['areaname'] for d in getDocs('usertap/taparea')]
    areas.append('*')
    status = ['pending','resolved','*']

    form=FORM(INPUT(_type="hidden",_name='action',_value="show"),
        TABLE(TR("Start date:",INPUT(_type="text",_name="startdate",value=request.vars.get('startdate','2011-01-01'))),
        TR("End date:",INPUT(_type="text",_name="enddate",value=request.vars.get('enddate','2012-01-01'))),
        TR("Monitor:",SELECT(monitors,_name="monitor",value=request.vars.get("monitor","*"))),
        TR("Area:",SELECT(areas,_name="areaf",value=request.vars.get("areaf","*"))),
        TR("Status:",SELECT(status,_name="statusf",value=request.vars.get("statusf","*"))),
        TR("As CSV:",INPUT(_type="checkbox",_name="csv",value=request.vars.get('csv',False))),
        TR("",INPUT(_type="submit",_value="SUBMIT"))))

    # Updates the document
    if request.vars.get('action','') == 'updateandshow':
       if request.vars.get('cancel','') == '':
           db = getDb()
           doc = db.get(request.vars['doc_id'])
           doc['status'] = request.vars['status']
           doc['comments'] = request.vars['comments']
           db[request.vars['doc_id']] = doc
           response.flash="Updated"
       else:
           response.flash="Edit cancelled "


    # Shows the captured status
    if request.vars.get('action','') in ('show','updateandshow'):
        monitorfilter = ""
        if(request.vars.get('monitor','*') != "*"): monitorfilter =  " && doc.username=='" +request.vars.get('monitor','*')+ "'"
        areafilter = ""
        if(request.vars.get('areaf','*') != "*"): areafilter =  " && doc.area=='" +request.vars.get('areaf','*')+ "'"
        statusfilter = ""
        if(request.vars.get('statusf','*') != "*"): statusfilter =  " && doc.status=='" +request.vars.get('statusf','*')+ "'"

        map_fun = '''function(doc) {
                       if (doc.type == 'problem' %s %s %s && doc.reportdate>='%s' && doc.reportdate<='%s'){
                         emit([doc.status, doc.reportdate, doc.area,doc.username,doc.tapid], doc);
                      }
                  }''' % (monitorfilter,areafilter,statusfilter,request.vars['startdate'],request.vars['enddate'])
        if(request.vars.get('csv',False)): 
            form =XML(form) + XML( "<table class='imagetable'>"+(renderCSV(getDocsByMap(map_fun),["status","reportdate","area","username","tapid","problem","comments"]))+"</table>")
        else:
            docs = getDocsByMap(map_fun)
            fields = ["status","reportdate","area","username","tapid","problem","comments"] 
            caption = {'tapid':'tap','username':'monitor'}
            r = "<tr>"+"\n".join(["<th>"+caption.get(f,f).title()+"</th>" for f in fields]) +"<th>Action</th>"+ "</tr>"
            for d in docs:
                r+="<tr>"+"\n".join(["<td>"+str(d.value[f]) +"</td>" for f in fields])
                r+="<td>"+str(FORM(INPUT(_type="submit",_value="Update"),
                                  INPUT(_type="hidden",_name='action',_value="update"),
                                  XML("".join(["<input type='hidden' name='%s' value=\"%s\"/>" % (f,d.value[f]) for f in d.value])),
                                  XML("<input type='hidden' name='doc_id' value=\"%s\"/>" % d.value['_id']),
                                  XML("".join(["<input type='hidden' name='%s' value=\"%s\"/>" % (k,request.vars[k]) for k in request.vars.keys() if k in ('startdate','enddate','monitor','areaf','statusf')]))))
                r+="</td></tr>"
            form =XML(form) + BR() + XML( "<table class='imagetable'>"+(XML(r))+"</table>")
    #show the update screen
    elif request.vars.get('action','')=='update':
        form=FORM(INPUT(_type="hidden",_name='action',_value="updateandshow"),
                  INPUT(_type="hidden",_name='startdate',_value=request.vars['startdate']),
                  INPUT(_type="hidden",_name='enddate',_value=request.vars['enddate']), 
                  INPUT(_type="hidden",_name='monitor',_value=request.vars['monitor']), 
                  INPUT(_type="hidden",_name='areaf',_value=request.vars['areaf']), 
                  INPUT(_type="hidden",_name='statusf',_value=request.vars['statusf']), 
                  INPUT(_type="hidden",_name='doc_id',_value=request.vars['doc_id']), 
                  TABLE(TR("Reported:",request.vars['reportdate']),
                        TR("Area:",request.vars['area']),
                        TR("Monitor:",request.vars['username']),
                        TR("Tap:",request.vars['tapid']),
                        TR("Problem:",request.vars['problem']),
                        TR("Status:",SELECT('pending','resolved', _name='status',value=request.vars['status'])),
                        TR("Comments:",TEXTAREA(_type='textarea',_name='comments',value=request.vars['comments'])),
                        TR(INPUT(_type="submit",_name="cancel",_value="Cancel"),INPUT(_type="submit",_value="Update"))))


    return dict(form=XML(form))


