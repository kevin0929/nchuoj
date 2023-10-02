# NCHUOJ

為配合 2021 中興大學暑期課程建立的 Online Judge。

技術方面 : 
 - 前端 : `HTML`、`CSS`、`JS`
 - 後端 : `PHP`
 - API : `Judge0`
 - Database : `MySQL`

使用者登入後，可以透過題號提交程式碼，後端會從資料庫抓取該題的測試資料，並將程式碼及測資送給 `Judge0` API 進行測試。

`Judge0` API 會將測試結果回傳給後端，後端再轉交給前端，並將測試結果顯示在畫面上。
