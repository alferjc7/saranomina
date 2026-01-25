--
-- PostgreSQL database dump
--

\restrict d3Tbc9tRYqGyeA3gFPqgwCUlKqdHoBdc0z5A3JDFmN2UIFnoRChrBNeJhSGcm0J

-- Dumped from database version 17.7
-- Dumped by pg_dump version 17.7

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: reportes; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA reportes;


ALTER SCHEMA reportes OWNER TO postgres;

--
-- Name: fn_contrato_cumple_filtros(bigint, bigint); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.fn_contrato_cumple_filtros(p_contrato_id bigint, p_logica_calculo_id bigint) RETURNS boolean
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_filtro RECORD;
    v_sql TEXT;
    v_result BOOLEAN;
    v_operador TEXT;
BEGIN
    FOR v_filtro IN
        SELECT campo, operador, valor
        FROM "gestionNomina_t_logica_calculo_filtro"
        WHERE logica_calculo_id = p_logica_calculo_id
    LOOP

        -- Normalizar operador
        v_operador := upper(replace(v_filtro.operador, '_', ' '));

        IF v_operador IN ('IN', 'NOT IN') THEN
            v_sql := format(
                'SELECT (%I %s (%s)) FROM "gestionContratos_t_contrato" WHERE id = %s',
                v_filtro.campo,
                v_operador,
                v_filtro.valor,
                p_contrato_id
            );
        ELSE
            v_sql := format(
                'SELECT (%I %s %L) FROM "gestionContratos_t_contrato" WHERE id = %s',
                v_filtro.campo,
                v_operador,
                v_filtro.valor,
                p_contrato_id
            );
        END IF;

        EXECUTE v_sql INTO v_result;

        IF v_result IS DISTINCT FROM TRUE THEN
            RETURN FALSE;
        END IF;

    END LOOP;

    RETURN TRUE;
END;
$$;


ALTER FUNCTION public.fn_contrato_cumple_filtros(p_contrato_id bigint, p_logica_calculo_id bigint) OWNER TO postgres;

--
-- Name: fn_dias_laborales_nomina(date, date); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.fn_dias_laborales_nomina(p_fecha_inicio date, p_fecha_fin date) RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE
    dia_ini INTEGER;
    dia_fin INTEGER;
    dias INTEGER;
    es_febrero BOOLEAN;
BEGIN
    -- Fechas inválidas
    IF p_fecha_inicio > p_fecha_fin THEN
        RETURN 0;
    END IF;

    dia_ini := EXTRACT(DAY FROM p_fecha_inicio);
    dia_fin := EXTRACT(DAY FROM p_fecha_fin);

    -- Regla nómina: el día 31 no existe
    IF dia_ini = 31 THEN
        dia_ini := 30;
    END IF;

    IF dia_fin = 31 THEN
        dia_fin := 30;
    END IF;

    -- ¿Es febrero?
    es_febrero :=
        EXTRACT(MONTH FROM p_fecha_inicio) = 2
        AND EXTRACT(MONTH FROM p_fecha_fin) = 2;

    -- Febrero completo siempre = 30
    IF es_febrero
       AND dia_ini = 1
       AND dia_fin >= 28 THEN
        RETURN 30;
    END IF;

    -- Cálculo base 30
    dias := (dia_fin - dia_ini) + 1;

    -- Ajustes finales
    IF dias < 0 THEN
        dias := 0;
    END IF;

    IF dias > 30 THEN
        dias := 30;
    END IF;

    RETURN dias;
END;
$$;


ALTER FUNCTION public.fn_dias_laborales_nomina(p_fecha_inicio date, p_fecha_fin date) OWNER TO postgres;

--
-- Name: fn_porc_solidaridad(numeric); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.fn_porc_solidaridad(p_base numeric) RETURNS numeric
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_total NUMERIC;
    v_smlmv NUMERIC;
    v_fsp1 NUMERIC;
    v_fsp2 NUMERIC;
    v_fsp3 NUMERIC;
    v_fsp4 NUMERIC;
    v_fsp5 NUMERIC;
    v_fsp6 NUMERIC;

BEGIN

    select valor_numerico
    into v_smlmv
    from public."parametros_parametrodetalle" 
    where parametro_id in(select id from 
                        public."parametros_parametrogeneral" 
                        where codigo = 'P_SIS') AND
            codigo = 'SMLMV';

    select FSP1,FSP2,FSP3,FSP4,FSP5,FSP6 
    into v_fsp1,v_fsp2,v_fsp3,v_fsp4,v_fsp5,v_fsp6
    from(select 
    sum( case when codigo =  'FSP_1' THEN valor_numerico  else 0 end) as FSP1,
    sum(case when codigo =  'FSP_2' THEN valor_numerico else 0  end) as FSP2,
    sum(case when codigo =  'FSP_3' THEN valor_numerico else 0 end) as FSP3,
    sum(case when codigo =  'FSP_4' THEN valor_numerico else 0 end) as FSP4,
    sum(case when codigo =  'FSP_5' THEN valor_numerico else 0 end) as FSP5,
    sum(case when codigo =  'FSP_6' THEN valor_numerico else 0 end) as FSP6
    from public."parametros_parametrodetalle" 
    where parametro_id in(select id from 
                        public."parametros_parametrogeneral" 
                        where codigo = 'P_FSP'));


    IF p_base >= (v_smlmv*4) and p_base < (v_smlmv*16)  THEN
    v_total := v_fsp1;
    ELSEIF  p_base >= (v_smlmv*16) and p_base < (v_smlmv*17) THEN
    v_total := v_fsp2;
    ELSEIF  p_base >= (v_smlmv*17) and p_base < (v_smlmv*18) THEN
    v_total := v_fsp3;
    ELSEIF p_base >= (v_smlmv*18) and p_base < (v_smlmv*19) THEN
    v_total := v_fsp4;
    ELSEIF p_base >= (v_smlmv*19) and p_base < (v_smlmv*20) THEN
    v_total := v_fsp5;
    ELSEIF p_base > (v_smlmv*20) THEN
    v_total := v_fsp6;
    END IF;
    
    
    RETURN v_total;

END;
$$;


ALTER FUNCTION public.fn_porc_solidaridad(p_base numeric) OWNER TO postgres;

--
-- Name: fn_sumatoria_deducciones(bigint, bigint, bigint, integer, integer, integer); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.fn_sumatoria_deducciones(p_empresa_id bigint, p_contrato_id bigint, p_tipo_nomina bigint, p_periodo integer, p_anio integer, p_mes integer) RETURNS numeric
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_total NUMERIC;
BEGIN
    select COALESCE(sum(ae.valor),0) 
    into v_total
    from public."gestionNomina_t_acumulado_empleado" ae 
    where ae.concepto_id in (select id
                        from public."gestionConceptos_t_concepto_empresa" 
                        where empresa_id = p_empresa_id and 
                        cod_concepto_id in(select id
                                        from public."gestionConceptos_t_conceptos" 
                                        where tipo_concepto = 'DED')) AND
        ae.contrato_id = p_contrato_id AND
        ae.periodo =  p_periodo AND
        ae.anio = p_anio AND
        ae.mes = p_mes AND
        ae.tipo_nomina_id = p_tipo_nomina;

    RETURN v_total;

END;
$$;


ALTER FUNCTION public.fn_sumatoria_deducciones(p_empresa_id bigint, p_contrato_id bigint, p_tipo_nomina bigint, p_periodo integer, p_anio integer, p_mes integer) OWNER TO postgres;

--
-- Name: fn_sumatoria_devengos(bigint, bigint, bigint, integer, integer, integer); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.fn_sumatoria_devengos(p_empresa_id bigint, p_contrato_id bigint, p_tipo_nomina bigint, p_periodo integer, p_anio integer, p_mes integer) RETURNS numeric
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_total NUMERIC;
BEGIN
    select COALESCE(sum(ae.valor),0) 
    into v_total
    from public."gestionNomina_t_acumulado_empleado" ae
    where concepto_id in (select id
                        from public."gestionConceptos_t_concepto_empresa" 
                        where empresa_id = p_empresa_id and 
                        cod_concepto_id in(select id
                                        from public."gestionConceptos_t_conceptos" 
                                        where tipo_concepto = 'DEV')) AND
        ae.contrato_id = p_contrato_id AND
        ae.periodo =  p_periodo AND
        ae.anio = p_anio AND
        ae.mes = p_mes AND
        ae.tipo_nomina_id = p_tipo_nomina;
        
    RETURN v_total;

END;
$$;


ALTER FUNCTION public.fn_sumatoria_devengos(p_empresa_id bigint, p_contrato_id bigint, p_tipo_nomina bigint, p_periodo integer, p_anio integer, p_mes integer) OWNER TO postgres;

--
-- Name: fn_sumatoria_grupo_conceptos(bigint, date, date, character varying); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.fn_sumatoria_grupo_conceptos(p_contrato_id bigint, p_fecha_inicio date, p_fecha_fin date, p_codigo_grupo character varying) RETURNS numeric
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_total NUMERIC;
BEGIN

    SELECT
        COALESCE(SUM(SUMAR), 0) - COALESCE(SUM(RESTAR), 0)
    INTO v_total
    FROM (

        SELECT 
            COALESCE(SUM(valor), 0) AS SUMAR,
            0 AS RESTAR
        FROM "gestionNomina_t_acumulado_empleado"
        WHERE contrato_id = p_contrato_id
          AND fecha_inicio >= p_fecha_inicio
          AND fecha_fin    <= p_fecha_fin
          AND concepto_id IN (
                SELECT concepto_id
                FROM "gestionConceptos_t_grupo_concepto_det"
                WHERE operacion = '+'
                  AND grupo_id IN (
                        SELECT id
                        FROM "gestionConceptos_t_grupo_concepto"
                        WHERE codigo = p_codigo_grupo
                  )
          )

        UNION ALL

        SELECT 
            0 AS SUMAR,
            COALESCE(SUM(valor), 0) AS RESTAR
        FROM "gestionNomina_t_acumulado_empleado"
        WHERE contrato_id = p_contrato_id
          AND fecha_inicio >= p_fecha_inicio
          AND fecha_fin    <= p_fecha_fin
          AND concepto_id IN (
                SELECT concepto_id
                FROM "gestionConceptos_t_grupo_concepto_det"
                WHERE operacion = '-'
                  AND grupo_id IN (
                        SELECT id
                        FROM "gestionConceptos_t_grupo_concepto"
                        WHERE codigo = p_codigo_grupo
                  )
          )

    ) t;

    RETURN v_total;

END;
$$;


ALTER FUNCTION public.fn_sumatoria_grupo_conceptos(p_contrato_id bigint, p_fecha_inicio date, p_fecha_fin date, p_codigo_grupo character varying) OWNER TO postgres;

--
-- Name: prc_1000_00(integer, integer, integer, integer, integer, integer, date, date, integer, integer, integer, integer, character varying); Type: PROCEDURE; Schema: public; Owner: postgres
--

CREATE PROCEDURE public.prc_1000_00(IN p_empresa_id integer, IN p_contrato_id integer, IN p_tipo_nomina_id integer, IN p_anio integer, IN p_mes integer, IN p_periodo integer, IN p_fecha_inicio date, IN p_fecha_fin date, IN p_concepto_id integer, IN p_proceso_id integer, IN p_modulo_id integer, IN p_periodo_nomina integer, IN p_sin_valor character varying)
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_salario NUMERIC;
    v_base NUMERIC;
    v_modulo BIGINT;
    f_ini DATE;
    f_fin DATE;
    unidades NUMERIC;
    unidades_per NUMERIC;
BEGIN
    INSERT INTO t_log_nomina (proceso_id, origen, mensaje)
    VALUES (p_proceso_id,'prc_1000_00','Inicio contrato=' || p_contrato_id || ' concepto=' || p_concepto_id);
    

    SELECT cs.salario
    INTO v_salario
    FROM "gestionContratos_t_contrato_salario" cs
    WHERE cs.contrato_id = p_contrato_id
      AND cs.estado = TRUE
      AND cs.tipo_salario_id in (select id                      
                                 from "parametros_t_tipo_salario" 
                                 where salario = 'BASICO')
    ORDER BY cs.fecha_inicio DESC
    LIMIT 1;

    v_base := v_salario;
    
    select fecha_ingreso, fecha_fin 
    into f_ini, f_fin
    from "gestionContratos_t_contrato"
    where empresa_id = p_empresa_id AND
    id = p_contrato_id AND
    estado = 'A';

    unidades_per := public.fn_dias_laborales_nomina(p_fecha_inicio,p_fecha_fin);
    v_salario := v_salario/unidades_per;
    
    --VALIDAR QUE LA FECHA INICIO DEL CONTRATO NO SEA MAYOR AL INICIO DEL PERIODO SI ES MAYOR REEMPLAZAR
    IF f_ini >  p_fecha_inicio AND f_ini <= p_fecha_fin THEN
        p_fecha_inicio := f_ini;
    END IF;    
    --VALIDAR QUE LA FECHA FIN DEL CONTRATO NO SEA MAYOR AL INICIO DEL PERIODO SI ES MAYOR REEMPLAZAR
    IF f_fin <  p_fecha_fin AND f_fin >= p_fecha_inicio THEN
        p_fecha_fin := f_fin;
    END IF;

    unidades = public.fn_dias_laborales_nomina(p_fecha_inicio,p_fecha_fin);
    v_salario := v_salario *unidades;

    INSERT INTO t_log_nomina (proceso_id, origen, mensaje)
    VALUES (p_proceso_id,'prc_1000_00','Salario encontrado=' || COALESCE(v_salario::TEXT, 'NULL'));

    IF v_salario IS NULL THEN
        RETURN;
    END IF;

    INSERT INTO t_log_nomina (proceso_id, origen, mensaje)
    VALUES (p_proceso_id,'prc_1000_00','Insertando acumulado');

    IF p_sin_valor = 'NB' and v_salario = 0 THEN

    INSERT INTO "gestionNomina_t_acumulado_empleado" (
        contrato_id,
        tipo_nomina_id,
        anio,
        mes,
        periodo,
        fecha_inicio,
        fecha_fin,
        concepto_id,
        unidad,
        base,
        valor,
        modulo_id,
        fecha_novedad,
        periodo_nomina_id
    )
    VALUES (
        p_contrato_id,
        p_tipo_nomina_id,
        p_anio,
        p_mes,
        p_periodo,
        p_fecha_inicio,
        p_fecha_fin,
        p_concepto_id,
        unidades,
        v_base,
        v_salario,
        p_modulo_id,
        p_fecha_fin,
        p_periodo_nomina
    );

    ELSEIF p_sin_valor = 'BO' and v_salario = 0 THEN

    INSERT INTO t_log_nomina (proceso_id, origen, mensaje)
    VALUES (p_proceso_id,'prc_1000_00','BORRAR LINEA');

    ELSE

    INSERT INTO "gestionNomina_t_acumulado_empleado" (
        contrato_id,
        tipo_nomina_id,
        anio,
        mes,
        periodo,
        fecha_inicio,
        fecha_fin,
        concepto_id,
        unidad,
        base,
        valor,
        modulo_id,
        fecha_novedad,
        periodo_nomina_id
    )
    VALUES (
        p_contrato_id,
        p_tipo_nomina_id,
        p_anio,
        p_mes,
        p_periodo,
        p_fecha_inicio,
        p_fecha_fin,
        p_concepto_id,
        unidades,
        v_base,
        v_salario,
        p_modulo_id,
        p_fecha_fin,
        p_periodo_nomina
    );

    END IF;

    INSERT INTO t_log_nomina (proceso_id, origen, mensaje)
    VALUES (p_proceso_id,'prc_1000_00','Inserta OK');


END;
$$;


ALTER PROCEDURE public.prc_1000_00(IN p_empresa_id integer, IN p_contrato_id integer, IN p_tipo_nomina_id integer, IN p_anio integer, IN p_mes integer, IN p_periodo integer, IN p_fecha_inicio date, IN p_fecha_fin date, IN p_concepto_id integer, IN p_proceso_id integer, IN p_modulo_id integer, IN p_periodo_nomina integer, IN p_sin_valor character varying) OWNER TO postgres;

--
-- Name: prc_1010_00(integer, integer, integer, integer, integer, integer, date, date, integer, integer, integer, integer, character varying); Type: PROCEDURE; Schema: public; Owner: postgres
--

CREATE PROCEDURE public.prc_1010_00(IN p_empresa_id integer, IN p_contrato_id integer, IN p_tipo_nomina_id integer, IN p_anio integer, IN p_mes integer, IN p_periodo integer, IN p_fecha_inicio date, IN p_fecha_fin date, IN p_concepto_id integer, IN p_proceso_id integer, IN p_modulo_id integer, IN p_periodo_nomina integer, IN p_sin_valor character varying)
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_salario NUMERIC;
    v_base NUMERIC;
    v_modulo BIGINT;
    f_ini DATE;
    f_fin DATE;
    unidades NUMERIC;
    unidades_per NUMERIC;
BEGIN
    INSERT INTO t_log_nomina (proceso_id, origen, mensaje)
    VALUES (p_proceso_id,'prc_1010_00','Inicio contrato=' || p_contrato_id || ' concepto=' || p_concepto_id);
    
    SELECT cs.salario
    INTO v_salario
    FROM "gestionContratos_t_contrato_salario" cs
    WHERE cs.contrato_id = p_contrato_id
      AND cs.estado = TRUE
      AND cs.tipo_salario_id in (select id                      
                                 from "parametros_t_tipo_salario" 
                                 where salario = 'INTEGRAL')
    ORDER BY cs.fecha_inicio DESC
    LIMIT 1;

    v_base := v_salario;

    select fecha_ingreso, fecha_fin 
    into f_ini, f_fin
    from "gestionContratos_t_contrato"
    where empresa_id = p_empresa_id AND
    id = p_contrato_id AND
    estado = 'A';

    unidades_per = public.fn_dias_laborales_nomina(p_fecha_inicio,p_fecha_fin);
    v_salario := v_salario/unidades_per;
    
    --VALIDAR QUE LA FECHA INICIO DEL CONTRATO NO SEA MAYOR AL INICIO DEL PERIODO SI ES MAYOR REEMPLAZAR
    IF f_ini >  p_fecha_inicio AND f_ini <= p_fecha_fin THEN
        p_fecha_inicio := f_ini;
    END IF;    
    --VALIDAR QUE LA FECHA FIN DEL CONTRATO NO SEA MAYOR AL INICIO DEL PERIODO SI ES MAYOR REEMPLAZAR
    IF f_fin <  p_fecha_fin AND f_fin >= p_fecha_inicio THEN
        p_fecha_fin := f_fin;
    END IF;

    unidades = public.fn_dias_laborales_nomina(p_fecha_inicio,p_fecha_fin);
    v_salario := v_salario *unidades;



    INSERT INTO t_log_nomina (proceso_id, origen, mensaje)
    VALUES (p_proceso_id,'prc_1010_00','Salario encontrado=' || COALESCE(v_salario::TEXT, 'NULL'));

    IF v_salario IS NULL THEN
        RETURN;
    END IF;

    INSERT INTO t_log_nomina (proceso_id, origen, mensaje)
    VALUES (p_proceso_id,'prc_1010_00','Insertando acumulado');

    IF p_sin_valor = 'NB' and v_salario = 0 THEN

    INSERT INTO "gestionNomina_t_acumulado_empleado" (
        contrato_id,
        tipo_nomina_id,
        anio,
        mes,
        periodo,
        fecha_inicio,
        fecha_fin,
        concepto_id,
        unidad,
        base,
        valor,
        modulo_id,
        fecha_novedad,
        periodo_nomina_id
    )
    VALUES (
        p_contrato_id,
        p_tipo_nomina_id,
        p_anio,
        p_mes,
        p_periodo,
        p_fecha_inicio,
        p_fecha_fin,
        p_concepto_id,
        unidades,
        v_base,
        v_salario,
        p_modulo_id,
        p_fecha_fin,
        p_periodo_nomina
    );

    ELSEIF p_sin_valor = 'BO' and v_salario = 0 THEN

    INSERT INTO t_log_nomina (proceso_id, origen, mensaje)
    VALUES (p_proceso_id,'prc_1010_00','BORRAR LINEA');

    ELSE

    INSERT INTO "gestionNomina_t_acumulado_empleado" (
        contrato_id,
        tipo_nomina_id,
        anio,
        mes,
        periodo,
        fecha_inicio,
        fecha_fin,
        concepto_id,
        unidad,
        base,
        valor,
        modulo_id,
        fecha_novedad,
        periodo_nomina_id
    )
    VALUES (
        p_contrato_id,
        p_tipo_nomina_id,
        p_anio,
        p_mes,
        p_periodo,
        p_fecha_inicio,
        p_fecha_fin,
        p_concepto_id,
        unidades,
        v_base,
        v_salario,
        p_modulo_id,
        p_fecha_fin,
        p_periodo_nomina
    );

    END IF;

    INSERT INTO t_log_nomina (proceso_id, origen, mensaje)
    VALUES (p_proceso_id,'prc_1010_00','Inserta OK');

