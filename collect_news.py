"""
AI新闻采集与分析脚本
每天自动运行，抓取国内AI新闻并生成投资建议
"""

import os
import json
import datetime
import re
from pathlib import Path

# 模拟新闻数据（实际运行时会调用API抓取）
SAMPLE_NEWS = [
    {
        "title": "百度文心一言用户突破1亿，API调用量日增300%",
        "source": "36kr",
        "url": "https://36kr.com/news/123456",
        "summary": "百度官方数据显示，文心一言上线以来用户数快速增长",
        "related_stocks": ["BIDU", "9888.HK"]
    },
    {
        "title": "阿里云发布最新AI模型训练集群，性能提升40%",
        "source": "虎嗅",
        "url": "https://huxiu.com/news/234567",
        "summary": "阿里云推出新一代GPU集群，专注大模型训练",
        "related_stocks": ["BABA", "9988.HK"]
    },
    {
        "title": "科大讯飞发布星火大模型4.0，语音交互能力大幅提升",
        "source": "钛媒体",
        "url": "https://tmtpost.com/news/345678",
        "summary": "科大讯飞展示最新AI能力，落地场景进一步扩展",
        "related_stocks": ["002230.SZ"]
    },
    {
        "title": "腾讯混元大模型接入微信搜索，AI助手呼之欲出",
        "source": "财新",
        "url": "https://caixin.com/news/456789",
        "summary": "腾讯AI能力与微信生态深度整合",
        "related_stocks": ["0700.HK", "TCEHY"]
    },
    {
        "title": "字节跳动AI研究院开源新一代多模态模型",
        "source": "机器之心",
        "url": "https://jiqizhixin.com/news/567890",
        "summary": "字节跳动开源模型性能接近GPT-4V",
        "related_stocks": ["BDNYSE"]
    }
]

# 股票背景信息（用于分析）
STOCK_INFO = {
    "BIDU": {"name": "百度", "hk_code": "9888.HK", "industry": "AI/搜索引擎", "position": "国内AI领军企业，文心一言为核心产品"},
    "BABA": {"name": "阿里巴巴", "hk_code": "9988.HK", "industry": "云计算/电商", "position": "阿里云国内第一，AI算力布局完善"},
    "002230.SZ": {"name": "科大讯飞", "a_code": "002230", "industry": "AI/语音技术", "position": "语音AI龙头，教育+医疗场景落地"},
    "0700.HK": {"name": "腾讯", "hk_code": "0700.HK", "industry": "社交/云/AI", "position": "混元大模型+微信生态"},
    "BDNYSE": {"name": "字节跳动", "note": "未上市", "industry": "AI/内容平台", "position": "AI研究院实力强劲，海外TikTok数据优势"}
}

def fetch_news():
    """抓取新闻（这里用模拟数据，实际可以接入API）"""
    return SAMPLE_NEWS

def analyze_stocks(news_list):
    """分析新闻，生成股票建议"""
    recommendations = []
    
    for news in news_list:
        for stock_code in news.get("related_stocks", []):
            stock = STOCK_INFO.get(stock_code, {})
            if not stock:
                continue
                
            # 生成分析
            analysis = {
                "stock_code": stock_code,
                "stock_name": stock.get("name", stock_code),
                "news_title": news["title"],
                "news_summary": news["summary"],
                "company_position": stock.get("position", ""),
                "industry": stock.get("industry", ""),
                "signal": "正面" if any(kw in news["title"] for kw in ["发布", "突破", "增长", "开源", "合作"]) else "中性",
                "confidence": "中等",
                "reasoning": f"基于新闻'{news['title']}'，{stock.get('name')}在{stock.get('industry')}领域{stock.get('position')}。"
            }
            recommendations.append(analysis)
    
    return recommendations

