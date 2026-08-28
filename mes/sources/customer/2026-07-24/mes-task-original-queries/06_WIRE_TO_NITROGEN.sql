-- 从MES获取焊线1完工送氮气柜的产品（等待进入焊线2）
-- TASK_TYPE: WIRE_TO_NITROGEN
-- 业务：WireBond1（MES step=焊线）→ 固定氮气柜；PDA 入柜后本行从快照消失
SELECT t.lot AS SUBLOT,
       tt.area AS AREA,
       t.eqp AS EQP,
       t.step AS STEP,
       wgdate AS DATES,
       ttt.PACKAGE AS PACKAGE
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
                WHERE  step = '焊线2'
                       AND state <> '关闭'
                       AND task = '入库') t) t,
       fw_eqpres_eqpinformation tt,
       v_fw_pc_workorder ttt
WHERE  t.eqp = tt.eqpno
       AND t.workorder = ttt.workorder
       AND tt.step = '焊线'
