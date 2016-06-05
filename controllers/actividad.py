# coding: utf8
# try something like

def index(): 
    #sql = "SELECT TIPO_ACTIVIDAD.nombre, CAMPO.nombre "
    #sql = sql + "FROM TIPO_ACTIVIDAD inner join CAMPO on TIPO_ACTIVIDAD.id = CAMPO.id_tipo_actividad;"
    rows = db(db.actividad).select()
    #rows = db.executesql(sql)
    return locals()

def tipos():
    rows = db(db.tipo_actividad).select()
    return locals()

def agregar():
    tipo = int(request.args(0))
    rows = db(db.act_posee_campo.id_tipo_act == tipo).select()
    fields = []
    for row in rows:
        nombre = db(db.campo.id == row.id_campo).select().first().nombre
        nombre = nombre.replace(" ", "_")
        fields.append(Field(nombre,'string'))
        #fields.append(Field(nombre,requires=IS_NOT_EMPTY()))

    form=SQLFORM.factory(*fields)
    if form.process().accepted:
        id_act = db.actividad.insert(id_tipo = tipo)
        for var in form.vars:
            campo = var.replace("_"," ")
            id_cam = db(db.campo.nombre==campo).select().first().id
            valor = getattr(form.vars ,var)
            db.tiene_campo.insert(id_actividad=id_act,id_campo=id_cam,valor_campo= valor)
        redirect(URL('index'))

    return locals()

def modificar():
    id_act = int(request.args(0))
    rows = db(db.tiene_campo.id_actividad == id_act).select()
    fields = []
    valores = []
    for row in rows:
        nombre = db(db.campo.id == row.id_campo).select().first().nombre
        nombre = nombre.replace(" ", "_")
        fields.append(Field(nombre,'string'))
        valores.append([nombre,row.valor_campo])

    form=SQLFORM.factory(*fields)

    for i in range(len(valores)):
        setattr(form.vars, valores[i][0], valores[i][1])

    if form.process().accepted:

        for var in form.vars:
            campo = var.replace("_"," ")
            id_cam = db(db.campo.nombre==campo).select().first().id
            valor = getattr(form.vars ,var)
            row = db((db.tiene_campo.id_actividad==id_act) & (db.tiene_campo.id_campo==id_cam)).select().first()
            row.valor_campo = valor
            row.update_record()

        redirect(URL('index'))

    return locals()
