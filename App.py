from flask import Flask, render_template_string

app = Flask(__name__)

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>GameVerse — 3 Games</title>
  <link href="https://fonts.googleapis.com/css2?family=Fredoka+One&family=Nunito:wght@400;600;700;800&display=swap" rel="stylesheet"/>

  <style>
    /* ============================================================
       CSS VARIABLES & RESET
    ============================================================ */
    :root {
      --bg:     #0a0a12;
      --bg2:    #12121e;
      --card:   #1a1a2e;
      --border: #2a2a45;
      --yellow: #f9c74f;
      --cyan:   #43e8d8;
      --pink:   #f72585;
      --green:  #4ade80;
      --text:   #fffffe;
      --text2:  #9090b8;
      --radius: 16px;
    }

    * { margin: 0; padding: 0; box-sizing: border-box; }
    html, body {
      background: var(--bg);
      color: var(--text);
      font-family: 'Nunito', sans-serif;
      min-height: 100vh;
    }

    /* ============================================================
       PAGE SWITCHER  (only .active page is visible)
    ============================================================ */
    .page         { display: none; min-height: 100vh; flex-direction: column; }
    .page.active  { display: flex; }

    /* ============================================================
       SHARED — TOP BAR
    ============================================================ */
    .topbar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 14px 28px;
      border-bottom: 1px solid var(--border);
      background: var(--bg2);
      position: sticky;
      top: 0;
      z-index: 99;
    }
    .logo               { font-family: 'Fredoka One', cursive; font-size: 24px; color: var(--yellow); }
    .logo span          { color: var(--cyan); }
    .back-btn {
      background: var(--card);
      border: 1px solid var(--border);
      color: var(--text2);
      padding: 7px 16px;
      border-radius: 30px;
      cursor: pointer;
      font-family: 'Nunito', sans-serif;
      font-size: 13px;
      font-weight: 700;
      transition: .2s;
    }
    .back-btn:hover     { border-color: var(--yellow); color: var(--yellow); }
    .topbar-stats       { display: flex; gap: 10px; }
    .stat-chip {
      background: var(--card);
      border: 1px solid var(--border);
      padding: 5px 13px;
      border-radius: 30px;
      font-size: 13px;
      font-weight: 700;
      color: var(--yellow);
    }

    /* ============================================================
       LANDING PAGE
    ============================================================ */
    .landing-hero {
      text-align: center;
      padding: 60px 20px 30px;
      background: radial-gradient(ellipse 80% 50% at 50% 0%, rgba(67,232,216,.07) 0%, transparent 70%);
    }
    .landing-hero h1 {
      font-family: 'Fredoka One', cursive;
      font-size: clamp(44px, 9vw, 100px);
      color: var(--text);
      letter-spacing: 2px;
      line-height: 1;
      margin-bottom: 10px;
    }
    .landing-hero h1 span { color: var(--yellow); }
    .landing-hero p       { font-size: 17px; color: var(--text2); margin-bottom: 44px; }

    /* Game selection cards */
    .cards-row {
      display: flex;
      gap: 22px;
      justify-content: center;
      padding: 0 28px 50px;
      flex-wrap: wrap;
    }
    .game-card {
      background: var(--card);
      border: 2px solid var(--border);
      border-radius: 22px;
      padding: 32px 28px;
      width: 290px;
      cursor: pointer;
      transition: transform .25s, border-color .25s, box-shadow .25s;
    }
    .game-card:hover {
      transform: translateY(-7px);
      border-color: var(--yellow);
      box-shadow: 0 18px 45px rgba(249,199,79,.14);
    }
    .game-card .icon {
      font-size: 52px;
      margin-bottom: 14px;
      display: block;
      animation: iconBob 3s ease-in-out infinite;
    }
    .game-card:nth-child(2) .icon { animation-delay: -1s; }
    .game-card:nth-child(3) .icon { animation-delay: -2s; }

    @keyframes iconBob {
      0%, 100% { transform: translateY(0);   }
      50%       { transform: translateY(-7px);}
    }

    .game-card h2        { font-family: 'Fredoka One', cursive; font-size: 32px; margin-bottom: 7px; color: var(--yellow); }
    .game-card p         { color: var(--text2); font-size: 14px; line-height: 1.6; margin-bottom: 18px; }
    .tags                { display: flex; gap: 7px; flex-wrap: wrap; }
    .tag {
      background: rgba(249,199,79,.1);
      border: 1px solid rgba(249,199,79,.3);
      color: var(--yellow);
      font-size: 11px;
      font-weight: 700;
      padding: 3px 10px;
      border-radius: 30px;
      text-transform: uppercase;
      letter-spacing: 1px;
    }
    .play-btn {
      display: flex;
      align-items: center;
      gap: 7px;
      margin-top: 20px;
      font-size: 14px;
      font-weight: 800;
      color: var(--bg);
      background: var(--yellow);
      padding: 11px 22px;
      border-radius: 11px;
      border: none;
      cursor: pointer;
      font-family: 'Nunito', sans-serif;
      transition: .2s;
      width: 100%;
      justify-content: center;
    }
    .play-btn:hover { background: #ffe57f; }

    /* ============================================================
       SHARED — GAME LAYOUT  (sidebar | center | sidebar)
    ============================================================ */
    .game-layout {
      display: grid;
      grid-template-columns: 210px 1fr 210px;
      gap: 18px;
      padding: 20px;
      flex: 1;
      align-items: start;
    }
    .sidebar    { display: flex; flex-direction: column; gap: 10px; }
    .panel      { background: var(--card); border: 1px solid var(--border); border-radius: var(--radius); padding: 16px; }
    .panel-label {
      font-size: 10px;
      font-weight: 800;
      letter-spacing: 2px;
      text-transform: uppercase;
      color: var(--text2);
      margin-bottom: 12px;
    }

    /* Difficulty buttons row */
    .diff-row   { display: flex; gap: 5px; }
    .diff-btn {
      flex: 1;
      background: var(--bg);
      border: 1px solid var(--border);
      color: var(--text2);
      padding: 8px;
      border-radius: 9px;
      cursor: pointer;
      font-family: 'Nunito', sans-serif;
      font-size: 12px;
      font-weight: 700;
      transition: .2s;
    }
    .diff-btn.on,
    .diff-btn:hover { background: var(--yellow); color: var(--bg); border-color: var(--yellow); }

    /* Stats list inside panels */
    .stat-list  { display: flex; flex-direction: column; gap: 9px; }
    .stat-row   { display: flex; justify-content: space-between; align-items: center; font-size: 13px; color: var(--text2); }
    .stat-row b { color: var(--yellow); font-size: 17px; font-family: 'Fredoka One', cursive; }

    /* Action buttons */
    .act-btn {
      width: 100%;
      padding: 12px;
      margin-bottom: 7px;
      background: var(--bg);
      border: 1px solid var(--border);
      color: var(--text);
      font-family: 'Nunito', sans-serif;
      font-size: 12px;
      font-weight: 800;
      letter-spacing: 1px;
      text-transform: uppercase;
      border-radius: 11px;
      cursor: pointer;
      transition: .2s;
    }
    .act-btn:hover          { border-color: var(--text2); }
    .act-btn.primary        { background: var(--yellow); color: var(--bg); border-color: var(--yellow); }
    .act-btn.primary:hover  { background: #ffe57f; }

    /* How-to-play text */
    .howto { font-size: 12px; color: var(--text2); line-height: 1.7; }

    /* ============================================================
       NUMPUZ — Sliding Puzzle
    ============================================================ */
    .center-area { display: flex; align-items: center; justify-content: center; position: relative; min-height: 480px; }

    #np-board {
      display: grid;
      gap: 7px;
      padding: 18px;
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 18px;
      box-shadow: 0 18px 55px rgba(0,0,0,.5);
    }

    .tile {
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: 'Fredoka One', cursive;
      font-size: 32px;
      background: linear-gradient(135deg, #1e1e35, #16162a);
      border: 2px solid var(--border);
      border-radius: 11px;
      cursor: pointer;
      transition: all .15s;
      user-select: none;
      color: var(--text);
      box-shadow: 0 4px 12px rgba(0,0,0,.4), inset 0 1px 0 rgba(255,255,255,.06);
    }
    .tile:hover:not(.empty) {
      background: linear-gradient(135deg, #2e2c50, #22204a);
      border-color: var(--yellow);
      box-shadow: 0 0 20px rgba(249,199,79,.25), 0 4px 12px rgba(0,0,0,.4);
      transform: scale(1.06) translateY(-2px);
    }
    .tile.movable { border-color: rgba(249,199,79,.6); }
    .tile.empty   { background: rgba(255,255,255,.02); border: 2px dashed rgba(255,255,255,.08); cursor: default; pointer-events: none; box-shadow: none; }
    .tile.placed  { color: var(--cyan); text-shadow: 0 0 12px rgba(67,232,216,.4); }

    @keyframes shake {
      0%, 100% { transform: translateX(0);  }
      25%       { transform: translateX(-5px); }
      75%       { transform: translateX(5px);  }
    }
    .tile.shake { animation: shake .3s ease; }

    /* Mini preview grid (right sidebar) */
    #np-preview { display: grid; gap: 3px; }
    .prev-t {
      display: flex;
      align-items: center;
      justify-content: center;
      background: var(--bg);
      border: 1px solid var(--border);
      border-radius: 5px;
      font-size: 10px;
      color: var(--text2);
      font-weight: 700;
      aspect-ratio: 1;
    }
    .prev-t.ok { background: rgba(67,232,216,.1); border-color: var(--cyan); color: var(--cyan); }

    /* Move history list */
    #np-hist { display: flex; flex-direction: column; gap: 5px; max-height: 170px; overflow-y: auto; }
    .hist-item { display: flex; justify-content: space-between; font-size: 11px; color: var(--text2); background: var(--bg); border-radius: 7px; padding: 5px 9px; }
    .hist-item b { color: var(--text); font-weight: 700; }

    /* ============================================================
       JIGSAW — Drag-and-Drop Puzzle
    ============================================================ */
    #jig-board {
      display: grid;
      gap: 3px;
      padding: 14px;
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 18px;
      box-shadow: 0 18px 55px rgba(0,0,0,.5);
    }

    .jcell { border: 2px dashed var(--border); border-radius: 9px; transition: .2s; position: relative; overflow: hidden; aspect-ratio: 1; }
    .jcell.over         { border-color: var(--yellow); background: rgba(249,199,79,.06); }
    .jcell.done         { border: 2px solid transparent; }
    .jcell.correct-pos  { box-shadow: inset 0 0 0 2px var(--cyan); }
    .jcell canvas       { display: block; width: 100%; height: 100%; }

    /* Piece tray (right sidebar) */
    #jig-tray { display: grid; grid-template-columns: repeat(3, 1fr); gap: 5px; max-height: 340px; overflow-y: auto; padding: 2px; }
    .piece {
      border: 2px solid var(--border);
      border-radius: 9px;
      cursor: grab;
      transition: .2s;
      overflow: hidden;
      aspect-ratio: 1;
      background: var(--bg);
    }
    .piece:hover       { transform: scale(1.1); border-color: var(--yellow); }
    .piece.used        { opacity: .2; pointer-events: none; }
    .piece canvas      { display: block; width: 100%; height: 100%; pointer-events: none; }

    /* Image theme selector buttons */
    .img-opts { display: flex; flex-direction: column; gap: 5px; }
    .img-opt {
      padding: 9px 13px;
      border-radius: 9px;
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      border: 2px solid transparent;
      color: white;
      transition: .2s;
      text-shadow: 0 1px 3px rgba(0,0,0,.5);
    }
    .img-opt:hover { transform: translateX(4px); }
    .img-opt.on    { border-color: var(--yellow); }

    #jig-ref { width: 100%; border-radius: 9px; border: 1px solid var(--border); }

    /* ============================================================
       PLATFORMER — Canvas Game
    ============================================================ */
    #plat-wrap {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      flex: 1;
      padding: 20px;
      gap: 16px;
      position: relative;
    }
    #gameCanvas {
      border-radius: 16px;
      border: 2px solid var(--border);
      box-shadow: 0 20px 60px rgba(0,0,0,.7);
      display: block;
      max-width: 100%;
    }

    /* Key-binding guide below the canvas */
    .key-guide { display: flex; gap: 8px; flex-wrap: wrap; justify-content: center; }
    .key-box   { background: var(--card); border: 1px solid var(--border); border-radius: 8px; padding: 5px 12px; font-size: 12px; font-weight: 700; color: var(--text2); }
    .key-box b { color: var(--yellow); }

    /* Start / Game-over overlay */
    #plat-overlay {
      position: absolute;
      inset: 0;
      display: flex;
      align-items: center;
      justify-content: center;
      background: rgba(10,10,18,.88);
      backdrop-filter: blur(8px);
      border-radius: 16px;
      z-index: 10;
      flex-direction: column;
      gap: 16px;
    }
    #plat-overlay.hidden { display: none; }
    .overlay-title { font-family: 'Fredoka One', cursive; font-size: 60px; color: var(--yellow); letter-spacing: 3px; text-align: center; line-height: 1.1; }
    .overlay-sub   { font-size: 15px; color: var(--text2); font-weight: 700; text-align: center; max-width: 400px; line-height: 1.6; }
    .overlay-btn {
      background: var(--yellow);
      color: var(--bg);
      font-family: 'Fredoka One', cursive;
      font-size: 22px;
      padding: 14px 40px;
      border: none;
      border-radius: 14px;
      cursor: pointer;
      transition: .2s;
      letter-spacing: 1px;
    }
    .overlay-btn:hover { background: #ffe57f; transform: scale(1.05); }

    /* ============================================================
       SHARED — WIN BANNER  (overlays the center area)
    ============================================================ */
    .win-banner {
      position: absolute;
      inset: 0;
      z-index: 50;
      display: none;
      align-items: center;
      justify-content: center;
      background: rgba(10,10,18,.92);
      border-radius: 18px;
      backdrop-filter: blur(8px);
    }
    .win-banner.show { display: flex; animation: fadeIn .4s ease; }

    @keyframes fadeIn {
      from { opacity: 0; transform: scale(.9); }
      to   { opacity: 1; transform: scale(1);  }
    }

    .wb         { text-align: center; padding: 36px; }
    .wb .emoji  { font-size: 68px; animation: bounce .6s ease; display: block; margin-bottom: 14px; }

    @keyframes bounce {
      0%   { transform: scale(0);   }
      60%  { transform: scale(1.2); }
      100% { transform: scale(1);   }
    }

    .wb h2 { font-family: 'Fredoka One', cursive; font-size: 52px; color: var(--yellow); letter-spacing: 3px; margin-bottom: 10px; }
    .wb p  { color: var(--text2); font-size: 13px; font-weight: 700; margin-bottom: 20px; line-height: 1.8; }
    .wb .act-btn { width: auto; display: inline-block; padding: 13px 32px; }

    /* ============================================================
       FOOTER
    ============================================================ */
    footer { text-align: center; padding: 18px; border-top: 1px solid var(--border); color: var(--text2); font-size: 12px; font-weight: 600; }
  </style>
</head>
<body>

<!-- ============================================================
     LANDING PAGE
============================================================ -->
<div id="home" class="page active">
  <div class="topbar">
    <div class="logo">Game<span>Verse</span></div>
    <div style="font-size:13px; color:var(--text2); font-weight:700;">3 Games — 1 Place 🎮</div>
  </div>

  <div class="landing-hero">
    <h1>PLAY &amp; <span>WIN</span></h1>
    <p>Three awesome games — NumPuz, Jigsaw &amp; Platformer!</p>
  </div>

  <div class="cards-row">
    <!-- NumPuz card -->
    <div class="game-card" onclick="openNumpuz()">
      <span class="icon">🔢</span>
      <h2>NumPuz</h2>
      <p>Slide numbered tiles into the correct order. A real test of your brain!</p>
      <div class="tags">
        <span class="tag">Sliding</span>
        <span class="tag">Logic</span>
      </div>
      <button class="play-btn">▶ Play NumPuz</button>
    </div>

    <!-- Jigsaw card -->
    <div class="game-card" onclick="openJigsaw()">
      <span class="icon">🧩</span>
      <h2>Jigsaw</h2>
      <p>Drag pieces to complete the picture. You can even use your own photo!</p>
      <div class="tags">
        <span class="tag">Drag &amp; Drop</span>
        <span class="tag">Visual</span>
      </div>
      <button class="play-btn">▶ Play Jigsaw</button>
    </div>

    <!-- Platformer card -->
    <div class="game-card" onclick="openPlatformer()">
      <span class="icon">🕹️</span>
      <h2>Platformer</h2>
      <p>Jump, grab coins, defeat enemies! Double-jump is also available!</p>
      <div class="tags">
        <span class="tag">Action</span>
        <span class="tag">Adventure</span>
      </div>
      <button class="play-btn">▶ Play Platformer</button>
    </div>
  </div>

  <footer>Made with ❤️ using Python Flask &nbsp;|&nbsp; GameVerse 2026</footer>
</div>


<!-- ============================================================
     NUMPUZ PAGE
============================================================ -->
<div id="np-page" class="page">
  <div class="topbar">
    <button class="back-btn" onclick="goHome()">← Home</button>
    <div class="logo">Num<span>Puz</span></div>
    <div class="topbar-stats">
      <div class="stat-chip" id="np-moves-chip">Moves: 0</div>
      <div class="stat-chip" id="np-time-chip">00:00</div>
    </div>
  </div>

  <div class="game-layout">
    <!-- Left sidebar: settings & stats -->
    <div class="sidebar">
      <div class="panel">
        <div class="panel-label">Difficulty</div>
        <div class="diff-row">
          <button class="diff-btn on" onclick="npSetSize(this, 3)">3x3</button>
          <button class="diff-btn"    onclick="npSetSize(this, 4)">4x4</button>
          <button class="diff-btn"    onclick="npSetSize(this, 5)">5x5</button>
        </div>
      </div>

      <div class="panel">
        <div class="panel-label">Stats</div>
        <div class="stat-list">
          <div class="stat-row"><span>Moves</span><b id="np-moves">0</b></div>
          <div class="stat-row"><span>Time</span> <b id="np-time">00:00</b></div>
          <div class="stat-row"><span>Best</span> <b id="np-best">--</b></div>
        </div>
      </div>

      <button class="act-btn primary" onclick="npNewGame()">Shuffle</button>
      <button class="act-btn"         onclick="npHint()">Hint</button>

      <div class="panel">
        <div class="panel-label">How to Play</div>
        <div class="howto">Click a tile next to the empty space, or use arrow keys. Arrange numbers 1 to N in order!</div>
      </div>
    </div>

    <!-- Center: the puzzle board + win banner -->
    <div class="center-area">
      <div id="np-board"></div>
      <div class="win-banner" id="np-win">
        <div class="wb">
          <span class="emoji">🎉</span>
          <h2>SOLVED!</h2>
          <p id="np-win-stats"></p>
          <button class="act-btn primary" onclick="npNewGame()">Play Again</button>
        </div>
      </div>
    </div>

    <!-- Right sidebar: preview grid & history -->
    <div class="sidebar">
      <div class="panel">
        <div class="panel-label">Preview</div>
        <div id="np-preview"></div>
      </div>
      <div class="panel">
        <div class="panel-label">History</div>
        <div id="np-hist">
          <div style="color:var(--text2); font-size:11px; text-align:center; padding:8px;">No games yet</div>
        </div>
      </div>
    </div>
  </div>
</div>


<!-- ============================================================
     JIGSAW PAGE
============================================================ -->
<div id="jig-page" class="page">
  <div class="topbar">
    <button class="back-btn" onclick="goHome()">← Home</button>
    <div class="logo">Jig<span>Saw</span></div>
    <div class="topbar-stats">
      <div class="stat-chip" id="jig-chip">0/0 pieces</div>
      <div class="stat-chip" id="jig-time-chip">00:00</div>
    </div>
  </div>

  <div class="game-layout">
    <!-- Left sidebar: image selector, grid size, stats -->
    <div class="sidebar">
      <div class="panel">
        <div class="panel-label">Choose Image</div>
        <div class="img-opts">
          <div class="img-opt on" data-img="nature" style="background:linear-gradient(135deg,#1a6b1a,#5cb85c)"  onclick="jigSetImg(this,'nature')">Nature</div>
          <div class="img-opt"    data-img="ocean"  style="background:linear-gradient(135deg,#0a2f8a,#0575e6)"  onclick="jigSetImg(this,'ocean')">Ocean</div>
          <div class="img-opt"    data-img="sunset" style="background:linear-gradient(135deg,#7c1c4b,#f7971e)"  onclick="jigSetImg(this,'sunset')">Sunset</div>
          <div class="img-opt"    data-img="space"  style="background:linear-gradient(135deg,#0d0030,#4a0080)"  onclick="jigSetImg(this,'space')">Space</div>
          <div class="img-opt"    data-img="city"   style="background:linear-gradient(135deg,#0a0a1a,#2a4080)"  onclick="jigSetImg(this,'city')">City</div>
          <label class="img-opt"  style="background:linear-gradient(135deg,#3a003a,#7a0070); cursor:pointer;" for="img-upload">📁 Your Photo</label>
          <input type="file" id="img-upload" accept="image/*" style="display:none" onchange="jigLoadCustom(this)"/>
        </div>

        <!-- Thumbnail preview after uploading a custom photo -->
        <div id="upload-preview-wrap" style="display:none; margin-top:8px;">
          <img id="upload-thumb" style="width:100%; border-radius:9px; border:2px solid var(--yellow); max-height:80px; object-fit:cover;"/>
          <div style="font-size:11px; color:var(--cyan); margin-top:5px; font-weight:700; text-align:center;">Photo ready!</div>
        </div>
      </div>

      <div class="panel">
        <div class="panel-label">Grid Size</div>
        <div class="diff-row">
          <button class="diff-btn on" onclick="jigSetGrid(this, 3)">3x3</button>
          <button class="diff-btn"    onclick="jigSetGrid(this, 4)">4x4</button>
          <button class="diff-btn"    onclick="jigSetGrid(this, 5)">5x5</button>
        </div>
      </div>

      <div class="panel">
        <div class="panel-label">Stats</div>
        <div class="stat-list">
          <div class="stat-row"><span>Placed</span><b id="jig-placed">0</b></div>
          <div class="stat-row"><span>Total</span> <b id="jig-total">0</b></div>
          <div class="stat-row"><span>Time</span>  <b id="jig-stime">00:00</b></div>
        </div>
      </div>

      <button class="act-btn primary" onclick="jigNewGame()">New Puzzle</button>
      <button class="act-btn"         onclick="jigTogglePreview()">Preview</button>
    </div>

    <!-- Center: the jigsaw board + win banner -->
    <div class="center-area" style="flex-direction:column; gap:12px;">
      <div id="jig-board"></div>
      <div class="win-banner" id="jig-win">
        <div class="wb">
          <span class="emoji">🧩</span>
          <h2>COMPLETE!</h2>
          <p id="jig-win-stats"></p>
          <button class="act-btn primary" onclick="jigNewGame()">New Puzzle</button>
        </div>
      </div>
    </div>

    <!-- Right sidebar: draggable piece tray & reference image -->
    <div class="sidebar">
      <div class="panel">
        <div class="panel-label">Piece Tray</div>
        <div id="jig-tray"></div>
      </div>
      <div class="panel">
        <div class="panel-label">Reference</div>
        <canvas id="jig-ref" width="180" height="180"></canvas>
      </div>
    </div>
  </div>
</div>


<!-- ============================================================
     PLATFORMER PAGE
============================================================ -->
<div id="plat-page" class="page">
  <div class="topbar">
    <button class="back-btn" onclick="goHome(); platStop()">← Home</button>
    <div class="logo">Plat<span>Former</span></div>
    <div class="topbar-stats">
      <div class="stat-chip" id="p-score-chip" style="color:var(--yellow)">Score: 0</div>
      <div class="stat-chip" id="p-lives-chip" style="color:var(--pink)">Lives: 3</div>
      <div class="stat-chip" id="p-time-chip"  style="color:var(--cyan)">60s</div>
      <div class="stat-chip" id="p-level-chip" style="color:var(--green)">Level 1</div>
    </div>
  </div>

  <div id="plat-wrap">
    <canvas id="gameCanvas" width="800" height="420"></canvas>

    <!-- Keyboard control hints -->
    <div class="key-guide">
      <div class="key-box"><b>← →</b> Move</div>
      <div class="key-box"><b>SPACE / Up</b> Jump</div>
      <div class="key-box"><b>Double Jump</b> allowed!</div>
      <div class="key-box"><b>Land on Enemy</b> = +20 pts</div>
      <div class="key-box"><b>Coin</b> = +10 pts</div>
    </div>

    <!-- Start / game-over overlay -->
    <div id="plat-overlay">
      <div class="overlay-title" id="ov-title">PLATFORMER</div>
      <div class="overlay-sub"   id="ov-sub">Jump, collect coins, defeat enemies! A 2-level adventure!</div>
      <button class="overlay-btn" id="ov-btn" onclick="platStart()">START GAME</button>
    </div>
  </div>
</div>


<script>
// ============================================================
// NAVIGATION — switch between pages
// ============================================================
function showPage(id) {
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  document.getElementById(id).classList.add('active');
  window.scrollTo(0, 0);
}
function goHome()        { showPage('home'); }
function openNumpuz()    { showPage('np-page');   npInit(3); }
function openJigsaw()    { showPage('jig-page');  jigInit(); }
function openPlatformer(){ showPage('plat-page'); document.getElementById('plat-overlay').classList.remove('hidden'); }


// ============================================================
// NUMPUZ — Sliding Number Puzzle
// ============================================================
var NP = { size: 3, board: [], moves: 0, secs: 0, timer: null, best: {}, history: [], active: false };

/** Initialise (or re-initialise) the puzzle with a given grid size. */
function npInit(sz) {
  NP.size = sz || NP.size;
  clearInterval(NP.timer);
  NP.moves = 0; NP.secs = 0; NP.active = false;
  npUpdateMoves(); npUpdateTime();
  document.getElementById('np-win').classList.remove('show');

  // Build solved board then shuffle via random valid moves
  NP.board = [];
  for (var i = 1; i < NP.size * NP.size; i++) NP.board.push(i);
  NP.board.push(0); // 0 represents the empty tile

  var emp = NP.board.indexOf(0);
  for (var i = 0; i < 300 + NP.size * 100; i++) {
    var r = Math.floor(emp / NP.size), c = emp % NP.size, nb = [];
    if (r > 0)            nb.push(emp - NP.size);
    if (r < NP.size - 1) nb.push(emp + NP.size);
    if (c > 0)            nb.push(emp - 1);
    if (c < NP.size - 1) nb.push(emp + 1);
    var nx = nb[Math.floor(Math.random() * nb.length)];
    var t = NP.board[emp]; NP.board[emp] = NP.board[nx]; NP.board[nx] = t;
    emp = nx;
  }

  npRender(); npRenderPreview();
  NP.timer = setInterval(function() { NP.secs++; npUpdateTime(); }, 1000);
  NP.active = true;
}

/** Change grid size via difficulty buttons. */
function npSetSize(btn, sz) {
  document.querySelectorAll('#np-page .diff-btn').forEach(b => b.classList.remove('on'));
  btn.classList.add('on');
  npInit(sz);
}

function npNewGame() { npInit(NP.size); }

/** Re-render the puzzle tiles onto the board element. */
function npRender() {
  var board = document.getElementById('np-board');
  if (!board) return;

  var TS = NP.size === 3 ? 108 : NP.size === 4 ? 80 : 62; // tile size in px
  board.style.gridTemplateColumns = 'repeat(' + NP.size + ', ' + TS + 'px)';
  board.innerHTML = '';

  NP.board.forEach(function(v, i) {
    var t = document.createElement('div');
    t.className = 'tile';
    t.style.width = t.style.height = TS + 'px';
    t.style.fontSize = (NP.size === 3 ? 34 : NP.size === 4 ? 24 : 18) + 'px';

    if (v === 0) {
      t.classList.add('empty');
    } else {
      t.textContent = v;
      if (v - 1 === i) t.classList.add('placed');   // tile is in its correct position
      if (npCanMove(i))  t.classList.add('movable'); // tile can slide into the empty space
      (function(idx) { t.onclick = function() { npClick(idx); }; })(i);
    }
    board.appendChild(t);
  });
}

/** Re-render the small preview grid in the right sidebar. */
function npRenderPreview() {
  var el = document.getElementById('np-preview');
  if (!el) return;
  el.style.gridTemplateColumns = 'repeat(' + NP.size + ', 1fr)';
  el.style.display = 'grid';
  el.style.gap = '3px';
  el.innerHTML = '';
  NP.board.forEach(function(v, i) {
    var t = document.createElement('div');
    t.className = 'prev-t' + (v !== 0 && v - 1 === i ? ' ok' : '');
    if (v !== 0) t.textContent = v;
    el.appendChild(t);
  });
}

/** Return true if tile at index i is adjacent to the empty tile. */
function npCanMove(i) {
  var emp = NP.board.indexOf(0);
  var r = Math.floor(i / NP.size),   c = i % NP.size;
  var er = Math.floor(emp / NP.size), ec = emp % NP.size;
  return (r === er && Math.abs(c - ec) === 1) || (c === ec && Math.abs(r - er) === 1);
}

/** Handle a tile click — slide it if valid, otherwise shake it. */
function npClick(i) {
  if (!NP.active) return;
  if (!npCanMove(i)) {
    // Shake the tile to signal it cannot move
    var tiles = document.querySelectorAll('#np-board .tile');
    tiles[i].classList.add('shake');
    setTimeout(function() { tiles[i].classList.remove('shake'); }, 300);
    return;
  }

  // Swap the clicked tile with the empty space
  var emp = NP.board.indexOf(0);
  var t = NP.board[i]; NP.board[i] = NP.board[emp]; NP.board[emp] = t;
  NP.moves++;
  npUpdateMoves(); npRender(); npRenderPreview();

  if (npCheckWin()) {
    NP.active = false;
    clearInterval(NP.timer);
    npRecordBest();
    NP.history.unshift({ size: NP.size, moves: NP.moves, secs: NP.secs });
    if (NP.history.length > 8) NP.history.pop();
    npRenderHistory();
    setTimeout(function() {
      document.getElementById('np-win-stats').innerHTML =
        NP.moves + ' moves &nbsp;·&nbsp; ' + fmtTime(NP.secs) + ' &nbsp;·&nbsp; ' + NP.size + 'x' + NP.size;
      document.getElementById('np-win').classList.add('show');
    }, 300);
  }
}

/** Return true when tiles 1…N are in order and 0 is last. */
function npCheckWin() {
  for (var i = 0; i < NP.board.length - 1; i++) if (NP.board[i] !== i + 1) return false;
  return NP.board[NP.board.length - 1] === 0;
}

function npUpdateMoves() {
  var v = NP.moves;
  var e1 = document.getElementById('np-moves');
  var e2 = document.getElementById('np-moves-chip');
  if (e1) e1.textContent = v;
  if (e2) e2.textContent = 'Moves: ' + v;
}

function npUpdateTime() {
  var t = fmtTime(NP.secs);
  var e1 = document.getElementById('np-time');
  var e2 = document.getElementById('np-time-chip');
  if (e1) e1.textContent = t;
  if (e2) e2.textContent = t;
}

/** Format seconds as MM:SS */
function fmtTime(s) {
  return String(Math.floor(s / 60)).padStart(2, '0') + ':' + String(s % 60).padStart(2, '0');
}

function npRecordBest() {
  var k = NP.size + 'x' + NP.size;
  if (!NP.best[k] || NP.secs < NP.best[k]) NP.best[k] = NP.secs;
  var el = document.getElementById('np-best');
  if (el) el.textContent = fmtTime(NP.best[k]);
}

function npRenderHistory() {
  var el = document.getElementById('np-hist');
  if (!el) return;
  if (!NP.history.length) {
    el.innerHTML = '<div style="color:var(--text2); font-size:11px; text-align:center; padding:8px;">No games yet</div>';
    return;
  }
  el.innerHTML = NP.history.map(function(h) {
    return '<div class="hist-item"><b>' + h.size + 'x' + h.size + '</b><span>' + h.moves + ' moves</span><span>' + fmtTime(h.secs) + '</span></div>';
  }).join('');
}

/** Briefly highlight tiles that are already in their correct positions. */
function npHint() {
  document.querySelectorAll('#np-board .tile.placed').forEach(function(t) {
    t.style.boxShadow = '0 0 22px rgba(67,232,216,.9)';
    setTimeout(function() { t.style.boxShadow = ''; }, 1500);
  });
}

// Arrow-key support for NumPuz
document.addEventListener('keydown', function(e) {
  if (!document.getElementById('np-page').classList.contains('active')) return;
  var emp = NP.board.indexOf(0);
  var er = Math.floor(emp / NP.size), ec = emp % NP.size, ti = -1;
  if (e.key === 'ArrowUp'    && er < NP.size - 1) ti = emp + NP.size;
  if (e.key === 'ArrowDown'  && er > 0)            ti = emp - NP.size;
  if (e.key === 'ArrowLeft'  && ec < NP.size - 1)  ti = emp + 1;
  if (e.key === 'ArrowRight' && ec > 0)             ti = emp - 1;
  if (ti >= 0) { e.preventDefault(); npClick(ti); }
});


// ============================================================
// JIGSAW — Drag-and-Drop Picture Puzzle
// ============================================================
var JIG = {
  grid: 3, img: 'nature', pieces: [], cells: [],
  secs: 0, timer: null, placed: 0, total: 0,
  active: false, dragging: null, showPreview: false, customImg: null
};

/** Canvas-drawing functions for each built-in image theme */
var JIG_IMGS = {
  nature: function(ctx, w, h) {
    // Sky gradient
    var g = ctx.createLinearGradient(0, 0, 0, h);
    g.addColorStop(0,   '#87CEEB'); g.addColorStop(.42, '#b0e0ff');
    g.addColorStop(.42, '#3a8a3a'); g.addColorStop(1,   '#1a4a1a');
    ctx.fillStyle = g; ctx.fillRect(0, 0, w, h);

    // Sun
    ctx.fillStyle = '#ffe566';
    ctx.beginPath(); ctx.arc(w * .78, h * .14, w * .07, 0, Math.PI * 2); ctx.fill();

    // Clouds
    ctx.fillStyle = 'rgba(255,255,255,.8)';
    [[w*.18, h*.1, w*.08], [w*.48, h*.07, w*.06], [w*.75, h*.12, w*.05]].forEach(function(d) {
      [0, .5, -.5].forEach(function(dx) {
        ctx.beginPath(); ctx.arc(d[0] + dx * d[2] * 1.2, d[1], d[2] * (1 - Math.abs(dx) * .3), 0, Math.PI * 2); ctx.fill();
      });
    });

    // Trees
    for (var i = 0; i < 8; i++) {
      var x = (w / 8) * i + w / 16, y = h * .5 + Math.sin(i) * 14, r = w / 18 + i * 1.4;
      ctx.fillStyle = '#1a5c1a';
      ctx.beginPath(); ctx.moveTo(x, y - r * 2.5); ctx.lineTo(x - r, y); ctx.lineTo(x + r, y); ctx.closePath(); ctx.fill();
      ctx.beginPath(); ctx.moveTo(x, y - r * 3.4); ctx.lineTo(x - r * .7, y - r); ctx.lineTo(x + r * .7, y - r); ctx.closePath(); ctx.fill();
      ctx.fillStyle = '#5a3010'; ctx.fillRect(x - r * .18, y, r * .36, r * .6);
    }

    // Ground
    var gg = ctx.createLinearGradient(0, h * .5, 0, h);
    gg.addColorStop(0, '#3a8a3a'); gg.addColorStop(1, '#1a4a1a');
    ctx.fillStyle = gg; ctx.fillRect(0, h * .5, w, h * .5);
  },

  ocean: function(ctx, w, h) {
    var g = ctx.createLinearGradient(0, 0, 0, h);
    g.addColorStop(0, '#87CEEB'); g.addColorStop(.38, '#4fc3f7');
    g.addColorStop(.38, '#0575e6'); g.addColorStop(1, '#003580');
    ctx.fillStyle = g; ctx.fillRect(0, 0, w, h);

    // Sun
    ctx.fillStyle = '#fffdb0';
    ctx.beginPath(); ctx.arc(w * .5, h * .12, w * .07, 0, Math.PI * 2); ctx.fill();

    // Wave lines
    for (var y = h * .4; y < h; y += h / 9) {
      ctx.strokeStyle = 'rgba(255,255,255,0.2)'; ctx.lineWidth = 2;
      ctx.beginPath();
      for (var x = 0; x <= w; x += 7) {
        var wy = y + Math.sin(x / 22 + y / 14) * h * .022;
        if (x === 0) ctx.moveTo(x, wy); else ctx.lineTo(x, wy);
      }
      ctx.stroke();
    }
  },

  sunset: function(ctx, w, h) {
    var g = ctx.createLinearGradient(0, 0, 0, h);
    g.addColorStop(0, '#1a0533'); g.addColorStop(.25, '#7c1c4b');
    g.addColorStop(.55, '#f7971e'); g.addColorStop(1, '#ffd200');
    ctx.fillStyle = g; ctx.fillRect(0, 0, w, h);

    // Sun on horizon
    ctx.fillStyle = 'rgba(255,255,150,.9)';
    ctx.beginPath(); ctx.arc(w / 2, h * .58, w * .04, 0, Math.PI * 2); ctx.fill();

    // City silhouette buildings
    ctx.fillStyle = '#0a0015';
    [[.03,.62,.08,.38],[.12,.42,.07,.55],[.22,.55,.1,.45],[.33,.35,.08,.65],[.42,.5,.09,.5],
     [.52,.38,.08,.62],[.61,.58,.09,.42],[.71,.3,.08,.7],[.8,.48,.1,.52],[.91,.42,.09,.58]]
    .forEach(function(b) { ctx.fillRect(b[0]*w, b[1]*h, b[2]*w, b[3]*h); });
  },

  space: function(ctx, w, h) {
    var g = ctx.createLinearGradient(0, 0, w, h);
    g.addColorStop(0, '#030010'); g.addColorStop(1, '#050020');
    ctx.fillStyle = g; ctx.fillRect(0, 0, w, h);

    // Stars
    for (var i = 0; i < 260; i++) {
      var x = Math.random() * w, y = Math.random() * h, r = Math.random() * 1.5 + .2;
      ctx.fillStyle = 'rgba(255,255,255,' + (Math.random() * .9 + .1) + ')';
      ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI * 2); ctx.fill();
    }

    // Nebula glow
    var ng = ctx.createRadialGradient(w*.65, h*.35, 0, w*.65, h*.35, w*.38);
    ng.addColorStop(0, 'rgba(180,0,255,.18)'); ng.addColorStop(1, 'transparent');
    ctx.fillStyle = ng; ctx.fillRect(0, 0, w, h);

    // Planet + ring
    ctx.fillStyle = '#7755cc';
    ctx.beginPath(); ctx.arc(w * .27, h * .3, w * .1, 0, Math.PI * 2); ctx.fill();
    ctx.strokeStyle = 'rgba(180,150,255,.4)'; ctx.lineWidth = 5;
    ctx.beginPath(); ctx.ellipse(w * .27, h * .3, w * .18, w * .042, -.28, 0, Math.PI * 2); ctx.stroke();
  },

  city: function(ctx, w, h) {
    var g = ctx.createLinearGradient(0, 0, 0, h);
    g.addColorStop(0, '#080818'); g.addColorStop(1, '#1a2050');
    ctx.fillStyle = g; ctx.fillRect(0, 0, w, h);

    // Stars
    for (var i = 0; i < 120; i++) {
      var x = Math.random() * w, y = Math.random() * h * .6, r = Math.random() * .9 + .2;
      ctx.fillStyle = 'rgba(255,255,255,' + (Math.random() * .5 + .1) + ')';
      ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI * 2); ctx.fill();
    }

    // Buildings with lit windows
    [[.03,.58,.08,.42],[.12,.42,.07,.58],[.20,.52,.1,.48],[.31,.32,.08,.68],[.40,.47,.1,.53],
     [.51,.37,.07,.63],[.59,.57,.09,.43],[.69,.28,.08,.72],[.78,.48,.09,.52],[.88,.42,.1,.58]]
    .forEach(function(b) {
      ctx.fillStyle = '#0f1830'; ctx.fillRect(b[0]*w, b[1]*h, b[2]*w, b[3]*h);
      for (var wy = b[1]*h + 7; wy < h - 5; wy += 11)
        for (var wx = b[0]*w + 4; wx < (b[0] + b[2])*w - 4; wx += 8)
          if (Math.random() > .3) { ctx.fillStyle = 'rgba(255,220,100,.65)'; ctx.fillRect(wx, wy, 4, 6); }
    });
  }
};

