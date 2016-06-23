# -*- coding: utf-8 -*-
# try something like

def get_tipo_usuario():
    if session.usuario != None:
        if session.usuario["tipo"] == "Bloqueado":
            redirect(URL(c = "default",f="index"))
        if session.usuario["tipo"] == "Administrador":
            if(session.usuario["tipo"] == "DEX"):
                admin = 2
            elif(session.usuario["tipo"] == "Administrador"):
                admin = 1
            elif(session.usuario["tipo"] == "Bloqueado"):      
                admin = -1
            else:
                admin = 0
        else:
            redirect(URL(c ="default",f="vMenuPrincipal"))
    else:
        redirect(URL(c ="default",f="index"))
        
    return admin

def vGestionarCatalogo():
    admin = get_tipo_usuario()
    session.nombreMostrar = ""
    session.nombreModificar = ""
    aux = db(db.CATALOGO).select(db.CATALOGO.nombre)
    return dict(admin = admin, catalogos = aux)

def vAgregarCatalogo():
    admin = get_tipo_usuario()
    forma=SQLFORM(                              # Se hace un formulario para introducir un nombre.
        db.CATALOGO,
        button=['Agregar'],
        fields=['nombre'],
        submit_button='Agregar',
        labels={'nombre':'Nombre'})
    if forma.accepts(request.vars, session):
        session.catAgregar = request.vars.nombre
        session.msgErr = 0
        redirect(URL('vAgregarCampos.html'))
    # En caso de que el formulario no sea aceptado
    elif forma.errors:
        session.message = 'Error en el formulario'
    # Metodo GET
    else:
        session.message = ''
    return(dict(forma = forma, admin = admin))
    
    
def vAgregarCampos():
    admin = get_tipo_usuario()
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
        idd_campo = db(db.CAMPO_CATALOGO.nombre == request.vars.nombre).select(db.CAMPO_CATALOGO.id_campo_cat)[0].id_campo_cat
        if len(db(db.CATALOGO_TIENE_CAMPO.id_campo_cat == idd_campo,db.CATALOGO_TIENE_CAMPO.id_catalogo == id_cat).select())>0:
            session.msgErr = 1
            session.message = 'Ya existe el campo'
        else:
            db.CATALOGO_TIENE_CAMPO.insert(id_catalogo = id_cat, id_campo_cat = idd_campo)
            session.msgErr = 0
        # Redirijo a la misma pagina para seguir agregando campos
        redirect(URL('vAgregarCampos'))
    # En caso de que el formulario no sea aceptado
    elif form.errors:
        session.message = 'Datos invalidos'
    # Metodo GET
    else:
        if(not(session.msgErr)):
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
    aux2 = db(db.CAMPO.despliega_cat == aux[0].id_catalogo).select()
    # Borro las relaciones (en caso de que hayan)
    if(len(aux) > 0):
        db(db.CATALOGO_TIENE_CAMPO.id_catalogo == aux[0].id_catalogo).delete()
        db(db.VALORES_CAMPO_CATALOGO.id_catalogo == aux[0].id_catalogo).delete()
        db(db.ACT_POSEE_CAMPO.id_campo == aux2[0]['id_campo']).delete()
        db(db.CAMPO.despliega_cat == aux[0].id_catalogo).delete()

    # Borro los campos asociados a estas relaciones
    for row in aux:
        db(db.CAMPO_CATALOGO.id_campo_cat == row.id_campo_cat).delete()

    # Borro el tipo actiidad
    db(db.CATALOGO.nombre == nombreCat).delete()
    
    redirect(URL('vGestionarCatalogo.html'))
    
    
