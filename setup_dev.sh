#!/bin/bash

VENV="SLACK_ENV"

# shellcheck source=./SLACK_ENV/bin/activate
. "./${VENV}/bin/activate" || (echo "Failed to activate virtual environment" && exit 1)
pip3 install -r requirements_dev.txt

# Set up the pre-push hook
PRE_PUSH_CONTENT=$(
    cat <<'EOF'
#!/bin/sh

# Your pre-push hook logic here
#!/bin/sh

echo "Running pre-push hook..."
. ./${VENV}/bin/activate
pylint --rcfile=.pylintrc ./**/*.py
pylint_err_code=$?
deactivate
exit $pylint_err_code

EOF
)

echo "${PRE_PUSH_CONTENT}" >".git/hooks/pre-push"
chmod +x ".git/hooks/pre-push"