END;
$$;


ALTER PROCEDURE public.prc_1010_00(IN p_empresa_id integer, IN p_contrato_id integer, IN p_tipo_nomina_id integer, IN p_anio integer, IN p_mes integer, IN p_periodo integer, IN p_fecha_inicio date, IN p_fecha_fin date, IN p_concepto_id integer, IN p_proceso_id integer, IN p_modulo_id integer, IN p_periodo_nomina integer, IN p_sin_valor character varying) OWNER TO postgres;

--
-- Name: prc_1012_00(integer, integer, integer, integer, integer, integer, date, date, integer, integer, integer, integer, character varying); Type: PROCEDURE; Schema: public; Owner: postgres
--

CREATE PROCEDURE public.prc_1012_00(IN p_empresa_id integer, IN p_contrato_id integer, IN p_tipo_nomina_id integer, IN p_anio integer, IN p_mes integer, IN p_periodo integer, IN p_fecha_inicio date, IN p_fecha_fin date, IN p_concepto_id integer, IN p_proceso_id integer, IN p_modulo_id integer, IN p_periodo_nomina integer, IN p_sin_valor character varying)
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_salario NUMERIC;
    v_base NUMERIC;
    v_modulo BIGINT;
    f_ini DATE;
    f_fin DATE;
    unidades NUMERIC;
    unidades_per NUMERIC;
BEGIN
    INSERT INTO t_log_nomina (proceso_id, origen, mensaje)
    VALUES (p_proceso_id,'prc_1012_00','Inicio contrato=' || p_contrato_id || ' concepto=' || p_concepto_id);
    
    SELECT cs.salario
    INTO v_salario
    FROM "gestionContratos_t_contrato_salario" cs
    WHERE cs.contrato_id = p_contrato_id
      AND cs.estado = TRUE
      AND cs.tipo_salario_id in (select id                      
                                 from "parametros_t_tipo_salario" 
                                 where salario = 'APRENDIZ')
    ORDER BY cs.fecha_inicio DESC
    LIMIT 1;

    v_base := v_salario;

    select fecha_ingreso, fecha_fin 
    into f_ini, f_fin
    from "gestionContratos_t_contrato"
    where empresa_id = p_empresa_id AND
    id = p_contrato_id AND
    estado = 'A';

    unidades_per = public.fn_dias_laborales_nomina(p_fecha_inicio,p_fecha_fin);
    v_salario := v_salario/unidades_per;
    
    --VALIDAR QUE LA FECHA INICIO DEL CONTRATO NO SEA MAYOR AL INICIO DEL PERIODO SI ES MAYOR REEMPLAZAR
    IF f_ini >  p_fecha_inicio AND f_ini <= p_fecha_fin THEN
        p_fecha_inicio := f_ini;
    END IF;    
    --VALIDAR QUE LA FECHA FIN DEL CONTRATO NO SEA MAYOR AL INICIO DEL PERIODO SI ES MAYOR REEMPLAZAR
    IF f_fin <  p_fecha_fin AND f_fin >= p_fecha_inicio THEN
        p_fecha_fin := f_fin;
    END IF;

    unidades = public.fn_dias_laborales_nomina(p_fecha_inicio,p_fecha_fin);
    v_salario := v_salario *unidades;


    INSERT INTO t_log_nomina (proceso_id, origen, mensaje)
    VALUES (p_proceso_id,'prc_1012_00','Salario encontrado=' || COALESCE(v_salario::TEXT, 'NULL'));

    IF v_salario IS NULL THEN
        RETURN;
    END IF;

    INSERT INTO t_log_nomina (proceso_id, origen, mensaje)
    VALUES (p_proceso_id,'prc_1012_00','Insertando acumulado');

    IF p_sin_valor = 'NB' and v_salario = 0 THEN

    INSERT INTO "gestionNomina_t_acumulado_empleado" (
        contrato_id,
        tipo_nomina_id,
        anio,
        mes,
        periodo,
        fecha_inicio,
        fecha_fin,
        concepto_id,
        unidad,
        base,
        valor,
        modulo_id,
        fecha_novedad,
        periodo_nomina_id
    )
    VALUES (
        p_contrato_id,
        p_tipo_nomina_id,
        p_anio,
        p_mes,
        p_periodo,
        p_fecha_inicio,
        p_fecha_fin,
        p_concepto_id,
        unidades,
        v_base,
        v_salario,
        p_modulo_id,
        p_fecha_fin,
        p_periodo_nomina
    );

    ELSEIF p_sin_valor = 'BO' and v_salario = 0 THEN

    INSERT INTO t_log_nomina (proceso_id, origen, mensaje)
    VALUES (p_proceso_id,'prc_1012_00','BORRAR LINEA');

    ELSE

    INSERT INTO "gestionNomina_t_acumulado_empleado" (
        contrato_id,
        tipo_nomina_id,
        anio,
        mes,
        periodo,
        fecha_inicio,
        fecha_fin,
        concepto_id,
        unidad,
        base,
        valor,
        modulo_id,
        fecha_novedad,
        periodo_nomina_id
    )
    VALUES (
        p_contrato_id,
        p_tipo_nomina_id,
        p_anio,
        p_mes,
        p_periodo,
        p_fecha_inicio,
        p_fecha_fin,
        p_concepto_id,
        unidades,
        v_base,
        v_salario,
        p_modulo_id,
        p_fecha_fin,
        p_periodo_nomina
    );

    END IF;

    INSERT INTO t_log_nomina (proceso_id, origen, mensaje)
    VALUES (p_proceso_id,'prc_1012_00','Inserta OK');

END;
$$;


ALTER PROCEDURE public.prc_1012_00(IN p_empresa_id integer, IN p_contrato_id integer, IN p_tipo_nomina_id integer, IN p_anio integer, IN p_mes integer, IN p_periodo integer, IN p_fecha_inicio date, IN p_fecha_fin date, IN p_concepto_id integer, IN p_proceso_id integer, IN p_modulo_id integer, IN p_periodo_nomina integer, IN p_sin_valor character varying) OWNER TO postgres;

--
-- Name: prc_11000_00(integer, integer, integer, integer, integer, integer, date, date, integer, integer, integer, integer, character varying); Type: PROCEDURE; Schema: public; Owner: postgres
--

CREATE PROCEDURE public.prc_11000_00(IN p_empresa_id integer, IN p_contrato_id integer, IN p_tipo_nomina_id integer, IN p_anio integer, IN p_mes integer, IN p_periodo integer, IN p_fecha_inicio date, IN p_fecha_fin date, IN p_concepto_id integer, IN p_proceso_id integer, IN p_modulo_id integer, IN p_periodo_nomina integer, IN p_sin_valor character varying)
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_total NUMERIC;
    v_devengos NUMERIC;
    v_deducciones NUMERIC;
    v_modulo BIGINT;
BEGIN
    
    v_devengos := public.fn_sumatoria_devengos(p_empresa_id,p_contrato_id, p_tipo_nomina_id, p_periodo, p_anio, p_mes);
    
    INSERT INTO t_log_nomina (proceso_id, origen, mensaje)
    VALUES (p_proceso_id,'prc_10000_00','devengos=' || COALESCE(v_devengos::TEXT, 'NULL'));

    
    v_deducciones := public.fn_sumatoria_deducciones(p_empresa_id,p_contrato_id, p_tipo_nomina_id, p_periodo, p_anio, p_mes);
    
    
    INSERT INTO t_log_nomina (proceso_id, origen, mensaje)
    VALUES (p_proceso_id,'prc_10000_00','deducciones=' || COALESCE(v_deducciones::TEXT, 'NULL'));

    
    v_total := v_devengos -v_deducciones;


    INSERT INTO "gestionNomina_t_acumulado_empleado" (
        contrato_id,
        tipo_nomina_id,
        anio,
        mes,
        periodo,
        fecha_inicio,
        fecha_fin,
        concepto_id,
        unidad,
        base,
        valor,
        modulo_id,
        fecha_novedad,
        periodo_nomina_id
    )
    VALUES (
        p_contrato_id,
        p_tipo_nomina_id,
        p_anio,
        p_mes,
        p_periodo,
        p_fecha_inicio,
        p_fecha_fin,
        p_concepto_id,
        30,
        v_total,
        v_total,
        p_modulo_id,
        p_fecha_fin,
        p_periodo_nomina
    );

    INSERT INTO t_log_nomina (proceso_id, origen, mensaje)
    VALUES (p_proceso_id,'prc_11000_00','Inserta OK');


END;
$$;


ALTER PROCEDURE public.prc_11000_00(IN p_empresa_id integer, IN p_contrato_id integer, IN p_tipo_nomina_id integer, IN p_anio integer, IN p_mes integer, IN p_periodo integer, IN p_fecha_inicio date, IN p_fecha_fin date, IN p_concepto_id integer, IN p_proceso_id integer, IN p_modulo_id integer, IN p_periodo_nomina integer, IN p_sin_valor character varying) OWNER TO postgres;

--
-- Name: prc_1200_00(integer, integer, integer, integer, integer, integer, date, date, integer, integer, integer, integer, character varying); Type: PROCEDURE; Schema: public; Owner: postgres
--

CREATE PROCEDURE public.prc_1200_00(IN p_empresa_id integer, IN p_contrato_id integer, IN p_tipo_nomina_id integer, IN p_anio integer, IN p_mes integer, IN p_periodo integer, IN p_fecha_inicio date, IN p_fecha_fin date, IN p_concepto_id integer, IN p_proceso_id integer, IN p_modulo_id integer, IN p_periodo_nomina integer, IN p_sin_valor character varying)
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_auxtr NUMERIC;
    v_modulo BIGINT;
    f_ini DATE;
    f_fin DATE;
    unidades NUMERIC;
    unidades_per NUMERIC;
    tope_aux NUMERIC;
    smlmv NUMERIC;
    v_salario NUMERIC;

BEGIN
    INSERT INTO t_log_nomina (proceso_id, origen, mensaje)
    VALUES (p_proceso_id,'prc_1200_00','Inicio contrato=' || p_contrato_id || ' concepto=' || p_concepto_id);
    
    select valor_numerico 
    into v_auxtr
    from parametros_parametrodetalle 
    where parametro_id in(select id 
                      from parametros_parametrogeneral
                      where codigo = 'P_SIS') AND
    codigo = 'AUXTR';

    select valor_numerico 
    into tope_aux
    from parametros_parametrodetalle 
    where parametro_id in(select id 
                      from parametros_parametrogeneral
                      where codigo = 'P_SIS') AND
    codigo = 'TOPAUX';

    select valor_numerico 
    into smlmv
    from parametros_parametrodetalle 
    where parametro_id in(select id 
                      from parametros_parametrogeneral
                      where codigo = 'P_SIS') AND
    codigo = 'SMLMV';

    select fecha_ingreso, fecha_fin 
    into f_ini, f_fin
    from "gestionContratos_t_contrato"
    where empresa_id = p_empresa_id AND
    id = p_contrato_id AND
    estado = 'A';

    SELECT cs.salario
    INTO v_salario
    FROM "gestionContratos_t_contrato_salario" cs
    WHERE cs.contrato_id = p_contrato_id
      AND cs.estado = TRUE
      AND cs.tipo_salario_id in (select id                      
                                 from "parametros_t_tipo_salario" 
                                 where salario = 'BASICO')
    ORDER BY cs.fecha_inicio DESC
    LIMIT 1;

    tope_aux := tope_aux * smlmv;

    IF v_salario <= tope_aux THEN
    
    unidades_per := public.fn_dias_laborales_nomina(p_fecha_inicio,p_fecha_fin);

    v_auxtr := v_auxtr/unidades_per;
    
    --VALIDAR QUE LA FECHA INICIO DEL CONTRATO NO SEA MAYOR AL INICIO DEL PERIODO SI ES MAYOR REEMPLAZAR
    IF f_ini >  p_fecha_inicio AND f_ini <= p_fecha_fin THEN
        p_fecha_inicio := f_ini;
    END IF;    
    --VALIDAR QUE LA FECHA FIN DEL CONTRATO NO SEA MAYOR AL INICIO DEL PERIODO SI ES MAYOR REEMPLAZAR
    IF f_fin <  p_fecha_fin AND f_fin >= p_fecha_inicio THEN
        p_fecha_fin := f_fin;
    END IF;

    unidades = public.fn_dias_laborales_nomina(p_fecha_inicio,p_fecha_fin);
    v_auxtr := v_auxtr*unidades;

    INSERT INTO t_log_nomina (proceso_id, origen, mensaje)
    VALUES (p_proceso_id,'prc_1200_00','Unidades=' || COALESCE(unidades::TEXT, 'NULL'));

    IF p_sin_valor = 'NB' and v_auxtr = 0 THEN

    INSERT INTO "gestionNomina_t_acumulado_empleado" (
        contrato_id,
        tipo_nomina_id,
        anio,
        mes,
        periodo,
        fecha_inicio,
        fecha_fin,
        concepto_id,
        unidad,
        base,
        valor,
        modulo_id,
        fecha_novedad,
        periodo_nomina_id
    )
    VALUES (
        p_contrato_id,
        p_tipo_nomina_id,
        p_anio,
        p_mes,
        p_periodo,
        p_fecha_inicio,
        p_fecha_fin,
        p_concepto_id,
        unidades,
        v_auxtr,
        v_auxtr,
        p_modulo_id,
        p_fecha_fin,
        p_periodo_nomina
    );

    ELSEIF p_sin_valor = 'BO' and v_auxtr = 0 THEN

    INSERT INTO t_log_nomina (proceso_id, origen, mensaje)
    VALUES (p_proceso_id,'prc_1200_00','BORRAR LINEA');

    ELSE

    INSERT INTO "gestionNomina_t_acumulado_empleado" (
        contrato_id,
        tipo_nomina_id,
        anio,
        mes,
        periodo,
        fecha_inicio,
        fecha_fin,
        concepto_id,
        unidad,
        base,
        valor,
        modulo_id,
        fecha_novedad,
        periodo_nomina_id
    )
    VALUES (
        p_contrato_id,
        p_tipo_nomina_id,
        p_anio,
        p_mes,
        p_periodo,
        p_fecha_inicio,
        p_fecha_fin,
        p_concepto_id,
        unidades,
        v_auxtr,
        v_auxtr,
        p_modulo_id,
        p_fecha_fin,
        p_periodo_nomina
    );

    END IF;

    END IF;

    INSERT INTO t_log_nomina (proceso_id, origen, mensaje)
    VALUES (p_proceso_id,'prc_1200_00','Inserta OK');


END;
$$;


ALTER PROCEDURE public.prc_1200_00(IN p_empresa_id integer, IN p_contrato_id integer, IN p_tipo_nomina_id integer, IN p_anio integer, IN p_mes integer, IN p_periodo integer, IN p_fecha_inicio date, IN p_fecha_fin date, IN p_concepto_id integer, IN p_proceso_id integer, IN p_modulo_id integer, IN p_periodo_nomina integer, IN p_sin_valor character varying) OWNER TO postgres;

--
-- Name: prc_5098_00(integer, integer, integer, integer, integer, integer, date, date, integer, integer, integer, integer, character varying); Type: PROCEDURE; Schema: public; Owner: postgres
--

CREATE PROCEDURE public.prc_5098_00(IN p_empresa_id integer, IN p_contrato_id integer, IN p_tipo_nomina_id integer, IN p_anio integer, IN p_mes integer, IN p_periodo integer, IN p_fecha_inicio date, IN p_fecha_fin date, IN p_concepto_id integer, IN p_proceso_id integer, IN p_modulo_id integer, IN p_periodo_nomina integer, IN p_sin_valor character varying)
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_valor NUMERIC;
    v_modulo BIGINT;
    v_t_salario VARCHAR;
    v_base NUMERIC;
    v_porc_base NUMERIC;
    v_porc_salud NUMERIC;
    v_ibc_min NUMERIC;
    v_smlmv NUMERIC;
    v_minibc NUMERIC;
    v_topibc NUMERIC;
    v_intibc NUMERIC;


