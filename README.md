# tjo-claude-plugins

Personal Claude Code plugin marketplace.

| Plugin | What it does |
|---|---|
| [explainer](plugins/explainer) | `explain`: picks the clearest explanation format (prose, diagram, page, video). `make-video`: narrated 3Blue1Brown-style videos. |
| [comments](plugins/comments) | `audit`: finds comments that do not earn their place and suggests a fix for each, grouped by fix size. |

## Install

```
claude plugin marketplace add trulsjo/tjo-claude-plugins
claude plugin install explainer@tjo-claude-plugins
claude plugin install comments@tjo-claude-plugins
```

Inside Claude Code: `/plugin marketplace add trulsjo/tjo-claude-plugins`, then `/plugin install explainer@tjo-claude-plugins`.
