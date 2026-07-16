-- GetEqpnoByArea

-- sql | Oracle
SELECT eqpno
FROM fw_eqpres_eqpinformation
WHERE area = :areano
  AND step = '装片';