BEGIN


    SELECT SUM(smlmv) smlmv, SUM(minibc) minibc, SUM(topibc) topibc, SUM(intibc) intibc 
    INTO v_smlmv,v_minibc,v_topibc, v_intibc
    FROM(
    select valor_numerico as SMLMV, 0 MINIBC, 0 TOPIBC, 0 INTIBC 
    from parametros_parametrodetalle 
    where parametro_id in(select id 
                      from parametros_parametrogeneral 
                      where codigo = 'P_SIS') AND
    codigo = 'SMLMV' 
    UNION
    select 0 SMLMV, 0 MINIBC, valor_numerico TOPIBC, 0 INTIBC 
    from parametros_parametrodetalle 
    where parametro_id in(select id 
                      from parametros_parametrogeneral 
                      where codigo = 'P_SIS') AND
    codigo = 'TOPIBC'
    UNION
    select 0 SMLMV, valor_numerico MINIBC, 0 TOPIBC, 0 INTIBC 
    from parametros_parametrodetalle 
    where parametro_id in(select id 
                      from parametros_parametrogeneral 
                      where codigo = 'P_SIS') AND
    codigo = 'MINIBC'
    UNION
    select 0 SMLMV, 0 MINIBC, 0 TOPIBC, valor_numerico INTIBC 
    from parametros_parametrodetalle 
    where parametro_id in(select id 
                      from parametros_parametrogeneral 
                      where codigo = 'P_SIS') AND
    codigo = 'INTIBC'); 

    INSERT INTO t_log_nomina (proceso_id, origen, mensaje)
    VALUES (p_proceso_id,'prc_5098_00','Inicio contrato=' || p_contrato_id || ' concepto=' || p_concepto_id);
    
    SELECT ts.salario
    INTO v_t_salario
    FROM "gestionContratos_t_contrato_salario" cs
    INNER JOIN "parametros_t_tipo_salario" ts ON cs.tipo_salario_id = ts.id
    WHERE cs.contrato_id = p_contrato_id AND
          cs.estado = TRUE;

    v_base := public.fn_sumatoria_grupo_conceptos(p_contrato_id, p_fecha_inicio, p_fecha_fin, 'BAS_SS');
    v_porc_base := 100;

    INSERT INTO t_log_nomina (proceso_id, origen, mensaje)
    VALUES (p_proceso_id,'prc_5098_00','Base=' || COALESCE(v_base::TEXT, 'NULL'));

    IF v_t_salario = 'INTEGRAL' THEN
        v_porc_base := v_intibc;        
    END IF;


    select valor_numerico
    into v_porc_salud 
    from parametros_parametrodetalle 
    where parametro_id in(select id 
                      from parametros_parametrogeneral 
                      where codigo = 'P_SAL')
    AND codigo = 'SAL_TR';

    
    INSERT INTO t_log_nomina (proceso_id, origen, mensaje)
    VALUES (p_proceso_id,'prc_5098_00','porcentaje salud=' || COALESCE(v_porc_salud ::TEXT, 'NULL'));

    v_base :=  v_base * (v_porc_base/100);

    IF v_base < (v_ibc_min*v_smlmv) THEN
        v_base := v_ibc_min*v_smlmv;
    END IF;

    IF v_base > (v_topibc*v_smlmv) THEN
        v_base := (v_topibc*v_smlmv);
    END IF;

    v_valor := v_base  * (v_porc_salud/100);
    
    IF p_sin_valor = 'NB' and v_valor = 0 THEN

    INSERT INTO "gestionNomina_t_acumulado_empleado" (
        contrato_id,
        tipo_nomina_id,
        anio,
        mes,
        periodo,
        fecha_inicio,
        fecha_fin,
        concepto_id,
        unidad,
        base,
        valor,
        modulo_id,
        fecha_novedad,
        periodo_nomina_id
    )
    VALUES (
        p_contrato_id,
        p_tipo_nomina_id,
        p_anio,
        p_mes,
        p_periodo,
        p_fecha_inicio,
        p_fecha_fin,
        p_concepto_id,
        30,
        v_base,
        v_valor,
        p_modulo_id,
        p_fecha_fin,
        p_periodo_nomina
    );

    ELSEIF p_sin_valor = 'BO' and v_valor = 0 THEN

    INSERT INTO t_log_nomina (proceso_id, origen, mensaje)
    VALUES (p_proceso_id,'prc_5098_00','BORRAR LINEA');

    ELSE

    INSERT INTO "gestionNomina_t_acumulado_empleado" (
        contrato_id,
        tipo_nomina_id,
        anio,
        mes,
        periodo,
        fecha_inicio,
        fecha_fin,
        concepto_id,
        unidad,
        base,
        valor,
        modulo_id,
        fecha_novedad,
        periodo_nomina_id
    )
    VALUES (
        p_contrato_id,
        p_tipo_nomina_id,
        p_anio,
        p_mes,
        p_periodo,
        p_fecha_inicio,
        p_fecha_fin,
        p_concepto_id,
        30,
        v_base,
        v_valor,
        p_modulo_id,
        p_fecha_fin,
        p_periodo_nomina
    );

    END IF;
    INSERT INTO t_log_nomina (proceso_id, origen, mensaje)
    VALUES (p_proceso_id,'prc_5098_00','Inserta OK');


END;
$$;


ALTER PROCEDURE public.prc_5098_00(IN p_empresa_id integer, IN p_contrato_id integer, IN p_tipo_nomina_id integer, IN p_anio integer, IN p_mes integer, IN p_periodo integer, IN p_fecha_inicio date, IN p_fecha_fin date, IN p_concepto_id integer, IN p_proceso_id integer, IN p_modulo_id integer, IN p_periodo_nomina integer, IN p_sin_valor character varying) OWNER TO postgres;

--
-- Name: prc_5198_00(integer, integer, integer, integer, integer, integer, date, date, integer, integer, integer, integer, character varying); Type: PROCEDURE; Schema: public; Owner: postgres
--

CREATE PROCEDURE public.prc_5198_00(IN p_empresa_id integer, IN p_contrato_id integer, IN p_tipo_nomina_id integer, IN p_anio integer, IN p_mes integer, IN p_periodo integer, IN p_fecha_inicio date, IN p_fecha_fin date, IN p_concepto_id integer, IN p_proceso_id integer, IN p_modulo_id integer, IN p_periodo_nomina integer, IN p_sin_valor character varying)
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_valor NUMERIC;
    v_modulo BIGINT;
    v_t_salario VARCHAR;
    v_base NUMERIC;
    v_porc_base NUMERIC;
    v_porc_pension NUMERIC;
    v_ibc_min NUMERIC;
    v_smlmv NUMERIC;
    v_minibc NUMERIC;
    v_topibc NUMERIC;
    v_intibc NUMERIC;


BEGIN

    SELECT SUM(smlmv) smlmv, SUM(minibc) minibc, SUM(topibc) topibc, SUM(intibc) intibc 
    INTO v_smlmv,v_minibc,v_topibc, v_intibc
    FROM(
    select valor_numerico as SMLMV, 0 MINIBC, 0 TOPIBC, 0 INTIBC 
    from parametros_parametrodetalle 
    where parametro_id in(select id 
                      from parametros_parametrogeneral 
                      where codigo = 'P_SIS') AND
    codigo = 'SMLMV' 
    UNION
    select 0 SMLMV, 0 MINIBC, valor_numerico TOPIBC, 0 INTIBC 
    from parametros_parametrodetalle 
    where parametro_id in(select id 
                      from parametros_parametrogeneral 
                      where codigo = 'P_SIS') AND
    codigo = 'TOPIBC'
    UNION
    select 0 SMLMV, valor_numerico MINIBC, 0 TOPIBC, 0 INTIBC 
    from parametros_parametrodetalle 
    where parametro_id in(select id 
                      from parametros_parametrogeneral 
                      where codigo = 'P_SIS') AND
    codigo = 'MINIBC'
    UNION
    select 0 SMLMV, 0 MINIBC, 0 TOPIBC, valor_numerico INTIBC 
    from parametros_parametrodetalle 
    where parametro_id in(select id 
                      from parametros_parametrogeneral 
                      where codigo = 'P_SIS') AND
    codigo = 'INTIBC'); 

    INSERT INTO t_log_nomina (proceso_id, origen, mensaje)
    VALUES (p_proceso_id,'prc_5198_00','Inicio contrato=' || p_contrato_id || ' concepto=' || p_concepto_id);
    
    SELECT ts.salario
    INTO v_t_salario
    FROM "gestionContratos_t_contrato_salario" cs
    INNER JOIN "parametros_t_tipo_salario" ts ON cs.tipo_salario_id = ts.id
    WHERE cs.contrato_id = p_contrato_id AND
          cs.estado = TRUE;

    v_base := public.fn_sumatoria_grupo_conceptos(p_contrato_id, p_fecha_inicio, p_fecha_fin, 'BAS_SS');
    v_porc_base := 100;

    INSERT INTO t_log_nomina (proceso_id, origen, mensaje)
    VALUES (p_proceso_id,'prc_5198_00','Base=' || COALESCE(v_base::TEXT, 'NULL'));

    IF v_t_salario = 'INTEGRAL' THEN
        v_porc_base := v_intibc;        
    END IF;

    select valor_numerico
    into v_porc_pension 
    from parametros_parametrodetalle 
    where parametro_id in(select id 
                      from parametros_parametrogeneral 
                      where codigo = 'P_PEN')
    AND codigo = 'PEN_TR';

    
    INSERT INTO t_log_nomina (proceso_id, origen, mensaje)
    VALUES (p_proceso_id,'prc_5198_00','porcentaje pension=' || COALESCE(v_porc_pension ::TEXT, 'NULL'));

    v_base :=  v_base * (v_porc_base/100);

    IF v_base < (v_ibc_min*v_smlmv) THEN
        v_base := v_ibc_min*v_smlmv;
    END IF;

    IF v_base > (v_topibc*v_smlmv) THEN
        v_base := (v_topibc*v_smlmv);
    END IF;

    v_valor := v_base  * (v_porc_pension/100);
    
    
    IF p_sin_valor = 'NB' and v_valor = 0 THEN

    INSERT INTO "gestionNomina_t_acumulado_empleado" (
        contrato_id,
        tipo_nomina_id,
        anio,
        mes,
        periodo,
        fecha_inicio,
        fecha_fin,
        concepto_id,
        unidad,
        base,
        valor,
        modulo_id,
        fecha_novedad,
        periodo_nomina_id
    )
    VALUES (
        p_contrato_id,
        p_tipo_nomina_id,
        p_anio,
        p_mes,
        p_periodo,
        p_fecha_inicio,
        p_fecha_fin,
        p_concepto_id,
        30,
        v_base,
        v_valor,
        p_modulo_id,
        p_fecha_fin,
        p_periodo_nomina
    );

    ELSEIF p_sin_valor = 'BO' and v_valor = 0 THEN

    INSERT INTO t_log_nomina (proceso_id, origen, mensaje)
    VALUES (p_proceso_id,'prc_5198_00','BORRAR LINEA');

    ELSE

    INSERT INTO "gestionNomina_t_acumulado_empleado" (
        contrato_id,
        tipo_nomina_id,
        anio,
        mes,
        periodo,
        fecha_inicio,
        fecha_fin,
        concepto_id,
        unidad,
        base,
        valor,
        modulo_id,
        fecha_novedad,
        periodo_nomina_id
    )
    VALUES (
        p_contrato_id,
        p_tipo_nomina_id,
        p_anio,
        p_mes,
        p_periodo,
        p_fecha_inicio,
        p_fecha_fin,
        p_concepto_id,
        30,
        v_base,
        v_valor,
        p_modulo_id,
        p_fecha_fin,
        p_periodo_nomina
    );

    END IF;

    INSERT INTO t_log_nomina (proceso_id, origen, mensaje)
    VALUES (p_proceso_id,'prc_5198_00','Inserta OK');


END;
$$;


ALTER PROCEDURE public.prc_5198_00(IN p_empresa_id integer, IN p_contrato_id integer, IN p_tipo_nomina_id integer, IN p_anio integer, IN p_mes integer, IN p_periodo integer, IN p_fecha_inicio date, IN p_fecha_fin date, IN p_concepto_id integer, IN p_proceso_id integer, IN p_modulo_id integer, IN p_periodo_nomina integer, IN p_sin_valor character varying) OWNER TO postgres;

--
-- Name: prc_5298_00(integer, integer, integer, integer, integer, integer, date, date, integer, integer, integer, integer, character varying); Type: PROCEDURE; Schema: public; Owner: postgres
--

CREATE PROCEDURE public.prc_5298_00(IN p_empresa_id integer, IN p_contrato_id integer, IN p_tipo_nomina_id integer, IN p_anio integer, IN p_mes integer, IN p_periodo integer, IN p_fecha_inicio date, IN p_fecha_fin date, IN p_concepto_id integer, IN p_proceso_id integer, IN p_modulo_id integer, IN p_periodo_nomina integer, IN p_sin_valor character varying)
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_valor NUMERIC;
    v_modulo BIGINT;
    v_t_salario VARCHAR;
    v_base NUMERIC;
    v_porc_base NUMERIC;
    v_porc_solidaridad NUMERIC;
    v_ibc_min NUMERIC;
    v_smlmv NUMERIC;
    v_minibc NUMERIC;
    v_topibc NUMERIC;
    v_intibc NUMERIC;


BEGIN

    SELECT SUM(smlmv) smlmv, SUM(minibc) minibc, SUM(topibc) topibc, SUM(intibc) intibc 
    INTO v_smlmv,v_minibc,v_topibc, v_intibc
    FROM(
    select valor_numerico as SMLMV, 0 MINIBC, 0 TOPIBC, 0 INTIBC 
    from parametros_parametrodetalle 
    where parametro_id in(select id 
                      from parametros_parametrogeneral 
                      where codigo = 'P_SIS') AND
    codigo = 'SMLMV' 
    UNION
    select 0 SMLMV, 0 MINIBC, valor_numerico TOPIBC, 0 INTIBC 
    from parametros_parametrodetalle 
    where parametro_id in(select id 
                      from parametros_parametrogeneral 
                      where codigo = 'P_SIS') AND
    codigo = 'TOPIBC'
    UNION
    select 0 SMLMV, valor_numerico MINIBC, 0 TOPIBC, 0 INTIBC 
    from parametros_parametrodetalle 
    where parametro_id in(select id 
                      from parametros_parametrogeneral 
                      where codigo = 'P_SIS') AND
    codigo = 'MINIBC'
    UNION
    select 0 SMLMV, 0 MINIBC, 0 TOPIBC, valor_numerico INTIBC 
    from parametros_parametrodetalle 
    where parametro_id in(select id 
                      from parametros_parametrogeneral 
                      where codigo = 'P_SIS') AND
    codigo = 'INTIBC'); 

    INSERT INTO t_log_nomina (proceso_id, origen, mensaje)
    VALUES (p_proceso_id,'prc_5298_00','Inicio contrato=' || p_contrato_id || ' concepto=' || p_concepto_id);
    
    SELECT ts.salario
    INTO v_t_salario
    FROM "gestionContratos_t_contrato_salario" cs
    INNER JOIN "parametros_t_tipo_salario" ts ON cs.tipo_salario_id = ts.id
    WHERE cs.contrato_id = p_contrato_id AND
          cs.estado = TRUE;

    v_base := public.fn_sumatoria_grupo_conceptos(p_contrato_id, p_fecha_inicio, p_fecha_fin, 'BAS_SS');
    v_porc_base := 100;

    INSERT INTO t_log_nomina (proceso_id, origen, mensaje)
    VALUES (p_proceso_id,'prc_5298_00','Base=' || COALESCE(v_base::TEXT, 'NULL'));

    IF v_t_salario = 'INTEGRAL' THEN
        v_porc_base := v_intibc;        
    END IF;

    v_base :=  v_base * (v_porc_base/100);

    v_porc_solidaridad := COALESCE(fn_porc_solidaridad(v_base),0);

    INSERT INTO t_log_nomina (proceso_id, origen, mensaje)
    VALUES (p_proceso_id,'prc_5298_00','porcentaje solidaridad=' || COALESCE(v_porc_solidaridad ::TEXT, 'NULL'));


    IF v_base < (v_ibc_min*v_smlmv) THEN
        v_base := v_ibc_min*v_smlmv;
    END IF;

    IF v_base > (v_topibc*v_smlmv) THEN
        v_base := (v_topibc*v_smlmv);
    END IF;

    if v_porc_solidaridad <> 0 then
    v_valor := v_base  * (v_porc_solidaridad/100);
    else
    v_valor := 0;
    end if;
    
    
    IF p_sin_valor = 'NB' and v_valor = 0 THEN

    INSERT INTO "gestionNomina_t_acumulado_empleado" (
        contrato_id,
        tipo_nomina_id,
        anio,
        mes,
        periodo,
        fecha_inicio,
        fecha_fin,
        concepto_id,
        unidad,
        base,
        valor,
        modulo_id,
        fecha_novedad,
        periodo_nomina_id
    )
    VALUES (
        p_contrato_id,
        p_tipo_nomina_id,
        p_anio,
        p_mes,
        p_periodo,
        p_fecha_inicio,
        p_fecha_fin,
        p_concepto_id,
        30,
        v_base,
        v_valor,
        p_modulo_id,
        p_fecha_fin,
        p_periodo_nomina
    );

    ELSEIF p_sin_valor = 'BO' and v_valor = 0 THEN

    INSERT INTO t_log_nomina (proceso_id, origen, mensaje)
    VALUES (p_proceso_id,'prc_5298_00','BORRAR LINEA');

    ELSE

    INSERT INTO "gestionNomina_t_acumulado_empleado" (
        contrato_id,
        tipo_nomina_id,
        anio,
        mes,
        periodo,
        fecha_inicio,
        fecha_fin,
        concepto_id,
        unidad,
        base,
        valor,
        modulo_id,
        fecha_novedad,
        periodo_nomina_id
    )
    VALUES (
        p_contrato_id,
        p_tipo_nomina_id,
        p_anio,
        p_mes,
        p_periodo,
        p_fecha_inicio,
        p_fecha_fin,
        p_concepto_id,
        30,
        v_base,
        v_valor,
        p_modulo_id,
        p_fecha_fin,
        p_periodo_nomina
    );

    END IF;

    INSERT INTO t_log_nomina (proceso_id, origen, mensaje)
    VALUES (p_proceso_id,'prc_5298_00','Inserta OK');


END;
$$;


ALTER PROCEDURE public.prc_5298_00(IN p_empresa_id integer, IN p_contrato_id integer, IN p_tipo_nomina_id integer, IN p_anio integer, IN p_mes integer, IN p_periodo integer, IN p_fecha_inicio date, IN p_fecha_fin date, IN p_concepto_id integer, IN p_proceso_id integer, IN p_modulo_id integer, IN p_periodo_nomina integer, IN p_sin_valor character varying) OWNER TO postgres;

--
-- Name: prc_cierre_nomina(integer, integer, integer, integer, integer, date, date, integer, integer); Type: PROCEDURE; Schema: public; Owner: postgres
--

CREATE PROCEDURE public.prc_cierre_nomina(IN p_empresa_id integer, IN p_tipo_nomina_id integer, IN p_anio integer, IN p_mes integer, IN p_periodo integer, IN p_fecha_inicio date, IN p_fecha_fin date, IN p_proceso_id integer, IN p_periodo_nomina integer)
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_contrato RECORD;
    v_concepto RECORD;
    v_sql TEXT;
    v_total_contratos INTEGER;
    v_contratos_procesados INTEGER := 0;
    v_progreso INTEGER;
