# 规范：GitHub Pages 文档部署

- `change slug`：`github-pages-deployment`
- 状态：`accepted`
- 负责人：qrlib maintainers

## 背景

仓库本地已经使用 `MkDocs + Material for MkDocs` 生成正确的文档站点，但远端 GitHub Pages 在缺少专用部署工作流时，会退回到默认的 Jekyll 渲染路径，直接把仓库中的 `docs/` 当作静态内容发布。

这会导致远端站点的主题、导航结构和本地 `mkdocs build` 产物不一致，也会让未来维护者误以为只要修改 `docs/` 就能得到与本地相同的线上效果。

## 目标

- 让 GitHub Pages 始终发布 `mkdocs build` 生成的 `site/` 目录
- 把文档部署路径固定为仓库内可审查的 GitHub Actions 工作流
- 保持项目页地址不变，继续使用 `https://qrhuang2021.github.io/qrlib/`
- 支持推送到 `main` 或 `master` 后自动部署，并支持手动触发部署

## 非目标

- 不引入 PR 预览部署
- 不切换到自定义域名
- 不把生成后的 `site/` 目录提交进 Git 仓库

## 公开契约

- 文档站点的唯一发布产物是 `mkdocs build` 输出的 `site/`
- `.github/workflows/docs.yml` 是 GitHub Pages 的规范发布入口
- 发布工作流必须在部署前执行依赖安装，并能直接运行 `mkdocs build`
- `mkdocs.yml` 必须声明与项目页一致的 `site_url`
- 远端文档视觉与导航应与本地 `mkdocs serve` / `mkdocs build` 结果保持一致

## 验收标准

- 仓库存在 `.github/workflows/docs.yml`
- 该工作流能在 `push` 到 `main` / `master` 时构建并部署 `site/`
- 该工作流支持 `workflow_dispatch`
- 本地 `mkdocs build` 仍可成功执行
- `AGENTS.md` 与维护者文档明确说明 Pages 采用 MkDocs 构建产物部署

## 兼容性与迁移

- GitHub Pages 访问地址保持不变
- 首次成功部署后，旧的 Jekyll 风格页面会被新的 MkDocs 产物覆盖
- 如果仓库的 Pages 尚未完全切换到 GitHub Actions，工作流应尽量通过 `actions/configure-pages` 自动完成启用
