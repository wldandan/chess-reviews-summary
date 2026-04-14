#!/usr/bin/env python3
"""Generate static HTML site from markdown files."""

import os
import markdown
from datetime import datetime

SRC_DIR = 'docs'
OUTPUT_DIR = '_site'

def get_md_files():
    """Get all markdown files in docs/ directory."""
    files = []
    if os.path.exists(SRC_DIR):
        for f in sorted(os.listdir(SRC_DIR)):
            if f.endswith('.md') and f != 'index.md':
                files.append(f)
    return files

def read_file(path):
    """Read file content."""
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def get_game_list():
    """Generate game list from markdown files."""
    games = []
    for f in get_md_files():
        # Parse filename: 2026-04-14_aaronwang2026_执白胜_aaronwang2026_vs_Clement924810_19步
        # parts[0]=date, parts[1]=player, parts[2]=color+result, parts[3]=player(again), parts[4]=vs, parts[5]=opponent
        parts = f.replace('.md', '').split('_')
        if len(parts) >= 6:
            date = parts[0]
            color_text = '执白' if '执白' in f else '执黑'
            result = '胜' if '胜' in f else ('和' if '和' in f else '败')
            opponent = parts[5]
            steps = parts[-1] if '步' in parts[-1] else '-'

            games.append({
                'date': date,
                'color': color_text,
                'result': result,
                'opponent': opponent,
                'steps': steps,
                'filename': f
            })
    return sorted(games, key=lambda x: x['date'], reverse=True)

def generate_index_html():
    """Generate index.html."""
    md_content = read_file(os.path.join(SRC_DIR, 'index.md'))
    html = markdown.Markdown(extensions=['tables']).convert(md_content)

    games = get_game_list()
    games_html = ''
    for g in games:
        link = f"./{g['filename'].replace('.md', '.html')}"
        games_html += f"""<tr>
          <td>{g['date']}</td>
          <td>{g['color']}</td>
          <td>{g['opponent']}</td>
          <td class="result-{g['result']}">{g['result']}</td>
          <td>{g['steps']}</td>
          <td><a href="{link}">查看</a></td>
        </tr>
"""

    template = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>棋谱回顾 - chess-reviews-summary</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 900px;
            margin: 0 auto;
            padding: 2rem;
            line-height: 1.6;
            background: #fafafa;
        }}
        h1 {{ color: #333; border-bottom: 2px solid #333; padding-bottom: 0.5rem; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            margin: 1rem 0;
        }}
        th, td {{
            padding: 0.75rem;
            text-align: left;
            border-bottom: 1px solid #eee;
        }}
        th {{ background: #f5f5f5; font-weight: 600; }}
        .result-胜 {{ color: #22c55e; font-weight: bold; }}
        .result-负 {{ color: #ef4444; }}
        .result-和 {{ color: #f59e0b; }}
        a {{ color: #2563eb; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        .back-link {{ margin-top: 2rem; }}
        footer {{ margin-top: 2rem; color: #666; font-size: 0.875rem; }}
    </style>
</head>
<body>
    <h1>🏁 棋谱回顾</h1>
    <table>
        <thead>
            <tr>
                <th>日期</th>
                <th>执方</th>
                <th>对手</th>
                <th>结果</th>
                <th>回合</th>
                <th>详情</th>
            </tr>
        </thead>
        <tbody>
            {games_html}
        </tbody>
    </table>
    <footer>自动生成于 {datetime.now().strftime('%Y-%m-%d %H:%M')}</footer>
</body>
</html>"""
    return template

def generate_game_html(filename):
    """Generate HTML for a single game markdown file."""
    md_content = read_file(os.path.join(SRC_DIR, filename))
    body_html = markdown.Markdown(extensions=['tables']).convert(md_content)

    title = filename.replace('.md', '').replace('_', ' ')

    template = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 900px;
            margin: 0 auto;
            padding: 2rem;
            line-height: 1.8;
            background: #fafafa;
        }}
        .content {{
            background: white;
            padding: 2rem;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        pre {{
            background: #f5f5f5;
            padding: 1rem;
            border-radius: 4px;
            overflow-x: auto;
        }}
        code {{
            background: #f5f5f5;
            padding: 0.2rem 0.4rem;
            border-radius: 3px;
            font-size: 0.9em;
        }}
        pre code {{ background: none; padding: 0; }}
        .back-link {{ margin-top: 2rem; }}
        a {{ color: #2563eb; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <div class="content">
        {body_html}
    </div>
    <div class="back-link">
        <a href="./index.html">← 返回列表</a>
    </div>
</body>
</html>"""
    return template

def main():
    """Main build function."""
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Generate index
    index_html = generate_index_html()
    with open(os.path.join(OUTPUT_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(index_html)

    # Generate game pages
    for f in get_md_files():
        html = generate_game_html(f)
        output_path = os.path.join(OUTPUT_DIR, f.replace('.md', '.html'))
        with open(output_path, 'w', encoding='utf-8') as out:
            out.write(html)

    print(f"Generated site with {len(get_md_files()) + 1} pages in {OUTPUT_DIR}/")

if __name__ == '__main__':
    main()