BEGIN    
    INSERT INTO t_log_nomina (proceso_id, origen, mensaje)
    VALUES (p_proceso_id,'prc_cierre_nomina','Inicio procesamiento empresa=' || p_empresa_id);

    SELECT COUNT(*)
    INTO v_total_contratos
    FROM "gestionContratos_t_contrato" c
    WHERE c.empresa_id = p_empresa_id
    AND c.tipo_nomina_id = p_tipo_nomina_id
    AND c.fecha_ingreso <= p_fecha_fin 
    AND c.estado = 'A';

    UPDATE "gestionNomina_t_proceso_nomina"
    SET progreso = 0
    WHERE id = p_proceso_id;
    COMMIT;


    FOR v_contrato IN
        SELECT c.id
        FROM  "gestionContratos_t_contrato" c
        WHERE c.empresa_id = p_empresa_id
          AND c.tipo_nomina_id = p_tipo_nomina_id
          AND c.fecha_ingreso <= p_fecha_fin 
          AND c.estado = 'A'
    LOOP

        INSERT INTO "gestionNomina_t_acumulado_empleado_def" (
        contrato_id,tipo_nomina_id,anio,mes,periodo,
        fecha_novedad,fecha_inicio,fecha_fin,concepto_id,
        unidad,base,valor,modulo_id,periodo_nomina_id,
        t01, v01, t02, v02, t03, v03, t04, v04, t05, v05,
        t06, v06, t07, v07, t08, v08, t09, v09, t10, v10,
        t11, v11, t12, v12, t13, v13, t14, v14, t15, v15,
        t16, v16, t17, v17, t18, v18, t19, v19, t20, v20,
        ft01, f01, ft02, f02, ft03, f03, ft04, f04)
        SELECT
        contrato_id,tipo_nomina_id,anio,mes,periodo,
        fecha_novedad,fecha_inicio,fecha_fin,concepto_id,
        unidad,base,valor,modulo_id,periodo_nomina_id,
        t01, v01, t02, v02, t03, v03, t04, v04, t05, v05,
        t06, v06, t07, v07, t08, v08, t09, v09, t10, v10,
        t11, v11, t12, v12, t13, v13, t14, v14, t15, v15,
        t16, v16, t17, v17, t18, v18, t19, v19, t20, v20,
        ft01, f01, ft02, f02, ft03, f03, ft04, f04
        FROM "gestionNomina_t_acumulado_empleado"
        WHERE contrato_id = v_contrato.id
        AND anio = p_anio
        AND mes = p_mes
        AND periodo = p_periodo
        AND periodo_nomina_id = p_periodo_nomina;

        DELETE FROM "gestionNomina_t_acumulado_empleado"
        WHERE contrato_id = v_contrato.id
        AND anio = p_anio
        AND mes = p_mes
        AND periodo = p_periodo
        AND periodo_nomina_id = p_periodo_nomina;
       
    v_contratos_procesados := v_contratos_procesados + 1;
    v_progreso := CEIL((v_contratos_procesados::NUMERIC / v_total_contratos) * 100);

    UPDATE "gestionNomina_t_proceso_nomina"
    SET progreso = LEAST(v_progreso, 100)
    WHERE id = p_proceso_id;
    COMMIT;
    
    END LOOP;
    
    INSERT INTO t_log_nomina (proceso_id, origen, mensaje)
    VALUES (p_proceso_id,'prc_cierre_nomina','Fin');
    
    UPDATE "gestionNomina_t_proceso_nomina"
    SET progreso = 100
    WHERE id = p_proceso_id;

    UPDATE "gestionNomina_t_periodo_nomina"
    SET estado = FALSE
    WHERE id = p_periodo_nomina;

END;
$$;


ALTER PROCEDURE public.prc_cierre_nomina(IN p_empresa_id integer, IN p_tipo_nomina_id integer, IN p_anio integer, IN p_mes integer, IN p_periodo integer, IN p_fecha_inicio date, IN p_fecha_fin date, IN p_proceso_id integer, IN p_periodo_nomina integer) OWNER TO postgres;

--
-- Name: prc_nov_00(integer, integer, integer, integer, integer, integer, date, date, integer, integer, integer, integer, character varying); Type: PROCEDURE; Schema: public; Owner: postgres
--

CREATE PROCEDURE public.prc_nov_00(IN p_empresa_id integer, IN p_contrato_id integer, IN p_tipo_nomina_id integer, IN p_anio integer, IN p_mes integer, IN p_periodo integer, IN p_fecha_inicio date, IN p_fecha_fin date, IN p_concepto_id integer, IN p_proceso_id integer, IN p_modulo_id integer, IN p_periodo_nomina integer, IN p_sin_valor character varying)
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_novedad RECORD;
    v_salario NUMERIC;
    v_jornada NUMERIC;
    v_porcentaje NUMERIC;
    v_modulo BIGINT;
    f_ini DATE;
    f_fin DATE;
    unidades NUMERIC;
    base NUMERIC;
    v_valor NUMERIC;
    v_base NUMERIC;
    v_unidades NUMERIC;

BEGIN
    INSERT INTO t_log_nomina (proceso_id, origen, mensaje)
    VALUES (p_proceso_id,'prc_nov_00','Inicio contrato=' || p_contrato_id || ' concepto=' || p_concepto_id);

    SELECT cs.salario
    INTO v_salario
    FROM "gestionContratos_t_contrato_salario" cs
    WHERE cs.contrato_id = p_contrato_id
      AND cs.estado = TRUE
      AND cs.tipo_salario_id in (select id                      
                                 from "parametros_t_tipo_salario" 
                                 where salario in ('BASICO','INTEGRAL'))
    ORDER BY cs.fecha_inicio DESC
    LIMIT 1;


    select valor_numerico
    into v_jornada
    from parametros_parametrodetalle 
    where parametro_id in(select id 
                      from public.parametros_parametrogeneral 
                      where codigo = 'P_SIS') AND
    codigo = 'JORLAB';

    select COALESCE(valor_numerico,0)
    into v_porcentaje
    from parametros_parametrodetalle 
    where parametro_id in(select id 
                      from public.parametros_parametrogeneral 
                      where codigo = 'P_EXTR') AND
    valor_texto in (SELECT c.cod_concepto
                    FROM "gestionNomina_t_logica_calculo" lc, 
                         "gestionConceptos_t_concepto_empresa" ce,
                         "gestionConceptos_t_conceptos" c
                    WHERE lc.concepto_id = ce.id
                    AND ce.cod_concepto_id = c.id
                    AND ce.empresa_id = p_empresa_id
                    AND lc.concepto_id = p_concepto_id
                    AND lc.tipo_nomina_id = p_tipo_nomina_id
                    AND lc.periodo = p_periodo
                    AND lc.logica IS NOT NULL) ;

    FOR v_novedad IN
        select  nt.unidad, nt.base, nt.valor, nt.fecha_novedad
        from "gestionNovedades_t_novedad_temporal" as nt
        where nt.contrato_id = p_contrato_id AND
        nt.anio = p_anio AND
        nt.mes = p_mes AND
        nt.periodo = p_periodo AND
        nt.concepto_id = p_concepto_id AND
        (nt.periodo_nomina_id = p_periodo_nomina or nt.fecha_novedad BETWEEN p_fecha_inicio and  p_fecha_fin)
    LOOP
 
    
    v_valor := v_novedad.valor;
    v_base :=  v_novedad.base;
    v_unidades := v_novedad.unidad;
    
    IF v_porcentaje <> 0 THEN
        v_base := (v_salario/v_jornada) * v_porcentaje;
        v_valor :=v_base * v_unidades;
    END IF;


    IF p_sin_valor = 'NB' and v_valor = 0 THEN

    INSERT INTO "gestionNomina_t_acumulado_empleado" (
        contrato_id,
        tipo_nomina_id,
        anio,
        mes,
        periodo,
        fecha_inicio,
        fecha_fin,
        concepto_id,
        unidad,
        base,
        valor,
        modulo_id,
        fecha_novedad,
        periodo_nomina_id
    )
    VALUES (
        p_contrato_id,
        p_tipo_nomina_id,
        p_anio,
        p_mes,
        p_periodo,
        p_fecha_inicio,
        p_fecha_fin,
        p_concepto_id,
        v_unidades,
        v_base,
        v_valor,
        p_modulo_id,
        v_novedad.fecha_novedad,
        p_periodo_nomina
    );

    ELSEIF p_sin_valor = 'BO' and v_valor = 0 THEN

    INSERT INTO t_log_nomina (proceso_id, origen, mensaje)
    VALUES (p_proceso_id,'prc_nov_00','BORRAR LINEA');

    ELSE

    INSERT INTO "gestionNomina_t_acumulado_empleado" (
        contrato_id,
        tipo_nomina_id,
        anio,
        mes,
        periodo,
        fecha_inicio,
        fecha_fin,
        concepto_id,
        unidad,
        base,
        valor,
        modulo_id,
        fecha_novedad,
        periodo_nomina_id
    )
    VALUES (
        p_contrato_id,
        p_tipo_nomina_id,
        p_anio,
        p_mes,
        p_periodo,
        p_fecha_inicio,
        p_fecha_fin,
        p_concepto_id,
        v_unidades,
        v_base,
        v_valor,
        p_modulo_id,
        v_novedad.fecha_novedad,
        p_periodo_nomina
    );

    END IF;
    
    END LOOP;

    INSERT INTO t_log_nomina (proceso_id, origen, mensaje)
    VALUES (p_proceso_id,'prc_nov_00','Inserta OK');



END;
$$;


ALTER PROCEDURE public.prc_nov_00(IN p_empresa_id integer, IN p_contrato_id integer, IN p_tipo_nomina_id integer, IN p_anio integer, IN p_mes integer, IN p_periodo integer, IN p_fecha_inicio date, IN p_fecha_fin date, IN p_concepto_id integer, IN p_proceso_id integer, IN p_modulo_id integer, IN p_periodo_nomina integer, IN p_sin_valor character varying) OWNER TO postgres;

--
-- Name: prc_procesar_nomina(integer, integer, integer, integer, integer, date, date, integer, integer); Type: PROCEDURE; Schema: public; Owner: postgres
--

CREATE PROCEDURE public.prc_procesar_nomina(IN p_empresa_id integer, IN p_tipo_nomina_id integer, IN p_anio integer, IN p_mes integer, IN p_periodo integer, IN p_fecha_inicio date, IN p_fecha_fin date, IN p_proceso_id integer, IN p_periodo_nomina integer)
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_contrato RECORD;
    v_concepto RECORD;
    v_sql TEXT;
    v_total_contratos INTEGER;
    v_contratos_procesados INTEGER := 0;
    v_progreso INTEGER;
BEGIN    
    INSERT INTO t_log_nomina (proceso_id, origen, mensaje)
    VALUES (p_proceso_id,'prc_procesar_nomina','Inicio procesamiento empresa=' || p_empresa_id);

    SELECT COUNT(*)
    INTO v_total_contratos
    FROM "gestionContratos_t_contrato" c
    WHERE c.empresa_id = p_empresa_id
    AND c.tipo_nomina_id = p_tipo_nomina_id
    AND c.fecha_ingreso <= p_fecha_fin 
    AND c.estado = 'A';

    UPDATE "gestionNomina_t_proceso_nomina"
    SET progreso = 0
    WHERE id = p_proceso_id;
    COMMIT;


    FOR v_contrato IN
        SELECT c.id
        FROM  "gestionContratos_t_contrato" c
        WHERE c.empresa_id = p_empresa_id
          AND c.tipo_nomina_id = p_tipo_nomina_id
          AND c.fecha_ingreso <= p_fecha_fin 
          AND c.estado = 'A'
    LOOP

        DELETE FROM "gestionNomina_t_acumulado_empleado"
        WHERE contrato_id = v_contrato.id
        AND anio = p_anio
        AND mes = p_mes
        AND periodo = p_periodo
        AND periodo_nomina_id = p_periodo_nomina;

        DELETE FROM t_log_nomina;

        INSERT INTO t_log_nomina (proceso_id, origen, mensaje)
        VALUES (p_proceso_id,'prc_procesar_nomina','Contrato encontrado id=' || v_contrato.id);

        FOR v_concepto IN
            SELECT c.cod_concepto,lc.orden,lc.concepto_id, lc.logica, lc.modulo_id, ce.sin_valor, lc.id
            FROM "gestionNomina_t_logica_calculo" lc, 
                 "gestionConceptos_t_concepto_empresa" ce,
                 public."gestionConceptos_t_conceptos" c
            WHERE lc.concepto_id = ce.id
              AND ce.cod_concepto_id = c.id
              AND ce.empresa_id = p_empresa_id
              AND lc.tipo_nomina_id = p_tipo_nomina_id
              AND lc.periodo = p_periodo
              AND lc.logica IS NOT NULL
              order by lc.orden, c.cod_concepto
        LOOP
 
        INSERT INTO t_log_nomina (proceso_id, origen, mensaje)
        VALUES (p_proceso_id,'prc_procesar_nomina','Borrado prenomina: ' || v_contrato.id);


        INSERT INTO t_log_nomina (proceso_id, origen, mensaje)
        VALUES (p_proceso_id,'prc_procesar_nomina','Concepto: ' || v_concepto);

        IF fn_contrato_cumple_filtros(v_contrato.id,v_concepto.id) THEN
            
            v_sql := format(
                'CALL %s(%s,%s,%s,%s,%s,%s,%L,%L,%s,%s,%s,%s,%L)',
                lower(v_concepto.logica),
                p_empresa_id,
                v_contrato.id,
                p_tipo_nomina_id,
                p_anio,
                p_mes,
                p_periodo,
                p_fecha_inicio,
                p_fecha_fin,
                v_concepto.concepto_id,
                p_proceso_id,
                v_concepto.modulo_id,
                p_periodo_nomina,
                v_concepto.sin_valor
            );
            
            
            EXECUTE v_sql;
        
        END IF;

            INSERT INTO t_log_nomina (proceso_id, origen, mensaje)
            VALUES (p_proceso_id,'prc_procesar_nomina','excecute procedimiento: ' || v_sql);

        END LOOP;
    
    v_contratos_procesados := v_contratos_procesados + 1;
    v_progreso := CEIL((v_contratos_procesados::NUMERIC / v_total_contratos) * 100);

    UPDATE "gestionNomina_t_proceso_nomina"
    SET progreso = LEAST(v_progreso, 100)
    WHERE id = p_proceso_id;
    COMMIT;
    END LOOP;
    
    INSERT INTO t_log_nomina (proceso_id, origen, mensaje)
    VALUES (p_proceso_id,'prc_procesar_nomina','Fin');
    
    UPDATE "gestionNomina_t_proceso_nomina"
    SET progreso = 100
    WHERE id = p_proceso_id;

END;
$$;


ALTER PROCEDURE public.prc_procesar_nomina(IN p_empresa_id integer, IN p_tipo_nomina_id integer, IN p_anio integer, IN p_mes integer, IN p_periodo integer, IN p_fecha_inicio date, IN p_fecha_fin date, IN p_proceso_id integer, IN p_periodo_nomina integer) OWNER TO postgres;

--
-- Name: banco(bigint); Type: FUNCTION; Schema: reportes; Owner: postgres
--

CREATE FUNCTION reportes.banco(p_id bigint) RETURNS text
    LANGUAGE sql STABLE
    AS $$
select banco 
from public.parametros_t_banco WHERE id = p_id;
$$;


ALTER FUNCTION reportes.banco(p_id bigint) OWNER TO postgres;

--
-- Name: cotizante(bigint); Type: FUNCTION; Schema: reportes; Owner: postgres
--

CREATE FUNCTION reportes.cotizante(p_id bigint) RETURNS text
    LANGUAGE sql STABLE
    AS $$
    SELECT descripcion FROM public.parametros_t_tipo_cotizante WHERE id = p_id;
$$;


ALTER FUNCTION reportes.cotizante(p_id bigint) OWNER TO postgres;

--
-- Name: nombre_empresa(bigint); Type: FUNCTION; Schema: reportes; Owner: postgres
--

CREATE FUNCTION reportes.nombre_empresa(p_id bigint) RETURNS text
    LANGUAGE sql STABLE
    AS $$
    SELECT razon_social FROM public."gestionClientes_t_empresa" WHERE id = p_id;
$$;


ALTER FUNCTION reportes.nombre_empresa(p_id bigint) OWNER TO postgres;

--
-- Name: nombre_identificacion(bigint); Type: FUNCTION; Schema: reportes; Owner: postgres
--

CREATE FUNCTION reportes.nombre_identificacion(p_id bigint) RETURNS text
    LANGUAGE sql STABLE
    AS $$
select concat(nombre,' ',segundo_nombre,' ',apellido,' ',segundo_apellido) as nombre
from public."gestionIdentificacion_t_identificacion" WHERE id = p_id;
$$;


ALTER FUNCTION reportes.nombre_identificacion(p_id bigint) OWNER TO postgres;

--
-- Name: numero_identificacion(bigint); Type: FUNCTION; Schema: reportes; Owner: postgres
--

CREATE FUNCTION reportes.numero_identificacion(p_id bigint) RETURNS text
    LANGUAGE sql STABLE
    AS $$
select identificacion
from public."gestionIdentificacion_t_identificacion" WHERE id = p_id;
$$;


ALTER FUNCTION reportes.numero_identificacion(p_id bigint) OWNER TO postgres;

--
-- Name: subcotizante(bigint); Type: FUNCTION; Schema: reportes; Owner: postgres
--

CREATE FUNCTION reportes.subcotizante(p_id bigint) RETURNS text
    LANGUAGE sql STABLE
    AS $$
    SELECT descripcion FROM public.parametros_t_subtipo_cotizante WHERE id = p_id;
$$;


ALTER FUNCTION reportes.subcotizante(p_id bigint) OWNER TO postgres;

--
-- Name: tipo_contrato(bigint); Type: FUNCTION; Schema: reportes; Owner: postgres
--

CREATE FUNCTION reportes.tipo_contrato(p_id bigint) RETURNS text
    LANGUAGE sql STABLE
    AS $$
select contrato
from public.parametros_t_tipo_contrato WHERE id = p_id;
$$;


ALTER FUNCTION reportes.tipo_contrato(p_id bigint) OWNER TO postgres;

--
-- Name: tipo_salario(bigint); Type: FUNCTION; Schema: reportes; Owner: postgres
--

CREATE FUNCTION reportes.tipo_salario(p_id bigint) RETURNS text
    LANGUAGE sql STABLE
    AS $$
select salario
from public.parametros_t_tipo_salario WHERE id = p_id;
$$;


