#!/bin/bash
# SessionStart: print the session-start line. Argument: join | resume | compact.
# Silent unless the registry root exists. Never creates it. Never fails the session.
set -u
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(dirname "$SCRIPT_DIR")}"

# Off switch: PEERS_HOOKS=off or PEERS_JOIN_HOOK=off prints nothing.
[ "${PEERS_HOOKS:-on}" = "off" ] && exit 0
[ "${PEERS_JOIN_HOOK:-on}" = "off" ] && exit 0

# Gate: no registry directory, no peer protocol.
ROOT="${AGENTS_OF_ANARCHY_ROOT:-}"
if [ -z "$ROOT" ]; then
  if [ -n "${XDG_DATA_HOME:-}" ]; then ROOT="$XDG_DATA_HOME/agents-of-anarchy"
  elif [ -n "${HOME:-}" ]; then ROOT="$HOME/.local/share/agents-of-anarchy"
  fi
fi
[ -n "$ROOT" ] && [ -d "$ROOT" ] || exit 0

case "${1:-}" in
  join|resume|compact) ;;
  *) exit 0 ;;
esac

TEMPLATE="$PLUGIN_ROOT/hooks/templates/peer-$1.txt"
[ -f "$TEMPLATE" ] && [ -r "$TEMPLATE" ] || exit 0

ESCAPED_ROOT="$(printf '%s' "$ROOT" | sed -e 's/[&|\\]/\\&/g')"
sed -e "s|<root>|$ESCAPED_ROOT|g" "$TEMPLATE" 2>/dev/null
exit 0
