# REA readiness and browser-observation boundary

Checked 2026-11-14 (Asia/Karachi). Research-only inspection; no REA installation, package acquisition, Codex configuration change, browser launch, native-provider installation or application-code modification was performed by this investigation scope.

## Local observations

| Check | Observed result | What it establishes |
| --- | --- | --- |
| Active agent tool metadata, narrow REA namespace/browser-tool-name search | No REA tools exposed | REA MCP is not usable from this running agent session. |
| Shared skill | `C:/Users/habiba/.agents/skills/reverse-engineer-anything/SKILL.md`, skill metadata version 42; examples pinned to rea-agents 6.7.0 | Instructions are installed. A skill is not an MCP server or an installed analysis runtime. |
| Shell command lookup | `rea`, `rea.cmd`, `rea.ps1` not resolved | No shell-visible REA CLI on this shell's PATH; not proof no other installation exists. |
| Usual global npm package location | No `C:/Users/habiba/AppData/Roaming/npm/node_modules/rea-agents/package.json` found | Bounded negative check of this one common global installation path only. |
| User Codex config | `C:/Users/habiba/.codex/config.toml` parsed; no `mcp_servers.rea` or args mentioning `rea-agents` candidate, no exact `rea` plugin config key | No explicit REA registration found in this inspected layer. Unrelated config values, environment maps and credentials were not printed or retained. |
| Project Codex config | `C:/Finova AlignIQ/.codex/config.toml` absent | No project-local registration in this location. |
| Plugin-only alternative | `codex plugin list --json` returned zero REA matches in its installed projection; remote marketplace listing failed due network access | No REA plugin established by this check. Remote/plugin-managed state is not comprehensively established. A failed remote listing is not evidence of an installed or broken REA server. |
| Node / npm | Node **v24.12.0**, npm **11.6.2** | Existing shell runtime versions; neither was changed. |
| Existing browser executables | Chrome `157.0.8103.51` at `C:/Program Files/Google/Chrome/Application/chrome.exe`; Edge `157.0.4341.46` at `C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe` | Files/version metadata only; neither browser was launched or attached by this readiness check. |

Codex help/list emitted non-fatal sandbox warnings about its temporary PATH-alias directory. No access policy was changed to suppress them. No `rea doctor` output exists: the CLI is absent and invoking npx could acquire a package. Therefore no provider readiness, CDP attachment, REA screenshot, REA Evidence ID or successful MCP handshake is claimed.

## Official upstream documents reviewed

- [REA README](https://github.com/morluto/rea/blob/main/README.md): role, installation separation, target classes and release limitations.
- [Installation and setup](https://github.com/morluto/rea/blob/main/docs/getting-started/installation.md): client-scoped dry-run, backups, bundled skill, runtime limits and plugin-only caveat.
- [Website observation with CDP](https://github.com/morluto/rea/blob/main/docs/guides/web/browser-observation.md): target scope, data minimization and capture limits.
- [Worked browser guide](https://rea.tools/guides/browser/): example observation sequence; it demonstrates REA, not PMCEASY.
- [Published npm metadata](https://registry.npmjs.org/rea-agents/latest) and [upstream package](https://github.com/morluto/rea/blob/main/package.json): both identify **6.9.0** at observation time and Node `^22.23.4 || ^24.22.1 || >=26.12.1`. Local Node 24.12.0 does not satisfy that requirement. Repository-main capabilities must still be checked against the selected installed release's actual schemas.
- [Official OpenAI CLI reference](https://learn.chatgpt.com/docs/cli/reference): installed-plugin listing and MCP commands. The skill copy and config inspection above are local evidence, not a product-wide installation inventory.

## Supported next setup, only after approval

REA configuration is unnecessary to complete the current public-page/screenshot gap analysis through available alternatives. If REA is wanted for a later authorized observation, first select an existing supported Node runtime or separately approve installing/upgrading one. REA setup does not upgrade Node/npm. No Hopper, Ghidra, IDA, Java, Frida or packet-capture tooling is required merely to inspect a website with a Chrome-family browser. [Setup guide](https://github.com/morluto/rea/blob/main/docs/getting-started/installation.md)

Run package acquisition outside the target project from a trusted directory. The following are **proposed, not executed**; npx can download software and write its cache even for doctor/dry-run:

```powershell
# After approval of package acquisition and selection of a compatible Node:
npx -y rea-agents@6.9.0 doctor --client codex --json
npx -y rea-agents@6.9.0 setup --client codex --dry-run --json

# Only after reviewing/approving the actual dry-run's exact paths,
# changes, backups and bundled-skill replacement:
npx -y rea-agents@6.9.0 setup --client codex --yes
```

The concrete dry-run has not run, so exact proposed write/backup paths are **not known**; the inspected default config path is not substituted for a setup plan. The installed skill's 6.7.0 examples are older than the observed 6.9.0 release; do not silently run them as proof of current support. After approved setup, restart/reconnect Codex and verify REA tools actually appear. Doctor checks configuration/prerequisites, not the active agent connection. Avoid installing a second server if a plugin-owned one is subsequently found. [Setup and plugin guidance](https://github.com/morluto/rea/blob/main/docs/getting-started/installation.md)

## Future browser capture constraints

Use a fresh dedicated profile, loopback debugging with an explicit port, and an exact `allowed_origins` filter such as `https://www.pmceasy.com`; add another origin only if the authorized task actually requires it. Discover and select the intended target before capture. A passive window sees only activity during attachment; missing traffic does not prove absence. Passive inspection and declared action scenarios have different authority. Close only owned browser resources. [CDP guide](https://github.com/morluto/rea/blob/main/docs/guides/web/browser-observation.md)

For this task, exclude cookies/tokens/storage, raw request/response bodies, unrelated tabs/origins and source-code export. Accessibility text and screenshots can themselves contain personal information, so use only public pages and omit or sanitize identifying example details. URL queries may survive REA credential redaction: the tool's built-in filtering is not a general de-identification guarantee. No authenticated PMCEASY observation, paid-product execution or server-side algorithm reconstruction is established by REA readiness. [CDP data minimization](https://github.com/morluto/rea/blob/main/docs/guides/web/browser-observation.md#data-minimization)

## Search and completeness boundary

This is a bounded inspection of the current tool set, PATH, one global npm location, user/project Codex configuration and a partially available plugin listing. Other accounts, remote Codex hosts, arbitrary npm caches and system-wide filesystem installations were not searched. The finding is **REA unavailable in this session**, with no matching registration in the inspected layers; it is not an exhaustive assertion that REA has never been installed anywhere.
