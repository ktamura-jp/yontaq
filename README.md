# 簡易アンケートシステム YontaQ

### 動かし方

- python3.8 が利用できる環境であること
- yontaq ディレクトリを適当な場所に置く
- パーミッションを適宜変更する
- ディレクトリ内でコマンドラインから以下を実行


    python3 app.py


ブラウザで http://localhost にアクセス
※ポートを変える場合は app.py の最終行 port=80 を別の値にする

#### uWSGI を使う場合

    pip3 install uWSGI

などにより uWSGI をインストールしたのち、ディレクトリ内で以下を実行

    sudo uwsgi --http :80 --wsgi-file app.py

※ポートを変える場合は :80 の箇所を :(別の値) にする

### 管理用コントロールパネル
http://(ホスト名orIPアドレス等)/mng

#### 表示項目

- Question ID
    - 設問番号を表す
- Status
    - 回答入力の受付・停止の状態を表す
- Setting
    - Online Agg
        - 回答が入力される都度集計を行うかどうか の設定を表す（TrueならON,　FalseならOFF）
        - Agg は aggregate の略

#### ボタン

- open/close
    - 回答入力の受付・停止 (=Status) 切り替え
- next_question
    - 次の設問に移行
- reset
    - 設問番号1を1に戻す。既存の回答は全部消去。
- online_agg_on/off
    - 回答が入力される都度集計を行うかどうかの切り替え
    - off(画面ではFalse) の場合、 Status=close にすると結果のグラフが表示される
    
