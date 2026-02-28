import re

file_path = r"c:\Users\komal\OneDrive\Desktop\placement_prepration_tracker\placement_prepration_tracker\tracker\templates\dashboard.html"

with open(file_path, "r", encoding="utf-8") as f:
    html = f.read()

# Remove style tag
html = re.sub(r'\<style\>.*?\</style\>', '', html, flags=re.DOTALL)

# HTML body bg and main wrap
html = html.replace(
    '<body class="text-slate-600 antialiased font-sans">',
    '<body class="bg-slate-900 text-slate-300 antialiased font-sans flex flex-col items-center justify-start min-h-screen relative overflow-x-hidden">\n    <div class="fixed top-0 right-0 w-[600px] h-[600px] bg-blue-600 rounded-full blur-[180px] opacity-10 transform translate-x-1/3 -translate-y-1/3 pointer-events-none z-0"></div>\n    <div class="fixed bottom-0 left-0 w-[500px] h-[500px] bg-purple-600 rounded-full blur-[180px] opacity-10 transform -translate-x-1/3 translate-y-1/3 pointer-events-none z-0"></div>\n    <div class="relative z-10 w-full min-h-screen flex flex-col">'
)
html = html.replace('</body>', '    </div>\n</body>')

# Global replacements
html = html.replace('bg-white', 'bg-slate-800/50 backdrop-blur-md')
html = html.replace('border-slate-200', 'border-slate-700/50')
html = html.replace('border-slate-100', 'border-slate-700/50')
html = html.replace('shadow-soft', 'shadow-lg border-slate-700/50')

html = html.replace('text-slate-900', 'text-white')
html = html.replace('text-slate-500', 'text-slate-400')
html = html.replace('text-slate-600', 'text-slate-300')

html = html.replace('bg-slate-800/50 backdrop-blur-md border-b border-slate-700/50 sticky top-0 z-50', 'bg-slate-900/80 backdrop-blur-md border-b border-slate-800 sticky top-0 z-50')
html = html.replace('text-primary-600', 'text-primary-400')
html = html.replace('hover:text-white', 'hover:text-white')
html = html.replace('bg-slate-200', 'bg-slate-700/50')

html = html.replace('bg-primary-100 border border-primary-700/50', 'bg-primary-900/50 border border-primary-700/50')
html = html.replace('text-primary-700', 'text-primary-400')

html = html.replace('bg-blue-50 ', 'bg-blue-500/10 border border-blue-500/20 ')
html = html.replace('text-blue-600', 'text-blue-400')

html = html.replace('bg-green-50 text-green-700', 'bg-green-500/10 text-green-400 border border-green-500/20')
html = html.replace('bg-slate-100 h-1.5', 'bg-slate-700 h-1.5')
html = html.replace('text-green-700', 'text-green-400')

html = html.replace('bg-orange-50 ', 'bg-orange-500/10 border border-orange-500/20 ')
html = html.replace('text-orange-500', 'text-orange-400')

html = html.replace('bg-purple-50 ', 'bg-purple-500/10 border border-purple-500/20 ')
html = html.replace('text-purple-500', 'text-purple-400')

html = html.replace('hover:bg-slate-50', 'hover:bg-slate-800')

html = html.replace('bg-slate-50 rounded-lg border border-dashed border-slate-700/50', 'bg-slate-900/50 rounded-lg border border-dashed border-slate-700')
html = html.replace('bg-slate-700/50 flex', 'bg-slate-800 border-slate-700 text-slate-500 flex')

html = html.replace('bg-indigo-50 border border-indigo-100', 'bg-indigo-500/10 border border-indigo-500/20')
html = html.replace('text-indigo-600', 'text-indigo-400')
html = html.replace('text-indigo-400 group-hover:bg-primary-400', 'text-indigo-400 group-hover:bg-primary-600')

html = html.replace('bg-slate-50 rounded-lg py-1 border border-slate-700/50', 'bg-slate-900 rounded-lg py-1 border border-slate-700')

html = html.replace("color: '#f1f5f9'", "color: '#334155'")
html = html.replace("usePointStyle: true,", "color: '#e2e8f0', usePointStyle: true,")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(html)

print("Dashboard text replaced successfully!")
