#!/usr/bin/env python3
"""
Trail — Full E2E Playwright test suite (Phase 5).
Covers: 5 app flows + cinematic intro + Passer intro + intro-already-seen.
"""
import sys, time, os
from pathlib import Path
from playwright.sync_api import sync_playwright

CHROMIUM = '/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell'
BASE_URL  = 'http://localhost:8080/trail-redesigned.html'
SS_DIR    = Path('/home/user/ui-ux-pro-max-skill/screenshots')
SS_DIR.mkdir(exist_ok=True)

results = []
failures = 0

def check(label, cond):
    global failures
    status = "✓" if cond else "✗"
    results.append(f"  {status} {label}")
    if not cond:
        failures += 1
        print(f"    FAIL: {label}")

def section(title):
    results.append(f"\n── {title} ──")
    print(f"\n[{title}]")

def skip_intro(page, timeout=2000):
    try:
        page.wait_for_selector('#cine-skip', timeout=timeout)
        page.evaluate("document.getElementById('cine-skip').click()")
        page.wait_for_selector('#cinematic-intro', state='detached', timeout=3000)
    except:
        pass

def fresh_ctx(browser, *, intro_seen=True, onb_done=True, viewport=None):
    vp = viewport or {"width": 393, "height": 852}
    ctx = browser.new_context(viewport=vp)
    scripts = []
    if intro_seen:
        scripts.append("localStorage.setItem('trail-intro-seen','1');")
    if onb_done:
        scripts.append("localStorage.setItem('trail-onboarding-done','1');")
    if scripts:
        ctx.add_init_script("".join(scripts))
    return ctx

