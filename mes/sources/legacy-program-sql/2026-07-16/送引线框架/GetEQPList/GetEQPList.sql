-- GetEQPList

-- sqlZP | Oracle
-- --- sqlZP
SELECT t.eqp, MAX(tt.area)
FROM v_fw_material_indetail t, fw_eqpres_eqpinformation tt
WHERE t.eqp = tt.eqpno
  AND t.type = '引线框'
  AND t.state = '上机'
  AND NVL(t.yxkagv, 0) = 0
  AND (tt.area LIKE 'A%' OR tt.area LIKE 'B%')
GROUP BY t.eqp;

-- sqlFC | Oracle
-- --- sqlFC
SELECT t.eqp, MAX(tt.area)
FROM v_fw_material_indetail t, fw_eqpres_eqpinformation tt
WHERE t.eqp = tt.eqpno
  AND t.type = '引线框'
  AND t.state = '上机'
  AND NVL(t.yxkagv, 0) = 0
  AND tt.step = '倒装'
GROUP BY t.eqp;

-- sqlTR | Oracle
-- --- sqlTR
SELECT t.eqp, MAX(tt.area)
FROM v_fw_material_indetail t, fw_eqpres_eqpinformation tt
WHERE t.eqp = tt.eqpno
  AND t.type = '引线框'
  AND t.state = '上机'
  AND NVL(t.yxkagv, 0) = 0
  AND (t.eqp LIKE '1ZP%' OR t.eqp LIKE '2ZP%')
GROUP BY t.eqp;
