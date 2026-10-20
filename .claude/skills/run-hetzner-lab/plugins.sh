# Plugins for the lab sibling session: the owner's public marketplaces, then the plugins.
# Run as the user lab. Used by the server setup at creation, and by `just remote::plugins`.
C="$HOME/.local/bin/claude"
"$C" plugin marketplace add ryzhakar/claude-skills
"$C" plugin marketplace add ryzhakar/memento
"$C" plugin marketplace add the-agents-of-anarchy/marketplace
"$C" plugin install manifesto@my-claude-skills
"$C" plugin install agent-conduct@my-claude-skills
"$C" plugin install memento@memento
"$C" plugin install peers@agents-of-anarchy
"$C" plugin list
