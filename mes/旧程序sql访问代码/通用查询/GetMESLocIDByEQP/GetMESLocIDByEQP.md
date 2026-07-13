```C#
public  string GetMESLocIDByEQP(string eqpno)
        {
            string Result = null;
            try
            {
                OracleConnection conn = new OracleConnection(ORACON);
                conn.Open();
                string sql = " select t.area from fw_eqpres_eqpinformation t where t.eqpno = '"+eqpno+"'";
                OracleCommand cmd = new OracleCommand(sql,conn);
                Result = cmd.ExecuteScalar().ToString();
                conn.Close();
                return Result;
            }
            catch
            {
                return Result;
            }
        }
```

## 代码说明

**功能概述：** 根据机台号查询 MES 中的 **物理区域号（area）**。

**Oracle 查询 SQL 做了什么：**
- `select t.area from fw_eqpres_eqpinformation t where t.eqpno = 机台号`
- 返回该机台在设备资源表中的区域编码

**用途：** 机台 → 区域映射，用于 AGV 导航（区域对应 `StationInfo.Loc_id`）、按区域汇总任务等。