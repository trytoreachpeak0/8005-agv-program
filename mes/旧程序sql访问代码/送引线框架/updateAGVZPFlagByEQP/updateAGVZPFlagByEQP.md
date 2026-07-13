```C#
private void UpdateAGVZPFlagByEQP(string eqpno)
        {
            try
            {
                OracleConnection conn = new OracleConnection(ORACON);
                conn.Open();
                string sql = " UPDATE fw_material_indetail SET yxkagv = 1 WHERE "+
                             " eqp='"+eqpno+"' and state='上机' and code in "+
                             " (select code from fw_eng_material where type='引线框')";
                OracleCommand cmd = new OracleCommand(sql, conn);
                cmd.ExecuteNonQuery();
                conn.Close();
                Addlist("机台["+eqpno+"]对应待送物料记录状态已更新");
                RecordIntoXlot(eqpno,AGVWorkType);
            }
            catch(Exception ex)
            {
                Addlist("更新机台["+eqpno+"]对应发料间送料任务状态信息时发生异常");
                Addlist("异常内容["+ex.Message+"]");
            }
        }
```

## 代码说明

**功能概述：** 某机台发料配送任务创建后，在 MES 标记该机台上机引线框「已由 AGV 处理」，并写入本地任务记录。

**Oracle 更新 SQL 做了什么：**
- `UPDATE fw_material_indetail SET yxkagv = 1`
- 条件：`eqp=机台号`、`state='上机'`，且 `code` 属于 `fw_eng_material` 中 `type='引线框'` 的物料编码
- **含义：** `yxkagv=1` 表示该上机引线框已纳入/完成 AGV 配送流程，避免重复下发

**后续：** 调用 `RecordIntoXlot(eqpno, AGVWorkType)` 在本地 SQL Server 记录任务（非本段 SQL）。