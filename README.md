# TaskLog REST API
プロジェクトのタスク・工数をREST API一元管理します。  
ユーザーはExcelまたはCSV形式のファイルをアップロードするか、画面上で直接単体入力を行うことで、プロジェクト・タスク・工数データを一括または個別に登録できます。登録後のデータはJSON形式でデータをレスポンスされます。他にも日次集計した工数をCSVでダウンロードすることも可能です。

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

1. **アクセストークンを取得**  
- POST `/api/auth/jwt/create/` エンドポイントを開く  
- スーパーユーザーのメールアドレスとパスワードを入力してExecuteをクリック
- レスポンスの `access` をコピー

2. **Swagger UI にトークンをセット**  
- 画面右上の **Authorize** ボタンをクリック  
- accessキーを貼り付ける

3. **各エンドポイントを “Try it out”**  
- 認証済み状態になっているので、あとは任意のAPIを開いて  
- Try it out → パラメータを入力 → Executeで動作確認できます  
