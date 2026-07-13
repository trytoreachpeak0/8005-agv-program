-- 从MES获取装片完工送焊线键合的产品
-- TASK_TYPE: DIE_TO_WIRE_STAGING
SELECT t.lot AS SUBLOT,
       tt.area AS AREA,
       t.eqp AS EQP,
       t.step AS STEP,
       wgdate AS DATES
FROM   (SELECT t.*,
               (SELECT Max(eqp)
                FROM   fw_wip_trans t1
                WHERE  t1.lot = t.lot
                       AND t1.dates = t.wgdate
                       AND t1.task = '完工') eqp
        FROM   (SELECT lot,
                       workorder,
                       step,
                       (SELECT Max(dates)
                        FROM   fw_wip_trans tt
                        WHERE  tt.lot = t.lot
                               AND task = '完工') wgdate
                FROM   v_fw_wip_sublot t
                WHERE  step IN ( '焊线', '键合' )
                       AND state <> '关闭'
                       AND task = '入库') t) t,
       fw_eqpres_eqpinformation tt
WHERE  t.eqp = tt.eqpno
       AND tt.step = '装片'