/** Draw the source image (theme or custom photo) onto a temporary canvas and return it. */
function jigDrawSrc(w, h) {
  var c = document.createElement('canvas'); c.width = w; c.height = h;
  var ctx = c.getContext('2d');
  if (JIG.img === 'custom' && JIG.customImg) {
    var img = JIG.customImg;
    var scale = Math.max(w / img.naturalWidth, h / img.naturalHeight);
    var sw = img.naturalWidth * scale, sh = img.naturalHeight * scale;
    ctx.drawImage(img, (w - sw) / 2, (h - sh) / 2, sw, sh);
  } else {
    (JIG_IMGS[JIG.img] || JIG_IMGS.nature)(ctx, w, h);
  }
  return c;
}

/** Calculate optimal cell size so the board fits the viewport. */
function jigCS() {
  return Math.floor((Math.min(window.innerWidth * .42, 480) - 32 - (JIG.grid - 1) * 4) / JIG.grid);
}

/** Initialise (or reset) the jigsaw puzzle. */
function jigInit() {
  clearInterval(JIG.timer);
  JIG.secs = 0; JIG.placed = 0; JIG.active = false; JIG.dragging = null;
  JIG.pieces = []; JIG.cells = [];
  document.getElementById('jig-win').classList.remove('show');

  var CS = jigCS(), W = CS * JIG.grid, H = CS * JIG.grid;
  var src = jigDrawSrc(W, H);
  JIG.total = JIG.grid * JIG.grid;

  // Slice the source image into individual piece canvases
  for (var id = 0; id < JIG.total; id++) {
    var r = Math.floor(id / JIG.grid), c = id % JIG.grid;
    var cv = document.createElement('canvas'); cv.width = CS; cv.height = CS;
    var ctx = cv.getContext('2d');
    ctx.drawImage(src, c * CS, r * CS, CS, CS, 0, 0, CS, CS);
    ctx.strokeStyle = 'rgba(255,255,255,.07)'; ctx.lineWidth = 1;
    ctx.strokeRect(.5, .5, CS - 1, CS - 1);
    JIG.pieces.push({ id: id, r: r, c: c, canvas: cv, placed: false });
  }

  // Shuffle the piece order in the tray
  JIG.pieces.sort(function() { return Math.random() - .5; });

  // Build the drop-target grid
  var board = document.getElementById('jig-board');
  board.style.gridTemplateColumns = 'repeat(' + JIG.grid + ', ' + CS + 'px)';
  board.innerHTML = ''; JIG.cells = [];

  for (var r = 0; r < JIG.grid; r++) {
    for (var c = 0; c < JIG.grid; c++) {
      var cell = document.createElement('div');
      cell.className = 'jcell'; cell.style.width = cell.style.height = CS + 'px';
      cell.dataset.r = r; cell.dataset.c = c;
      // Attach drag-over / drop handlers
      (function(tr, tc, cel) {
        cel.ondragover  = function(e) { e.preventDefault(); cel.classList.add('over'); };
        cel.ondragleave = function()  { cel.classList.remove('over'); };
        cel.ondrop      = function(e) { e.preventDefault(); cel.classList.remove('over'); jigDrop(tr, tc, cel); };
      })(r, c, cell);
      board.appendChild(cell);
      JIG.cells.push({ r: r, c: c, el: cell, filled: false });
    }
  }

  jigRenderTray(); jigDrawRef(); jigUpdateStats();
  JIG.timer = setInterval(function() { JIG.secs++; jigUpdateTime(); }, 1000);
  JIG.active = true;
}

