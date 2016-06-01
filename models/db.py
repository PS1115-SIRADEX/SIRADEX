# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.14.1":
    raise HTTP(500, "Requires web2py 2.13.3 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# app configuration made easy. Look inside private/appconfig.ini
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
myconf = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL("postgres://Siradex:Siradex@localhost:5432/Siradex", pool_size=10)
else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = ['*'] if request.is_local else []
# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = myconf.get('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.get('forms.separator') or ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

from gluon.tools import Auth, Service, PluginManager

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=myconf.get('host.names'))
service = Service()
plugins = PluginManager()

# -------------------------------------------------------------------------
# create all tables needed by auth if not custom tables
# -------------------------------------------------------------------------
auth.define_tables(username=False, signature=False)

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.get('smtp.server')
mail.settings.sender = myconf.get('smtp.sender')
mail.settings.login = myconf.get('smtp.login')
mail.settings.tls = myconf.get('smtp.tls') or False
mail.settings.ssl = myconf.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

# -------------------------------------------------------------------------
# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> db.mytable.insert(myfield='value')
# >>> rows = db(db.mytable.myfield == 'value').select(db.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
# -------------------------------------------------------------------------

db.define_table('USUARIO',
                Field('ci','string',length=10, notnull=True,required=True, unique=True),
                Field('nombres','string',length=50,required=True),
                Field('apellido','string',length=50,required=True),
                Field('password','password',required=True),
                Field('telefono','string',length=15,required=True),
                Field('email','string',length=50,required=True),
                Field('tipo','integer',length=15,required=True),
                primarykey=['ci'],
                migrate=False
);

db.define_table('USBID',
                Field('ci_usuario',db.USUARIO.ci),
                Field('usbid','string',length=20, notnull=True, unique=True),
                primarykey=['ci_usuario'],
                migrate=False
);

db.define_table('JEFE_DEPENDENCIA',
                Field('id_jefe','id'),
                Field('ci_usuario',db.USUARIO.ci),
                primarykey=['ci_usuario','id_jefe'],
                migrate=False
);

db.define_table('TIPO_ACTIVIDAD',
                Field('id_tipo','id'),
                
                Field('nombre','string',length=128, notnull=True,unique=True,
                      requires=[IS_NOT_EMPTY(error_message='No puede ser vacía'),
                                IS_LENGTH(128,error_message='El nombre debe ser de menos 128 caracteres'),
                                IS_NOT_IN_DB(db, 'TIPO_ACTIVIDAD.nombre',error_message='Ese nombre ya existe')]),
                
                Field('tipo_p_r','string', length=1, notnull=True, requires=IS_IN_SET(['P', 'R']),default='P' ,
                    widget=SQLFORM.widgets.radio.widget),
                Field('descripcion','string',length=2048, notnull=True, 
                      requires=[IS_NOT_EMPTY(error_message='No puede ser vacía'),
                                IS_LENGTH(2048,error_message='El nombre no pude ser más de 2048 caracteres')]),
                
                Field('programa','string', length=128, notnull=True, 
                      requires=[IS_NOT_EMPTY(error_message='No puede ser vacía'),
                                IS_LENGTH(128,error_message='El nombre no pude ser más de 127 caracteres')]),
                Field('validacion','string', length=128, notnull=True,default='True'),
                Field('producto', 'string', length=256,
                      requires=[IS_NOT_EMPTY(error_message='No puede ser vacía'),
                                IS_LENGTH(256,error_message='El nombre no pude ser más de 256 caracteres')]),
                Field('nro_campos', 'integer', requires=IS_NOT_EMPTY(error_message='No puede ser vacía')),
                Field('id_jefe_creado',db.JEFE_DEPENDENCIA.id_jefe),
                Field('ci_usuario_propone',db.USUARIO.ci),
                primarykey=['id_tipo'],
                migrate=False

);

