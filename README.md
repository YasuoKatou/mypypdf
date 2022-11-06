# mypypdf

## 機能

PDFファイルに保存されている文字列を抽出する（工事中）

状況：最も簡単な方法でPDFのテキストを抽出できた。実行結果は、「./samples/pdf_sample_01_result.txt」を参照

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
