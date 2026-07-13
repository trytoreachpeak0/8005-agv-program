```C#
private void LoadDGVByZPEQP(string eqpno)
        {
            //try
            //{
            //    ZPEQPLocID = GetMESLocIDByEQP(eqpno);
            //    ZPEQPNeedProDGV.DataSource = null;
            //    ZPEQPNeedProDGV.Rows.Clear();
            //    ZPEQPNeedProDGV.ReadOnly = true;
            //    OracleConnection conn = new OracleConnection(ORACON);
            //    conn.Open();
            //    string sql = " select t.sublot,t.spec,t.eqp,get_wip_eqpstep(t.eqp) " +
            //                  " lotno from v_fw_material_indetail t where t.eqp = '"+eqpno+"' and t.type = '引线框' " +
            //                  " and t.state = '上机' and nvl(t.yxkagv,0)= 0 ";
            //    OracleDataAdapter cmd = new OracleDataAdapter(sql, conn);
            //    DataTable dt = new DataTable();
            //    cmd.Fill(dt);
            //    ZPEQPNeedProDGV.DataSource = dt.DefaultView;
            //    conn.Close();
            //    Addlist("机台["+eqpno+"]待送物料信息已加载");

            //}
            //catch(Exception ex)
            //{
            //    Addlist("加载机台["+eqpno+"]待送物料信息发生异常");
            //    Addlist("异常内容["+ex.Message+"]");
            //    ProLotNoTxt.Clear();
            //    ProLotNoTxt.Focus();
            //}
        }
```

## 代码说明

**功能概述：** 按机台号加载「待送物料」到界面 DataGridView（**当前整段实现已被注释，实际不执行**）。

**被注释的 Oracle 查询 SQL 做了什么：**
- 表/视图：`v_fw_material_indetail`
- 条件：`eqp=机台号`、`type='引线框'`、`state='上机'`、`nvl(yxkagv,0)=0`（尚未标记 AGV 配送）
- 返回：`sublot`（子批）、`spec`、`eqp`、`get_wip_eqpstep(t.eqp) lotno`（机台当前在制 lot）

**用途（设计意图）：** 在发料间送料场景，展示某装片机台上已上机、待 AGV 配送的引线框物料明细。