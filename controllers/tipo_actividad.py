# -*- coding: utf-8 -*-
''' '''
'''
Vista de Gestionar Tipo Actividad, tiene las opciones:
- Agregar Tipo
- Eliminar Tipo
- Papelera (No funcional)
'''
def gestionar():
    # Obtengo datos de los tipo_actividades en base de datos para generar
    # tabla que los muestre
    ids = db(db.TIPO_ACTIVIDAD.id_tipo != None).select(db.TIPO_ACTIVIDAD.id_tipo)
    nombres = db(db.TIPO_ACTIVIDAD.id_tipo != None).select(db.TIPO_ACTIVIDAD.nombre)
    descripcion = db(db.TIPO_ACTIVIDAD.id_tipo != None).select(db.TIPO_ACTIVIDAD.descripcion)
    programas = db(db.TIPO_ACTIVIDAD.id_tipo != None).select(db.TIPO_ACTIVIDAD.programa)

    # Decido que mensaje se va a mostrar
    # v------- Esto no funciona, obviamente
    if(session.message not in ['Tipo Eliminado', 'Tipo agregado exitosamente']):
        session.message = ''
    
    return dict(ids=ids,nombres=nombres,descripcion=descripcion, programas = programas)

'''
Vista con el formulario para agregar un Tipo Actividad
'''
def agregar_tipo():
    # Configuro widgets para el formulario de Agregar Tipo Actividad
    db.TIPO_ACTIVIDAD.nombre.widget = SQLFORM.widgets.string.widget
    db.TIPO_ACTIVIDAD.tipo_p_r.widget = SQLFORM.widgets.radio.widget
    db.TIPO_ACTIVIDAD.descripcion.widget = SQLFORM.widgets.text.widget
    db.TIPO_ACTIVIDAD.programa.widget = SQLFORM.widgets.text.widget
    db.TIPO_ACTIVIDAD.producto.widget = SQLFORM.widgets.text.widget
    db.TIPO_ACTIVIDAD.nro_campos.widget = SQLFORM.widgets.integer.widget

    # Genero el formulario para el tipo_actividad
    formulario = SQLFORM(db.TIPO_ACTIVIDAD,
                         buttons=['submit'],
                         fields=[
                                 'nombre','tipo_p_r','descripcion','programa','producto'
                                ],
                         formatstyle="divs",
                         submit_button='Registrar Tipo Actividad'
                        )
  

    # Metodos POST
    # En caso de que los datos del formulario sean aceptados
    if formulario.accepts(request.vars, session):
        session.form_nombre = request.vars.nombre
        redirect(URL('agregar_tipo_campos.html'))
    # En caso de que el formulario no sea aceptado
    elif formulario.errors:
        session.message = 'Error en el formulario'
    # Metodo GET
    else:
        session.message = ''
        
    return dict(formulario=formulario)

'''
Vista con el formulario para agregar campos al tipo actividad,
tambien tiene una tabla con los campos que ya han sido agregados
'''
def agregar_tipo_campos():
    # Obtengo el nombre del tipo_actividad desde el objeto global 'session'
    nombre_tipo = session.form_nombre
    
    # Creo query para realizar busqueda de los campos que ya han sido agregados
    # a ese tipo actividad
    query = reduce(lambda a, b: (a&b),[db.TIPO_ACTIVIDAD.nombre == nombre_tipo,
                                      db.TIPO_ACTIVIDAD.id_tipo == db.ACT_POSEE_CAMPO.id_tipo_act,
                                      db.ACT_POSEE_CAMPO.id_campo == db.CAMPO.id_campo])
    # Guardo los resultados de dicho query en 'campos_guardados'
    campos_guardados = db(query).select(db.CAMPO.ALL, db.ACT_POSEE_CAMPO.ALL)

    # Busco el id del tipo_actividad
    id_tipo = db(db.TIPO_ACTIVIDAD.nombre == nombre_tipo).select(db.TIPO_ACTIVIDAD.id_tipo)[0].id_tipo

    # Genero formulario para los campos
    form = SQLFORM(db.CAMPO,
                   submit_button='Agregar',
                   fields = ['nombre', 'lista', 'obligatorio'],
                   labels = {'lista' : 'Tipo'}
                   )

    # Metodos POST
    # En caso de que los datos del formulario sean aceptados
    if form.accepts(request.vars, session):
        # Busco el id del campo(que fue agregado al presionar boton
        # de submit) y agrego el objeto de tipo ACT_POSEE_CAMPO a la base
        # (es la relacion entre el campo y el tipo)
        idd_campo = db(db.CAMPO.nombre == request.vars.nombre).select(db.CAMPO.id_campo)[0].id_campo
        db.ACT_POSEE_CAMPO.insert(id_tipo_act = id_tipo, id_campo = idd_campo)
        # Redirijo a la misma pagina para seguir agregando campos
        redirect(URL('agregar_tipo_campos.html'))
     # En caso de que el formulario no sea aceptado
    elif form.errors:
        session.message = 'Datos invalidos'
    # Metodo GET
    else:
        session.message = ''
    
    return dict(form = form, campos = campos_guardados)

