-- GetMESLocIDByEQP

-- sql | Oracle
SELECT t.area
FROM fw_eqpres_eqpinformation t
WHERE t.eqpno = :eqpno;
