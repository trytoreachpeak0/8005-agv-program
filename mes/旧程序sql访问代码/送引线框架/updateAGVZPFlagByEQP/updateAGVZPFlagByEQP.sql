-- updateAGVZPFlagByEQP

-- sql | Oracle
UPDATE fw_material_indetail
SET yxkagv = 1
WHERE eqp = :eqpno
  AND state = '上机'
  AND code IN (
    SELECT code
    FROM fw_eng_material
    WHERE type = '引线框'
  );