def vAgregarElementoCampo():
    admin = get_tipo_usuario()
    nombreCat = request.args[0]
    print("nombre: ",nombreCat)
    query = reduce(lambda a, b: (a&b),[db.CATALOGO.nombre == nombreCat,
                                      db.CATALOGO.id_catalogo == db.CATALOGO_TIENE_CAMPO.id_catalogo,
                                      db.CATALOGO_TIENE_CAMPO.id_campo_cat == db.CAMPO_CATALOGO.id_campo_cat])
    aux = db(query).select(db.CAMPO_CATALOGO.nombre)
    cmpo = []
    ids = []
    # Nombres de los campos
    for raw in aux:
        cmpo.append(raw['nombre'])
    print("cmpo: ",cmpo)
    id_cat = db(db.CATALOGO.nombre == nombreCat).select(db.CATALOGO.id_catalogo)[0]['id_catalogo']
    arrId = db(query).select(db.CAMPO_CATALOGO.id_campo_cat)
    iterador = len(cmpo)
    # Ids
    for raw in arrId:
        ids.append(raw['id_campo_cat'])
    arreglo = []
    for i in cmpo:
        arreglo += [ Field(str(i),'string', label=T(str(i))) ]
    if(len(arreglo) > 0):
        forma = SQLFORM.factory(
            *arreglo)
    else:
        session.message = "El catalogo no posee campos"
        redirect(URL('vGestionarCatalogo.html'))
    
    if len(request.vars)>0:
        for i in range(0,iterador):
            valor = request.vars[str(cmpo[i])]
            print("valor: ",valor)
            query2 = reduce(lambda a, b: (a&b), [db.VALORES_CAMPO_CATALOGO.valor == valor, db.VALORES_CAMPO_CATALOGO.id_catalogo == id_cat,
                                                 db.VALORES_CAMPO_CATALOGO.id_campo_cat == ids[i]])
            if(len(db(query2).select()) > 0):
                session.nombreMostrar = nombreCat
                session.message = "El valor de un campo esta duplicado"
                redirect(URL('vMostrarCatalogo.html'))
        for i in range(0,iterador):
            valor = request.vars[str(cmpo[i])]
            print("valor: ",valor)
            db.VALORES_CAMPO_CATALOGO.insert(id_campo_cat = ids[i], id_catalogo = id_cat, valor = valor)
        session.nombreMostrar = nombreCat
        redirect(URL('vMostrarCatalogo.html'))

    return (dict(forma = forma))

    
def vConsultarCatalogo():
    return response.render()

def vMostrarCatalogo():
    admin = get_tipo_usuario()
    # Obtengo el nombre del tipo_actividad desde el objeto global 'session'
    if(session.nombreMostrar != ""):
        nombreCat = session.nombreMostrar
    else:
        nombreCat = request.args[0]
    
    # Creo query para realizar busqueda de los campos que ya han sido agregados
    # a ese tipo actividad
    query = reduce(lambda a, b: (a&b),[db.CATALOGO.nombre == nombreCat,
                                      db.CATALOGO.id_catalogo == db.CATALOGO_TIENE_CAMPO.id_catalogo,
                                      db.CATALOGO_TIENE_CAMPO.id_campo_cat == db.CAMPO_CATALOGO.id_campo_cat])
    query2 = reduce(lambda a, b: (a&b),[db.CATALOGO.nombre == nombreCat,
                                       db.VALORES_CAMPO_CATALOGO.id_campo_cat == db.CAMPO_CATALOGO.id_campo_cat,
                                       db.VALORES_CAMPO_CATALOGO.id_catalogo == db.CATALOGO.id_catalogo])
    # Guardo los resultados de dicho query en 'campos_guardados'
    campos_guardados = db(query).select(db.CAMPO_CATALOGO.ALL, db.CATALOGO_TIENE_CAMPO.ALL)
    id_campos = db(query).select(db.CATALOGO_TIENE_CAMPO.ALL)
    valores_campos = db(query2).select(db.VALORES_CAMPO_CATALOGO.ALL)
    nroCampos = len(campos_guardados)
    nroValores = len(valores_campos)
    print("campos:",nroCampos)
    print("valores:",nroValores)
    print("ids: ",id_campos)
    # En caso de que los datos del formulario sean aceptados
    if(nroCampos != 0):
        nroFilas = nroValores/nroCampos
    else:
        nroFilas = 0
    filas = []
    columnas = []
    print("Valores_Campos: ")
    print(valores_campos)
    j = 0
    for i in range(0,len(id_campos)):
        arr = []
        id_act = id_campos[i]['id_campo_cat']
        for j in range(0,len(valores_campos)):
            if(valores_campos[j]['id_campo_cat'] == id_act):
                arr.append(valores_campos[j])
        columnas.append(arr)
    print("Columnas",columnas)
    j = 0
    for i in range(0,nroFilas):
        aux = []
        for j in range(0,len(columnas)):
            aux.append(columnas[j][i])
        filas.insert(-1,aux)
    print("filas: ",filas)
    session.filas = filas
    return dict(campos_guardados = campos_guardados,filas = filas, admin = admin, nombre = nombreCat)


