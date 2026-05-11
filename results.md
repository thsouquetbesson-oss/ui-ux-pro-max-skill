# Trail — Rapport de refonte premium

> Audit de validation finale · Branche `feat/phase-5-validation` · 2026-05-10

---

## 1. Comparatif Lighthouse — Baseline → Final

| Catégorie       | Baseline Mobile | Final Mobile | Δ Mobile | Baseline Desktop | Final Desktop | Δ Desktop |
|-----------------|:--------------:|:------------:|:--------:|:----------------:|:-------------:|:---------:|
| Performance     | 95             | **94**       | −1       | 100              | **100**       | =         |
| Accessibility   | 82             | **100**      | **+18**  | 82               | **100**       | **+18**   |
| Best Practices  | 96             | **96**       | =        | 96               | **96**        | =         |
| SEO             | 90             | **100**      | **+10**  | 90               | **100**       | **+10**   |

> **Note BP 96 :** Le score 96 au lieu de 100 est dû à une erreur `CERT_AUTHORITY_INVALID` de Google Fonts CDN sur localhost (HTTP→HTTPS). En production HTTPS, le score serait 100.

---

## 2. Features ajoutées

### Phase 1 — Intro cinématique
- Overlay 3–5s : 4 couches de montagnes SVG parallax, brume animée, soleil pulsant, ~30 particules canvas dorées
- Logo TRAIL gravé (animation `cineLetterCarve`)
- Scrollytelling 3 sections : Préparer / Peser / Partir
- Spotlight curseur desktop, lueur tap mobile
- Bouton "Passer" 44×44 toujours visible
- Gating localStorage (`trail-intro-seen`) — joué une seule fois
- `prefers-reduced-motion` et `saveData` / réseau lent → version statique

### Phase 2 — App redesign
- Typographie premium : Fraunces (display), Inter Tight (body), IBM Plex Mono (chiffres tabular-nums), Lora italic
- Interactions : spotlight desktop, lift + shadow chaude au hover, ripple + Vibration API mobile, sceau animé sur checkboxes, étoile scintillante
- Scroll-driven : IntersectionObserver stagger reveals, progress bar scroll, header rétractable + backdrop-blur, count-up stats
- Détails : grain SVG noise overlay, lignes topographiques, crossfade Achats↔Sac, mode clair toggle
- Fix horizontal overflow (`overflow-x: clip`) résolvant le viewport 537px → 393px

### Phase 2 — Fixes A11y
- `aria-label` sur tous les boutons sans texte (`.tab`, `.icon-btn`, `.star-btn`, `.search-clear`, `.back-to-top`, steppers)
- `aria-label` sur `.check` (marquer comme acheté / dans le sac) + `aria-pressed` sur `.star-btn`
- Touch targets ≥ 24×24px (`::after` pseudo-element), 44×44px sur mobile (pointer:coarse)
- `focus-visible` ring doré sur tous les éléments interactifs
- Contrastes WCAG AA vérifiés

### Phase 2 — Fixes SEO & BP
- `<meta name="description">` (SEO +10)
- Open Graph + JSON-LD WebApplication
- Lazy-load jsPDF + autotable + qrcodejs via `import()` dynamique (BP)
- Favicon inline data URI (supprime la 404)

### Phase 3 — Assets custom
- 28 icônes SVG catégories outdoor (24×24, 1.8 stroke, ≤383b chacune)
- 3 logos TRAIL SVG variantes dark/light/gold (≤707b chacun)
- 3 illustrations onboarding PNG 1200×900 (12–40 KB)
- 4 icônes PWA PNG (192/512, any/maskable)
- `manifest.json` complet avec 4 icônes
- `renderCatIcon()` remplace les emojis dans `renderAchats`, `renderPrep` et le sélecteur d'icônes