with sync_playwright() as pw:
    browser = pw.chromium.launch(
        executable_path=CHROMIUM,
        args=['--no-sandbox','--disable-dev-shm-usage','--disable-web-security']
    )

    # ══════════════════════════════════════════════════════════════
    # FLOW 1 — Catégorie → Article → Coche → Switch panel → PDF
    # ══════════════════════════════════════════════════════════════
    section("Flow 1: Catégorie → Article → Coche → Sac → Export")
    ctx = fresh_ctx(browser)
    p = ctx.new_page()
    p.goto(BASE_URL)
    p.wait_for_selector('.category', timeout=6000)

    # 1a. Add a new category via direct function call
    cats_before = p.evaluate("document.querySelectorAll('.category').length")
    p.evaluate("openCategoryModal(null)")
    p.wait_for_selector('#cat-modal.show', timeout=3000)
    p.fill('#cat-name-input', 'Test Catégorie')
    p.evaluate("saveCategoryModal()")
    time.sleep(0.4)
    modal_gone = p.evaluate("!document.getElementById('cat-modal').classList.contains('show')")
    check(f"Category modal saved and closed", modal_gone)

    # 1b. Open item modal on first category
    first_cat_id = p.evaluate("document.querySelector('.category')?.dataset?.catId")
    p.evaluate(f"openItemModal('{first_cat_id}', null)")
    p.wait_for_selector('#item-modal.show', timeout=3000)
    p.fill('#item-name-input', 'Chaussures trail')
    p.fill('#item-price-input', '120')
    p.fill('#item-weight-input', '650')
    p.evaluate("saveItemModal()")
    time.sleep(0.4)

    items = p.evaluate("document.querySelectorAll('.item').length")
    check(f"Item created ({items} total)", items > 0)

    # 1c. Check the item (mark as purchased)
    p.evaluate("""
        () => {
            const chk = document.querySelector('.item .check');
            if (chk) chk.click();
        }
    """)
    time.sleep(0.2)
    checked = p.evaluate("document.querySelectorAll('.item.done').length")
    check(f"Item checked/done ({checked})", checked > 0)

    # 1d. Switch to Préparation tab
    p.evaluate("switchTab('prep')")
    time.sleep(0.3)
    prep_active = p.evaluate("document.getElementById('panel-prep').classList.contains('active')")
    check("Switched to Préparation panel", prep_active)

    # 1e. Try export PDF (just trigger — can't verify file in headless)
    exported = p.evaluate("""
        () => {
            if (typeof exportAchatsPDF === 'function') return true;
            return false;
        }
    """)
    check("exportAchatsPDF function accessible", exported)

    p.screenshot(path=str(SS_DIR / 'flow1-panel-prep.png'))
    ctx.close()

    # ══════════════════════════════════════════════════════════════
    # FLOW 2 — Recherche achats
    # ══════════════════════════════════════════════════════════════
    section("Flow 2: Recherche dans Achats")
    ctx = fresh_ctx(browser)
    p = ctx.new_page()
    p.goto(BASE_URL)
    p.wait_for_selector('.category', timeout=6000)

    p.fill('#search-achats', 'chaussures')
    time.sleep(0.3)
    clear_btn = p.query_selector('#panel-achats .search-clear')
    has_show = p.evaluate("document.querySelector('#panel-achats .search-clear').classList.contains('show')")
    check("Search clear button visible", has_show)

    p.evaluate("clearSearch('achats')")
    time.sleep(0.2)
    clear_gone = p.evaluate("!document.querySelector('#panel-achats .search-clear').classList.contains('show')")
    check("Search clear after clearSearch()", clear_gone)

    p.screenshot(path=str(SS_DIR / 'flow2-search.png'))
    ctx.close()

    # ══════════════════════════════════════════════════════════════
    # FLOW 3 — Placeholder tabs Itinéraire + Budget
    # ══════════════════════════════════════════════════════════════
    section("Flow 3: Onglets Itinéraire et Budget")
    ctx = fresh_ctx(browser)
    p = ctx.new_page()
    p.goto(BASE_URL)
    p.wait_for_selector('.tab', timeout=5000)

    p.evaluate("switchTab('itineraire')")
    time.sleep(0.3)
    itin = p.evaluate("document.getElementById('panel-itineraire').classList.contains('active')")
    check("Itinéraire panel active", itin)
    title_itin = p.evaluate("document.querySelector('#panel-itineraire .placeholder-title')?.textContent")
    check(f"Itinéraire placeholder title correct ('{title_itin}')", title_itin == 'Itinéraire')

    p.screenshot(path=str(SS_DIR / 'flow3-itineraire.png'))

    p.evaluate("switchTab('budget')")
    time.sleep(0.3)
    bud = p.evaluate("document.getElementById('panel-budget').classList.contains('active')")
    check("Budget panel active", bud)
    title_bud = p.evaluate("document.querySelector('#panel-budget .placeholder-title')?.textContent")
    check(f"Budget placeholder title correct ('{title_bud}')", title_bud == 'Budget')

    p.screenshot(path=str(SS_DIR / 'flow3-budget.png'))
    ctx.close()

    # ══════════════════════════════════════════════════════════════
    # FLOW 4 — SVG icons + Onboarding PNGs
    # ══════════════════════════════════════════════════════════════
    section("Flow 4: SVG Icons + Onboarding PNGs")
    ctx = fresh_ctx(browser)
    p = ctx.new_page()
    p.goto(BASE_URL)
    p.wait_for_selector('.category', timeout=5000)

    svg_in_cats = p.evaluate("document.querySelectorAll('.cat-emoji svg').length")
    check(f"SVG icons in category headers ({svg_in_cats})", svg_in_cats > 0)

    onb_imgs = p.evaluate("document.querySelectorAll('.onb-img').length")
    check(f"Onboarding PNG images in DOM ({onb_imgs})", onb_imgs == 3)

    p.screenshot(path=str(SS_DIR / 'flow4-categories-svg.png'))
    ctx.close()

    # ══════════════════════════════════════════════════════════════
    # FLOW 5 — A11y: aria-labels, focus ring, touch targets
    # ══════════════════════════════════════════════════════════════
    section("Flow 5: Accessibilité")
    ctx = fresh_ctx(browser)
    p = ctx.new_page()
    p.goto(BASE_URL)
    p.wait_for_selector('.category', timeout=5000)

    tabs_with_label = p.evaluate("document.querySelectorAll('.tab[aria-label]').length")
    check(f"All tabs have aria-label ({tabs_with_label}/4)", tabs_with_label == 4)

    check_inputs_with_label = p.evaluate("Array.from(document.querySelectorAll('input.check')).every(i => i.getAttribute('aria-label'))")
    check("All .check inputs have aria-label", check_inputs_with_label)

    back_label = p.evaluate("document.querySelector('.back-to-top')?.getAttribute('aria-label')")
    check(f"back-to-top has aria-label ('{back_label}')", bool(back_label))

    p.screenshot(path=str(SS_DIR / 'flow5-a11y.png'))
    ctx.close()

    # ══════════════════════════════════════════════════════════════
    # INTRO FLOW 1 — Cinematic intro complet (enter button)
    # ══════════════════════════════════════════════════════════════
    section("Intro Flow 1: Intro cinématique → Entrer")
    ctx = browser.new_context(viewport={"width": 393, "height": 852})
    p = ctx.new_page()
    p.goto(BASE_URL)
    try:
        p.wait_for_selector('#cinematic-intro:not([hidden])', timeout=3000)
        intro_shown = True
    except:
        intro_shown = False
    check("Cinematic intro shown on first load", intro_shown)

    if intro_shown:
        skip_btn = p.query_selector('#cine-skip')
        check("Skip button visible", bool(skip_btn))
        p.evaluate("document.getElementById('cine-skip').click()")
        try:
            p.wait_for_selector('#cinematic-intro', state='detached', timeout=4000)
            intro_gone = True
        except:
            intro_gone = False
        check("Intro dismissed after click", intro_gone)

    p.screenshot(path=str(SS_DIR / 'intro-dismissed.png'))
    ctx.close()

    # ══════════════════════════════════════════════════════════════
    # INTRO FLOW 2 — Intro déjà vue (localStorage)
    # ══════════════════════════════════════════════════════════════
    section("Intro Flow 2: Intro déjà vue (localStorage)")
    ctx = fresh_ctx(browser, intro_seen=True, onb_done=True)
    p = ctx.new_page()
    p.goto(BASE_URL)
    p.wait_for_load_state('networkidle')
    time.sleep(0.5)
    intro_absent = p.evaluate("!document.getElementById('cinematic-intro') || document.getElementById('cinematic-intro').hidden")
    check("Intro not shown when already seen", intro_absent)
    p.wait_for_selector('.category', timeout=5000)
    check("App renders directly", True)
    p.screenshot(path=str(SS_DIR / 'intro-already-seen.png'))
    ctx.close()

    browser.close()

# ══════════════════════════════════════════════════════════════════
# REPORT
# ══════════════════════════════════════════════════════════════════
print("\n" + "═"*52)
print("  TRAIL — Full E2E Test Suite Results")
print("═"*52)
for r in results:
    print(r)
passed = sum(1 for r in results if '✓' in r)
total  = sum(1 for r in results if ('✓' in r or '✗' in r))
print(f"\n{'═'*52}")
print(f"  {passed}/{total} passed  {'✅ ALL GOOD' if failures == 0 else f'❌ {failures} FAILED'}")
print("═"*52)

screenshots = list(SS_DIR.glob('*.png'))
print(f"\nScreenshots saved: {len(screenshots)}")
for s in sorted(screenshots):
    print(f"  {s.name}")

sys.exit(0 if failures == 0 else 1)
