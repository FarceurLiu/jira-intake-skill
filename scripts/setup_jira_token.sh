#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_PATH="$SCRIPT_DIR/../config/team-config.private.json"
SAMPLE_PATH="$SCRIPT_DIR/../config/team-config.private.sample.json"
ENV_PATH="$SCRIPT_DIR/../config/.env"
DONE_MARKER="/tmp/jira_intake_setup_done"

echo ""
echo "=== Jira Intake Skill 設定 ==="
echo ""

# 先檢查 python3 是否可用，避免後續跑到一半才失敗
if ! command -v python3 >/dev/null 2>&1; then
  echo "錯誤：找不到 python3。"
  echo "scripts 直連 Jira 的設定流程需要 Python 3，但這個 repo 不會自動幫你安裝。"
  echo "請先自行安裝 Python 3，或請工程師協助安裝後，再重新執行這個設定腳本。"
  echo "如果你只需要產出 Jira 草稿，仍然可以直接使用零設定模式。"
  echo ""
  read -p "按 Enter 關閉..."
  exit 1
fi

# 若 private config 不存在，從 sample 複製
if [[ ! -f "$CONFIG_PATH" ]]; then
  if [[ -f "$SAMPLE_PATH" ]]; then
    cp "$SAMPLE_PATH" "$CONFIG_PATH"
    echo "✓ 已從範本建立 config"
  else
    echo "錯誤：找不到 config 範本，請確認 $SAMPLE_PATH 存在"
    exit 1
  fi
fi

# 詢問 baseUrl（若還是預設佔位值則必填）
current_base_url=$(python3 -c "import json; d=json.load(open('$CONFIG_PATH')); print(d.get('baseUrl',''))" 2>/dev/null)
if [[ "$current_base_url" == *"your-domain"* || -z "$current_base_url" ]]; then
  read -p "Jira 網址（例如 https://your-company.atlassian.net）: " jira_base_url
  if [[ -z "$jira_base_url" ]]; then
    echo "錯誤：Jira 網址不能為空"
    exit 1
  fi
else
  jira_base_url="$current_base_url"
  echo "使用現有 baseUrl：$jira_base_url"
fi

# 詢問 projectKey（若還是預設佔位值則必填）
current_project_key=$(python3 -c "import json; d=json.load(open('$CONFIG_PATH')); print(d.get('projectKey',''))" 2>/dev/null)
if [[ "$current_project_key" == "APP" || -z "$current_project_key" ]]; then
  read -p "Jira 專案代碼（例如 APP、PROJ）: " jira_project_key
  if [[ -z "$jira_project_key" ]]; then
    echo "錯誤：專案代碼不能為空"
    exit 1
  fi
else
  jira_project_key="$current_project_key"
  echo "使用現有 projectKey：$jira_project_key"
fi

# 開 token 產生頁
open "https://id.atlassian.com/manage-profile/security/api-tokens" 2>/dev/null

echo ""
echo "瀏覽器已開啟 Atlassian token 頁面。"
echo "請產生一個新的 API Token，複製後回來繼續。"
echo ""

# 詢問 email
read -p "Jira 登入 Email: " jira_email
if [[ -z "$jira_email" ]]; then
  echo "錯誤：Email 不能為空"
  exit 1
fi

# 詢問 token（不顯示）
read -s -p "貼上 API Token（輸入不會顯示）: " jira_token
echo ""
if [[ -z "$jira_token" ]]; then
  echo "錯誤：Token 不能為空"
  exit 1
fi

# 寫入 config/.env，避免修改使用者 shell 啟動檔
mkdir -p "$(dirname "$ENV_PATH")"
cat > "$ENV_PATH" <<EOF
JIRA_API_TOKEN=$jira_token
EOF
chmod 600 "$ENV_PATH" 2>/dev/null || true
echo "✓ 已寫入 config/.env"
export JIRA_API_TOKEN="$jira_token"

# 更新 config
python3 - <<PYEOF
import json, sys
path = "$CONFIG_PATH"
try:
    with open(path, 'r') as f:
        config = json.load(f)
    config['baseUrl'] = "$jira_base_url"
    config['projectKey'] = "$jira_project_key"
    config['email'] = "$jira_email"
    with open(path, 'w') as f:
        json.dump(config, f, indent=2)
    print("✓ 已更新 config（baseUrl / projectKey / email）")
except Exception as e:
    print(f"錯誤：無法更新 config：{e}")
    sys.exit(1)
PYEOF

if [[ $? -ne 0 ]]; then
  exit 1
fi

# 驗證連線
echo ""
echo "正在驗證 Jira 連線..."
python3 "$SCRIPT_DIR/jira_lookup_metadata.py" "$CONFIG_PATH" projects 2>&1 | head -20

if [[ $? -eq 0 ]]; then
  echo "done" > "$DONE_MARKER"
  echo ""
  echo "✓ 設定完成，可以關閉這個視窗回到 agent"
else
  echo ""
  echo "⚠ 連線驗證失敗，請確認 Jira 網址、Email 和 Token 是否正確"
fi

echo ""
read -p "按 Enter 關閉..."