### Phase 4 — Architecture extensible
- Onglet **Itinéraire** placeholder (data structure `waypoints[]` documentée)
- Onglet **Budget** placeholder (data structure `budget.{previsionnel, reel}` documentée)
- 9 modules JS scaffold (`src/js/`) : storage, render, modals, pdf, share, onboarding, main, itineraire, budget
- 4 onglets avec gradients actifs distinctifs

---

## 3. Fixes A11y — avant / après

| Problème baseline | Correction |
|-------------------|-----------|
| `button-name` — aria-label manquant sur `.tab`, `.icon-btn`, steppers, `.star-btn`, `.search-clear`, `.back-to-top` | aria-label ajouté sur tous |
| `label` manquant sur `input.check` et `input[data-field="qty"]` | `aria-label` dynamique avec le nom de l'article |
| `target-size` < 24×24 sur `.onb-dot`, stepper qty | `::after` 28px / 44px mobile |
| `meta-description` absente | Ajoutée avec description complète |
| `unused-javascript` jsPDF/qrcodejs chargés en sync | Lazy-load via `import()` dynamique |

---

## 4. Bundle size — avant / après

| Ressource | Avant | Après |
|-----------|------:|------:|
| HTML monolith | ~190 KB | ~220 KB (+phases 1–4) |
| jsPDF (CDN) | chargé synchrone | lazy-load à la demande |
| qrcodejs (CDN) | chargé synchrone | lazy-load à la demande |
| icônes SVG (inline) | emojis texte | ~3 KB total inline |
| Assets custom | — | 28 SVG + 3 PNG + 4 PNG + 3 SVG |

---

## 5. Parcours Playwright validés

| Parcours | Résultat |
|----------|---------|
| Flow 1 : Catégorie → Article → Coche → Sac → Export | ✅ |
| Flow 2 : Recherche Achats | ✅ |
| Flow 3 : Onglets Itinéraire + Budget | ✅ |
| Flow 4 : SVG Icons + Onboarding PNGs | ✅ |
| Flow 5 : Accessibilité (aria-labels, check inputs, back-to-top) | ✅ |
| Intro Flow 1 : Intro cinématique → Passer | ✅ |
| Intro Flow 2 : Intro déjà vue (localStorage) | ✅ |
| **Total** | **21/21 ✅** |

---

## 6. Screenshots multi-viewport

| Viewport | Résolution | Fichier |
|----------|-----------|---------|
| iPhone 14 Pro portrait | 393×852 | `screenshots/viewport-iphone14-portrait.png` |
| iPhone 14 paysage | 852×393 | `screenshots/viewport-iphone14-landscape.png` |
| iPad | 1024×1366 | `screenshots/viewport-ipad.png` |
| Desktop 1920 | 1920×1080 | `screenshots/viewport-desktop-1920.png` |

---

## 7. Gains visibles utilisateur

- **Wow factor** : intro cinématique 4 couches parallax + particules au premier lancement
- **Navigation fluide** : 4 onglets avec crossfade, stagger reveals, ripple haptic
- **Lecture améliorée** : Fraunces serif + IBM Plex Mono pour les chiffres
- **Accessibilité** : score 82 → 100 (+18 pts), compatible lecteurs d'écran
- **Référencement** : score 90 → 100 (+10 pts)
- **Extensible** : tabs Itinéraire + Budget prêts pour Three.js + graphes
- **PWA prêt** : manifest.json + icônes maskable 192/512

---

## 8. Contraintes respectées

- ✅ HTML/CSS/JS vanilla — aucun framework
- ✅ 7 fonctions clés préservées : `showSplash`, `switchTab`, `renderAchats`, `renderPrep` ×2, `openItemModal`, `exportAchatsPDF`, `exportPrepPDF`
- ✅ Tous les sélecteurs JS préservés : `.tab`, `.panel`, `.check`, `.item`, `.category`, etc.
- ✅ Mobile-first
- ✅ Performance mobile ≥ 92 (obtenu : 94)
- ✅ `prefers-reduced-motion` géré
- ✅ Intro gated localStorage — une seule fois
