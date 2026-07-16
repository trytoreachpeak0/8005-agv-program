-- CallAGV2ZPEQP

-- [历史/已注释] sql | Oracle
SELECT *
FROM (
  SELECT workorder, lot, state, eqp, task,
         (SELECT AREA
          FROM fw_eqpres_eqpinformation tt
          WHERE tt.eqpno = (
            SELECT MAX(eqp)
            FROM fw_wip_trans
            WHERE sysid = (
              SELECT MAX(sysid)
              FROM fw_wip_trans ttt
              WHERE ttt.lot = t.lot
                AND ttt.task = '完工'
                AND NVL(ttt.remark, 'NA') NOT LIKE '取消%'
            )
          )
         ) area
  FROM V_FW_WIP_SUBLOT t
  WHERE STEP LIKE '装片烘烤%'
    AND state <> '关闭'
    AND task = '入站'
) t
WHERE (area LIKE 'A%' OR area LIKE 'B%' OR area LIKE 'N7%')
  AND NOT EXISTS (
    SELECT *
    FROM FW_FUNCTIONTEST_AVG tt
    WHERE tt.lot = t.lot
      AND tt.tag = 1
      AND tt.fl = '装片-装片烘烤'
  )
ORDER BY area;

-- sql | Oracle
SELECT *
FROM (
  SELECT workorder, lot, state, eqp, task,
         (SELECT AREA
          FROM fw_eqpres_eqpinformation tt
          WHERE tt.eqpno = (
            SELECT MAX(eqp)
            FROM fw_wip_trans
            WHERE sysid = (
              SELECT MAX(sysid)
              FROM fw_wip_trans ttt
              WHERE ttt.lot = t.lot
                AND ttt.task = '完工'
                AND NVL(ttt.remark, 'NA') NOT LIKE '取消%'
            )
          )
         ) area
  FROM V_FW_WIP_SUBLOT t
  WHERE STEP LIKE '装片烘烤%'
    AND state <> '关闭'
    AND task = '入站'
) t
WHERE (area LIKE 'A%' OR area LIKE 'B%')
  AND NOT EXISTS (
    SELECT *
    FROM FW_FUNCTIONTEST_AVG tt
    WHERE tt.lot = t.lot
      AND tt.tag = 1
      AND tt.fl = '装片-装片烘烤'
  )
ORDER BY area;

-- PointSql | SQL Server
SELECT TOP 1 Station_id
FROM StationInfo
WHERE Loc_id = :loc_id;
