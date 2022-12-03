# PDFファイルのPagesクラス

クラス名：PDFPages

Pagesクラスで保持する情報

1. ページ数（/Count）
1. Kidsオブジェクト

## ケース１
```
7 0 obj
<</Count 1/Kids[ 2 0 R ]/Type/Pages>>
endobj
```

## ケース２
```
3 0 obj
<<
/Type /Pages
/Kids 
[
6 0 R
]
/Count 1
/ProcSet [/PDF /Text /ImageB /ImageC]
>>
endobj
```