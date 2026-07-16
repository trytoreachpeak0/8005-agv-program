```C#
public bool CheckDFNLOT(string LOT)
        {
            try
            {
                string sql = "SELECT  count(*) " +
                             " FROM V_FW_WIP_SUBLOT t WHERE STEP LIKE '装片烘烤%' " +
                             " and state<>'关闭' and task='入站' and lot='" + LOT + "'";
                OracleConnection con = new OracleConnection(ORACON);
                con.Open();
                OracleCommand cmd = new OracleCommand(sql, con);
                int Result = Convert.ToInt16(cmd.ExecuteScalar().ToString());
                con.Close();
                if (Result > 0)
                {
                    return true;
                }
                else
                {
                    return false;
                }

            }
            catch (Exception ex)
            {
                Addlist("查询MES中DFN结批工作令[" + LockLotNo.Text + "]发生异常");
                Addlist("异常信息[" + ex.Message + "]");
                return false;
            }
        }
```

## 代码说明

**功能概述：** 校验指定 lot 是否为 MES 中有效的「DFN 结批、装片烘烤待入站」批次。

**Oracle 查询 SQL 做了什么：**
- `SELECT count(*)` from `V_FW_WIP_SUBLOT`
- 条件：`STEP LIKE '装片烘烤%'`、`state<>'关闭'`、`task='入站'`、`lot=传入LOT`
- `count > 0` 返回 `true`，否则 `false`

**用途：** 扫码/录入工作令或 lot 时的合法性检查，确认该批确实处于待送烘箱前的装片烘烤入站状态。