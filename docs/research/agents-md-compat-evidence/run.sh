#!/usr/bin/env bash
# usage: CFG=<config dir> [ADDENV=1] run.sh <cwd> <tag> <read-path or -> [extra claude args...]
CC="$LOCALAPPDATA/Claude-Data/claude_pzs8sxrjxfjjc/claude-code/2.1.330/9424831ad51c/claude.exe"
root=/c/work/8005-scratch/agents-md-compat
d="$1"; tag="$2"; rp="$3"; shift 3
cd "$d" || exit 9
keep_add="$ADDENV"; cfg="$CFG"
for v in $(env | grep -oE '^CLAUDE[A-Z_]*'); do unset "$v"; done
unset AI_AGENT
export CLAUDE_CONFIG_DIR="$cfg"
[ -n "$keep_add" ] && export CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1
export ANTHROPIC_BASE_URL=http://127.0.0.1:18798 ANTHROPIC_API_KEY=local-probe-placeholder CLAUDE_CODE_MAX_RETRIES=0
prompt="PROBE-$tag"; [ "$rp" != "-" ] && prompt="$prompt READ=$rp"
"$CC" -p --model haiku --tools Read --allowedTools Read --debug-file "$root/logs/$tag.debug.log" "$@" -- "$prompt" < /dev/null > "$root/logs/$tag.out" 2>&1
echo "exit=$?"
