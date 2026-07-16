-- LoadDGVByZPEQP

-- [历史/已注释] sql | Oracle
SELECT t.sublot, t.spec, t.eqp, get_wip_eqpstep(t.eqp) lotno
FROM v_fw_material_indetail t
WHERE t.eqp = :eqpno
  AND t.type = '引线框'
  AND t.state = '上机'
  AND NVL(t.yxkagv, 0) = 0;