/** Populate the piece tray in the right sidebar. */
function jigRenderTray() {
  var tray = document.getElementById('jig-tray');
  if (!tray) return;
  tray.innerHTML = '';

  JIG.pieces.forEach(function(p) {
    var div = document.createElement('div');
    div.className = 'piece' + (p.placed ? ' used' : '');
    div.draggable = !p.placed;
    div.dataset.id = p.id;

    // Thumbnail canvas
    var mini = document.createElement('canvas'); mini.width = 56; mini.height = 56;
    mini.getContext('2d').drawImage(p.canvas, 0, 0, 56, 56);
    div.appendChild(mini);

    // Drag start/end events
    (function(pc, d) {
      d.ondragstart = function(e) {
        if (pc.placed) return;
        JIG.dragging = pc.id;
        e.dataTransfer.effectAllowed = 'move';
        setTimeout(function() { d.style.opacity = '.4'; }, 0);
      };
      d.ondragend = function() { d.style.opacity = ''; JIG.dragging = null; };
    })(p, div);

    tray.appendChild(div);
    p.trayEl = div;
  });
}

/** Handle a piece being dropped onto a cell. */
function jigDrop(tr, tc, cellEl) {
  if (JIG.dragging === null) return;

  // Find the dragged piece
  var piece = null;
  for (var i = 0; i < JIG.pieces.length; i++) if (JIG.pieces[i].id === JIG.dragging) { piece = JIG.pieces[i]; break; }
  if (!piece || piece.placed) return;

  // Find the target cell data
  var cellData = null;
  for (var i = 0; i < JIG.cells.length; i++) if (JIG.cells[i].r === tr && JIG.cells[i].c === tc) { cellData = JIG.cells[i]; break; }
  if (cellData && cellData.filled) return;

  // Draw the piece into the cell, tinting green (correct) or red (wrong)
  var CS = jigCS(), cv = document.createElement('canvas'); cv.width = CS; cv.height = CS;
  var ctx = cv.getContext('2d'); ctx.drawImage(piece.canvas, 0, 0, CS, CS);
  var isRight = (piece.r === tr && piece.c === tc);

  if (isRight) {
    ctx.fillStyle = 'rgba(67,232,216,.1)'; ctx.fillRect(0, 0, CS, CS);
    JIG.placed++;
  } else {
    ctx.fillStyle = 'rgba(255,80,80,.1)'; ctx.fillRect(0, 0, CS, CS);
    jigSetupCellDrag(cellEl, piece, cellData); // allow moving wrongly-placed pieces
    piece.placed = 'wrong';
  }

  cellEl.innerHTML = ''; cellEl.appendChild(cv); cellEl.classList.add('done');
  if (isRight) { cellEl.classList.add('correct-pos'); piece.placed = true; }
  if (cellData) cellData.filled = true;
  if (piece.trayEl) { piece.trayEl.classList.add('used'); piece.trayEl.draggable = false; }
  JIG.dragging = null;
  jigUpdateStats();

  // Check for puzzle completion
  if (JIG.placed === JIG.total) {
    JIG.active = false; clearInterval(JIG.timer);
    setTimeout(function() {
      document.getElementById('jig-win-stats').innerHTML = JIG.grid + 'x' + JIG.grid + ' &nbsp;·&nbsp; ' + fmtTime(JIG.secs);
      document.getElementById('jig-win').classList.add('show');
    }, 400);
  }
}

