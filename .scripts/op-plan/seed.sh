#!/usr/bin/env bash
#
# Seed the Kainos-Logos OpenProject project (identifier: kainos-logos) from the
# repo's plan/ + action-steps/. Faithful translation, one OpenProject resource per
# planning unit:
#
#   4 Epic       — one per phase (plan/30-phases/*/README.md goals + roadmap contract)
#  22 Task       — one per action-steps/ directive (description = the directive, verbatim)
#   4 Milestone  — phase sign-offs with exit-criteria checklists
#  29 relations — parent (task→epic) + predecessor edges exactly matching the
#                 directives' "Prerequisites" (incl. the 21/22-before-20 exception)
#
# Priorities follow the plan's own emphases: step 11 (C2, "emotional center"),
# step 16 (E2 runs, "most important results"), step 20 (final acceptance) = High;
# the rest Normal.
#
# Idempotency guard: aborts if the project already contains work packages.
# To re-seed from scratch: delete the WPs (op wp delete <id>) and run again.

set -euo pipefail
cd "$(dirname "$0")/../.."          # repo root
OP=./project-management/op
HERE=.scripts/op-plan

# ── guard ─────────────────────────────────────────────────────────────────
if ! "$OP" wp list | grep -q "No work packages found"; then
    echo "ERROR: 'kainos-logos' already has work packages — refusing to double-seed." >&2
    exit 1
fi

wpid() { sed -n 's/.*#\([0-9][0-9]*\).*/\1/p' | head -1; }

# ── ensure the Milestone type (id 2) is enabled on this project ─────────────
# OP 17 does not expose a v3 API to manage a project's work package types
# (UI-only setting). On this local docker instance the setting is just the
# projects_types join table, so add the row directly if missing.
ensure_milestone_type() {
    local ev url tok ident
    ev=$(grep -E '^(OPENPROJECT_URL|OPENPROJECT_ACCESS_TOKEN|OPENPROJECT_PROJECT_ID)=' .env | head -3 | perl -ne 'if (/^(\w+)="?(.+?)"?\s*$/) { print "$1=\"$2\"\n" }')
    # shellcheck disable=SC1090
    . <(echo "$ev" | sed 's/^/export /')
    local have
    have=$(curl -s -H "Authorization: Bearer $OPENPROJECT_ACCESS_TOKEN" \
              "${OPENPROJECT_URL}/api/v3/workspaces/${OPENPROJECT_PROJECT_ID}/types")
    if echo "$have" | grep -q '/api/v3/types/2'; then
        echo "Milestone type already enabled."
        return 0
    fi
    echo "Milestone type missing → adding via projects_types table (local docker DB)…"
    docker exec openproject-db-1 psql -U postgres -d openproject \
        -c "INSERT INTO projects_types (project_id, type_id)
            SELECT p.id, 2 FROM projects p WHERE p.identifier='${OPENPROJECT_PROJECT_ID}'
            ON CONFLICT DO NOTHING;" || {
        echo "ERROR: could not add Milestone type automatically; enable it in the UI (Project → Settings → Work packages)" >&2
        exit 1
    }
}
ensure_milestone_type

# ── 1. epics (one per phase) ──────────────────────────────────────────────
echo "Creating phase epics…"
E=()
EPIC_NAMES=( "Phase 0 — Foundation" "Phase 1 — Regex" "Phase 2 — 20 Questions" "Phase 3 — Generalization" )
for i in 0 1 2 3; do
    E[$i]=$("$OP" wp create "${EPIC_NAMES[$i]}" --type Epic \
                   --description "$(cat "$HERE/epic-$i.md")" | wpid)
    echo "  #${E[$i]}  ${EPIC_NAMES[$i]}"
done

# ── 2. tasks (one per directive) ──────────────────────────────────────────
echo "Creating directive tasks…"
declare -A NUM_FILE NUM_PLAN
NUM_FILE=( [01]=01-scaffold.md [02]=02-codex-model-store.md [03]=03-codex-explain-ir.md
           [04]=04-golden-cli.md [05]=05-harness-ci.md [06]=06-regex-ir-emitter.md
           [07]=07-kernel-lexicon.md [08]=08-resolver-judge-pipeline.md
           [09]=09-seed-corpus-parity.md [10]=10-compositionality.md
           [11]=11-persistence-uncertainty.md [12]=12-llm-ab-baseline.md
           [13]=13-q20-corpus-oracle.md [14]=14-q20-hypothesis-selector.md
           [15]=15-q20-learning-dashboard.md [16]=16-q20-e2-runs.md
           [17]=17-llm-kernel.md [18]=18-numerics-topology.md
           [19]=19-distributed-codex.md [20]=20-multimodal-final.md
           [21]=21-projection-planning.md [22]=22-workspace-memory.md )
NUM_PLAN=( [01]="P0.01" [02]="P0.02–P0.03" [03]="P0.04–P0.05" [04]="P0.06–P0.07"
           [05]="P0.08–P0.10" [06]="P1.01–P1.02" [07]="P1.03–P1.04"
           [08]="P1.05–P1.07" [09]="P1.08–P1.09" [10]="P1.10–P1.11"
           [11]="P1.12–P1.13" [12]="P1.14–P1.16" [13]="P2.01–P2.02"
           [14]="P2.03–P2.06" [15]="P2.07–P2.09" [16]="P2.10–P2.15"
           [17]="P3.01–P3.02" [18]="P3.03–P3.05" [19]="P3.06–P3.08"
           [20]="P3.09–P3.11" [21]="P3.12–P3.14" [22]="P3.15–P3.17" )