ALTER FUNCTION reportes.tipo_salario(p_id bigint) OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: accounts_usuarioerp; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.accounts_usuarioerp (
    id bigint NOT NULL,
    identificacion character varying(20) NOT NULL,
    nombre_completo character varying(150) NOT NULL,
    cargo character varying(100),
    activo boolean NOT NULL,
    fecha_creacion timestamp with time zone NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.accounts_usuarioerp OWNER TO postgres;

--
-- Name: accounts_usuarioerp_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.accounts_usuarioerp ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.accounts_usuarioerp_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: api_t_area; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.api_t_area (
    id bigint NOT NULL,
    codigo character varying(10) NOT NULL,
    nombre character varying(100) NOT NULL,
    estado boolean NOT NULL
);


ALTER TABLE public.api_t_area OWNER TO postgres;

--
-- Name: api_t_area_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.api_t_area ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.api_t_area_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: api_t_cargo; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.api_t_cargo (
    id bigint NOT NULL,
    codigo character varying(5) NOT NULL,
    nombre character varying(50) NOT NULL,
    estado boolean NOT NULL
);


ALTER TABLE public.api_t_cargo OWNER TO postgres;

--
-- Name: api_t_cargo_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.api_t_cargo ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.api_t_cargo_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: api_t_lista; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.api_t_lista (
    id bigint NOT NULL,
    codigo character varying(6) NOT NULL,
    nombre character varying(100) NOT NULL,
    descripcion character varying(100) NOT NULL
);


ALTER TABLE public.api_t_lista OWNER TO postgres;

--
-- Name: api_t_lista_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.api_t_lista ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.api_t_lista_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO postgres;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.auth_group ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group_permissions (
    id bigint NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO postgres;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.auth_group_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO postgres;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.auth_permission ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(150) NOT NULL,
    last_name character varying(150) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE public.auth_user OWNER TO postgres;

--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_user_groups (
    id bigint NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.auth_user_groups OWNER TO postgres;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.auth_user_groups ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.auth_user ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_user_user_permissions (
    id bigint NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_user_user_permissions OWNER TO postgres;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.auth_user_user_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: authtoken_token; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.authtoken_token (
    key character varying(40) NOT NULL,
    created timestamp with time zone NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.authtoken_token OWNER TO postgres;

--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO postgres;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.django_admin_log ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO postgres;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.django_content_type ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_migrations (
    id bigint NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO postgres;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.django_migrations ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO postgres;

--
-- Name: gestionClientes_t_cliente; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."gestionClientes_t_cliente" (
    id bigint NOT NULL,
    nombre_cliente character varying(100) NOT NULL,
    estado_cliente boolean NOT NULL,
    celular character varying(24)
);


ALTER TABLE public."gestionClientes_t_cliente" OWNER TO postgres;

--
-- Name: gestionClientes_t_cliente_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public."gestionClientes_t_cliente" ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public."gestionClientes_t_cliente_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: gestionClientes_t_empresa; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."gestionClientes_t_empresa" (
    id bigint NOT NULL,
    codigo_empresa character varying(6) NOT NULL,
    nit_empresa character varying(20) NOT NULL,
    razon_social character varying(200) NOT NULL,
    direccion character varying(200) NOT NULL,
    telefono character varying(24) NOT NULL,
    codigo_cliente_id bigint NOT NULL,
    digito_verificacion character varying(1)
);


ALTER TABLE public."gestionClientes_t_empresa" OWNER TO postgres;

--
-- Name: gestionClientes_t_empresa_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public."gestionClientes_t_empresa" ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public."gestionClientes_t_empresa_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: gestionClientes_usuarioempresa; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."gestionClientes_usuarioempresa" (
    id bigint NOT NULL,
    activo boolean NOT NULL,
    fecha_asignacion timestamp with time zone NOT NULL,
    empresa_id bigint NOT NULL,
    usuario_id integer NOT NULL
);


ALTER TABLE public."gestionClientes_usuarioempresa" OWNER TO postgres;

--
-- Name: gestionClientes_usuarioempresa_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public."gestionClientes_usuarioempresa" ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public."gestionClientes_usuarioempresa_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: gestionConceptos_t_concepto_empresa; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."gestionConceptos_t_concepto_empresa" (
    id bigint NOT NULL,
    desc_concepto_emp character varying(100) NOT NULL,
    tipo_redondeo character varying(2) NOT NULL,
    sin_valor character varying(2) NOT NULL,
    user_creator character varying(50),
    date_created date,
    cod_concepto_id bigint NOT NULL,
    empresa_id bigint NOT NULL,
    concepto_cliente character varying(10),
    concepto_espejo_id bigint
);


ALTER TABLE public."gestionConceptos_t_concepto_empresa" OWNER TO postgres;

--
-- Name: gestionConceptos_t_concepto_empresa_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public."gestionConceptos_t_concepto_empresa" ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public."gestionConceptos_t_concepto_empresa_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: gestionConceptos_t_conceptos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."gestionConceptos_t_conceptos" (
    id bigint NOT NULL,
    cod_concepto character varying(5) NOT NULL,
    desc_concepto character varying(100) NOT NULL,
    desc_concepto_eng character varying(100) NOT NULL,
    tipo_concepto character varying(3) NOT NULL,
    user_creator character varying(50),
    date_created date
);


ALTER TABLE public."gestionConceptos_t_conceptos" OWNER TO postgres;

--
-- Name: gestionConceptos_t_conceptos_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public."gestionConceptos_t_conceptos" ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public."gestionConceptos_t_conceptos_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: gestionConceptos_t_grupo_concepto; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."gestionConceptos_t_grupo_concepto" (
    id bigint NOT NULL,
    codigo character varying(6) NOT NULL,
    titulo character varying(100) NOT NULL,
    descripcion text NOT NULL,
    user_creator character varying(50),
    date_created date
);


ALTER TABLE public."gestionConceptos_t_grupo_concepto" OWNER TO postgres;

--
-- Name: gestionConceptos_t_grupo_concepto_det; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."gestionConceptos_t_grupo_concepto_det" (
    id bigint NOT NULL,
    user_creator character varying(50),
    date_created date,
    concepto_id bigint NOT NULL,
    grupo_id bigint NOT NULL,
    operacion character varying(1) NOT NULL
);


ALTER TABLE public."gestionConceptos_t_grupo_concepto_det" OWNER TO postgres;

--
-- Name: gestionConceptos_t_grupo_concepto_det_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public."gestionConceptos_t_grupo_concepto_det" ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public."gestionConceptos_t_grupo_concepto_det_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: gestionConceptos_t_grupo_concepto_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public."gestionConceptos_t_grupo_concepto" ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public."gestionConceptos_t_grupo_concepto_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: gestionContratos_t_contrato; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."gestionContratos_t_contrato" (
    id bigint NOT NULL,
    cod_contrato bigint NOT NULL,
    fecha_ingreso date NOT NULL,
    fecha_fin date,
    periodo_vac integer NOT NULL,
    codigo_interno character varying(16),
    procedimiento character varying(1) NOT NULL,
    porcentaje_retencion numeric(5,2),
    estado character varying(1) NOT NULL,
    cesantias character varying(3) NOT NULL,
    user_creator character varying(50),
    date_created date,
    empresa_id bigint NOT NULL,
    identificacion_id bigint NOT NULL,
    subtipo_cotizante_id bigint NOT NULL,
    tipo_contrato_id bigint NOT NULL,
    tipo_cotizante_id bigint NOT NULL,
    tipo_nomina_id bigint NOT NULL,
    motivo_retiro_id bigint,
    fecha_ret date
);


ALTER TABLE public."gestionContratos_t_contrato" OWNER TO postgres;

--
-- Name: gestionContratos_t_contrato_banco; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."gestionContratos_t_contrato_banco" (
    id bigint NOT NULL,
    cuenta character varying(20) NOT NULL,
    fecha_inicio date NOT NULL,
    fecha_fin date,
    estado boolean NOT NULL,
    user_creator character varying(50),
    date_created date,
    banco_id bigint NOT NULL,
    contrato_id bigint NOT NULL,
    numero_cuenta character varying(20)
);


ALTER TABLE public."gestionContratos_t_contrato_banco" OWNER TO postgres;

--
-- Name: gestionContratos_t_contrato_banco_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public."gestionContratos_t_contrato_banco" ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public."gestionContratos_t_contrato_banco_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: gestionContratos_t_contrato_deducibles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."gestionContratos_t_contrato_deducibles" (
    id bigint NOT NULL,
    tipo_deducible character varying NOT NULL,
    fecha_inicio date NOT NULL,
    fecha_fin date NOT NULL,
    user_creator character varying(50),
    date_created date,
    contrato_id bigint NOT NULL,
    valor numeric(12,0) NOT NULL
);


ALTER TABLE public."gestionContratos_t_contrato_deducibles" OWNER TO postgres;

--
-- Name: gestionContratos_t_contrato_deducibles_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public."gestionContratos_t_contrato_deducibles" ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public."gestionContratos_t_contrato_deducibles_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: gestionContratos_t_contrato_entidadesss; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."gestionContratos_t_contrato_entidadesss" (
    id bigint NOT NULL,
    tipo_entidad character varying(10) NOT NULL,
    fecha_inicio date NOT NULL,
    fecha_fin date,
    user_creator character varying(50),
    date_created date,
    contrato_id bigint NOT NULL,
    entidad_id bigint NOT NULL
);


ALTER TABLE public."gestionContratos_t_contrato_entidadesss" OWNER TO postgres;

--
-- Name: gestionContratos_t_contrato_entidadesss_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public."gestionContratos_t_contrato_entidadesss" ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public."gestionContratos_t_contrato_entidadesss_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: gestionContratos_t_contrato_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public."gestionContratos_t_contrato" ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public."gestionContratos_t_contrato_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: gestionContratos_t_contrato_salario; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."gestionContratos_t_contrato_salario" (
    id bigint NOT NULL,
    salario numeric(12,0) NOT NULL,
    fecha_inicio date NOT NULL,
    fecha_fin date,
    estado boolean NOT NULL,
    retroactivo boolean NOT NULL,
    user_creator character varying(50),
    date_created date,
    contrato_id bigint NOT NULL,
    tipo_salario_id bigint NOT NULL
);


ALTER TABLE public."gestionContratos_t_contrato_salario" OWNER TO postgres;

--
-- Name: gestionContratos_t_contrato_salario_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public."gestionContratos_t_contrato_salario" ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public."gestionContratos_t_contrato_salario_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: gestionIdentificacion_t_beneficiario; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."gestionIdentificacion_t_beneficiario" (
    id bigint NOT NULL,
    iden_beneficiario character varying(24) NOT NULL,
    nombre_completo character varying(200) NOT NULL,
    fecha_nacimiento date NOT NULL,
    parentesco integer,
    exogena boolean NOT NULL,
    iden_titular_id bigint NOT NULL,
    tipo_ide_ben_id bigint NOT NULL
);


ALTER TABLE public."gestionIdentificacion_t_beneficiario" OWNER TO postgres;

--
-- Name: gestionIdentificacion_t_beneficiario_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public."gestionIdentificacion_t_beneficiario" ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public."gestionIdentificacion_t_beneficiario_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: gestionIdentificacion_t_identificacion; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."gestionIdentificacion_t_identificacion" (
    id bigint NOT NULL,
    identificacion character varying(24) NOT NULL,
    nombre character varying(100) NOT NULL,
    segundo_nombre character varying(100),
    apellido character varying(100) NOT NULL,
    segundo_apellido character varying(100),
    fecha_nacimiento date NOT NULL,
    fecha_exp_doc date NOT NULL,
    telefono character varying(30),
    celular character varying(30) NOT NULL,
    direccion character varying(100) NOT NULL,
    estado_civil integer,
    genero integer,
    correo_personal character varying(254) NOT NULL,
    correo_coorporativo character varying(254),
    tipo_ide_id bigint NOT NULL
);


ALTER TABLE public."gestionIdentificacion_t_identificacion" OWNER TO postgres;

--
-- Name: gestionIdentificacion_t_identificacion_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public."gestionIdentificacion_t_identificacion" ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public."gestionIdentificacion_t_identificacion_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: gestionIdentificacion_t_tipo_ide; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."gestionIdentificacion_t_tipo_ide" (
    id bigint NOT NULL,
    cod_ide character varying(8) NOT NULL,
    desc_ide character varying(32) NOT NULL,
    estado_ide boolean NOT NULL,
    user_creator character varying(50),
    date_created date NOT NULL
);


ALTER TABLE public."gestionIdentificacion_t_tipo_ide" OWNER TO postgres;

--
-- Name: gestionIdentificacion_t_tipo_ide_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public."gestionIdentificacion_t_tipo_ide" ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public."gestionIdentificacion_t_tipo_ide_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: gestionNomina_t_acumulado_empleado; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."gestionNomina_t_acumulado_empleado" (
    id bigint NOT NULL,
    anio integer NOT NULL,
    mes integer NOT NULL,
    periodo integer NOT NULL,
    fecha_novedad date,
    fecha_inicio date,
    fecha_fin date,
    unidad numeric(10,0) NOT NULL,
    base numeric(15,0) NOT NULL,
    valor numeric(15,0) NOT NULL,
    t01 character varying(100),
    v01 numeric(15,2),
    t02 character varying(100),
    v02 numeric(15,2),
    t03 character varying(100),
    v03 numeric(15,2),
    t04 character varying(100),
    v04 numeric(15,2),
    t05 character varying(100),
    v05 numeric(15,2),
    t06 character varying(100),
    v06 numeric(15,2),
    t07 character varying(100),
    v07 numeric(15,2),
    t08 character varying(100),
    v08 numeric(15,2),
    t09 character varying(100),
    v09 numeric(15,2),
    t10 character varying(100),
    v10 numeric(15,2),
    t11 character varying(100),
    v11 numeric(15,2),
    t12 character varying(100),
    v12 numeric(15,2),
    t13 character varying(100),
    v13 numeric(15,2),
    t14 character varying(100),
    v14 numeric(15,2),
    t15 character varying(100),
    v15 numeric(15,2),
    t16 character varying(100),
    v16 numeric(15,2),
    t17 character varying(100),
    v17 numeric(15,2),
    t18 character varying(100),
    v18 numeric(15,2),
    t19 character varying(100),
    v19 numeric(15,2),
    t20 character varying(100),
    v20 numeric(15,2),
    ft01 character varying(100),
    f01 date,
    ft02 character varying(100),
    f02 date,
    ft03 character varying(100),
    f03 date,
    ft04 character varying(100),
    f04 date,
    concepto_id bigint NOT NULL,
    contrato_id bigint NOT NULL,
    modulo_id bigint,
    tipo_nomina_id bigint NOT NULL,
    periodo_nomina_id bigint NOT NULL
);


ALTER TABLE public."gestionNomina_t_acumulado_empleado" OWNER TO postgres;

--
-- Name: gestionNomina_t_acumulado_empleado_def; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."gestionNomina_t_acumulado_empleado_def" (
    id bigint NOT NULL,
    anio integer NOT NULL,
    mes integer NOT NULL,
    periodo integer NOT NULL,
    fecha_novedad date,
    fecha_inicio date,
    fecha_fin date,
    unidad numeric(10,0) NOT NULL,
    base numeric(15,0) NOT NULL,
    valor numeric(15,0) NOT NULL,
    t01 character varying(100),
    v01 numeric(15,2),
    t02 character varying(100),
    v02 numeric(15,2),
    t03 character varying(100),
    v03 numeric(15,2),
    t04 character varying(100),
    v04 numeric(15,2),
    t05 character varying(100),
    v05 numeric(15,2),
    t06 character varying(100),
    v06 numeric(15,2),
    t07 character varying(100),
    v07 numeric(15,2),
    t08 character varying(100),
    v08 numeric(15,2),
    t09 character varying(100),
    v09 numeric(15,2),
    t10 character varying(100),
    v10 numeric(15,2),
    t11 character varying(100),
    v11 numeric(15,2),
    t12 character varying(100),
    v12 numeric(15,2),
    t13 character varying(100),
    v13 numeric(15,2),
    t14 character varying(100),
    v14 numeric(15,2),
    t15 character varying(100),
    v15 numeric(15,2),
    t16 character varying(100),
    v16 numeric(15,2),
    t17 character varying(100),
    v17 numeric(15,2),
    t18 character varying(100),
    v18 numeric(15,2),
    t19 character varying(100),
    v19 numeric(15,2),
    t20 character varying(100),
    v20 numeric(15,2),
    ft01 character varying(100),
    f01 date,
    ft02 character varying(100),
    f02 date,
    ft03 character varying(100),
    f03 date,
    ft04 character varying(100),
    f04 date,
    concepto_id bigint NOT NULL,
    contrato_id bigint NOT NULL,
    modulo_id bigint,
    periodo_nomina_id bigint NOT NULL,
    tipo_nomina_id bigint NOT NULL
);


ALTER TABLE public."gestionNomina_t_acumulado_empleado_def" OWNER TO postgres;

--
-- Name: gestionNomina_t_acumulado_empleado_def_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public."gestionNomina_t_acumulado_empleado_def" ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public."gestionNomina_t_acumulado_empleado_def_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: gestionNomina_t_acumulado_empleado_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public."gestionNomina_t_acumulado_empleado" ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public."gestionNomina_t_acumulado_empleado_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: gestionNomina_t_logica_calculo; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."gestionNomina_t_logica_calculo" (
    id bigint NOT NULL,
    periodo integer NOT NULL,
    logica character varying(200),
    user_creator character varying(50),
    date_created date,
    concepto_id bigint NOT NULL,
    empresa_id bigint NOT NULL,
    modulo_id bigint,
    tipo_nomina_id bigint NOT NULL,
    orden integer NOT NULL
);


ALTER TABLE public."gestionNomina_t_logica_calculo" OWNER TO postgres;

--
-- Name: gestionNomina_t_logica_calculo_filtro; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."gestionNomina_t_logica_calculo_filtro" (
    id bigint NOT NULL,
    campo character varying(50) NOT NULL,
    operador character varying(20) NOT NULL,
    valor integer NOT NULL,
    user_creator character varying(50),
    date_created date,
    logica_calculo_id bigint NOT NULL
);


ALTER TABLE public."gestionNomina_t_logica_calculo_filtro" OWNER TO postgres;

--
-- Name: gestionNomina_t_logica_calculo_filtro_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public."gestionNomina_t_logica_calculo_filtro" ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public."gestionNomina_t_logica_calculo_filtro_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: gestionNomina_t_logica_calculo_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public."gestionNomina_t_logica_calculo" ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public."gestionNomina_t_logica_calculo_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: gestionNomina_t_periodo_nomina; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."gestionNomina_t_periodo_nomina" (
    id bigint NOT NULL,
    codigo integer,
    anio integer NOT NULL,
    mes integer NOT NULL,
    periodo integer NOT NULL,
    fecha_inicio date NOT NULL,
    fecha_fin date NOT NULL,
    empresa_id bigint NOT NULL,
    tipo_nomina_id bigint NOT NULL,
    date_created date,
    user_creator character varying(50),
    estado boolean NOT NULL
);


ALTER TABLE public."gestionNomina_t_periodo_nomina" OWNER TO postgres;

--
-- Name: gestionNomina_t_periodo_nomina_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public."gestionNomina_t_periodo_nomina" ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public."gestionNomina_t_periodo_nomina_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: gestionNomina_t_proceso_nomina; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."gestionNomina_t_proceso_nomina" (
    id bigint NOT NULL,
    estado character varying(1) NOT NULL,
    date_created timestamp with time zone NOT NULL,
    date_finished timestamp with time zone,
    mensaje_error text,
    user_creator character varying(50),
    periodo_nomina_id bigint NOT NULL,
    progreso smallint NOT NULL,
    CONSTRAINT "gestionNomina_t_proceso_nomina_progreso_check" CHECK ((progreso >= 0))
);


ALTER TABLE public."gestionNomina_t_proceso_nomina" OWNER TO postgres;

