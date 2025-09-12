import csv
import re

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

def generate_html(videos, output_file="index.html"):
    """Generate Tinder-like swipe + Reels-like scroll site with overlays visible for 0.5s"""
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>YouTube Swipe Website</title>
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
                height: 640px; /* 9:16 */
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
                justify-content: space-between;
                align-items: center;
                padding: 10px;
                box-sizing: border-box;
                transition: transform 0.4s ease, opacity 0.4s ease;
            }
            img {
                width: 100%;
                max-height: 70%;
                border-radius: 12px;
                object-fit: cover;
            }
            h2 {
                color: white;
                margin: 10px 0;
                text-align: center;
                font-size: 16px;
            }
            .watch-now {
                width: 90%;
                background: #e50914;
                color: white;
                text-align: center;
                padding: 12px;
                margin-bottom: 20px;
                border-radius: 10px;
                font-size: 18px;
                font-weight: bold;
                text-decoration: none;
                transition: background 0.3s;
            }
            .watch-now:hover {
                background: #b20710;
            }
            /* Animated overlays */
            .overlay {
                position: fixed;
                top: 40%;
                left: 50%;
                transform: translate(-50%, -50%) scale(0.8);
                font-size: 42px;
                font-weight: bold;
                opacity: 0;
                pointer-events: none;
                transition: opacity 0.5s ease, transform 0.5s ease;
                z-index: 9999;
                text-align: center;
            }
            .overlay.show {
                opacity: 1;
                transform: translate(-50%, -50%) scale(1);
            }
            .overlay.interested {
                color: #00ff88;
                text-shadow: 0 0 20px #00ff88;
            }
            .overlay.not {
                color: #ff4444;
                text-shadow: 0 0 20px #ff4444;
            }
        </style>
    </head>
    <body>
        <div class="phone" id="phone">
    """
    for i, (title, url, thumb) in enumerate(videos):
        html += f"""
            <div class="card" style="z-index:{len(videos)-i}">
                <img src="{thumb}" alt="{title}">
                <h2>{title}</h2>
                <a href="{url}" target="_blank" class="watch-now">▶ Watch Now</a>
            </div>
        """

    # Global overlay elements
    html += """
        </div>
        <div class="overlay interested" id="interestedOverlay">INTERESTED</div>
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
                }, 500); // overlay now stays for 0.5 seconds
            }

            showCard(current);

            // Keyboard control
            document.addEventListener('keydown', (e) => {
                if (e.key === 'ArrowRight') {
                    swipeCard('right');
                } else if (e.key === 'ArrowLeft') {
                    swipeCard('left');
                } else if (e.key === 'ArrowUp') {
                    swipeCard('up'); // skip like reels
                }
            });

            // Touch swipe
            let startX = 0, startY = 0;
            document.getElementById('phone').addEventListener('touchstart', e => {
                startX = e.touches[0].clientX;
                startY = e.touches[0].clientY;
            });
            document.getElementById('phone').addEventListener('touchend', e => {
                let endX = e.changedTouches[0].clientX;
                let endY = e.changedTouches[0].clientY;
                let diffX = endX - startX;
                let diffY = startY - endY;
                if (Math.abs(diffX) > Math.abs(diffY)) {
                    if (diffX > 50) {
                        swipeCard('right');
                    } else if (diffX < -50) {
                        swipeCard('left');
                    }
                } else {
                    if (diffY > 50) {
                        swipeCard('up'); // reels-like skip
                    }
                }
            });
        </script>
    </body>
    </html>
    """
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ Website generated: {output_file}")

def main():
    videos = []
    with open("videos.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            title = row["title"].strip()
            url = row["url"].strip()
            video_id = extract_video_id(url)
            if video_id:
                thumb = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
                videos.append((title, url, thumb))
            else:
                print(f"⚠️ Skipping invalid URL: {url}")
    generate_html(videos)

if __name__ == "__main__":
    main()
