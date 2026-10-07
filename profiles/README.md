# 配置说明

配置表达个人发布要求，不改变官方规则的适用条件。

| 配置 | 路径 | 行为 |
| --- | --- | --- |
| 公开默认 | [references/user-profile.json](../references/user-profile.json) | 四平台中性预检，不强制禁用所有网址 |
| 可选严格地址模式 | [strict-address.json](strict-address.json) | 小红书、抖音画面中的网址、疑似网址及具体地址按用户要求提示修改 |

默认配置保留原路径；两个配置的原有内容均保留。只有用户明确要求时才启用严格地址模式，候选命中仍需回看原帧确认识别。

`build_review_context.py` 与 `scan_candidates.py` 均支持 `--profile <配置路径>`；用法见 [使用指南](../docs/usage.md)。配置不能代替全片检查，未完成逐帧检查时不能宣称“零网址”。

[返回首页](../README.md)
