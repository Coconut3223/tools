# Tools 

**modify according to the requirements**


## alignment

Thanks [Kamil Slowikowski](https://gist.github.com/slowkow/06c6dba9180d013dfd82bec217d22eb5)


**Example**

``` py
'''
踏入2017年維港兩岸有三十三萬人欣賞煙花慶祝各個倒數熱門地點亦人頭湧湧迎接新〇〇〇〇〇〇〇〇〇一〇〇〇〇〇〇〇年璀璨煙花告別2016人人用手機留住最美一刻期望新一年同樣精彩
〇〇2017年維港兩岸有三十三萬人欣賞煙花慶祝各個度數據本地點都人頭湧湧迎接新嘅兩電一齊睇下倒數一刻外面有幾咁熱鬧最殘煙花告別2016〇人用手機留住最靚一刻期望新一年同樣精彩
'''
```

**Changes:**

- To align sentences, Chinese characters which take up 2-bytes use `gap_str='〇'`, English characters use `gap_str='O'`

## demo_diff

Thanks [zyzcss](https://github.com/zyzcss/python-diff/tree/main)

**Examples:**

```html
當中兩條主線，我<span style='color:red;font-weight:500;text-decoration:line-through;'>哋</span><span style='color:green;font-weight:500;'>們</span><span style='font-weight:700;background-color:#FFF3CC;'>要更好發揮香港一國兩制下的背景，背靠祖國</span><span style='color:green;font-weight:500;'>、</span>聯通世界<span style='color:red;font-weight:500;text-decoration:line-through;'>嘅</span><span style='color:green;font-weight:500;'>的</span>
```

展示结果：

![](./pics/demo_diff_1.png)

當中兩條主線，我<span style='color:red;font-weight:500;text-decoration:line-through;'>哋</span><span style='color:green;font-weight:500;'>們</span><span style='font-weight:700;background-color:#FFF3CC;'>要更好發揮香港一國兩制下的背景，背靠祖國</span><span style='color:green;font-weight:500;'>、</span>聯通世界<span style='color:red;font-weight:500;text-decoration:line-through;'>嘅</span><span style='color:green;font-weight:500;'>的</span>

**Changes:**

- `demo_diff.show_md(results:List[List[str]], md_path:str, keywords:List[str])` 
  - `results`: to process a list of sentences
  - `md_path`: results will be 
  - `keywords` are parsed to emphasize keywords with the specified background-color
- `demo_diff.run(..., unit='word', lang='zh')`
  - `unit` & `lang` to specify the tokenizer to tokenize the sentence


