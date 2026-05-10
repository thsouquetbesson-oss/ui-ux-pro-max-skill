# Trail — Diagnostic baseline pré-refonte premium

> Audit Lighthouse réalisé le 2026-05-09 sur `trail-redesigned.html`
> (4640 lignes, racine du repo, branche `claude/add-anthropic-skills-plugin-qalYJ`).

---

## 1. Scores baseline Lighthouse

| Catégorie       | Mobile | Desktop |
|-----------------|:------:|:-------:|
| Performance     |  95    |  100    |
| Accessibility   |  82    |   82    |
| Best Practices  |  96    |   96    |
| SEO             |  90    |   90    |
| PWA             |  N/A*  |  N/A*   |

*\*Lighthouse 13 ne note plus la catégorie PWA depuis la v12.*

---

## 2. Top 5 problèmes prioritaires

| # | Problème | Cible | Impact | Effort |
|---|----------|-------|:------:|:------:|
| 1 | `button-name` — `aria-label` manquant | `.tab` (Achats / Préparation), `.icon-btn` (edit / delete catégorie), `[data-step="qty-minus"]` / `[data-step="qty-plus"]`, `.star-btn`, `.search-clear`, `.back-to-top` | A11y +6 à +8 | Facile |
| 2 | `label` — labels manquants sur les inputs | `<input class="check">`, `<input data-field="qty">` | A11y +6 | Facile |
| 3 | `target-size` — touch targets < 24×24px | `.onb-dot`, stepper qty input | A11y +4 | Facile |
| 4 | `meta-description` absente dans `<head>` | `<head>` | SEO +10 | Facile |
| 5 | `unused-javascript` + `unused-css-rules` — 46 KB JS + 35 KB CSS chargés en synchrone et non utilisés au boot | `jsPDF`, `jspdf-autotable`, `qrcodejs` (CDN cdnjs) | Perf mobile +3 à +5 / BP +4 | Moyen |

> Note : les `errors-in-console` (CERT_AUTHORITY_INVALID, 404) sont des artefacts du test local HTTPS→localhost et ne sont pas un vrai problème prod.

---

## 3. Plan des phases — objectifs mesurables

### Phase 1 — Intro cinématique (effet WOW)
**Branche :** `feat/phase-1-cinematic-intro`
- Cinematic landing 3-5s : silhouette montagne SVG parallax 4 couches, brume animée, soleil levant pulse, particules dorées canvas (~30), logo TRAIL gravure-dans-roche, scrollytelling 3 sections (Préparer / Peser / Partir), spotlight curseur desktop, lueur-au-tap mobile, parallax mouse-follow.
- **Contraintes :** ≤ 200 KB total · 60 FPS iPhone 12+ · `prefers-reduced-motion` géré · bouton "Passer" 44×44 toujours visible · joué une seule fois (`localStorage: trail-intro-seen`) · data-saver = intro statique.
- **Objectif perf :** Performance mobile ≥ 92 (ne pas chuter sous baseline – 3).
- **Livrables :** screenshots intro frame 1/2/3 + écran final, delta Lighthouse vs baseline, parcours Playwright "intro complet" + "Passer".

