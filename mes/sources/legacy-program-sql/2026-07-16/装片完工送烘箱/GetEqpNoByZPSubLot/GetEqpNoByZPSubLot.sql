-- GetEqpNoByZPSubLot

-- sql | Oracle
SELECT eqp
FROM FW_FUNCTIONTEST_AVG tt
WHERE tt.lot = :lotno;
