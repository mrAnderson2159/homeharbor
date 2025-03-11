# ~/.zshenv custom aliases for HomeHarbor
# aliases.zsh

# Generic
alias get="curl"
alias post="curl -X POST"

# HOMEHARBOR
alias homeharbor-venv='cd ~/homeharbor/backend; [ -d venv ] || python3 -m venv venv; source venv/bin/activate'

_homeharbor_migrate() {
    homeharbor-venv
    alembic -c alembic.ini revision --autogenerate -m "$1"
    alembic -c alembic.ini upgrade head
}
alias homeharbor-migrate=_homeharbor_migrate
alias homeharbor-psql='psql -d homeharbor --port=15432'
alias homeharbor-tree='homeharbor-venv; cd ..; tree -I venv -I __pycache__ -I node_modules -I database -I _amministrazione'

function homeharbor-start {
    local debug="${1:-false}"
    local database="${2:-homeharbor}"

    homeharbor-venv
    cd ..
    DEBUG_MODE=$debug DATABASE=$database npm start
}
