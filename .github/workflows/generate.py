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

INDEX_CSS = """
    * { margin: 0; padding: 0; box-sizing: border-box; }
    :root {
        --bg-dark: #1a1a2e;
        --bg-card: #16213e;
        --accent-gold: #e6b800;
        --accent-green: #4ade80;
        --text-light: #f1f5f9;
        --text-muted: #94a3b8;
        --border: #334155;
    }
    body {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        background: var(--bg-dark);
        color: var(--text-light);
        min-height: 100vh;
    }
    .container {
        max-width: 1000px;
        margin: 0 auto;
        padding: 3rem 2rem;
    }
    header {
        text-align: center;
        margin-bottom: 4rem;
    }
    header::before {
        content: '♔';
        font-size: 4rem;
        color: var(--accent-gold);
        display: block;
        margin-bottom: 1rem;
        text-shadow: 0 0 30px rgba(230, 184, 0, 0.5);
    }
    h1 {
        font-size: 2.5rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        color: var(--text-muted);
        font-size: 1rem;
    }
    .stats {
        display: flex;
        justify-content: center;
        gap: 3rem;
        margin: 3rem 0;
        padding: 2rem;
        background: var(--bg-card);
        border-radius: 12px;
        border: 1px solid var(--border);
    }
    .stat { text-align: center; }
    .stat-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--accent-gold);
    }
    .stat-label {
        color: var(--text-muted);
        font-size: 0.875rem;
        margin-top: 0.5rem;
    }
    .games-section h2 {
        font-size: 1.25rem;
        color: var(--accent-gold);
        margin-bottom: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid var(--accent-gold);
        display: inline-block;
    }
    .game-list { display: flex; flex-direction: column; gap: 1rem; }
    .game-card {
        background: var(--bg-card);
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid var(--border);
        display: grid;
        grid-template-columns: auto 1fr auto;
        align-items: center;
        gap: 1.5rem;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    .game-card:hover {
        border-color: var(--accent-gold);
        transform: translateX(8px);
        box-shadow: 0 0 20px rgba(230, 184, 0, 0.2);
    }
    .game-result {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.25rem;
        font-weight: 700;
    }
    .result-win { background: linear-gradient(135deg, #22c55e, #16a34a); color: white; }
    .result-draw { background: linear-gradient(135deg, #f59e0b, #d97706); color: white; }
    .result-loss { background: linear-gradient(135deg, #ef4444, #dc2626); color: white; }
    .game-info h3 { font-size: 1.1rem; margin-bottom: 0.5rem; }
    .game-meta { display: flex; gap: 1rem; color: var(--text-muted); font-size: 0.875rem; }
    .game-color {
        padding: 0.25rem 0.75rem;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 500;
    }
    .color-white { background: #f8fafc; color: #1e293b; }
    .color-black { background: #334155; color: #f1f5f9; }
    .game-link {
        color: var(--accent-gold);
        text-decoration: none;
        padding: 0.5rem 1rem;
        border: 1px solid var(--accent-gold);
        border-radius: 6px;
        transition: all 0.3s ease;
    }
    .game-link:hover { background: var(--accent-gold); color: var(--bg-dark); }
    footer {
        text-align: center;
        margin-top: 4rem;
        padding-top: 2rem;
        border-top: 1px solid var(--border);
        color: var(--text-muted);
        font-size: 0.875rem;
    }
"""

