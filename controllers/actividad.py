# coding: utf8
# try something like


def tipos():
    #sql = "SELECT TIPO_ACTIVIDAD.nombre, CAMPO.nombre "
    #sql = sql + "FROM TIPO_ACTIVIDAD inner join CAMPO on TIPO_ACTIVIDAD.id = CAMPO.id_tipo_actividad;"
    rows = db(db.tipo_actividad).select()
    #rows = db.executesql(sql)
    return locals()

def agregar():
    tipo = int(request.args(0))
    rows = db(db.act_posee_campo.id_tipo_act == tipo).select()
    fields = []
    for row in rows:
        #print(row.id_campo)
        nombre = db(db.campo.id == row.id_campo).select().first().nombre
        nombre = nombre.replace(" ", "_")

        fields.append(Field(nombre,'string'))
        #fields.append(Field(nombre,requires=IS_NOT_EMPTY()))

    form=SQLFORM.factory(*fields)
    if form.process().accepted:
        id_act = db.actividad.insert(id_tipo = tipo)
        print(id_act)
        for var in form.vars:
            print(var)
            campo = var.replace("_"," ")
            id_cam = db(db.campo.nombre==campo).select().first().id
            print(id_cam)
            valor = getattr(form.vars ,var)
            db.tiene_campo.insert(id_actividad=id_act,id_campo=id_cam,valor_campo= valor)
            #print()


    return locals()

def register():
    form=SQLFORM.factory(db.client,db.address)
    if form.process().accepted:
        id = db.client.insert(**db.client._filter_fields(form.vars))
        form.vars.client=id
        id = db.address.insert(**db.address._filter_fields(form.vars))
        response.flash='Thanks for filling the form'
    return dict(form=form)

def procesar():
    pass

'''
row=db((db.people.name==request.args(0))& 
               (db.people.company_id==db.company.id)).select().first()
people_name=row.people.name
company_name=row.company.name

people_and_their_companies=db(db.people.company_id==db.company.id)
row=people_and_their_companies(db.people.name==request.args (0)).select().first()

SQLFORM(table, record=None,
       deletable=False,
       linkto=None,
       upload=None,
       fields=None,
       labels=None,
       col3={}, submit_button='Submit',
       delete_label='Check to delete:',
       showid=True,
       readonly=False,
       comments=True,
       keepopts=[],
       ignore_rw=False,
       record_id=None,
       formstyle='table3cols',
       buttons=['submit'],
       separator=': ',
       **attributes)
fields = ['name']
'''
