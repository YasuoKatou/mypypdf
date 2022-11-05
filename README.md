# mypypdf

## 機能

PDFファイルに保存されている文字列を抽出する（工事中）

状況：フォントの位置が判明したので、フォントのオブジェクトから「ToUnicode」を取得し、CMAPを取得する処理を実装中

補足：暗号化されたPDFは、対象外とする。

## pdf_read02.py

指定したPDFオブジェクトをコンソールに出力する（工事中）

* 「/Filter/FlateDecode」に対応

起動引数

* --file-path {string}   ファイルのパス





## ツール

### ■ hexdump

指定のファイルをHEXまたは文字列でコンソールに出力する

起動引数

* --file-path {string}   ファイルのパス
* --limit {number}       ダンプのバイト数
* --offset {number}      ファイルのオフセット（バイト数）
* --plain-text {string}  ダンプを文字列で出力するときの文字コード（utf-8）
