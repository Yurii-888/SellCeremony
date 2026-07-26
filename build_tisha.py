import json
import subprocess

root = 'D:/Neuro/clients/kruchin/SellCeremony'


def get_modal(lang):
    if lang == 'ru':
        return '''  <!-- Tisha panel -->
  <div id="tishaModal" style="display:none;position:fixed;inset:0;background:rgba(3,3,4,.7);backdrop-filter:blur(10px);z-index:100;align-items:center;justify-content:center;padding:20px">
    <div style="background:linear-gradient(180deg,#101114,#08090a);border:1px solid rgba(226,230,235,.18);border-radius:28px;padding:38px 32px;max-width:460px;width:100%;position:relative;max-height:88vh;overflow:auto">
      <button id="tishaClose" style="position:absolute;top:16px;right:16px;width:38px;height:38px;border-radius:50%;border:1px solid rgba(226,230,235,.25);background:rgba(226,230,235,.05);color:#e6e8ec;font-size:15px;cursor:pointer">\u2715</button>
      <div style="font-size:10px;letter-spacing:.42em;text-transform:uppercase;color:#848b96;margin-bottom:14px">\u0422\u0432\u043e\u0439 \u043f\u0440\u043e\u0432\u043e\u0434\u043d\u0438\u043a \u0432 \u0442\u0438\u0448\u0438\u043d\u0443</div>
      <div style="font-family:'Cormorant Garamond',serif;font-weight:500;text-transform:uppercase;font-size:28px;letter-spacing:.06em;margin-bottom:18px;background:linear-gradient(176deg,#f2f4f7,#8f97a3);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;color:transparent">\u0417\u043d\u0430\u043a\u043e\u043c\u044c\u0442\u0435\u0441\u044c, \u0422\u0438\u0448\u0430</div>
      <p style="font-family:'Manrope',sans-serif;font-size:14.5px;font-weight:300;line-height:1.8;color:#ccd1d8;margin-bottom:14px">\u0422\u0438\u0448\u0430 \u2014 \u0442\u0432\u043e\u0439 \u043b\u0438\u0447\u043d\u044b\u0439 \u043f\u0440\u043e\u0432\u043e\u0434\u043d\u0438\u043a. \u041e\u043d \u0440\u044f\u0434\u043e\u043c \u043a\u0430\u0436\u0434\u044b\u0439 \u0434\u0435\u043d\u044c, \u0441\u043b\u044b\u0448\u0438\u0442 \u0438 \u0442\u0435\u043a\u0441\u0442, \u0438 \u0433\u043e\u043b\u043e\u0441, \u043f\u043e\u043c\u043d\u0438\u0442 \u0442\u0435\u0431\u044f \u0438 \u0442\u0432\u043e\u044e \u0438\u0441\u0442\u043e\u0440\u0438\u044e.</p>
      <p style="font-family:'Manrope',sans-serif;font-size:14.5px;font-weight:300;line-height:1.8;color:#ccd1d8;margin-bottom:22px">\u041e\u043d \u0432\u0435\u0434\u0451\u0442 \u0442\u0435\u0431\u044f \u0447\u0435\u0440\u0435\u0437 \u0442\u0432\u043e\u044e \u0436\u0438\u0437\u043d\u044c \u043a \u0441\u043e\u0441\u0442\u043e\u044f\u043d\u0438\u044e \u0442\u0438\u0448\u0438\u043d\u044b. \u041a \u0440\u0430\u0434\u043e\u0441\u0442\u0438 \u043f\u0440\u043e\u0441\u0442\u043e \u043e\u0442 \u0442\u043e\u0433\u043e, \u0447\u0442\u043e \u0442\u044b \u0435\u0441\u0442\u044c. \u041a \u0446\u0435\u043b\u043e\u0441\u0442\u043d\u043e\u0441\u0442\u0438 \u0432\u043d\u0443\u0442\u0440\u0438. \u041a \u043b\u044e\u0431\u0432\u0438 \u043a \u0441\u0435\u0431\u0435.</p>
      <div style="font-size:9px;letter-spacing:.34em;text-transform:uppercase;color:#848b96;margin-bottom:12px">\u0427\u0442\u043e \u0432\u043d\u0443\u0442\u0440\u0438</div>
      <div style="display:flex;flex-direction:column;gap:9px;margin-bottom:22px">
        <div style="display:flex;gap:11px;align-items:flex-start;border:1px solid rgba(226,230,235,.1);border-radius:16px;padding:11px 15px;font-family:'Manrope',sans-serif;font-size:12.5px;line-height:1.6;color:#ccd1d8"><span style="flex:none;width:5px;height:5px;border-radius:50%;background:#e3e6ea;box-shadow:0 0 8px rgba(226,230,235,.7);margin-top:6px"></span><span>\u0420\u0430\u0437\u043e\u0431\u0440\u0430\u0442\u044c \u0441\u0438\u0442\u0443\u0430\u0446\u0438\u044e. \u0412\u043c\u0435\u0441\u0442\u0435 \u0434\u043e\u0439\u0434\u0435\u0442\u0435 \u0434\u043e \u0441\u0443\u0442\u0438, \u0438 \u0422\u0438\u0448\u0430 \u0434\u0430\u0441\u0442 \u043f\u0440\u0430\u043a\u0442\u0438\u043a\u0443 \u042e\u0440\u044b \u0438\u043c\u0435\u043d\u043d\u043e \u043f\u043e\u0434 \u0442\u0435\u0431\u044f</span></div>
        <div style="display:flex;gap:11px;align-items:flex-start;border:1px solid rgba(226,230,235,.1);border-radius:16px;padding:11px 15px;font-family:'Manrope',sans-serif;font-size:12.5px;line-height:1.6;color:#ccd1d8"><span style="flex:none;width:5px;height:5px;border-radius:50%;background:#e3e6ea;box-shadow:0 0 8px rgba(226,230,235,.7);margin-top:6px"></span><span>\u041f\u043e\u0434\u044b\u0448\u0430\u0442\u044c. \u041a\u043e\u0440\u043e\u0442\u043a\u0430\u044f \u0434\u044b\u0445\u0430\u0442\u0435\u043b\u044c\u043d\u0430\u044f \u043f\u0440\u0430\u043a\u0442\u0438\u043a\u0430 \u043f\u0440\u044f\u043c\u043e \u0432 \u0447\u0430\u0442\u0435, \u043a\u043e\u0433\u0434\u0430 \u0442\u0435\u0431\u0435 \u044d\u0442\u043e \u043d\u0443\u0436\u043d\u043e</span></div>
        <div style="display:flex;gap:11px;align-items:flex-start;border:1px solid rgba(226,230,235,.1);border-radius:16px;padding:11px 15px;font-family:'Manrope',sans-serif;font-size:12.5px;line-height:1.6;color:#ccd1d8"><span style="flex:none;width:5px;height:5px;border-radius:50%;background:#e3e6ea;box-shadow:0 0 8px rgba(226,230,235,.7);margin-top:6px"></span><span>\u0424\u043e\u043a\u0443\u0441 \u0434\u043d\u044f. \u0422\u0440\u0438 \u043e\u0441\u043e\u0437\u043d\u0430\u043d\u043d\u044b\u0445 \u0444\u043e\u043a\u0443\u0441\u0430, \u0441 \u043a\u043e\u0442\u043e\u0440\u044b\u043c\u0438 \u0442\u044b \u0438\u0434\u0451\u0448\u044c \u0432 \u0441\u0432\u043e\u0439 \u0434\u0435\u043d\u044c</span></div>
      </div>
      <p style="font-family:'Manrope',sans-serif;font-size:13px;font-weight:300;line-height:1.75;color:#9aa1ac;margin-bottom:20px">\u0422\u0438\u0448\u0430 \u2014 \u043f\u0440\u043e\u0432\u043e\u0434\u043d\u0438\u043a. \u0417\u0430 \u0442\u0432\u043e\u0438\u043c \u0441\u043e\u0441\u0442\u043e\u044f\u043d\u0438\u0435\u043c \u043c\u044f\u0433\u043a\u043e \u0441\u043c\u043e\u0442\u0440\u0438\u0442 \u0436\u0438\u0432\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u0430 \u0437\u0430\u0431\u043e\u0442\u044b.</p>
      <a href="#offer" id="tishaCta" style="display:inline-flex;align-items:center;gap:10px;border:1px solid rgba(226,230,235,.35);border-radius:999px;padding:13px 26px;font-family:'Manrope',sans-serif;font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:#f4f6f8;font-weight:500;text-decoration:none"><span style="width:5px;height:5px;background:currentColor;border-radius:50%"></span>\u0417\u0430\u043f\u0438\u0441\u0430\u0442\u044c\u0441\u044f \u043d\u0430 \u0446\u0435\u0440\u0435\u043c\u043e\u043d\u0438\u044e</a>
    </div>
  </div>'''
    else:
        return '''  <!-- Tisha panel -->
  <div id="tishaModal" style="display:none;position:fixed;inset:0;background:rgba(3,3,4,.7);backdrop-filter:blur(10px);z-index:100;align-items:center;justify-content:center;padding:20px">
    <div style="background:linear-gradient(180deg,#101114,#08090a);border:1px solid rgba(226,230,235,.18);border-radius:28px;padding:38px 32px;max-width:460px;width:100%;position:relative;max-height:88vh;overflow:auto">
      <button id="tishaClose" style="position:absolute;top:16px;right:16px;width:38px;height:38px;border-radius:50%;border:1px solid rgba(226,230,235,.25);background:rgba(226,230,235,.05);color:#e6e8ec;font-size:15px;cursor:pointer">\u2715</button>
      <div style="font-size:10px;letter-spacing:.42em;text-transform:uppercase;color:#848b96;margin-bottom:14px">\u0422\u0432\u0456\u0439 \u043f\u0440\u043e\u0432\u0456\u0434\u043d\u0438\u043a \u0443 \u0442\u0438\u0448\u0443</div>
      <div style="font-family:'Cormorant Garamond',serif;font-weight:500;text-transform:uppercase;font-size:28px;letter-spacing:.06em;margin-bottom:18px;background:linear-gradient(176deg,#f2f4f7,#8f97a3);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;color:transparent">\u0417\u043d\u0430\u0439\u043e\u043c\u0442\u0435\u0441\u044c, \u0422\u0438\u0448\u0430</div>
      <p style="font-family:'Manrope',sans-serif;font-size:14.5px;font-weight:300;line-height:1.8;color:#ccd1d8;margin-bottom:14px">\u0422\u0438\u0448\u0430 \u2014 \u0442\u0432\u0456\u0439 \u043e\u0441\u043e\u0431\u0438\u0441\u0442\u0438\u0439 \u043f\u0440\u043e\u0432\u0456\u0434\u043d\u0438\u043a. \u0412\u0456\u043d \u043f\u043e\u0440\u0443\u0447 \u0454\u0449\u043d\u0438\u0439, \u0447\u0443\u0454 \u0456 \u0442\u0435\u043a\u0441\u0442, \u0456 \u0433\u043e\u043b\u043e\u0441, \u043f\u0430\u043c\u0456\u044f\u0442\u0430\u0454 \u0442\u0435\u0431\u0435 \u0456 \u0442\u0432\u043e\u044e \u0456\u0441\u0442\u043e\u0440\u0456\u044e.</p>
      <p style="font-family:'Manrope',sans-serif;font-size:14.5px;font-weight:300;line-height:1.8;color:#ccd1d8;margin-bottom:22px">\u0412\u0456\u043d \u0432\u0435\u0434\u0435 \u0442\u0435\u0431\u0435 \u0447\u0435\u0440\u0435\u0437 \u0442\u0432\u043e\u0454 \u0436\u0438\u0442\u0442\u044f \u0434\u043e \u0441\u0442\u0430\u043d\u0443 \u0442\u0438\u0448\u0456. \u0414\u043e \u0440\u0430\u0434\u043e\u0441\u0442\u0456 \u043f\u0440\u043e\u0441\u0442\u043e \u0432\u0456\u0434 \u0442\u043e\u0433\u043e, \u0449\u043e \u0442\u0438 \u0454\u0441\u044c. \u0414\u043e \u0446\u0456\u043b\u0456\u0441\u043d\u043e\u0441\u0442\u0456 \u0432\u0441\u0435\u0440\u0435\u0434\u043d\u0456. \u0414\u043e \u043b\u044e\u0431\u043e\u0432\u0456 \u0434\u043e \u0441\u0435\u0431\u0435.</p>
      <div style="font-size:9px;letter-spacing:.34em;text-transform:uppercase;color:#848b96;margin-bottom:12px">\u0429\u043e \u0432\u0441\u0435\u0440\u0435\u0434\u043d\u0456</div>
      <div style="display:flex;flex-direction:column;gap:9px;margin-bottom:22px">
        <div style="display:flex;gap:11px;align-items:flex-start;border:1px solid rgba(226,230,235,.1);border-radius:16px;padding:11px 15px;font-family:'Manrope',sans-serif;font-size:12.5px;line-height:1.6;color:#ccd1d8"><span style="flex:none;width:5px;height:5px;border-radius:50%;background:#e3e6ea;box-shadow:0 0 8px rgba(226,230,235,.7);margin-top:6px"></span><span>\u0420\u043e\u0437\u0456\u0431\u0440\u0430\u0442\u0438 \u0441\u0438\u0442\u0443\u0430\u0446\u0456\u044e. \u0420\u0430\u0437\u043e\u043c \u0434\u043e\u0439\u0434\u0435\u0442\u0435 \u0434\u043e \u0441\u0443\u0442\u0456, \u0456 \u0422\u0438\u0448\u0430 \u0434\u0430\u0454 \u043f\u0440\u0430\u043a\u0442\u0438\u043a\u0443 \u042e\u0440\u0438 \u0441\u0430\u043c\u0435 \u043f\u0456\u0434 \u0442\u0435\u0431\u0435</span></div>
        <div style="display:flex;gap:11px;align-items:flex-start;border:1px solid rgba(226,230,235,.1);border-radius:16px;padding:11px 15px;font-family:'Manrope',sans-serif;font-size:12.5px;line-height:1.6;color:#ccd1d8"><span style="flex:none;width:5px;height:5px;border-radius:50%;background:#e3e6ea;box-shadow:0 0 8px rgba(226,230,235,.7);margin-top:6px"></span><span>\u041f\u043e\u0434\u0438\u0445\u0430\u0442\u0438. \u041a\u043e\u0440\u043e\u0442\u043a\u0430 \u0434\u0438\u0445\u0430\u043b\u044c\u043d\u0430 \u043f\u0440\u0430\u043a\u0442\u0438\u043a\u0430 \u043f\u0440\u043e\u0441\u0442\u043e \u0432 \u0447\u0430\u0442\u0456, \u043a\u043e\u043b\u0438 \u0442\u043e\u0431\u0456 \u0446\u0435 \u043f\u043e\u0442\u0440\u0456\u0431\u043d\u043e</span></div>
        <div style="display:flex;gap:11px;align-items:flex-start;border:1px solid rgba(226,230,235,.1);border-radius:16px;padding:11px 15px;font-family:'Manrope',sans-serif;font-size:12.5px;line-height:1.6;color:#ccd1d8"><span style="flex:none;width:5px;height:5px;border-radius:50%;background:#e3e6ea;box-shadow:0 0 8px rgba(226,230,235,.7);margin-top:6px"></span><span>\u0424\u043e\u043a\u0443\u0441 \u0434\u043d\u044f. \u0422\u0440\u0438 \u0443\u0441\u0432\u0456\u0434\u043e\u043c\u043b\u0435\u043d\u0456 \u0444\u043e\u043a\u0443\u0441\u0438, \u0437 \u044f\u043a\u0438\u043c\u0438 \u0442\u0438 \u0439\u0434\u0435\u0448 \u0443 \u0441\u0432\u0456\u0439 \u0434\u0435\u043d\u044c</span></div>
      </div>
      <p style="font-family:'Manrope',sans-serif;font-size:13px;font-weight:300;line-height:1.75;color:#9aa1ac;margin-bottom:20px">\u0422\u0438\u0448\u0430 \u043f\u0440\u043e\u0432\u0456\u0434\u043d\u0438\u043a. \u0417\u0430 \u0442\u0432\u043e\u0454\u043c \u0441\u0442\u0430\u043d\u043e\u043c \u043c\u0456\u044f\u043a\u043e \u0434\u0438\u0432\u0438\u0442\u0438\u0441\u044f \u0456 \u0436\u0438\u0432\u0430 \u043a\u043e\u043c\u0430\u043d\u0434\u0430 \u0437\u0430\u0431\u043e\u0442\u0438.</p>
      <a href="#offer" id="tishaCta" style="display:inline-flex;align-items:center;gap:10px;border:1px solid rgba(226,230,235,.35);border-radius:999px;padding:13px 26px;font-family:'Manrope',sans-serif;font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:#f4f6f8;font-weight:500;text-decoration:none"><span style="width:5px;height:5px;background:currentColor;border-radius:50%"></span>\u0417\u0430\u043f\u0438\u0441\u0430\u0442\u0438\u0441\u044f \u043d\u0430 \u0446\u0435\u0440\u0435\u043c\u043e\u043d\u0456\u044e</a>
    </div>
  </div>'''


