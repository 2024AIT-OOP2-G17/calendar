<!-- # calendar (進捗)

| 担当者   | 作業内容      | 状況     | 備考 |
| -------------- | -------------- | ----------- | -------------------------------------- |
| 籔下晃大 |カレンダーを増やす機能 |カレンダーの追加はできているが予定をカレンダーごとに分ける方法を考え中 | |
| 三宅玲央 |期限の近いものをカレンダーの下に表示|実装済み、カレンダーの登録事項に年が追加されたらそれに対応する | |
| 不破麻郁子|カレンダーのデザインと表示|実装済み | |
| 酒井翔琉 |用事を登録する |登録済みの予定を編集する機能を追加中 | |
| 野中勇飛 |登録したものをカレンダーに表示する|達成済みリスト画面を作成中 | |
| 小沢航希 |登録画面のデザイン |カレンダー作成画面のcss | | -->

# アプリ名
## オリカレ
- 自分だけの**オリ**ジナルの**カレ**ンダーを作れる

#　アプリの概要
- ToDoリストを組み合わせたカレンダー
- カレンダーの名前を設定することで**複数のカレンダーを生成**
- 予定を追加したい日付をクリックすると登録画面に遷移し、日付、タイトル、内容を登録する
- 登録された日付に予定が表示される
- 予定日が一定期間内に入ったものはカレンダー下部に表示

# 動作条件
- python3.7以降

## 使用ライブラリ
- Flask
- jinja2
- peewee
- sqlite3

# 操作方法
## アプリの立ち上げ
- app.pyを実行し、サーバーを立ち上げて、URLを開く
## 月の切り替え
- 日付の両サイドに位置する三角ボタンをクリックし、参照している月に対して、翌月・先月に移動する
## 予定の追加
- 予定を追加したいカレンダーの日付をクリックし、予定追加画面でタイトルと詳細を記入する
## 予定の編集・完了
- 変更したい予定をクリックし、内容を変え保存する
## 直近のタスクの確認
- カレンダー下にて閲覧可能
## 達成済み予定の確認
- 直近のタスク下、「達成済みリスト」をクリックすることで、閲覧可能