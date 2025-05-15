# TaskLog API  

## プロジェクトの全体像と目的 🚀
タスク・工数・ユーザーを **REST API 一つで一元管理** し、Excel 依存の現場を安全に Web 化することを目的としています。  
ファイル取込・日次集計・CSV ダウンロードまで備え、PM・DEV・ACC それぞれの業務フローを最短ステップで支援します。

```bash
# 依存追加
pip install -r requirements.txt          # drf-yasg を含む

# Swagger 導入済みなので設定不要、起動後に /swagger/ へアクセス
python manage.py migrate
python manage.py runserver
