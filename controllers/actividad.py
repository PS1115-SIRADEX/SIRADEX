# coding: utf8
# try something like
def index(): 
    #sql = "SELECT TIPO_ACTIVIDAD.nombre, CAMPO.nombre "
    #sql = sql + "FROM TIPO_ACTIVIDAD inner join CAMPO on TIPO_ACTIVIDAD.id = CAMPO.id_tipo_actividad;"
    rows = db(db.actividad).select()
    #rows = db.executesql(sql)
    return locals()

def tipos(): 
    #sql = "SELECT TIPO_ACTIVIDAD.nombre, CAMPO.nombre "
    #sql = sql + "FROM TIPO_ACTIVIDAD inner join CAMPO on TIPO_ACTIVIDAD.id = CAMPO.id_tipo_actividad;"
    rows = db(db.tipo_actividad).select()
    #rows = db.executesql(sql)
    return locals()

def agregar():
    id_tipo = int(request.args(0))

    rows = db(db.act_posee_campo.id_tipo_act == id_tipo).select()
    fields = []
    for row in rows:
        print(row.id_campo)
        nombre = db(db.campo.id == row.id_campo).select().first().nombre
        fields.append(nombre)

    form = FORM(Field)
    print(fields)
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
    a = reques.args()
    print(a)

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
