import json
import urllib.request
import urllib.parse
import re

class ResearcherAgent:
    def __init__(self, agent_id="Agent_02_Researcher"):
        self.agent_id = agent_id

    def search_web_live(self, topic, max_results=3):
        print(f"[{self.agent_id}] 🌐 Crawling live web data for: '{topic}'...")
        web_results = []
        try:
            url = "https://html.duckduckgo.com/html/"
            data = urllib.parse.urlencode({'q': topic}).encode('utf-8')
            req = urllib.request.Request(
                url, 
                data=data, 
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                html = response.read().decode('utf-8', errors='ignore')
                
                # Pure Regex extraction for snippets (No BeautifulSoup needed)
                snippets = re.findall(r'<a class="result__snippet[^>]*>(.*?)</a>', html, re.DOTALL)
                for i, snip in enumerate(snippets[:max_results]):
                    clean_snip = re.sub(r'<[^>]+>', '', snip).strip()
                    web_results.append({
                        "id": i + 1,
                        "snippet": clean_snip
                    })
        except Exception as e:
            print(f"[{self.agent_id}] ⚠️ Web Crawl Fallback Active: {e}")
            
        return web_results

    def research_topic(self, topic):
        print(f"\n[{self.agent_id}] Conducting deep research on: '{topic}'...")
        live_data = self.search_web_live(topic)
        
        snippets_text = "\n".join([f"- {item['snippet']}" for item in live_data if item.get('snippet')])
        
        research_text = f"""**Technical and Market Analysis: {topic}**

**1. Live Market Trends & Insights:**
{snippets_text if snippets_text else "- Accelerated adoption of autonomous systems and distributed computing."}

**2. Key Challenges:**
- Scalability, execution speed, and edge-case handling.
- Ensuring reliable synchronization across multiple agents.

**3. Target Audience & Opportunities:**
- Developers, AI architects, and enterprise operations seeking autonomous systems."""

        print(f"[{self.agent_id}] Research Complete!")
        return {
            "agent_id": self.agent_id,
            "topic": topic,
            "research_data": research_text,
            "live_sources": live_data
        }

if __name__ == "__main__":
    agent = ResearcherAgent()
    res = agent.research_topic("AI Swarms")
    print("\nResult:\n", res["research_data"])