GAME_CSS = """
    * { margin: 0; padding: 0; box-sizing: border-box; }
    :root {
        --bg-dark: #1a1a2e;
        --bg-card: #16213e;
        --accent-gold: #e6b800;
        --text-light: #f1f5f9;
        --text-muted: #94a3b8;
        --border: #334155;
    }
    body {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        background: var(--bg-dark);
        color: var(--text-light);
        min-height: 100vh;
        padding: 2rem;
    }
    .container {
        max-width: 800px;
        margin: 0 auto;
    }
    .back-link {
        display: inline-block;
        margin-bottom: 2rem;
        color: var(--accent-gold);
        text-decoration: none;
        font-size: 0.875rem;
    }
    .back-link:hover { text-decoration: underline; }
    .content {
        background: var(--bg-card);
        border-radius: 12px;
        padding: 2.5rem;
        border: 1px solid var(--border);
    }
    h1 {
        font-size: 1.75rem;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid var(--border);
    }
    .content h2 {
        color: var(--accent-gold);
        font-size: 1.1rem;
        margin: 1.5rem 0 0.75rem;
    }
    .content h3 {
        color: var(--text-light);
        font-size: 1rem;
        margin: 1rem 0 0.5rem;
    }
    .content p { line-height: 1.8; margin-bottom: 1rem; }
    .content ul, .content ol { margin-left: 1.5rem; margin-bottom: 1rem; }
    .content li { line-height: 1.8; margin-bottom: 0.25rem; }
    .content strong { color: var(--accent-gold); }
    .content code {
        background: var(--bg-dark);
        padding: 0.2rem 0.4rem;
        border-radius: 3px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.9em;
    }
    .content pre {
        background: var(--bg-dark);
        padding: 1rem;
        border-radius: 8px;
        overflow-x: auto;
        margin: 1rem 0;
    }
    .content pre code { background: none; padding: 0; }
    .content hr {
        border: none;
        border-top: 1px solid var(--border);
        margin: 1.5rem 0;
    }
"""

def generate_index_html():
    """Generate index.html with Style A (dark chess theme)."""
    games = get_game_list()

    # Calculate stats
    total = len(games)
    wins = sum(1 for g in games if g['result'] == '胜')
    draws = sum(1 for g in games if g['result'] == '和')
    losses = sum(1 for g in games if g['result'] == '败')

    games_html = ''
    for g in games:
        link = f"./{g['filename'].replace('.md', '.html')}"
        color_class = 'color-white' if g['color'] == '执白' else 'color-black'
        result_class = f'result-{g["result"]}'
        games_html += f"""
        <div class="game-card">
            <div class="game-result {result_class}">{g['result']}</div>
            <div class="game-info">
                <h3>vs {g['opponent']}</h3>
                <div class="game-meta">
                    <span class="game-color {color_class}">{g['color']}</span>
                    <span>{g['date']}</span>
                    <span>{g['steps']}步</span>
                </div>
            </div>
            <a href="{link}" class="game-link">查看 →</a>
        </div>
"""

    template = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>棋谱回顾 - chess-reviews-summary</title>
    <style>{INDEX_CSS}</style>
</head>
<body>
    <div class="container">
        <header>
            <h1>棋谱回顾</h1>
            <p class="subtitle">aaronwang2026 的国际象棋对局记录</p>
        </header>

        <div class="stats">
            <div class="stat">
                <div class="stat-value">{total}</div>
                <div class="stat-label">总对局</div>
            </div>
            <div class="stat">
                <div class="stat-value" style="color: #22c55e;">{wins}</div>
                <div class="stat-label">胜</div>
            </div>
            <div class="stat">
                <div class="stat-value" style="color: #f59e0b;">{draws}</div>
                <div class="stat-label">和</div>
            </div>
            <div class="stat">
                <div class="stat-value" style="color: #ef4444;">{losses}</div>
                <div class="stat-label">败</div>
            </div>
        </div>

        <section class="games-section">
            <h2>近期对局</h2>
            <div class="game-list">
                {games_html}
            </div>
        </section>

        <footer>
            <p>♔ 棋谱回顾 · 自动生成于 {datetime.now().strftime('%Y-%m-%d')}</p>
        </footer>
    </div>
</body>
</html>"""
    return template

def generate_game_html(filename):
    """Generate HTML for a single game markdown file."""
    md_content = read_file(os.path.join(SRC_DIR, filename))
    body_html = markdown.Markdown(extensions=['tables', 'fenced_code']).convert(md_content)

    title = filename.replace('.md', '').replace('_', ' ')

    template = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>{GAME_CSS}</style>
</head>
<body>
    <div class="container">
        <a href="./index.html" class="back-link">← 返回列表</a>
        <div class="content">
            {body_html}
        </div>
    </div>
</body>
</html>"""
    return template

def main():
    """Main build function."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    index_html = generate_index_html()
    with open(os.path.join(OUTPUT_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(index_html)

    for f in get_md_files():
        html = generate_game_html(f)
        output_path = os.path.join(OUTPUT_DIR, f.replace('.md', '.html'))
        with open(output_path, 'w', encoding='utf-8') as out:
            out.write(html)

    print(f"Generated site with {len(get_md_files()) + 1} pages in {OUTPUT_DIR}/")

if __name__ == '__main__':
    main()
