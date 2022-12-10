# PDFファイルのKidsクラス

クラス名：PDFPages

Pagesクラスで保持する情報

1. Fontオブジェクト（/Font）
1. Contentsオブジェクト（/Contents）

## ケース１
```
2 0 obj
<</Contents 19 0 R /MediaBox[ 0 0 515 728]/Parent 7 0 R /Resources<</ExtGState<</G3 3 0 R >>/Font<</F4 4 0 R /F5 5 0 R >>/ProcSet[/PDF/Text/ImageB/ImageC/ImageI]>>/StructParents 0/Type/Page>>
endobj
```

## ケース２
```
6 0 obj
<<
/Type /Page
/Parent 3 0 R
/Contents 8 0 R
/Resources 10 0 R
/Annots 11 0 R
/MediaBox [0 0 595.000000 842.000000]
>>
endobj
```
/Resources 10 0 R
```
10 0 obj
<<
/ColorSpace <<
/PCSp 5 0 R
/CSp /DeviceRGB
/CSpg /DeviceGray
>>
/ExtGState <<
/GSa 4 0 R
>>
/Pattern <<
>>
/Font <<
/F7 7 0 R
>>
/XObject <<
>>
>>
endobj
```