--
-- Name: gestionNomina_t_proceso_nomina_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public."gestionNomina_t_proceso_nomina" ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public."gestionNomina_t_proceso_nomina_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: gestionNovedades_t_novedad_temporal; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."gestionNovedades_t_novedad_temporal" (
    id bigint NOT NULL,
    anio integer NOT NULL,
    mes integer NOT NULL,
    periodo integer NOT NULL,
    unidad numeric(10,0) NOT NULL,
    base numeric(15,0) NOT NULL,
    valor numeric(15,0) NOT NULL,
    fecha_novedad date,
    fecha_inicio date,
    fecha_fin date,
    estado boolean NOT NULL,
    user_creator character varying(50),
    date_created date,
    concepto_id bigint NOT NULL,
    contrato_id bigint NOT NULL,
    periodo_nomina_id bigint NOT NULL,
    tipo_nomina_id bigint NOT NULL
);


ALTER TABLE public."gestionNovedades_t_novedad_temporal" OWNER TO postgres;

--
-- Name: gestionNovedades_t_novedad_temporal_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public."gestionNovedades_t_novedad_temporal" ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public."gestionNovedades_t_novedad_temporal_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: gestionReportes_parametroreporte; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."gestionReportes_parametroreporte" (
    id bigint NOT NULL,
    nombre character varying(50) NOT NULL,
    etiqueta character varying(100) NOT NULL,
    tipo_dato character varying(10) NOT NULL,
    requerido boolean NOT NULL,
    orden integer NOT NULL,
    reporte_id bigint NOT NULL,
    CONSTRAINT "gestionReportes_parametroreporte_orden_check" CHECK ((orden >= 0))
);


ALTER TABLE public."gestionReportes_parametroreporte" OWNER TO postgres;

--
-- Name: gestionReportes_parametroreporte_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public."gestionReportes_parametroreporte" ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public."gestionReportes_parametroreporte_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: gestionReportes_reporte; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."gestionReportes_reporte" (
    id bigint NOT NULL,
    nombre character varying(150) NOT NULL,
    descripcion text NOT NULL,
    ruta_jasper character varying(255) NOT NULL,
    activo boolean NOT NULL,
    user_creator character varying(150),
    date_created timestamp with time zone
);


ALTER TABLE public."gestionReportes_reporte" OWNER TO postgres;

--
-- Name: gestionReportes_reporte_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public."gestionReportes_reporte" ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public."gestionReportes_reporte_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: parametros_parametrodetalle; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.parametros_parametrodetalle (
    id bigint NOT NULL,
    codigo character varying(6) NOT NULL,
    valor_texto character varying(255),
    valor_numerico numeric(15,3),
    fecha_inicio date,
    fecha_fin date,
    valor_booleano boolean NOT NULL,
    activo boolean NOT NULL,
    parametro_id bigint NOT NULL,
    date_created date,
    user_creator character varying(50)
);


ALTER TABLE public.parametros_parametrodetalle OWNER TO postgres;

--
-- Name: parametros_parametrodetalle_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.parametros_parametrodetalle ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.parametros_parametrodetalle_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: parametros_parametrogeneral; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.parametros_parametrogeneral (
    id bigint NOT NULL,
    codigo character varying(6) NOT NULL,
    titulo character varying(100) NOT NULL,
    descripcion text NOT NULL,
    activo boolean NOT NULL,
    date_created date,
    user_creator character varying(50)
);


ALTER TABLE public.parametros_parametrogeneral OWNER TO postgres;

--
-- Name: parametros_parametrogeneral_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.parametros_parametrogeneral ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.parametros_parametrogeneral_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: parametros_t_banco; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.parametros_t_banco (
    id bigint NOT NULL,
    banco character varying(200) NOT NULL,
    codigo_ach character varying(3),
    codigo_pse character varying(4),
    codigo_br character varying(2),
    codigo_fintech character varying(4),
    estado boolean NOT NULL,
    user_creator character varying(50),
    date_created date
);


ALTER TABLE public.parametros_t_banco OWNER TO postgres;

--
-- Name: parametros_t_banco_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.parametros_t_banco ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.parametros_t_banco_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: parametros_t_conceptos_salario; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.parametros_t_conceptos_salario (
    id bigint NOT NULL,
    user_creator character varying(50),
    date_created date,
    concepto_id bigint NOT NULL,
    tipo_salario_id bigint NOT NULL
);


ALTER TABLE public.parametros_t_conceptos_salario OWNER TO postgres;

--
-- Name: parametros_t_conceptos_salario_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.parametros_t_conceptos_salario ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.parametros_t_conceptos_salario_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: parametros_t_entidadesss; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.parametros_t_entidadesss (
    id bigint NOT NULL,
    tipo character varying(3) NOT NULL,
    codigo character varying(10) NOT NULL,
    nit character varying(16) NOT NULL,
    nombre character varying(100) NOT NULL,
    user_creator character varying(50),
    date_created date
);


ALTER TABLE public.parametros_t_entidadesss OWNER TO postgres;

--
-- Name: parametros_t_entidadesss_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.parametros_t_entidadesss ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.parametros_t_entidadesss_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: parametros_t_subtipo_cotizante; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.parametros_t_subtipo_cotizante (
    id bigint NOT NULL,
    codigo character varying(2) NOT NULL,
    descripcion character varying(100) NOT NULL,
    estado boolean NOT NULL,
    user_creator character varying(50),
    date_created date,
    codigo_cotizante_id bigint NOT NULL
);


ALTER TABLE public.parametros_t_subtipo_cotizante OWNER TO postgres;

--
-- Name: parametros_t_subtipo_cotizante_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.parametros_t_subtipo_cotizante ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.parametros_t_subtipo_cotizante_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: parametros_t_tipo_contrato; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.parametros_t_tipo_contrato (
    id bigint NOT NULL,
    contrato character varying(50) NOT NULL,
    estado boolean NOT NULL,
    user_creator character varying(50),
    date_created date
);


ALTER TABLE public.parametros_t_tipo_contrato OWNER TO postgres;

--
-- Name: parametros_t_tipo_contrato_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.parametros_t_tipo_contrato ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.parametros_t_tipo_contrato_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: parametros_t_tipo_cotizante; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.parametros_t_tipo_cotizante (
    id bigint NOT NULL,
    codigo character varying(2) NOT NULL,
    descripcion character varying(100) NOT NULL,
    estado boolean NOT NULL,
    user_creator character varying(50),
    date_created date
);


ALTER TABLE public.parametros_t_tipo_cotizante OWNER TO postgres;

--
-- Name: parametros_t_tipo_cotizante_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.parametros_t_tipo_cotizante ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.parametros_t_tipo_cotizante_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: parametros_t_tipo_nomina; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.parametros_t_tipo_nomina (
    id bigint NOT NULL,
    codigo character varying(2) NOT NULL,
    descripcion character varying(100) NOT NULL,
    estado boolean NOT NULL,
    user_creator character varying(50),
    date_created date,
    asigna_contrato boolean NOT NULL
);


ALTER TABLE public.parametros_t_tipo_nomina OWNER TO postgres;

--
-- Name: parametros_t_tipo_nomina_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.parametros_t_tipo_nomina ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.parametros_t_tipo_nomina_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: parametros_t_tipo_salario; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.parametros_t_tipo_salario (
    id bigint NOT NULL,
    salario character varying(50) NOT NULL,
    estado boolean NOT NULL,
    user_creator character varying(50),
    date_created date
);


ALTER TABLE public.parametros_t_tipo_salario OWNER TO postgres;

--
-- Name: parametros_t_tipo_salario_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.parametros_t_tipo_salario ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.parametros_t_tipo_salario_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: t_log_nomina; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.t_log_nomina (
    id integer NOT NULL,
    proceso_id integer,
    fecha timestamp without time zone DEFAULT now(),
    origen character varying(50),
    mensaje text
);


ALTER TABLE public.t_log_nomina OWNER TO postgres;

--
-- Name: t_log_nomina_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.t_log_nomina_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.t_log_nomina_id_seq OWNER TO postgres;

--
-- Name: t_log_nomina_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.t_log_nomina_id_seq OWNED BY public.t_log_nomina.id;


--
-- Name: v_porc_salud; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.v_porc_salud (
    valor_numerico numeric(15,3)
);


ALTER TABLE public.v_porc_salud OWNER TO postgres;

--
-- Name: v_salario; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.v_salario (
    salario numeric(12,0)
);


ALTER TABLE public.v_salario OWNER TO postgres;

--
-- Name: t_log_nomina id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.t_log_nomina ALTER COLUMN id SET DEFAULT nextval('public.t_log_nomina_id_seq'::regclass);


--
-- Name: accounts_usuarioerp accounts_usuarioerp_identificacion_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_usuarioerp
    ADD CONSTRAINT accounts_usuarioerp_identificacion_key UNIQUE (identificacion);


--
-- Name: accounts_usuarioerp accounts_usuarioerp_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_usuarioerp
    ADD CONSTRAINT accounts_usuarioerp_pkey PRIMARY KEY (id);


--
-- Name: accounts_usuarioerp accounts_usuarioerp_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_usuarioerp
    ADD CONSTRAINT accounts_usuarioerp_user_id_key UNIQUE (user_id);


--
-- Name: api_t_area api_t_area_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.api_t_area
    ADD CONSTRAINT api_t_area_pkey PRIMARY KEY (id);


--
-- Name: api_t_cargo api_t_cargo_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.api_t_cargo
    ADD CONSTRAINT api_t_cargo_pkey PRIMARY KEY (id);


--
-- Name: api_t_lista api_t_lista_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.api_t_lista
    ADD CONSTRAINT api_t_lista_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_user_id_group_id_94350c0c_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq UNIQUE (user_id, group_id);


--
-- Name: auth_user auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_permission_id_14a6b632_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq UNIQUE (user_id, permission_id);


--
-- Name: auth_user auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: authtoken_token authtoken_token_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.authtoken_token
    ADD CONSTRAINT authtoken_token_pkey PRIMARY KEY (key);


--
-- Name: authtoken_token authtoken_token_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.authtoken_token
    ADD CONSTRAINT authtoken_token_user_id_key UNIQUE (user_id);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: gestionClientes_t_cliente gestionClientes_t_cliente_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionClientes_t_cliente"
    ADD CONSTRAINT "gestionClientes_t_cliente_pkey" PRIMARY KEY (id);


--
-- Name: gestionClientes_t_empresa gestionClientes_t_empresa_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionClientes_t_empresa"
    ADD CONSTRAINT "gestionClientes_t_empresa_pkey" PRIMARY KEY (id);


--
-- Name: gestionClientes_usuarioempresa gestionClientes_usuarioe_usuario_id_empresa_id_402d169d_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionClientes_usuarioempresa"
    ADD CONSTRAINT "gestionClientes_usuarioe_usuario_id_empresa_id_402d169d_uniq" UNIQUE (usuario_id, empresa_id);


--
-- Name: gestionClientes_usuarioempresa gestionClientes_usuarioempresa_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionClientes_usuarioempresa"
    ADD CONSTRAINT "gestionClientes_usuarioempresa_pkey" PRIMARY KEY (id);


--
-- Name: gestionConceptos_t_concepto_empresa gestionConceptos_t_concepto_empresa_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionConceptos_t_concepto_empresa"
    ADD CONSTRAINT "gestionConceptos_t_concepto_empresa_pkey" PRIMARY KEY (id);


--
-- Name: gestionConceptos_t_conceptos gestionConceptos_t_conceptos_cod_concepto_ba4d2c4b_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionConceptos_t_conceptos"
    ADD CONSTRAINT "gestionConceptos_t_conceptos_cod_concepto_ba4d2c4b_uniq" UNIQUE (cod_concepto);


--
-- Name: gestionConceptos_t_conceptos gestionConceptos_t_conceptos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionConceptos_t_conceptos"
    ADD CONSTRAINT "gestionConceptos_t_conceptos_pkey" PRIMARY KEY (id);


--
-- Name: gestionConceptos_t_grupo_concepto gestionConceptos_t_grupo_concepto_codigo_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionConceptos_t_grupo_concepto"
    ADD CONSTRAINT "gestionConceptos_t_grupo_concepto_codigo_key" UNIQUE (codigo);


--
-- Name: gestionConceptos_t_grupo_concepto_det gestionConceptos_t_grupo_concepto_det_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionConceptos_t_grupo_concepto_det"
    ADD CONSTRAINT "gestionConceptos_t_grupo_concepto_det_pkey" PRIMARY KEY (id);


--
-- Name: gestionConceptos_t_grupo_concepto gestionConceptos_t_grupo_concepto_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionConceptos_t_grupo_concepto"
    ADD CONSTRAINT "gestionConceptos_t_grupo_concepto_pkey" PRIMARY KEY (id);


--
-- Name: gestionConceptos_t_grupo_concepto_det gestionConceptos_t_grupo_grupo_id_concepto_id_179aded6_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionConceptos_t_grupo_concepto_det"
    ADD CONSTRAINT "gestionConceptos_t_grupo_grupo_id_concepto_id_179aded6_uniq" UNIQUE (grupo_id, concepto_id);


--
-- Name: gestionContratos_t_contrato gestionContratos_t_contr_empresa_id_cod_contrato_3045757b_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionContratos_t_contrato"
    ADD CONSTRAINT "gestionContratos_t_contr_empresa_id_cod_contrato_3045757b_uniq" UNIQUE (empresa_id, cod_contrato);


--
-- Name: gestionContratos_t_contrato_banco gestionContratos_t_contrato_banco_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionContratos_t_contrato_banco"
    ADD CONSTRAINT "gestionContratos_t_contrato_banco_pkey" PRIMARY KEY (id);


--
-- Name: gestionContratos_t_contrato_deducibles gestionContratos_t_contrato_deducibles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionContratos_t_contrato_deducibles"
    ADD CONSTRAINT "gestionContratos_t_contrato_deducibles_pkey" PRIMARY KEY (id);


--
-- Name: gestionContratos_t_contrato_entidadesss gestionContratos_t_contrato_entidadesss_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionContratos_t_contrato_entidadesss"
    ADD CONSTRAINT "gestionContratos_t_contrato_entidadesss_pkey" PRIMARY KEY (id);


--
-- Name: gestionContratos_t_contrato gestionContratos_t_contrato_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionContratos_t_contrato"
    ADD CONSTRAINT "gestionContratos_t_contrato_pkey" PRIMARY KEY (id);


--
-- Name: gestionContratos_t_contrato_salario gestionContratos_t_contrato_salario_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionContratos_t_contrato_salario"
    ADD CONSTRAINT "gestionContratos_t_contrato_salario_pkey" PRIMARY KEY (id);


--
-- Name: gestionIdentificacion_t_beneficiario gestionIdentificacion_t_beneficiario_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionIdentificacion_t_beneficiario"
    ADD CONSTRAINT "gestionIdentificacion_t_beneficiario_pkey" PRIMARY KEY (id);


--
-- Name: gestionIdentificacion_t_identificacion gestionIdentificacion_t_identificacion_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionIdentificacion_t_identificacion"
    ADD CONSTRAINT "gestionIdentificacion_t_identificacion_pkey" PRIMARY KEY (id);


--
-- Name: gestionIdentificacion_t_tipo_ide gestionIdentificacion_t_tipo_ide_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionIdentificacion_t_tipo_ide"
    ADD CONSTRAINT "gestionIdentificacion_t_tipo_ide_pkey" PRIMARY KEY (id);


--
-- Name: gestionNomina_t_acumulado_empleado_def gestionNomina_t_acumulado_empleado_def_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionNomina_t_acumulado_empleado_def"
    ADD CONSTRAINT "gestionNomina_t_acumulado_empleado_def_pkey" PRIMARY KEY (id);


--
-- Name: gestionNomina_t_acumulado_empleado gestionNomina_t_acumulado_empleado_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionNomina_t_acumulado_empleado"
    ADD CONSTRAINT "gestionNomina_t_acumulado_empleado_pkey" PRIMARY KEY (id);


--
-- Name: gestionNomina_t_logica_calculo_filtro gestionNomina_t_logica_calculo_filtro_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionNomina_t_logica_calculo_filtro"
    ADD CONSTRAINT "gestionNomina_t_logica_calculo_filtro_pkey" PRIMARY KEY (id);


--
-- Name: gestionNomina_t_logica_calculo gestionNomina_t_logica_calculo_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionNomina_t_logica_calculo"
    ADD CONSTRAINT "gestionNomina_t_logica_calculo_pkey" PRIMARY KEY (id);


--
-- Name: gestionNomina_t_periodo_nomina gestionNomina_t_periodo__empresa_id_tipo_nomina_i_e1096ffe_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionNomina_t_periodo_nomina"
    ADD CONSTRAINT "gestionNomina_t_periodo__empresa_id_tipo_nomina_i_e1096ffe_uniq" UNIQUE (empresa_id, tipo_nomina_id, anio, mes, periodo);


--
-- Name: gestionNomina_t_periodo_nomina gestionNomina_t_periodo_nomina_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionNomina_t_periodo_nomina"
    ADD CONSTRAINT "gestionNomina_t_periodo_nomina_pkey" PRIMARY KEY (id);


--
-- Name: gestionNomina_t_proceso_nomina gestionNomina_t_proceso_nomina_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionNomina_t_proceso_nomina"
    ADD CONSTRAINT "gestionNomina_t_proceso_nomina_pkey" PRIMARY KEY (id);


--
-- Name: gestionNovedades_t_novedad_temporal gestionNovedades_t_novedad_temporal_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionNovedades_t_novedad_temporal"
    ADD CONSTRAINT "gestionNovedades_t_novedad_temporal_pkey" PRIMARY KEY (id);


--
-- Name: gestionReportes_parametroreporte gestionReportes_parametroreporte_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionReportes_parametroreporte"
    ADD CONSTRAINT "gestionReportes_parametroreporte_pkey" PRIMARY KEY (id);


--
-- Name: gestionReportes_reporte gestionReportes_reporte_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionReportes_reporte"
    ADD CONSTRAINT "gestionReportes_reporte_pkey" PRIMARY KEY (id);


--
-- Name: parametros_parametrodetalle parametros_parametrodetalle_parametro_id_codigo_ffcadb6b_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.parametros_parametrodetalle
    ADD CONSTRAINT parametros_parametrodetalle_parametro_id_codigo_ffcadb6b_uniq UNIQUE (parametro_id, codigo);


--
-- Name: parametros_parametrodetalle parametros_parametrodetalle_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.parametros_parametrodetalle
    ADD CONSTRAINT parametros_parametrodetalle_pkey PRIMARY KEY (id);


--
-- Name: parametros_parametrogeneral parametros_parametrogeneral_codigo_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.parametros_parametrogeneral
    ADD CONSTRAINT parametros_parametrogeneral_codigo_key UNIQUE (codigo);


--
-- Name: parametros_parametrogeneral parametros_parametrogeneral_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.parametros_parametrogeneral
    ADD CONSTRAINT parametros_parametrogeneral_pkey PRIMARY KEY (id);


