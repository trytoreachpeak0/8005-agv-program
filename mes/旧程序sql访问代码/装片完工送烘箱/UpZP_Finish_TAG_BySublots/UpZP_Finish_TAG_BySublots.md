```C# 
// 450行 送烘箱软件
private void UpZP_Finish_TAG_BySublots(List<string> sublots)
        {
            try
            {
                string sql = null;
                if (sublots.Count > 0)
                {
                    OracleConnection conn = new OracleConnection(ORACON);
                    conn.Open();
                    for (int i = 0; i < sublots.Count; i++)
                    {
                        sql = "update FW_FUNCTIONTEST_AVG set tag = 1 where lot='" + sublots[i] + "'  ";
                        OracleCommand cmd = new OracleCommand(sql, conn);
                        cmd.ExecuteNonQuery();
                        Addlist("装片任务:组装批次[" + sublots[i] + "]运送标记已更新");
                    }
                    conn.Close();
                }
            }
            catch (Exception ex)
            {
                Addlist("根据组装批次更新运送标记时发生异常");
                Addlist(ex.Message);
            }
        }
```

## 代码说明

**功能概述：** 对一批 **组装批次 lot 列表** 批量更新 MES 运送标记，表示装片完工送烘箱任务已处理。

**Oracle 更新 SQL 做了什么：**
- 循环：`update FW_FUNCTIONTEST_AVG set tag = 1 where lot='某sublot'`
- `tag=1`：已运送/已处理标记
- 表 `FW_FUNCTIONTEST_AVG` 在查询侧用 `fl='装片-装片烘烤'` 过滤，更新语句未写 `fl` 条件

**调用方：** `UpZPFinish_TAG_ByAreaNo`、`CancelQXJOB_Click_1` 等先查 lot 列表再调用本方法。

---

### 同文件内其他代码片段说明

**`UpZPFinish_TAG_ByAreaNo`：** 按区域查待送烘烤 lot → 调用本方法打标（详见 `UpZPFinish_TAG_ByAreaNo.md`）。

**`HKSPEC`：** 查 lot 烘烤规格（详见 `HKSPEC.md`）。

**`RecordIntoMesHistory`：** 更新 `FW_MAT_DELIVERY.USERNAME` 记录 AGV 配送人（详见 `RecordIntoMesHistory.md`）。

锐评：根据sublot去把标志位打为1