# TaskLog API  

## プロジェクトの全体像と目的
タスク・工数・ユーザーを **REST API 一つで一元管理**します。  
ファイル取込・日次集計・CSV ダウンロードまで備え、PM・DEV・ACC それぞれの業務フローを最短ステップで支援します。

## 環境構築
```bash
# 仮想環境の作成・有効化
python -m venv venv
source venv/bin/activate    # Windows: .\venv\Scripts\activate

# パッケージインストール
pip install -r requirements.txt

# マイグレーション＆管理者ユーザ作成
python manage.py migrate
python manage.py createsuperuser

# サーバ起動
python manage.py runserver
```

## Swagger での認証手順
/api/auth/jwt/create/ でアクセストークン取得
スーパーユーザーのemailとpassowrdを入力

Swagger UI の右上「Authorize」クリック
取得したアクセストークンを入力

各エンドポイントを “Try it out” 可能
