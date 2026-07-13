-- 从MES获取装片完工送烘箱的产品
-- TASK_TYPE: DIE_TO_OVEN
SELECT t.lot AS SUBLOT,
       tt.area AS AREA,
       t.eqp AS EQP,
       t.step AS STEP,
       t.wgdate AS DATES
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
                WHERE  step IN ( '装片烘烤', '装片压力烘烤' )
                       AND state <> '关闭'
                       AND task = '入站'
               ) t
       ) t,
       fw_eqpres_eqpinformation tt
WHERE  t.eqp = tt.eqpno
       AND tt.step = '装片'
