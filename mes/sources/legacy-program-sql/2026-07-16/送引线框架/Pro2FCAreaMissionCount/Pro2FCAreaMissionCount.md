```C#
public int Pro2FCAreaMissionCount()
        {
            int Result = 0;
            try
            {
                OracleConnection conn = new OracleConnection(ORACON);
                conn.Open();
                string sql = " select count(*) from v_fw_material_indetail t,fw_eqpres_eqpinformation tt where " +
                             " t.eqp=tt.eqpno and t.type='引线框' and t.state='上机' and nvl(t.yxkagv,0)=0 and " +
                             " tt.step='倒装'";
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

**功能概述：** 统计 **倒装（FC）工序** 机台上待 AGV 配送的引线框任务数量。

**Oracle 查询 SQL 做了什么：**
- `count(*)`，物料明细联机台信息表
- 条件：引线框、上机、`yxkagv=0`、`fw_eqpres_eqpinformation.step='倒装'`

**用途：** 判断倒装区域发料间是否还有待配送任务，用于 AGV 优先级或是否继续轮询。