-- UpZP_Finish_TAG_BySublots

-- sql | Oracle | 循环批量更新
UPDATE FW_FUNCTIONTEST_AVG
SET tag = 1
WHERE lot = :lotno;
