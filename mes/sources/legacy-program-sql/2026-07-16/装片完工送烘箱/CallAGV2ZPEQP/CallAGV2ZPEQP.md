```C#
public bool CallAGV2ZPEQP()
        {
            //zp_finish_sublots.Clear();
            try
            {
                List<string> loc_id_str = new List<string>();
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
                        loc_id_str.Add(rd["area"].ToString());
                    }
                }
                rd.Close();
                conn.Close();
                string FirstLocStr = GetBiggerLocByNowArea(loc_id_str);
                if (String.IsNullOrEmpty(FirstLocStr))
                {
                    FirstLocStr = GetFirstLocByPosID(loc_id_str);
                }
                if (!String.IsNullOrEmpty(FirstLocStr))
                {

                    string pointstr = null;
                    string PointSql = "select top 1 Station_id from StationInfo where Loc_id = '" + FirstLocStr + "' ";
                    SqlConnection con = new SqlConnection(strSQLcon);
                    con.Open();
                    SqlCommand sqlcmd = new SqlCommand(PointSql, con);
                    pointstr = sqlcmd.ExecuteScalar().ToString();
                    con.Close();
                    if (!String.IsNullOrEmpty(pointstr))
                    {
                        this.Invoke(new MethodInvoker(delegate { AGVMoveTo.Text = FirstLocStr; }));
                        ADDORDER(Convert.ToInt16(pointstr));
                        return true;
                    }
                    else
                    {
                        Addlist("区域号[" + FirstLocStr + "] 未绑定地图点位 请联系管理员确认");
                        return false;
                    }
                }
                else
                {
                    Addlist("未能从MES中获取到装片完工待送烘烤任务对应的信息！");
                    return false;
                }
            }
            catch (Exception ex)
            {
                Addlist("装片完工任务呼叫小车时发生异常");
                Addlist(ex.Message);
                return false;
            }
        }
```

## 代码说明

**功能概述：** **装片完工送烘烤** 场景下呼叫 AGV：从 MES 取待送批次所在区域，选定目标区域后查本地地图点位并下发移动订单。

**Oracle 查询 SQL 做了什么：**
- 与 `ZPMatFinishedCount` 相同逻辑，但 `select *` 取明细
- 将每行非空 `area` 加入 `loc_id_str`
- 经 `GetBiggerLocByNowArea` / `GetFirstLocByPosID` 选一个优先区域 `FirstLocStr`

**SQL Server 查询 SQL 做了什么：**
- `select top 1 Station_id from StationInfo where Loc_id = 区域号`
- 将 MES 区域号映射为 AGV 地图 **站点 ID（Station_id）**

**后续：** `ADDORDER(站点ID)` 向 AGV 系统下单，界面显示 `AGVMoveTo`。

**双库分工：** Oracle = 业务批次与区域；SQL Server = AGV 地图/站点配置。