/** Allow a wrongly-placed piece to be dragged back out of its cell. */
function jigSetupCellDrag(cellEl, piece, cellData) {
  cellEl.draggable = true;
  cellEl.ondragstart = function(e) {
    JIG.dragging = piece.id;
    e.dataTransfer.effectAllowed = 'move';
    setTimeout(function() {
      cellEl.innerHTML = ''; cellEl.classList.remove('done');
      if (cellData) cellData.filled = false;
      piece.placed = false;
      if (piece.trayEl) { piece.trayEl.classList.remove('used'); piece.trayEl.draggable = true; }
      cellEl.draggable = false; cellEl.ondragstart = null;
    }, 0);
  };
}

/** Render the small reference image in the right sidebar. */
function jigDrawRef() {
  var cv = document.getElementById('jig-ref'); if (!cv) return;
  var ctx = cv.getContext('2d'), src = jigDrawSrc(180, 180);
  ctx.drawImage(src, 0, 0, 180, 180);
  // Draw grid lines over the reference
  ctx.strokeStyle = 'rgba(255,255,255,.2)'; ctx.lineWidth = 1;
  var s = 180 / JIG.grid;
  for (var i = 1; i < JIG.grid; i++) {
    ctx.beginPath(); ctx.moveTo(i * s, 0); ctx.lineTo(i * s, 180); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(0, i * s); ctx.lineTo(180, i * s); ctx.stroke();
  }
}

