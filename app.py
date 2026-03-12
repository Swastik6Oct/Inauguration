import streamlit as st
import streamlit.components.v1 as components
import base64
import os
import html

st.set_page_config(page_title="Digital Inauguration Ceremony", layout="wide")

DEFAULT_TEXT = """Inauguration of
Sabha Griha

by
General Manager
East Coast Railway

15 March 2026"""


def file_to_b64(path: str) -> str:
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return ""


cut_b64 = file_to_b64("cut.wav")
curtain_b64 = file_to_b64("curtain.wav")
reveal_b64 = file_to_b64("reveal.wav")

if "run_id" not in st.session_state:
    st.session_state.run_id = 0

with st.sidebar:
    st.header("Ceremony Controls")
    message = st.text_area("Text to reveal", value=DEFAULT_TEXT, height=180)
    font_size = st.slider("Font size", 26, 72, 42, 2)
    text_color = st.selectbox("Text color", ["#d4af37", "#f2d36b", "#cfa228", "#ffffff"], index=0)
    cut_clicked = st.button("✂ Cut Ribbon", use_container_width=True)
    reset_clicked = st.button("Reset", use_container_width=True)

if cut_clicked:
    st.session_state.run_id += 1

if reset_clicked:
    st.session_state.run_id = 0

safe_message = html.escape(message).replace("\n", "<br>")
run_id = st.session_state.run_id

cut_audio = f"""
<audio id="cutAudio" preload="auto">
  <source src="data:audio/wav;base64,{cut_b64}" type="audio/wav">
</audio>
""" if cut_b64 else ""

curtain_audio = f"""
<audio id="curtainAudio" preload="auto">
  <source src="data:audio/wav;base64,{curtain_b64}" type="audio/wav">
</audio>
""" if curtain_b64 else ""

reveal_audio = f"""
<audio id="revealAudio" preload="auto">
  <source src="data:audio/wav;base64,{reveal_b64}" type="audio/wav">
</audio>
""" if reveal_b64 else ""