'''
Metodo auxiliar usado para agregar el mensaje de exito
al agregar un tipo actividad, solo guarda el mensaje y redirige a
la pagina de gestionar
'''
def agregar_tipo_aux():
    session.message = 'Tipo agregado exitosamente'
    redirect(URL('gestionar.html'))

'''
Metodo que aborta la creacion de un tipo_actividad en la vista de
agregar campos, no solo elimina los campos y las relaciones sino
que tambien elimina el tipo_actividad (que a este punto ya se
encuentra en la base)
'''
def eliminar_campos():
    # Obtengo el nombre del tipo_actividad
    nombre_tipo = session.form_nombre

    # Construyo query para obtener la relacion entre los campos y el tipo
    # actividad que quiero eliminar
    query = reduce(lambda a, b: (a&b),[db.TIPO_ACTIVIDAD.nombre == nombre_tipo,
                                      db.TIPO_ACTIVIDAD.id_tipo == db.ACT_POSEE_CAMPO.id_tipo_act,
                                      db.ACT_POSEE_CAMPO.id_campo == db.CAMPO.id_campo])
    # Guardo los resultados en 'aux'
    aux = db(query).select(db.ACT_POSEE_CAMPO.ALL)

    # Borro las relaciones (en caso de que hayan)
    if(len(aux) > 0):
        db(db.ACT_POSEE_CAMPO.id_tipo_act == aux[0].id_tipo_act).delete()

    # Borro los campos asociados a estas relaciones
    for row in aux:
        db(db.CAMPO.id_campo == row.id_campo).delete()

    # Borro el tipo actiidad
    db(db.TIPO_ACTIVIDAD.nombre == nombre_tipo).delete()
    
    redirect(URL('gestionar.html'))

'''
Metodo que elimina un tipo actividad guardado en la base
'''
def eliminar_tipo():

    # Formulario para el nombre del tipo actividad
    form = FORM('Nombre del Tipo Actividad:', INPUT(_name='nombre', _class = 'field'), INPUT(_type='submit', _value ='Elimiar'))

    # Metodos POST
    # En caso de ser aceptado el formulario
    if form.accepts(request.vars, session):
        # Primero verifico que el tipo_actividad este en la base
        if (db(db.TIPO_ACTIVIDAD.nombre == request.vars.nombre).count() == 1):
            # Obtengo el nombre del mismo
            nombre_tipo = request.vars.nombre

            # Construyo query para buscar los campos y relaciones del tipo
            query = reduce(lambda a, b: (a&b),[db.TIPO_ACTIVIDAD.nombre == nombre_tipo,
                                      db.TIPO_ACTIVIDAD.id_tipo == db.ACT_POSEE_CAMPO.id_tipo_act,
                                      db.ACT_POSEE_CAMPO.id_campo == db.CAMPO.id_campo])

            # Guardo los reusltados en 'aux'
            aux = db(query).select(db.ACT_POSEE_CAMPO.ALL)

            # Borro las relaciones
            if(len(aux) > 0):
                db(db.ACT_POSEE_CAMPO.id_tipo_act == aux[0].id_tipo_act).delete()

            # Borro los campos
            for row in aux:
                db(db.CAMPO.id_campo == row.id_campo).delete()

            # Borro el tipo_activdad
            db(db.TIPO_ACTIVIDAD.nombre == nombre_tipo).delete()

            # Guardo mensaje de exito
            session.message = 'Tipo Eliminado'
            redirect(URL('gestionar.html'))
        else:
            # En caso de que no se enceuntre el tipo, guardo mensaje de error
            session.message = 'No se encontro un tipo con ese nombre'
    # En caso de no ser aceptado el formulario
    elif form.errors:
        session.message = 'Error en el formulario'
    # Metodo GET
    else:
        session.message = ''
        
    return dict(form = form)


def guardar_archivos():
    
    return True;
