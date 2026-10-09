"""Public demo chrome; canonical workspace views remain byte-stable."""
def build(runtime, state):
    page = runtime.render(state).decode('utf-8')
    page = page.replace('</nav>', '<a href="index.html">← Zur Landingpage</a></nav>', 1)
    page = page.replace('Wissensraum · Offline', 'Synthetische Demo · Stand 9. Oktober 2026', 1)
    return page.encode('utf-8')
