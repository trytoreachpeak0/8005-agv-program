-- 从MES获取派工待送区送往指定焊线和键合机台的产品
-- TASK_TYPE: STAGING_TO_WIRE
SELECT t.lot AS SUBLOT,
       tt.area AS AREA,
       t.step AS STEP,
       t.eqp AS EQP,
       t.lasttime AS DATES,
       ttt.PACKAGE AS PACKAGE
FROM   v_fw_wip_sublot t,
       fw_eqpres_eqpinformation tt,
       v_fw_pc_workorder ttt
WHERE  t.eqp = tt.eqpno
       AND t.workorder = ttt.workorder
       AND t.step IN ( '焊线', '键合' )
       AND t.task = '入站'
       AND t.state <> '关闭'
