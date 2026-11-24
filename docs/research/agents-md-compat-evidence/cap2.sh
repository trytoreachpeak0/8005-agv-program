#!/usr/bin/env bash
# usage: cap.sh <dir> <capdir-tag> [extra claude args...]  -- sends one prompt to local sink on 18765, logs debug
CC="$LOCALAPPDATA/Claude-Data/claude_pzs8sxrjxfjjc/claude-code/2.1.330/9424831ad51c/claude.exe"
root=/c/work/8005-scratch/agents-md-compat
d="$1"; tag="$2"; shift 2
cd "$d" || exit 9
for v in $(env | grep -oE '^CLAUDE[A-Z_]*'); do unset "$v"; done
unset AI_AGENT
[ -n "$CFG" ] && export CLAUDE_CONFIG_DIR="$CFG"
export ANTHROPIC_BASE_URL=http://127.0.0.1:18765 ANTHROPIC_API_KEY=sk-ant-dummy-local-capture CLAUDE_CODE_MAX_RETRIES=0
"$CC" -p --model haiku --tools "" --debug-file "$root/logs/$tag.debug.log" "$@" -- "PROBE-$tag" < /dev/null > "$root/logs/$tag.out" 2>&1
echo "exit=$?"
