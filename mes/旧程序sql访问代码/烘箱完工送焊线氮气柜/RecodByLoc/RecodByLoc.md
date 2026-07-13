```C#
private void RecodByLoc(string locid)
        {
            try
            {
                if (String.IsNullOrEmpty(locid))
                {
                    Addlist("区域信息不允许为空，请检查后重试！");
                    return;
                }
                SqlConnection con = new SqlConnection(strSQLcon);
                con.Open();
                string sql = " select * from (SELECT  workorder,lot,state,eqp,task," +
                             " (select AREA from fw_eqpres_eqpinformation tt where tt.eqpno = (select max(eqp) " +
                              " from fw_wip_trans ttt where ttt.lot = t.lot and ttt.task = '完工' and nvl(ttt.remark, 'NA')" +
                              " not like '取消%')) area" +
                              " FROM V_FW_WIP_SUBLOT t WHERE STEP LIKE '装片烘烤%'" +
                             " and state<>'关闭' and task = '入站') t where ( area like 'A%' or area like 'B%' or area like 'N%' ) " +
                             " and not exists(select * from FW_FUNCTIONTEST_AVG tt where tt.lot = t.lot and tt.tag = 1 and tt.fl = '装片-装片烘烤') order by area  ";
                OracleConnection conn = new OracleConnection(ORACON);
                conn.Open();
                OracleCommand cmd = new OracleCommand(sql, conn);
                OracleDataReader rd = cmd.ExecuteReader();
                while (rd.Read())
                {
                    if (!String.IsNullOrEmpty(rd["LOT"].ToString()))
                    {
                        string Inssql = "Insert Into XLOTtable Values ('" + rd["LOT"].ToString() + "','T3') ";
                        SqlCommand InCmd = new SqlCommand(Inssql, con);
                        InCmd.ExecuteNonQuery();
                    }
                }
                rd.Close();
                con.Close();
                conn.Close();
                Addlist("区域[" + locid + "]的DFN结批送烘箱任务已记录到本地");
            }
            catch (Exception ex)
            {
                Addlist("区域[" + locid + "]记录DFN结批送烘箱任务记录到本地发生异常");
                Addlist("异常信息[" + ex.Message + "]");
            }
        }
```

## 代码说明

**功能概述：** 按区域将「装片完工、待送烘箱」的 DFN 结批批次记录到本地 SQL Server 表，供 AGV/烘箱程序后续调度使用。

**数据库：**
- **Oracle（MES）**：查询待送烘箱批次
- **SQL Server（本地）**：写入 `XLOTtable`

**Oracle 查询 SQL 做了什么：**
1. 从 `V_FW_WIP_SUBLOT` 取工序为「装片烘烤%」、状态非「关闭」、任务为「入站」的子批
2. 通过 `fw_wip_trans` 找该 lot 最近一次非「取消%」的「完工」记录，关联 `fw_eqpres_eqpinformation` 得到机台所在 **区域（area）**
3. 只保留区域以 A/B/N 开头的批次
4. 排除已在 `FW_FUNCTIONTEST_AVG` 中标记（`tag=1`，分类 `装片-装片烘烤`）的 lot
5. 按区域排序

**SQL Server 插入 SQL 做了什么：**
- 将查到的每个 `LOT` 插入本地 `XLOTtable`，类型固定为 `'T3'`（表示某类送烘箱任务）

**注意：** 参数 `locid` 仅用于日志提示，实际查询未按该区域过滤；存在 SQL 拼接，有注入风险。

锐评：这个函数的引用为0，根本就没用掉，感觉像是原先程序为了去重做的