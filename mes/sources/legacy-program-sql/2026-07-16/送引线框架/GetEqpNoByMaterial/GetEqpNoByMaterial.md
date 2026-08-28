```C#
public string GetEqpNoByMaterial(string material)
        {
            ZPLotNoStr = null;
            string Result = null;
            try
            {

                OracleConnection conn = new OracleConnection(ORACON);
                conn.Open();
                string sql = " select  t.eqp,get_wip_eqpstep(t.eqp) lotno " +
                              " from v_fw_material_indetail t where "+
                              " t.sublot='"+material+"' and t.type = '引线框' " +
                              " and t.state = '上机' ";
                OracleCommand cmd = new OracleCommand(sql,conn);
                OracleDataReader rd = cmd.ExecuteReader();
                while (rd.Read())
                {
                    Result = rd["eqp"].ToString();
                    ZPLotNoStr = rd["lotno"].ToString();
                }
                rd.Close();
                conn.Close();
                if (!String.IsNullOrEmpty(Result))
                {
                    Addlist("查询到子批信息绑定[" + Result + "]机台");
                }
                else
                {
                    Addlist("查询子批对应机台号失败，请确认录入子批信息是否正确");
                    //ProLotNoTxt.Clear();
                    //ProLotNoTxt.Focus();
                }
                return Result;               
            }
            catch (Exception ex)
            {
                Addlist("查询子批对应机台号失败，请确认录入子批信息是否正确");
                //ProLotNoTxt.Clear();
                //ProLotNoTxt.Focus();
                ZPLotNoStr = null;
                return Result;
            }
        }
```

## 代码说明

**功能概述：** 根据物料子批号（引线框 sublot）反查其当前上机的 **机台号** 及机台在制 **lotno**。

**Oracle 查询 SQL 做了什么：**
- `v_fw_material_indetail`：`sublot=物料号`、`type='引线框'`、`state='上机'`
- 返回 `eqp`（机台）、`get_wip_eqpstep(t.eqp) lotno`（该机台当前 WIP 步骤对应 lot）
- 结果写入 `Result`（机台）和全局 `ZPLotNoStr`（lot）

**用途：** 扫码引线框子批后，定位应对应哪台装片机，用于发料间 → 机台的 AGV 送料任务。