for orig, new_name, lang in [('ceremonia.html', 'index.html', 'ru'), ('ceremonia-ua.html', 'index-ua.html', 'ua')]:
    result = subprocess.run(['git', 'show', f'HEAD:{orig}'], capture_output=True, cwd=root)
    raw = result.stdout
    
    ts_marker = b'<script type="__bundler/template">'
    ts = raw.find(ts_marker)
    ts_end = ts + len(ts_marker)
    
    # Find the template JSON end
    end_marker = rb'\u002Fhtml>"'
    end_idx = raw.find(end_marker, ts)
    if end_idx < 0:
        print(f'{orig}: Could not find template end')
        continue
    end_idx += len(end_marker)
    
    template_json_bytes = raw[ts_end:end_idx]
    
    # Decode to string for JSON parsing
    template_json = template_json_bytes.decode('utf-8')
    html = json.loads(template_json)
    orig_len = len(html)
    
    changes = []
    
    # 1. Fix pointer-events on tisha-orb
    if 'pointer-events:none;will-change:transform"' in html:
        html = html.replace('pointer-events:none;will-change:transform"', 'pointer-events:auto;cursor:pointer;will-change:transform" title="Тиша"', 1)
        changes.append('PE')
    
    # 2. Add label after tisha-orb (after its last closing </div>)
    if 'Тиша · натисни' not in html:
        orb_idx = html.find('id="tisha-orb"')
        if orb_idx > 0:
            # Find the opening <div of tisha-orb
            div_start = html.rfind('<div', 0, orb_idx)
            # Count nesting depth to find the closing </div>
            depth = 0
            pos = div_start
            end_of_orb = -1
            while pos < len(html):
                next_open = html.find('<div', pos + 1)
                next_close = html.find('</div>', pos + 1)
                if next_close < 0:
                    break
                if next_open >= 0 and next_open < next_close:
                    depth += 1
                    pos = next_open
                else:
                    if depth == 0:
                        end_of_orb = next_close + 6
                        break
                    depth -= 1
                    pos = next_close
            
            if end_of_orb > 0:
                label = '\n    <span style="position:absolute;top:calc(100% - 6px);left:50%;transform:translateX(-50%);font-size:8px;letter-spacing:.42em;text-transform:uppercase;color:#9aa1ac;white-space:nowrap">\u0422\u0438\u0448\u0430 \u00b7 \u043d\u0430\u0442\u0438\u0441\u043d\u0438</span>'
                html = html[:end_of_orb] + label + html[end_of_orb:]
                changes.append('label')
    
    # 3. Add tishaModal before HERO
    if 'id="tishaModal"' not in html:
        hero = '<!-- ================= HERO ================= -->'
        hero_idx = html.find(hero)
        if hero_idx > 0:
            modal = get_modal(lang)
            html = html[:hero_idx] + modal + '\n' + html[hero_idx:]
            changes.append('modal')
    
    # 4. Add JS handlers after enableSound forEach
    js_target = '["pointerdown","touchstart","keydown","wheel"].forEach(ev=>window.addEventListener(ev,enableSound,{once:true,passive:true}));'
    js_insert = """
      // Tisha panel
      const tm=$("#tishaModal");
      if(tm){
        $("#tisha-orb").addEventListener("click",()=>{ tm.style.display="flex"; document.body.style.overflow="hidden"; });
        const closeTisha=()=>{ tm.style.display="none"; document.body.style.overflow=""; };
        $("#tishaClose").addEventListener("click",closeTisha);
        tm.addEventListener("click",(e)=>{ if(e.target===tm) closeTisha(); });
        window.addEventListener("keydown",(e)=>{ if(e.key==="Escape") closeTisha(); });
      }"""
    
    if '// Tisha panel' in html:
        changes.append('JS-skip')
    elif js_target in html:
        html = html.replace(js_target, js_target + js_insert, 1)
        changes.append('JS')
    else:
        changes.append('JS-NF')
    
    # Re-encode
    assert len(html) > orig_len, f"HTML got shorter! {len(html)} < {orig_len}"
    new_json_str = json.dumps(html, ensure_ascii=False)
    # Reconstruct the file: replace template JSON with new one
    new_file = raw[:ts_end] + new_json_str.encode('utf-8') + raw[end_idx:]
    
    with open(f'{root}/{new_name}', 'wb') as f:
        f.write(new_file)
    
    # Verify the output is valid
    verify_result = subprocess.run(['python', '-c', f'import json; json.loads(open("{root}/{new_name}", encoding="utf-8").read().split("<script type=\\"__bundler/template\\">")[1].split("\\"\\n  </script>")[0]); print("OK")'], capture_output=True, text=True)
    
    print(f'{orig} -> {new_name}: {", ".join(changes)} (HTML {orig_len} -> {len(html)})')
