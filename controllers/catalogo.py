# -*- coding: utf-8 -*-
# try something like
def vGestionarCatalogo():
    if session.usuario != None:
        if session.usuario["tipo"] == "DEX" or session.usuario["tipo"] == "Administrador":
            if(session.usuario["tipo"] == "DEX"):
                admin = 2
            elif(session.usuario["tipo"] == "Administrador"):
                admin = 1
            else:
                admin = 0
        else:
            redirect(URL(c ="default",f="vMenuPrincipal"))
    else:
        redirect(URL(c ="default",f="index"))
    forma=SQLFORM(                              # Se hace un formulario para introducir un nombre.
        db.CATALOGO,
        button=['Agregar'],
        fields=['nombre'],
        submit_button='Agregar',
        labels={'nombre':'Nombre'})
    if forma.accepts(request.vars, session):
        session.catAgregar = request.vars.nombre
        redirect(URL('vAgregarCampos.html'))
    # En caso de que el formulario no sea aceptado
    elif forma.errors:
        session.message = 'Error en el formulario'
    # Metodo GET
    else:
        session.message = ''
    aux = db(db.CATALOGO).select(db.CATALOGO.nombre)
    return dict(forma=forma, admin = admin, catalogos = aux, message = session.message)

def vAgregarCampos():
    print("EPALE")
    if session.usuario != None:
        if session.usuario["tipo"] == "DEX" or session.usuario["tipo"] == "Administrador":
            if(session.usuario["tipo"] == "DEX"):
                admin = 2
            elif(session.usuario["tipo"] == "Administrador"):
                admin = 1
            else:
                admin = 0
        else:
            redirect(URL(c ="default",f="vMenuPrincipal"))
    else:
        redirect(URL(c ="default",f="index"))
    # Obtengo el nombre del tipo_actividad desde el objeto global 'session'
    nombreCat = session.catAgregar
    
    # Creo query para realizar busqueda de los campos que ya han sido agregados
    # a ese tipo actividad
    query = reduce(lambda a, b: (a&b),[db.CATALOGO.nombre == nombreCat,
                                      db.CATALOGO.id_catalogo == db.CATALOGO_TIENE_CAMPO.id_catalogo,
                                      db.CATALOGO_TIENE_CAMPO.id_campo_cat == db.CAMPO_CATALOGO.id_campo_cat])
    # Guardo los resultados de dicho query en 'campos_guardados'
    campos_guardados = db(query).select(db.CAMPO_CATALOGO.ALL, db.CATALOGO_TIENE_CAMPO.ALL)
    print(nombreCat)
    # Busco el id del tipo_actividad
    id_cat = db(db.CATALOGO.nombre == nombreCat).select()[0].id_catalogo

    # Genero formulario para los campos
    form = SQLFORM(db.CAMPO_CATALOGO,
                   submit_button='Agregar',
                   fields = ['nombre', 'tipo_cat', 'eliminar'],
                   labels = {'tipo_cat' : 'Tipo'}
                   )
    # Metodos POST
    # En caso de que los datos del formulario sean aceptados
    if form.accepts(request.vars, session):
        # Busco el id del campo(que fue agregado al presionar boton
        # de submit) y agrego el objeto de tipo ACT_POSEE_CAMPO a la base
        # (es la relacion entre el campo y el tipo)
        print("PASO POR ACA")
        idd_campo = db(db.CAMPO_CATALOGO.nombre == request.vars.nombre).select(db.CAMPO_CATALOGO.id_campo_cat)[0].id_campo_cat
        db.CATALOGO_TIENE_CAMPO.insert(id_catalogo = id_cat, id_campo_cat = idd_campo)
        # Redirijo a la misma pagina para seguir agregando campos
        redirect(URL('vAgregarCampos.html'))
    # En caso de que el formulario no sea aceptado
    elif form.errors:
        session.message = 'Datos invalidos'
    # Metodo GET
    else:
        session.message = ''

    return dict(form = form, campos_guardados = campos_guardados,admin = admin)



'''
Metodo auxiliar usado para agregar el mensaje de exito
al agregar un tipo actividad, solo guarda el mensaje y redirige a
la pagina de gestionar
'''
def agregarTipoAux():
    
    session.message = 'Tipo agregado exitosamente'
    redirect(URL('vGestionarCatalogo.html'))
    
    
'''
Metodo que aborta la creacion de un tipo_actividad en la vista de
agregar campos, no solo elimina los campos y las relaciones sino
que tambien elimina el tipo_actividad (que a este punto ya se
encuentra en la base)
'''
def eliminarCampos():
    # Obtengo el nombre del tipo_actividad
    if len(request.args)!=0:
        nombreCat = request.args[0]
    else:
        nombreCat = session.catAgregar

    # Construyo query para obtener la relacion entre los campos y el tipo
    # actividad que quiero eliminar
    query = reduce(lambda a, b: (a&b),[db.CATALOGO.nombre == nombreCat,
                                      db.CATALOGO.id_catalogo == db.CATALOGO_TIENE_CAMPO.id_catalogo,
                                      db.CATALOGO_TIENE_CAMPO.id_campo_cat == db.CAMPO_CATALOGO.id_campo_cat])
    # Guardo los resultados en 'aux'
    aux = db(query).select(db.CATALOGO_TIENE_CAMPO.ALL)

    # Borro las relaciones (en caso de que hayan)
    if(len(aux) > 0):
        db(db.CATALOGO_TIENE_CAMPO.id_catalogo == aux[0].id_catalogo).delete()

    # Borro los campos asociados a estas relaciones
    for row in aux:
        db(db.CAMPO_CATALOGO.id_campo_cat == row.id_campo_cat).delete()

    # Borro el tipo actiidad
    db(db.CATALOGO.nombre == nombreCat).delete()
    
    redirect(URL('vGestionarCatalogo.html'))
    
    
def vAgregarElementoCampo():
    if session.usuario != None:
        if session.usuario["tipo"] == "DEX" or session.usuario["tipo"] == "Administrador":
            if(session.usuario["tipo"] == "DEX"):
                admin = 2
            elif(session.usuario["tipo"] == "Administrador"):
                admin = 1
            else:
                admin = 0
        else:
            redirect(URL(c ="default",f="vMenuPrincipal"))
    else:
        redirect(URL(c ="default",f="index"))
    nombreCat = request.args[0]
    query = reduce(lambda a, b: (a&b),[db.CATALOGO.nombre == nombreCat,
                                      db.CATALOGO.id_catalogo == db.CATALOGO_TIENE_CAMPO.id_catalogo,
                                      db.CATALOGO_TIENE_CAMPO.id_campo_cat == db.CAMPO_CATALOGO.id_campo_cat])
    aux = db(query).select(db.CAMPO_CATALOGO.nombre)
    cmpo = []
    for raw in aux:
        print(raw)
    aux2 = db(query).select(db.CAMPO_CATALOGO.id_campo_cat)
    forma=SQLFORM(                              # Se hace un formulario para introducir un nombre.
        db.CATALOGO_CONTIENE_CAMPO,
        button=['Modificar'],
        fields=['valor'],
        submit_button='Agregar',
        labels={'valor':'Valor'})
    return (dict(forma = forma))

    
def vConsultarCatalogo():
    return response.render()