### Phase 2 — App redesign (sobre + raffiné)
**Branche :** `feat/phase-2-app-redesign`
- Typo : Fraunces (display, axes opsz/SOFT/WONK), Inter Tight (body), IBM Plex Mono (chiffres tabular-nums), Lora italic (accents).
- Interactions : spotlight discret desktop, cards lift + shadow chaude au hover, ripple + Vibration API mobile, sceau animé sur checkboxes, étoile scintillante sur essentiels, bordure respire au focus, modals scale + blur, toast slide-bottom avec rebond.
- Scroll-driven : IntersectionObserver révèle catégories (stagger 50→300ms), progress bar scroll, header rétracte + backdrop-blur, count-up sur stats.
- Détails : grain SVG noise overlay, lignes topographiques décor, crossfade Achats↔Sac, mode clair toggle.
- **Fixes A11y intégrés** : `aria-label` sur tous boutons sans texte, `<label>`/`aria-label` sur `.check` + qty, touch targets 24×24 min (44×44 mobile), contrastes WCAG AA, sémantique `<main>`/`<nav>`/`<section>`, `focus-visible` ring doré.
- **Fixes SEO** : `<meta name="description">`, Open Graph, JSON-LD WebApplication, `<html lang="fr">` vérifié.
- **Fixes BP** : lazy-load jsPDF + autotable + qrcodejs via `import()` dynamique, zéro erreur console, ressources HTTPS.
- **Préservation absolue** des IDs/classes manipulés : `.tab`, `.panel`, `.check`, `.item`, `.category`, `.field`, `.stepper`, `.star-btn`, `.add-item-btn`, `.empty-state`, `.highlight`, `.collapsed`, `.done`, `.taken`, `.selected`, `.show`, `.hide`, `.over`, `.has-margin`, `.search-match` etc.
- **Vérif** : `grep -c "function showSplash\|switchTab\|renderAchats\|renderPrep\|openItemModal\|exportAchatsPDF\|exportPrepPDF" trail-redesigned.html` → 7.
- **Objectifs Lighthouse mobile** : Perf ≥ 95 · A11y ≥ 95 · BP = 100 · SEO ≥ 95.
- **Livrables :** screenshots Achats / Préparation / modal item / modal trek, parcours Playwright complet (catégorie → article → coche → switch panel → export PDF).

### Phase 3 — Assets custom (canvas-design)
**Branche :** `feat/phase-3-custom-assets`
- Logo TRAIL premium SVG (montagne stylisée + lettres custom) — variantes dark/light/doré ≤ 5 KB.
- 3 illustrations onboarding PNG 2× (≤ 80 KB chacune) : sac low-poly, étalage outdoor, sac coupé silhouette.
- 24 icônes SVG catégories (≤ 2 KB chacune) remplaçant les emojis.
- Favicon + icônes PWA 192/512 (maskable + standard).
- Splash screens iOS par tailles courantes.
- **Objectif perf :** Performance mobile ≥ 92 (poids assets contrôlé).

### Phase 4 — Architecture extensible
**Branche :** `feat/phase-4-architecture`
- Onglet "Itinéraire" placeholder (futur Three.js + low-poly + parcours animé, structure data `waypoints[{lat, lng, alt, label, day, etape}]`).
- Onglet "Budget" placeholder (futur graph prévisionnel vs réel, structure `budget = { previsionnel: {cat: amount}, reel: [{date, cat, label, amount}] }`).
- Refactor JS en modules : `storage.js`, `render.js`, `modals.js`, `pdf.js` (lazy), `share.js` (lazy), `onboarding.js`, `main.js`, `itineraire.js` (vide), `budget.js` (vide).
- **Vérif :** les 7 fonctions clés réparties dans les modules toujours présentes (grep = 7).

### Phase 5 — Validation finale
**Branche :** `feat/phase-5-validation`
- 5 parcours Playwright + intro cinématique + Passer intro + intro déjà vue (localStorage). Zéro bug toléré.
- Tableau comparatif Lighthouse baseline → final (mobile + desktop).
- Screenshots multi-viewport : iPhone 14 Pro portrait, mobile paysage 852×393, iPad 1024×1366, desktop 1920×1080, 4K 3840×2160.
- Test perf throttlé (CPU 4× + 3G slow) : intro graceful-degrade, app utilisable.
- Rapport `results.md` final : comparatif baseline vs final · features ajoutées · fixes A11y · liens screenshots · bundle size avant/après · gains visibles utilisateur.

---

## 4. Objectifs mobile à l'issue de la refonte

| Catégorie       | Baseline | Cible | Δ      |
|-----------------|:--------:|:-----:|:------:|
| Performance     | 95       | ≥ 95  | maintien |
| Accessibility   | 82       | ≥ 95  | **+13** |
| Best Practices  | 96       | 100   | **+4**  |
| SEO             | 90       | ≥ 95  | **+5**  |

---

## 5. Contraintes globales

- **HTML/CSS/JS vanilla** — aucun framework.
- **Préservation absolue** de la logique métier (les 7 fonctions clés et tous les sélecteurs JS doivent rester intacts).
- **Mobile-first** dans toute décision design.
- **Performance > esthétique** en cas de conflit.
- **Une branche par phase**, validation explicite avant chaque suivante.
