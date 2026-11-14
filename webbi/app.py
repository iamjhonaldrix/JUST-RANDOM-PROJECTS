from flask import Flask, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>For Raines ❤️</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
            overflow-x: hidden;
        }
        .card {
            background: #ffffff;
            max-width: 520px;
            width: 100%;
            border-radius: 24px;
            padding: 40px 30px;
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.12);
            text-align: center;
            position: relative;
            z-index: 10;
        }
        .heart-icon {
            font-size: 55px;
            cursor: pointer;
            user-select: none;
            display: inline-block;
            transition: transform 0.2s ease;
        }
        .heart-icon:hover {
            transform: scale(1.2);
        }
        h1 {
            color: #2c3e50;
            font-size: 2.2rem;
            margin: 10px 0 15px;
        }
        p.message {
            color: #555555;
            font-size: 1.05rem;
            line-height: 1.6;
            margin-bottom: 25px;
        }
        .btn-group {
            display: flex;
            flex-direction: column;
            gap: 12px;
            margin-bottom: 25px;
        }
        .btn {
            background: #ff4b2b;
            color: white;
            border: none;
            padding: 12px 24px;
            font-size: 0.95rem;
            font-weight: 600;
            border-radius: 30px;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(255, 75, 43, 0.3);
            transition: all 0.2s ease;
        }
        .btn:hover {
            background: #e03e20;
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(255, 75, 43, 0.4);
        }
        .btn-secondary {
            background: #f0f0f0;
            color: #444;
            box-shadow: none;
        }
        .btn-secondary:hover {
            background: #e2e2e2;
            color: #111;
            box-shadow: none;
        }
        .interactive-box {
            background: #fff5f6;
            border: 2px dashed #ffb6c1;
            border-radius: 16px;
            padding: 15px 20px;
            font-size: 1rem;
            color: #d63384;
            font-weight: 600;
            min-height: 60px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: opacity 0.3s ease;
        }
        .floating-heart {
            position: fixed;
            pointer-events: none;
            animation: floatUp 2s ease-out forwards;
            font-size: 24px;
            z-index: 100;
        }
        @keyframes floatUp {
            0% {
                opacity: 1;
                transform: translateY(0) scale(1);
            }
            100% {
                opacity: 0;
                transform: translateY(-120px) scale(1.5);
            }
        }
    </style>
</head>
<body>
    <div class="card">
        <div class="heart-icon" id="mainHeart">❤️</div>
        <h1>Hi, Raine!</h1>
        
        <p class="message">
            Just a gentle reminder of how incredibly special you are. Thank you for bringing so much light, comfort, and warmth into every single day.
        </p>

        <div class="btn-group">
            <button class="btn" onclick="nextReason()">Tap for a Reason why you're awesome ✨</button>
            <button class="btn btn-secondary" onclick="sendLove(event)">Send Love back 💖</button>
        </div>

        <div class="interactive-box" id="reasonBox">
            Click the button above to unlock a message!
        </div>
    </div>

    <script>
        const reasons = [
            "Your smile effortlessly brightens up the entire room. ✨",
            "You have the sweetest, most caring heart. ❤️",
            "Even quiet moments with you feel special and peaceful. 🌙",
            "You bring so much joy into every ordinary day. ☀️",
            "Thank you for simply being you you're truly unmatched. 👑"
        ];

        let index = 0;

        function nextReason() {
            const box = document.getElementById("reasonBox");
            box.innerText = reasons[index];
            index = (index + 1) % reasons.length;
            spawnHeartAtCenter();
        }

        function sendLove(e) {
            const box = document.getElementById("reasonBox");
            box.innerText = "Love received! Sending tons of warm hugs back to you! 🤗💌";
            
            // Spawn multiple hearts on click
            for (let i = 0; i < 6; i++) {
                setTimeout(() => {
                    const x = e.clientX + (Math.random() * 60 - 30);
                    const y = e.clientY + (Math.random() * 60 - 30);
                    createHeart(x, y);
                }, i * 80);
            }
        }

        document.getElementById("mainHeart").addEventListener("click", (e) => {
            createHeart(e.clientX, e.clientY);
        });

        function spawnHeartAtCenter() {
            const rect = document.getElementById("mainHeart").getBoundingClientRect();
            createHeart(rect.left + rect.width / 2, rect.top + rect.height / 2);
        }

        function createHeart(x, y) {
            const heart = document.createElement("div");
            heart.className = "floating-heart";
            heart.innerText = ["❤️", "💖", "💕", "✨", "🌸"][Math.floor(Math.random() * 5)];
            heart.style.left = `${x - 12}px`;
            heart.style.top = `${y - 12}px`;
            document.body.appendChild(heart);

            setTimeout(() => {
                heart.remove();
            }, 2000);
        }
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
