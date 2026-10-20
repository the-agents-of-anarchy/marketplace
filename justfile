# Run the plugin tests
test:
    uv run --with pytest pytest -q peers/tests

# Lab server on Hetzner: mosh terminal, SSH shell, message-socket forwarding
mod remote