--
-- Name: parametros_t_banco parametros_t_banco_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.parametros_t_banco
    ADD CONSTRAINT parametros_t_banco_pkey PRIMARY KEY (id);


--
-- Name: parametros_t_conceptos_salario parametros_t_conceptos_salario_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.parametros_t_conceptos_salario
    ADD CONSTRAINT parametros_t_conceptos_salario_pkey PRIMARY KEY (id);


--
-- Name: parametros_t_conceptos_salario parametros_t_conceptos_salario_tipo_salario_id_476ef608_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.parametros_t_conceptos_salario
    ADD CONSTRAINT parametros_t_conceptos_salario_tipo_salario_id_476ef608_uniq UNIQUE (tipo_salario_id);


--
-- Name: parametros_t_entidadesss parametros_t_entidadesss_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.parametros_t_entidadesss
    ADD CONSTRAINT parametros_t_entidadesss_pkey PRIMARY KEY (id);


--
-- Name: parametros_t_subtipo_cotizante parametros_t_subtipo_cotizante_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.parametros_t_subtipo_cotizante
    ADD CONSTRAINT parametros_t_subtipo_cotizante_pkey PRIMARY KEY (id);


--
-- Name: parametros_t_tipo_contrato parametros_t_tipo_contrato_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.parametros_t_tipo_contrato
    ADD CONSTRAINT parametros_t_tipo_contrato_pkey PRIMARY KEY (id);


--
-- Name: parametros_t_tipo_cotizante parametros_t_tipo_cotizante_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.parametros_t_tipo_cotizante
    ADD CONSTRAINT parametros_t_tipo_cotizante_pkey PRIMARY KEY (id);


--
-- Name: parametros_t_tipo_nomina parametros_t_tipo_nomina_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.parametros_t_tipo_nomina
    ADD CONSTRAINT parametros_t_tipo_nomina_pkey PRIMARY KEY (id);


--
-- Name: parametros_t_tipo_salario parametros_t_tipo_salario_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.parametros_t_tipo_salario
    ADD CONSTRAINT parametros_t_tipo_salario_pkey PRIMARY KEY (id);


--
-- Name: t_log_nomina t_log_nomina_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.t_log_nomina
    ADD CONSTRAINT t_log_nomina_pkey PRIMARY KEY (id);


--
-- Name: gestionConceptos_t_concepto_empresa unique_concepto_por_empresa; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionConceptos_t_concepto_empresa"
    ADD CONSTRAINT unique_concepto_por_empresa UNIQUE (empresa_id, cod_concepto_id);


--
-- Name: gestionIdentificacion_t_identificacion unique_tipo_numero; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionIdentificacion_t_identificacion"
    ADD CONSTRAINT unique_tipo_numero UNIQUE (tipo_ide_id, identificacion);


--
-- Name: gestionNomina_t_logica_calculo uq_logica_empresa_nomina_periodo_concepto; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionNomina_t_logica_calculo"
    ADD CONSTRAINT uq_logica_empresa_nomina_periodo_concepto UNIQUE (empresa_id, tipo_nomina_id, periodo, concepto_id);


--
-- Name: accounts_usuarioerp_identificacion_f84b50f3_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX accounts_usuarioerp_identificacion_f84b50f3_like ON public.accounts_usuarioerp USING btree (identificacion varchar_pattern_ops);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_group_id_97559544; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_groups_group_id_97559544 ON public.auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_user_id_6a12ed8b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_groups_user_id_6a12ed8b ON public.auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_permission_id_1fbb5f2c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_user_permissions_permission_id_1fbb5f2c ON public.auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_user_id_a95ead1b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_user_permissions_user_id_a95ead1b ON public.auth_user_user_permissions USING btree (user_id);


--
-- Name: auth_user_username_6821ab7c_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_username_6821ab7c_like ON public.auth_user USING btree (username varchar_pattern_ops);


--
-- Name: authtoken_token_key_10f0b77e_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX authtoken_token_key_10f0b77e_like ON public.authtoken_token USING btree (key varchar_pattern_ops);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: gestionClientes_t_empresa_codigo_cliente_id_27e55413; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "gestionClientes_t_empresa_codigo_cliente_id_27e55413" ON public."gestionClientes_t_empresa" USING btree (codigo_cliente_id);


--
-- Name: gestionClientes_usuarioempresa_empresa_id_9813ece2; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "gestionClientes_usuarioempresa_empresa_id_9813ece2" ON public."gestionClientes_usuarioempresa" USING btree (empresa_id);


--
-- Name: gestionClientes_usuarioempresa_usuario_id_08d644be; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "gestionClientes_usuarioempresa_usuario_id_08d644be" ON public."gestionClientes_usuarioempresa" USING btree (usuario_id);


--
-- Name: gestionConceptos_t_concepto_empresa_cod_concepto_id_fec3fc41; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "gestionConceptos_t_concepto_empresa_cod_concepto_id_fec3fc41" ON public."gestionConceptos_t_concepto_empresa" USING btree (cod_concepto_id);


--
-- Name: gestionConceptos_t_concepto_empresa_concepto_espejo_id_2349fc4a; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "gestionConceptos_t_concepto_empresa_concepto_espejo_id_2349fc4a" ON public."gestionConceptos_t_concepto_empresa" USING btree (concepto_espejo_id);


--
-- Name: gestionConceptos_t_concepto_empresa_empresa_id_911ae5a7; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "gestionConceptos_t_concepto_empresa_empresa_id_911ae5a7" ON public."gestionConceptos_t_concepto_empresa" USING btree (empresa_id);


--
-- Name: gestionConceptos_t_conceptos_cod_concepto_ba4d2c4b_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "gestionConceptos_t_conceptos_cod_concepto_ba4d2c4b_like" ON public."gestionConceptos_t_conceptos" USING btree (cod_concepto varchar_pattern_ops);


--
-- Name: gestionConceptos_t_grupo_concepto_codigo_35739b32_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "gestionConceptos_t_grupo_concepto_codigo_35739b32_like" ON public."gestionConceptos_t_grupo_concepto" USING btree (codigo varchar_pattern_ops);


--
-- Name: gestionConceptos_t_grupo_concepto_det_concepto_id_6e19b586; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "gestionConceptos_t_grupo_concepto_det_concepto_id_6e19b586" ON public."gestionConceptos_t_grupo_concepto_det" USING btree (concepto_id);


--
-- Name: gestionConceptos_t_grupo_concepto_det_grupo_id_e2b253f7; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "gestionConceptos_t_grupo_concepto_det_grupo_id_e2b253f7" ON public."gestionConceptos_t_grupo_concepto_det" USING btree (grupo_id);


--
-- Name: gestionContratos_t_contrato_banco_banco_id_936907b3; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "gestionContratos_t_contrato_banco_banco_id_936907b3" ON public."gestionContratos_t_contrato_banco" USING btree (banco_id);


--
-- Name: gestionContratos_t_contrato_banco_contrato_id_aafd93e1; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "gestionContratos_t_contrato_banco_contrato_id_aafd93e1" ON public."gestionContratos_t_contrato_banco" USING btree (contrato_id);


--
-- Name: gestionContratos_t_contrato_deducibles_contrato_id_446a6056; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "gestionContratos_t_contrato_deducibles_contrato_id_446a6056" ON public."gestionContratos_t_contrato_deducibles" USING btree (contrato_id);


--
-- Name: gestionContratos_t_contrato_empresa_id_4e92d0ec; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "gestionContratos_t_contrato_empresa_id_4e92d0ec" ON public."gestionContratos_t_contrato" USING btree (empresa_id);


--
-- Name: gestionContratos_t_contrato_entidadesss_contrato_id_655ee560; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "gestionContratos_t_contrato_entidadesss_contrato_id_655ee560" ON public."gestionContratos_t_contrato_entidadesss" USING btree (contrato_id);


--
-- Name: gestionContratos_t_contrato_entidadesss_entidad_id_ce21fb10; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "gestionContratos_t_contrato_entidadesss_entidad_id_ce21fb10" ON public."gestionContratos_t_contrato_entidadesss" USING btree (entidad_id);


--
-- Name: gestionContratos_t_contrato_identificacion_id_b17600d3; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "gestionContratos_t_contrato_identificacion_id_b17600d3" ON public."gestionContratos_t_contrato" USING btree (identificacion_id);


--
-- Name: gestionContratos_t_contrato_motivo_retiro_id_1259f26f; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "gestionContratos_t_contrato_motivo_retiro_id_1259f26f" ON public."gestionContratos_t_contrato" USING btree (motivo_retiro_id);


--
-- Name: gestionContratos_t_contrato_salario_contrato_id_0392e292; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "gestionContratos_t_contrato_salario_contrato_id_0392e292" ON public."gestionContratos_t_contrato_salario" USING btree (contrato_id);


--
-- Name: gestionContratos_t_contrato_salario_tipo_salario_id_a8b8718a; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "gestionContratos_t_contrato_salario_tipo_salario_id_a8b8718a" ON public."gestionContratos_t_contrato_salario" USING btree (tipo_salario_id);


--
-- Name: gestionContratos_t_contrato_subtipo_cotizante_id_ae3dc1a5; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "gestionContratos_t_contrato_subtipo_cotizante_id_ae3dc1a5" ON public."gestionContratos_t_contrato" USING btree (subtipo_cotizante_id);


--
-- Name: gestionContratos_t_contrato_tipo_contrato_id_27353c09; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "gestionContratos_t_contrato_tipo_contrato_id_27353c09" ON public."gestionContratos_t_contrato" USING btree (tipo_contrato_id);


--
-- Name: gestionContratos_t_contrato_tipo_cotizante_id_5e1ee974; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "gestionContratos_t_contrato_tipo_cotizante_id_5e1ee974" ON public."gestionContratos_t_contrato" USING btree (tipo_cotizante_id);


--
-- Name: gestionContratos_t_contrato_tipo_nomina_id_82c281c8; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "gestionContratos_t_contrato_tipo_nomina_id_82c281c8" ON public."gestionContratos_t_contrato" USING btree (tipo_nomina_id);


--
-- Name: gestionIdentificacion_t_beneficiario_iden_titular_id_c050b02b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "gestionIdentificacion_t_beneficiario_iden_titular_id_c050b02b" ON public."gestionIdentificacion_t_beneficiario" USING btree (iden_titular_id);


--
-- Name: gestionIdentificacion_t_beneficiario_tipo_ide_ben_id_d2c27e54; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "gestionIdentificacion_t_beneficiario_tipo_ide_ben_id_d2c27e54" ON public."gestionIdentificacion_t_beneficiario" USING btree (tipo_ide_ben_id);


--
-- Name: gestionIdentificacion_t_identificacion_tipo_ide_id_3caa56cf; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "gestionIdentificacion_t_identificacion_tipo_ide_id_3caa56cf" ON public."gestionIdentificacion_t_identificacion" USING btree (tipo_ide_id);


--
-- Name: gestionNomina_t_acumulado__periodo_nomina_id_f53b5e49; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "gestionNomina_t_acumulado__periodo_nomina_id_f53b5e49" ON public."gestionNomina_t_acumulado_empleado_def" USING btree (periodo_nomina_id);


--
-- Name: gestionNomina_t_acumulado_empleado_concepto_id_219f2ea2; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "gestionNomina_t_acumulado_empleado_concepto_id_219f2ea2" ON public."gestionNomina_t_acumulado_empleado" USING btree (concepto_id);


--
-- Name: gestionNomina_t_acumulado_empleado_contrato_id_fd8a38d9; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "gestionNomina_t_acumulado_empleado_contrato_id_fd8a38d9" ON public."gestionNomina_t_acumulado_empleado" USING btree (contrato_id);


--
-- Name: gestionNomina_t_acumulado_empleado_def_concepto_id_e32f7dcb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "gestionNomina_t_acumulado_empleado_def_concepto_id_e32f7dcb" ON public."gestionNomina_t_acumulado_empleado_def" USING btree (concepto_id);


--
-- Name: gestionNomina_t_acumulado_empleado_def_contrato_id_5be2a7fe; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "gestionNomina_t_acumulado_empleado_def_contrato_id_5be2a7fe" ON public."gestionNomina_t_acumulado_empleado_def" USING btree (contrato_id);


--
-- Name: gestionNomina_t_acumulado_empleado_def_modulo_id_92ff28f3; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "gestionNomina_t_acumulado_empleado_def_modulo_id_92ff28f3" ON public."gestionNomina_t_acumulado_empleado_def" USING btree (modulo_id);


--
-- Name: gestionNomina_t_acumulado_empleado_def_tipo_nomina_id_595cc7c6; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "gestionNomina_t_acumulado_empleado_def_tipo_nomina_id_595cc7c6" ON public."gestionNomina_t_acumulado_empleado_def" USING btree (tipo_nomina_id);


--
-- Name: gestionNomina_t_acumulado_empleado_modulo_id_5e455b98; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "gestionNomina_t_acumulado_empleado_modulo_id_5e455b98" ON public."gestionNomina_t_acumulado_empleado" USING btree (modulo_id);


--
-- Name: gestionNomina_t_acumulado_empleado_periodo_nomina_id_8f05ea2c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "gestionNomina_t_acumulado_empleado_periodo_nomina_id_8f05ea2c" ON public."gestionNomina_t_acumulado_empleado" USING btree (periodo_nomina_id);


--
-- Name: gestionNomina_t_acumulado_empleado_tipo_nomina_id_26929396; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "gestionNomina_t_acumulado_empleado_tipo_nomina_id_26929396" ON public."gestionNomina_t_acumulado_empleado" USING btree (tipo_nomina_id);


--
-- Name: gestionNomina_t_logica_cal_logica_calculo_id_207a2d24; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "gestionNomina_t_logica_cal_logica_calculo_id_207a2d24" ON public."gestionNomina_t_logica_calculo_filtro" USING btree (logica_calculo_id);


--
-- Name: gestionNomina_t_logica_calculo_concepto_id_ff1bbf85; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "gestionNomina_t_logica_calculo_concepto_id_ff1bbf85" ON public."gestionNomina_t_logica_calculo" USING btree (concepto_id);


--
-- Name: gestionNomina_t_logica_calculo_empresa_id_4c9c0ad6; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "gestionNomina_t_logica_calculo_empresa_id_4c9c0ad6" ON public."gestionNomina_t_logica_calculo" USING btree (empresa_id);


--
-- Name: gestionNomina_t_logica_calculo_modulo_id_70cef7f6; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "gestionNomina_t_logica_calculo_modulo_id_70cef7f6" ON public."gestionNomina_t_logica_calculo" USING btree (modulo_id);


--
-- Name: gestionNomina_t_logica_calculo_tipo_nomina_id_77c268a7; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "gestionNomina_t_logica_calculo_tipo_nomina_id_77c268a7" ON public."gestionNomina_t_logica_calculo" USING btree (tipo_nomina_id);


--
-- Name: gestionNomina_t_periodo_nomina_empresa_id_e02737bf; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "gestionNomina_t_periodo_nomina_empresa_id_e02737bf" ON public."gestionNomina_t_periodo_nomina" USING btree (empresa_id);


--
-- Name: gestionNomina_t_periodo_nomina_tipo_nomina_id_97f113a0; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "gestionNomina_t_periodo_nomina_tipo_nomina_id_97f113a0" ON public."gestionNomina_t_periodo_nomina" USING btree (tipo_nomina_id);


--
-- Name: gestionNomina_t_proceso_nomina_periodo_nomina_id_87906a13; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "gestionNomina_t_proceso_nomina_periodo_nomina_id_87906a13" ON public."gestionNomina_t_proceso_nomina" USING btree (periodo_nomina_id);


--
-- Name: gestionNovedades_t_novedad_temporal_concepto_id_d9e5b4fd; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "gestionNovedades_t_novedad_temporal_concepto_id_d9e5b4fd" ON public."gestionNovedades_t_novedad_temporal" USING btree (concepto_id);


--
-- Name: gestionNovedades_t_novedad_temporal_contrato_id_24da56b1; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "gestionNovedades_t_novedad_temporal_contrato_id_24da56b1" ON public."gestionNovedades_t_novedad_temporal" USING btree (contrato_id);


--
-- Name: gestionNovedades_t_novedad_temporal_periodo_nomina_id_ce4fd767; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "gestionNovedades_t_novedad_temporal_periodo_nomina_id_ce4fd767" ON public."gestionNovedades_t_novedad_temporal" USING btree (periodo_nomina_id);


--
-- Name: gestionNovedades_t_novedad_temporal_tipo_nomina_id_d9639603; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "gestionNovedades_t_novedad_temporal_tipo_nomina_id_d9639603" ON public."gestionNovedades_t_novedad_temporal" USING btree (tipo_nomina_id);


--
-- Name: gestionReportes_parametroreporte_reporte_id_a7568a3f; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "gestionReportes_parametroreporte_reporte_id_a7568a3f" ON public."gestionReportes_parametroreporte" USING btree (reporte_id);


--
-- Name: parametros_parametrodetalle_parametro_id_496f09aa; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX parametros_parametrodetalle_parametro_id_496f09aa ON public.parametros_parametrodetalle USING btree (parametro_id);


--
-- Name: parametros_parametrogeneral_codigo_4c5ed547_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX parametros_parametrogeneral_codigo_4c5ed547_like ON public.parametros_parametrogeneral USING btree (codigo varchar_pattern_ops);


--
-- Name: parametros_t_conceptos_salario_concepto_id_689ec1c0; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX parametros_t_conceptos_salario_concepto_id_689ec1c0 ON public.parametros_t_conceptos_salario USING btree (concepto_id);


--
-- Name: parametros_t_subtipo_cotizante_codigo_cotizante_id_b779553b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX parametros_t_subtipo_cotizante_codigo_cotizante_id_b779553b ON public.parametros_t_subtipo_cotizante USING btree (codigo_cotizante_id);


