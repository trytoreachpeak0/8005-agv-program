```C#
private void CancelQXJOB_Click_1(object sender, EventArgs e)
        {
            try
            {

                if (MessageBox.Show(this, "确认取消所有机台配送任务？", "取消任务提示", MessageBoxButtons.YesNo) == DialogResult.Yes)
                {
                    tabControl1.SelectedIndex = 0;
                    zp_finish_sublots.Clear();
                    /*
                    string sql = " select * " +
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
                    string sql = " select * " +
                            " from(SELECT workorder," +
                            " lot,state, eqp,task,(select AREA from fw_eqpres_eqpinformation tt " +
                            " where tt.eqpno = (select max(eqp) from fw_wip_trans where " +
                            " sysid = (select max(sysid) from fw_wip_trans ttt  where ttt.lot = t.lot" +
                            " and ttt.task = '完工' and nvl(ttt.remark, 'NA') not like '取消%') )) area " +
                            " FROM V_FW_WIP_SUBLOT t WHERE STEP LIKE '装片烘烤%' and state<> '关闭' " +
                            " and task = '入站') t where(area like 'A%' or area like 'B%') " +
                            " and not exists(select * from FW_FUNCTIONTEST_AVG tt where tt.lot = t.lot " +
                            " and tt.tag = 1  and tt.fl = '装片-装片烘烤') order by area ";
                    OracleConnection conn = new OracleConnection(ORACON);
                    conn.Open();
                    OracleCommand cmd = new OracleCommand(sql, conn);
                    OracleDataReader rd = cmd.ExecuteReader();
                    while (rd.Read())
                    {
                        if (!String.IsNullOrEmpty(rd["area"].ToString()))
                        {
                            zp_finish_sublots.Add(rd["lot"].ToString());
                        }
                    }
                    rd.Close();
                    conn.Close();
                    UpZP_Finish_TAG_BySublots(zp_finish_sublots);
                    //LotNoTxt.ReadOnly = true;
                    //GetZPAreaList();
                    //if (AreaList.Count > 0)
                    //{
                    //    for (int i = 0; i < AreaList.Count; i++)
                    //    {
                    //        UpdateAGVHXFlagByArea(AreaList[i]);
                    //    }
                    //    Addlist("宿迁老厂所有装片完工待送烘烤任务状态已记录");
                    //}
                    if (CheckProInBoxFlag() == true)
                    {
                        AGVProFinishFlag = true;
                        return;
                    }
                    CallAGVFlag = false;
                    LockLotNo.ReadOnly = false;
                }
            }
            catch (Exception ex)
            {
                Addlist("手动取消装片完工送烘烤任务失败,异常：" + ex.Message);
            }
        }
```

## 代码说明

**功能概述：** 用户确认后「取消所有机台配送任务」——从 MES 查出当前待送烘烤的装片完工批次，批量打运送标记，并复位 AGV 呼叫相关界面状态。

**Oracle 查询 SQL 做了什么：**
1. 与 `GetZPAreaList` / `CallAGV2ZPEQP` 同类逻辑：装片烘烤工序、入站、未关闭
2. 通过 `fw_wip_trans` 最大 `sysid` 的完工记录关联机台区域
3. 区域过滤为 **A% 或 B%**（注释掉的旧版还包含 N7%）
4. 排除 `FW_FUNCTIONTEST_AVG` 中已标记 `tag=1` 且 `fl='装片-装片烘烤'` 的 lot
5. 将符合条件的 `lot` 加入 `zp_finish_sublots` 列表

**后续调用：**
- `UpZP_Finish_TAG_BySublots`：把这些 lot 在 `FW_FUNCTIONTEST_AVG` 中 `tag` 置为 1（视为已处理/已取消配送）
- `CheckProInBoxFlag()`：检查发料间是否在途任务
- 设置 `CallAGVFlag = false`，解锁 `LockLotNo`

**业务含义：** 手动批量「清掉」装片完工待送烘烤任务，避免 AGV 继续调度。