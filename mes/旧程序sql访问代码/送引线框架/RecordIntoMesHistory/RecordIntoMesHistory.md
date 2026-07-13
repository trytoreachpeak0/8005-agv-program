```C#
private void RecordIntoMesHistory(string lotno,string eqpno)
        {
            try
            {
                string sql = " update FW_MAT_DELIVERY set USERNAME='"+AGVName+"' "+
                             " where lot='"+lotno+"' and eqp='"+eqpno+"' and mattype='引线框'";
                OracleConnection conn = new OracleConnection(ORACON);
                conn.Open();
                OracleCommand cmd = new OracleCommand(sql,conn);
                cmd.ExecuteNonQuery();
                conn.Close();
                Addlist("机台["+eqpno+"] 组装批次["+lotno+"] 更新MES配送人信息");
            }
            catch(Exception ex)
            {
                Addlist("机台["+eqpno+"] 组装批次["+lotno+"] 更新MES配送人异常");
                Addlist("异常内容["+ex.Message+"]");
            }
        }
```

## 代码说明

**功能概述：** AGV 完成配送后，在 MES 物料配送表中记录 **配送人（AGV 名称）**。

**Oracle 更新 SQL 做了什么：**
- `UPDATE FW_MAT_DELIVERY SET USERNAME = AGVName`
- 条件：`lot`、`eqp`、`mattype='引线框'`
- **含义：** 将指定 lot+机台+引线框类型的配送记录的操作人更新为当前 AGV 标识

**用途：** MES 追溯：谁（哪台 AGV）完成了该批引线框到机台的配送。