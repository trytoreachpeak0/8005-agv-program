#!/usr/bin/env bash
# Review-round scenarios (run after setup.sh; same s/ tree). Each block lists the runs that use it.
set -e
cd /c/work/8005-scratch/agents-md-compat/s
mk(){ mkdir -p "$(dirname "$1")"; printf '%s\n' "${@:2}" > "$1"; }
base=C:/work/8005-scratch/agents-md-compat
cfg(){ mkdir -p "../$1" && printf '%s\n' "$2" > "../$1/.claude.json"; }   # throwaway CLAUDE_CONFIG_DIR with a .claude.json

# Q: workspace root imports a repo clone below it; session started in the root or in a subdirectory (plain directory, no git)
mk Q/CLAUDE.md            '@repos/r/CLAUDE.md' '' 'MARKER-Q-ROOT'
mk Q/repos/r/CLAUDE.md    'MARKER-Q-REPO'
mkdir -p Q/sub
cfg cfgQ0         '{}'
cfg cfgQsub       "{\"projects\":{\"$base/s/Q/sub\":{\"hasClaudeMdExternalIncludesApproved\":true,\"hasClaudeMdExternalIncludesWarningShown\":true}}}"
cfg cfgQroot      "{\"projects\":{\"$base/s/Q\":{\"hasClaudeMdExternalIncludesApproved\":true,\"hasClaudeMdExternalIncludesWarningShown\":true}}}"
# runs: CFG=cfgQ0 run.sh Q q-Q -; CFG=cfgQ0 run.sh Q/sub q-Qsub -; CFG=cfgQsub run.sh Q/sub q-QsubOk -; CFG=cfgQroot run.sh Q/sub q-QsubRootOk -

# Qg: same layout inside a git repository (the v1 workspace is one)
mk Qg/CLAUDE.md           '@repos/r/CLAUDE.md' '' 'MARKER-QG-ROOT'
mk Qg/repos/r/CLAUDE.md   'MARKER-QG-REPO'
mkdir -p Qg/sub && printf 'x\n' > Qg/sub/keep.txt
( cd Qg && git init -q && git add -A && git -c user.name=t -c user.email=t@t commit -qm init )
cfg cfgQg0        '{}'
cfg cfgQgroot     "{\"projects\":{\"$base/s/Qg\":{\"hasClaudeMdExternalIncludesApproved\":true,\"hasClaudeMdExternalIncludesWarningShown\":true}}}"
# runs: CFG=cfgQg0 run.sh Qg/sub q-Qgsub -; CFG=cfgQgroot run.sh Qg/sub q-QgsubRootOk -

# N4 / N5: identical LF files committed, cloned with core.autocrlf=true; N5 pins only AGENTS.md to eol=lf
for n in N4 N5; do
  mkdir -p ${n}src && ( cd ${n}src && git init -q && printf '# N\nMARKER-%s-SAME\n' $n > CLAUDE.md && cp CLAUDE.md AGENTS.md \
    && { [ $n = N5 ] && printf 'AGENTS.md text eol=lf\n' > .gitattributes || true; } \
    && git -c core.autocrlf=false add -A && git -c user.name=t -c user.email=t@t commit -qm init )
  git -c core.autocrlf=true clone -q ${n}src $n
done
# runs: CFG=cfgQ0 run.sh N4 q-N4 - --settings ../../both.settings.json; same for N5 (q-N5)

# X4c / X4d: a nested import resolves relative to the importing file, not the session's working directory
mk X/p4c/CLAUDE.md                     '@ws/CLAUDE.md' '' 'MARKER-X4C'
mk X/p4c/ws/CLAUDE.md                  '@repos/test-lab/CLAUDE.md' '' 'MARKER-X4C-WS'
mk X/p4c/repos/test-lab/CLAUDE.md      'MARKER-X4C-CWD-RELATIVE-TARGET'     # exists only relative to the working directory
mk X/p4d/CLAUDE.md                     '@ws/CLAUDE.md' '' 'MARKER-X4D'
mk X/p4d/ws/CLAUDE.md                  '@repos/test-lab/CLAUDE.md' '' 'MARKER-X4D-WS'
mk X/p4d/ws/repos/test-lab/CLAUDE.md   'MARKER-X4D-FILE-RELATIVE-TARGET'    # exists relative to ws/CLAUDE.md
# runs: CFG=cfgQ0 run.sh X/p4c q-X4c -; CFG=cfgQ0 run.sh X/p4d q-X4d -

# W / R: does a CLAUDE.md in another directory load when Claude reads a file there?
mk W/CLAUDE.md            'MARKER-W-ROOT'
mk W/sub/CLAUDE.md        'MARKER-W-SUB'
printf 'x\n' > W/sub/f.txt
mk R/CLAUDE.md            'MARKER-R-REPO'
printf 'x\n' > R/f.txt
mkdir -p Wa/.claude && mk Wa/CLAUDE.md 'MARKER-WA-ROOT'
printf '{"permissions":{"additionalDirectories":["%s/s/R"]}}\n' "$base" > Wa/.claude/settings.json   # like v2's additionalDirectories
cfg cfgW          "{\"projects\":{\"$base/s/W\":{\"hasTrustDialogAccepted\":true},\"$base/s/Wa\":{\"hasTrustDialogAccepted\":true}}}"
# runs (each prompt makes the fake API answer with one Read of the given file, then inspects the follow-up request):
#   CFG=cfgW run.sh W q-z1 $base/s/W/sub/f.txt                           control: subdirectory under the working directory
#   CFG=cfgW run.sh W q-z2 $base/s/R/f.txt --add-dir $base/s/R           --add-dir, no env var
#   CFG=cfgW ADDENV=1 run.sh W q-z3 $base/s/R/f.txt --add-dir $base/s/R  --add-dir with CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1
#   CFG=cfgW run.sh Wa q-z4 $base/s/R/f.txt                              additional directory from project settings
#   CFG=cfgW ADDENV=1 run.sh Wa q-z5 $base/s/R/f.txt                     same, with the env var
echo setup2-ok
