# -*- coding: utf-8 -*-
db.define_table('USUARIO',
                Field('nombre','string')
                )

db.define_table('TIPO_ACTIVIDAD',
                Field('nombre','text',notnull = True),
                Field('tipo_p_r','string',notnull = True),
                Field('descripcion','text', notnull = True),
                Field('programa','text', notnull = True),
                Field('validacion','text', notnull = True),
                Field('nro_productos', 'integer'),
                Field('nro_campos','integer'),
                Field('ci_usuario_propone','reference USUARIO')
                )

db.define_table('ACTIVIDAD',
                Field('id_tipo','reference TIPO_ACTIVIDAD'),
                Field('validacion','string', default = 'En espera' ),
                Field('estado','string' ),
                Field('evaluacion_criterio', 'text'),
                Field('evaluacion_valor','text'),
                Field('ci_usuario_modifica', 'reference USUARIO'),
                Field('ci_usuario_elimina', 'reference USUARIO'),
                Field('ci_usuario_crea', 'reference USUARIO')
                )

db.define_table('CAMPO',
                Field('obligatorio','boolean'),
                Field('nombre', 'string'),
                Field('id_tipo_actividad', 'reference TIPO_ACTIVIDAD')
                )

db.define_table('VALOR_CAMPO',
                Field('id_campo','reference CAMPO '),
                Field('id_tipo','reference TIPO_ACTIVIDAD '),
                Field('valor','string',notnull = True)
                )

db.define_table('client',
     Field('name'))

db.define_table('address',
    Field('client','reference client',
          writable=False,readable=False),
    Field('street'),Field('city'))
