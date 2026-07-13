```C#
private void UpZPFinish_TAG_ByAreaNo(string areastr)
        {
            zp_finish_sublots.Clear();
            try
            {
                OracleConnection conn = new OracleConnection(ORACON);
                conn.Open();
                /* szy 11/12
                string sql = " select * " +
                               " from(SELECT workorder," +
                               " lot,state, eqp,task,(select AREA from fw_eqpres_eqpinformation tt " +
                               " where tt.eqpno = (select max(eqp) from fw_wip_trans where " +
                               " sysid = (select max(sysid) from fw_wip_trans ttt  where ttt.lot = t.lot" +
                               " and ttt.task = '完工' and nvl(ttt.remark, 'NA') not like '取消%') )) area " +
                               " FROM V_FW_WIP_SUBLOT t WHERE STEP LIKE '装片烘烤%' and state<> '关闭' " +
                               " and task = '入站') t where(area like 'A%' or area like 'B%' or area like 'N7%') " +
                               " and not exists(select * from FW_FUNCTIONTEST_AVG tt where tt.lot = t.lot " +
                               " and tt.tag = 1  and tt.fl = '装片-装片烘烤') and area = '"+areastr+"' order by area ";
                */
                string sql = " select * " +
                               " from(SELECT workorder," +
                               " lot,state, eqp,task,(select AREA from fw_eqpres_eqpinformation tt " +
                               " where tt.eqpno = (select max(eqp) from fw_wip_trans where " +
                               " sysid = (select max(sysid) from fw_wip_trans ttt  where ttt.lot = t.lot" +
                               " and ttt.task = '完工' and nvl(ttt.remark, 'NA') not like '取消%') )) area " +
                               " FROM V_FW_WIP_SUBLOT t WHERE STEP LIKE '装片烘烤%' and state<> '关闭' " +
                               " and task = '入站') t where(area like 'A%' or area like 'B%') " +
                               " and not exists(select * from FW_FUNCTIONTEST_AVG tt where tt.lot = t.lot " +
                               " and tt.tag = 1  and tt.fl = '装片-装片烘烤') and area = '" + areastr + "' order by area ";
                OracleCommand cmd = new OracleCommand(sql, conn);
                OracleDataReader rd = cmd.ExecuteReader();
                while (rd.Read())
                {
                    zp_finish_sublots.Add(rd["lot"].ToString());
                }
                rd.Close();
                conn.Close();
                UpZP_Finish_TAG_BySublots(zp_finish_sublots);
            }
            catch (Exception ex)
            {
                Addlist("更新区域号[" + areastr + "]对应装片完工送料任务状态信息时发生异常");
                Addlist("异常内容[" + ex.Message + "]");
            }
        }
```

## 代码说明

**功能概述：** 按 **指定区域号** 查出该区域待送烘烤的装片完工 lot 列表，并批量更新运送标记。

**Oracle 查询 SQL 做了什么：**
- 与 `CallAGV2ZPEQP` / `ZPMatFinishedCount` 同一套装片完工待送烘烤逻辑
- 额外条件：`area = areastr`（只处理该区域）
- 将 `lot` 填入 `zp_finish_sublots`

**后续：** 调用 `UpZP_Finish_TAG_BySublots`，对每个 lot 执行 `UPDATE FW_FUNCTIONTEST_AVG SET tag=1`

**业务含义：** 某区域 AGV 已取走/已处理完该批送烘箱任务后，在 MES 打标，避免重复呼叫。

锐评： 没屌用，就是根据某个区域查询到所有的批号，然后把这些批号都设置为1