-- RecordIntoMesHistory

-- sql | Oracle
UPDATE FW_MAT_DELIVERY
SET USERNAME = :agv_name
WHERE lot = :lotno
  AND eqp = :eqpno
  AND mattype = '引线框';
