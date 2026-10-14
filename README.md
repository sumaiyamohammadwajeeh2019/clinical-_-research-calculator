# Clinical & Research Variables Calculator
By **Dr. Sumaiya Mohammad, Physiologist, Bangladesh**

Physiology + clinical calculators: MAP, Pulse Pressure, Shock Index, Cardiac Output, BSA, BMI, Fluids (4-2-1), IBW (Devine), eGFR/CrCl (Cockcroft-Gault), Anion Gap, Corrected Calcium, Osmolality, Lipid panel (Friedewald LDL, VLDL, Non-HDL, TC/HDL).

## Run locally
```
pip install -r requirements.txt
python app.py
```
Open http://localhost:5000 — health: `/healthz`

## Deploy
- **Render:** uses `render.yaml` + `Procfile`, health check `/healthz`
- **Heroku/Railway:** `Procfile` → `gunicorn app:app`
- **Any static host (GitHub Pages/Netlify):** use `index.html` (standalone, no server needed)

## API
`POST /api/calculate` JSON e.g. `{"tc":200,"hdl":50,"tg":150}` → `{ldl, vldl, non_hdl, tc_hdl_ratio}` + echo.

## PWA
`static/manifest.json` + `static/service-worker.js` enabled for install/offline.
