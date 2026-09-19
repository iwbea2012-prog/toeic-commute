# TOEIC 移動中トレーニング

移動中（電車・営業車）に使うTOEIC学習アプリ。単一の `index.html` で動きます。

- 🚃 電車モード：手ぶら自動再生／タップ学習／単語帳（432語）
- 🚗 運転モード：音声だけ（単語・シャドーイング・Part2・Part3・Part5）
- 📅 毎日の問題：`daily/YYYY-MM-DD.json`（毎朝5:00 JST に自動生成）。`daily/latest.json` は最新のコピー

問題ファイルの形式チェック: `python3 tools/validate_daily.py daily/YYYY-MM-DD.json`
