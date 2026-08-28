```C#
public string HKSPEC(string lot)
        {
            try
            {
                string Result = null;
                string sql = "select t.* from (select t.*,tt.eqp eqp2,tt.step step2,get_mat_bomspec(tt.step,t.workorder,'装片胶') dbspec,get_mat_dbspec_hk(t.STEP,t.WorkOrder,0) hkspec," +
                            " (select MAX(area) from fw_eqpres_eqpinformation ttt where ttt.eqpno=tt.eqp) area " +
                            " from  (SELECT workorder, lot, state, eqp, task,step,(select max(sysid) from fw_wip_trans tt where tt.lot=t.lot and task='完工' and nvl(remark,'NA') not like '取消%') id " +
                            " FROM V_FW_WIP_SUBLOT t " +
                            " WHERE STEP LIKE '装片烘烤%' " +
                            " and state <> '关闭' " +
                            " and task = '入站') t,fw_wip_trans tt where t.id=tt.sysid) t where  lot='" + lot + "'";
                OracleConnection con = new OracleConnection(ORACON);
                con.Open();
                OracleCommand cmd = new OracleCommand(sql, con);
                OracleDataReader rd = cmd.ExecuteReader();
                while (rd.Read())
                {
                    Result = rd["HKSPEC"].ToString();
                }
                rd.Close();
                con.Close();
                return Result;
            }
            catch
            {
                return null;
            }
        }
```

## 代码说明

**功能概述：** 根据 lot 查询该批在装片烘烤入站阶段的 **烘烤规格（HKSPEC）**，供烘箱程序按规格设温/设时。

**Oracle 查询 SQL 做了什么（较复杂）：**
1. 内层：从 `V_FW_WIP_SUBLOT` 取装片烘烤%、入站、未关闭批次，并算 `fw_wip_trans` 最近有效完工的 `sysid` 为 `id`
2. 中层：与 `fw_wip_trans` 关联得完工机台 `eqp2`、步骤 `step2`
3. 调用 Oracle 函数：
   - `get_mat_bomspec(...,'装片胶')` → 装片胶 BOM 规格
   - `get_mat_dbspec_hk(STEP, WorkOrder, 0)` → **烘烤规格 hkspec**
4. 子查询 `fw_eqpres_eqpinformation` 得 `area`
5. 外层 `where lot = 指定lot`，读取 `HKSPEC` 字段返回

**用途：** 送烘箱前按 MES 物料/工艺规则确定烘烤参数，避免人工查规格。