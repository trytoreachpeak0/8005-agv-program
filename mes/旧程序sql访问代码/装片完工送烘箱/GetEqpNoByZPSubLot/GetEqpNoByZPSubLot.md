```C#
public string GetEqpNoByZPSubLot(string lotno)
        {
            string Result = null;
            try
            {
                string sql = "select eqp from FW_FUNCTIONTEST_AVG tt where tt.lot = '"+lotno+"' ";
                OracleConnection conn = new OracleConnection(ORACON);
                conn.Open();
                OracleCommand cmd = new OracleCommand(sql,conn);
                Result = cmd.ExecuteScalar().ToString();
                conn.Close();
                return Result;
            }
            catch(Exception ex)
            {
                Addlist("根据装片随件单["+lotno+"]获取机台号信息发生异常");
                Addlist("异常信息["+ex.Message+"]");
                return Result;
            }
        }
```

## 代码说明

**功能概述：** 根据装片 **随件单 lot** 从功能测试/运送标记表反查关联 **机台号**。

**Oracle 查询 SQL 做了什么：**
- `select eqp from FW_FUNCTIONTEST_AVG where lot = lotno`
- `FW_FUNCTIONTEST_AVG` 存 lot 与机台、运送标记（tag）、分类（fl）等扩展信息

**用途：** 已知随件单号时定位送烘箱/装片完工对应的机台，用于后续更新标记或配送记录。