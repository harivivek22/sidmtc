import csv
import re
import os

def extract_video_id(url: str) -> str:
    """Extract the YouTube video ID from different URL formats"""
    match = re.search(r"youtu\.be/([A-Za-z0-9_-]{11})", url)
    if match:
        return match.group(1)
    match = re.search(r"v=([A-Za-z0-9_-]{11})", url)
    if match:
        return match.group(1)
    match = re.search(r"embed/([A-Za-z0-9_-]{11})", url)
    if match:
        return match.group(1)
    return None


def generate_homepage(output_file="home.html"):
    """Generate a modern homepage"""
    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>TFI WIKI - Home</title>
  <style>
    body {
      margin: 0;
      height: 100vh;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      background: linear-gradient(135deg, #0f0f0f, #1c1c1c);
      font-family: Arial, sans-serif;
      color: white;
      text-align: center;
    }
    h1 {
      font-size: 40px;
      font-weight: bold;
      margin-bottom: 20px;
      color: #e50914;
      text-shadow: 0 0 10px rgba(229, 9, 20, 0.8);
      letter-spacing: 2px;
    }
    a img {
      width: 320px;
      max-width: 80%;
      border-radius: 16px;
      margin-bottom: 25px;
      box-shadow: 0 8px 25px rgba(0,0,0,0.6);
      transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    a img:hover {
      transform: scale(1.07);
      box-shadow: 0 12px 35px rgba(229, 9, 20, 0.8);
    }
    .tagline {
      font-size: 14px;
      color: #aaa;
      margin-top: 10px;
      letter-spacing: 1px;
    }
    footer {
      position: absolute;
      bottom: 15px;
      font-size: 13px;
      color: #555;
    }
  </style>
</head>
<body>
  <h1>TFI WIKI</h1>
  <a href="index.html">
    <img src="https://upload.wikimedia.org/wikipedia/en/0/0c/OG_Poster.jpg" alt="OG Poster">
  </a>
  <div class="tagline">Click the poster to explore</div>
  <footer>© 2025 TFI WIKI | All Rights Reserved</footer>
</body>
</html>
"""
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ Modern homepage generated: {output_file}")


def generate_swipe(videos, categories, output_file="index.html"):
    """Generate swipe site with videos + categories gallery"""
    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1, user-scalable=no">
  <title>Swipe Website</title>
  <style>
    body {
      margin: 0;
      height: 100vh;
      display: flex;
      justify-content: center;
      align-items: center;
      background: #111;
      font-family: Arial, sans-serif;
      overflow: hidden;
    }
    .phone {
      width: 360px;
      height: 640px;
      background: #222;
      border-radius: 20px;
      overflow: hidden;
      position: relative;
      box-shadow: 0 6px 20px rgba(0,0,0,0.5);
    }
    .card {
      position: absolute;
      width: 100%;
      height: 100%;
      display: flex;
      flex-direction: column;
      justify-content: flex-start;
      align-items: center;
      padding: 10px;
      box-sizing: border-box;
      transition: transform 0.4s ease, opacity 0.4s ease;
      overflow-y: auto;
    }
    img {
      width: 100%;
      height: 75%;
      border-radius: 12px;
      object-fit: cover;
    }
    h2 {
      color: white;
      margin: 10px 0;
      text-align: center;
      font-size: 16px;
    }
    .watch-now, .visit-now {
      width: 90%;
      text-align: center;
      padding: 12px;
      margin-bottom: 20px;
      border-radius: 10px;
      font-size: 18px;
      font-weight: bold;
      text-decoration: none;
      transition: background 0.3s;
      display: inline-block;
    }
    .watch-now { background: #e50914; color: white; }
    .visit-now { background: #007bff; color: white; }
    .overlay {
      position: fixed;
      top: 40%;
      left: 50%;
      transform: translate(-50%, -50%) scale(0.8);
      font-size: 32px;
      font-weight: bold;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.5s ease, transform 0.5s ease;
      z-index: 9999;
      text-align: center;
      padding: 20px 40px;
      border-radius: 20px;
      background: rgba(0, 0, 0, 0.7);
    }
    .overlay.show { opacity: 1; transform: translate(-50%, -50%) scale(1); }
    .overlay.interested { color: #00ff88; text-shadow: 0 0 20px #00ff88; }
    .overlay.not { color: #ff4444; text-shadow: 0 0 20px #ff4444; }

    /* Categories page */
    .categories {
      width: 100%;
    }
    .category-block {
      margin-bottom: 20px;
    }
    .category-block h3 {
      color: #e50914;
      font-size: 18px;
      margin-bottom: 10px;
    }
    .thumb-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 10px;
    }
    .thumb-grid a img {
      width: 100%;
      height: 100px;
      object-fit: cover;
      border-radius: 8px;
      transition: transform 0.3s;
    }
    .thumb-grid a img:hover {
      transform: scale(1.05);
    }
  </style>
</head>
<body>
  <div class="phone" id="phone">
"""
    for i, (title, url, thumb, is_youtube) in enumerate(videos):
        button_class = "watch-now" if is_youtube else "visit-now"
        button_text = "▶ Watch Now" if is_youtube else "🌐 Visit Now"
        html += f"""
    <div class="card" style="z-index:{len(videos)-i+1}">
      <img src="{thumb}" alt="{title}">
      <h2>{title}</h2>
      <a href="{url}" target="_blank" class="{button_class}">{button_text}</a>
    </div>
"""

    # Categories tab
    html += """
    <div class="card" style="z-index:1">
      <h2>Browse by Category</h2>
      <div class="categories">
"""
    for category, items in categories.items():
        html += f"""        <div class="category-block">
          <h3>{category}</h3>
          <div class="thumb-grid">
"""
        for (title, url, thumb, _) in items:
            html += f"""            <a href="{url}" target="_blank"><img src="{thumb}" alt="{title}"></a>\n"""
        html += """          </div>
        </div>
"""

    html += """      </div>
    </div>
"""

    html += """
  </div>
  <div class="overlay interested" id="interestedOverlay">MARKED AS WATCHED</div>
  <div class="overlay not" id="notOverlay">NOT INTERESTED</div>
  <script>
    let cards = document.querySelectorAll('.card');
    let current = 0;
    const interestedOverlay = document.getElementById('interestedOverlay');
    const notOverlay = document.getElementById('notOverlay');

    function showCard(index) {
      cards.forEach((card, i) => {
        if (i === index) {
          card.style.transform = 'translateY(0)';
          card.style.opacity = '1';
          card.style.pointerEvents = "auto";
        } else if (i < index) {
          card.style.opacity = '0';
          card.style.pointerEvents = "none";
        } else {
          card.style.transform = 'translateY(100%)';
          card.style.opacity = '0';
          card.style.pointerEvents = "none";
        }
      });
    }

    function swipeCard(action) {
      if (current >= cards.length) return;
      let card = cards[current];
      if (action === 'right') {
        interestedOverlay.classList.add('show');
        card.style.transform = 'translateX(100%) rotate(15deg)';
      } else if (action === 'left') {
        notOverlay.classList.add('show');
        card.style.transform = 'translateX(-100%) rotate(-15deg)';
      } else if (action === 'up') {
        card.style.transform = 'translateY(-100%)';
      }
      setTimeout(() => {
        if (action === 'right') interestedOverlay.classList.remove('show');
        if (action === 'left') notOverlay.classList.remove('show');
        current++;
        if (current < cards.length) {
          showCard(current);
        }
      }, 500);
    }

    showCard(current);

    document.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowRight') swipeCard('right');
      else if (e.key === 'ArrowLeft') swipeCard('left');
      else if (e.key === 'ArrowUp') swipeCard('up');
    });

    let startX = 0, startY = 0;
    document.getElementById('phone').addEventListener('touchstart', e => {
      startX = e.touches[0].clientX;
      startY = e.touches[0].clientY;
    }, { passive: true });
    document.getElementById('phone').addEventListener('touchend', e => {
      let endX = e.changedTouches[0].clientX;
      let endY = e.changedTouches[0].clientY;
      let diffX = endX - startX;
      let diffY = startY - endY;
      if (Math.abs(diffX) > Math.abs(diffY)) {
        if (diffX > 50) swipeCard('right');
        else if (diffX < -50) swipeCard('left');
      } else {
        if (diffY > 50) swipeCard('up');
      }
    }, { passive: true });
  </script>
</body>
</html>
"""
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ Swipe site with categories generated: {output_file}")


def main():
    videos = []
    categories = {"🎵 Music": [], "🎬 Movies": [], "🛍 Merchandise": [], "⭐ Others": []}

    with open("videos.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            title = row["title"].strip()
            url = row["url"].strip()
            thumb = row.get("thumbnail", "").strip()
            video_id = extract_video_id(url)

            # Special case: The OG Merchandise → custom thumbnail
            if title.lower() == "the og merchandise":
                thumb = "https://theogwear.com/cdn/shop/files/logo.png"

            if not thumb and video_id:
                thumb = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
            if not thumb:
                thumb = "https://via.placeholder.com/360x200.png?text=Website+Preview"

            is_youtube = bool(video_id)
            video_entry = (title, url, thumb, is_youtube)
            videos.append(video_entry)

            # Categorize
            if title.startswith("MV"):
                categories["🎵 Music"].append(video_entry)
            elif title.startswith("M"):
                categories["🎬 Movies"].append(video_entry)
            elif "merch" in title.lower():
                categories["🛍 Merchandise"].append(video_entry)
            else:
                categories["⭐ Others"].append(video_entry)

    generate_swipe(videos, categories)
    generate_homepage()


if __name__ == "__main__":
    main()
