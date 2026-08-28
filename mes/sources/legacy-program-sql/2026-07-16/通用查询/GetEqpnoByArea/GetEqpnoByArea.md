```C#
public string GetEqpnoByArea(string areano)
        {
            string Result = null;
            try
            {
                string sql = "select eqpno from fw_eqpres_eqpinformation where area='"+areano+"' and step='装片' ";
                OracleConnection conn = new OracleConnection(ORACON);
                conn.Open();
                OracleCommand cmd = new OracleCommand(sql, conn);
                Result = cmd.ExecuteScalar().ToString();
                conn.Close();
                return Result;
            }
            catch (Exception ex)
            {
                Addlist("根据区域号[" + areano + "]获取机台号信息发生异常");
                Addlist("异常信息[" + ex.Message + "]");
                return Result;
            }
        }
```

## 代码说明

**功能概述：** 根据 **区域号** 查询该区域下 **装片工序** 的机台号。

**Oracle 查询 SQL 做了什么：**
- `select eqpno from fw_eqpres_eqpinformation where area=区域号 and step='装片'`
- 一个区域可能有多台机，此处用 `ExecuteScalar` 只取一条

**用途：** 区域 → 机台反向查询，用于按区域触发送料或更新 MES 状态。