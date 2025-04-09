# 特別研究
BeagleBone Greenの計測制御ボードの開発  
基本的な接続方法は特別研究論文に記載されています

# 使用機器・モジュール
  - BeagleBone Green
    - 最新イメージをインストール
  - fiap
    - https://github.com/iwax2/raspi-fiap を参考に
   
# BBGの初期設定
  - ユーザの作成
  - ユーザをwheelユーザグループに追加
  - ファイアウォールの設定
  - SSHの設定
  - サーバーの時刻同期
  - タイムゾーンの設定

# 接続
  - I2C
![Image](https://github.com/user-attachments/assets/8573fbc2-2e66-4a90-9edd-a841507d7f1b)
    - I2C1 P9.17 & P9.18 または P9.24 & P9.26
    - I2C2 P9.19 & P9.20
  - UART
![Image](https://github.com/user-attachments/assets/9c072b58-f727-470a-a623-2a33974d212a)
    - UART1 P9.24 & P9.26
    - UART2 P9.21 & P9.22
    - TXD, RXDのみ記載・3~5略
参照：https://wiki.seeedstudio.com/BeagleBone_Green/

# ピンの設定
I2C1, UARTでは初期状態では認識されない場合があるためピン設定を行う
```
$ config-pin P9.17 i2c
$ config-pin P9.18 i2c
$ config-pin P9.24 uart
$ config-pin P9.17 uart
```

