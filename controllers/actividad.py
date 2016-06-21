# coding: utf8
# try something like

from pprint import pprint

def gestionar():
#    if session.usuario != None:
#        if session.usuario["tipo"] == "DEX" or session.usuario["tipo"] == "Administrador":
#            if(session.usuario["tipo"] == "DEX"):
#                admin = 2
#            elif(session.usuario["tipo"] == "Administrador"):
#                admin = 1
#            else:
#                admin = 0
#        else:
#            redirect(URL(c ="actividad",f="gestionar"))
#    else:
#        redirect(URL(c ="default",f="index"))

    rows = db(db.ACTIVIDAD.ci_usuario_crea==session.usuario['cedula']).select()
    detalles = {}

    for row in rows:
        dict_campos = dict()
        campos = db((db.TIENE_CAMPO.id_campo == db.CAMPO.id_campo)
                    & (db.TIENE_CAMPO.id_actividad == row.id_actividad)).select()

        for campo in campos:
            dict_campos[campo.CAMPO.nombre] = campo.TIENE_CAMPO.valor_campo

        detalles[row] = dict_campos

    return locals()

def tipos():
#    if session.usuario != None:
#        if session.usuario["tipo"] == "DEX" or session.usuario["tipo"] == "Administrador":
#            if(session.usuario["tipo"] == "DEX"):
#                admin = 2
#            elif(session.usuario["tipo"] == "Administrador"):
#                admin = 1
#            else:
#                admin = 0
#        else:
#            redirect(URL(c ="actividad",f="gestionar"))
#    else:
#        redirect(URL(c ="default",f="index"))

    rows = db(db.TIPO_ACTIVIDAD.papelera=='False').select()
    return locals()

def agregar():
#    if session.usuario != None:
#        if session.usuario["tipo"] == "DEX" or session.usuario["tipo"] == "Administrador":
#            if(session.usuario["tipo"] == "DEX"):
#                admin = 2
#            elif(session.usuario["tipo"] == "Administrador"):
#                admin = 1
#            else:
#                admin = 0
#        else:
#            redirect(URL(c ="actividad",f="gestionar"))
#    else:
#        redirect(URL(c ="default",f="index"))

    tipo = int(request.args(0))
    rows = db(db.ACT_POSEE_CAMPO.id_tipo_act == tipo).select()
    nombre_tipo = db(db.TIPO_ACTIVIDAD.id_tipo == tipo).select().first().nombre
    fields = []
    for row in rows:
        rows_campo = db(db.CAMPO.id_campo == row.id_campo).select().first()
        nombre = rows_campo.nombre
        nombre = nombre.replace(" ", "_")
        obligatorio = rows_campo.obligatorio

        if obligatorio:
            fields.append(Field(nombre,'string',requires=IS_NOT_EMPTY()))
        else:
            fields.append(Field(nombre,'string'))


    form=SQLFORM.factory(*fields)

    if form.process().accepted:
        dicc_act = db.ACTIVIDAD.insert(id_tipo = tipo,ci_usuario_crea= session.usuario['cedula'])
        id_act = dicc_act['id_actividad']
        for var in form.vars:
            campo = var.replace("_"," ")
            id_cam = db(db.CAMPO.nombre==campo).select().first().id_campo
            valor = getattr(form.vars ,var)
            db.TIENE_CAMPO.insert(id_actividad=id_act,id_campo=id_cam,valor_campo= valor)
        redirect(URL('gestionar'))
    elif form.errors:
        response.flash = 'el formulario tiene errores'

    return locals()

def modificar():
#    if session.usuario != None:
#        if session.usuario["tipo"] == "DEX" or session.usuario["tipo"] == "Administrador":
#            if(session.usuario["tipo"] == "DEX"):
#                admin = 2
#            elif(session.usuario["tipo"] == "Administrador"):
#                admin = 1
#            else:
#                admin = 0
#        else:
#            redirect(URL(c ="actividad",f="gestionar"))
#    else:
#        redirect(URL(c ="default",f="index"))

    id_act = int(request.args(0))
    rows = db(db.TIENE_CAMPO.id_actividad == id_act).select()
    fields = []
    valores = []
    for row in rows:
        rows_campo = db(db.CAMPO.id_campo == row.id_campo).select().first()
        nombre = rows_campo.nombre
        nombre = nombre.replace(" ", "_")
        obligatorio = rows_campo.obligatorio

        if obligatorio:
            fields.append(Field(nombre,'string',requires=IS_NOT_EMPTY()))
        else:
            fields.append(Field(nombre,'string'))

        valores.append([nombre,row.valor_campo])

    form=SQLFORM.factory(*fields)

    for i in range(len(valores)):
        setattr(form.vars, valores[i][0], valores[i][1])

    if form.process().accepted:

        for var in form.vars:
            campo = var.replace("_"," ")
            id_cam = db(db.CAMPO.nombre==campo).select().first().id_campo
            valor = getattr(form.vars ,var)

            sql = "UPDATE TIENE_CAMPO SET valor_campo = '" + valor
            sql = sql + "' WHERE id_actividad = '" + str(id_act) + "' AND id_campo = '" + str(id_cam) + "';"
            db.executesql(sql)

            update_act = "UPDATE ACTIVIDAD SET ci_usuario_modifica = '" + str(session.usuario['cedula'])
            update_act = update_act + "' WHERE id_actividad = '" + str(id_act) + "';"
            db.executesql(update_act)

        redirect(URL('gestionar'))

    return locals()


def eliminar():
    id_act = int(request.args(0))

    set_tiene_campo = db(db.TIENE_CAMPO.id_actividad == id_act)
    set_tiene_campo.delete()
    actividad = db(db.ACTIVIDAD.id_actividad == id_act)
    actividad.delete()

    redirect(URL('gestionar'))

    #return "Actividad {} eliminada".format(actividad)
    return locals()
