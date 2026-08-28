-- GetEqpNoByMaterial

-- sql | Oracle
SELECT t.eqp, get_wip_eqpstep(t.eqp) lotno
FROM v_fw_material_indetail t
WHERE t.sublot = :material
  AND t.type = '引线框'
  AND t.state = '上机';
