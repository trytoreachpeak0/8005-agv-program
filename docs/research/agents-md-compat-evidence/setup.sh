#!/usr/bin/env bash
set -e
cd /c/work/8005-scratch/agents-md-compat
mk(){ mkdir -p "$(dirname "$1")"; printf '%s\n' "${@:2}" > "$1"; }
rm -rf s; mkdir s; cd s
mk A/AGENTS.md            '# A' 'MARKER-A-AGENTS'
mk B/AGENTS.md            '# B' 'MARKER-B-AGENTS'
mk B/CLAUDE.md            '# B' 'MARKER-B-CLAUDE'
mk C/AGENTS.md            '# C' 'MARKER-C-AGENTS'
mk C/CLAUDE.md            '@AGENTS.md' '' '## Claude only' 'MARKER-C-CLAUDE-ONLY'
mk D/AGENTS.md            '# D' 'MARKER-D-AGENTS'
mk D/CLAUDE.local.md      '# D local' 'MARKER-D-LOCAL'
mk E/.claude/AGENTS.md    '# E' 'MARKER-E-DOTCLAUDE-AGENTS'
mk F/CLAUDE.md            '# F parent' 'MARKER-F-PARENT-CLAUDE'
mk F/sub/AGENTS.md        '# F sub' 'MARKER-F-SUB-AGENTS'
mk G/AGENTS.md            '# G parent' 'MARKER-G-PARENT-AGENTS'
mk G/sub/AGENTS.md        '# G sub' 'MARKER-G-SUB-AGENTS'
mk H/shared/CLAUDE.md     '# shared' 'MARKER-H-SHARED-CLAUDE'
mk H/shared/AGENTS.md     '# shared agents' 'MARKER-H-SHARED-AGENTS'
mk H/proj/CLAUDE.md       '@../shared/CLAUDE.md' '' 'MARKER-H-PROJ-CLAUDE'
mk H/proj2/AGENTS.md      '@../shared/AGENTS.md' '' 'MARKER-H-PROJ2-AGENTS'
mk I/AGENTS.md            '@extra.md' '' 'MARKER-I-AGENTS'
mk I/extra.md             'MARKER-I-IMPORTED-BY-AGENTS'
mk K/AGENTS.md            '# K' 'MARKER-K-AGENTS' '' '```' '@fenced.md' '```' '' 'Inline `@span.md` stays literal.'
mk K/fenced.md            'MARKER-K-FENCED-SHOULD-NOT-LOAD'
mk K/span.md              'MARKER-K-SPAN-SHOULD-NOT-LOAD'
mk L/cfg/AGENTS.md        'MARKER-L-USER-LEVEL-AGENTS'
mk L/cfg/CLAUDE.md        'MARKER-L-USER-LEVEL-CLAUDE'
mk L/proj/AGENTS.md       'MARKER-L-PROJ-AGENTS'
mkdir -p M

mk N/CLAUDE.md            '# N' 'MARKER-N-SAME-CONTENT'
cp N/CLAUDE.md N/AGENTS.md                      # byte-identical copy
mk N3/CLAUDE.md           '# N' 'MARKER-N3-SAME'
printf '# N\r\nMARKER-N3-SAME\r\n' > N3/AGENTS.md  # same text, CRLF line endings
# J: committed symlink CLAUDE.md -> AGENTS.md, cloned with the Windows default core.symlinks=false
mkdir Jsrc && ( cd Jsrc && git init -q && printf '# J\nMARKER-J-AGENTS\n' > AGENTS.md && git add AGENTS.md \
  && git update-index --add --cacheinfo 120000,"$(printf 'AGENTS.md' | git hash-object -w --stdin)",CLAUDE.md \
  && git -c user.name=t -c user.email=t@t commit -qm init )
git -c core.symlinks=false clone -q Jsrc J-nosym   # CLAUDE.md becomes a 9-byte text file "AGENTS.md"
git -c core.symlinks=true  clone -q Jsrc J-sym || true  # without Developer Mode: "unable to create symlink CLAUDE.md: Permission denied"
mkdir -p ../proj-settings/.claude && cp B/*.md ../proj-settings/ && cp ../both.settings.json ../proj-settings/.claude/settings.json
echo setup-ok
# X: ways around the external-import approval (section 4 of the report)
mkdir -p X/shared X/p1 X/p2/.claude X/p3/.claude X/p4/ws X/p5
printf 'MARKER-X-SHARED-CLAUDE\n' > X/shared/CLAUDE.md
printf '@link/CLAUDE.md\n\nMARKER-X-P1\n' > X/p1/CLAUDE.md
cmd //c mklink //J "$(cygpath -w "$PWD/X/p1/link")" "$(cygpath -w "$PWD/X/shared")"   # directory junction, no admin needed
printf 'MARKER-X-P2\n' > X/p2/CLAUDE.md
printf '{"permissions":{"additionalDirectories":["../shared"]},"env":{"CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD":"1"}}\n' > X/p2/.claude/settings.json
printf 'MARKER-X-P3\n' > X/p3/CLAUDE.md
printf '{"hooks":{"SessionStart":[{"hooks":[{"type":"command","command":"cat ../shared/CLAUDE.md"}]}]}}\n' > X/p3/.claude/settings.json
printf '@ws/CLAUDE.md\n\nMARKER-X-P4\n' > X/p4/CLAUDE.md
printf '@repos/test-lab/CLAUDE.md\n\nMARKER-X-P4-WS-CLONE\n' > X/p4/ws/CLAUDE.md   # nested import whose target does not exist in the clone
printf 'MARKER-X-P5\n' > X/p5/CLAUDE.md
mkdir -p ../cfgT && printf '{"projects":{"C:/work/8005-scratch/agents-md-compat/s/X/p2":{"hasTrustDialogAccepted":true}}}\n' > ../cfgT/.claude.json
# runs: cap.sh X/p1 r6-X1; cap.sh X/p2 r6-X2; cap.sh X/p3 r6-X3; cap.sh X/p4 r6-X4;
#       cap3.sh X/p5 r7-X2c --add-dir ../shared; CFG=cfgT cap2.sh X/p2 r8-X2e; CFG=cfgT cap4.sh X/p2 r9-X2f