db.define_table('ACTIVIDAD',
                Field('id_actividad', 'id'),
                Field('id_tipo', db.TIPO_ACTIVIDAD.id_tipo),
                Field('validacion','string',default='En espera'),
                Field('estado','string'),
                Field('evaluacion_criterio','string',length=256),
                Field('evaluacion_valor','string', length=256),
                Field('ci_usuario_modifica', db.USUARIO.ci),
                Field('ci_usuario_elimina', db.USUARIO.ci),
                Field('ci_usuario_crea', db.USUARIO.ci),
                primarykey=['id_actividad'],
                migrate=False
);

db.define_table('PERMISOS_TIPO_ACT',
                Field('permiso','string',length=256),
                Field('id_tipo', db.TIPO_ACTIVIDAD.id_tipo),
                primarykey=['permiso','id_tipo'],
                migrate=False

);

db.define_table('CATALOGO',
                Field('id_catalogo','id'),
                Field('nro_campos','integer'),
                Field('nombre','string', length=128),
                primarykey=['id_catalogo'],
                migrate=False
);


db.define_table('CAMPO',
                Field('id_campo','id'),
                Field('obligatorio', 'boolean'),
                Field('nombre','string', length=64,
                      requires = [IS_NOT_IN_DB(db, 'CAMPO.nombre',error_message='')]),
                Field('lista', 'string', length=64),
                Field('despliega_cat',db.CATALOGO.id_catalogo),
                primarykey=['id_campo'],
                migrate=False
);


db.define_table('CAMPO_CATALOGO',
                Field('id_campo_cat', 'id'),
                Field('tipo_cat','string', length=256),
                Field('nombre', 'string', length=64),
                primarykey=['id_campo_cat'],
                migrate=False
);


db.define_table('LOG',
                Field('accion','string'),
                Field('accion_fecha','datetime'),
                Field('accion_ip','string'),
                Field('descripcion','string'),
                Field('ci_usuario',db.USUARIO.ci),
                primarykey=['accion','accion_fecha','accion_ip'],
                migrate=False
);


db.define_table('PARTICIPA_ACT',
                Field('ci_usuario',db.USUARIO.ci),
                Field('id_actividad',db.ACTIVIDAD.id_actividad),
                primarykey=['ci_usuario','id_actividad'],
                migrate=False
);

db.define_table('TIENE_CAMPO',
                Field('id_actividad',db.ACTIVIDAD.id_actividad),
                Field('id_campo', db.CAMPO.id_campo),
                Field('valor_campo', 'string', length=256),
                primarykey=['id_actividad', 'id_campo'],
                migrate=False
);

db.define_table('ACT_POSEE_CAMPO',
                Field('id_tipo_act', db.TIPO_ACTIVIDAD.id_tipo),
                Field('id_campo', db.CAMPO.id_campo),
                primarykey=['id_tipo_act', 'id_campo'],
                migrate=False
);

db.define_table('GESTIONA_TIPO_ACT',
                Field('id_jefe', db.JEFE_DEPENDENCIA.id_jefe),
                Field('id_tipo_act', db.TIPO_ACTIVIDAD.id_tipo),
                primarykey=['id_jefe','id_tipo_act'],
                migrate=False
);


db.define_table('GESTIONA_CATALOGO',
                Field('id_jefe', db.JEFE_DEPENDENCIA.id_jefe),
                Field('id_catalogo',db.CATALOGO.id_catalogo),
                primarykey=['id_jefe','id_catalogo'],
                migrate=False
);

db.define_table('CATALOGO_TIENE_CAMPO',
                Field('id_catalogo',db.CATALOGO.id_catalogo),
                Field('id_campo_cat',db.CAMPO_CATALOGO.id_campo_cat),
                primarykey=['id_catalogo','id_campo_cat'],
                migrate=False
);

db.define_table('CATALOGO_CONTIENE_CAMPO',
                Field('id_catalogo',db.CATALOGO.id_catalogo),
                Field('id_campo_cat',db.CAMPO_CATALOGO.id_campo_cat),
                Field('valor','string', length=256),
                primarykey=['id_catalogo','id_campo_cat'],
                migrate=False
);
#crfrefrw


# -------------------------------------------------------------------------
# after defining tables, uncomment below to enable auditing
# -------------------------------------------------------------------------
# auth.enable_record_versioning(db)
