-- HKSPEC

-- sql | Oracle
SELECT t.*
FROM (
  SELECT t.*,
         tt.eqp eqp2,
         tt.step step2,
         get_mat_bomspec(tt.step, t.workorder, '装片胶') dbspec,
         get_mat_dbspec_hk(t.STEP, t.WorkOrder, 0) hkspec,
         (SELECT MAX(area) FROM fw_eqpres_eqpinformation ttt WHERE ttt.eqpno = tt.eqp) area
  FROM (
    SELECT workorder, lot, state, eqp, task, step,
           (SELECT MAX(sysid)
            FROM fw_wip_trans tt
            WHERE tt.lot = t.lot
              AND task = '完工'
              AND NVL(remark, 'NA') NOT LIKE '取消%') id
    FROM V_FW_WIP_SUBLOT t
    WHERE STEP LIKE '装片烘烤%'
      AND state <> '关闭'
      AND task = '入站'
  ) t, fw_wip_trans tt
  WHERE t.id = tt.sysid
) t
WHERE lot = :lotno;
