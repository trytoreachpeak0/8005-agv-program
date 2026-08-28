```C#
private void GetEQPList()
        {
            try
            {
                Addlist("正在加载待配送物料机台号列表信息......");
                AreaList = new List<string>();
                //ZPEQPNeedProDGV.DataSource = null;
                //ZPEQPNeedProDGV.Rows.Clear();
                //ZPEQPNeedProDGV.ReadOnly = true;
                //ZPEQPList.Text = null;
                //ZPEQPList.Items.Clear();
                OracleConnection conn = new OracleConnection(ORACON);
                conn.Open();
                string sqlZP = " select t.eqp,max(tt.area) from v_fw_material_indetail t,fw_eqpres_eqpinformation tt where" +
                             " t.eqp = tt.eqpno and t.type = '引线框' and t.state = '上机' and nvl(t.yxkagv,0)= 0 and " +
                             " (tt.area like 'A%' or tt.area like 'B%') group by t.eqp";
                OracleCommand cmdZP = new OracleCommand(sqlZP, conn);
                OracleDataReader rdZP = cmdZP.ExecuteReader();
                while (rdZP.Read())
                {
                    AreaList.Add(rdZP["eqp"].ToString());
                }
                rdZP.Close();

                string sqlFC = " select t.eqp,max(tt.area) from v_fw_material_indetail t,fw_eqpres_eqpinformation tt where" +
                             " t.eqp = tt.eqpno and t.type = '引线框' and t.state = '上机' and nvl(t.yxkagv,0)= 0 and " +
                             " tt.step='倒装' group by t.eqp";
                OracleCommand cmdFC = new OracleCommand(sqlFC,conn);
                OracleDataReader rdFC = cmdFC.ExecuteReader();
                while (rdFC.Read())
                {
                    AreaList.Add(rdFC["eqp"].ToString());
                }
                rdFC.Close();

                string sqlTR = " select t.eqp,max(tt.area) from v_fw_material_indetail t,fw_eqpres_eqpinformation tt where" +
                             " t.eqp = tt.eqpno and t.type = '引线框' and t.state = '上机' and nvl(t.yxkagv,0)= 0 and " +
                             " (t.eqp like '1ZP%' or t.eqp like '2ZP%') group by t.eqp";
                OracleCommand cmdTR = new OracleCommand(sqlTR,conn);
                OracleDataReader rdTR = cmdTR.ExecuteReader();
                while (rdTR.Read())
                {
                    AreaList.Add(rdTR["eqp"].ToString());
                }
                rdTR.Close();
                conn.Close();
                Addlist("待配送物料机台号列表信息加载完成");
            }
            catch(Exception ex)
            {
                Addlist("获取待配送物料机台号列表信息发生异常");
                Addlist("异常内容["+ex.Message+"]");
            }
        }
```

## 代码说明

**功能概述：** 汇总三类「待发料/待配送引线框」场景的 **机台号列表**，写入 `AreaList`（此处变量名实为机台列表，非区域）。

**Oracle 查询 SQL（三条，结构相同，过滤不同）：**

| SQL | 关联表 | 核心条件 | 场景 |
|-----|--------|----------|------|
| sqlZP | `v_fw_material_indetail` + `fw_eqpres_eqpinformation` | 引线框上机、`yxkagv=0`、区域 A%或B% | 宿迁装片区发料 |
| sqlFC | 同上 | `yxkagv=0`、`tt.step='倒装'` | 倒装工序发料 |
| sqlTR | 同上 | `yxkagv=0`、机台号 like `1ZP%` 或 `2ZP%` | 特定 ZP 产线发料 |

公共条件：`type='引线框'`、`state='上机'`、`nvl(yxkagv,0)=0`（未送 AGV）。  
`group by t.eqp`，`max(tt.area)` 取区域。

**用途：** 轮询或展示所有有待配送物料的机台，驱动发料间 AGV 任务生成。