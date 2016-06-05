# -*- coding: utf-8 -*-

db.define_table('tipo_actividad',
                Field('nombre','text',notnull = True),
                Field('tipo_p_r','string',notnull = True),
                Field('descripcion','text', notnull = True),
                Field('programa','text', notnull = True),
                Field('validacion','text', notnull = True),
                Field('nro_productos', 'integer'),
                Field('nro_campos','integer'),
                Field('ci_usuario_propone','reference usuario')
                )

db.define_table('actividad',
                Field('id_tipo','reference tipo_actividad'),
                Field('validacion','string', default = 'En espera' ),
                Field('estado','string' ),
                Field('evaluacion_criterio', 'text'),
                Field('evaluacion_valor','text'),
#                Field('ci_usuario_modifica', 'reference usuario'),
#                Field('ci_usuario_elimina', 'reference usuario'),
                Field('ci_usuario_crea', 'reference usuario')
                )

db.define_table('campo',
                Field('obligatorio','boolean'),
                Field('nombre', 'string')
                )

db.define_table('tiene_campo',
                Field('id_actividad','reference actividad'),
                Field('id_campo','reference campo'),
                Field('valor_campo','string'),
                )

db.define_table('act_posee_campo',
                Field('id_tipo_act','integer','reference tipo_actividad'),
                Field('id_campo' ,'reference campo')
                )

db.define_table('client',
     Field('name'))

db.define_table('address',
    Field('client','reference client',
          writable=False,readable=False),
    Field('street'),Field('city'))