html_code = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
<style>
    body {{
        margin: 0;
        background: #170306;
        overflow: hidden;
        font-family: Georgia, serif;
    }}

    .wrap {{
        width: 100%;
        height: 760px;
        display: flex;
        justify-content: center;
        align-items: center;
        background: radial-gradient(circle at center, #2d0b12 0%, #170306 100%);
    }}

    .stage {{
        position: relative;
        width: 1120px;
        height: 720px;
        background: #3a0d12;
        border: 8px solid #b88b2a;
        box-sizing: border-box;
        overflow: hidden;
    }}

    .inner {{
        position: absolute;
        inset: 18px;
        background: #101010;
        border: 3px solid #d4af37;
        box-sizing: border-box;
    }}

    .header {{
        position: absolute;
        left: 170px;
        right: 170px;
        top: 24px;
        height: 86px;
        background: #050505;
        border: 3px solid #d4af37;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        color: #d4af37;
        letter-spacing: 0.5px;
    }}

    .header .line1 {{
        font-size: 32px;
        font-weight: 700;
    }}

    .header .line2 {{
        font-size: 20px;
        font-weight: 700;
        color: #f2d36b;
        margin-top: 6px;
    }}

    .rod {{
        position: absolute;
        top: 118px;
        left: 72px;
        right: 72px;
        height: 14px;
        background: linear-gradient(to right, #8e6c12, #d4af37, #8e6c12);
    }}

    .opening {{
        position: absolute;
        top: 133px;
        left: 56px;
        right: 56px;
        bottom: 48px;
        background: #0b0b0b;
        overflow: hidden;
    }}

    .text-layer {{
        position: absolute;
        top: 180px;
        left: 120px;
        right: 120px;
        bottom: 110px;
        display: flex;
        justify-content: center;
        align-items: center;
        text-align: center;
        color: {text_color};
        font-size: {font_size}px;
        font-weight: 700;
        line-height: 1.35;
        opacity: 0;
    }}

    .text-box {{
        max-width: 100%;
        word-break: break-word;
    }}

    .valance {{
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 84px;
        background:
            radial-gradient(circle at 5% -10%, transparent 52px, #7a1024 53px),
            radial-gradient(circle at 16% -10%, transparent 52px, #7a1024 53px),
            radial-gradient(circle at 27% -10%, transparent 52px, #7a1024 53px),
            radial-gradient(circle at 38% -10%, transparent 52px, #7a1024 53px),
            radial-gradient(circle at 49% -10%, transparent 52px, #7a1024 53px),
            radial-gradient(circle at 60% -10%, transparent 52px, #7a1024 53px),
            radial-gradient(circle at 71% -10%, transparent 52px, #7a1024 53px),
            radial-gradient(circle at 82% -10%, transparent 52px, #7a1024 53px),
            radial-gradient(circle at 93% -10%, transparent 52px, #7a1024 53px);
        border-bottom: 2px solid #55101a;
        z-index: 4;
    }}

    .curtain {{
        position: absolute;
        top: 62px;
        bottom: 0;
        width: 52%;
        background:
            repeating-linear-gradient(
                90deg,
                #62101f 0px,
                #62101f 10px,
                #7a1024 10px,
                #7a1024 26px,
                #99283b 26px,
                #99283b 30px,
                #7a1024 30px,
                #7a1024 46px
            );
        z-index: 3;
        transition: transform 3.6s ease-in-out;
    }}

    .curtain.left {{
        left: 0;
        border-right: 2px solid #561019;
    }}

    .curtain.right {{
        right: 0;
        border-left: 2px solid #561019;
    }}

    .tie {{
        position: absolute;
        top: 210px;
        width: 34px;
        height: 34px;
        border-radius: 50%;
        background: #d4af37;
        border: 2px solid #8e6c12;
        z-index: 5;
    }}

    .tie.left {{ right: -16px; }}
    .tie.right {{ left: -16px; }}

    .ribbon-zone {{
        position: absolute;
        left: 120px;
        right: 120px;
        bottom: 96px;
        height: 90px;
        z-index: 6;
    }}

    .ribbon-left, .ribbon-right {{
        position: absolute;
        top: 34px;
        height: 18px;
        background: #cf0000;
        border-radius: 999px;
        box-shadow: 0 -4px 0 #ff9a9a inset;
    }}

    .ribbon-left {{
        left: 0;
        width: calc(50% - 62px);
        transform-origin: right center;
    }}

    .ribbon-right {{
        right: 0;
        width: calc(50% - 62px);
        transform-origin: left center;
    }}

    .knot {{
        position: absolute;
        left: 50%;
        top: 25px;
        transform: translateX(-50%);
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background: #b30000;
        border: 2px solid #7a0000;
    }}

    .bow-left, .bow-right {{
        position: absolute;
        top: 18px;
        width: 36px;
        height: 36px;
        background: #c40000;
        border: 2px solid #7a0000;
    }}

    .bow-left {{
        left: calc(50% - 40px);
        clip-path: polygon(100% 50%, 0 0, 32% 50%, 0 100%);
    }}

    .bow-right {{
        left: calc(50% + 4px);
        clip-path: polygon(0 50%, 100% 0, 68% 50%, 100% 100%);
    }}

    .tail-left, .tail-right {{
        position: absolute;
        top: 47px;
        width: 16px;
        height: 34px;
        background: #aa0000;
        border: 1px solid #7a0000;
    }}

    .tail-left {{
        left: calc(50% - 12px);
        clip-path: polygon(0 0, 100% 0, 50% 100%);
    }}

    .tail-right {{
        left: calc(50% + 2px);
        clip-path: polygon(0 0, 100% 0, 50% 100%);
    }}

    .scissor {{
        position: absolute;
        left: 50%;
        top: 12px;
        transform: translateX(-50%);
        font-size: 46px;
        color: #f2f2f2;
        transition: opacity 1.6s linear;
        z-index: 7;
    }}

    .confetti {{
        position: absolute;
        inset: 0;
        pointer-events: none;
        z-index: 8;
    }}

    .piece {{
        position: absolute;
        width: 8px;
        height: 12px;
        opacity: 0;
    }}

    .run .ribbon-left {{
        animation: cutLeft 1.8s ease forwards, fadeRibbon 1.4s ease 1.8s forwards;
    }}

    .run .ribbon-right {{
        animation: cutRight 1.8s ease forwards, fadeRibbon 1.4s ease 1.8s forwards;
    }}

    .run .knot {{
        animation: knotDrop 1.8s ease forwards, fadeRibbon 1.4s ease 1.8s forwards;
    }}

    .run .bow-left {{
        animation: bowLeft 1.8s ease forwards, fadeRibbon 1.4s ease 1.8s forwards;
    }}

    .run .bow-right {{
        animation: bowRight 1.8s ease forwards, fadeRibbon 1.4s ease 1.8s forwards;
    }}

    .run .tail-left {{
        animation: bowLeft 1.8s ease forwards, fadeRibbon 1.4s ease 1.8s forwards;
    }}

    .run .tail-right {{
        animation: bowRight 1.8s ease forwards, fadeRibbon 1.4s ease 1.8s forwards;
    }}

    .run .scissor {{
        animation: scissorFloat 1.0s ease, scissorFade 1.6s linear 0.4s forwards;
    }}

    .run .curtain.left {{
        animation: openLeft 3.4s ease-in-out 3.4s forwards;
    }}

    .run .curtain.right {{
        animation: openRight 3.4s ease-in-out 3.4s forwards;
    }}

    .run .text-layer {{
        animation: showText 0.4s linear 7.3s forwards;
    }}

    @keyframes cutLeft {{
        to {{
            transform: translate(-112px, 38px) rotate(-9deg);
        }}
    }}

    @keyframes cutRight {{
        to {{
            transform: translate(112px, 38px) rotate(9deg);
        }}
    }}

    @keyframes knotDrop {{
        to {{
            transform: translate(-50%, 26px);
        }}
    }}

    @keyframes bowLeft {{
        to {{
            transform: translate(-18px, 26px) rotate(-8deg);
        }}
    }}

    @keyframes bowRight {{
        to {{
            transform: translate(18px, 26px) rotate(8deg);
        }}
    }}

    @keyframes fadeRibbon {{
        to {{
            opacity: 0;
        }}
    }}

    @keyframes scissorFloat {{
        0% {{ transform: translateX(-50%) translateY(0); }}
        50% {{ transform: translateX(-50%) translateY(-8px); }}
        100% {{ transform: translateX(-50%) translateY(0); }}
    }}

    @keyframes scissorFade {{
        to {{ opacity: 0; }}
    }}

    @keyframes openLeft {{
        to {{ transform: translateX(-92%); }}
    }}

    @keyframes openRight {{
        to {{ transform: translateX(92%); }}
    }}

    @keyframes showText {{
        to {{ opacity: 1; }}
    }}
</style>
</head>
<body>
<div class="wrap">
    <div class="stage">
        <div class="inner"></div>
        <div class="header">
            <div class="line1">EAST COAST RAILWAY</div>
            <div class="line2">Digital Inauguration Ceremony</div>
        </div>
        <div class="rod"></div>

        <div class="opening {'run' if run_id > 0 else ''}" id="opening-{run_id}">
            <div class="text-layer" id="textLayer">
                <div class="text-box" id="typedText"></div>
            </div>

            <div class="valance"></div>

            <div class="curtain left">
                <div class="tie left"></div>
            </div>
            <div class="curtain right">
                <div class="tie right"></div>
            </div>

            <div class="ribbon-zone">
                <div class="ribbon-left"></div>
                <div class="ribbon-right"></div>
                <div class="knot"></div>
                <div class="bow-left"></div>
                <div class="bow-right"></div>
                <div class="tail-left"></div>
                <div class="tail-right"></div>
                <div class="scissor">✂</div>
            </div>

            <div class="confetti" id="confetti"></div>
        </div>
    </div>
</div>

{cut_audio}
{curtain_audio}
{reveal_audio}

<script>
const fullText = `{safe_message}`;
const runId = {run_id};

function typeHtmlSlowly(target, htmlText, delayMs=85) {{
    const tokens = htmlText.split(/(<br>)/g);
    let i = 0;
    target.innerHTML = "";
    function step() {{
        if (i < tokens.length) {{
            target.innerHTML += tokens[i];
            i += 1;
            setTimeout(step, delayMs);
        }}
    }}
    step();
}}

function launchConfetti() {{
    const confetti = document.getElementById("confetti");
    const colors = ["#ff0000","#ffd700","#00a2ff","#00aa55","#ff66cc","#ff8800","#7a3cff"];
    confetti.innerHTML = "";
    for (let i = 0; i < 90; i++) {{
        const p = document.createElement("div");
        p.className = "piece";
        p.style.left = (Math.random() * 100) + "%";
        p.style.top = (10 + Math.random() * 20) + "%";
        p.style.background = colors[Math.floor(Math.random() * colors.length)];
        p.style.opacity = "1";
        p.animate(
            [
                {{ transform: "translateY(0px) rotate(0deg)", opacity: 1 }},
                {{ transform: `translateY(${420 + Math.random()*180}px) translateX(${(Math.random()-0.5)*140}px) rotate(${360 + Math.random()*400}deg)`, opacity: 1 }}
            ],
            {{
                duration: 2400 + Math.random() * 1400,
                easing: "ease-in"
            }}
        );
        confetti.appendChild(p);
    }}
}}

if (runId > 0) {{
    setTimeout(() => {{
        const a = document.getElementById("cutAudio");
        if (a) a.play().catch(() => null);
    }}, 150);

    setTimeout(() => {{
        const a = document.getElementById("curtainAudio");
        if (a) a.play().catch(() => null);
    }}, 3400);

    setTimeout(() => {{
        const typed = document.getElementById("typedText");
        typeHtmlSlowly(typed, fullText, 140);
        const a = document.getElementById("revealAudio");
        if (a) a.play().catch(() => null);
    }}, 7400);

    setTimeout(() => {{
        launchConfetti();
    }}, 9000);
}}
</script>
</body>
</html>
"""

components.html(html_code, height=780, scrolling=False)