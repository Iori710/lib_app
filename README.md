# 分散型図書管理アプリ
トップページ
![図書館サービスログイン - Google Chrome 2025_04_21 11_08_10](https://github.com/user-attachments/assets/d1c5e176-f2a6-4ded-9669-ac0463210344)

## 概要
「ある会社のビル内に点在している書籍をデータで管理し、予約・貸出・返却を行う」ことを想定したアプリです

## 動作環境
- Windows 11
- Python 3.9.12
- Django 4.2.19
- PostgreSQL 17.4
- Bootstrap 5.3.0
- FullCalendar 6.1.17

## 使用方法

### 検索
トップページ上部の検索フォームから検索できます
![図書館サービスログイン - Google Chrome 2025_04_21 11_09_11](https://github.com/user-attachments/assets/eb086d09-176a-4fba-9d53-5d7b3365bc15)

「ハンドブック 記者」などのように複数のキーワードでの検索も可能です
![図書館サービスログイン - Google Chrome 2025_04_21 11_34_21](https://github.com/user-attachments/assets/807fcef6-d5a8-4a27-87b9-1a41d31a70c9)

### 予約
予約画面ではカレンダーが表示されるので、貸出したい日付をドラッグし、そのまま返却したい日付まで動かします（**当日から貸出したい場合も予約を行ってください**）
![図書館サービスログイン - Google Chrome 2025_04_21 11_09_56](https://github.com/user-attachments/assets/09544b9f-c7a3-4786-a739-4a0fba527e42)

### 貸出・返却
貸出・返却の際は貸出・返却画面にて**裏表紙2段目にあるバーコードの番号**を入力します(1枚目画像赤線部)
![IMG_3205_redline](https://github.com/user-attachments/assets/8fd79551-2e01-48be-bd24-424271408924)
![図書館サービスログイン - Google Chrome 2025_04_21 11_59_23](https://github.com/user-attachments/assets/08362b9a-c495-44fb-8f93-9e18e5979d9e)
![貸出・返却画面 - Google Chrome 2025_04_21 12_01_05](https://github.com/user-attachments/assets/2b9e377f-3d2a-4d32-97ed-ff864b5ba140)

### レビュー
返却時にレビューを残すことができます(評価のみも可)
![貸出・返却画面 - Google Chrome 2025_04_21 12_01_51](https://github.com/user-attachments/assets/beed7732-2c38-4416-9e29-d407c004cc6f)
![貸出・返却画面 - Google Chrome 2025_04_21 12_02_35](https://github.com/user-attachments/assets/76207b1d-9fdb-4db0-868a-7a37e7f1bcd1)
このレビューは書籍詳細情報画面で確認できます
![レビュー記入 - Google Chrome 2025_04_21 12_05_18](https://github.com/user-attachments/assets/2f76394b-cf94-4036-99bd-a15ce583fcd1)

### 書籍登録
書籍のISBN、保管場所、裏表紙2段目にあるバーコードの番号(日本図書コード)を入力して登録します
![書籍登録 - Google Chrome 2025_04_22 11_38_00](https://github.com/user-attachments/assets/152bbefa-cd2c-4be0-88a5-c5498a7c1d7d)
登録に成功した場合、書籍のタイトルなどが表示されます
![書籍登録 - Google Chrome 2025_04_22 11_38_12](https://github.com/user-attachments/assets/58fdccd2-4735-4ac0-8d8f-d02722306bf7)


## 詳細
- ログイン
  - ユーザーは管理者側から作成
- ナビゲーションバー
  - トップページ
    - 「図書館サービス」を押すと遷移
  - プルダウンメニュー
    - マイページ
      - 予約書籍・貸出日確認
      - 貸出書籍・返却日確認
      - ユーザー設定
        - ユーザーネーム変更
        - パスワード変更
    - 貸出・返却
    - お知らせ一覧
      - 全てのお知らせが見れる
    - 問い合わせフォーム
    - ログアウト
- トップページ
  - 書籍検索
  - (貸出日が過ぎている・返却日が近いもしくは過ぎている時)アナウンスメッセージ
  - 最新のお知らせ(最新3件)
  - お知らせ一覧
  - 問い合わせフォーム
- 検索結果
  - 書籍予約
  - 書籍詳細情報
    - 最新レビュー(最新3件)
    - レビューをもっと見る
      - その書籍の平均評価、全てのレビューが見れる
- 書籍予約画面
  - カレンダー
  - イベント作成(貸出・返却日指定)
    - 予約が入っている場合、その日付に「予約済」と表示
- 貸出・返却画面
  - レビュー(返却時のみ)
- 書籍登録画面
  - ISBN・保管場所・日本図書コード(裏表紙2段目にあるバーコードの番号)を入力
- 管理者画面
  - ユーザー・問い合わせの管理、お知らせの更新

## 参考URL
[【Django】FullCalendarでスケジュールのDB登録・表示【実践向け】](https://chigusa-web.com/blog/django-fullcalendar/)<br>
[FullCalendarの使い方](https://qiita.com/imp555sti/items/ee9809768f6dc9439ab5)<br>
[FullCalendar v6のカスタマイズ：日本語で「日」を消す・多言語対応、デザインの調整方法](https://bloosh.jp/tips/5409/)<br>
[【Django】サイト内検索機能を組み込んで複数のキーワード入力に対応させる](https://zerofromlight.com/blogs/detail/59/)

## システム構成図・設計図など
### システム構成図
![](./svg/システム構成図.drawio.svg)
以下の設計図は実装前に作られたものであり、一部設計図とは異なる機能が実装されている
### ユースケース図
![](./svg/ユースケース図.drawio.svg)
### 画面遷移図
![](./svg/画面遷移図.drawio.svg)
### ER図
![](./svg/ER図.drawio.svg)