/** Toggle a semi-transparent overlay showing the full completed picture. */
function jigTogglePreview() {
  JIG.showPreview = !JIG.showPreview;
  var ov = document.getElementById('jig-ov');
  var ca = document.querySelector('#jig-page .center-area');
  if (JIG.showPreview) {
    if (!ov) {
      ov = document.createElement('canvas'); ov.id = 'jig-ov';
      ov.style.cssText = 'position:absolute;inset:0;width:100%;height:100%;border-radius:18px;opacity:.65;z-index:10;pointer-events:none;';
      ca.style.position = 'relative'; ca.appendChild(ov);
    }
    var cs = jigCS(), w = cs * JIG.grid, h = cs * JIG.grid, pad = 32;
    ov.width = w + pad * 2; ov.height = h + pad * 2;
    ov.style.left = '-' + pad + 'px'; ov.style.top = '-' + pad + 'px';
    ov.getContext('2d').drawImage(jigDrawSrc(w, h), pad, pad, w, h);
    ov.style.display = 'block';
  } else if (ov) {
    ov.style.display = 'none';
  }
}

function jigUpdateStats() {
  var correct = JIG.pieces.filter(p => p.placed === true).length;
  var e1 = document.getElementById('jig-placed');
  var e2 = document.getElementById('jig-chip');
  var e3 = document.getElementById('jig-total');
  if (e1) e1.textContent = correct;
  if (e2) e2.textContent = correct + '/' + JIG.total + ' pieces';
  if (e3) e3.textContent = JIG.total;
}