--
-- Name: accounts_usuarioerp accounts_usuarioerp_user_id_1792e82c_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_usuarioerp
    ADD CONSTRAINT accounts_usuarioerp_user_id_1792e82c_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_group_id_97559544_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_user_id_6a12ed8b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: authtoken_token authtoken_token_user_id_35299eff_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.authtoken_token
    ADD CONSTRAINT authtoken_token_user_id_35299eff_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: gestionClientes_t_empresa gestionClientes_t_em_codigo_cliente_id_27e55413_fk_gestionCl; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionClientes_t_empresa"
    ADD CONSTRAINT "gestionClientes_t_em_codigo_cliente_id_27e55413_fk_gestionCl" FOREIGN KEY (codigo_cliente_id) REFERENCES public."gestionClientes_t_cliente"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: gestionClientes_usuarioempresa gestionClientes_usua_empresa_id_9813ece2_fk_gestionCl; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionClientes_usuarioempresa"
    ADD CONSTRAINT "gestionClientes_usua_empresa_id_9813ece2_fk_gestionCl" FOREIGN KEY (empresa_id) REFERENCES public."gestionClientes_t_empresa"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: gestionClientes_usuarioempresa gestionClientes_usua_usuario_id_08d644be_fk_auth_user; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionClientes_usuarioempresa"
    ADD CONSTRAINT "gestionClientes_usua_usuario_id_08d644be_fk_auth_user" FOREIGN KEY (usuario_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: gestionConceptos_t_concepto_empresa gestionConceptos_t_c_cod_concepto_id_fec3fc41_fk_gestionCo; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionConceptos_t_concepto_empresa"
    ADD CONSTRAINT "gestionConceptos_t_c_cod_concepto_id_fec3fc41_fk_gestionCo" FOREIGN KEY (cod_concepto_id) REFERENCES public."gestionConceptos_t_conceptos"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: gestionConceptos_t_concepto_empresa gestionConceptos_t_c_concepto_espejo_id_2349fc4a_fk_gestionCo; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionConceptos_t_concepto_empresa"
    ADD CONSTRAINT "gestionConceptos_t_c_concepto_espejo_id_2349fc4a_fk_gestionCo" FOREIGN KEY (concepto_espejo_id) REFERENCES public."gestionConceptos_t_conceptos"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: gestionConceptos_t_concepto_empresa gestionConceptos_t_c_empresa_id_911ae5a7_fk_gestionCl; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionConceptos_t_concepto_empresa"
    ADD CONSTRAINT "gestionConceptos_t_c_empresa_id_911ae5a7_fk_gestionCl" FOREIGN KEY (empresa_id) REFERENCES public."gestionClientes_t_empresa"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: gestionConceptos_t_grupo_concepto_det gestionConceptos_t_g_concepto_id_6e19b586_fk_gestionCo; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionConceptos_t_grupo_concepto_det"
    ADD CONSTRAINT "gestionConceptos_t_g_concepto_id_6e19b586_fk_gestionCo" FOREIGN KEY (concepto_id) REFERENCES public."gestionConceptos_t_concepto_empresa"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: gestionConceptos_t_grupo_concepto_det gestionConceptos_t_g_grupo_id_e2b253f7_fk_gestionCo; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionConceptos_t_grupo_concepto_det"
    ADD CONSTRAINT "gestionConceptos_t_g_grupo_id_e2b253f7_fk_gestionCo" FOREIGN KEY (grupo_id) REFERENCES public."gestionConceptos_t_grupo_concepto"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: gestionContratos_t_contrato_banco gestionContratos_t_c_banco_id_936907b3_fk_parametro; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionContratos_t_contrato_banco"
    ADD CONSTRAINT "gestionContratos_t_c_banco_id_936907b3_fk_parametro" FOREIGN KEY (banco_id) REFERENCES public.parametros_t_banco(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: gestionContratos_t_contrato_salario gestionContratos_t_c_contrato_id_0392e292_fk_gestionCo; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionContratos_t_contrato_salario"
    ADD CONSTRAINT "gestionContratos_t_c_contrato_id_0392e292_fk_gestionCo" FOREIGN KEY (contrato_id) REFERENCES public."gestionContratos_t_contrato"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: gestionContratos_t_contrato_deducibles gestionContratos_t_c_contrato_id_446a6056_fk_gestionCo; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionContratos_t_contrato_deducibles"
    ADD CONSTRAINT "gestionContratos_t_c_contrato_id_446a6056_fk_gestionCo" FOREIGN KEY (contrato_id) REFERENCES public."gestionContratos_t_contrato"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: gestionContratos_t_contrato_entidadesss gestionContratos_t_c_contrato_id_655ee560_fk_gestionCo; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionContratos_t_contrato_entidadesss"
    ADD CONSTRAINT "gestionContratos_t_c_contrato_id_655ee560_fk_gestionCo" FOREIGN KEY (contrato_id) REFERENCES public."gestionContratos_t_contrato"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: gestionContratos_t_contrato_banco gestionContratos_t_c_contrato_id_aafd93e1_fk_gestionCo; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionContratos_t_contrato_banco"
    ADD CONSTRAINT "gestionContratos_t_c_contrato_id_aafd93e1_fk_gestionCo" FOREIGN KEY (contrato_id) REFERENCES public."gestionContratos_t_contrato"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: gestionContratos_t_contrato gestionContratos_t_c_empresa_id_4e92d0ec_fk_gestionCl; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionContratos_t_contrato"
    ADD CONSTRAINT "gestionContratos_t_c_empresa_id_4e92d0ec_fk_gestionCl" FOREIGN KEY (empresa_id) REFERENCES public."gestionClientes_t_empresa"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: gestionContratos_t_contrato_entidadesss gestionContratos_t_c_entidad_id_ce21fb10_fk_parametro; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionContratos_t_contrato_entidadesss"
    ADD CONSTRAINT "gestionContratos_t_c_entidad_id_ce21fb10_fk_parametro" FOREIGN KEY (entidad_id) REFERENCES public.parametros_t_entidadesss(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: gestionContratos_t_contrato gestionContratos_t_c_identificacion_id_b17600d3_fk_gestionId; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionContratos_t_contrato"
    ADD CONSTRAINT "gestionContratos_t_c_identificacion_id_b17600d3_fk_gestionId" FOREIGN KEY (identificacion_id) REFERENCES public."gestionIdentificacion_t_identificacion"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: gestionContratos_t_contrato gestionContratos_t_c_motivo_retiro_id_1259f26f_fk_parametro; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionContratos_t_contrato"
    ADD CONSTRAINT "gestionContratos_t_c_motivo_retiro_id_1259f26f_fk_parametro" FOREIGN KEY (motivo_retiro_id) REFERENCES public.parametros_parametrodetalle(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: gestionContratos_t_contrato gestionContratos_t_c_subtipo_cotizante_id_ae3dc1a5_fk_parametro; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionContratos_t_contrato"
    ADD CONSTRAINT "gestionContratos_t_c_subtipo_cotizante_id_ae3dc1a5_fk_parametro" FOREIGN KEY (subtipo_cotizante_id) REFERENCES public.parametros_t_subtipo_cotizante(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: gestionContratos_t_contrato gestionContratos_t_c_tipo_contrato_id_27353c09_fk_parametro; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionContratos_t_contrato"
    ADD CONSTRAINT "gestionContratos_t_c_tipo_contrato_id_27353c09_fk_parametro" FOREIGN KEY (tipo_contrato_id) REFERENCES public.parametros_t_tipo_contrato(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: gestionContratos_t_contrato gestionContratos_t_c_tipo_cotizante_id_5e1ee974_fk_parametro; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionContratos_t_contrato"
    ADD CONSTRAINT "gestionContratos_t_c_tipo_cotizante_id_5e1ee974_fk_parametro" FOREIGN KEY (tipo_cotizante_id) REFERENCES public.parametros_t_tipo_cotizante(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: gestionContratos_t_contrato gestionContratos_t_c_tipo_nomina_id_82c281c8_fk_parametro; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionContratos_t_contrato"
    ADD CONSTRAINT "gestionContratos_t_c_tipo_nomina_id_82c281c8_fk_parametro" FOREIGN KEY (tipo_nomina_id) REFERENCES public.parametros_t_tipo_nomina(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: gestionContratos_t_contrato_salario gestionContratos_t_c_tipo_salario_id_a8b8718a_fk_parametro; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionContratos_t_contrato_salario"
    ADD CONSTRAINT "gestionContratos_t_c_tipo_salario_id_a8b8718a_fk_parametro" FOREIGN KEY (tipo_salario_id) REFERENCES public.parametros_t_tipo_salario(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: gestionIdentificacion_t_beneficiario gestionIdentificacio_iden_titular_id_c050b02b_fk_gestionId; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionIdentificacion_t_beneficiario"
    ADD CONSTRAINT "gestionIdentificacio_iden_titular_id_c050b02b_fk_gestionId" FOREIGN KEY (iden_titular_id) REFERENCES public."gestionIdentificacion_t_identificacion"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: gestionIdentificacion_t_beneficiario gestionIdentificacio_tipo_ide_ben_id_d2c27e54_fk_gestionId; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionIdentificacion_t_beneficiario"
    ADD CONSTRAINT "gestionIdentificacio_tipo_ide_ben_id_d2c27e54_fk_gestionId" FOREIGN KEY (tipo_ide_ben_id) REFERENCES public."gestionIdentificacion_t_tipo_ide"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: gestionIdentificacion_t_identificacion gestionIdentificacio_tipo_ide_id_3caa56cf_fk_gestionId; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionIdentificacion_t_identificacion"
    ADD CONSTRAINT "gestionIdentificacio_tipo_ide_id_3caa56cf_fk_gestionId" FOREIGN KEY (tipo_ide_id) REFERENCES public."gestionIdentificacion_t_tipo_ide"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: gestionNomina_t_acumulado_empleado gestionNomina_t_acum_concepto_id_219f2ea2_fk_gestionCo; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionNomina_t_acumulado_empleado"
    ADD CONSTRAINT "gestionNomina_t_acum_concepto_id_219f2ea2_fk_gestionCo" FOREIGN KEY (concepto_id) REFERENCES public."gestionConceptos_t_concepto_empresa"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: gestionNomina_t_acumulado_empleado_def gestionNomina_t_acum_concepto_id_e32f7dcb_fk_gestionCo; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionNomina_t_acumulado_empleado_def"
    ADD CONSTRAINT "gestionNomina_t_acum_concepto_id_e32f7dcb_fk_gestionCo" FOREIGN KEY (concepto_id) REFERENCES public."gestionConceptos_t_concepto_empresa"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: gestionNomina_t_acumulado_empleado_def gestionNomina_t_acum_contrato_id_5be2a7fe_fk_gestionCo; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionNomina_t_acumulado_empleado_def"
    ADD CONSTRAINT "gestionNomina_t_acum_contrato_id_5be2a7fe_fk_gestionCo" FOREIGN KEY (contrato_id) REFERENCES public."gestionContratos_t_contrato"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: gestionNomina_t_acumulado_empleado gestionNomina_t_acum_contrato_id_fd8a38d9_fk_gestionCo; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionNomina_t_acumulado_empleado"
    ADD CONSTRAINT "gestionNomina_t_acum_contrato_id_fd8a38d9_fk_gestionCo" FOREIGN KEY (contrato_id) REFERENCES public."gestionContratos_t_contrato"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: gestionNomina_t_acumulado_empleado gestionNomina_t_acum_modulo_id_5e455b98_fk_parametro; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionNomina_t_acumulado_empleado"
    ADD CONSTRAINT "gestionNomina_t_acum_modulo_id_5e455b98_fk_parametro" FOREIGN KEY (modulo_id) REFERENCES public.parametros_parametrodetalle(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: gestionNomina_t_acumulado_empleado_def gestionNomina_t_acum_modulo_id_92ff28f3_fk_parametro; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionNomina_t_acumulado_empleado_def"
    ADD CONSTRAINT "gestionNomina_t_acum_modulo_id_92ff28f3_fk_parametro" FOREIGN KEY (modulo_id) REFERENCES public.parametros_parametrodetalle(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: gestionNomina_t_acumulado_empleado gestionNomina_t_acum_periodo_nomina_id_8f05ea2c_fk_gestionNo; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionNomina_t_acumulado_empleado"
    ADD CONSTRAINT "gestionNomina_t_acum_periodo_nomina_id_8f05ea2c_fk_gestionNo" FOREIGN KEY (periodo_nomina_id) REFERENCES public."gestionNomina_t_periodo_nomina"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: gestionNomina_t_acumulado_empleado_def gestionNomina_t_acum_periodo_nomina_id_f53b5e49_fk_gestionNo; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionNomina_t_acumulado_empleado_def"
    ADD CONSTRAINT "gestionNomina_t_acum_periodo_nomina_id_f53b5e49_fk_gestionNo" FOREIGN KEY (periodo_nomina_id) REFERENCES public."gestionNomina_t_periodo_nomina"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: gestionNomina_t_acumulado_empleado gestionNomina_t_acum_tipo_nomina_id_26929396_fk_parametro; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionNomina_t_acumulado_empleado"
    ADD CONSTRAINT "gestionNomina_t_acum_tipo_nomina_id_26929396_fk_parametro" FOREIGN KEY (tipo_nomina_id) REFERENCES public.parametros_t_tipo_nomina(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: gestionNomina_t_acumulado_empleado_def gestionNomina_t_acum_tipo_nomina_id_595cc7c6_fk_parametro; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionNomina_t_acumulado_empleado_def"
    ADD CONSTRAINT "gestionNomina_t_acum_tipo_nomina_id_595cc7c6_fk_parametro" FOREIGN KEY (tipo_nomina_id) REFERENCES public.parametros_t_tipo_nomina(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: gestionNomina_t_logica_calculo gestionNomina_t_logi_concepto_id_ff1bbf85_fk_gestionCo; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionNomina_t_logica_calculo"
    ADD CONSTRAINT "gestionNomina_t_logi_concepto_id_ff1bbf85_fk_gestionCo" FOREIGN KEY (concepto_id) REFERENCES public."gestionConceptos_t_concepto_empresa"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: gestionNomina_t_logica_calculo gestionNomina_t_logi_empresa_id_4c9c0ad6_fk_gestionCl; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionNomina_t_logica_calculo"
    ADD CONSTRAINT "gestionNomina_t_logi_empresa_id_4c9c0ad6_fk_gestionCl" FOREIGN KEY (empresa_id) REFERENCES public."gestionClientes_t_empresa"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: gestionNomina_t_logica_calculo_filtro gestionNomina_t_logi_logica_calculo_id_207a2d24_fk_gestionNo; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionNomina_t_logica_calculo_filtro"
    ADD CONSTRAINT "gestionNomina_t_logi_logica_calculo_id_207a2d24_fk_gestionNo" FOREIGN KEY (logica_calculo_id) REFERENCES public."gestionNomina_t_logica_calculo"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: gestionNomina_t_logica_calculo gestionNomina_t_logi_modulo_id_70cef7f6_fk_parametro; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionNomina_t_logica_calculo"
    ADD CONSTRAINT "gestionNomina_t_logi_modulo_id_70cef7f6_fk_parametro" FOREIGN KEY (modulo_id) REFERENCES public.parametros_parametrodetalle(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: gestionNomina_t_logica_calculo gestionNomina_t_logi_tipo_nomina_id_77c268a7_fk_parametro; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionNomina_t_logica_calculo"
    ADD CONSTRAINT "gestionNomina_t_logi_tipo_nomina_id_77c268a7_fk_parametro" FOREIGN KEY (tipo_nomina_id) REFERENCES public.parametros_t_tipo_nomina(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: gestionNomina_t_periodo_nomina gestionNomina_t_peri_empresa_id_e02737bf_fk_gestionCl; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionNomina_t_periodo_nomina"
    ADD CONSTRAINT "gestionNomina_t_peri_empresa_id_e02737bf_fk_gestionCl" FOREIGN KEY (empresa_id) REFERENCES public."gestionClientes_t_empresa"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: gestionNomina_t_periodo_nomina gestionNomina_t_peri_tipo_nomina_id_97f113a0_fk_parametro; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionNomina_t_periodo_nomina"
    ADD CONSTRAINT "gestionNomina_t_peri_tipo_nomina_id_97f113a0_fk_parametro" FOREIGN KEY (tipo_nomina_id) REFERENCES public.parametros_t_tipo_nomina(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: gestionNomina_t_proceso_nomina gestionNomina_t_proc_periodo_nomina_id_87906a13_fk_gestionNo; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionNomina_t_proceso_nomina"
    ADD CONSTRAINT "gestionNomina_t_proc_periodo_nomina_id_87906a13_fk_gestionNo" FOREIGN KEY (periodo_nomina_id) REFERENCES public."gestionNomina_t_periodo_nomina"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: gestionNovedades_t_novedad_temporal gestionNovedades_t_n_concepto_id_d9e5b4fd_fk_gestionCo; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionNovedades_t_novedad_temporal"
    ADD CONSTRAINT "gestionNovedades_t_n_concepto_id_d9e5b4fd_fk_gestionCo" FOREIGN KEY (concepto_id) REFERENCES public."gestionConceptos_t_concepto_empresa"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: gestionNovedades_t_novedad_temporal gestionNovedades_t_n_contrato_id_24da56b1_fk_gestionCo; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionNovedades_t_novedad_temporal"
    ADD CONSTRAINT "gestionNovedades_t_n_contrato_id_24da56b1_fk_gestionCo" FOREIGN KEY (contrato_id) REFERENCES public."gestionContratos_t_contrato"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: gestionNovedades_t_novedad_temporal gestionNovedades_t_n_periodo_nomina_id_ce4fd767_fk_gestionNo; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionNovedades_t_novedad_temporal"
    ADD CONSTRAINT "gestionNovedades_t_n_periodo_nomina_id_ce4fd767_fk_gestionNo" FOREIGN KEY (periodo_nomina_id) REFERENCES public."gestionNomina_t_periodo_nomina"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: gestionNovedades_t_novedad_temporal gestionNovedades_t_n_tipo_nomina_id_d9639603_fk_parametro; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionNovedades_t_novedad_temporal"
    ADD CONSTRAINT "gestionNovedades_t_n_tipo_nomina_id_d9639603_fk_parametro" FOREIGN KEY (tipo_nomina_id) REFERENCES public.parametros_t_tipo_nomina(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: gestionReportes_parametroreporte gestionReportes_para_reporte_id_a7568a3f_fk_gestionRe; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."gestionReportes_parametroreporte"
    ADD CONSTRAINT "gestionReportes_para_reporte_id_a7568a3f_fk_gestionRe" FOREIGN KEY (reporte_id) REFERENCES public."gestionReportes_reporte"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: parametros_parametrodetalle parametros_parametro_parametro_id_496f09aa_fk_parametro; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.parametros_parametrodetalle
    ADD CONSTRAINT parametros_parametro_parametro_id_496f09aa_fk_parametro FOREIGN KEY (parametro_id) REFERENCES public.parametros_parametrogeneral(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: parametros_t_conceptos_salario parametros_t_concept_concepto_id_689ec1c0_fk_gestionCo; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.parametros_t_conceptos_salario
    ADD CONSTRAINT "parametros_t_concept_concepto_id_689ec1c0_fk_gestionCo" FOREIGN KEY (concepto_id) REFERENCES public."gestionConceptos_t_conceptos"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: parametros_t_conceptos_salario parametros_t_concept_tipo_salario_id_476ef608_fk_parametro; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.parametros_t_conceptos_salario
    ADD CONSTRAINT parametros_t_concept_tipo_salario_id_476ef608_fk_parametro FOREIGN KEY (tipo_salario_id) REFERENCES public.parametros_t_tipo_salario(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: parametros_t_subtipo_cotizante parametros_t_subtipo_codigo_cotizante_id_b779553b_fk_parametro; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.parametros_t_subtipo_cotizante
    ADD CONSTRAINT parametros_t_subtipo_codigo_cotizante_id_b779553b_fk_parametro FOREIGN KEY (codigo_cotizante_id) REFERENCES public.parametros_t_tipo_cotizante(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

\unrestrict d3Tbc9tRYqGyeA3gFPqgwCUlKqdHoBdc0z5A3JDFmN2UIFnoRChrBNeJhSGcm0J

