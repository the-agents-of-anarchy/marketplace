#!/bin/bash
set -u

readonly TAG_PATTERN='^\[(hazard|ask|answer|notice)\]'
readonly STAMP_MARKER='sent 20'
readonly STAMP_FORMAT='+%Y-%m-%dT%H:%M%z'
readonly STAMPED_INPUT_FILTER='
  def stamped_lines($lines; $stamp):
    if ($lines[1] // "" | startswith("reply:"))
    then $lines[0:1] + [$lines[1] + " · sent " + $stamp] + $lines[2:]
    else $lines[0:1] + ["sent " + $stamp] + $lines[1:]
    end;
  .tool_input as $input
  | $input.message as $message
  | select($message | type == "string")
  | ($message | split("\n")) as $lines
  | select(($lines[0] // "") | test($tag_pattern))
  | select($message | contains($stamp_marker) | not)
  | {hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "allow",
      updatedInput: ($input | .message = (stamped_lines($lines; $stamp) | join("\n")))
    }}
'

society_root() {
  if [ -n "${AGENTS_OF_ANARCHY_ROOT:-}" ]; then echo "$AGENTS_OF_ANARCHY_ROOT"
  elif [ -n "${XDG_DATA_HOME:-}" ]; then echo "$XDG_DATA_HOME/agents-of-anarchy"
  elif [ -n "${HOME:-}" ]; then echo "$HOME/.local/share/agents-of-anarchy"
  fi
}

main() {
  local root stamp
  root=$(society_root)
  [ -n "$root" ] && [ -d "$root" ] || exit 0
  command -v jq >/dev/null 2>&1 || exit 0
  stamp=$(date "$STAMP_FORMAT" 2>/dev/null)
  [ -n "$stamp" ] || exit 0
  jq -c --arg stamp "$stamp" --arg tag_pattern "$TAG_PATTERN" --arg stamp_marker "$STAMP_MARKER" "$STAMPED_INPUT_FILTER" 2>/dev/null
  exit 0
}

main