function jigUpdateTime() {
  var t = fmtTime(JIG.secs);
  var e1 = document.getElementById('jig-stime');
  var e2 = document.getElementById('jig-time-chip');
  if (e1) e1.textContent = t;
  if (e2) e2.textContent = t;
}

/** Load a user-uploaded image as the custom jigsaw theme. */
function jigLoadCustom(input) {
  var file = input.files[0]; if (!file) return;
  var reader = new FileReader();
  reader.onload = function(e) {
    var img = new Image();
    img.onload = function() {
      JIG.customImg = img; JIG.img = 'custom';
      document.getElementById('upload-thumb').src = e.target.result;
      document.getElementById('upload-preview-wrap').style.display = 'block';
      document.querySelectorAll('.img-opt').forEach(o => o.classList.remove('on'));
      jigInit();
    };
    img.src = e.target.result;
  };
  reader.readAsDataURL(file);
}

function jigSetImg(btn, img) {
  document.querySelectorAll('.img-opt').forEach(o => o.classList.remove('on'));
  btn.classList.add('on');
  JIG.img = img;
  if (img !== 'custom') document.getElementById('upload-preview-wrap').style.display = 'none';
}

function jigSetGrid(btn, g) {
  document.querySelectorAll('#jig-page .diff-btn').forEach(b => b.classList.remove('on'));
  btn.classList.add('on');
  JIG.grid = g;
}

function jigNewGame() { jigInit(); }


// ============================================================
// PLATFORMER — Side-scrolling Canvas Game
// ============================================================
var PL_CANVAS = document.getElementById('gameCanvas');
var PL_CTX    = PL_CANVAS.getContext('2d');
var PW = PL_CANVAS.width, PH = PL_CANVAS.height;

// Global game state
var G = {
  running: false, level: 1, score: 0, lives: 3, timeLeft: 60,
  timer: null, raf: null, player: null,
  platforms: [], enemies: [], coins: [], particles: [], stars: [],
  camX: 0, keys: {}, tick: 0
};

/** Spawn coloured particle burst at (x, y). */
function spawnParts(x, y, col, n) {
  n = n || 8;
  for (var i = 0; i < n; i++)
    G.particles.push({ x: x, y: y, vx: (Math.random() - .5) * 7, vy: -(Math.random() * 5 + 1), life: 1, color: col, sz: Math.random() * 5 + 2 });
}

// ----- Draw helpers -----------------------------------------

function plDrawPlayer(x, y, w, h, dir) {
  var cx = x + w / 2;   // horizontal center
  var headR = w * 0.52; // big round head radius
  var bodyH = h * 0.42; // chubby body height
  var bodyY = y + h - bodyH; // body top
  var headCY = bodyY - headR * 0.55; // head center Y (overlaps body for chibi look)

  // --- Shadow (soft ellipse on the ground) ---
  PL_CTX.save();
  PL_CTX.globalAlpha = 0.18;
  PL_CTX.fillStyle = '#000';
  PL_CTX.beginPath();
  PL_CTX.ellipse(cx, y + h + 2, w * 0.45, 4, 0, 0, Math.PI * 2);
  PL_CTX.fill();
  PL_CTX.restore();

  // --- Tiny legs ---
  PL_CTX.fillStyle = '#1565c0';
  var legW = w * 0.22, legH = h * 0.18;
  // left leg
  PL_CTX.beginPath();
  PL_CTX.roundRect(cx - legW * 1.3, y + h - legH, legW, legH, 5);
  PL_CTX.fill();
  // right leg
  PL_CTX.beginPath();
  PL_CTX.roundRect(cx + legW * 0.3, y + h - legH, legW, legH, 5);
  PL_CTX.fill();
  // tiny shoes
  PL_CTX.fillStyle = '#0d1b3e';
  PL_CTX.beginPath(); PL_CTX.ellipse(cx - legW * 0.9,  y + h + 1, legW * 0.75, 4, 0, 0, Math.PI * 2); PL_CTX.fill();
  PL_CTX.beginPath(); PL_CTX.ellipse(cx + legW * 0.7,  y + h + 1, legW * 0.75, 4, 0, 0, Math.PI * 2); PL_CTX.fill();

  // --- Chubby body ---
  PL_CTX.fillStyle = '#29b6f6';
  PL_CTX.beginPath();
  PL_CTX.roundRect(x + w * 0.1, bodyY, w * 0.8, bodyH, [8, 8, 10, 10]);
  PL_CTX.fill();

  // Belly highlight stripe
  PL_CTX.fillStyle = 'rgba(255,255,255,0.25)';
  PL_CTX.beginPath();
  PL_CTX.roundRect(cx - w * 0.14, bodyY + 4, w * 0.28, bodyH * 0.55, 5);
  PL_CTX.fill();

  // --- Tiny arms (little rectangles sticking out the sides) ---
  PL_CTX.fillStyle = '#29b6f6';
  var armW = w * 0.18, armH = h * 0.22, armY = bodyY + 4;
  // left arm
  PL_CTX.beginPath();
  PL_CTX.roundRect(x - armW + w * 0.08, armY, armW, armH, 5);
  PL_CTX.fill();
  // right arm
  PL_CTX.beginPath();
  PL_CTX.roundRect(x + w - w * 0.08, armY, armW, armH, 5);
  PL_CTX.fill();
  // little hands (circles)
  PL_CTX.fillStyle = '#fff9c4';
  PL_CTX.beginPath(); PL_CTX.arc(x - armW * 0.3 + w * 0.08, armY + armH, armW * 0.48, 0, Math.PI * 2); PL_CTX.fill();
  PL_CTX.beginPath(); PL_CTX.arc(x + w - w * 0.08 + armW * 0.7, armY + armH, armW * 0.48, 0, Math.PI * 2); PL_CTX.fill();

  // --- Big round head ---
  PL_CTX.fillStyle = '#fff9c4'; // pale skin
  PL_CTX.beginPath();
  PL_CTX.arc(cx, headCY, headR, 0, Math.PI * 2);
  PL_CTX.fill();

  // Head sheen highlight
  PL_CTX.fillStyle = 'rgba(255,255,255,0.45)';
  PL_CTX.beginPath();
  PL_CTX.ellipse(cx - headR * 0.2, headCY - headR * 0.32, headR * 0.32, headR * 0.18, -0.4, 0, Math.PI * 2);
  PL_CTX.fill();

  // --- Cute hat / hair tuft ---
  PL_CTX.fillStyle = '#1565c0';
  PL_CTX.beginPath();
  PL_CTX.ellipse(cx, headCY - headR * 0.82, headR * 0.72, headR * 0.3, 0, Math.PI, 0); // hat brim
  PL_CTX.fill();
  PL_CTX.beginPath();
  PL_CTX.roundRect(cx - headR * 0.38, headCY - headR * 1.35, headR * 0.76, headR * 0.62, [8, 8, 0, 0]); // hat top
  PL_CTX.fill();
  // hat band
  PL_CTX.fillStyle = '#f9c74f';
  PL_CTX.fillRect(cx - headR * 0.38, headCY - headR * 0.96, headR * 0.76, headR * 0.14);
  // little star on hat
  PL_CTX.fillStyle = '#fff';
  PL_CTX.font = 'bold ' + Math.round(headR * 0.38) + 'px serif';
  PL_CTX.textAlign = 'center';
  PL_CTX.textBaseline = 'middle';
  PL_CTX.fillText('★', cx, headCY - headR * 1.06);

  // --- Big sparkly eyes ---
  var eyeOffX = headR * 0.33;
  var eyeY    = headCY + headR * 0.05;
  var eyeR    = headR * 0.28;
  var lEyeX   = cx - eyeOffX;
  var rEyeX   = cx + eyeOffX;

  // White sclera
  PL_CTX.fillStyle = '#ffffff';
  PL_CTX.beginPath(); PL_CTX.arc(lEyeX, eyeY, eyeR, 0, Math.PI * 2); PL_CTX.fill();
  PL_CTX.beginPath(); PL_CTX.arc(rEyeX, eyeY, eyeR, 0, Math.PI * 2); PL_CTX.fill();

  // Iris (facing direction)
  var irisShift = dir * eyeR * 0.18;
  PL_CTX.fillStyle = '#1a237e';
  PL_CTX.beginPath(); PL_CTX.arc(lEyeX + irisShift, eyeY + eyeR * 0.08, eyeR * 0.72, 0, Math.PI * 2); PL_CTX.fill();
  PL_CTX.beginPath(); PL_CTX.arc(rEyeX + irisShift, eyeY + eyeR * 0.08, eyeR * 0.72, 0, Math.PI * 2); PL_CTX.fill();

  // Pupil
  PL_CTX.fillStyle = '#000';
  PL_CTX.beginPath(); PL_CTX.arc(lEyeX + irisShift, eyeY + eyeR * 0.1, eyeR * 0.42, 0, Math.PI * 2); PL_CTX.fill();
  PL_CTX.beginPath(); PL_CTX.arc(rEyeX + irisShift, eyeY + eyeR * 0.1, eyeR * 0.42, 0, Math.PI * 2); PL_CTX.fill();

  // Sparkle dot (top-left of pupil)
  PL_CTX.fillStyle = '#fff';
  PL_CTX.beginPath(); PL_CTX.arc(lEyeX + irisShift - eyeR * 0.18, eyeY - eyeR * 0.06, eyeR * 0.18, 0, Math.PI * 2); PL_CTX.fill();
  PL_CTX.beginPath(); PL_CTX.arc(rEyeX + irisShift - eyeR * 0.18, eyeY - eyeR * 0.06, eyeR * 0.18, 0, Math.PI * 2); PL_CTX.fill();

  // Eyelashes (3 tiny lines above each eye)
  PL_CTX.strokeStyle = '#1a237e'; PL_CTX.lineWidth = 1.5; PL_CTX.lineCap = 'round';
  [-eyeR * 0.3, 0, eyeR * 0.3].forEach(function(ox) {
    PL_CTX.beginPath(); PL_CTX.moveTo(lEyeX + ox, eyeY - eyeR); PL_CTX.lineTo(lEyeX + ox, eyeY - eyeR * 1.32); PL_CTX.stroke();
    PL_CTX.beginPath(); PL_CTX.moveTo(rEyeX + ox, eyeY - eyeR); PL_CTX.lineTo(rEyeX + ox, eyeY - eyeR * 1.32); PL_CTX.stroke();
  });

  // --- Rosy cheeks ---
  PL_CTX.save();
  PL_CTX.globalAlpha = 0.38;
  PL_CTX.fillStyle = '#f48fb1';
  PL_CTX.beginPath(); PL_CTX.ellipse(lEyeX - eyeR * 0.1, eyeY + eyeR * 0.82, eyeR * 0.62, eyeR * 0.36, 0, 0, Math.PI * 2); PL_CTX.fill();
  PL_CTX.beginPath(); PL_CTX.ellipse(rEyeX + eyeR * 0.1, eyeY + eyeR * 0.82, eyeR * 0.62, eyeR * 0.36, 0, 0, Math.PI * 2); PL_CTX.fill();
  PL_CTX.restore();

  // --- Cute small nose ---
  PL_CTX.fillStyle = '#f9a825';
  PL_CTX.beginPath(); PL_CTX.arc(cx, eyeY + eyeR * 0.82, eyeR * 0.16, 0, Math.PI * 2); PL_CTX.fill();

  // --- Happy little smile ---
  PL_CTX.strokeStyle = '#c62828'; PL_CTX.lineWidth = 2; PL_CTX.lineCap = 'round';
  PL_CTX.beginPath();
  PL_CTX.arc(cx, eyeY + eyeR * 0.75, eyeR * 0.46, 0.2, Math.PI - 0.2);
  PL_CTX.stroke();

  // Reset textBaseline to avoid side-effects
  PL_CTX.textBaseline = 'alphabetic';
}

