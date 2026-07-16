```C#
private void GetZPAreaList()
        {
            try
            {
                Addlist("正在加载待送烘烤物料区域号列表信息......");
                AreaList = new List<string>();
                OracleConnection conn = new OracleConnection(ORACON);
                conn.Open();
                string sql = " select * from (SELECT  workorder,lot,state,eqp,task," +
                             " (select AREA from fw_eqpres_eqpinformation tt where tt.eqpno = (select max(eqp) " +
                              " from fw_wip_trans ttt where ttt.lot = t.lot and ttt.task = '完工' and nvl(ttt.remark, 'NA')" +
                              " not like '取消%')) area" +
                              " FROM V_FW_WIP_SUBLOT t WHERE STEP LIKE '装片烘烤%'" +
                             " and state<>'关闭' and task = '入站') t where ( area like 'A%' or area like 'B%' or area like 'N%' ) " +
                             " and not exists(select * from FW_FUNCTIONTEST_AVG tt where tt.lot = t.lot and tt.tag = 1 and tt.fl = '装片-装片烘烤') order by area  ";
                OracleCommand cmd = new OracleCommand(sql, conn);
                OracleDataReader rd = cmd.ExecuteReader();
                while (rd.Read())
                {
                    AreaList.Add(rd["area"].ToString());
                }
                rd.Close();
                conn.Close();
                Addlist("装片完工机台区域号信息加载完成");
            }
            catch (Exception ex)
            {
                Addlist("加载待送烘烤设备区域号发生异常");
                Addlist(ex.Message);
            }
        }
```

## 代码说明

**功能概述：** 加载「装片完工、待送烘烤」任务涉及的 **机台区域号列表**，存入 `AreaList`。

**Oracle 查询 SQL 做了什么：**
1. 主表 `V_FW_WIP_SUBLOT`：工序 `装片烘烤%`，`task='入站'`，`state<>'关闭'`
2. 子查询从 `fw_wip_trans` 取该 lot 最近一次有效「完工」机台，再查 `fw_eqpres_eqpinformation.AREA`
3. 区域限定 A%/B%/N%
4. `NOT EXISTS FW_FUNCTIONTEST_AVG`：排除已打运送标记的批次
5. 按 `area` 排序；代码将每行 `area` 加入 `AreaList`（可能有重复区域）

**用途：** 为按区域批量更新烘箱/AGV 标记（如 `UpZPFinish_TAG_ByAreaNo`）提供区域枚举。