def vModificarCampos():
    admin = get_tipo_usuario()
    print("Argumentos: ",request.args)
    print("FILAS: ",session.filas)
    for j in session.filas[int(request.args[1])]:
        if j['valor']==request.args[0]:
            diccionario = j
            dcc = session.filas[int(request.args[1])]
    print(diccionario)
    print("DCC:",dcc)
    query = reduce(lambda a, b: (a&b),[db.CATALOGO.id_catalogo == diccionario['id_catalogo'],
                                      db.CATALOGO.id_catalogo == db.CATALOGO_TIENE_CAMPO.id_catalogo,
                                      db.CATALOGO_TIENE_CAMPO.id_campo_cat == db.CAMPO_CATALOGO.id_campo_cat])
    aux = db(query).select(db.CAMPO_CATALOGO.nombre)
    nombreCat = db(query).select(db.CATALOGO.nombre)[0]['nombre']
    print("NOMBREEEEEE: ",nombreCat)
    print(aux)
    cmpo = []
    ids = []
    # Nombres de los campos
    for raw in aux:
        cmpo.append(raw['nombre'])
        print(raw['nombre'])
    id_cat = db(db.CATALOGO.id_catalogo == diccionario['id_catalogo']).select(db.CATALOGO.id_catalogo)[0]['id_catalogo']
    print("CATALOGO")
    print(id_cat)
    arrId = db(query).select(db.CAMPO_CATALOGO.id_campo_cat)
    
    # Ids
    for raw in arrId:
        ids.append(raw['id_campo_cat'])
    print(ids[0])
    arreglo = []
    df =None
    for i in range(0,len(cmpo)):
        for f in dcc:
            if(f['id_campo_cat'] == ids[i]):
                df = f['valor']
        if df != None:
            arreglo += [ Field(str(cmpo[i]),'string',default= df, label=T(str(cmpo[i]))) ]
    forma = SQLFORM.factory(
        *arreglo)
    
    if len(request.vars)>0:
        for i in range(0,len(cmpo)):
            for f in dcc:
                if(f['id_campo_cat'] == ids[i]):
                    df = f['valor']
            valor = request.vars[str(cmpo[i])]
            db(db.VALORES_CAMPO_CATALOGO.valor == df).delete()
            try:
                db.VALORES_CAMPO_CATALOGO.insert(id_campo_cat = ids[i], id_catalogo = id_cat, valor = valor)
            except:
                session.message = "El valor de un campo esta duplicado"
        session.nombreMostrar = nombreCat
        redirect(URL('vMostrarCatalogo.html'))
    return (dict(forma = forma))

def eliminarValorCampo():
    admin = get_tipo_usuario()
    print(request.args)
    for dic in session.filas:
        for i in dic:
            if i['valor']==request.args[0]:
                diccionario = i
                dcc = dic
    print(diccionario)

    query = reduce(lambda a, b: (a&b),[db.CATALOGO.id_catalogo == diccionario['id_catalogo'],
                                      db.CATALOGO.id_catalogo == db.CATALOGO_TIENE_CAMPO.id_catalogo,
                                      db.CATALOGO_TIENE_CAMPO.id_campo_cat == db.CAMPO_CATALOGO.id_campo_cat])
    aux = db(query).select(db.CAMPO_CATALOGO.nombre)
    print(aux)
    cmpo = []
    ids = []
    # Nombres de los campos
    for raw in aux:
        cmpo.append(raw['nombre'])
    id_cat = db(db.CATALOGO.id_catalogo == diccionario['id_catalogo']).select(db.CATALOGO.id_catalogo)[0]['id_catalogo']
    arrId = db(query).select(db.CAMPO_CATALOGO.id_campo_cat)
    
    # Ids
    for raw in arrId:
        ids.append(raw['id_campo_cat'])
    for i in range(0,len(cmpo)):
        for f in dcc:
            if(f['id_campo_cat'] == ids[i]):
                df = f['valor']
        db(db.VALORES_CAMPO_CATALOGO.valor == df).delete()
    session.nombreMostrar = db(db.CATALOGO.id_catalogo == diccionario['id_catalogo']).select(db.CATALOGO.nombre)[0]['nombre']
    redirect(URL('vMostrarCatalogo.html'))

