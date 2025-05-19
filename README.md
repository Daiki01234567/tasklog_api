# TaskLog API  

## プロジェクトの全体像と目的
タスク・工数・ユーザーをREST API 一つで一元管理し、Excel 依存の現場を安全に Web 化することを目的としています。  
ファイル取込・日次集計・CSV ダウンロードまで備え、PM・DEV・ACC それぞれの業務フローを最短ステップで支援します。

> **Swagger アクセス:** `http://localhost:8000/api/schema/swagger-ui/`
curl -H "" http://127.0.0.1:8000/api/projects/

### インストール手順 (追記)

```bash
# 依存追加
pip install -r requirements.txt

# Swagger 導入済みなので設定不要、起動後に /swagger/ へアクセス
python manage.py migrate
python manage.py runserver
