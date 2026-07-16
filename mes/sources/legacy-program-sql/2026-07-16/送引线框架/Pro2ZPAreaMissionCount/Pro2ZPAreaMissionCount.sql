-- Pro2ZPAreaMissionCount

-- sql | Oracle
SELECT COUNT(*)
FROM v_fw_material_indetail t, fw_eqpres_eqpinformation tt
WHERE t.eqp = tt.eqpno
  AND t.type = '引线框'
  AND t.state = '上机'
  AND NVL(t.yxkagv, 0) = 0
  AND (tt.area LIKE 'A%' OR tt.area LIKE 'B%');
