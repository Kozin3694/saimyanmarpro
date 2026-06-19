import streamlit as st
import streamlit.components.v1 as components
import edge_tts
import asyncio
import os
import base64
import uuid

# --- 1. Streamlit Page Configuration ---
st.set_page_config(layout="wide", page_title="စိုင်းမြန်မာ အသံပြောင်းစနစ် Pro", initial_sidebar_state="collapsed")

# --- Streamlit ရဲ့ မူလ Header, Footer များကို ဖျောက်ရန် ---
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    iframe { border: none !important; }
    .block-container {
        padding: 0rem !important;
        max-width: 100% !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. HTML / CSS / JS UI Code ---
HTML_CODE = r"""
<!DOCTYPE html>
<html lang="my" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>စိုင်းမြန်မာ အသံပြောင်းစနစ် Pro</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: { 
                extend: { 
                    colors: { 
                        primary: '#ec4899', 
                        darkBg: '#0f172a',
                        darkPanel: '#1e293b'
                    },
                    animation: {
                        'spin-slow': 'spin 3s linear infinite',
                    }
                } 
            }
        }
    </script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Padauk:wght@400;700&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&display=swap');

        body {
            font-family: 'Padauk', sans-serif;
            transition: background-color 0.3s ease;
            -webkit-tap-highlight-color: transparent;
        }

        body {
            background-color: #f8fafc;
            background-image: url("data:image/svg+xml,%3Csvg width='150' height='150' viewBox='0 0 150 150' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' stroke='%23cbd5e1' stroke-width='1.5' stroke-linecap='round' stroke-linejoin='round' opacity='0.7'%3E%3Cpath d='M30 35c-3 0-5 2-5 5s2 5 5 5 5-2 5-5-2-5-5-5zm-10-8c-2 0-4 2-4 4s2 4 4 4 4-2 4-4-2-4-4-4zm18 0c-2 0-4 2-4 4s2 4 4 4 4-2 4-4-2-4-4-4zm-8 18c-5 0-9-3-10-7 0-2 2-4 5-4h10c3 0 5 2 5 4-1 4-5 7-10 7z'/%3E%3Cpath d='M110 40c-2-2-6-2-8 0l-15 15c-3 3-3 7 0 10s7 3 10 0l15-15c3-3 3-7 0-10z'/%3E%3Ccircle cx='105' cy='35' r='3'/%3E%3Ccircle cx='115' cy='45' r='3'/%3E%3Ccircle cx='85' cy='55' r='3'/%3E%3Ccircle cx='95' cy='65' r='3'/%3E%3Cpath d='M40 100c12-6 25-6 38 0-13 6-26 6-38 0zM78 100l12-12v24zM53 98v4M65 98v4'/%3E%3Cpath d='M110 105l4-10 4 10 10 3-8 7 3 10-10-5-10 5 3-10-8-7 10-3z'/%3E%3Cpath d='M80 15a10 10 0 0 1 10 10m-20 0a10 10 0 0 1 10-10'/%3E%3C/g%3E%3C/svg%3E");
            background-attachment: fixed;
        }
        .dark body {
            background-color: #0f172a;
            background-image: url("data:image/svg+xml,%3Csvg width='150' height='150' viewBox='0 0 150 150' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' stroke='%23334155' stroke-width='1.5' stroke-linecap='round' stroke-linejoin='round' opacity='0.4'%3E%3Cpath d='M30 35c-3 0-5 2-5 5s2 5 5 5 5-2 5-5-2-5-5-5zm-10-8c-2 0-4 2-4 4s2 4 4 4 4-2 4-4-2-4-4-4zm18 0c-2 0-4 2-4 4s2 4 4 4 4-2 4-4-2-4-4-4zm-8 18c-5 0-9-3-10-7 0-2 2-4 5-4h10c3 0 5 2 5 4-1 4-5 7-10 7z'/%3E%3Cpath d='M110 40c-2-2-6-2-8 0l-15 15c-3 3-3 7 0 10s7 3 10 0l15-15c3-3 3-7 0-10z'/%3E%3Ccircle cx='105' cy='35' r='3'/%3E%3Ccircle cx='115' cy='45' r='3'/%3E%3Ccircle cx='85' cy='55' r='3'/%3E%3Ccircle cx='95' cy='65' r='3'/%3E%3Cpath d='M40 100c12-6 25-6 38 0-13 6-26 6-38 0zM78 100l12-12v24zM53 98v4M65 98v4'/%3E%3Cpath d='M110 105l4-10 4 10 10 3-8 7 3 10-10-5-10 5 3-10-8-7 10-3z'/%3E%3Cpath d='M80 15a10 10 0 0 1 10 10m-20 0a10 10 0 0 1 10-10'/%3E%3C/g%3E%3C/svg%3E");
        }

        .custom-scrollbar::-webkit-scrollbar { width: 6px; }
        .custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
        .custom-scrollbar::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 6px; }
        .dark .custom-scrollbar::-webkit-scrollbar-thumb { background: #475569; }

        .bouncy-btn { position: relative; transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275); }
        .bouncy-btn:hover { transform: translateY(-4px) scale(1.03); box-shadow: 0 12px 25px -5px rgba(236, 72, 153, 0.6); border-color: #ec4899; z-index: 10; }
        .bouncy-btn:active { transform: scale(0.92); }
        .active-btn { transform: scale(1.02); }

        .style-btn.active-btn {
            border-color: #ec4899 !important; color: #ec4899 !important; box-shadow: 0 4px 15px rgba(236, 72, 153, 0.5), inset 0 0 10px rgba(236, 72, 153, 0.2) !important; transform: scale(1.05); background-color: transparent !important;
        }
        .dark .style-btn.active-btn {
            border-color: #f472b6 !important; color: #f472b6 !important; box-shadow: 0 4px 15px rgba(236, 72, 153, 0.6), inset 0 0 10px rgba(236, 72, 153, 0.2) !important;
        }

        .voice-btn { text-align: left; position: relative; overflow: hidden; }
        .active-btn.voice-btn { border-color: #a855f7 !important; }
        .play-icon-wrapper { position: relative; z-index: 2; }
        .voice-btn:hover .play-icon-wrapper::before,
        .active-btn.voice-btn .play-icon-wrapper::before {
            content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0; border-radius: 50%; border: 2px solid #a855f7; z-index: -1; animation: ripple-wave 1.2s infinite ease-out;
        }
        @keyframes ripple-wave { 0% { transform: scale(1); opacity: 1; } 100% { transform: scale(1.8); opacity: 0; } }

        .slider-container { position: relative; width: 100%; height: 12px; border-radius: 10px; background: #e2e8f0; overflow: hidden; box-shadow: inset 0 1px 2px rgba(0,0,0,0.1); }
        .dark .slider-container { background: #1e293b; box-shadow: inset 0 1px 2px rgba(0,0,0,0.3); }

        .slider-fill { position: absolute; top: 0; left: 0; height: 100%; background: linear-gradient(to right, #3b82f6, #8b5cf6, #ec4899); border-radius: 10px; pointer-events: none; }

        .slider-input { position: absolute; top: 0; left: 0; width: 100%; height: 100%; -webkit-appearance: none; appearance: none; background: transparent; outline: none; margin: 0; z-index: 2; cursor: pointer; }
        .slider-input::-webkit-slider-thumb { -webkit-appearance: none; appearance: none; width: 24px; height: 24px; border-radius: 50%; background: #ffffff; border: 3px solid #ec4899; box-shadow: 0 2px 6px rgba(0,0,0,0.2); cursor: grab; transition: transform 0.1s ease; margin-top: -6px; position: relative; z-index: 3; }
        .slider-input::-webkit-slider-thumb:active { transform: scale(1.1); cursor: grabbing; }

        .solid-control-btn { position: relative; overflow: hidden; transition: all 0.2s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1); border: 2px solid #cbd5e1; background-color: #fff; color: #475569; }
        .dark .solid-control-btn { border-color: #475569; background-color: #1e293b; color: #cbd5e1; box-shadow: 0 2px 4px rgba(0,0,0,0.3); }
        .solid-control-btn:hover { border-color: #ec4899; color: #ec4899; background-color: #fdf2f8; }
        .dark .solid-control-btn:hover { background-color: #334155; }
        .solid-control-btn:active { transform: scale(0.95); background-color: #fce7f3; }
        .dark .solid-control-btn:active { background-color: #475569; }

        .logo-container { position: relative; width: 140px; height: 140px; display: flex; align-items: center; justify-content: center; }
        @keyframes ring-spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        .logo-ring { position: absolute; width: 100%; height: 100%; border-radius: 50%; border: 4px dashed transparent; border-top-color: #ec4899; border-right-color: #a855f7; border-bottom-color: #3b82f6; border-left-color: #14b8a6; animation: ring-spin 6s linear infinite; }
        .logo-inner { position: relative; z-index: 10; text-align: center; padding: 15px; border-radius: 50%; width: 120px; height: 120px; display: flex; flex-direction: column; justify-content: center; align-items: center; box-shadow: 0 4px 10px rgba(0,0,0,0.1); background: #1e293b; }
        .dark .logo-inner { box-shadow: 0 4px 10px rgba(0,0,0,0.3); }

        .visualizer-container { display: flex; align-items: center; justify-content: center; height: 60px; gap: 3px; margin-bottom: 15px; overflow: hidden; background: rgba(0,0,0,0.2); border-radius: 10px; padding: 5px; }
        .wave-bar-new { width: 4px; background: #cbd5e1; border-radius: 2px; height: 4px; transition: all 0.1s ease; flex-grow: 1; max-width: 8px; }
        .dark .wave-bar-new { background: #475569; }
        .visualizer-active .wave-bar-new { background: linear-gradient(to top, #3b82f6, #2dd4bf); animation: wave-animation 0.5s infinite ease-in-out alternate; }
        @keyframes wave-animation { 0% { height: 10%; opacity: 0.7; } 100% { height: 90%; opacity: 1; } }
        .wave-bar-new:nth-child(1) { animation-delay: 0.0s; animation-duration: 0.4s; }
        .wave-bar-new:nth-child(2) { animation-delay: 0.1s; animation-duration: 0.5s; }
        .wave-bar-new:nth-child(3) { animation-delay: 0.2s; animation-duration: 0.6s; }
        .wave-bar-new:nth-child(4) { animation-delay: 0.3s; animation-duration: 0.45s; }
        .wave-bar-new:nth-child(5) { animation-delay: 0.4s; animation-duration: 0.55s; }
        .wave-bar-new:nth-child(6) { animation-delay: 0.5s; animation-duration: 0.65s; }
        .wave-bar-new:nth-child(7) { animation-delay: 0.4s; animation-duration: 0.5s; }
        .wave-bar-new:nth-child(8) { animation-delay: 0.3s; animation-duration: 0.4s; }
        .wave-bar-new:nth-child(9) { animation-delay: 0.2s; animation-duration: 0.6s; }
        .wave-bar-new:nth-child(10) { animation-delay: 0.1s; animation-duration: 0.45s; }
        .wave-bar-new:nth-child(11) { animation-delay: 0.0s; animation-duration: 0.55s; }
        .wave-bar-new:nth-child(12) { animation-delay: 0.1s; animation-duration: 0.65s; }
        .wave-bar-new:nth-child(13) { animation-delay: 0.2s; animation-duration: 0.5s; }
        .wave-bar-new:nth-child(14) { animation-delay: 0.3s; animation-duration: 0.4s; }
        .wave-bar-new:nth-child(15) { animation-delay: 0.4s; animation-duration: 0.6s; }
        .wave-bar-new:nth-child(16) { animation-delay: 0.5s; animation-duration: 0.45s; }
        .wave-bar-new:nth-child(17) { animation-delay: 0.4s; animation-duration: 0.55s; }
        .wave-bar-new:nth-child(18) { animation-delay: 0.3s; animation-duration: 0.65s; }
        .wave-bar-new:nth-child(19) { animation-delay: 0.2s; animation-duration: 0.5s; }
        .wave-bar-new:nth-child(20) { animation-delay: 0.1s; animation-duration: 0.4s; }

        .no-bounce-input { transition: border-color 0.2s, box-shadow 0.2s; }
        .no-bounce-input:focus-within { border-color: #ec4899; box-shadow: 0 0 0 3px rgba(236, 72, 153, 0.2); }
    </style>
</head>
<body class="text-slate-800 dark:text-white min-h-screen p-3 sm:p-4 flex flex-col items-center">

    <div class="w-full max-w-2xl flex justify-end mb-2 relative z-10">
        <button onclick="toggleTheme()" id="themeBtn" class="bouncy-btn bg-white/90 dark:bg-slate-800/90 backdrop-blur-sm text-slate-700 dark:text-slate-200 px-5 py-2.5 rounded-full text-sm font-bold shadow-md border border-slate-300 dark:border-slate-700 flex items-center gap-2">
            ☀️ အလင်းမုဒ်
        </button>
    </div>

    <div class="text-center mb-8 sm:mb-10 w-full max-w-2xl relative z-10 flex flex-col items-center">
        
        <div class="logo-container mb-6">
            <div class="logo-ring"></div>
            <div class="logo-inner">
                <div class="font-['Orbitron'] text-[16px] font-bold text-[#3b82f6] tracking-wide leading-none">SaiMyanmar</div>
                <div class="font-['Orbitron'] text-[22px] font-bold text-[#f43f5e] tracking-wider my-1.5 leading-none">TTS</div>
                <div class="font-['Padauk'] text-[13px] text-slate-300">မြန်မာ</div>
            </div>
        </div>

        <h1 class="text-3xl sm:text-4xl font-extrabold mb-6 drop-shadow-md flex items-center justify-center flex-wrap gap-x-2 gap-y-1" style="line-height: 1.4;">
            <span class="text-[#06b6d4]">စိုင်းမြန်မာ</span>
            <span class="text-[#94a3b8]">အသံပြောင်းစနစ်</span>
            <span class="text-[#a855f7]">Pro</span>
        </h1>
        
        <div class="bouncy-btn inline-block border-[3px] border-pink-500 bg-white/90 dark:bg-slate-900/90 backdrop-blur-md rounded-2xl px-6 py-3 shadow-[0_0_20px_rgba(236,72,153,0.4)] mb-8">
            <p class="text-sm sm:text-base font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-pink-600 via-purple-500 to-blue-500 dark:from-pink-400 dark:via-purple-400 dark:to-blue-400 tracking-wide uppercase">
                စိုင်းမြန်မာ Telegram Channel မှ ကြိုဆိုပါတယ်
            </p>
        </div>
        
        <div class="bg-white/95 dark:bg-[#1e293b]/95 backdrop-blur-md border-l-[6px] border-pink-500 p-5 sm:p-6 rounded-2xl shadow-xl border border-slate-200 dark:border-slate-700/50 text-left relative transition-all">
            <h3 class="text-pink-600 dark:text-pink-500 font-extrabold text-lg mb-3 flex items-center justify-center gap-2">
                <span>⚠️</span> အရေးကြီး အသိပေးချက် <span>⚠️</span>
            </h3>
            <p class="text-slate-700 dark:text-slate-300 text-[14.5px] font-medium leading-relaxed mb-5 text-center">
                ကျွန်တော်တို့ <span class="text-pink-600 dark:text-pink-400 font-bold">SAIMYANMAR TTS PRO</span> ကို အသုံးပြုသူ အရမ်းများလာတဲ့အတွက် Server အသစ်သို့ ပြောင်းလဲတပ်ဆင်ထားပါတယ်။ ဒါကြောင့် အရင် Server အဟောင်းမှာ အသံထုတ်မရတာမျိုး ဖြစ်သွားတာပါ။ <br><br>
                ရှေ့ဆက်ပြီး System အသစ်တွေချထားရင် အလွယ်တကူ သိရှိနိုင်ဖို့ <span class="text-blue-600 dark:text-blue-400 font-bold">Users အဟောင်းရော အသစ်ပါ အားလုံး</span> အောက်က Telegram Channel ကို Join ထားပေးကြပါ။
            </p>
            <a href="https://t.me/saimyanmar123" target="_blank" rel="noopener noreferrer" class="bouncy-btn block w-full bg-gradient-to-r from-pink-600 to-purple-600 hover:from-pink-500 hover:to-purple-500 text-white text-base font-bold py-3.5 px-6 rounded-xl shadow-lg transition-all text-center border-2 border-pink-400/50">
                👉 Telegram Group သို့ ယခုပဲ ဝင်ထားပါ 👈
            </a>
        </div>
    </div>

    <div class="w-full max-w-2xl bg-white/95 dark:bg-[#1e293b]/95 backdrop-blur-lg rounded-[2rem] shadow-2xl p-4 sm:p-7 border border-slate-200 dark:border-slate-700 relative z-10 mb-10">
        
        <h2 class="text-pink-600 dark:text-pink-400 text-sm font-extrabold tracking-widest mb-4 border-b-2 border-slate-200 dark:border-slate-700 pb-2">အသံရွေးချယ်ပါ</h2>
        <div id="voices-grid" class="grid grid-cols-2 gap-2 sm:gap-3 mb-6 max-h-[300px] overflow-y-auto custom-scrollbar p-2">
        </div>

        <h2 class="text-purple-600 dark:text-purple-400 text-sm font-extrabold tracking-widest mb-4 border-b-2 border-slate-200 dark:border-slate-700 pb-2 mt-6">အသံစတိုင်နှင့် ပေါင်းစပ်မှုများ</h2>
        <div id="recap-grid" class="grid grid-cols-2 sm:grid-cols-3 gap-2 sm:gap-3 mb-6 max-h-40 overflow-y-auto custom-scrollbar p-2">
        </div>

        <h2 class="text-blue-600 dark:text-blue-400 text-sm font-extrabold tracking-widest mb-3 border-b-2 border-slate-200 dark:border-slate-700 pb-2 mt-6">စကားပြော စိတ်ခံစားမှု စတိုင်များ</h2>
        <div id="emotions-grid" class="grid grid-cols-3 sm:grid-cols-4 gap-2 mb-8 p-2">
        </div>

        <div class="mb-5 bg-slate-50 dark:bg-slate-800/50 p-5 rounded-2xl border border-slate-200 dark:border-slate-700 shadow-sm">
            <div class="flex justify-between items-center mb-5">
                <span class="text-sm font-extrabold text-slate-700 dark:text-slate-300 tracking-widest uppercase">အမြန်နှုန်း (Speed)</span>
                <span id="speed-val" class="font-mono text-base font-bold text-white bg-pink-500 px-4 py-1 rounded-lg shadow-sm">+၀</span>
            </div>
            <div class="flex items-center justify-between gap-4">
                <button onclick="changeVal('speed', -5)" class="solid-control-btn w-12 h-12 rounded-xl font-bold text-2xl flex items-center justify-center pb-1">-</button>
                <div class="slider-container flex-1 relative h-8">
                    <div class="slider-fill" id="speed-fill" style="width: 50%;"></div>
                    <input type="range" id="speed" min="-100" max="100" value="0" class="slider-input" oninput="updateSlider('speed', this.value)">
                </div>
                <button onclick="changeVal('speed', 5)" class="solid-control-btn w-12 h-12 rounded-xl font-bold text-2xl flex items-center justify-center pb-1">+</button>
            </div>
        </div>

        <div class="mb-8 bg-slate-50 dark:bg-slate-800/50 p-5 rounded-2xl border border-slate-200 dark:border-slate-700 shadow-sm">
            <div class="flex justify-between items-center mb-5">
                <span class="text-sm font-extrabold text-slate-700 dark:text-slate-300 tracking-widest uppercase">အသံ အတက်/အကျ (Pitch)</span>
                <span id="pitch-val" class="font-mono text-base font-bold text-white bg-purple-500 px-4 py-1 rounded-lg shadow-sm">+၀</span>
            </div>
            <div class="flex items-center justify-between gap-4">
                <button onclick="changeVal('pitch', -5)" class="solid-control-btn w-12 h-12 rounded-xl font-bold text-2xl flex items-center justify-center pb-1">-</button>
                <div class="slider-container flex-1 relative h-8">
                    <div class="slider-fill" id="pitch-fill" style="width: 50%;"></div>
                    <input type="range" id="pitch" min="-100" max="100" value="0" class="slider-input" oninput="updateSlider('pitch', this.value)">
                </div>
                <button onclick="changeVal('pitch', 5)" class="solid-control-btn w-12 h-12 rounded-xl font-bold text-2xl flex items-center justify-center pb-1">+</button>
            </div>
        </div>

        <div class="flex justify-between items-center mb-4 mt-4">
            <h2 class="text-slate-800 dark:text-slate-200 text-sm font-extrabold tracking-widest">စာသားထည့်သွင်းပါ</h2>
            <div class="flex gap-2">
                <button onclick="pasteText()" class="bouncy-btn text-xs bg-blue-600 text-white px-4 py-2 rounded-xl shadow-md font-bold">ကူးထည့်မည်</button>
                <button onclick="clearText()" class="bouncy-btn text-xs bg-red-600 text-white px-4 py-2 rounded-xl shadow-md font-bold">ဖျက်မည်</button>
            </div>
        </div>
        
        <textarea id="text-input" rows="5" maxlength="10000" oninput="updateCharCount()" class="w-full bg-slate-50 dark:bg-slate-900 text-slate-900 dark:text-white border-2 border-slate-300 dark:border-slate-600 rounded-2xl p-4 focus:outline-none focus:border-pink-500 dark:focus:border-pink-500 focus:ring-2 focus:ring-pink-500/30 text-base leading-relaxed custom-scrollbar shadow-inner transition-all hover:shadow-[0_0_15px_rgba(236,72,153,0.2)]" placeholder="ဤနေရာတွင် မြန်မာစာများ ရိုက်ထည့်ပါ သို့မဟုတ် ကူးထည့်ပါ..."></textarea>
        
        <div class="text-right text-xs font-bold text-slate-500 mt-2 mb-6">
            <span id="char-count">၀</span> / ၁၀၀၀၀
        </div>

        <button id="generate-btn" onclick="generateAudio()" class="bouncy-btn w-full bg-gradient-to-r from-pink-600 to-purple-600 text-white font-extrabold py-4 px-4 rounded-2xl shadow-[0_8px_20px_rgba(236,72,153,0.5)] flex justify-center items-center text-xl tracking-widest border-2 border-pink-400/30">
            အသံထုတ်ယူမည်
        </button>

        <div id="audio-container" class="mt-8 hidden">
            <div class="bg-slate-50 dark:bg-slate-900/80 border-2 border-slate-200 dark:border-slate-700 rounded-3xl p-5 sm:p-6 relative overflow-hidden shadow-inner">
                
                <p class="text-center text-xs font-extrabold text-slate-500 dark:text-slate-400 mb-2 tracking-widest uppercase">အသံဖွင့်စက်</p>
                
                <div id="visualizer" class="visualizer-container">
                    <div class="wave-bar-new"></div><div class="wave-bar-new"></div>
                    <div class="wave-bar-new"></div><div class="wave-bar-new"></div>
                    <div class="wave-bar-new"></div><div class="wave-bar-new"></div>
                    <div class="wave-bar-new"></div><div class="wave-bar-new"></div>
                    <div class="wave-bar-new"></div><div class="wave-bar-new"></div>
                    <div class="wave-bar-new"></div><div class="wave-bar-new"></div>
                    <div class="wave-bar-new"></div><div class="wave-bar-new"></div>
                    <div class="wave-bar-new"></div><div class="wave-bar-new"></div>
                    <div class="wave-bar-new"></div><div class="wave-bar-new"></div>
                    <div class="wave-bar-new"></div><div class="wave-bar-new"></div>
                </div>
                
                <audio id="audio-player" controls class="w-full mb-6 rounded-xl border border-slate-300 dark:border-slate-700 shadow-sm relative z-20"></audio>
                
                <div class="mb-6 relative z-20">
                    <label class="block text-xs text-slate-600 dark:text-slate-400 mb-2 font-extrabold">သိမ်းဆည်းမည့် ဖိုင်အမည် (စိတ်ကြိုက်ပြင်နိုင်သည်)</label>
                    <div class="no-bounce-input flex bg-white dark:bg-slate-800 border-2 border-slate-300 dark:border-slate-600 rounded-xl overflow-hidden shadow-sm">
                        <input type="text" id="custom-filename" value="My_Voice_Record" class="w-full bg-transparent text-slate-800 dark:text-white px-4 py-3 text-sm font-bold focus:outline-none" placeholder="ဖိုင်အမည်ရေးပါ">
                        <span class="bg-slate-100 dark:bg-slate-700 text-slate-500 dark:text-slate-300 px-4 py-3 text-sm font-bold border-l-2 border-slate-300 dark:border-slate-600 flex items-center">.mp3</span>
                    </div>
                </div>

                <a id="download-link" href="#" onclick="setDownloadName()" class="bouncy-btn w-full bg-green-500 hover:bg-green-400 text-white font-extrabold py-4 px-4 rounded-xl flex justify-center items-center text-base tracking-wider shadow-[0_5px_15px_rgba(34,197,94,0.4)] border border-green-400 relative z-20">
                    ⬇️ အသံဖိုင်ဒေါင်းမည်
                </a>
            </div>
        </div>
    </div>

    <script>
        // --- 3. STREAMLIT & JS COMMUNICATION ---
        function sendMessageToStreamlitClient(type, data) {
            var outData = Object.assign({ isStreamlitMessage: true, type: type }, data);
            window.parent.postMessage(outData, "*");
        }

        const Streamlit = {
            setComponentReady: function() { sendMessageToStreamlitClient("streamlit:componentReady", {apiVersion: 1}); },
            setFrameHeight: function() { sendMessageToStreamlitClient("streamlit:setFrameHeight", {height: document.documentElement.scrollHeight}); },
            setComponentValue: function(value) { sendMessageToStreamlitClient("streamlit:setComponentValue", {value: value}); }
        };

        window.addEventListener("message", function(event) {
            if (event.data.type === "streamlit:render") {
                Streamlit.setFrameHeight();
                const args = event.data.args;
                
                if (args.audio_b64 && args.audio_b64 !== window.last_audio_b64) {
                    window.last_audio_b64 = args.audio_b64;
                    playAudioBase64(args.audio_b64);
                }
                
                if (args.error && args.error !== window.last_error) {
                    window.last_error = args.error;
                    alert("အမှားအယွင်းဖြစ်ပေါ်နေပါသည်: " + args.error);
                    resetButton();
                }
            }
        });

        // --- 4. ORIGINAL JS LOGIC ---
        const voices = [
            { id: 'v1', name: 'ကိုစိုင်းစိုင်း', gender: 'ယောက်ျားလေး' },
            { id: 'v2', name: 'မဖွေးဖွေး', gender: 'မိန်းကလေး' },
            { id: 'v3', name: 'ကိုနေတိုး', gender: 'ယောက်ျားလေး' },
            { id: 'v4', name: 'ကိုအောင်ရဲလင်း', gender: 'ယောက်ျားလေး' },
            { id: 'v5', name: 'ကိုမြင့်မြတ်', gender: 'ယောက်ျားလေး' },
            { id: 'v6', name: 'မဝတ်မှုံရွှေရည်', gender: 'မိန်းကလေး' },
            { id: 'v7', name: 'ကိုဒေါင်း', gender: 'ယောက်ျားလေး' },
            { id: 'v8', name: 'မသက်မွန်မြင့်', gender: 'မိန်းကလေး' },
            { id: 'v9', name: 'ကိုလူမင်း', gender: 'ယောက်ျားလေး' },
            { id: 'v10', name: 'မအိန္ဒြာကျော်ဇင်', gender: 'မိန်းကလေး' },
            { id: 'v11', name: 'မရွှေမှုံရတီ', gender: 'မိန်းကလေး' },
            { id: 'v12', name: 'ကိုပြေတီဦး', gender: 'ယောက်ျားလေး' },
            { id: 'v13', name: 'မသင်ဇာဝင့်ကျော်', gender: 'မိန်းကလေး' },
            { id: 'v14', name: 'ကိုပိုင်တံခွန်', gender: 'ယောက်ျားလေး' }
        ];

        const recapStyles = [
            { id: 'Normal', name: 'ပုံမှန်အသံ', speed: 0, pitch: 0 },
            { id: 'NyoGyi_25', name: 'ကျားကြီး ၁', speed: 0, pitch: 25 },
            { id: 'NyoGyi_35', name: 'ကျားကြီး ၂', speed: 0, pitch: 35 },
            { id: 'NyoGyi_45', name: 'ကျားကြီး ၃', speed: 0, pitch: 45 },
            { id: 'Nilar_40', name: 'နီလာ ချွဲသံ', speed: 0, pitch: 40 },
            { id: 'Combo_15', name: 'ပေါင်းစပ် ၁၅', speed: 15, pitch: 15 },
            { id: 'Combo_30', name: 'ပေါင်းစပ် ၃၀', speed: 30, pitch: 30 },
            { id: 'Combo_50', name: 'ပေါင်းစပ် ၅၀', speed: 50, pitch: 50 },
            { id: 'Pitch_20', name: 'အသံသေး ၂၀', speed: 0, pitch: 20 },
            { id: 'Pitch_50', name: 'အသံသေး ၅၀', speed: 0, pitch: 50 }
        ];

        const emotions = [
            { id: 'EXCITING', name: 'စိတ်လှုပ်ရှား 🤩', s: 15, p: 10 },
            { id: 'CALM', name: 'တည်ငြိမ် 😌', s: -10, p: -5 },
            { id: 'PROFESSIONAL', name: 'သတင်း 💼', s: 0, p: -2 },
            { id: 'NARRATIVE', name: 'ဇာတ်ကြောင်း 📖', s: -5, p: 0 },
            { id: 'HAPPY', name: 'ပျော်ရွှင် 😊', s: 10, p: 15 },
            { id: 'SERIOUS', name: 'လေးနက် 😠', s: -5, p: -10 },
            { id: 'WHISPER', name: 'တီးတိုး 🤫', s: -15, p: -20 },
            { id: 'SAD', name: 'ဝမ်းနည်း 😢', s: -15, p: -15 },
            { id: 'SARCASTIC', name: 'ရွဲ့ပြော 🙄', s: -10, p: 5 },
            { id: 'ANGRY', name: 'ဒေါသထွက် 🤬', s: 20, p: -10 },
            { id: 'FEAR', name: 'ကြောက်လန့် 😨', s: 10, p: 20 }
        ];

        let selectedVoiceId = voices[0].id;

        function init() {
            updateThemeBtnText();

            const vGrid = document.getElementById('voices-grid');
            voices.forEach(v => {
                let btn = document.createElement('button');
                btn.className = `bouncy-btn voice-btn w-full border-2 border-slate-200 dark:border-slate-700 bg-white dark:bg-[#1e293b] rounded-xl p-3 flex flex-row items-center gap-3.5 hover:bg-slate-50 dark:hover:bg-slate-800 transition-all ${v.id === selectedVoiceId ? 'active-btn' : ''}`;
                btn.onclick = () => selectVoice(v.id, btn);
                btn.innerHTML = `
                    <div class="play-icon-wrapper flex-shrink-0 w-10 h-10 rounded-full bg-[#8b5cf6] flex items-center justify-center relative">
                        <svg class="w-4 h-4 text-white ml-1 pointer-events-none" fill="currentColor" viewBox="0 0 20 20"><path d="M4.018 14L14.22 9 4.018 4v10z"></path></svg>
                    </div>
                    <div class="flex flex-col text-left pointer-events-none">
                        <span class="text-[14px] font-bold text-slate-800 dark:text-slate-200 mb-0.5">${v.name}</span>
                        <span class="text-[12px] text-slate-500 dark:text-slate-400 font-medium">${v.gender}</span>
                    </div>
                `;
                vGrid.appendChild(btn);
            });

            const rGrid = document.getElementById('recap-grid');
            recapStyles.forEach(r => {
                let btn = document.createElement('button');
                btn.className = 'bouncy-btn style-btn border-2 border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-300 text-[11px] font-extrabold py-2 px-1 rounded-lg shadow-sm';
                btn.onclick = () => applyPreset(btn, r.speed, r.pitch);
                btn.innerText = r.name;
                rGrid.appendChild(btn);
            });

            const eGrid = document.getElementById('emotions-grid');
            emotions.forEach(e => {
                let btn = document.createElement('button');
                btn.className = 'bouncy-btn style-btn border-2 border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-300 text-[10px] font-extrabold py-2 px-1 rounded-lg shadow-sm';
                btn.onclick = () => applyPreset(btn, e.s, e.p);
                btn.innerText = e.name;
                eGrid.appendChild(btn);
            });

            updateSlider('speed', 0);
            updateSlider('pitch', 0);
        }

        function toggleTheme() {
            document.documentElement.classList.toggle('dark');
            updateThemeBtnText();
        }

        function updateThemeBtnText() {
            const isDark = document.documentElement.classList.contains('dark');
            document.getElementById('themeBtn').innerText = isDark ? "☀️ အလင်းမုဒ်" : "🌙 အမှောင်မုဒ်";
        }

        function selectVoice(id, btnElement) {
            selectedVoiceId = id;
            document.querySelectorAll('.voice-btn').forEach(b => b.classList.remove('active-btn'));
            btnElement.classList.add('active-btn');
        }

        function applyPreset(btnElement, speed, pitch) {
            document.querySelectorAll('.style-btn').forEach(b => b.classList.remove('active-btn'));
            btnElement.classList.add('active-btn');
            
            document.getElementById('speed').value = speed;
            document.getElementById('pitch').value = pitch;
            updateSlider('speed', speed);
            updateSlider('pitch', pitch);
        }

        function changeVal(id, amount) {
            let el = document.getElementById(id);
            let newVal = parseInt(el.value) + amount;
            if(newVal > 100) newVal = 100;
            if(newVal < -100) newVal = -100;
            el.value = newVal;
            updateSlider(id, newVal);
            document.querySelectorAll('.style-btn').forEach(b => b.classList.remove('active-btn'));
        }

        function updateSlider(id, val) {
            const min = -100;
            const max = 100;
            const percentage = ((val - min) / (max - min)) * 100;
            document.getElementById(id + '-fill').style.width = percentage + '%';
            
            let displayVal = val > 0 ? "+" + val : val;
            document.getElementById(id + '-val').innerText = toMyanmarNum(displayVal);
        }

        function toMyanmarNum(numStr) {
            const mmNums = ['၀','၁','၂','၃','၄','၅','၆','၇','၈','၉'];
            return numStr.toString().replace(/[0-9]/g, function(w) { return mmNums[w]; });
        }

        function updateCharCount() {
            let len = document.getElementById('text-input').value.length;
            document.getElementById('char-count').innerText = toMyanmarNum(len);
        }

        async function pasteText() {
            try {
                const text = await navigator.clipboard.readText();
                const inputArea = document.getElementById('text-input');
                inputArea.value = (inputArea.value + text).substring(0, 10000); 
                updateCharCount();
            } catch (err) { alert("စာသား ကူးထည့်၍ မရပါ။ စာရိုက်မည့်အကွက်ကို ဖိ၍ Paste လုပ်ပါ။"); }
        }

        function clearText() {
            document.getElementById('text-input').value = '';
            updateCharCount();
        }

        function setDownloadName() {
            let customName = document.getElementById('custom-filename').value.trim();
            if(!customName) customName = "SaiMyanmar_TTS";
            document.getElementById('download-link').download = customName + ".mp3";
        }

        const audioPlayer = document.getElementById('audio-player');
        const visualizerContainer = document.getElementById('visualizer');

        audioPlayer.addEventListener('play', () => { visualizerContainer.classList.add('visualizer-active'); });
        audioPlayer.addEventListener('pause', () => { visualizerContainer.classList.remove('visualizer-active'); });
        audioPlayer.addEventListener('ended', () => { visualizerContainer.classList.remove('visualizer-active'); });

        function playAudioBase64(b64) {
            audioPlayer.src = "data:audio/mp3;base64," + b64;
            const container = document.getElementById('audio-container');
            container.classList.remove('hidden');
            document.getElementById('download-link').href = audioPlayer.src;
            setDownloadName();
            resetButton();
            
            // --- Auto Scroll to Audio Player ပေါင်းထည့်ထားပါသည် ---
            setTimeout(() => {
                Streamlit.setFrameHeight(); // iframe အရှည်ကို အရင်ညှိမည်
                setTimeout(() => {
                    container.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }, 100);
            }, 100);
        }

        function resetButton() {
            const btn = document.getElementById('generate-btn');
            btn.innerHTML = "အသံထုတ်ယူမည်";
            btn.classList.remove('opacity-75', 'cursor-wait');
            Streamlit.setFrameHeight();
        }

        function generateAudio() {
            let originalText = document.getElementById('text-input').value;
            const speed = document.getElementById('speed').value;
            const pitch = document.getElementById('pitch').value;
            const btn = document.getElementById('generate-btn');

            if(!originalText.trim()) { alert("ကျေးဇူးပြု၍ စာသားထည့်သွင်းပါ။"); return; }

            btn.innerHTML = "ခဏစောင့်ပါ... (Generating...)";
            btn.classList.add('opacity-75', 'cursor-wait');
            
            let processedText = originalText;

            const engToMmMap = { 'A':'အေ ', 'B':'ဘီ ', 'C':'စီ ', 'D':'ဒီ ', 'E':'အီး ', 'F':'အက်ဖ် ', 'G':'ဂျီ ', 'H':'အိတ်ချ် ', 'I':'အိုင် ', 'J':'ဂျေ ', 'K':'ကေ ', 'L':'အယ်လ် ', 'M':'အမ် ', 'N':'အန် ', 'O':'အို ', 'P':'ပီ ', 'Q':'ကျူ ', 'R':'အာ ', 'S':'အက်စ် ', 'T':'တီ ', 'U':'ယူ ', 'V':'ဗွီ ', 'W':'ဒဗလျူ ', 'X':'အက်စ် ', 'Y':'ဝိုင် ', 'Z':'ဇက် ' };
            processedText = processedText.replace(/\b[A-Z]{2,}\b/g, function(match) {
                let spelledOut = '';
                for(let i=0; i<match.length; i++) { spelledOut += engToMmMap[match[i]] || match[i]; }
                return spelledOut;
            });

            const wordMap = { 'subscribe': 'ဆပ်စခရိုက်ဘ်', 'like': 'လိုက်ခ်', 'follow': 'ဖောလိုး', 'share': 'ရှယ်ယာ', 'comment': 'ကောမန့်', 'page': 'ပေ့ချ်', 'channel': 'ချန်နယ်', 'admin': 'အက်ဒမင်', 'car': 'ကား', 'part': 'အပိုင်း', 'ep': 'အပိုင်း', 'episode': 'အပိုင်း', 'website': 'ဝက်ဘ်ဆိုက်', 'welcome': 'ဝဲလ်ကမ်း', 'hello': 'ဟဲလို', 'hi': 'ဟိုင်း', 'facebook': 'ဖေ့စ်ဘွတ်ခ်', 'youtube': 'ယူကျု', 'tiktok': 'တစ်တော့', 'google': 'ဂူဂယ်လ်', 'movie': 'ရုပ်ရှင်', 'recap': 'ရီကပ်', 'spoiler': 'စပွိုင်လာ', 'story': 'စတိုရီ', 'end': 'ဇာတ်သိမ်း', 'action': 'အက်ရှင်', 'drama': 'ဒရာမာ', 'comedy': 'ကော်မဒီ', 'ok': 'အိုကေ', 'yes': 'ယက်စ်', 'no': 'နိုး', 'boy': 'ဘွိုင်း', 'girl': 'ဂဲလ်', 'man': 'မန်း', 'boss': 'ဘော့စ်', 'sir': 'ဆာ', 'mr': 'မစ္စတာ', 'miss': 'မစ်စ်', 'link': 'လင့်ခ်', 'video': 'ဗီဒီယို', 'update': 'အပ်ဒိတ်', 'tools': 'တူးလ်စ်', 'error': 'အဲရာ', 'code': 'ကုတ်', 'free': 'ဖရီး', 'vpn': 'ဗွီပီအန်', 'wifi': 'ဝိုင်ဖိုင်', 'internet': 'အင်တာနက်', 'group': 'ဂရု', 'post': 'ပို့စ်', 'live': 'လိုက်ဖ်', 'stream': 'စထရင်း', 'bot': 'ဘော့တ်', 'api': 'အေပီအိုင်', 'server': 'ဆာဗာ', 'app': 'အက်ပ်', 'game': 'ဂိမ်း', 'play': 'ပလေး', 'pause': 'ပေါ့စ်', 'stop': 'စတော့ပ်', 'next': 'နက်စ်', 'back': 'ဘက်', 'cancel': 'ကင်ဆယ်', 'save': 'ဆေ့ဖ်', 'delete': 'ဒိလစ်', 'edit': 'အက်ဒစ်', 'copy': 'ကော်ပီ', 'paste': 'ပေ့စ်', 'cut': 'ကတ်', 'settings': 'ဆက်တင်', 'profile': 'ပရိုဖိုင်', 'account': 'အကောင့်', 'login': 'လော့ဂ်အင်', 'logout': 'လော့ဂ်အောက်', 'password': 'ပတ်စ်ဝေါ့ဒ်', 'email': 'အီးမေးလ်', 'phone': 'ဖုန်း', 'message': 'မက်ဆေ့ချ်', 'chat': 'ချက်', 'call': 'ကော', 'video call': 'ဗီဒီယိုကော', 'voice': 'ဗွိုက်စ်', 'audio': 'အော်ဒီယို', 'sound': 'ဆောင်း', 'music': 'မြူးဇစ်', 'song': 'သီချင်း', 'singer': 'ဆင်ဂါ', 'actor': 'အက်တာ', 'actress': 'အက်ထရက်စ်', 'director': 'ဒါရိုက်တာ', 'producer': 'ပရိုဂျူဆာ', 'writer': 'ရိုက်တာ', 'camera': 'ကင်မရာ', 'photo': 'ဖိုတို', 'picture': 'ပစ်ချာ', 'image': 'အင်းမေ့ချ်', 'download': 'ဒေါင်းလုဒ်', 'upload': 'အပ်လုဒ်', 'install': 'အင်စတော', 'uninstall': 'အန်အင်စတော', 'upgrade': 'အပ်ဂရိတ်', 'premium': 'ပရီမီယမ်', 'pro': 'ပရို', 'vip': 'ဗွီအိုင်ပီ', 'ai': 'အေအိုင်', 'cpu': 'စီပီယူ', 'gpu': 'ဂျီပီယူ', 'ram': 'ရမ်', 'rom': 'ရွမ်', 'pc': 'ပီစီ', 'laptop': 'လက်ပ်တော့', 'mobile': 'မိုဘိုင်း', 'tablet': 'တက်ဘလက်', 'android': 'အန်ဒရွိုက်', 'ios': 'အိုင်အိုအက်စ်', 'windows': 'ဝင်းဒိုး', 'mac': 'မက်', 'linux': 'လင်းနစ်' };
            for (let word in wordMap) {
                let regex = new RegExp('\\b' + word + '\\b', 'gi');
                processedText = processedText.replace(regex, wordMap[word] + ' ');
            }

            // --- Send Data to Streamlit Python Backend ---
            Streamlit.setComponentValue({
                text: processedText,
                voice: selectedVoiceId,
                speed: speed,
                pitch: pitch,
                timestamp: Date.now()
            });
        }

        window.onload = function() {
            init();
            Streamlit.setComponentReady();
            setTimeout(() => Streamlit.setFrameHeight(), 100);

            const resizeObserver = new ResizeObserver(() => Streamlit.setFrameHeight());
            resizeObserver.observe(document.body);
        };
    </script>
</body>
</html>
"""

# --- 3. Streamlit Custom Component ဖန်တီးခြင်း ---
component_dir = os.path.join(os.path.dirname(__file__), "tts_ui_component")
os.makedirs(component_dir, exist_ok=True)
html_path = os.path.join(component_dir, "index.html")

# လိုအပ်မှသာ HTML ဖိုင်ကို အသစ်ပြန်ရေးရန် (Iframe Refresh မဖြစ်စေရန် File Check လုပ်ခြင်း)
write_html = True
if os.path.exists(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        if f.read() == HTML_CODE:
            write_html = False

if write_html:
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(HTML_CODE)

# HTML UI ကို Streamlit ထဲသို့ ထည့်သွင်းခြင်း
tts_ui = components.declare_component("tts_ui", path=component_dir)

# --- 4. Python Backend အလုပ်လုပ်မည့် အပိုင်း ---
VOICE_MAP = {
    "v1": "my-MM-ThihaNeural", "v2": "my-MM-NilarNeural", "v3": "it-IT-GiuseppeMultilingualNeural",
    "v4": "en-AU-WilliamMultilingualNeural", "v5": "en-US-AndrewMultilingualNeural",
    "v6": "en-US-AvaMultilingualNeural", "v7": "en-US-BrianMultilingualNeural",
    "v8": "en-US-EmmaMultilingualNeural", "v9": "fr-FR-RemyMultilingualNeural",
    "v10": "fr-FR-VivienneMultilingualNeural", "v11": "de-DE-SeraphinaMultilingualNeural",
    "v12": "de-DE-FlorianMultilingualNeural", "v13": "pt-BR-ThalitaMultilingualNeural",
    "v14": "ko-KR-HyunsuMultilingualNeural"
}

async def generate_tts(text, voice_id, speed, pitch):
    rate = f"{speed}%" if str(speed).startswith(("+", "-")) else f"+{speed}%"
    pitch_str = f"{pitch}Hz" if str(pitch).startswith(("+", "-")) else f"+{pitch}Hz"
    real_voice = VOICE_MAP.get(voice_id, "my-MM-ThihaNeural")

    output_file = f"temp_{uuid.uuid4().hex}.mp3"
    communicate = edge_tts.Communicate(text, real_voice, rate=rate, pitch=pitch_str)
    await communicate.save(output_file)
    return output_file

if "audio_b64" not in st.session_state:
    st.session_state.audio_b64 = None
if "error" not in st.session_state:
    st.session_state.error = None
if "last_timestamp" not in st.session_state:
    st.session_state.last_timestamp = None

ui_state = tts_ui(audio_b64=st.session_state.audio_b64, error=st.session_state.error)

if ui_state and ui_state.get("timestamp") != st.session_state.last_timestamp:
    st.session_state.last_timestamp = ui_state["timestamp"]
    st.session_state.error = None 
    
    text = ui_state.get("text", "")
    voice = ui_state.get("voice", "v1")
    speed = ui_state.get("speed", 0)
    pitch = ui_state.get("pitch", 0)
    
    try:
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
        output_file = loop.run_until_complete(generate_tts(text, voice, speed, pitch))
        
        with open(output_file, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
        
        os.remove(output_file) 
        
        st.session_state.audio_b64 = b64
        
    except Exception as e:
        st.session_state.error = str(e)
        st.session_state.audio_b64 = None
        
    st.rerun()