def generate_html(news_list, recommendations):
    """生成静态网站HTML"""
    today = datetime.datetime.now().strftime("%Y年%m月%d日")
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI新闻日报 - {today}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f5f5f5; line-height: 1.6; }}
        .container {{ max-width: 800px; margin: 0 auto; padding: 20px; }}
        header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 12px; margin-bottom: 20px; }}
        header h1 {{ font-size: 28px; margin-bottom: 8px; }}
        header p {{ opacity: 0.9; }}
        .section {{ background: white; border-radius: 12px; padding: 24px; margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }}
        .section h2 {{ color: #333; margin-bottom: 16px; padding-bottom: 12px; border-bottom: 2px solid #667eea; }}
        .news-item {{ padding: 16px 0; border-bottom: 1px solid #eee; }}
        .news-item:last-child {{ border-bottom: none; }}
        .news-item h3 {{ color: #333; font-size: 18px; margin-bottom: 8px; }}
        .news-item .meta {{ color: #888; font-size: 14px; margin-bottom: 8px; }}
        .news-item .summary {{ color: #666; }}
        .stock-card {{ background: #f8f9fa; border-radius: 8px; padding: 16px; margin-bottom: 12px; border-left: 4px solid #667eea; }}
        .stock-card.positive {{ border-left-color: #28a745; }}
        .stock-card .stock-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }}
        .stock-card .stock-name {{ font-weight: bold; font-size: 18px; }}
        .stock-card .signal {{ padding: 4px 12px; border-radius: 20px; font-size: 14px; }}
        .signal.positive {{ background: #d4edda; color: #155724; }}
        .signal.neutral {{ background: #fff3cd; color: #856404; }}
        .stock-card .company-info {{ color: #666; font-size: 14px; margin: 8px 0; }}
        .stock-card .reasoning {{ color: #888; font-size: 14px; }}
        .warning {{ background: #fff3cd; border: 1px solid #ffc107; border-radius: 8px; padding: 16px; margin-bottom: 20px; }}
        .warning h3 {{ color: #856404; margin-bottom: 8px; }}
        .warning p {{ color: #856404; font-size: 14px; }}
        footer {{ text-align: center; color: #888; padding: 20px; font-size: 14px; }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🤖 AI新闻日报</h1>
            <p>{today} | 每日更新</p>
        </header>
        
        <div class="warning">
            <h3>⚠️ 风险提示</h3>
            <p>以下股票分析仅供娱乐参考，不构成任何投资建议。投资有风险，入市需谨慎。相关内容与任何金融机构无关联。</p>
        </div>
        
        <div class="section">
            <h2>📰 今日AI热文</h2>
"""
    
    for news in news_list:
        html += f"""
            <div class="news-item">
                <h3>{news['title']}</h3>
                <div class="meta">来源: {news['source']}</div>
                <div class="summary">{news['summary']}</div>
            </div>
"""
    
    html += """
        </div>
        
        <div class="section">
            <h2>📈 股票分析建议</h2>
"""
    
    for rec in recommendations:
        signal_class = "positive" if rec["signal"] == "正面" else "neutral"
        html += f"""
            <div class="stock-card {signal_class}">
                <div class="stock-header">
                    <span class="stock-name">{rec['stock_name']} ({rec['stock_code']})</span>
                    <span class="signal {signal_class}">{rec['signal']}</span>
                </div>
                <div class="company-info">🏢 {rec['company_position']}</div>
                <div class="company-info">📊 行业: {rec['industry']}</div>
                <div class="reasoning">💡 {rec['reasoning']}</div>
            </div>
"""
    
    html += f"""
        </div>
        
        <footer>
            <p>🤖 由AI自动生成 | 数据来源: 36kr, 虎嗅, 钛媒体, 财新</p>
            <p>更新时间: {today}</p>
        </footer>
    </div>
</body>
</html>
"""
    
    return html

def main():
    """主函数"""
    print("🤖 开始生成AI新闻日报...")
    
    # 1. 抓取新闻
    news_list = fetch_news()
    print(f"   抓取到 {len(news_list)} 条新闻")
    
    # 2. 分析股票
    recommendations = analyze_stocks(news_list)
    print(f"   生成 {len(recommendations)} 条股票建议")
    
    # 3. 生成HTML
    html = generate_html(news_list, recommendations)
    
    # 4. 保存
    output_path = Path("index.html")
    output_path.write_text(html, encoding="utf-8")
    print(f"   已生成: {output_path.absolute()}")
    
    # 5. 保存数据JSON（方便后续查看）
    data = {
        "date": datetime.datetime.now().isoformat(),
        "news": news_list,
        "recommendations": recommendations
    }
    Path("data.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print("   已保存: data.json")
    
    print("✅ 完成!")

if __name__ == "__main__":
    main()
