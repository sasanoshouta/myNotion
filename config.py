class Config:
    # 自身のトークンに変更
    notion_token = 'hogehoge'
    notion_endpoint = 'https://api.notion.com/v1'
    # 更新したいDB_idに変更
    database_id = 'hogehoge'
    headers = {
        'Authorization': f'Bearer {notion_token}',
        'Content-Type': 'application/json',
        'Notion-Version': '2021-08-16'
    }
