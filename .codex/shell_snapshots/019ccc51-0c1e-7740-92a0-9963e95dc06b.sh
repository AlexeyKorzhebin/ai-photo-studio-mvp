# Snapshot file
# Unset all aliases to avoid conflicts with functions
# Functions
gawklibpath_append () 
{ 
    [ -z "$AWKLIBPATH" ] && AWKLIBPATH=`gawk 'BEGIN {print ENVIRON["AWKLIBPATH"]}'`;
    export AWKLIBPATH="$AWKLIBPATH:$*"
}
gawklibpath_default () 
{ 
    unset AWKLIBPATH;
    export AWKLIBPATH=`gawk 'BEGIN {print ENVIRON["AWKLIBPATH"]}'`
}
gawklibpath_prepend () 
{ 
    [ -z "$AWKLIBPATH" ] && AWKLIBPATH=`gawk 'BEGIN {print ENVIRON["AWKLIBPATH"]}'`;
    export AWKLIBPATH="$*:$AWKLIBPATH"
}
gawkpath_append () 
{ 
    [ -z "$AWKPATH" ] && AWKPATH=`gawk 'BEGIN {print ENVIRON["AWKPATH"]}'`;
    export AWKPATH="$AWKPATH:$*"
}
gawkpath_default () 
{ 
    unset AWKPATH;
    export AWKPATH=`gawk 'BEGIN {print ENVIRON["AWKPATH"]}'`
}
gawkpath_prepend () 
{ 
    [ -z "$AWKPATH" ] && AWKPATH=`gawk 'BEGIN {print ENVIRON["AWKPATH"]}'`;
    export AWKPATH="$*:$AWKPATH"
}

# setopts 3
set -o braceexpand
set -o hashall
set -o interactive-comments

# aliases 0

# exports 39
declare -x BRIDGE_NO_RESTORE="true"
declare -x BRIDGE_PROFILE="/tmp/pinchtab-profile"
declare -x BROWSER="pinchtab"
declare -x CAILA_API_KEY="1000128412.204871.rBMB6ZSHWOlB53a7nbDt2e0rdcuDUdSEX5vVWVIL"
declare -x CODEX_HOME="/home/openclaw/projects/ai-photo-studio-mvp/.codex"
declare -x CODEX_MANAGED_BY_NPM="1"
declare -x DBUS_SESSION_BUS_ADDRESS="unix:path=/run/user/1001/bus"
declare -x HOME="/home/openclaw"
declare -x HOMEBREW_CELLAR="/home/linuxbrew/.linuxbrew/Cellar"
declare -x HOMEBREW_PREFIX="/home/linuxbrew/.linuxbrew"
declare -x HOMEBREW_REPOSITORY="/home/linuxbrew/.linuxbrew/Homebrew"
declare -x INFOPATH="/home/linuxbrew/.linuxbrew/share/info:"
declare -x INVOCATION_ID="0ac80b0a71084bc1b2e46c005d19f867"
declare -x JOURNAL_STREAM="8:3775233"
declare -x LANG="C.UTF-8"
declare -x LOGNAME="openclaw"
declare -x MANAGERPID="930"
declare -x NODE_NO_WARNINGS="1"
declare -x OPENCLAW_GATEWAY_PORT="18789"
declare -x OPENCLAW_GATEWAY_TOKEN="8c9e351965a8fab0babf85b8f74077044b67fd9f23ff134b"
declare -x OPENCLAW_NODE_OPTIONS_READY="1"
declare -x OPENCLAW_PATH_BOOTSTRAPPED="1"
declare -x OPENCLAW_SERVICE_KIND="gateway"
declare -x OPENCLAW_SERVICE_MARKER="openclaw"
declare -x OPENCLAW_SERVICE_VERSION="2026.3.1"
declare -x OPENCLAW_SHELL="exec"
declare -x OPENCLAW_SYSTEMD_UNIT="openclaw-gateway.service"
declare -x OPENROUTER_API_KEY="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"
declare -x PATH="/home/linuxbrew/.linuxbrew/bin:/home/linuxbrew/.linuxbrew/sbin:/home/openclaw/.local/bin:/home/openclaw/bin:/home/openclaw/projects/ai-photo-studio-mvp/.codex/tmp/arg0/codex-arg0TSzdDM:/home/openclaw/.npm-global/lib/node_modules/@openai/codex/node_modules/@openai/codex-linux-x64/vendor/x86_64-unknown-linux-musl/path:/home/linuxbrew/.linuxbrew/bin:/home/linuxbrew/.linuxbrew/sbin:/usr/local/bin:/home/openclaw/.local/bin:/usr/bin:/bin:/home/openclaw/.npm-global/bin:/home/openclaw/bin:/home/openclaw/.volta/bin:/home/openclaw/.asdf/shims:/home/openclaw/.bun/bin:/home/openclaw/.nvm/current/bin:/home/openclaw/.fnm/current/bin:/home/openclaw/.local/share/pnpm:/snap/bin"
declare -x QT_ACCESSIBILITY="1"
declare -x SHELL="/bin/bash"
declare -x SHLVL="1"
declare -x SYSTEMD_EXEC_PID="663052"
declare -x TERM="xterm-256color"
declare -x TMPDIR="/tmp"
declare -x USER="openclaw"
declare -x VIPSHOME="/target"
declare -x XDG_DATA_DIRS="/usr/local/share/:/usr/share/:/var/lib/snapd/desktop"
declare -x XDG_RUNTIME_DIR="/run/user/1001"