function plDrawEnemy(x, y, w, h) {
  // Body
  var bg = PL_CTX.createLinearGradient(x, y, x, y + h);
  bg.addColorStop(0, '#ef5350'); bg.addColorStop(1, '#b71c1c');
  PL_CTX.fillStyle = bg; PL_CTX.beginPath(); PL_CTX.roundRect(x, y, w, h, 8); PL_CTX.fill();

  // Horns
  PL_CTX.fillStyle = '#ff8f00';
  PL_CTX.beginPath(); PL_CTX.moveTo(x + 8, y); PL_CTX.lineTo(x + 3, y - 13); PL_CTX.lineTo(x + 15, y - 2); PL_CTX.fill();
  PL_CTX.beginPath(); PL_CTX.moveTo(x + w - 8, y); PL_CTX.lineTo(x + w - 3, y - 13); PL_CTX.lineTo(x + w - 15, y - 2); PL_CTX.fill();

  // Eyes
  PL_CTX.fillStyle = '#ffff00';
  PL_CTX.beginPath(); PL_CTX.arc(x + w * .3, y + h * .35, 5, 0, Math.PI * 2); PL_CTX.fill();
  PL_CTX.beginPath(); PL_CTX.arc(x + w * .7, y + h * .35, 5, 0, Math.PI * 2); PL_CTX.fill();
  PL_CTX.fillStyle = '#000';
  PL_CTX.beginPath(); PL_CTX.arc(x + w * .3, y + h * .37, 2.5, 0, Math.PI * 2); PL_CTX.fill();
  PL_CTX.beginPath(); PL_CTX.arc(x + w * .7, y + h * .37, 2.5, 0, Math.PI * 2); PL_CTX.fill();

  // Angry eyebrows
  PL_CTX.strokeStyle = '#000'; PL_CTX.lineWidth = 2.5;
  PL_CTX.beginPath(); PL_CTX.moveTo(x + 6,     y + h * .22); PL_CTX.lineTo(x + w * .38, y + h * .28); PL_CTX.stroke();
  PL_CTX.beginPath(); PL_CTX.moveTo(x + w - 6, y + h * .22); PL_CTX.lineTo(x + w * .62, y + h * .28); PL_CTX.stroke();

  // Mouth
  PL_CTX.strokeStyle = '#ffff00'; PL_CTX.lineWidth = 2;
  PL_CTX.beginPath(); PL_CTX.arc(x + w / 2, y + h * .65, 7, 0, Math.PI); PL_CTX.stroke();
}

function plDrawCoin(x, y) {
  var bob = Math.sin(G.tick * .06) * 4; // animated bobbing
  var cg = PL_CTX.createRadialGradient(x + 10, y + 10 + bob, 2, x + 10, y + 10 + bob, 11);
  cg.addColorStop(0, '#fff176'); cg.addColorStop(.5, '#ffd600'); cg.addColorStop(1, '#ff6f00');
  PL_CTX.fillStyle = cg;
  PL_CTX.beginPath(); PL_CTX.arc(x + 10, y + 10 + bob, 11, 0, Math.PI * 2); PL_CTX.fill();
  PL_CTX.strokeStyle = '#ffab00'; PL_CTX.lineWidth = 2;
  PL_CTX.beginPath(); PL_CTX.arc(x + 10, y + 10 + bob, 11, 0, Math.PI * 2); PL_CTX.stroke();
  PL_CTX.fillStyle = 'rgba(255,255,255,.5)';
  PL_CTX.beginPath(); PL_CTX.arc(x + 7, y + 7 + bob, 3.5, 0, Math.PI * 2); PL_CTX.fill();
}

function plDrawPlatform(x, y, w, h, type) {
  if (type === 'ground') {
    var gg = PL_CTX.createLinearGradient(x, y, x, y + h);
    gg.addColorStop(0, '#4caf50'); gg.addColorStop(.3, '#388e3c'); gg.addColorStop(1, '#1b5e20');
    PL_CTX.fillStyle = gg; PL_CTX.fillRect(x, y, w, h);
    PL_CTX.fillStyle = '#66bb6a'; PL_CTX.fillRect(x, y, w, 6); // grass strip on top
  } else {
    var pg = PL_CTX.createLinearGradient(x, y, x, y + h);
    pg.addColorStop(0, '#8d6e63'); pg.addColorStop(1, '#4e342e');
    PL_CTX.fillStyle = pg; PL_CTX.beginPath(); PL_CTX.roundRect(x, y, w, h, 6); PL_CTX.fill();
    PL_CTX.fillStyle = 'rgba(255,255,255,.08)'; PL_CTX.fillRect(x, y, w, 4); // highlight edge
  }
}

function plDrawFinish(x, y) {
  // Flag pole
  PL_CTX.fillStyle = '#bdbdbd'; PL_CTX.fillRect(x + 18, y - 60, 4, 60);
  // Waving flag
  var fw = 28, wave = Math.sin(G.tick * .07) * 4;
  PL_CTX.fillStyle = '#4ade80';
  PL_CTX.beginPath(); PL_CTX.moveTo(x + 22, y - 60); PL_CTX.lineTo(x + 22 + fw, y - 60 + fw / 2 + wave); PL_CTX.lineTo(x + 22, y - 60 + fw); PL_CTX.fill();
  // Star base marker
  PL_CTX.font = '20px serif'; PL_CTX.textAlign = 'center';
  PL_CTX.fillText('⭐', x + 20, y + 8);
}

/** Draw scrolling sky, stars, and moon for the current level. */
function plDrawBg() {
  var skies = { 1: ['#1a237e', '#283593'], 2: ['#4a148c', '#7b1fa2'] };
  var s = skies[G.level] || skies[1];
  var sky = PL_CTX.createLinearGradient(0, 0, 0, PH * .6);
  sky.addColorStop(0, s[0]); sky.addColorStop(1, s[1]);
  PL_CTX.fillStyle = sky; PL_CTX.fillRect(0, 0, PW, PH);

  // Generate stars once per level load
  if (!G.stars.length)
    for (var i = 0; i < 70; i++)
      G.stars.push({ x: Math.random() * 2400, y: Math.random() * PH * .5, r: Math.random() * 1.4 + .3 });

  // Stars scroll at parallax speed (30% of camera)
  G.stars.forEach(function(st) {
    var sx = ((st.x - G.camX * .3) % PW + PW) % PW;
    PL_CTX.fillStyle = 'rgba(255,255,255,.6)';
    PL_CTX.beginPath(); PL_CTX.arc(sx, st.y, st.r, 0, Math.PI * 2); PL_CTX.fill();
  });

  // Moon (parallax 15%)
  var mx = ((500 - G.camX * .15) % PW + PW) % PW;
  var mg = PL_CTX.createRadialGradient(mx, 55, 0, mx, 55, 32);
  mg.addColorStop(0, '#fffde7'); mg.addColorStop(1, '#fff59d');
  PL_CTX.fillStyle = mg; PL_CTX.beginPath(); PL_CTX.arc(mx, 55, 30, 0, Math.PI * 2); PL_CTX.fill();
}

// ----- Level data -------------------------------------------

