# PDFファイルのFontクラス

クラス名：PDFFont

Fontクラスで保持する情報

1. CMapオブジェクト（/ToUnicode）
  * CMap1：beginbfchar 〜 endbfrange
  * CMapRange：beginbfrange 〜 endbfrange


## ケース１
```
4 0 obj
<</BaseFont/AAAAAA+MS-PGothic/DescendantFonts[ 11 0 R ]/Encoding/Identity-H/Subtype/Type0/ToUnicode 12 0 R /Type/Font>>
endobj
5 0 obj
<</BaseFont/BAAAAA+ArialMT/DescendantFonts[ 15 0 R ]/Encoding/Identity-H/Subtype/Type0/ToUnicode 16 0 R /Type/Font>>
endobj
```

```
/CIDInit /ProcSet findresource begin
12 dict begin
begincmap
/CIDSystemInfo
<<  /Registry (Adobe)
/Ordering (UCS)
/Supplement 0
>> def
/CMapName /Adobe-Identity-UCS def
/CMapType 2 def
1 begincodespacerange
<0000> <FFFF>
endcodespacerange
7 beginbfchar
<473B> <30AD>
<4743> <30B5>
<4765> <30D7>
<476F> <30E1>
<4773> <30E5>
<4779> <30EB>
<4781> <30F3>
endbfchar
1 beginbfrange
<4756> <4757> <30C8>
endbfrange
endcmap
CMapName currentdict /CMap defineresource pop
end
end
```

```
/CIDInit /ProcSet findresource begin
12 dict begin
begincmap
/CIDSystemInfo
<<  /Registry (Adobe)
/Ordering (UCS)
/Supplement 0
>> def
/CMapName /Adobe-Identity-UCS def
/CMapType 2 def
1 begincodespacerange
<0000> <FFFF>
endcodespacerange
4 beginbfchar
<0003> <0020>
<0027> <0044>
<0029> <0046>
<0033> <0050>
endbfchar
endcmap
CMapName currentdict /CMap defineresource pop
end
end
```

## ケース２
```
7 0 obj
<< /Type /Font
/Subtype /Type0
/BaseFont /IPAPGothic
/Encoding /Identity-H
/DescendantFonts [14 0 R]
/ToUnicode 15 0 R>>
endobj
```

```
15 0 obj
<< /Length 448 >>
stream
/CIDInit /ProcSet findresource begin
12 dict begin
begincmap
/CIDSystemInfo << /Registry (Adobe) /Ordering (UCS) /Supplement 0 >> def
/CMapName /Adobe-Identity-UCS def
/CMapType 2 def
1 begincodespacerange
<0000> <FFFF>
endcodespacerange
2 beginbfrange
<0000> <0000> <0000>
<0001> <000C> [<30B5> <30F3> <30D7> <30EB> <0050> <0044> <0046> <30C9> <30AD> <30E5> <30E1> <30C8> ]
endbfrange
endcmap
CMapName currentdict /CMap defineresource pop
end
end

endstream
endobj
```