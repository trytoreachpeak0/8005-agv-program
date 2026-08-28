-- CheckDFNLOT

-- sql | Oracle
SELECT COUNT(*)
FROM V_FW_WIP_SUBLOT t
WHERE STEP LIKE '装片烘烤%'
  AND state <> '关闭'
  AND task = '入站'
  AND lot = :lotno;
