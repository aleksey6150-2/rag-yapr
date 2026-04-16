#!/bin/bash
# Установка cron-задачи для ежедневного обновления индекса в 06:00.
#
# Использование:
#   chmod +x task6/setup_cron.sh
#   ./task6/setup_cron.sh
#
# Для удаления задачи:
#   crontab -l | grep -v "update_index.py" | crontab -

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VENV_PYTHON="$PROJECT_DIR/.venv/bin/python"
UPDATE_SCRIPT="$SCRIPT_DIR/update_index.py"

# Проверки
if [ ! -f "$VENV_PYTHON" ]; then
    echo "Error: Python venv not found at $VENV_PYTHON"
    echo "Run: python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

if [ ! -f "$UPDATE_SCRIPT" ]; then
    echo "Error: update_index.py not found at $UPDATE_SCRIPT"
    exit 1
fi

# Cron-строка: каждый день в 06:00
CRON_LINE="0 6 * * * cd $PROJECT_DIR && $VENV_PYTHON $UPDATE_SCRIPT >> $SCRIPT_DIR/logs/cron.log 2>&1"

# Добавляем, не дублируя
(crontab -l 2>/dev/null | grep -v "update_index.py"; echo "$CRON_LINE") | crontab -

echo "Cron job installed:"
echo "  $CRON_LINE"
echo ""
echo "Verify with: crontab -l"
echo "Logs will be at: $SCRIPT_DIR/logs/cron.log"
