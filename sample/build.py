#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
採用サイト デモ・ジェネレーター / Studio Maple
--------------------------------------------------
商談ごとの「社名差し替えデモ」は、下の CONFIG と BRAND を書き換えて
    python3 build.py
を実行するだけ。dist/ に5ページ + style.css + site.js が生成される。

差し替えるのは基本この2つの辞書だけ。本文まで実企業に寄せたい場合は
PAGES 内のテキストを直接編集する。
"""
import os, shutil, html

OUT = "dist"

# ============================================================
# ここだけ書き換える ①：会社情報
# ============================================================
CONFIG = {
    "company":     "株式会社仁淀川建設",
    "short":       "仁淀川建設",
    "romaji":      "NIYODOGAWA KENSETSU RECRUITING",
    "zip":         "781-21XX",
    "address":     "高知県吾川郡いの町XXXX",
    "tel":         "0XX-XXX-XXXX",
    "tel_link":    "0XXXXXXXXX",          # tel: 用（ハイフンなし）
    "tel_hours":   "平日 8:00〜17:00",
    "business":    "土木一式工事・舗装工事・河川維持工事 ほか",
    "founded":     1978,
    "years":       48,
    "employees":   35,
    "avg_age":     44,
    "projects":    120,
    "midcareer":   8,
    "ceo":         "仁淀 太郎",
    "site_url":    "https://studiomaple.jp/sample/",   # OGP用の絶対URL
    "is_demo":     True,                                # False にすると免責とバナーが消える
}

# ============================================================
# ここだけ書き換える ②：ブランドカラー
# ============================================================
BRAND = {
    "ink":         "#12333d",   # 濃色（ヘッダー/フッター/見出し）
    "primary":     "#15839f",   # メインカラー（仁淀ブルー）
    "primary_deep":"#0c5b70",   # メインの濃いほう（リンク/数字）
    "mist":        "#eaf4f6",   # 淡い面
    "paper":       "#fafcfc",   # 背景
    "accent":      "#e59d18",   # アクセント（工事標識のアンバー）
    "accent_ink":  "#3d2a00",   # アクセント上の文字色
    "text":        "#31414a",
    "muted":       "#5c6d73",   # AA適合（mist背景で4.82:1）
    "line":        "#d4e4e8",
    "hero_pale":   "#a8d8e4",
}

# スタジオメイプル側の情報（about.html で使用）
SM = {
    "name":   "スタジオメイプル",
    "person": "岩見 梓司",
    "mail":   "iwami@studiomaple.jp",
    "url":    "https://studiomaple.jp/",
    "tel":    "",   # 載せるなら記入
}

# ============================================================
# 補助金のプレースホルダー ★要綱を確認して必ず実数に差し替えること★
# ============================================================
SUBSIDY = {
    "name":        "高知県求人情報発信等支援事業費補助金",
    "rate":        "◯分の◯",          # 補助率
    "cap":         "◯◯万円",           # 上限額
    "price":       "◯◯◯,◯◯◯",        # 制作費（税込）
    "grant":       "◯◯◯,◯◯◯",        # 補助額
    "net":         "65,000",            # 実質負担
    "requirement": "高知県ワーク・ライフ・バランス推進企業認証",
}

C = CONFIG

# ------------------------------------------------------------
# 共通パーツ
# ------------------------------------------------------------
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link href="https://fonts.googleapis.com/css2?'
         'family=Zen+Kaku+Gothic+New:wght@700;900&family=Noto+Sans+JP:wght@400;700'
         '&display=swap" rel="stylesheet">')

# ファビコン（外部ファイル不要のインラインSVG）
FAVICON = ('<link rel="icon" href="data:image/svg+xml,'
           '%3Csvg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 40 40\'%3E'
           '%3Crect width=\'40\' height=\'40\' rx=\'9\' fill=\'%2315839f\'/%3E'
           '%3Cpath d=\'M6 25c5-6 9 2 14-3s9 1 14-4\' fill=\'none\' stroke=\'white\' '
           'stroke-width=\'3\' stroke-linecap=\'round\'/%3E%3C/svg%3E">')

LOGO = '''<svg class="brand-mark" viewBox="0 0 40 40" aria-hidden="true">
        <rect width="40" height="40" rx="9" fill="%s"/>
        <path d="M6 25c5-6 9 2 14-3s9 1 14-4" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round"/>
        <path d="M6 32c5-6 9 2 14-3s9 1 14-4" fill="none" stroke="%s" stroke-width="2.4" stroke-linecap="round"/>
      </svg>''' % (BRAND["primary"], BRAND["hero_pale"])

NAV = [("index.html", "トップ"), ("work.html", "仕事内容"),
       ("voices.html", "社員の声"), ("recruit.html", "募集要項")]


def head(page, title, desc):
    og_title = html.escape(title)
    og_desc = html.escape(desc)
    return f'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{og_title}</title>
<meta name="description" content="{og_desc}">
<meta property="og:type" content="website">
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{og_desc}">
<meta property="og:url" content="{C["site_url"]}{page}">
<meta property="og:image" content="{C["site_url"]}ogp.png">
<meta property="og:site_name" content="{C["company"]} 採用サイト（制作サンプル）">
<meta name="twitter:card" content="summary_large_image">
{FAVICON}
{FONTS}
<link rel="stylesheet" href="style.css?v=2">
</head>
<body>
<a class="skip" href="#main">本文へスキップ</a>
'''


def header(current):
    items = ""
    for href, label in NAV:
        cur = ' aria-current="page"' if href == current else ""
        cta = ' class="nav-cta"' if href == "recruit.html" else ""
        items += f'      <a href="{href}"{cta}{cur}>{label}</a>\n'
    return f'''<header class="site-header">
  <div class="header-in">
    <a class="brand" href="index.html" aria-label="{C["short"]} 採用サイト トップ">
      {LOGO}
      <span class="brand-name">{C["short"]}<small>RECRUITING SITE</small></span>
    </a>
    <nav class="gnav" aria-label="サイト内メニュー">
{items}    </nav>
  </div>
</header>
'''


def footer():
    disc = ""
    if C["is_demo"]:
        disc = ('    <p class="disclaimer">本サイトは、' + SM["name"] +
                'が採用サイトの制作サンプルとして作成した架空の企業サイトです。'
                '社名・人物・数値はすべて架空のものであり、実在の企業・団体・人物とは関係ありません。'
                '<br><a href="about.html">サイト制作についてのご案内はこちら →</a></p>\n')
    return f'''<footer class="site-footer">
  <div class="footer-in">
    <p class="fbrand">{C["company"]}</p>
    <p>〒{C["zip"]} {C["address"]}<br>
       TEL：<a href="tel:{C["tel_link"]}">{C["tel"]}</a>（採用担当・{C["tel_hours"]}）<br>
       事業内容：{C["business"]}</p>
{disc}  </div>
</footer>
'''


def banner(msg):
    if not C["is_demo"]:
        return ""
    return f'''<div class="sample-banner" role="complementary" aria-label="制作サンプルのご案内">
  <span class="tag">制作サンプル</span>
  <span class="msg">{msg}</span>
  <a class="banner-cta" href="about.html">料金と補助金を見る →</a>
</div>
'''


def scripts():
    return '<script src="site.js"></script>\n</body>\n</html>\n'


RIVER = ('<svg class="river" viewBox="0 0 1200 34" preserveAspectRatio="none" aria-hidden="true">'
         '<path d="M0 20 C200 4 380 32 600 18 S1000 6 1200 22 V34 H0 Z" fill="currentColor"/></svg>')
RIVER_UP = ('<svg class="river on-mist" viewBox="0 0 1200 34" preserveAspectRatio="none" aria-hidden="true">'
            '<path d="M0 20 C200 4 380 32 600 18 S1000 6 1200 22 V0 H0 Z" fill="currentColor"/></svg>')

# WLB認証バッジ（★実案件では認証マーク画像に差し替え）
CERT = f'''<div class="cert">
  <svg class="cert-mark" viewBox="0 0 64 64" aria-hidden="true">
    <circle cx="32" cy="32" r="29" fill="none" stroke="{BRAND['primary']}" stroke-width="2.5"/>
    <circle cx="32" cy="32" r="23" fill="{BRAND['mist']}"/>
    <path d="M21 33l7 7 15-16" fill="none" stroke="{BRAND['primary_deep']}" stroke-width="4"
          stroke-linecap="round" stroke-linejoin="round"/>
  </svg>
  <div>
    <p class="cert-name">高知県ワーク・ライフ・バランス推進企業認証</p>
    <p class="cert-note">週休二日制への移行、有給取得率78%、資格取得費用の全額会社負担。
      掛け声ではなく、制度として整えました。</p>
  </div>
</div>'''


# ============================================================
# 各ページの本文
# ============================================================
def page_index():
    return f'''{head("index.html", f"採用サイト｜{C['company']}（制作サンプル）",
                     f"高知県いの町の総合建設会社・{C['short']}（架空）の採用サイト制作サンプル。取材・撮影・応募フォームまで、スタジオメイプルが制作しました。")}
{header("index.html")}
<main id="main">
  <section class="hero">
    <svg class="hero-scene" viewBox="0 0 1200 560" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
      <defs>
        <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stop-color="{BRAND['ink']}"/><stop offset="1" stop-color="{BRAND['primary_deep']}"/>
        </linearGradient>
        <linearGradient id="water" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stop-color="{BRAND['primary']}"/><stop offset="1" stop-color="#0a4a5c"/>
        </linearGradient>
      </defs>
      <rect width="1200" height="560" fill="url(#sky)"/>
      <path d="M0 300 L260 170 L470 290 L700 150 L950 300 L1200 210 V560 H0 Z" fill="#0e4152" opacity=".85"/>
      <path d="M0 360 L300 260 L560 370 L860 240 L1200 350 V560 H0 Z" fill="#0b3644" opacity=".9"/>
      <path d="M0 420 C300 380 500 470 750 430 S1050 380 1200 420 V560 H0 Z" fill="url(#water)"/>
      <path d="M0 470 C300 430 520 515 780 478 S1080 430 1200 470" fill="none" stroke="{BRAND['hero_pale']}" stroke-width="3" opacity=".5"/>
      <path d="M0 505 C300 468 520 548 780 512 S1080 468 1200 505" fill="none" stroke="{BRAND['hero_pale']}" stroke-width="2" opacity=".3"/>
    </svg>
    <div class="hero-in">
      <p class="eyebrow">{C["romaji"]}</p>
      <h1>あなたが今日直した道を、<br>あした、誰かが渡っていく。</h1>
      <p>仁淀川のほとりで{C["years"]}年。わたしたちは、いの町とその周辺の道路・河川・農地をつくり、直し、守ってきた総合建設会社です。次の{C["years"]}年を一緒につくる仲間を、経験の有無を問わず募集しています。</p>
      <div class="hero-cta">
        <a class="btn btn-accent" href="recruit.html">募集要項を見る</a>
        <a class="btn btn-ghost" href="voices.html">先輩の話を聞く</a>
      </div>
    </div>
  </section>
  {RIVER}

  <section class="section">
    <div class="section-in">
      <p class="sec-label">ABOUT US</p>
      <h2>数字で見る、{C["short"]}</h2>
      <p class="lede">大きな会社ではありません。そのぶん、一人ひとりの仕事が町の風景に残ります。</p>
      <div class="stats">
        <div class="stat"><b>{C["years"]}<small>年</small></b><span>創業{C["founded"]}年・いの町</span></div>
        <div class="stat"><b>{C["employees"]}<small>名</small></b><span>従業員数（平均年齢{C["avg_age"]}歳）</span></div>
        <div class="stat"><b>{C["projects"]}<small>件</small></b><span>年間施工件数（公共工事中心）</span></div>
        <div class="stat"><b>{C["midcareer"]}<small>名</small></b><span>直近5年の中途入社</span></div>
      </div>
      {CERT}
    </div>
  </section>

  <section class="section tint">
    <div class="section-in">
      <p class="sec-label">CONTENTS</p>
      <h2>働く前に、知ってほしいこと</h2>
      <div class="cards">
        <a class="card" href="work.html">
          <h3>仕事内容と1日の流れ</h3>
          <p>朝7時半の点呼から17時の帰所まで。土木の現場の実際と、未経験からの成長ステップ。</p>
          <span class="more">くわしく見る →</span>
        </a>
        <a class="card" href="voices.html">
          <h3>社員の声</h3>
          <p>いの町育ちの3年目、大阪からUターンした現場監督、二児の母の土木職。3人の本音インタビュー。</p>
          <span class="more">くわしく見る →</span>
        </a>
        <a class="card" href="recruit.html">
          <h3>募集要項・応募</h3>
          <p>正社員（土木作業員・現場監督候補）。給与、休日、資格取得支援の詳細と応募フォーム。</p>
          <span class="more">くわしく見る →</span>
        </a>
      </div>
    </div>
  </section>
  {RIVER_UP}

  <section class="section">
    <div class="section-in">
      <p class="sec-label">MESSAGE</p>
      <h2>代表からのメッセージ</h2>
      <div class="message">
        <figure class="photo portrait">
          <figcaption>※代表の写真が入ります（取材時に撮影）</figcaption>
        </figure>
        <div>
          <p>建設業は「きつい仕事」と言われてきました。否定はしません。夏は暑いし、雨の予報に一喜一憂する仕事です。ただ、{C["years"]}年この町で商売をしてきて確かに言えるのは、台風のあと真っ先に道を開けるのはわたしたちだ、ということです。誰かがやらなければ、町は止まる。その「誰か」であることの誇りを、給料や休日といった当たり前の待遇と一緒に、次の世代へ渡していきたい。</p>
          <p>週休二日制への移行も、資格取得費用の全額会社負担も、すでに済ませました。掛け声だけでは、人は残りませんから。</p>
          <p>経験は問いません。重機の免許も、入ってから取ればいい。仁淀川の見える事務所で、お待ちしています。</p>
          <p class="sign">{C["company"]} 代表取締役<b>{C["ceo"]}</b></p>
        </div>
      </div>
    </div>
  </section>
</main>
{footer()}
{banner("このような採用サイトを、県の補助金活用で実質負担 約6.5万円から。")}
{scripts()}'''


def page_work():
    return f'''{head("work.html", f"仕事内容｜{C['company']} 採用サイト（制作サンプル）",
                     "道路・河川・造成の仕事内容、現場の1日の流れ、未経験からの成長ステップ。")}
{header("work.html")}
<main id="main">
  <section class="section">
    <div class="section-in">
      <p class="sec-label">WORK</p>
      <h1>道路と河川を、つくって、直して、守る仕事</h1>
      <p class="lede">主な現場は、いの町と高知市周辺の道路改良・舗装・河川維持工事です。国や県、町から発注される公共工事が中心なので、景気に左右されにくく、仕事は年間を通じて安定しています。ここでは、土木部のいちばん標準的な1日をご紹介します。</p>
      <figure class="photo" style="margin-top:24px">
        <figcaption>※現場の写真が入ります（取材時に撮影）</figcaption>
      </figure>
    </div>
  </section>

  <section class="section">
    <div class="section-in">
      <p class="sec-label">OUR FIELD</p>
      <h2>こんな仕事をしています</h2>
      <p class="lede">私たちの仕事は、完成すると「当たり前の景色」になります。毎日通る道、雨の日に地域を守る排水路、家族が安心して暮らせる土地。派手ではないけれど、暮らしを下支えする仕事です。</p>
      <div class="cards">
        <div class="card static">
          <h3>道路・舗装工事</h3>
          <p>地域の生活道路や駐車場を整備する仕事。車や人が安全に通れるよう、地面をならし、舗装し、仕上げます。</p>
        </div>
        <div class="card static">
          <h3>河川・排水まわりの工事</h3>
          <p>大雨のときに水があふれないよう、排水路や護岸を整えます。仁淀川流域で暮らす地域の、防災につながる仕事です。</p>
        </div>
        <div class="card static">
          <h3>造成・外構工事</h3>
          <p>住宅や施設を建てる前の土地づくり、駐車場、ブロック塀やフェンスなど。暮らしのいちばん近くに、形として残ります。</p>
        </div>
      </div>
    </div>
  </section>

  <section class="section tint">
    <div class="section-in">
      <p class="sec-label">DAILY SCHEDULE</p>
      <h2>現場のある日の流れ</h2>
      <p class="lede">実働7時間30分。休憩は午前・昼・午後の3回、合わせて120分とっています。</p>
      <ol class="tl">
        <li><time>7:30</time><b>会社集合・朝礼</b><p>ラジオ体操と、その日の作業・安全確認（KY活動）。社用車に乗り合わせて現場へ。現場はほとんどが会社から車で30分圏内です。</p></li>
        <li><time>8:00</time><b>現場作業スタート</b><p>舗装の打ち替え、側溝の据え付け、法面の補修など。未経験の方はまず、測量の手元や合図・誘導からはじめます。</p></li>
        <li><time>10:00</time><b>休憩（30分）</b><p>暑い時期は休憩を増やして体調優先。飲み物は会社支給です。</p></li>
        <li><time>12:00</time><b>昼休憩（60分）</b><p>車で仮眠する人、川を見ながら弁当の人、それぞれ。</p></li>
        <li><time>15:00</time><b>休憩（30分）</b><p>午後の後半戦の前にもう一度。無理をしない・させないのが現場の共通ルールです。</p></li>
        <li><time>17:00</time><b>帰所・片付け・日報</b><p>道具を洗って日報を書いたら解散。残業は月平均10時間ほど。工期前でも19時を超えることはほぼありません。</p></li>
      </ol>
    </div>
  </section>
  {RIVER_UP}

  <section class="section">
    <div class="section-in">
      <p class="sec-label">CAREER STEP</p>
      <h2>未経験からの成長ステップ</h2>
      <p class="lede">最初から難しい作業を一人で任せることはありません。入社後はまず、道具や材料の準備、片付け、資材の運搬、測量や位置出しのサポート、安全確認といった補助作業から。現場の流れを覚えながら、できることを少しずつ増やしていきます。資格取得の費用（受験料・講習費・教材費）は全額会社負担。取得すれば資格手当が毎月の給与に上乗せされます。</p>
      <div class="steps">
        <div class="step">
          <span class="yr">1年目</span>
          <h3>現場を覚える</h3>
          <p>先輩とペアで、測量の手元・合図誘導・簡単な作業から。まずは小型車両系建機と玉掛けの資格を取得します。</p>
        </div>
        <div class="step">
          <span class="yr">3年目</span>
          <h3>重機に乗る</h3>
          <p>バックホウなどの重機オペレーターとして作業の中心に。2級土木施工管理技士の受験をここで勧めています。</p>
        </div>
        <div class="step">
          <span class="yr">5年目〜</span>
          <h3>現場を任される</h3>
          <p>現場代理人として工程・安全・原価を管理する側へ。1級取得者には監理技術者への道もあります。</p>
        </div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="section-in">
      <p class="sec-label">HONESTLY</p>
      <h2>正直にいうと、楽な仕事ではありません</h2>
      <p class="lede">外での作業なので、夏は暑く、冬は寒い日もあります。重いものを運ぶ場面もありますし、天候で予定が変わることもあります。ただし、一人で無理をさせることはありません。休憩を取りながら、チームで声をかけ合い、安全を第一に進めるのがこの会社のやり方です。「体を動かす仕事がしたい」「机に向かうより現場が合っている」「手に職をつけたい」——そんな方には、続けるほど面白くなる仕事です。</p>
      <div class="steps" style="margin-top:22px">
        <div class="step plain">
          <h3>身につく技術</h3>
          <p>土木の基礎知識、道具や重機の扱い、現場の安全管理。地域の暮らしを支える技術が、手に残ります。</p>
        </div>
        <div class="step plain">
          <h3>身につく力</h3>
          <p>チームで段取りを組み、声をかけ合って進める力。現場は一人では回りません。だから、人が育ちます。</p>
        </div>
        <div class="step plain">
          <h3>その先のキャリア</h3>
          <p>重機オペレーター、職長、現場管理者。資格を取るほどできる仕事が増え、次のステップが見えてきます。</p>
        </div>
      </div>
    </div>
  </section>

  <section class="section tint">
    <div class="section-in">
      <p class="sec-label">Q&amp;A</p>
      <h2>正直に答えます、よくある質問</h2>
      <div class="faq">
        <details>
          <summary>体力に自信がないのですが、やっていけますか？</summary>
          <p>最初の1ヶ月は誰でも筋肉痛です。ただ、今の土木は機械化が進んでいて「力仕事を根性で乗り切る」場面は昔よりずっと減りました。60代の現役も2名います。慣れるまでは作業量を調整するので、心配いりません。</p>
        </details>
        <details>
          <summary>休みは本当に取れますか？</summary>
          <p>週休二日制（4週8休）へ移行済みで、年間休日は105日です。日曜は完全に休み。台風などの災害対応で出勤した場合は、必ず代休を取ってもらいます。有給取得率は78%（昨年実績）です。</p>
        </details>
        <details>
          <summary>資格も経験もありません。応募できますか？</summary>
          <p>できます。直近5年の中途入社{C["midcareer"]}名のうち5名は、前職が運送・飲食・製造など建設未経験でした。必要な資格は入社後に会社負担で取れます。普通免許だけあれば大丈夫です。</p>
        </details>
        <details>
          <summary>転勤はありますか？</summary>
          <p>ありません。勤務地は高知県内（主にいの町・高知市周辺）のみです。県外への長期出張もありません。</p>
        </details>
        <details>
          <summary>応募の前に、職場を見学できますか？</summary>
          <p>できます。というより、おすすめしています。事務所と現場の雰囲気を見て、先輩と話してから決めてください。見学だけで終わっても、まったく問題ありません。</p>
        </details>
        <details>
          <summary>県外からの応募もできますか？</summary>
          <p>もちろんです。Uターン・Iターンで高知に戻る・移る方を歓迎しています。現に、大阪から転職してきた現場監督が働いています（<a href="voices.html">社員の声</a>で本人が話しています）。遠方の方はオンラインでの面談も可能です。</p>
        </details>
      </div>
    </div>
  </section>
</main>
{footer()}
{banner("仕事内容・1日の流れの取材と執筆も込みで、実質負担 約6.5万円から。")}
{scripts()}'''


def page_voices():
    return f'''{head("voices.html", f"社員の声｜{C['company']} 採用サイト（制作サンプル）",
                     "新卒3年目、Uターン転職の現場監督、二児の母。3人の本音インタビュー。")}
{header("voices.html")}
<main id="main">
  <section class="section">
    <div class="section-in">
      <p class="sec-label">VOICES</p>
      <h1>ここで働く3人の、本当の話</h1>
      <p class="lede">求人票には書けないことを、そのまま聞きました。いいことも、大変なことも。</p>

      <article class="voice">
        <div class="voice-head">
          <figure class="photo portrait">
            <figcaption>※本人の写真が入ります（取材時に撮影）</figcaption>
          </figure>
          <div>
            <p class="who">土木部 ｜ 2023年入社（高卒・新卒） ｜ いの町出身<b>沢田 陸（22）</b></p>
            <p class="pull">じいちゃんに「あの橋、おまえがやったがか」って言われた日のことは、たぶん一生忘れんです。</p>
          </div>
        </div>
        <dl class="qa">
          <dt>入社のきっかけは？</dt>
          <dd>正直に言うと、消去法でした。高校の求人票で「家から通える」「県外転勤なし」で絞ったら残ったのがここで。土木が何をする仕事かも、ちゃんとは分かってなかったです。</dd>
          <dt>入ってみて、想像と違ったことは？</dt>
          <dd>思ったより「頭を使う」ことです。図面どおりに側溝ひとつ据えるのも、水の流れを考えて数ミリ単位で調整する。力仕事は機械がやるので、人間の仕事は段取りと精度なんですよね。あと、先輩が思ったより優しい（笑）。怒鳴られたことは3年で一回もないです。</dd>
          <dt>いちばん印象に残っている仕事は？</dt>
          <dd>2年目に入った、町内の橋の補修工事です。完成してしばらくして、じいちゃんと車で通ったときに「あの橋、おまえがやったがか」って。地元で働くって、こういうことかと思いました。自分のやった仕事の上を、家族が通るんです。</dd>
          <dt>これから挑戦したいことは？</dt>
          <dd>今年、2級土木施工管理技士を受けます。費用は会社持ちなので、落ちたら申し訳ないっていうプレッシャーはありますけど（笑）。いつか自分が現場代理人として、後輩に段取りを教える側になりたいです。</dd>
        </dl>
      </article>

      <article class="voice">
        <div class="voice-head">
          <figure class="photo portrait">
            <figcaption>※本人の写真が入ります（取材時に撮影）</figcaption>
          </figure>
          <div>
            <p class="who">工事部 現場監督 ｜ 2020年入社（中途・Uターン） ｜ 大阪の建設会社から転職<b>中平 健吾（39）</b></p>
            <p class="pull">給料は少し下がりました。でも、夕方に子どもと仁淀川で泳げる。この差額なら、安い買い物やったと思ってます。</p>
          </div>
        </div>
        <dl class="qa">
          <dt>Uターンを決めた理由は？</dt>
          <dd>大阪で現場監督を10年やって、長男が小学校に上がるタイミングで考えました。向こうでの暮らしに不満はなかったけど、平日に子どもの顔を見た記憶がほとんどなくて。親も高知におるし、戻るなら今かなと。</dd>
          <dt>転職で不安だったことは？</dt>
          <dd>収入面と、「地方の建設会社って昭和のままなんじゃないか」という偏見です（笑）。収入は正直、大阪時代より下がりました。ただ家賃と駐車場代が半分以下になったので、手元に残るお金はほぼ変わってないです。社風のほうは、いい意味で裏切られました。工程管理はクラウドだし、休日もちゃんと取れる。</dd>
          <dt>今の仕事のやりがいは？</dt>
          <dd>都会の現場は大きいけど、自分は歯車の一枚でした。ここは町道から河川まで、規模は小さくても最初から最後まで自分の裁量で回せる。発注者の役場の人も、通行止めのお願いをする近所の人も、顔見知りなんですよ。仕事の全部に顔が見える。これは都会では味わえなかった感覚です。</dd>
          <dt>Uターン転職を考えている人へ、ひとこと。</dt>
          <dd>「地方は仕事がない」って言いますけど、少なくともこの業界は逆で、仕事はあるのに人がいない。経験者なら即戦力として迎えられるし、待遇の交渉もちゃんと聞いてもらえます。迷っているなら、一度この会社の現場を見に来たらいいと思います。仁淀川、ほんまにきれいなんで。</dd>
        </dl>
      </article>

      <article class="voice">
        <div class="voice-head">
          <figure class="photo portrait">
            <figcaption>※本人の写真が入ります（取材時に撮影）</figcaption>
          </figure>
          <div>
            <p class="who">土木部 ｜ 2017年入社（中途） ｜ 二児の母<b>岡林 美咲（38）</b></p>
            <p class="pull">子どもの行事は、早めに言えばちゃんと休める。それが当たり前じゃない職場を、前職で知っているので。</p>
          </div>
        </div>
        <dl class="qa">
          <dt>建設業で働くことに、不安はありませんでしたか？</dt>
          <dd>ありました。「休みにくそう」というイメージが強かったので。実際に入ってみると、忙しい時期はもちろんありますが、子どもの行事や家庭の用事は早めに相談すれば調整してもらえる雰囲気があります。参観日で休んで嫌な顔をされたことは、一度もないです。</dd>
          <dt>大変なところも、正直に教えてください。</dt>
          <dd>外の仕事なので、夏は暑いです。それは間違いない（笑）。雨で予定が変わることもあります。ただ、チームで声をかけ合いながら進める仕事なので、一人で抱え込む感じがないんです。誰かが無理をしそうになると、周りが気づいて止める。そういう現場です。</dd>
          <dt>長く続けられている理由は？</dt>
          <dd>自分のやった仕事が地域に残ることと、それを家族が知っていることだと思います。娘に「この道、お母さんがやったが？」と聞かれるのは、悪くないですよ。</dd>
        </dl>
      </article>

    </div>
  </section>
</main>
{footer()}
{banner("社員インタビューの取材・執筆・撮影込みで、実質負担 約6.5万円から。")}
{scripts()}'''


def page_recruit():
    return f'''{head("recruit.html", f"募集要項・応募｜{C['company']} 採用サイト（制作サンプル）",
                     "正社員（土木作業員・現場監督候補）。給与・休日・資格取得支援の詳細と応募フォーム。")}
{header("recruit.html")}
<main id="main">
  <section class="section">
    <div class="section-in">
      <p class="sec-label">RECRUIT</p>
      <h1>募集要項</h1>
      <p class="lede">新卒・中途を問わず、通年で採用しています。見学だけのご連絡も歓迎です。</p>

      {CERT}

      <table class="rq">
        <tbody>
        <tr><th>雇用形態</th><td><b class="badge">正社員</b>期間の定めなし（試用期間3ヶ月・待遇変更なし）</td></tr>
        <tr><th>募集職種</th><td>① 土木作業員（未経験可）<br>② 現場監督・現場監督候補（経験者優遇）</td></tr>
        <tr><th>勤務地</th><td><b class="badge">高知県内</b>本社（{C["address"]}）および いの町・高知市周辺の各現場<br>※県外転勤・長期出張なし</td></tr>
        <tr><th>勤務時間</th><td>7:30〜17:00<br>（実働7時間30分／休憩計120分：午前30分・昼60分・午後30分）</td></tr>
        <tr><th>時間外労働</th><td>月平均10時間 ※工期前でも19時を超えることはほぼありません</td></tr>
        <tr><th>給与</th><td>① 月給21万〜28万円<br>② 月給26万〜38万円<br>※経験・資格を考慮のうえ決定／昇給年1回・賞与年2回（昨年実績 計3.2ヶ月）</td></tr>
        <tr><th>諸手当</th><td>資格手当（例：1級土木施工管理技士 月2万円）、家族手当、通勤手当、現場手当</td></tr>
        <tr><th>休日休暇</th><td>週休二日制（4週8休）・日曜完全休／年間休日105日／夏季・年末年始／有給取得率78%（昨年実績）</td></tr>
        <tr><th>応募資格</th><td>普通自動車免許（AT限定可）<br>※建設業の経験・資格は不問。経験者・有資格者は給与にて優遇します</td></tr>
        <tr><th>福利厚生</th><td>社会保険完備、退職金制度、資格取得費用の全額会社負担、作業着・安全靴支給、マイカー通勤可（駐車場あり）、健康診断（年1回）</td></tr>
        <tr><th>選考の流れ</th><td>応募 → 会社・現場見学（希望者） → 面接1回 → 内定<br>※履歴書は面接時で構いません</td></tr>
        </tbody>
      </table>
    </div>
  </section>

  <section class="section">
    <div class="section-in">
      <p class="sec-label">WHO WE WANT</p>
      <h2>経験より、人柄を見ています</h2>
      <p class="lede">あいさつができること。時間を守れること。分からないことを、分からないと言えること。採用で見ているのは、ほとんどそれだけです。体を動かす仕事が好きな方、地元で長く働きたい方、手に職をつけたい方。建設業の経験がなくても、入社後に少しずつ覚えていけば大丈夫です。</p>
    </div>
  </section>

  <section class="section tint">
    <div class="section-in">
      <p class="sec-label">ENTRY</p>
      <h2>応募・見学のお申し込み</h2>
      <p class="lede">2営業日以内に、採用担当からご連絡します。「少し気になる」「まずは話だけ聞いてみたい」「未経験でも大丈夫か相談したい」——その段階のご連絡こそ歓迎です。お急ぎの方は<a href="tel:{C["tel_link"]}">お電話（{C["tel"]}・{C["tel_hours"]}）</a>でもどうぞ。</p>

      <form class="form" id="entryForm">
        <div class="row">
          <label for="f-name">お名前<span class="req">必須</span></label>
          <input id="f-name" type="text" name="name" autocomplete="name" placeholder="例）高知 太郎" required>
        </div>
        <div class="row">
          <label for="f-tel">お電話番号<span class="req">必須</span></label>
          <input id="f-tel" type="tel" name="tel" autocomplete="tel" placeholder="例）090-0000-0000" required>
        </div>
        <div class="row">
          <label for="f-type">ご希望<span class="req">必須</span></label>
          <select id="f-type" name="type" required>
            <option value="">選択してください</option>
            <option>応募したい（土木作業員）</option>
            <option>応募したい（現場監督・候補）</option>
            <option>まずは会社・現場を見学したい</option>
            <option>質問したい</option>
          </select>
        </div>
        <div class="row">
          <label for="f-msg">メッセージ（任意）</label>
          <textarea id="f-msg" name="message" rows="4" placeholder="ご質問やご希望の連絡時間帯などがあればご記入ください"></textarea>
        </div>
        <button type="submit">この内容で送信する</button>
        <p class="fine">※これは制作サンプルです。送信ボタンの動作だけ、実物と同じようにお試しいただけます。</p>
      </form>

      <div class="thanks" id="thanks" tabindex="-1" role="status" hidden>
        <p class="thanks-mark" aria-hidden="true">✓</p>
        <h3>送信を受け付けました</h3>
        <p>2営業日以内に、採用担当からご連絡します。<br>
           お急ぎの場合は <a href="tel:{C["tel_link"]}">{C["tel"]}</a>（{C["tel_hours"]}）へ。</p>
        <p class="fine">※これは制作サンプルのため、実際にはメールは送信されていません。<br>
           実案件では、この内容が採用担当者のメールに即時届き、応募件数が自動で記録されます（補助金の実績報告にそのまま使えます）。</p>
        <button type="button" id="reAgain" class="ghost">もう一度フォームを見る</button>
      </div>
    </div>
  </section>
</main>
{footer()}
{banner("応募フォームと応募数の自動記録まで込みで、実質負担 約6.5万円から。")}
{scripts()}'''


def page_about():
    S = SUBSIDY
    return f'''{head("about.html", f"採用サイト制作のご案内｜{SM['name']}",
                     f"高知県の補助金を活用した、WLB認証企業向けの採用サイト制作。料金・制作の流れ・よくある質問。")}
<header class="site-header sm">
  <div class="header-in">
    <a class="brand" href="{SM["url"]}" aria-label="{SM["name"]}">
      <svg class="brand-mark" viewBox="0 0 40 40" aria-hidden="true">
        <rect width="40" height="40" rx="9" fill="{BRAND['accent']}"/>
        <path d="M20 8l4 8 8-2-5 7 5 7-8-2-4 8-4-8-8 2 5-7-5-7 8 2z" fill="{BRAND['accent_ink']}" opacity=".85"/>
      </svg>
      <span class="brand-name">{SM["name"]}<small>WEB / 取材・執筆</small></span>
    </a>
    <nav class="gnav" aria-label="サイト内メニュー">
      <a href="index.html">← サンプルに戻る</a>
    </nav>
  </div>
</header>

<main id="main">
  <section class="section sm-hero">
    <div class="section-in">
      <p class="sec-label">FOR EMPLOYERS</p>
      <h1>求人票では、もう人は来ません。</h1>
      <p class="lede">いま見ていただいたのは、{SM["name"]}が制作した採用サイトのサンプルです。
        架空の建設会社を題材に、取材から執筆・撮影・デザイン・応募フォームまで、実際にお納めするものと同じ内容で作りました。<br>
        高知県の補助金（{S["name"]}）を使えば、この4ページ構成のサイトを
        <b class="hl">実質のご負担 約{S["net"]}円</b>から制作できます。</p>
      <div class="hero-cta">
        <a class="btn btn-accent" href="#contact">まず相談してみる</a>
        <a class="btn btn-line" href="#price">料金と補助金を見る</a>
      </div>
    </div>
  </section>
  {RIVER}

  <section class="section" id="price">
    <div class="section-in">
      <p class="sec-label">PRICE</p>
      <h2>料金と、補助金の内訳</h2>
      <!-- ★★★ 要確認 ★★★
           下の金額・補助率・上限は仮のプレースホルダーです。
           必ず最新の交付要綱で確認し、実数に差し替えてから公開すること。 -->
      <table class="rq price">
        <tbody>
        <tr><th>制作費（4ページ／取材・撮影／応募フォーム設置）</th><td class="num">{S["price"]} 円</td></tr>
        <tr><th>{S["name"]}<br><small>補助率 {S["rate"]}・上限 {S["cap"]}</small></th><td class="num minus">− {S["grant"]} 円</td></tr>
        <tr class="total"><th>実質のご負担</th><td class="num">約 {S["net"]} 円</td></tr>
        </tbody>
      </table>
      <p class="note">※補助金は<b>採択が前提</b>です。不採択となった場合は、着手前であればキャンセル（費用ゼロ）、着手後は制作費のみをご請求します。申請前に必ずご説明します。<br>
        ※補助率・上限額・対象経費は年度により変わります。ご相談時点の最新の要綱でご案内します。</p>
    </div>
  </section>

  <section class="section tint">
    <div class="section-in">
      <p class="sec-label">WHAT'S INCLUDED</p>
      <h2>含まれるもの／含まれないもの</h2>
      <div class="two">
        <div class="incl">
          <h3>含まれます</h3>
          <ul>
            <li>取材（半日・1回／御社と現場へお伺いします）</li>
            <li>原稿の執筆（社員インタビュー3本・代表メッセージ・仕事内容）</li>
            <li>写真撮影（現場・社員・代表）</li>
            <li>デザイン・コーディング（4ページ／スマホ対応）</li>
            <li>応募フォームの設置と、応募数の自動記録</li>
            <li>Googleしごと検索（求人の構造化データ）への対応</li>
            <li>補助金の申請書類・実績報告のサポート</li>
            <li>公開後1ヶ月の修正対応</li>
          </ul>
        </div>
        <div class="excl">
          <h3>含まれません（別途）</h3>
          <ul>
            <li>独自ドメイン代・サーバー代（年 1万円前後）</li>
            <li>公開2ヶ月目以降の更新・追加ページ</li>
            <li>ロゴの新規制作</li>
            <li>求人媒体への出稿費</li>
            <li>取材が2回以上になる場合の追加取材費</li>
          </ul>
        </div>
      </div>
    </div>
  </section>
  {RIVER_UP}

  <section class="section">
    <div class="section-in">
      <p class="sec-label">FLOW</p>
      <h2>制作の流れ</h2>
      <p class="lede">御社にお願いすることは、<b>取材の半日</b>と、<b>原稿の確認</b>だけです。書類づくりも文章も、こちらで用意します。</p>
      <ol class="tl flow">
        <li><time>STEP 1</time><b>ご相談・お見積り（無料）</b><p>お電話かメールで。「補助金が使えるか知りたい」だけのご連絡でかまいません。認証の有無と要件を、こちらで確認します。</p></li>
        <li><time>STEP 2</time><b>補助金の申請（約2週間）</b><p>申請書類はこちらで作成し、御社には押印と提出だけをお願いします。</p></li>
        <li><time>STEP 3</time><b>取材・撮影（半日・1回）</b><p>代表と社員3名にお話を伺い、現場と事務所で撮影します。事前準備は不要です。</p></li>
        <li><time>STEP 4</time><b>初稿のご確認（取材から約2週間）</b><p>実際に動くサイトの形でお見せします。文章・写真の差し替えは、ここで何度でも。</p></li>
        <li><time>STEP 5</time><b>公開</b><p>ご相談から、おおむね2ヶ月で公開できます。</p></li>
        <li><time>STEP 6</time><b>実績報告のサポート</b><p>応募数のデータをお渡しし、報告書の作成までお手伝いします。</p></li>
      </ol>
    </div>
  </section>

  <section class="section tint">
    <div class="section-in">
      <p class="sec-label">Q&amp;A</p>
      <h2>よくあるご質問</h2>
      <div class="faq">
        <details>
          <summary>{S["requirement"]}を持っていないと使えませんか？</summary>
          <p>補助金の要件になっている場合があります。まだ認証を受けていない場合も、認証の取得から並行してご相談いただけます。まずは現状をお聞かせください。</p>
        </details>
        <details>
          <summary>補助金は必ず通りますか？</summary>
          <p>採択を保証することはできません。ですので、不採択の場合は着手前であればキャンセル（費用ゼロ）としています。この条件は契約書に明記します。</p>
        </details>
        <details>
          <summary>写真は誰が撮るのですか？</summary>
          <p>私が取材と一緒に撮影します。カメラマンの手配は不要です。素材写真を買って並べるのではなく、御社の現場と社員の顔で作るのが、この仕事のいちばん大事なところだと思っています。</p>
        </details>
        <details>
          <summary>社員インタビューを、うちの社員が嫌がりそうです。</summary>
          <p>よくあるご相談です。取材は1人30分ほど、雑談の延長のような形で進めます。原稿は必ずご本人に確認していただき、載せたくない部分は削ります。顔出しなしのご希望にも対応します。</p>
        </details>
        <details>
          <summary>すでにホームページがあります。作り直しになりますか？</summary>
          <p>いいえ。既存サイトはそのままに、採用に特化したページを新しく足す形が一般的です。既存サイトからリンクを1本張っていただくだけで済みます。</p>
        </details>
        <details>
          <summary>公開後、自分たちで更新できますか？</summary>
          <p>募集要項の数字など、変更が起きやすい箇所については、更新の方法をお渡しします。それでも難しい場合は、月額の保守（別途）でお引き受けします。</p>
        </details>
        <details>
          <summary>本当に応募が増えるのですか？</summary>
          <p>サイトを作っただけで応募が来る、とは申し上げません。効くのは「求人票に書けない情報が、外から見える」ことです。ハローワークの求人票、ロゴ入り封筒、チラシ、SNS——あらゆる接点からこのサイトへ誘導して、はじめて機能します。その導線の設計まで含めてご提案します。</p>
        </details>
      </div>
    </div>
  </section>

  <section class="section" id="contact">
    <div class="section-in">
      <p class="sec-label">CONTACT</p>
      <h2>まずは、話だけでも</h2>
      <p class="lede">「補助金が使えるか確認したい」「見積もりだけ欲しい」——その段階のご連絡を歓迎します。売り込みの電話はいたしません。</p>
      <div class="contact">
        <a class="contact-card" href="mailto:{SM["mail"]}?subject=%E6%8E%A1%E7%94%A8%E3%82%B5%E3%82%A4%E3%83%88%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6">
          <span class="ct-label">メールで相談する</span>
          <b>{SM["mail"]}</b>
          <span class="ct-note">24時間受付・2営業日以内に返信します</span>
        </a>
        <div class="contact-card static">
          <span class="ct-label">担当</span>
          <b>{SM["name"]}　{SM["person"]}</b>
          <span class="ct-note">高知県吾川郡いの町／取材・執筆歴6年。<br>Web制作と、中小企業の業務自動化を手がけています。</span>
        </div>
      </div>
    </div>
  </section>
</main>

<footer class="site-footer">
  <div class="footer-in">
    <p class="fbrand">{SM["name"]}</p>
    <p>高知県吾川郡いの町 ｜ <a href="mailto:{SM["mail"]}">{SM["mail"]}</a> ｜ <a href="{SM["url"]}">{SM["url"]}</a><br>
       事業内容：取材・執筆／Webサイト制作／業務自動化（GAS・AI）の導入支援</p>
    <p class="disclaimer">本サイト内の「{C["company"]}」は、制作サンプルのための架空の企業です。
      社名・人物・数値はすべて架空のものであり、実在の企業・団体・人物とは関係ありません。<br>
      補助金の金額・補助率・要件は年度により変わります。記載は目安であり、ご相談時点の最新の要綱でご案内します。</p>
  </div>
</footer>
{scripts()}'''


# ============================================================
# CSS
# ============================================================
def build_css():
    B = BRAND
    return f'''/* ============================================================
   {C["company"]}（架空）採用サイト ― 制作サンプル
   Studio Maple demo / mobile-first
   色は :root だけ差し替えれば、サイト全体に反映されます。
   ============================================================ */
:root{{
  --ink:{B["ink"]};
  --primary:{B["primary"]};
  --primary-deep:{B["primary_deep"]};
  --mist:{B["mist"]};
  --paper:{B["paper"]};
  --text:{B["text"]};
  --muted:{B["muted"]};          /* WCAG AA適合（mist背景で4.82:1） */
  --accent:{B["accent"]};
  --accent-ink:{B["accent_ink"]};
  --line:{B["line"]};
  --pale:{B["hero_pale"]};
  --disp:"Zen Kaku Gothic New","Noto Sans JP",sans-serif;
  --body:"Noto Sans JP",sans-serif;
}}
*{{margin:0;padding:0;box-sizing:border-box}}
html{{scroll-behavior:smooth}}
@media (prefers-reduced-motion: reduce){{
  html{{scroll-behavior:auto}}
  *,*::before,*::after{{animation:none!important;transition:none!important;scroll-behavior:auto!important}}
}}
body{{
  font-family:var(--body);
  color:var(--text);
  background:var(--paper);
  line-height:1.9;
  font-size:15px;
  -webkit-font-smoothing:antialiased;
}}
body.has-banner{{padding-bottom:var(--banner-h,72px)}}
img,svg{{max-width:100%;display:block}}
a{{color:var(--primary-deep)}}
a:focus-visible,button:focus-visible,summary:focus-visible,
input:focus-visible,select:focus-visible,textarea:focus-visible{{
  outline:3px solid var(--accent);outline-offset:2px;
}}
[hidden]{{display:none!important}}

/* ---------- skip link ---------- */
.skip{{
  position:absolute;left:12px;top:-60px;z-index:200;
  background:var(--ink);color:#fff;text-decoration:none;
  padding:10px 18px;border-radius:0 0 10px 10px;font-weight:700;font-size:13px;
  transition:top .15s ease;
}}
.skip:focus{{top:0}}

/* ---------- header ---------- */
.site-header{{
  position:sticky;top:0;z-index:50;
  background:rgba(250,252,252,.93);backdrop-filter:blur(8px);
  border-bottom:1px solid var(--line);
}}
.header-in{{max-width:960px;margin:0 auto;padding:10px 20px;display:flex;align-items:center;justify-content:space-between;gap:12px}}
.brand{{display:flex;align-items:center;gap:10px;text-decoration:none;color:var(--ink)}}
.brand-mark{{width:34px;height:34px;flex:none}}
.brand-name{{font-family:var(--disp);font-weight:900;font-size:16px;letter-spacing:.04em;line-height:1.25}}
.brand-name small{{display:block;font-size:9.5px;font-weight:500;color:var(--muted);letter-spacing:.2em}}
.gnav{{display:flex;gap:4px;flex-wrap:wrap}}
.gnav a{{
  text-decoration:none;font-size:13px;font-weight:700;color:var(--ink);
  padding:7px 10px;border-radius:999px;
}}
.gnav a[aria-current="page"]{{background:var(--mist);color:var(--primary-deep)}}
.gnav a.nav-cta{{background:var(--accent);color:var(--accent-ink)}}

/* ---------- hero ---------- */
.hero{{position:relative;background:var(--ink);color:#f2fafc;overflow:hidden}}
.hero-scene{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.9}}
.hero-in{{position:relative;max-width:960px;margin:0 auto;padding:88px 24px 96px}}
.hero .eyebrow{{font-size:12px;letter-spacing:.26em;color:var(--pale);font-weight:700;margin-bottom:18px}}
.hero h1{{
  font-family:var(--disp);font-weight:900;font-size:clamp(28px,6.4vw,46px);
  line-height:1.5;letter-spacing:.02em;text-wrap:balance;color:#f2fafc;
}}
.hero p{{margin-top:18px;max-width:34em;font-size:15px;color:#d6ecf1}}
.hero-cta{{margin-top:28px;display:flex;gap:12px;flex-wrap:wrap}}
.btn{{
  display:inline-block;text-decoration:none;font-family:var(--disp);font-weight:900;
  font-size:14.5px;letter-spacing:.06em;padding:13px 26px;border-radius:999px;
}}
.btn-accent{{background:var(--accent);color:var(--accent-ink)}}
.btn-ghost{{border:1.5px solid #8fc6d3;color:#eaf7fa}}
.btn-line{{border:1.5px solid var(--line);color:var(--primary-deep);background:#fff}}

/* ---------- river divider ---------- */
.river{{display:block;width:100%;height:34px;color:var(--paper)}}
.river.on-mist{{color:var(--mist)}}

/* ---------- sections ---------- */
.section{{padding:56px 20px}}
.section.tint{{background:var(--mist)}}
.section-in{{max-width:880px;margin:0 auto}}
.sec-label{{
  display:inline-flex;align-items:center;gap:8px;
  font-size:12px;font-weight:700;letter-spacing:.22em;color:var(--primary-deep);margin-bottom:10px;
}}
.sec-label::before{{content:"";width:26px;height:2px;background:var(--primary);border-radius:2px}}
h1,h2{{font-family:var(--disp);font-weight:900;color:var(--ink);line-height:1.55;letter-spacing:.02em}}
main h1{{font-size:clamp(23px,5vw,31px);margin-bottom:18px}}
h2{{font-size:clamp(21px,4.6vw,28px);margin-bottom:18px}}
.lede{{max-width:38em}}
.hl{{color:var(--primary-deep)}}

/* ---------- stats ---------- */
.stats{{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin-top:26px}}
@media(min-width:640px){{.stats{{grid-template-columns:repeat(4,1fr)}}}}
.stat{{background:#fff;border:1px solid var(--line);border-radius:12px;padding:16px 14px;text-align:center}}
.stat b{{font-family:var(--disp);font-weight:900;font-size:27px;color:var(--primary-deep);display:block;line-height:1.3}}
.stat b small{{font-size:13px}}
.stat span{{font-size:12px;color:var(--muted)}}

/* ---------- WLB認証バッジ ---------- */
.cert{{
  display:flex;gap:16px;align-items:flex-start;
  margin-top:26px;padding:18px 18px;
  background:#fff;border:1px solid var(--line);border-left:5px solid var(--primary);
  border-radius:0 12px 12px 0;
}}
.cert-mark{{width:52px;height:52px;flex:none}}
.cert-name{{font-family:var(--disp);font-weight:900;font-size:15px;color:var(--ink);line-height:1.5}}
.cert-note{{font-size:13px;color:var(--muted);margin-top:5px}}

/* ---------- cards ---------- */
.cards{{display:grid;gap:14px;margin-top:26px}}
@media(min-width:640px){{.cards{{grid-template-columns:repeat(3,1fr)}}}}
.card{{
  background:#fff;border:1px solid var(--line);border-radius:14px;padding:20px 18px;
  text-decoration:none;color:var(--text);display:block;
  transition:transform .18s ease, box-shadow .18s ease;
}}
.card:hover{{transform:translateY(-3px);box-shadow:0 10px 24px rgba(18,51,61,.10)}}
.card.static:hover{{transform:none;box-shadow:none}}
.card h3{{font-family:var(--disp);font-weight:900;font-size:17px;color:var(--ink);margin:0 0 8px}}
.card p{{font-size:13.5px;color:var(--muted)}}
.card .more{{display:inline-block;margin-top:12px;font-size:13px;font-weight:700;color:var(--primary-deep)}}

/* ---------- photo placeholder ---------- */
.photo{{
  position:relative;border-radius:14px;overflow:hidden;
  background:linear-gradient(135deg,#bcdde6 0%, #7fb8c8 55%, #4f93a8 100%);
  aspect-ratio:16/9;display:flex;align-items:flex-end;
}}
.photo.portrait{{aspect-ratio:4/5}}
.photo::before{{
  content:"";position:absolute;inset:0;
  background:
    radial-gradient(120% 60% at 20% 10%, rgba(255,255,255,.5), transparent 60%),
    repeating-linear-gradient(-8deg, transparent 0 26px, rgba(255,255,255,.16) 26px 28px);
}}
.photo figcaption{{
  position:relative;width:100%;font-size:11.5px;color:#0c3a47;
  background:rgba(250,252,252,.85);padding:6px 12px;
}}

/* ---------- timeline ---------- */
.tl{{list-style:none;margin-top:26px;border-left:3px solid var(--primary);padding-left:0}}
.tl li{{position:relative;padding:0 0 22px 26px}}
.tl li::before{{
  content:"";position:absolute;left:-8px;top:8px;width:13px;height:13px;border-radius:50%;
  background:var(--paper);border:3px solid var(--primary);
}}
.section.tint .tl li::before{{background:var(--mist)}}
.tl time{{font-family:var(--disp);font-weight:900;color:var(--primary-deep);font-size:15px;letter-spacing:.05em;display:block}}
.tl.flow time{{font-size:12.5px;letter-spacing:.14em}}
.tl b{{font-size:15px;color:var(--ink)}}
.tl p{{font-size:13.5px;color:var(--muted);margin-top:2px;max-width:36em}}

/* ---------- steps ---------- */
.steps{{display:grid;gap:14px;margin-top:26px}}
@media(min-width:640px){{.steps{{grid-template-columns:repeat(3,1fr)}}}}
.step{{background:#fff;border-top:4px solid var(--primary);border-radius:0 0 12px 12px;
  box-shadow:0 1px 0 var(--line), 0 6px 18px rgba(18,51,61,.05);padding:18px 16px}}
.step.plain{{border-top-color:var(--accent)}}
.step .yr{{font-family:var(--disp);font-weight:900;color:var(--primary);font-size:13px;letter-spacing:.1em}}
.step h3{{font-family:var(--disp);font-weight:900;font-size:16px;color:var(--ink);margin:4px 0 8px}}
.step p{{font-size:13.5px;color:var(--muted)}}

/* ---------- FAQ ---------- */
.faq{{margin-top:26px;display:grid;gap:10px}}
.faq details{{background:#fff;border:1px solid var(--line);border-radius:12px}}
.faq summary{{
  cursor:pointer;list-style:none;display:flex;gap:10px;align-items:baseline;
  font-weight:700;color:var(--ink);font-size:14.5px;padding:14px 16px;
}}
.faq summary::-webkit-details-marker{{display:none}}
.faq summary::before{{content:"Q";font-family:var(--disp);font-weight:900;color:var(--accent);flex:none}}
.faq details p{{padding:0 16px 14px 38px;font-size:14px;color:var(--muted)}}
.faq details[open] summary{{color:var(--primary-deep)}}

/* ---------- interview ---------- */
.voice{{background:#fff;border:1px solid var(--line);border-radius:16px;padding:24px 20px;margin-top:28px}}
@media(min-width:720px){{.voice{{padding:32px 30px}}}}
.voice-head{{display:grid;gap:18px;margin-bottom:8px}}
@media(min-width:640px){{.voice-head{{grid-template-columns:180px 1fr;align-items:end}}}}
.voice .who{{font-size:13px;color:var(--muted)}}
.voice .who b{{display:block;font-family:var(--disp);font-weight:900;font-size:19px;color:var(--ink);letter-spacing:.04em}}
.pull{{
  font-family:var(--disp);font-weight:700;font-size:clamp(18px,4.2vw,23px);
  line-height:1.85;color:var(--primary-deep);margin:14px 0 6px;text-wrap:balance;
}}
.pull::before{{content:"\\201C";color:var(--accent)}}
.pull::after{{content:"\\201D";color:var(--accent)}}
.qa{{margin-top:16px}}
.qa dt{{font-weight:700;color:var(--ink);font-size:14.5px;margin-top:16px;padding-left:1.4em;text-indent:-1.4em}}
.qa dt::before{{content:"― ";color:var(--primary)}}
.qa dd{{font-size:14.5px;margin-top:6px}}

/* ---------- 要項テーブル（モバイルで縦積み） ---------- */
.rq{{width:100%;border-collapse:collapse;margin-top:26px;background:#fff;
  border:1px solid var(--line);border-radius:14px;overflow:hidden;font-size:14.5px}}
.rq th,.rq td{{padding:13px 15px;vertical-align:top;text-align:left}}
.rq th{{background:var(--mist);color:var(--ink);font-size:13px;letter-spacing:.03em;font-weight:700}}
.rq td b.badge{{
  display:inline-block;background:var(--primary-deep);color:#fff;border-radius:6px;
  font-size:12.5px;padding:2px 9px;margin-right:8px;font-weight:700;
}}
/* モバイル：縦積み */
@media(max-width:599px){{
  .rq,.rq tbody,.rq tr,.rq th,.rq td{{display:block;width:100%}}
  .rq tr{{border-bottom:1px solid var(--line)}}
  .rq tr:last-child{{border-bottom:none}}
  .rq th{{padding:10px 15px 6px;border-radius:0}}
  .rq td{{padding:10px 15px 16px}}
}}
/* デスクトップ：2カラム */
@media(min-width:600px){{
  .rq th{{width:32%;border-bottom:1px solid var(--line)}}
  .rq td{{border-bottom:1px solid var(--line)}}
  .rq tr:last-child th,.rq tr:last-child td{{border-bottom:none}}
}}
/* 料金表 */
.rq.price td.num{{font-family:var(--disp);font-weight:900;font-size:17px;color:var(--ink);white-space:nowrap}}
.rq.price td.minus{{color:var(--primary-deep)}}
.rq.price th small{{display:block;font-weight:400;color:var(--muted);font-size:12px;margin-top:2px}}
.rq.price tr.total th{{background:var(--ink);color:#fff}}
.rq.price tr.total td{{background:#fff8e9}}
.rq.price tr.total td.num{{font-size:21px;color:#8a5b00}}
.note{{margin-top:14px;font-size:13px;color:var(--muted);background:var(--mist);
  border-radius:10px;padding:14px 16px}}

/* ---------- 含まれる / 含まれない ---------- */
.two{{display:grid;gap:16px;margin-top:26px}}
@media(min-width:720px){{.two{{grid-template-columns:1fr 1fr}}}}
.two > div{{background:#fff;border:1px solid var(--line);border-radius:14px;padding:20px 18px}}
.two h3{{font-family:var(--disp);font-weight:900;font-size:16px;color:var(--ink);margin-bottom:12px}}
.two ul{{list-style:none}}
.two li{{position:relative;padding-left:24px;font-size:14px;margin-bottom:8px;line-height:1.7}}
.incl li::before{{content:"✓";position:absolute;left:0;top:0;color:var(--primary);font-weight:900}}
.excl li{{color:var(--muted)}}
.excl li::before{{content:"−";position:absolute;left:2px;top:0;color:var(--muted);font-weight:900}}

/* ---------- form ---------- */
.form{{margin-top:30px;background:#fff;border:1px solid var(--line);border-radius:16px;padding:22px 20px}}
.form .row{{margin-bottom:16px}}
.form label{{display:block;font-weight:700;font-size:13.5px;color:var(--ink);margin-bottom:6px}}
.form label .req{{color:#b0620a;font-size:11.5px;margin-left:6px;font-weight:700}}
.form input,.form select,.form textarea{{
  width:100%;border:1.5px solid var(--line);border-radius:10px;background:var(--paper);
  padding:11px 12px;font:inherit;font-size:16px;color:var(--text);
}}
.form input:focus,.form select:focus,.form textarea:focus{{border-color:var(--primary)}}
.form input:user-invalid,.form select:user-invalid{{border-color:#c0392b}}
.form button{{
  width:100%;border:none;cursor:pointer;background:var(--accent);color:var(--accent-ink);
  font-family:var(--disp);font-weight:900;font-size:15.5px;letter-spacing:.08em;
  padding:15px;border-radius:999px;
}}
.form .fine{{font-size:12.5px;color:var(--muted);margin-top:12px}}

/* ---------- 送信完了（擬似） ---------- */
.thanks{{
  margin-top:30px;background:#fff;border:2px solid var(--primary);border-radius:16px;
  padding:30px 22px;text-align:center;
}}
.thanks:focus{{outline:none}}
.thanks-mark{{
  width:54px;height:54px;margin:0 auto 14px;border-radius:50%;
  background:var(--primary);color:#fff;
  font-size:27px;line-height:54px;font-weight:900;
}}
.thanks h3{{font-family:var(--disp);font-weight:900;font-size:20px;color:var(--ink);margin-bottom:10px}}
.thanks p{{font-size:14.5px}}
.thanks .fine{{
  margin-top:18px;padding-top:14px;border-top:1px dashed var(--line);
  text-align:left;font-size:12.5px;color:var(--muted);
}}
.thanks .ghost{{
  margin-top:18px;background:none;border:1.5px solid var(--line);color:var(--muted);
  border-radius:999px;padding:10px 22px;font:inherit;font-size:13px;cursor:pointer;
}}

/* ---------- message ---------- */
.message{{display:grid;gap:22px;margin-top:26px}}
@media(min-width:720px){{.message{{grid-template-columns:240px 1fr}}}}
.message p + p{{margin-top:12px}}
.message .sign{{font-size:13.5px;color:var(--muted);margin-top:18px}}
.message .sign b{{font-family:var(--disp);font-weight:900;color:var(--ink);font-size:16px;margin-left:8px}}

/* ---------- about（スタジオメイプル面） ---------- */
.site-header.sm{{border-bottom:2px solid var(--accent)}}
.sm-hero{{background:var(--mist);padding-top:48px;padding-bottom:48px}}
.sm-hero .lede{{max-width:40em;font-size:15px}}
.sm-hero .hero-cta{{margin-top:26px;display:flex;gap:12px;flex-wrap:wrap}}
.contact{{display:grid;gap:14px;margin-top:26px}}
@media(min-width:720px){{.contact{{grid-template-columns:1fr 1fr}}}}
.contact-card{{
  display:block;background:#fff;border:1px solid var(--line);border-radius:14px;
  padding:20px 18px;text-decoration:none;color:var(--text);
  transition:transform .18s ease, box-shadow .18s ease;
}}
.contact-card:not(.static):hover{{transform:translateY(-3px);box-shadow:0 10px 24px rgba(18,51,61,.10)}}
.contact-card .ct-label{{display:block;font-size:12px;letter-spacing:.16em;color:var(--muted);font-weight:700}}
.contact-card b{{display:block;font-family:var(--disp);font-weight:900;font-size:17px;color:var(--ink);
  margin:6px 0 8px;word-break:break-all}}
.contact-card .ct-note{{display:block;font-size:13px;color:var(--muted)}}

/* ---------- footer ---------- */
.site-footer{{background:var(--ink);color:#c7dfe6;padding:40px 20px 32px;font-size:13px}}
.footer-in{{max-width:880px;margin:0 auto}}
.site-footer a{{color:#a8d8e4}}
.site-footer .fbrand{{font-family:var(--disp);font-weight:900;color:#fff;font-size:16px;margin-bottom:8px}}
.site-footer .disclaimer{{
  margin-top:18px;padding:12px 14px;border:1px dashed #4d7684;border-radius:10px;
  color:#a9ccd6;line-height:1.8;font-size:12.5px;
}}

/* ---------- 制作サンプルの固定バナー ---------- */
.sample-banner{{
  position:fixed;left:0;right:0;bottom:0;z-index:100;
  background:#2c2418;color:#fff;
  display:flex;align-items:center;justify-content:center;gap:8px 12px;flex-wrap:wrap;
  padding:10px 14px;font-size:12.5px;line-height:1.5;text-align:center;
  box-shadow:0 -4px 16px rgba(0,0,0,.18);
}}
.sample-banner .tag{{
  background:var(--accent);color:var(--accent-ink);font-weight:900;font-family:var(--disp);
  border-radius:6px;padding:2px 8px;font-size:11.5px;flex:none;
}}
.sample-banner .msg{{color:#e8ddc9}}
.sample-banner .banner-cta{{
  background:#fff;color:#2c2418;font-weight:900;font-family:var(--disp);
  text-decoration:none;border-radius:999px;padding:6px 16px;font-size:12.5px;flex:none;
}}
@media(max-width:480px){{
  .sample-banner{{gap:6px 8px;padding:9px 12px}}
  .sample-banner .msg{{width:100%;order:3;font-size:11.5px}}
}}
'''


# ============================================================
# JS
# ============================================================
SITE_JS = '''/* ============================================================
   site.js ― Studio Maple demo
   ① 流入経路（?src=）を保持して、問い合わせ導線に引き継ぐ
   ② 固定バナーの高さぶんだけ body の下余白を確保する
   ③ 応募フォームの擬似送信（完了画面の表示）
   ============================================================ */
(function () {
  'use strict';

  /* ---------- ① 流入経路の保持 ---------- */
  var KEY = 'sm_src';
  var q = new URLSearchParams(location.search).get('src');
  if (q) { try { sessionStorage.setItem(KEY, q); } catch (e) {} }

  var src = q;
  if (!src) { try { src = sessionStorage.getItem(KEY); } catch (e) {} }
  if (!src) src = 'direct';

  // サイト内リンクに src を引き継ぐ（回遊しても経路が消えない）
  document.querySelectorAll('a[href$=".html"]').forEach(function (a) {
    var href = a.getAttribute('href');
    if (!href || href.indexOf('//') === 0 || /^https?:/i.test(href)) return;
    var u = new URL(href, location.href);
    u.searchParams.set('src', src);
    a.setAttribute('href', u.pathname.split('/').pop() + u.search + u.hash);
  });

  // 外部リンク（studiomaple.jp）に src を付与
  document.querySelectorAll('a[href*="studiomaple.jp"]').forEach(function (a) {
    try {
      var u = new URL(a.href);
      u.searchParams.set('src', src);
      a.href = u.toString();
    } catch (e) {}
  });

  // mailto の本文に経路を埋め込む（＝届いたメールを見れば経路がわかる）
  document.querySelectorAll('a[href^="mailto:"]').forEach(function (a) {
    var sep = a.getAttribute('href').indexOf('?') > -1 ? '&' : '?';
    a.setAttribute('href', a.getAttribute('href') + sep +
      'body=' + encodeURIComponent('\\n\\n----------\\n参照元：' + src + '（自動付与）'));
  });

  // GA4 を入れる場合はここで送る
  // if (window.gtag) gtag('event', 'demo_view', { src: src });

  /* ---------- ② 固定バナーの高さを body に反映 ---------- */
  var banner = document.querySelector('.sample-banner');
  if (banner) {
    document.body.classList.add('has-banner');
    var sync = function () {
      document.body.style.setProperty('--banner-h', banner.offsetHeight + 8 + 'px');
    };
    sync();
    window.addEventListener('resize', sync);
    if (window.ResizeObserver) new ResizeObserver(sync).observe(banner);
  }

  /* ---------- ③ 応募フォームの擬似送信 ---------- */
  var form = document.getElementById('entryForm');
  var thanks = document.getElementById('thanks');
  if (form && thanks) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();          // 実送信はしない（required でブラウザが先に検証する）
      form.hidden = true;
      thanks.hidden = false;
      thanks.scrollIntoView({ block: 'center', behavior: 'smooth' });
      thanks.focus();
    });
    var again = document.getElementById('reAgain');
    if (again) {
      again.addEventListener('click', function () {
        thanks.hidden = true;
        form.hidden = false;
        form.reset();
        form.scrollIntoView({ block: 'center', behavior: 'smooth' });
      });
    }
  }
})();
'''


# ============================================================
def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)

    pages = {
        "index.html":   page_index(),
        "work.html":    page_work(),
        "voices.html":  page_voices(),
        "recruit.html": page_recruit(),
        "about.html":   page_about(),
    }
    for name, content in pages.items():
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            f.write(content)

    with open(os.path.join(OUT, "style.css"), "w", encoding="utf-8") as f:
        f.write(build_css())
    with open(os.path.join(OUT, "site.js"), "w", encoding="utf-8") as f:
        f.write(SITE_JS)

    print("built:", ", ".join(sorted(os.listdir(OUT))))


if __name__ == "__main__":
    main()
