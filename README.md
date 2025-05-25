# TaskLog REST API
プロジェクトのタスク・工数をREST API一元管理します。  
ユーザーはExcelまたはCSV形式のファイルをアップロードするか、画面上で直接単体入力を行うことで、プロジェクト・タスク・工数データを一括または個別に登録できます。他にも日次集計した工数をCSVでダウンロードすることも可能です。

## 機能一覧

### プロジェクト管理
- プロジェクト名、説明、作成日時の管理
- プロジェクトに関連タスクが残っている場合、プロジェクトの削除不可

### タスク管理
- タイトル、予定工数、期限日、ステータス（TODO／DOING／DONE）、email、更新日
- プロジェクト内で同一名称のタスク登録不可

### 工数管理
- タスク、email、作業時間、作業日の管理
- 同一タスクを同一日付で重複登録不可
- 日別作業時間の集計・CSVダウンロード機能

### 権限管理
- PM：全ての操作が可能
- DEV：自身のタスク・工数の登録・更新が可能
- ACC：レポートの閲覧・ダウンロードのみ可能

### セキュリティ
- JWTトークンによる認証・認可

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

## APIドキュメント・Swagger での認証手順

API仕様はSwagger UIで確認できます。
[http://localhost:8000/api/schema/swagger-ui/](http://localhost:8000/api/schema/swagger-ui/)

1. **アクセストークンの取得**
    - `POST /auth/jwt/create/` エンドポイントを開く
    - スーパーユーザーのメールアドレスとパスワードを入力しExecute
    - レスポンスの`access`をコピー

2. **Swagger UI へトークンセット**
    - 画面右上のAuthorizeボタンをクリック
    - 取得したaccessトークンを貼り付けて認証

3. **各エンドポイントの利用**
    - “Try it out” でリクエスト実行
    - パラメータを入力し、Executeで動作確認

サンプルのExcel／CSVファイルは `docs/`フォルダ内にあります。
