import os
import re
from openai import OpenAI
from tqdm import tqdm
import json
import pandas as pd
from langchain_community.chat_models import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_community.document_loaders import WebBaseLoader

DASHSCOPE_API_KEY = #使用OpenAI_API_KEY
BASE_URL = #使用API_KEY平台地址

class AIAgentExpert:
    def __init__(self):
        self.llm = ChatOpenAI(
            api_key=DASHSCOPE_API_KEY,
            base_url=BASE_URL,
            model="qwen-max", 
            temperature=0.3
        )

        self.judge_llm = ChatOpenAI(
            api_key=DASHSCOPE_API_KEY,
            base_url=BASE_URL,
            model="qwen2.5-32b-instruct", 
            temperature=0
        )

        self.memory = ChatMessageHistory(
            k=3, 
            memory_key="chat_history", 
            return_messages=True
        )

        Tavily_api_key = #使用Tavily_API_KEY
        self.search = TavilySearchResults(k=8, tavily_api_key=Tavily_api_key) 
        
    def define_search_strategy(self, refined_query):
        strategy_prompt = f"""
        你是一个搜索战略专家。请分析用户需求：{refined_query}

        ### 任务 1：场景识别
        判定属于：[办公效率、开发者工具、多模态创作、学术科研、垂直领域咨询] 哪一类？

        ### 任务 2：分配配额 (总和必须为 5)
        请根据场景特性，决定 [榜单排名, 深度评测, 工程部署, 真实体验] 各自需要搜几篇文章。

        ### 任务 3：定制搜索词
        为配额大于 0 的维度，分别生成一个针对性的搜索词。
        - 榜单类：加入 "top list", "best tools" 等
        - 评测类：加入 "review", "test results", "comparison" 等
        - 部署类：加入 "how to install", "setup guide" 等
        - 体验类：加入 "pros and cons", "user feedback", "pitfalls" 等

        输出格式 (JSON):
        {{
          "scenario": "场景名",
          "plans": [
              {{"dimension": "维度名", "quota": 数量, "special_query": "针对性搜索词"}}
          ]
        }}
        """
        raw_res = self.llm.invoke(strategy_prompt).content
        return self.safe_parse_json(raw_res)
    
    def safe_parse_json(self, text):
        if hasattr(text, 'content'):
            text = text.content
        text = text.replace("```json", "").replace("```", "").strip()
        try:
            return json.loads(text)
        except Exception:
            try:
                match = re.search(r'(\[.*\]|\{.*\})', text, re.DOTALL)
                if match:
                    json_str = match.group(1)
                    while json_str:
                        try:
                            return json.loads(json_str)
                        except json.JSONDecodeError:
                            last_bracket = max(json_str.rfind(']'), json_str.rfind('}'))
                            if last_bracket == -1: break
                            json_str = json_str[:last_bracket + 1]
            except Exception as e:
                print(f"❌ 解析失败: {e}")
        return [] if text.strip().startswith('[') else {}

    def execute_quota_search(self, strategy_data):
        final_results = []
        all_context_for_top5 = ""
        for plan in strategy_data.get("plans", []):
            quota = plan['quota']
            if quota <= 0: continue
            print(f"🎯 正在为维度【{plan['dimension']}】寻找 {quota} 篇文章...")
            raw_search_content = self.search.run(plan['special_query'])
            for item in raw_search_content:
                all_context_for_top5 += f"\n来源:{item.get('title')}\n内容:{item.get('content')}\n"
            refine_prompt = f"""
            请从以下搜索结果中，精准挑选出 {quota} 篇最符合“{plan['dimension']}”特征的文章。
            【搜索结果】：{raw_search_content}
            输出格式 (JSON 列表):
            [{{"title": "标题", "url": "链接", "dimension": "{plan['dimension']}"}}]
            """
            picked_res = self.llm.invoke(refine_prompt).content
            picked_list = self.safe_parse_json(picked_res)
            if isinstance(picked_list, list):
                final_results.extend(picked_list[:quota])
        return {
            "identified_scenario": strategy_data['scenario'],
            "distribution_strategy": {p['dimension']: p['quota'] for p in strategy_data['plans']},
            "selected_results": final_results,
            "full_context": all_context_for_top5
        }
    
    def run(self, user_input):
        print(f"🌟 接收到需求: {user_input}")
        print("🧠 正在分析场景并动态分配信源权重...")
        strategy_data = self.define_search_strategy(user_input)
        if not strategy_data or "plans" not in strategy_data:
            return "❌ 战略规划失败。"
        scenario = strategy_data.get('scenario', '通用')
        print(f"🚀 已识别场景：【{scenario}】")
        print("📡 开始执行定向配额检索...")
        raw_data = self.execute_quota_search(strategy_data)
        if not raw_data.get("selected_results"):
            return f"🔍 在【{scenario}】场景下未能检索到相关内容。"
        print("✍️ 正在整理最终推荐报告...")
        reference_report = self.render_report(raw_data)
        print("💡 正在精炼最强推荐...")
        top_5_summary = self.extract_top_recommendations(
            raw_data.get('full_context', ''), 
            user_input
        )
        final_output = [
            "## 🏆 专家精选：Top 5 核心推荐",
            top_5_summary,
            "\n" + "-"*40,
            reference_report
        ]
        return "\n".join(final_output)
    
    def extract_top_recommendations(self, full_context, user_query):
        trimmed_context = full_context[:8000] 
        prompt = f"""
        你是一个 AI 行业分析师。请从以下背景数据中，为用户精选 5 个最匹配的工具。
        【用户需求】：{user_query}
        【背景数据】：{trimmed_context}
        任务要求：
        1. 给出 Top 5 工具名、核心优势、以及官网链接。
        2. 链接须从背景数据提取，找不到写N/A，严禁编造。
        3. 使用 Markdown 表格输出。
        """
        return self.llm.invoke(prompt).content

    def render_report(self, data):
        results = data.get("selected_results", [])
        report_lines = [f"## 参考文献\n"]
        current_dim = ""
        for item in results:
            if item.get('dimension') != current_dim:
                current_dim = item.get('dimension')
                report_lines.append(f"\n### 【{current_dim}】")
            report_lines.append(f"- **[{item['title']}]({item['url']})**")
        return "\n".join(report_lines)
    
    def calculate_distribution_adaptation(self, excel_path):
        try:
            df = pd.read_excel(excel_path)
            df.columns = df.columns.str.strip()
        except Exception as e:
            print(f"❌ 读取 Excel 失败: {e}")
            return
        results = []
        for _, row in tqdm(df.iterrows(), total=len(df)):
            query = row['Question']
            try:
                ideal_dist = eval(row['Ideal_Weight_Distribution'])
            except:
                continue
            strategy_data = self.define_search_strategy(query)
            if strategy_data and "plans" in strategy_data:
                actual_dist = {p['dimension']: p['quota'] for p in strategy_data['plans']}
            else:
                actual_dist = {}
            match_count = 0
            dimensions = ["榜单排名", "深度评测", "工程部署", "真实体验"]
            for label in dimensions:
                match_count += min(ideal_dist.get(label, 0), actual_dist.get(label, 0))
            adaptation_score = (match_count / 5) * 100
            results.append({
                "Query": query,
                "场景判定": strategy_data.get("scenario", "未知"),
                "理想分布": str(ideal_dist),
                "Agent决策分布": str(actual_dist),
                "适配得分": adaptation_score
            })
        res_df = pd.DataFrame(results)
        res_df.to_excel("Agent决策对齐报告.xlsx", index=False)
        print(f"\n📊 平均对齐度: {res_df['适配得分'].mean():.2f}%")

if __name__ == "__main__":
    agent = AIAgentExpert()
    print("🚀 欢迎使用场景化 AI 推荐助手！")
    user_query = input("👉 请输入您的需求：")
    if user_query.strip() and user_query.lower() not in ['exit', 'quit']:
        try:
            result = agent.run(user_query)
            print("\n" + "="*30 + "\n" + result + "\n" + "="*30)
        except Exception as e:
            print(f"❌ 运行出错：{e}")
    
    # 若要运行模型测评：检测模型对各类文章的权重分配是否准确，请运行下面代码，否则不需要运行
    # agent.calculate_distribution_adaptation("请修改为本地路径，使用名为"动态权重分布评测集"的xlsx文件")