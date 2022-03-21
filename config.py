class Config:
    notion_token = 'hogehoge'
    notion_endpoint = 'https://api.notion.com/v1'
    database_id = 'hogehoge'
    headers = {
        'Authorization': f'Bearer {notion_token}',
        'Content-Type': 'application/json',
        'Notion-Version': '2021-08-16'
    }
