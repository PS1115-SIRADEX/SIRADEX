# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------
import os
import re
from gluon.tools import Crud
def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    datosComp = []
    message=auth.settings.login_form.get_user()
    print message
    if message != None:
        imprimir1 = os.popen("ldapsearch -x -h ldap.usb.ve -b \"dc=usb,dc=ve\" uid="+ message.get('username') +" | grep '^givenName\|^personalId\|^sn\|^uid:\|^mail\|^studentId\|^career'")
        for line in imprimir1.readlines():
            line = line.split(':')
            datosComp.append(line[1])   
        #db.usuario.insert(ci=24242424,usbid=232323,telefono=1212,correo_alter = 'arty')
        usuarioActual = db(db.usuario.ci == datosComp[3]).select()
        print len(usuarioActual)
        if len(usuarioActual) == 1:
            for usuario in usuarioActual:
                print usuario.telefono
            redirect(URL('vMenuPrincipal'))
        else:
            db.usuario.insert(ci=datosComp[3],
				usbid=datosComp[0],
				nombres=datosComp[1],
				apellidos=datosComp[2],
				correo_inst=datosComp[4])
            print "Registro"
            usuarios = db(db.usuario).select()
            for raw in usuarios:
                print raw.nombres
            redirect(URL('vRegistroUsuario'))
        return dict(form = '')
    else:
	return dict(form = '')

def vRegistroUsuario():
    datosComp = []
    message=auth.settings.login_form.get_user()
    if message != None:
        imprimir1 = os.popen("ldapsearch -x -h ldap.usb.ve -b \"dc=usb,dc=ve\" uid="+ message.get('username') +" | grep '^givenName\|^personalId\|^sn\|^uid:\|^mail\|^studentId\|^career'")
        for line in imprimir1.readlines():
            line = line.split(':')
            datosComp.append(line[1])
        form = SQLFORM.factory(
            Field("USBID", default=datosComp[0],writable = False),
            Field('Nombres',default=datosComp[1],writable = False),
            Field('apellidos', default=datosComp[2],writable=False),
            readonly=True)
        usuarios = db(db.usuario).select()
        for raw in usuarios:
            if raw.ci == datosComp[3]:
                forma=SQLFORM(
                    db.usuario,
                    raw,
                    button=['Registrarse'],
                    fields=['telefono','correo_alter'],
                    submit_button='Registrarse',
                    labels={'telefono':'Teléfono', 'correo_alter':'Correo alternativo'})
                break
        if len(request.vars)!=0:
            nuevoTelefono = request.vars.telefono
            nuevoCorreoAlter = request.vars.correo_alter
            db(db.usuario.ci == datosComp[3]).update(telefono=nuevoTelefono, correo_alter=nuevoCorreoAlter)
            redirect(URL('vMenuPrincipal'))
    return dict(form1 = form, form = forma)

def vVerPerfil():
    datosComp = []
    message=auth.settings.login_form.get_user()
    if message != None:
        imprimir1 = os.popen("ldapsearch -x -h ldap.usb.ve -b \"dc=usb,dc=ve\" uid="+ message.get('username') +" | grep '^givenName\|^personalId\|^sn\|^uid:\|^mail\|^studentId\|^career'")
        for line in imprimir1.readlines():
            line = line.split(':')
            datosComp.append(line[1])
        tlf = None
        correo_a = None
        correo_i = None
        usuarios = db(db.usuario).select()
        for raw in usuarios:
            if raw.ci == datosComp[3]:
                tlf = raw.telefono
                correo_a = raw.correo_alter
                correo_i = raw.correo_inst
        form = SQLFORM.factory(
            Field("USBID", default=datosComp[0],writable = False),
            Field('Nombres',default=datosComp[1],writable = False),
            Field('apellidos', default=datosComp[2],writable=False),
            Field('Correo_Institucional', default=correo_i,writable=False),
            Field('Telefono', default=tlf,writable=False),
            Field('Correo_Alternativo', default=correo_a,writable=False),
            readonly=True)
    return dict(form1 = form)

def vMenuPrincipal(): 
    return response.render()

def vEditarPerfil():
    datosComp = []
    message=auth.settings.login_form.get_user()
    if message != None:
        imprimir1 = os.popen("ldapsearch -x -h ldap.usb.ve -b \"dc=usb,dc=ve\" uid="+ message.get('username') +" | grep '^givenName\|^personalId\|^sn\|^uid:\|^mail\|^studentId\|^career'")
        for line in imprimir1.readlines():
            line = line.split(':')
            datosComp.append(line[1])
        form = SQLFORM.factory(
            Field("USBID", default=datosComp[0],writable = False),
            Field('Nombres',default=datosComp[1],writable = False),
            Field('apellidos', default=datosComp[2],writable=False),
            readonly=True)
        usuarios = db(db.usuario).select()
        for raw in usuarios:
            if raw.ci == datosComp[3]:
                forma=SQLFORM(
                    db.usuario,
                    record=raw,
					button=['Actualizar'],
					fields=['telefono','correo_alter'],
					submit_button='Actualizar',
					labels={'telefono':'Teléfono', 'correo_alter':'Correo alternativo'})
		#if forma.acst.cepts(request.vars, session):
        if len(request.vars)!=0:
            nuevoTelefono = request.vars.telefono
            nuevoCorreoAlter = request.vars.correo_alter
            db(db.usuario.ci == datosComp[3]).update(telefono=nuevoTelefono, correo_alter=nuevoCorreoAlter)
            redirect(URL('vVerPerfil'))
		#break
                #elif forma.errors:
                #    print ("Error")
                #else:
    return dict(form1 = form, form = forma)

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
