# 视频平台审核

给助手发送视频，联合检查语音、字幕和全画面文字，分别指出 B站、小红书、抖音的发布风险、时间点、依据与修改建议。

这是可供 Codex 使用的技能。脚本负责提取证据和寻找可疑线索，助手负责结合完整语境、平台规则与发布场景复核。它不连接平台内部审核系统，也不保证过审。

## 能检查什么

- 每条音轨独立转写；语音、字幕和画面文字互不覆盖。
- 检查浏览器地址栏、水印、片头片尾、具体地址、二维码，以及拆分域名、口述号码、拆字联系方式和资源领取话术。
- 按平台、普通投稿/商业推广/带货/课程等场景分别判断。
- 包含58项检查点和26个来源记录。来源核查日期为2026-09-06；证据状态与适用范围单独记录，实际审核时需继续核对更新。
- 输出原文、时间点、平台差异、修改建议及未检查范围。

默认配置要求小红书和抖音画面不保留网址、疑似网址及具体地址。这是可调整的保守发布要求，不等同于平台普遍禁止一切网址。B站也需检查商业导流、恶意链接、隐私及课程限制。

## 安装与使用

将本仓库放入 Codex 的技能目录，例如：

```sh
git clone https://github.com/huangbai-AI/video-platform-review.git ~/.codex/skills/video-platform-review
```

如果该目录已经存在，请先保留已有内容，不要直接覆盖。安装后新建对话，发送视频并说：

> 用 $video-platform-review 按 B站、小红书、抖音检查这个视频，标出时间点和修改建议。

也可以只指定一个平台。发布偏好在 [user-profile.json](references/user-profile.json) 中配置。

## 本地识别依赖

当前提取脚本使用 Python 3、FFmpeg（含 ffprobe）、whisper.cpp 的 whisper-cli 和多语言语音模型；全画面文字及二维码识别使用 macOS Vision，需可用的 Swift 编译器。模型不包含在仓库中。其他系统需自行接入说明中的替代工具，当前脚本不会自动安装或切换。

依赖与模型配置见 [提取说明](references/extraction.md)。无需上传视频到云端。

```sh
python3 scripts/extract_video.py /视频路径.mp4 --out /空的证据目录 --model /模型路径.bin
python3 scripts/scan_candidates.py /证据目录/evidence.json --out /证据目录/candidates.json
```

默认抽样每秒约两帧，并补场景切换。严格排查闪现网址时使用 `--fps 0` 逐帧扫描；抽样无法排除短暂文字。逐帧识别也可能漏读模糊小字，仍需查看原帧。

## 规则与资料

- [技能完整流程](SKILL.md)
- [58项审核清单](references/checklist.md)
- [三平台差异](references/platforms.md)
- [规则来源与获取状态](references/sources.json)
- [规则更新方法](references/source-refresh.md)
- [报告与验收示例](references/report-and-tests.md)
- [GitHub类似项目比较](references/github-projects.md)
- [参考技能评估](references/local-reference-review.md)

关键词命中仅表示需要复核。否定、反诈、科普、正常引用和实际营销需区别判断；缺少封面、标题、资质或授权材料时，不声称已检查这些部分。此工具不自动发布、上传或覆盖原视频。

## 验证

```sh
python3 scripts/test_candidates.py
```

现有35组文本测试覆盖网址变体、号码、误报、平台区别、否定语境、原文保留和跨帧拼接。开发时另以合成视频验证过中文语音、双音轨、全画面文字及单帧网址；测试素材和语音模型不随仓库发布。这些测试不是平台审核准确率评测。
