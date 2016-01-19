# 說明

這是設計給台科人專用的短網址服務，可和 [Short-Url-Extension](https://github.com/linroex/Short-Url-Extension) 專案搭配使用。

# 待辦

- 自訂短網址
- 短網址分析功能(depend Google Analytics)
- 密碼
- 介面優化
- Log 分析
- 如果發生特殊事件會email通知（搭配log分析、logstash）
- 程式碼重構
- 測試&Travis CI
- 額度控制（秒）
- 重新設計key產生的演算法，避開特定難以辨識字元（例如q、o、0、g等等）
- 檢查網址是否存在？ 可能有些問題需要處理
- Server 不該在每日限制內
- 延遲時間計算
- 修正演算法：使用序號去產生key的問題