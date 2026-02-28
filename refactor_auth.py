import os

templates = [
    r"c:\Users\komal\OneDrive\Desktop\placement_prepration_tracker\placement_prepration_tracker\tracker\templates\login.html",
    r"c:\Users\komal\OneDrive\Desktop\placement_prepration_tracker\placement_prepration_tracker\tracker\templates\register.html"
]

for file_path in templates:
    with open(file_path, "r", encoding="utf-8") as f:
        html = f.read()

    # Body background
    html = html.replace('bg-gray-50 text-slate-900', 'bg-slate-900 text-slate-300')
    html = html.replace('bg-white', 'bg-slate-800/50 backdrop-blur-md') # Right panel was white.
    
    # Right pane background
    html = html.replace('p-8 bg-slate-800/50 backdrop-blur-md', 'p-8 bg-slate-900 relative')
    
    # Text colors
    html = html.replace('text-gray-900', 'text-white')
    html = html.replace('text-gray-700', 'text-slate-300')
    html = html.replace('text-gray-500', 'text-slate-400')
    html = html.replace('text-gray-600', 'text-slate-400')
    html = html.replace('text-gray-400', 'text-slate-500')
    
    # Input fields
    html = html.replace('border-gray-300', 'border-slate-700')
    html = html.replace('text-white placeholder-gray-400', 'text-white placeholder-slate-500 bg-slate-800/50')
    
    # Checkbox
    html = html.replace('border-slate-700 text-blue-600', 'border-slate-700 bg-slate-800 text-blue-500')

    # Add blobs to right pane
    blob = '''<div class="absolute inset-0 opacity-20 pattern-grid" style="background-image: radial-gradient(circle at 2px 2px, rgba(255,255,255,0.05) 1px, transparent 0); background-size: 24px 24px;"></div>
        <div class="absolute bottom-0 right-0 w-[400px] h-[400px] bg-purple-600 rounded-full blur-[150px] opacity-10 transform translate-x-1/3 translate-y-1/3 pointer-events-none z-0"></div>
        <div class="absolute top-0 left-0 w-[400px] h-[400px] bg-blue-600 rounded-full blur-[150px] opacity-10 transform -translate-x-1/3 -translate-y-1/3 pointer-events-none z-0"></div>'''
    
    html = html.replace('<div class="w-full max-w-md">', blob + '\n        <div class="w-full max-w-md relative z-10">')
    html = html.replace('<div class="w-full max-w-md my-auto">', blob + '\n        <div class="w-full max-w-md my-auto relative z-10">')
    
    html = html.replace('bg-red-50 border border-red-200 text-red-700', 'bg-red-500/10 border border-red-500/20 text-red-400')
    html = html.replace('bg-blue-600 hover:bg-blue-700', 'bg-blue-600 hover:bg-blue-500 shadow-lg shadow-blue-600/30')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)

print("Auth text replaced successfully!")
