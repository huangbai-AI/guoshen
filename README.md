# 过审 · guoshen

给 AI 一条视频，按 **通用规则 + 单平台规则** 检查语音、字幕与画面，给出可回看的时间点、依据和改法。支持 **小红书、抖音、B站、视频号**。

过审是一套开放的审核预检流程，不是永久有效的禁词表，也不连接平台内部审核系统。规则会变，案例有语境；我们把来源、时间和不确定性一起保留下来。

![视频、语音、字幕与画面一起检查](assets/illustrations/01-review.png)

## 怎么用

将仓库放入 Codex 技能目录；已有同名目录时先备份：

```sh
git clone https://github.com/huangbai-AI/guoshen.git ~/.codex/skills/guoshen
```

新建对话，发送视频并说：

> 用 $guoshen 检查这条视频在小红书、抖音、B站、视频号的发布风险，标出原文、时间点、依据和改法。

也可以只指定一个平台，或补充“这是商业合作”“只是加热失败”。审核结果分别标记：明确风险、需复核、按你的要求修改、未发现明显问题、未检查。不会给虚构的通过率。

当前提取工具使用 Python 3、FFmpeg、whisper.cpp 的 whisper-cli 与多语言模型；全画面文字和二维码识别使用 macOS Vision，需要 Swift。模型不随仓库发布。其他系统的接入方案见 [提取说明](references/extraction.md)，当前不会自动切换工具。

```sh
python3 scripts/build_review_context.py --platforms xiaohongshu douyin bilibili wechat_channels --as-of 2026-09-07 --out /tmp/review-context.json
python3 scripts/extract_video.py /视频路径.mp4 --out /空的证据目录 --model /模型路径.bin
python3 scripts/scan_candidates.py /证据目录/evidence.json --out /证据目录/candidates.json
```

日期改为实际审核日期。脚本提取证据、召回线索；**AI 助手结合完整上下文复核并写报告**，不是跑完命令就自动得出违规结论。独立运行脚本的接入方需要自行提供这一步。[完整审核流程](docs/ai-review.md) 写明输入、核查顺序、提示词和输出要求。

默认约每秒两帧并补场景切换；严格排查闪现地址使用 `--fps 0` 逐帧识别，仍需回看小字与模糊画面。未完成全片检查时不能声称“零网址”。

## 通用逻辑，平台分别维护

![通用规则与四个平台规则叠加](assets/illustrations/02-rules.png)

| 层级 | 内容 | 入口 |
| --- | --- | --- |
| 通用规则 | 违法危险、隐私、真实性、版权、广告、AI标识等58项检查问题 | [通用清单](rules/common/checklist.md) |
| 平台规则 | 平台社区规则、导流、官方入口与专项场景 | [小红书](rules/platforms/xiaohongshu.md) · [抖音](rules/platforms/douyin.md) · [B站](rules/platforms/bilibili.md) · [视频号](rules/platforms/wechat_channels.md) |
| 来源与时间 | 官方正文、入口、二手资料分开；记录适用期与复核日期 | [来源台账](references/sources.json) · [版本治理](docs/rule-lifecycle.md) |
| 个人要求 | 可选的更保守发布偏好，不冒充官方禁令 | [公开默认](references/user-profile.json) · [严格地址模式](profiles/strict-address.json) |

当前有26条结构化检查规则、28个来源记录。来源记录不等于28份已取得的官方全文；**视频号运营规范正文已核实，外链、直播、电商等专项仍须按场景补查**；来源缺口必须输出需复核。各条核查日期单独记录，重构代码不会刷新旧来源的核查日期。

不把“小红书/抖音出现任何网址必违规”或“B站任何网址都允许”写成统一结论。需结合实际导流目的、官方挂载权限、商业场景和当期条款。严格地址模式只是用户可选要求；扫描时加 `--profile profiles/strict-address.json`。

## 把卡审经历变成可复核的案例

![拒审与通过案例对照，复核后更新规则](assets/illustrations/03-cases.png)

**拒审 → 保存通知与版本 → 对照修改和重试 → 提出假设 → 人工复核 → 更新有日期的规则。** 通过、申诉成功和与既有判断相反的案例，同样有价值。

- [案例区与填写说明](cases/README.md)：把事实、平台通知、AI推断和干扰因素分开。
- [提交案例](https://github.com/huangbai-AI/guoshen/issues/new?template=case.yml)：先匿名化，上传即公开，请勿包含私人原片、联系方式或未获授权截图。
- [提议规则修订](https://github.com/huangbai-AI/guoshen/issues/new?template=rule-change.yml)：补来源、日期、适用场景和反例。
- [贡献指南](CONTRIBUTING.md)：欢迎 PR，支持新增平台、提取工具、规则和分析方法。

当前提供5个**模拟填写示例**，真实案例区尚待社区贡献。模拟示例不计入统计、不作为规则证据。“删掉一个内容后通过”只能支持假设，不能单独证明它就是拒审原因。

## 开发与验证

```sh
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate_framework.py
python3 scripts/test_candidates.py
python3 scripts/test_framework.py
```

自动检查数据格式、日期、跨文件引用和平台隔离；人工复核负责证据真实性、适用语境与匿名化。这些测试不是平台审核准确率测评。历史拒审不能仅用今天的规则倒推；过期规则和正文缺口须保留在报告中。

延伸资料：[技能入口](SKILL.md) · [类似开源项目](references/github-projects.md) · [更新记录](CHANGELOG.md) · [配图说明](assets/illustrations/README.md)。

原创代码和文档使用 [MIT 许可](LICENSE)；第三方规则及引用的权利说明见 [NOTICE](NOTICE)。
