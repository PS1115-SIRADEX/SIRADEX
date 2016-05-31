# coding: utf8
# try something like
def tipos(): 
    #sql = "SELECT TIPO_ACTIVIDAD.nombre, CAMPO.nombre "
    #sql = sql + "FROM TIPO_ACTIVIDAD inner join CAMPO on TIPO_ACTIVIDAD.id = CAMPO.id_tipo_actividad;"
    rows = db(db.tipo_actividad).select()
    #rows = db.executesql(sql)
    return locals()

def agregar():
    tipo = request.args(0)
    return locals()

def register():
    form=SQLFORM.factory(db.client,db.address)
    if form.process().accepted:
        id = db.client.insert(**db.client._filter_fields(form.vars))
        form.vars.client=id
        id = db.address.insert(**db.address._filter_fields(form.vars))
        response.flash='Thanks for filling the form'
    return dict(form=form)
