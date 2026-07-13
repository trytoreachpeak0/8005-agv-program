```C#
public int Pro2ZPAreaMissionCount()
        {
            int Result = 0;
            try
            {
                OracleConnection conn = new OracleConnection(ORACON);
                conn.Open();
                string sql = " select count(*) from v_fw_material_indetail t,fw_eqpres_eqpinformation tt where " +
                             " t.eqp=tt.eqpno and t.type='引线框' and t.state='上机' and nvl(t.yxkagv,0)=0 and " +
                             " (tt.area like 'A%' or tt.area like 'B%')";
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

**功能概述：** 统计 **装片区（A%/B% 区域）** 上待 AGV 配送的引线框任务数量。

**Oracle 查询 SQL 做了什么：**
- `count(*)` from `v_fw_material_indetail` join `fw_eqpres_eqpinformation`
- 条件：引线框、上机、`yxkagv=0`、区域 `A%` 或 `B%`

**用途：** 与 FC、TR 计数配合，判断装片区域发料间待办数量，决定 AGV 是否继续处理发料任务。