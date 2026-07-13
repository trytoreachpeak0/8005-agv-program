-- 从MES获取派工待送区送往指定焊线和键合机台的产品
-- TASK_TYPE: STAGING_TO_WIRE
SELECT t.lot AS SUBLOT,
       tt.area AS AREA,
       t.step AS STEP,
       t.eqp AS EQP,
       t.lasttime AS DATES
FROM   v_fw_wip_sublot t,
       fw_eqpres_eqpinformation tt
WHERE  t.eqp = tt.eqpno
       AND t.step IN ( '焊线', '键合' )
       AND t.task = '入站'
       AND t.state <> '关闭'
