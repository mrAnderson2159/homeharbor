# ~/.zshenv custom aliases for HomeHarbor
# aliases.zsh

# Generic
alias get="curl"
alias post="curl -X POST"

# HOMEHARBOR
alias homeharbor-venv='cd ~/homeharbor/backend; [ -d venv ] || python3 -m venv venv; source venv/bin/activate;'
alias homeharbor-psql='psql -d homeharbor --port=15432'
alias homeharbor-tree='homeharbor-venv; cd ..; tree -I venv -I __pycache__ -I node_modules -I database -I _amministrazione'

alias homeharbor-migrate='function _homeharbor_migrate() {
  if [ -z "$1" ]; then
    echo "\033[1;31m❌ Errore:\033[0m specifica lo schema (es. paperless)";
    return 1;
  fi

  schema=$1
  shift

  if [ -z "$1" ]; then
    echo "\033[1;31m❌ Errore:\033[0m specifica un messaggio per la migrazione";
    return 1;
  fi

  homeharbor-venv

  echo "\033[1;34m📦 Creazione revisione per schema:\033[0m $schema"

  if ALEMBIC_SCHEMA=$schema alembic -c alembic.ini revision --autogenerate -m "$@"; then
    latest=$(ls -t alembic/versions | head -n1)

    if grep -q "pass" "alembic/versions/$latest"; then
      echo "\033[1;33m⚠️  Migrazione vuota rilevata, verrà eliminata:\033[0m $latest"
      rm "alembic/versions/$latest"
    else
      echo "\033[1;32m✅ Migrazione creata correttamente.\033[0m"
      ALEMBIC_SCHEMA=$schema alembic -c alembic.ini upgrade head
    fi
  else
    echo "\033[1;31m❌ Errore durante la creazione della migrazione, upgrade annullato.\033[0m"
    return 1
  fi
}; _homeharbor_migrate'

alias homeharbor-stamp='function _homeharbor_stamp() {
  if [ -z "$1" ]; then
    echo "\033[1;31m❌ Errore:\033[0m specifica lo schema da sincronizzare (es. paperless)";
    return 1;
  fi

  schema=$1
  homeharbor-venv

  echo "\033[1;34m📌 Stampando head per schema:\033[0m $schema"
  ALEMBIC_SCHEMA=$schema alembic -c alembic.ini stamp head
}; _homeharbor_stamp'



function homeharbor-start {
    local debug="${1:-false}"
    local database="${2:-homeharbor}"

    homeharbor-venv
    cd ..
    DEBUG_MODE=$debug DATABASE=$database npm start
}