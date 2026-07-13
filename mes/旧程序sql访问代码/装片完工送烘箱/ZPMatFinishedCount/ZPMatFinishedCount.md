```C#
public int ZPMatFinishedCount()
        {
            int Result = 0;
            try
            {
                OracleConnection conn = new OracleConnection(ORACON);
                conn.Open();
                /*
                string sql = " select count(*) " +
                             " from(SELECT workorder," +
                             " lot,state, eqp,task,(select AREA from fw_eqpres_eqpinformation tt " +
                             " where tt.eqpno = (select max(eqp) from fw_wip_trans where " +
                             " sysid = (select max(sysid) from fw_wip_trans ttt  where ttt.lot = t.lot" +
                             " and ttt.task = '完工' and nvl(ttt.remark, 'NA') not like '取消%') )) area " +
                             " FROM V_FW_WIP_SUBLOT t WHERE STEP LIKE '装片烘烤%' and state<> '关闭' " +
                             " and task = '入站') t where(area like 'A%' or area like 'B%' or area like 'N7%') " +
                             " and not exists(select * from FW_FUNCTIONTEST_AVG tt where tt.lot = t.lot " +
                             " and tt.tag = 1  and tt.fl = '装片-装片烘烤') order by area ";
                */
                string sql = " select count(*) " +
                             " from(SELECT workorder," +
                             " lot,state, eqp,task,(select AREA from fw_eqpres_eqpinformation tt " +
                             " where tt.eqpno = (select max(eqp) from fw_wip_trans where " +
                             " sysid = (select max(sysid) from fw_wip_trans ttt  where ttt.lot = t.lot" +
                             " and ttt.task = '完工' and nvl(ttt.remark, 'NA') not like '取消%') )) area " +
                             " FROM V_FW_WIP_SUBLOT t WHERE STEP LIKE '装片烘烤%' and state<> '关闭' " +
                             " and task = '入站') t where(area like 'A%' or area like 'B%') " +
                             " and not exists(select * from FW_FUNCTIONTEST_AVG tt where tt.lot = t.lot " +
                             " and tt.tag = 1  and tt.fl = '装片-装片烘烤') order by area ";
                OracleCommand cmd = new OracleCommand(sql, conn);
                Result = Convert.ToInt32(cmd.ExecuteScalar().ToString());
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

**功能概述：** 统计当前 MES 中 **装片完工、待送烘烤** 的批次总数（与呼叫 AGV 送烘箱的核心查询一致）。

**Oracle 查询 SQL 做了什么：**
- 内层：装片烘烤%、入站、未关闭的 `V_FW_WIP_SUBLOT`
- 通过 `fw_wip_trans` 最大 sysid 完工记录关联 `fw_eqpres_eqpinformation` 得 `area`
- 外层：`area like A% or B%`，且 `FW_FUNCTIONTEST_AVG` 中无 `tag=1` + `fl='装片-装片烘烤'` 记录
- 对结果 `count(*)`

**用途：** 轮询判断是否存在装片完工送烘箱任务；为 0 时可能不触发 `CallAGV2ZPEQP`。