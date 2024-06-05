# JSON Hook Transmitter

JSON Hook Transmitter 是一個用於接收、轉換並轉發 webhook payload 的中介服務，旨在解決原服務與目的服務之間的數據格式轉換問題。

## 功能
- 接收來自原服務的 webhook 請求
- 根據自定義規則轉換 webhook payload
- 將轉換後的 payload 轉發到目的服務

## 安裝
1. clone 此倉庫：
    ```bash
    git clone https://github.com/your-username/json-hook-transmitter.git
    cd json-hook-transmitter
    ```

2. 安裝依賴：
    ```bash
    pip install -r requirements.txt
    ```

3. 配置環境變數：
    - 創建 `.env` 文件，並添加必要的配置，例如目標服務的 URL。

## 使用
1. 根據轉換規則提供 transformer，請參考 `transformer/sample.py`，示例如下：
    ```python
    import json
    import os

    def transform(raw):
        return {
            "new_field_1": "A",
            "new_field_2": "B",
            "new_field_3": "C"
        }
    ```

2. 掛載並指明 transformer 名稱，以容器運行為例：
    ```shell
    otherWebHookServer=http://localhost:5000/transformed
    sudo podman run --name json-hook-transmitter --rm -it \
      -p 5001:5000 \
      -v ${PWD}/transformer/sample.py:/app/sample.py \
      -e WEBHOOK_PROXY_TRANSFORMER=sample \
      -e WEBHOOK_PROXY_DEBUG=true \
      -e REWRITE_ENDPOINT=${otherWebHookServer} \
      docker.io/neildeng/json-hook-transmitter:latest
    ```
    說明：
    - `-v ${PWD}/transformer/sample.py:/app/sample.py`：掛載 transformer 檔案位置
    - `-e WEBHOOK_PROXY_TRANSFORMER=sample`：提供動態載入的 transformer 名稱
    - `-e REWRITE_ENDPOINT=${otherWebHookServer}`：提供轉發 webhook 的 endpoint
    - `-e WEBHOOK_PROXY_DEBUG=true`：是否為 debug 模式

3. 以下為簡易的範例：
    ```shell
    # 檢查健康狀態
    curl http://localhost:5001/health | jq

    # 獲取系統參數
    curl http://localhost:5001/info | jq

    # 發送 webhook
    curl -L -X POST http://localhost:5001/webhook -H "Content-Type: application/json" -d '{ "original_field_1": "A", "original_field_2": "B"}'

    # 預期回應
    # {"response":{"new_field_1":"A","new_field_2":"B","new_field_3":"C"},"status":"success"}
    ```

## 貢獻
歡迎貢獻！你可以提交 issue 或 pull request。

## 授權
本專案採用 MIT 許可證，詳情請參閱 [LICENSE](LICENSE) 文件。