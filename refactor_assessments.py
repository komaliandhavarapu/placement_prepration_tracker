import os
import re

templates = [
    r"c:\Users\komal\OneDrive\Desktop\placement_prepration_tracker\placement_prepration_tracker\tracker\templates\mock_test.html",
    r"c:\Users\komal\OneDrive\Desktop\placement_prepration_tracker\placement_prepration_tracker\tracker\templates\practice.html",
    r"c:\Users\komal\OneDrive\Desktop\placement_prepration_tracker\placement_prepration_tracker\tracker\templates\mock_interview.html"
]

for file_path in templates:
    if not os.path.exists(file_path):
        continue
        
    with open(file_path, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Backgrounds and text basics
    html = html.replace('bg-slate-900 text-white min-h-screen', 'bg-[#f8f5ff] text-slate-800 min-h-screen') 
    
    # 2. Accents
    # Keep the blue and purple blobs, they look good on the light theme too! We might just lower opacity or keep them.
    # Actually wait, let's keep them exactly as they are `opacity-10`.
    
    # 3. Headers and Titles
    html = html.replace('bg-slate-800/50 backdrop-blur-md border border-slate-700', 'bg-white shadow-[0_4px_20px_-4px_rgba(147,51,234,0.1)] border border-purple-100')
    html = html.replace('text-white', 'text-slate-900') # For titles
    html = html.replace('text-slate-400', 'text-slate-500') # Subtitles
    html = html.replace('text-slate-100', 'text-slate-800') # Question text
    html = html.replace('text-slate-300', 'text-slate-700') # Option text
    
    # 4. Question Cards
    html = html.replace('bg-slate-800/80 backdrop-blur-md border border-slate-700', 'bg-white shadow-sm border border-purple-50 hover:shadow-[0_4px_20px_-4px_rgba(147,51,234,0.1)] hover:border-purple-200 text-slate-900')
    html = html.replace('hover:bg-slate-800/90 hover:border-slate-600', '') # remove hover bg, keep shadow
    html = html.replace('bg-slate-700 text-blue-400 font-bold text-sm border border-slate-600', 'bg-purple-100 text-purple-700 font-bold text-sm border border-purple-200')
    html = html.replace('group-hover:bg-blue-600 group-hover:text-white group-hover:border-blue-500', 'group-hover:bg-purple-600 group-hover:text-white group-hover:border-purple-500')
    
    # 5. Options
    html = html.replace('border border-slate-700 bg-slate-900/50 hover:bg-slate-700 hover:border-blue-500/50', 'border border-purple-100 bg-purple-50/30 hover:bg-purple-50 hover:border-purple-400 text-slate-900')
    
    # 6. Buttons
    html = html.replace('bg-blue-600 hover:bg-blue-500 text-white font-bold rounded-2xl shadow-lg shadow-blue-600/30 text-lg', 'bg-purple-600 hover:bg-purple-700 text-white font-bold rounded-2xl shadow-lg shadow-purple-600/30 text-lg')
    html = html.replace('bg-blue-600 hover:bg-blue-500', 'bg-purple-600 hover:bg-purple-700')
    html = html.replace('shadow-blue-600/30', 'shadow-purple-600/30')
    
    html = html.replace('bg-slate-700 hover:bg-slate-600 text-white font-bold rounded-xl border border-slate-600', 'bg-white hover:bg-slate-50 text-slate-700 font-bold rounded-xl border border-slate-200')
    
    # 7. Timers / Icons
    html = html.replace('bg-blue-500/20 text-blue-400 flex justify-center items-center shadow-inner border border-blue-500/30', 'bg-purple-100 text-purple-600 flex justify-center items-center border border-purple-200')
    html = html.replace('bg-red-500/10 border border-red-500/20 px-5 py-2.5 rounded-xl flex items-center gap-3', 'bg-pink-50 border border-pink-200 px-5 py-2.5 rounded-xl flex items-center gap-3')
    html = html.replace('text-red-400 text-lg animate-pulse', 'text-pink-600 text-lg animate-pulse')
    html = html.replace('text-red-400 font-black text-xl tracking-widest', 'text-pink-600 font-black text-xl tracking-widest')
    
    # 8. Success / Submit View (in Mock test / Practice)
    html = html.replace('bg-slate-800/80 backdrop-blur-xl border border-slate-700', 'bg-white shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-purple-100')
    html = html.replace('bg-slate-900 border border-slate-700 text-green-400', 'bg-green-50 border border-green-200 text-green-600')
    html = html.replace('text-green-500/10 to-emerald-500/10', 'from-purple-50/50 to-fuchsia-50/50')
    
    # 9. Style Block Radio Buttons
    html = html.replace('box-shadow: inset 1em 1em #3b82f6;', 'box-shadow: inset 1em 1em #9333ea;') # purple-600
    html = html.replace('border-color: #3b82f6;', 'border-color: #9333ea;')
    
    # 10. AI Interview Specific
    html = html.replace('bg-slate-900/90 hidden', 'bg-white/95 hidden')
    html = html.replace('bg-slate-900 px-4 py-2 rounded-lg border border-slate-700 shadow-inner text-slate-900', 'bg-slate-50 px-4 py-2 rounded-lg border border-slate-200 shadow-sm text-slate-800')
    html = html.replace('bg-slate-900/50 p-4 rounded-xl border border-slate-700/50', 'bg-purple-50/50 p-4 rounded-xl border border-purple-100/50 text-slate-700')
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html)
        
print("Assessments text replaced successfully!")
