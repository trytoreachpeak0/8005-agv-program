SELECT 'WIRE_TO_FULL_INSPECTION' AS TASK_TYPE,
       t.lot AS SUBLOT, tt.area AS AREA, t.eqp AS EQP,
       t.step AS STEP, t.wgdate AS DATES, ttt.PACKAGE AS PACKAGE
FROM (
       SELECT t.*,
              (SELECT MAX(t1.eqp) FROM fw_wip_trans t1
                WHERE t1.lot = t.lot AND t1.dates = t.wgdate AND t1.task = '完工') eqp
       FROM (
              SELECT lot, workorder, step,
                     (SELECT MAX(dates) FROM fw_wip_trans tt
                       WHERE tt.lot = t.lot AND tt.task = '完工') wgdate
              FROM v_fw_wip_sublot t
              WHERE step ='焊线全检'
                AND state <> '关闭'
                AND task = '完工'
            ) t
     ) t,
     fw_eqpres_eqpinformation tt,
     v_fw_pc_workorder ttt
WHERE t.eqp = tt.eqpno
  AND t.workorder = ttt.workorder
  AND tt.step in ('焊线','键合')
