from langchain_community.chat_models import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from dotenv import load_dotenv


# 連接 SQLite 資料庫# -- coding: utf-8 --

import sys
import io
import os

# 確保編碼正確
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
os.environ["PYTHONIOENCODING"] = "utf-8"

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("❌ 環境變數 OPENAI_API_KEY 沒有載入！請確認 .env 檔案是否存在，且格式正確")

os.environ["OPENAI_API_KEY"] = api_key

from langchain_community.chat_models import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain

# 初始化資料庫連線
db = SQLDatabase.from_uri("sqlite:///test.db")

# 使用 GPT-4（或 gpt-3.5-turbo）
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

# 組合成查詢鏈
db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)

# 輸入問題
query = input("🧠 請輸入你的查詢問題：")

# 使用 invoke 取代 .run()
response = db_chain.invoke({"query": query})

# 顯示結果
print("\n🔍 查詢結果：")
print(response)

db = SQLDatabase.from_uri("sqlite:///test.db")

# 初始化 GPT 模型（gpt-4 或 gpt-3.5-turbo）
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

# 建立查詢鏈
db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)

# 使用者輸入自然語言問題
query = input("🧠 請輸入你的查詢問題：")

# 執行查詢
response = db_chain.run(query)

# 顯示結果
print("\n🔍 查詢結果：")
print(response)
