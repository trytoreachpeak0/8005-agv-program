```C#
public int Pro2TRAreaMissionCount()
        {
            int Result = 0;
            try
            {
                OracleConnection conn = new OracleConnection(ORACON);
                conn.Open();
                string sql = " select count(*) from v_fw_material_indetail t,fw_eqpres_eqpinformation tt where " +
                             " t.eqp=tt.eqpno and t.type='引线框' and t.state='上机'  and (t.eqp like '1ZP%' or t.eqp like '2ZP%') "+
                             " and nvl(t.yxkagv,0)= 0 ";
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

**功能概述：** 统计 **TR 产线（1ZP%/2ZP% 机台）** 上待 AGV 配送的引线框任务数量。

**Oracle 查询 SQL 做了什么：**
- `count(*)` from `v_fw_material_indetail t` join `fw_eqpres_eqpinformation tt` on `t.eqp=tt.eqpno`
- 条件：引线框、上机、`yxkagv=0`、机台号匹配 `1ZP%` 或 `2ZP%`

**用途：** 发料间调度时判断 TR 区域是否还有待送任务（与 `Pro2ZPAreaMissionCount`、`Pro2FCAreaMissionCount` 分区计数）。