/** Reset entity arrays and load the specified level's layout. */
function plLoadLevel(lvl) {
  G.camX = 0; G.particles = []; G.stars = [];

  var levels = {
    1: {
      platforms: [
        { x: 0,    y: 360, w: 1900, h: 60, t: 'ground' },
        { x: 280,  y: 295, w: 130,  h: 20, t: 'float'  },
        { x: 490,  y: 248, w: 130,  h: 20, t: 'float'  },
        { x: 710,  y: 208, w: 130,  h: 20, t: 'float'  },
        { x: 960,  y: 268, w: 130,  h: 20, t: 'float'  },
        { x: 1190, y: 228, w: 130,  h: 20, t: 'float'  },
        { x: 1410, y: 288, w: 130,  h: 20, t: 'float'  }
      ],
      enemies: [
        { x: 490,  y: 320, w: 38, h: 38, spd: 2,   dir: 1,  mn: 380,  mx: 700  },
        { x: 960,  y: 320, w: 38, h: 38, spd: 2.5, dir: 1,  mn: 820,  mx: 1100 },
        { x: 1300, y: 320, w: 38, h: 38, spd: 3,   dir: -1, mn: 1200, mx: 1520 }
      ],
      coins:  [{ x: 300, y: 263 }, { x: 508, y: 216 }, { x: 728, y: 175 }, { x: 978, y: 236 }, { x: 1208, y: 196 }, { x: 1428, y: 256 }],
      finish: { x: 1700, y: 290, w: 40, h: 70 }
    },
    2: {
      platforms: [
        { x: 0,    y: 360, w: 2200, h: 60, t: 'ground' },
        { x: 180,  y: 308, w: 100,  h: 20, t: 'float'  },
        { x: 360,  y: 262, w: 100,  h: 20, t: 'float'  },
        { x: 550,  y: 218, w: 100,  h: 20, t: 'float'  },
        { x: 750,  y: 175, w: 120,  h: 20, t: 'float'  },
        { x: 970,  y: 215, w: 100,  h: 20, t: 'float'  },
        { x: 1160, y: 262, w: 100,  h: 20, t: 'float'  },
        { x: 1390, y: 210, w: 120,  h: 20, t: 'float'  },
        { x: 1630, y: 265, w: 100,  h: 20, t: 'float'  }
      ],
      enemies: [
        { x: 360,  y: 320, w: 38, h: 38, spd: 3,   dir: 1,  mn: 270,  mx: 560  },
        { x: 750,  y: 320, w: 38, h: 38, spd: 3.5, dir: -1, mn: 610,  mx: 910  },
        { x: 1160, y: 320, w: 38, h: 38, spd: 4,   dir: 1,  mn: 1010, mx: 1310 },
        { x: 1630, y: 320, w: 38, h: 38, spd: 4.5, dir: -1, mn: 1510, mx: 1900 }
      ],
      coins:  [{ x: 198, y: 275 }, { x: 378, y: 230 }, { x: 568, y: 186 }, { x: 768, y: 142 }, { x: 988, y: 183 }, { x: 1178, y: 230 }, { x: 1408, y: 178 }, { x: 1648, y: 233 }],
      finish: { x: 2020, y: 295, w: 40, h: 70 }
    }
  };

  var data = levels[lvl] || levels[2];
  G.platforms = data.platforms;
  G.enemies   = data.enemies.map(e => ({ x: e.x, y: e.y, w: e.w, h: e.h, spd: e.spd, dir: e.dir, mn: e.mn, mx: e.mx, dead: false }));
  G.coins     = data.coins.map(c  => ({ x: c.x, y: c.y, w: 20, h: 20, got: false }));
  G.finish    = data.finish;
  G.player    = { x: 100, y: 280, w: 36, h: 50, vx: 0, vy: 0, dir: 1, onGround: false, jumps: 0 };
}

// ----- Game state transitions --------------------------------

function plRespawn() {
  G.lives--;
  plUpdateHUD();
  spawnParts(G.player.x - G.camX, G.player.y, '#f72585', 14);
  if (G.lives <= 0) {
    platGameOver('GAME OVER', 'All lives used up!');
  } else {
    G.player.x = 100; G.player.y = 280;
    G.player.vx = 0;  G.player.vy = 0;
    G.camX = 0;
  }
}

function plNextLevel() {
  G.level++; G.score += 50;
  if (G.level > 2) {
    platWin();
  } else {
    plLoadLevel(G.level); plUpdateHUD();
    showOverlay('LEVEL ' + G.level, 'Next level! Even harder now!', 'CONTINUE', platStart);
  }
}

function platWin() {
  platStop();
  showOverlay('YOU WIN!', 'Score: ' + G.score + ' — Excellent!', 'PLAY AGAIN', function() {
    G.level = 1; G.score = 0; G.lives = 3; G.timeLeft = 60; platStart();
  });
}

function platGameOver(title, sub) {
  platStop();
  showOverlay(title, sub + ' | Score: ' + G.score, 'TRY AGAIN', function() {
    G.level = 1; G.score = 0; G.lives = 3; G.timeLeft = 60; platStart();
  });
}

function showOverlay(title, sub, btnLabel, cb) {
  var ov = document.getElementById('plat-overlay');
  document.getElementById('ov-title').textContent = title;
  document.getElementById('ov-sub').textContent   = sub;
  var b = document.getElementById('ov-btn');
  b.textContent = btnLabel;
  b.onclick = cb;
  ov.classList.remove('hidden');
}

function plUpdateHUD() {
  document.getElementById('p-score-chip').textContent = 'Score: ' + G.score;
  document.getElementById('p-lives-chip').textContent = 'Lives: ' + G.lives;
  document.getElementById('p-time-chip').textContent  = G.timeLeft + 's';
  document.getElementById('p-level-chip').textContent = 'Level ' + G.level;
}

// ----- Game loop --------------------------------------------

function platStart() {
  document.getElementById('plat-overlay').classList.add('hidden');
  plLoadLevel(G.level); plUpdateHUD();
  G.running = true; G.stars = [];
  clearInterval(G.timer);
  G.timer = setInterval(function() {
    G.timeLeft--; plUpdateHUD();
    if (G.timeLeft <= 0) platGameOver('TIME UP!', 'Time has run out!');
  }, 1000);
  G.raf = requestAnimationFrame(platLoop);
}

function platStop() {
  G.running = false;
  cancelAnimationFrame(G.raf);
  clearInterval(G.timer);
}

function platLoop() {
  if (!G.running) return;
  G.tick++;
  PL_CTX.clearRect(0, 0, PW, PH);
  plDrawBg();

  var pl = G.player;

  // --- Input → velocity ---
  if (G.keys['ArrowLeft']  || G.keys['a']) { pl.vx = -4.5; pl.dir = -1; }
  else if (G.keys['ArrowRight'] || G.keys['d']) { pl.vx = 4.5;  pl.dir =  1; }
  else pl.vx *= .7; // friction when no key held

  // --- Gravity ---
  pl.vy += 0.55;
  if (pl.vy > 14) pl.vy = 14; // terminal velocity
  pl.x += pl.vx;
  pl.y += pl.vy;
  if (pl.x < 0) pl.x = 0;

  // --- Platform collision ---
  pl.onGround = false;
  G.platforms.forEach(function(p) {
    // Land on top
    if (pl.x + pl.w > p.x && pl.x < p.x + p.w && pl.y + pl.h > p.y && pl.y + pl.h < p.y + p.h + 16 && pl.vy >= 0) {
      pl.y = p.y - pl.h; pl.vy = 0; pl.onGround = true; pl.jumps = 0;
    }
    // Hit the underside
    if (pl.x + pl.w > p.x && pl.x < p.x + p.w && pl.y < p.y + p.h && pl.y + pl.h > p.y && !pl.onGround && pl.vy < 0) {
      pl.vy = 2;
    }
  });

  // Fell off the bottom → respawn
  if (pl.y > PH + 30) plRespawn();

  // --- Smooth camera follow (lerp) ---
  var tc = pl.x - PW / 3;
  G.camX += (tc - G.camX) * .12;
  if (G.camX < 0) G.camX = 0;

  // --- Draw platforms ---
  G.platforms.forEach(p => plDrawPlatform(p.x - G.camX, p.y, p.w, p.h, p.t));

  // --- Coins ---
  G.coins.forEach(function(c) {
    if (c.got) return;
    plDrawCoin(c.x - G.camX, c.y);
    if (pl.x < c.x + c.w && pl.x + pl.w > c.x && pl.y < c.y + c.h && pl.y + pl.h > c.y) {
      c.got = true; G.score += 10;
      spawnParts(c.x - G.camX + 10, c.y, '#ffd600', 10);
      plUpdateHUD();
    }
  });

  // --- Enemies ---
  G.enemies.forEach(function(e) {
    if (e.dead) return;
    e.x += e.spd * e.dir;
    if (e.x < e.mn || e.x > e.mx) e.dir *= -1; // bounce between patrol bounds
    plDrawEnemy(e.x - G.camX, e.y, e.w, e.h);

    // Collision with player
    if (pl.x + pl.w - 5 > e.x && pl.x + 5 < e.x + e.w && pl.y + pl.h > e.y && pl.y < e.y + e.h) {
      if (pl.vy > 0 && pl.y + pl.h < e.y + e.h * .5 + 12) {
        // Stomped the enemy from above
        e.dead = true; pl.vy = -9; G.score += 20;
        spawnParts(e.x - G.camX + e.w / 2, e.y, '#ef5350', 14);
        plUpdateHUD();
      } else {
        // Player ran into the enemy
        plRespawn();
      }
    }
  });

  // --- Finish flag ---
  var f = G.finish;
  plDrawFinish(f.x - G.camX, f.y);
  if (pl.x + pl.w > f.x && pl.x < f.x + f.w && pl.y + pl.h > f.y && pl.y < f.y + f.h + f.h) plNextLevel();

  // --- Particles ---
  G.particles = G.particles.filter(p => p.life > 0);
  G.particles.forEach(function(p) {
    p.x += p.vx; p.y += p.vy; p.vy += .3; p.life -= .04;
    PL_CTX.save();
    PL_CTX.globalAlpha = p.life;
    PL_CTX.fillStyle = p.color;
    PL_CTX.beginPath(); PL_CTX.arc(p.x, p.y, p.sz, 0, Math.PI * 2); PL_CTX.fill();
    PL_CTX.restore();
  });

  // --- Player (drawn last so it appears on top) ---
  plDrawPlayer(pl.x - G.camX, pl.y, pl.w, pl.h, pl.dir);

  G.raf = requestAnimationFrame(platLoop);
}

// ----- Keyboard handling ------------------------------------

document.addEventListener('keydown', function(e) {
  G.keys[e.key] = true;

  // Jump (up to 2 times)
  if (document.getElementById('plat-page').classList.contains('active')) {
    if ((e.key === ' ' || e.key === 'ArrowUp') && G.player && G.player.jumps < 2) {
      e.preventDefault();
      G.player.vy = -12;
      G.player.jumps++;
      spawnParts(G.player.x - G.camX + G.player.w / 2, G.player.y + G.player.h, '#4fc3f7', 5);
    }
  }
});

document.addEventListener('keyup', function(e) { G.keys[e.key] = false; });
</script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML)


if __name__ == "__main__":
    print("=" * 45)
    print("  🎮  GameVerse is running!")
    print("  🌐  Open: http://localhost:5000")
    print("=" * 45)
    app.run(debug=False)