def vModificarCatalogo():
    admin = get_tipo_usuario()
    # Obtengo el nombre del tipo_actividad desde el objeto global 'session'
    if(session.nombreModificar != ""):
        nombreCat = session.nombreModificar
    else:
        nombreCat = request.args[0]
    
    # Creo query para realizar busqueda de los campos que ya han sido agregados
    # a ese tipo actividad
        ###########################################################################
            ###########################################################################
    query = reduce(lambda a, b: (a&b),[db.CATALOGO.nombre == nombreCat,
                                      db.CATALOGO.id_catalogo == db.CATALOGO_TIENE_CAMPO.id_catalogo,
                                      db.CATALOGO_TIENE_CAMPO.id_campo_cat == db.CAMPO_CATALOGO.id_campo_cat])
    query2 = reduce(lambda a, b: (a&b),[db.CATALOGO.nombre == nombreCat,
                                      db.CATALOGO.id_catalogo == db.CATALOGO_TIENE_CAMPO.id_catalogo,
                                      db.CATALOGO_TIENE_CAMPO.id_campo_cat == db.CAMPO_CATALOGO.id_campo_cat,
                                      db.VALORES_CAMPO_CATALOGO.id_campo_cat == db.CAMPO_CATALOGO.id_campo_cat,
                                      db.VALORES_CAMPO_CATALOGO.id_catalogo == db.CATALOGO.id_catalogo])
    ###########################################################################
        ###########################################################################
            ###########################################################################
                ###########################################################################
    # Guardo los resultados de dicho query en 'campos_guardados'
    campos_guardados = db(query).select(db.CAMPO_CATALOGO.ALL, db.CATALOGO.ALL)
    print("CAMPOS GUARDADOS ",campos_guardados)
    valores = db(query2).select(db.VALORES_CAMPO_CATALOGO.ALL)
    campos = db(query).select(db.CAMPO_CATALOGO.ALL)
    print("Valores: ",valores)
    print("campos: ",campos)
    print(nombreCat)
    if(len(campos) > 0):
        total = len(valores)/len(campos)
    else:
        total = 0
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
        idd_campo = db(db.CAMPO_CATALOGO.nombre == request.vars.nombre).select(db.CAMPO_CATALOGO.id_campo_cat)[0].id_campo_cat
        if len(db(db.CATALOGO_TIENE_CAMPO.id_campo_cat == idd_campo,db.CATALOGO_TIENE_CAMPO.id_catalogo == id_cat).select())>0:
            session.msgErr = 1
            session.message = 'Ya existe el campo'
        else:
            db.CATALOGO_TIENE_CAMPO.insert(id_catalogo = id_cat, id_campo_cat = idd_campo)
            valor_aux = " "
            print("EL TOTAL ES: ",total)
            for i in range(0,total):
                db.VALORES_CAMPO_CATALOGO.insert(id_catalogo = id_cat, id_campo_cat = idd_campo, valor = valor_aux*(i+1))
            session.msgErr = 0
        # Redirijo a la misma pagina para seguir agregando campos
        session.nombreModificar = nombreCat
        redirect(URL('vModificarCatalogo'))
    # En caso de que el formulario no sea aceptado
    elif form.errors:
        session.message = 'Datos invalidos'
    # Metodo GET
    else:
        if(not(session.msgErr)):
            session.message = ''

    return dict(form = form, campos_guardados = campos_guardados,admin = admin)

def eliminarCampos2():
    # Obtengo el nombre del tipo_actividad
    if len(request.args)!=0:
        nombreCat = request.args[0]
    else:
        nombreCat = session.catAgregar

    # Construyo query para obtener la relacion entre los campos y el tipo
    # actividad que quiero eliminar
    db(db.CATALOGO_TIENE_CAMPO.id_campo_cat == request.args[1]).delete()
    db(db.VALORES_CAMPO_CATALOGO.id_campo_cat == request.args[1]).delete()

    db(db.CAMPO_CATALOGO.id_campo_cat == request.args[1]).delete()
    session.nombreModificar = nombreCat
    
    redirect(URL('vModificarCatalogo.html'))
