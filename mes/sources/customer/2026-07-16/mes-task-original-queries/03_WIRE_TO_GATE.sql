-- 从MES获取焊线和键合完工送关卡的产品
-- TASK_TYPE: WIRE_TO_GATE
SELECT t.lot as SUBLOT,
       tt.area as AREA,
       t.eqp as EQP,
       t.step as STEP,
       t.wgdate AS DATES,
       ttt.PACKAGE AS PACKAGE
FROM   (
        SELECT t.*,
               (
                SELECT Max(t1.eqp)
                FROM   fw_wip_trans t1
                WHERE  t1.lot = t.lot
                       AND t1.dates = t.wgdate
                       AND t1.task = '完工'
               ) eqp
        FROM   (
                SELECT lot,
                       workorder,
                       step,
                       (
                        SELECT Max(dates)
                        FROM   fw_wip_trans tt
                        WHERE  tt.lot = t.lot
                               AND tt.task = '完工'
                       ) wgdate
                FROM   v_fw_wip_sublot t
                WHERE  step IN ( '焊线关卡' )
                       AND state <> '关闭'
                       AND task = '入库'
               ) t
       ) t,
       fw_eqpres_eqpinformation tt,
       v_fw_pc_workorder ttt
WHERE  t.eqp = tt.eqpno
       AND t.workorder = ttt.workorder
       AND tt.step in ( '焊线','键合')