phase_of() {
    case $1 in
        0[1-5]) echo 0 ;;
        06|0[7-9]|1[0-2]) echo 1 ;;
        1[3-6]) echo 2 ;;
        *) echo 3 ;;
    esac
}

declare -A T PRIO PHASEN
PHASEN=( [0]="0 (Foundation)" [1]="1 (Regex)" [2]="2 (20 Questions)" [3]="3 (Generalization)" )
mkdir -p "$HERE/tasks"
for num in 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22; do
    f="action-steps/${NUM_FILE[$num]}"
    p=$(phase_of "$num")
    # Priorities follow the plan's own emphases:
    #   11 — "C2 is the emotional center of the whole project"
    #   16 — "E2.3 and E2.5 … the two most important results for the project's thesis"
    #   20 — final consolidation + project acceptance
    case $num in 11|16|20) prio=High ;; *) prio=Normal ;; esac
    PRIO[$num]=$prio

    subject=$(sed -n '1s/^# Action Step [0-9][0-9] — //p' "$f")
    {
        printf '> **Source of truth:** `%s` (this description mirrors that file verbatim; if they drift, the file wins).\n' "$f"
        printf '> **Plan mapping:** %s · Phase: %s · Execution order is encoded as predecessor links on this ticket.\n\n' "${NUM_PLAN[$num]}" "${PHASEN[$p]}"
        cat "$f"
    } > "$HERE/tasks/$num.md"

    T[$num]=$("$OP" wp create "Step $num — $subject" --type Task --parent "${E[$p]}" \
                      --priority "$prio" --description "$(cat "$HERE/tasks/$num.md")" | wpid)
    echo "  #${T[$num]}  [$prio] Step $num — $subject"
done

# ── 3. milestones (phase sign-offs) ───────────────────────────────────────
echo "Creating sign-off milestones…"
M=()
M_NAMES=( "Phase 0 sign-off" "Phase 1 sign-off" "Phase 2 sign-off" "Phase 3 sign-off (project acceptance)" )
for i in 0 1 2 3; do
    M[$i]=$("$OP" wp create "${M_NAMES[$i]}" --type Milestone --parent "${E[$i]}" \
                    --description "$(cat "$HERE/milestone-$i.md")" | wpid)
    echo "  #${M[$i]}  ${M_NAMES[$i]}"
done

# ── 4. predecessor relations ───────────────────────────────────────────────
# Each "A B" = A must finish before B starts. Edges come from the directives'
# "Prerequisites" sections (direct prerequisites only; chains imply the rest):
#   Phase 0 chain 01→…→05;   05 (phase 0 done) → 06
#   Phase 1 chain 06→…→12;   12 (phase 1 done) → 13, → 17, → 18
#   Phase 2 chain 13→14→15→16; 16 (phase 2 done) → 19, → 21, → 22
#   20 final consolidation needs 17–19 AND 21–22 (the ordering exception)
#   milestones: the last step of each phase precedes its sign-off
LINKS=(
    "01 02" "02 03" "03 04" "04 05"
    "05 06"
    "06 07" "07 08" "08 09" "09 10" "10 11" "11 12"
    "12 13"
    "13 14" "14 15" "15 16"
    "12 17" "12 18"
    "16 19" "16 21" "16 22"
    "17 20" "18 20" "19 20" "21 20" "22 20"
)
echo "Creating predecessor relations…"
for l in "${LINKS[@]}"; do
    read -r a b <<<"$l"
    "$OP" wp link "${T[$a]}" --precedes "${T[$b]}" > /dev/null
    echo "  #${T[$a]} → #${T[$b]}"
done
"$OP" wp link "${T[05]}" --precedes "${M[0]}" > /dev/null; echo "  #${T[05]} → #${M[0]} (milestone)"
"$OP" wp link "${T[12]}" --precedes "${M[1]}" > /dev/null; echo "  #${T[12]} → #${M[1]} (milestone)"
"$OP" wp link "${T[16]}" --precedes "${M[2]}" > /dev/null; echo "  #${T[16]} → #${M[2]} (milestone)"
"$OP" wp link "${T[20]}" --precedes "${M[3]}" > /dev/null; echo "  #${T[20]} → #${M[3]} (milestone)"

# ── 5. append the ticket table to each epic's description ─────────────────
echo "Updating epic descriptions with ticket tables…"
PHASE_TICKETS=( "01 02 03 04 05" "06 07 08 09 10 11 12" "13 14 15 16" "17 18 19 20 21 22" )
for p in 0 1 2 3; do
    {
        cat "$HERE/epic-$p.md"
        echo
        echo "## Work packages (this epic)"
        echo
        echo "| Ticket | Directive | Plan actions | Priority |"
        echo "|---|---|---|---|"
        for n in ${PHASE_TICKETS[$p]}; do
            s=$(sed -n '1s/^# Action Step [0-9][0-9] — //p' "action-steps/${NUM_FILE[$n]}")
            echo "| #${T[$n]} | [$n] $s | ${NUM_PLAN[$n]} | ${PRIO[$n]} |"
        done
    } > "$HERE/epic-${p}.full.md"
    "$OP" wp update "${E[$p]}" description="$(cat "$HERE/epic-${p}.full.md")"
done

# ── 6. summary ─────────────────────────────────────────────────────────────
echo
echo "────────────────────── RESULT ──────────────────────"
"$OP" wp list
"$OP" board summary
echo "Done. Ticket IDs (for the action-steps/README ledger):"
for num in 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22; do
    echo "  step $num → #${T[$num]}"
done
echo "Epics: #${E[0]} #${E[1]} #${E[2]} #${E[3]}   Milestones: #${M[0]} #${M[1]} #${M[2]} #${M[3]}"
