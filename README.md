# 飯野家の夕食献立アプリ

GitHub Pagesで無料公開するための静的Webアプリです。ビルド不要で、`index.html` を含むこのフォルダ一式をGitHubリポジトリに置けば動きます。

毎週土曜9:00(JST)にGitHub Actionsが `scripts/generate_week.py` を実行し、前週の `data/meal-plan.json` を分析して翌週分の `data.js` と `data/meal-plan.json` を更新します。

バズレシピ由来の主菜を中心に、夕食向けの汁物・野菜料理・買い物リストを表示します。

## 無料公開の手順

1. GitHubで新しいPublicリポジトリを作成する。
2. このフォルダ内のファイルをすべてリポジトリ直下にアップロードする。
3. GitHubの `Settings` → `Pages` を開く。
4. `Build and deployment` のSourceを `Deploy from a branch` にする。
5. Branchを `main`、Folderを `/root` にして保存する。
6. 表示された `https://ユーザー名.github.io/リポジトリ名/` をiPhoneで開く。
7. Safariの共有ボタンから「ホーム画面に追加」を選ぶ。

## 週次更新

`.github/workflows/weekly-meal-plan.yml` により、GitHub上で毎週土曜9:00(JST)に献立が更新されます。手動で試す場合はGitHubの `Actions` → `Weekly meal plan` → `Run workflow` を押してください。

買い物リストのチェック状態はiPhone側のブラウザに保存されます。週が変わると新しいチェック状態になります。

## 注意

GitHub Freeで完全無料にする場合、GitHub Pagesの公開元リポジトリはPublicにするのが前提です。献立内容を公開したくない場合は、Cloudflare Pagesなど別の無料ホスティングを検討してください。
