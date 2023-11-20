insert into finanzas_categorias_ingreso ("descripcion", "monedero_defecto") select 'Nómina Borja', fm.id from finanzas_monederos fm where fm.nombre = 'Cuenta Banco Borja';
insert into finanzas_categorias_ingreso ("descripcion", "monedero_defecto") select 'Otras ganancias patrimoniales', fm.id from finanzas_monederos fm where fm.nombre = 'Cuenta Banco Borja';
insert into finanzas_categorias_ingreso ("descripcion", "monedero_defecto") select 'Ingresos extraordinarios', fm.id from finanzas_monederos fm where fm.nombre = 'Cuenta Banco Borja';
insert into finanzas_categorias_ingreso ("descripcion", "cuenta_abono_defecto", "monedero_defecto") select 'Becas', fc.id, fm.id from finanzas_cuentas fc, finanzas_monederos fm where fc.nombre = 'Formación' and  fm.nombre = 'Cuenta Banco Borja';
insert into finanzas_categorias_ingreso ("descripcion", "cuenta_abono_defecto", "monedero_defecto") select 'Subvenciones', fc.id, fm.id from finanzas_cuentas fc, finanzas_monederos fm where fc.nombre = 'Ahorro' and  fm.nombre = 'Cuenta Banco Borja';
insert into finanzas_categorias_ingreso ("descripcion", "cuenta_abono_defecto", "monedero_defecto") select 'Devoluciones de Básicos', fc.id, fm.id from finanzas_cuentas fc, finanzas_monederos fm where fc.nombre = 'Básicos' and  fm.nombre = 'Cuenta Banco Borja';
insert into finanzas_categorias_ingreso ("descripcion", "cuenta_abono_defecto", "monedero_defecto") select 'Devoluciones de Formación', fc.id, fm.id from finanzas_cuentas fc, finanzas_monederos fm where fc.nombre = 'Formación' and  fm.nombre = 'Cuenta Banco Borja';
insert into finanzas_categorias_ingreso ("descripcion", "cuenta_abono_defecto", "monedero_defecto") select 'Devoluciones de Ocio', fc.id, fm.id from finanzas_cuentas fc, finanzas_monederos fm where fc.nombre = 'Ocio' and  fm.nombre = 'Cuenta Banco Borja';
insert into finanzas_categorias_ingreso ("descripcion", "cuenta_abono_defecto", "monedero_defecto") select 'Devoluciones de préstamos de otras personas', fc.id, fm.id from finanzas_cuentas fc, finanzas_monederos fm where fc.nombre = 'Básicos' and  fm.nombre = 'Cuenta Banco Borja';
insert into finanzas_categorias_ingreso ("descripcion", "cuenta_abono_defecto", "monedero_defecto") select 'Dividendos', fc.id, fm.id from finanzas_cuentas fc, finanzas_monederos fm where fc.nombre = 'Inversión' and  fm.nombre = 'Degiro';
insert into finanzas_categorias_ingreso ("descripcion", "cuenta_abono_defecto", "monedero_defecto") select 'Donación de otras personas', fc.id, fm.id from finanzas_cuentas fc, finanzas_monederos fm where fc.nombre = 'Básicos' and  fm.nombre = 'Cuenta Banco Borja';
insert into finanzas_categorias_ingreso ("descripcion", "cuenta_abono_defecto", "monedero_defecto") select 'Ganancia en apuestas y juegos', fc.id, fm.id from finanzas_cuentas fc, finanzas_monederos fm where fc.nombre = 'Ocio' and  fm.nombre = 'Cuenta Banco Borja';
insert into finanzas_categorias_ingreso ("descripcion", "cuenta_abono_defecto", "monedero_defecto") select 'Ingresos por venta de acciones', fc.id, fm.id from finanzas_cuentas fc, finanzas_monederos fm where fc.nombre = 'Inversión' and  fm.nombre = 'Degiro';
insert into finanzas_categorias_ingreso ("descripcion", "cuenta_abono_defecto", "monedero_defecto") select 'Intereses', fc.id, fm.id from finanzas_cuentas fc, finanzas_monederos fm where fc.nombre = 'Inversión' and  fm.nombre = 'Cuenta Banco Borja';
insert into finanzas_categorias_ingreso ("descripcion", "cuenta_abono_defecto", "monedero_defecto") select 'Otros', fc.id, fm.id from finanzas_cuentas fc, finanzas_monederos fm where fc.nombre = 'Básicos' and  fm.nombre = 'Cuenta Banco Borja';
insert into finanzas_categorias_ingreso ("descripcion", "cuenta_abono_defecto", "monedero_defecto") select 'Préstamos de otras personas', fc.id, fm.id from finanzas_cuentas fc, finanzas_monederos fm where fc.nombre = 'Básicos' and  fm.nombre = 'Cuenta Banco Borja';
insert into finanzas_categorias_ingreso ("descripcion", "cuenta_abono_defecto", "monedero_defecto") select 'Rentas y alquileres', fc.id, fm.id from finanzas_cuentas fc, finanzas_monederos fm where fc.nombre = 'Inversión' and  fm.nombre = 'Cuenta Banco Borja';
insert into finanzas_categorias_ingreso ("descripcion", "cuenta_abono_defecto", "monedero_defecto") select 'Transferencia a Ahorro', fc.id, fm.id from finanzas_cuentas fc, finanzas_monederos fm where fc.nombre = 'Ahorro' and  fm.nombre = 'Cuenta Banco Borja';
insert into finanzas_categorias_ingreso ("descripcion", "cuenta_abono_defecto", "monedero_defecto") select 'Transferencia a Básicos', fc.id, fm.id from finanzas_cuentas fc, finanzas_monederos fm where fc.nombre = 'Básicos' and  fm.nombre = 'Cuenta Banco Borja';
insert into finanzas_categorias_ingreso ("descripcion", "cuenta_abono_defecto", "monedero_defecto") select 'Transferencia a Formación', fc.id, fm.id from finanzas_cuentas fc, finanzas_monederos fm where fc.nombre = 'Formación' and  fm.nombre = 'Cuenta Banco Borja';
insert into finanzas_categorias_ingreso ("descripcion", "cuenta_abono_defecto", "monedero_defecto") select 'Transferencia a Inversión', fc.id, fm.id from finanzas_cuentas fc, finanzas_monederos fm where fc.nombre = 'Inversión' and  fm.nombre = 'Cuenta Banco Borja';
insert into finanzas_categorias_ingreso ("descripcion", "cuenta_abono_defecto", "monedero_defecto") select 'Transferencia a Ocio', fc.id, fm.id from finanzas_cuentas fc, finanzas_monederos fm where fc.nombre = 'Ocio' and  fm.nombre = 'Cuenta Banco Borja';