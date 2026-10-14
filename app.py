from flask import Flask, render_template_string, request, jsonify, send_from_directory
import os
import json
import logging

APP_NAME = "Clinical & Research Variables Calculator"
AUTHOR_NAME = "Dr. Sumaiya Mohammad, Physiologist, Bangladesh"
ADSENSE_CLIENT = os.environ.get("ADSENSE_CLIENT_ID", "ca-pub-XXXXXXXXXXXXXXXX")
PRO_API_KEY = os.environ.get("PRO_API_KEY", "demo-pro-key-123")
CONTACT_EMAIL = os.environ.get("CONTACT_EMAIL", "physiologypro.contact@gmail.com")

app = Flask(__name__)

# --- YOUR HTML CODE (Physiology Pro) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Clinical & Research Variables Calculator</title>
<meta name="description" content="Clinical & Research Variables Calculator by Dr. Sumaiya Mohammad, Physiologist, Bangladesh. Free MAP, BMI, GFR, Fluids, Electrolyte, Lipid calculators for clinical and research use.">
<link rel="canonical" href="/">
<meta name="theme-color" content="#0b3d91">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_CLIENT}" crossorigin="anonymous"></script>
<link rel="manifest" href="/static/manifest.json">
<link rel="icon" type="image/svg+xml" href="/static/icon-192.svg">
<link rel="apple-touch-icon" href="/static/icon-192.svg">
<style>
.ad-label{font-size:9px;color:#94a3b8;text-align:center;letter-spacing:1px;margin-bottom:2px}
.ad-box{background:#f8fafc;border:1px dashed #cbd5e1;border-radius:8px;padding:6px;margin:10px 0;text-align:center;min-height:90px}
.pro-wrap{background:linear-gradient(135deg,#1e1b4b,#6d28d9);border-radius:12px;padding:16px;color:#fff;margin:10px 0}
.pro-grid{display:flex;gap:10px;flex-wrap:wrap;margin-top:10px}.pro-card{flex:1;min-width:200px;background:#fff;color:#1e293b;border-radius:10px;padding:12px;text-align:center}
.pro-price{font-size:22px;font-weight:900}.pro-btn{display:inline-block;margin-top:8px;padding:8px 16px;border-radius:8px;font-weight:800;text-decoration:none;cursor:pointer;border:none}
.pro-details{background:rgba(255,255,255,.12);border-radius:8px;padding:8px;margin-top:10px;font-size:11px}
.pro-details summary{cursor:pointer;font-weight:800}
#proTable{display:none;margin-top:10px}
:root{--b:#0b3d91}
*{font-family:system-ui,Arial,sans-serif;box-sizing:border-box}
body{background:#eef2f7;padding:6px;margin:0}
.p{background:#fff;max-width:900px;margin:auto;border-radius:12px;padding:14px;box-shadow:0 4px 15px rgba(0,0,0,.08)}
.h{background:linear-gradient(135deg,#0b3d91,#2563eb);color:#fff;padding:14px;border-radius:10px;margin:-14px -14px 12px -14px;text-align:center}
label{font-size:9px;font-weight:800;color:#334155;display:block;margin-top:8px;text-transform:none}
input,select{width:100%;padding:8px;border:1.5px solid #cbd5e1;border-radius:7px;font-size:13px;margin-top:2px}
.s{background:#eef6ff;border-left:4px solid var(--b);padding:6px 10px;font-weight:800;color:var(--b);margin:14px 0 8px 0;font-size:11px;border-radius:0 6px 6px 0}
.r{display:flex;gap:8px;flex-wrap:wrap}.r>div{flex:1;min-width:120px}
.box{border:2px solid #e2e8f0;border-radius:10px;padding:10px;text-align:center;flex:1;min-width:140px;background:#fff}
.val{font-size:20px;font-weight:900}
.badge{font-size:9px;padding:3px 8px;border-radius:20px;font-weight:700;display:inline-block}
.logo{display:flex;align-items:center;justify-content:center;gap:10px}
.logo img{width:48px;height:48px;border-radius:12px;background:#fff;padding:4px;box-shadow:0 2px 8px rgba(0,0,0,.2)}
</style></head><body><div class="p">
<div class="h"><div class="logo"><img src="/static/icon-192.svg" alt="ClinicCalc logo"><div style="text-align:left"><div style="font-size:16px;font-weight:900;line-height:1.1">Clinical & Research Variables Calculator</div><div style="font-size:11px;font-weight:700">Dr. Sumaiya Mohammad, Physiologist, Bangladesh</div></div></div><p style="margin:6px 0 0 0;font-size:10px;opacity:.9">MAP | BSA | Shock Index | Pulse Pressure | GFR | CrCl | Fluid | BMI | Anion Gap | Corrected Ca | Lipid | Mg</p></div>
<div class="s">INPUTS - Auto Calculate</div>
<div style="font-size:10px;color:#64748b;margin:4px 0">Enter patient values — normal range shown under each variable.</div>
<div class="r">
<div><label for="bp">BP ex: 120/80</label><input id="bp" name="bp" placeholder="120/80" oninput="calc()"><small style="font-size:9px;color:#64748b">N: 90/60 - 120/80</small></div>
<div><label for="hr">Pulse HR</label><input id="hr" name="hr" type="number" placeholder="80" oninput="calc()"><small style="font-size:9px;color:#64748b">N: 60-100 bpm</small></div>
<div><label for="wt">Weight kg</label><input id="wt" name="wt" type="number" placeholder="65" oninput="calc()"><small style="font-size:9px;color:#64748b">Adult: 50-80 kg</small></div>
<div><label for="ht">Height cm</label><input id="ht" name="ht" type="number" placeholder="170" oninput="calc()"><small style="font-size:9px;color:#64748b">Adult: 150-180 cm</small></div>
<div><label for="age">Age</label><input id="age" name="age" type="number" placeholder="40" oninput="calc()"><small style="font-size:9px;color:#64748b">Years</small></div>
<div><label for="sex">Sex</label><select id="sex" name="sex" onchange="calc()"><option>Male</option><option>Female</option></select><small style="font-size:9px;color:#64748b">M / F</small></div>
</div>
<div class="r">
<div><label for="cr">Creatinine mg/dl</label><input id="cr" name="cr" type="number" step="0.1" placeholder="1.0" oninput="calc()"><small style="font-size:9px;color:#64748b">N: 0.6-1.2</small></div>
<div><label for="na">Na mEq/l</label><input id="na" name="na" type="number" placeholder="140" oninput="calc()"><small style="font-size:9px;color:#64748b">N: 135-145</small></div>
<div><label for="cl">Cl mEq/l</label><input id="cl" name="cl" type="number" placeholder="100" oninput="calc()"><small style="font-size:9px;color:#64748b">N: 98-107</small></div>
<div><label for="hco3">HCO3 mEq/l</label><input id="hco3" name="hco3" type="number" placeholder="24" oninput="calc()"><small style="font-size:9px;color:#64748b">N: 22-28</small></div>
<div><label for="alb">Albumin g/dl</label><input id="alb" name="alb" type="number" placeholder="4.0" oninput="calc()"><small style="font-size:9px;color:#64748b">N: 3.5-5.5</small></div>
<div><label for="ca">Ca mg/dl</label><input id="ca" name="ca" type="number" placeholder="9.5" oninput="calc()"><small style="font-size:9px;color:#64748b">N: 8.5-10.5</small></div>
</div>
<div class="r">
<div><label for="bun">BUN mg/dl</label><input id="bun" name="bun" type="number" placeholder="15" oninput="calc()"><small style="font-size:9px;color:#64748b">N: 7-20</small></div>
<div><label for="glu">Glucose mg/dl</label><input id="glu" name="glu" type="number" placeholder="100" oninput="calc()"><small style="font-size:9px;color:#64748b">N fasting: 70-100</small></div>
<div><label for="sv">Stroke Volume ml</label><input id="sv" name="sv" type="number" value="70" oninput="calc()"><small style="font-size:9px;color:#64748b">N: 50-100</small></div>
</div>
<div class="r">
<div><label for="tc">Total Cholesterol mg/dl</label><input id="tc" name="tc" type="number" placeholder="200" oninput="calc()"><small style="font-size:9px;color:#64748b">N: <200</small></div>
<div><label for="hdl">HDL mg/dl</label><input id="hdl" name="hdl" type="number" placeholder="50" oninput="calc()"><small style="font-size:9px;color:#64748b">N: M>40 F>50</small></div>
<div><label for="tg">Triglycerides mg/dl</label><input id="tg" name="tg" type="number" placeholder="150" oninput="calc()"><small style="font-size:9px;color:#64748b">N: <150</small></div>
<div><label for="mg">Magnesium mg/dl</label><input id="mg" name="mg" type="number" step="0.1" placeholder="2.0" oninput="calc()"><small style="font-size:9px;color:#64748b">N: 1.7-2.2</small></div>
</div>
<div class="s">1. VITAL CALCULATORS</div>
<div class="r">
<div class="box" style="border-color:#f59e0b"><div style="font-size:9px;font-weight:800">MAP</div><div id="mapV" class="val" style="color:#d97706">-- mmHg</div><div id="mapB" class="badge" style="background:#fef3c7">Formula: (SBP+2DBP)/3</div></div>
<div class="box" style="border-color:#0ea5e9"><div style="font-size:9px;font-weight:800">PULSE PRESSURE</div><div id="ppV" class="val" style="color:#0b3d91">-- mmHg</div><div id="ppB" class="badge" style="background:#e0f2fe">SBP-DBP | N:40-60</div></div>
<div class="box" style="border-color:#ef4444"><div style="font-size:9px;font-weight:800">SHOCK INDEX</div><div id="siV" class="val" style="color:#dc2626">--</div><div id="siB" class="badge" style="background:#fee2e2">HR/SBP | <0.7 N, >1 Shock</div></div>
<div class="box" style="border-color:#0891b2"><div style="font-size:9px;font-weight:800">CARDIAC OUTPUT</div><div id="coV" class="val" style="color:#0891b2">-- l/min</div><div class="badge" style="background:#cffafe">HR × SV</div></div>
</div>
<div class="s">2. BODY CALCULATORS</div>
<div class="r">
<div class="box" style="border-color:#16a34a"><div style="font-size:9px;font-weight:800">BSA</div><div id="bsaV" class="val" style="color:#16a34a">-- m²</div><div class="badge" style="background:#dcfce7">√(H×W/3600)</div></div>
<div class="box" style="border-color:#7c3aed"><div style="font-size:9px;font-weight:800">BMI</div><div id="bmiV" class="val">--</div><div id="bmiB" class="badge" style="background:#ede9fe">--</div></div>
<div class="box" style="border-color:#ea580c"><div style="font-size:9px;font-weight:800">FLUID (4-2-1)</div><div id="fluidV" class="val" style="color:#ea580c">-- ml/hr</div><div id="fluidB" class="badge" style="background:#ffedd5">-- /day</div></div>
<div class="box" style="border-color:#7c3aed"><div style="font-size:9px;font-weight:800">IBW Devine</div><div id="ibwV" class="val" style="color:#7c3aed">-- kg</div><div class="badge" style="background:#ede9fe">Ideal Weight</div></div>
</div>
<div class="s">3. KIDNEY + ELECTROLYTE</div>
<div class="r">
<div class="box" style="border-color:#7c3aed;background:#f5f3ff"><div style="font-size:9px;font-weight:800">eGFR / CrCl</div><div id="gfrV" class="val" style="color:#7c3aed">-- ml/min</div><div id="gfrB" class="badge" style="background:#ede9fe">Cockcroft-Gault</div></div>
<div class="box" style="border-color:#0891b2"><div style="font-size:9px;font-weight:800">ANION GAP</div><div id="agV" class="val">--</div><div id="agB" class="badge" style="background:#cffafe">Na-(Cl+HCO3)</div></div>
<div class="box" style="border-color:#16a34a"><div style="font-size:9px;font-weight:800">CORRECTED CALCIUM</div><div id="caV" class="val" style="color:#16a34a">--</div><div class="badge" style="background:#dcfce7">Ca+0.8×(4-Alb)</div></div>
<div class="box" style="border-color:#0e7490"><div style="font-size:9px;font-weight:800">OSMOLALITY</div><div id="osmV" class="val">--</div><div class="badge" style="background:#ccfbf1">2Na+Glu/18+BUN/2.8</div></div>
<div class="box" style="border-color:#047857;background:#ecfdf5"><div style="font-size:9px;font-weight:800">CORRECTED MAGNESIUM</div><div id="cmgV" class="val" style="color:#047857">-- mg/dl</div><div id="cmgB" class="badge" style="background:#a7f3d0">Mg+0.005×(40-Alb g/l)</div></div>
</div>
<div class="s">4. LIPID CALCULATOR - Friedewald</div>
<div class="r">
<div class="box" style="border-color:#dc2626;background:#fef2f2"><div style="font-size:9px;font-weight:800">LDL CHOLESTEROL</div><div id="ldlV" class="val" style="color:#dc2626">-- mg/dl</div><div id="ldlB" class="badge" style="background:#fee2e2">TC-HDL-TG/5</div></div>
<div class="box" style="border-color:#f59e0b"><div style="font-size:9px;font-weight:800">VLDL (TG/5)</div><div id="vldlV" class="val" style="color:#d97706">-- mg/dl</div><div id="vldlB" class="badge" style="background:#fef3c7">TG/5 | TG N &lt;150</div></div>
<div class="box" style="border-color:#7c3aed;background:#f5f3ff"><div style="font-size:9px;font-weight:800">NON-HDL</div><div id="nonhdlV" class="val" style="color:#7c3aed">-- mg/dl</div><div id="nonhdlB" class="badge" style="background:#ede9fe">TC-HDL | Goal &lt;130</div></div>
<div class="box" style="border-color:#0891b2"><div style="font-size:9px;font-weight:800">TC/HDL RATIO</div><div id="tchrV" class="val" style="color:#0891b2">--</div><div id="tchrB" class="badge" style="background:#cffafe">Ideal &lt;3.5</div></div>
</div>
<div class="s">INTERPRETATION</div>
<div id="interp" style="background:#f8fafc;border:1.5px solid #e2e8f0;border-radius:8px;padding:10px;font-size:11px;line-height:1.6">Enter BP as 120/80 to start auto calculation...</div>
<div class="ad-box"><div class="ad-label">ADVERTISEMENT</div><ins class="adsbygoogle" style="display:block" data-ad-client="{ADSENSE_CLIENT}" data-ad-slot="2345678901" data-ad-format="auto" data-full-width-responsive="true"></ins><script>(adsbygoogle=window.adsbygoogle||[]).push({});</script></div>
<div class="s">PRO FOR CLINICS, HOSPITALS & INSTITUTIONS</div>
<div class="pro-wrap">
<div style="font-size:13px;font-weight:900">PRO — For Clinics, Hospitals & Institutions</div>
<div style="font-size:11px;opacity:.9;margin-top:4px">Bulk calculations • EMR integration • No ads • Priority support</div>
<div style="margin-top:10px"><button class="pro-btn" style="background:#fbbf24;color:#1e1b4b" onclick="document.getElementById('proTable').style.display=document.getElementById('proTable').style.display==='block'?'none':'block'">Request Clinic Key →</button></div>
<div id="proTable">
<div class="pro-grid">
<div class="pro-card"><div style="font-size:10px;font-weight:800;color:#64748b">FREE</div><div class="pro-price">৳0 / $0</div><div style="font-size:11px">All calculators<br>Print results<br>With ads</div><details class="pro-details" style="color:#fff;background:rgba(0,0,0,.2)"><summary>Current plan</summary><div style="margin-top:6px">You are on FREE — ৳0 / $0 forever. No key needed.</div></details></div>
<div class="pro-card" style="border:2px solid #fbbf24"><div style="font-size:10px;font-weight:800;color:#7c3aed">PRO CLINIC</div><div class="pro-price">৳1,500/year</div><div style="font-size:10px;font-weight:800;color:#059669;background:#d1fae5;border-radius:6px;padding:2px 6px;display:inline-block;margin-top:4px">Introductory Offer (Regular ৳5,000)</div><div style="font-size:11px;text-align:left">Bulk use<br>EMR integration (API)<br>No ads<br>Clinic API key<br>Priority support</div><a class="pro-btn" style="background:#7c3aed;color:#fff" href="/contact">Contact to Get Key →</a><div style="font-size:11px;margin-top:6px;font-weight:700">physiologypro.contact@gmail.com</div><details class="pro-details" style="color:#1e293b;background:#f1f5f9"><summary>For IT Team: POST /api/pro/calculate with X-API-Key</summary><div style="margin-top:6px;text-align:left">Send POST JSON to <code>/api/pro/calculate</code> with header <code>X-API-Key: YOUR-CLINIC-KEY</code>. Same fields as /api/calculate (tc, hdl, tg...). Contact physiologypro.contact@gmail.com to get clinic key.</div></details></div>
</div>
</div>
</div>
</div>
<div class="ad-box"><div class="ad-label">ADVERTISEMENT</div><ins class="adsbygoogle" style="display:block" data-ad-client="{ADSENSE_CLIENT}" data-ad-slot="3456789012" data-ad-format="auto" data-full-width-responsive="true"></ins><script>(adsbygoogle=window.adsbygoogle||[]).push({});</script></div>
<div style="font-size:10px;color:#64748b;background:#f8fafc;border-radius:8px;padding:8px;margin-top:8px">⚕️ Educational only — not medical advice. Verify with lab & clinician. | <a href="/privacy">Privacy</a> | <a href="/terms">Terms</a> | <a href="/contact">Contact</a> | © Clinical & Research Variables Calculator — Dr. Sumaiya Mohammad</div>
<div style="text-align:center;margin-top:12px"><button type="button" onclick="window.print()" style="padding:8px 14px;border:none;background:#e2e8f0;border-radius:6px;font-weight:700">Print</button> <button type="button" onclick="location.reload()" style="padding:8px 14px;border:none;background:var(--b);color:#fff;border-radius:6px;font-weight:700">Reset</button></div>
</div><script>
function calc(){
let bp=document.getElementById('bp').value,hr=parseFloat(document.getElementById('hr').value),wt=parseFloat(document.getElementById('wt').value),ht=parseFloat(document.getElementById('ht').value),age=parseFloat(document.getElementById('age').value),cr=parseFloat(document.getElementById('cr').value),sex=document.getElementById('sex').value,sv=parseFloat(document.getElementById('sv').value)||70,na=parseFloat(document.getElementById('na').value),cl=parseFloat(document.getElementById('cl').value),hco3=parseFloat(document.getElementById('hco3').value),alb=parseFloat(document.getElementById('alb').value),ca=parseFloat(document.getElementById('ca').value),bun=parseFloat(document.getElementById('bun').value),glu=parseFloat(document.getElementById('glu').value),tc=parseFloat(document.getElementById('tc').value),hdl=parseFloat(document.getElementById('hdl').value),tg=parseFloat(document.getElementById('tg').value),mg=parseFloat(document.getElementById('mg').value);
let sbp=0,dbp=0;if(bp.includes('/')){let a=bp.split('/');sbp=parseFloat(a[0]);dbp=parseFloat(a[1]);}
if(sbp&&dbp){
let map=((sbp+2*dbp)/3).toFixed(1);document.getElementById('mapV').textContent=map+' mmHg';document.getElementById('mapB').textContent=map<70?'Low ⚠️ Hypo - <70':map<=100?'Normal ✅ 70-100':'High ⚠️ >100';
let pp=sbp-dbp;document.getElementById('ppV').textContent=pp+' mmHg';document.getElementById('ppB').textContent=pp<30?'Narrow ⚠️ <30':pp<=60?'Normal ✅ 40-60':'Wide ⚠️ >60';
if(hr&&sbp){let si=(hr/sbp).toFixed(2);document.getElementById('siV').textContent=si;document.getElementById('siB').textContent=si<0.7?'Normal ✅ <0.7':si<1?'Borderline ⚠️ 0.7-1':'SHOCK ⚠️ >1';}
}
if(hr){document.getElementById('coV').textContent=(hr*sv/1000).toFixed(2)+' l/min';}
if(wt&&ht){
let bsa=Math.sqrt((ht*wt)/3600).toFixed(2);document.getElementById('bsaV').textContent=bsa+' m²';
let bmi=(wt/((ht/100)*(ht/100))).toFixed(1);document.getElementById('bmiV').textContent=bmi;let bb=document.getElementById('bmiB');if(bmi<18.5)bb.textContent='Underweight';else if(bmi<25)bb.textContent='Normal ✅';else if(bmi<30)bb.textContent='Overweight ⚠️';else bb.textContent='Obese ❌';
let fluid=wt<=10?wt*4:wt<=20?40+(wt-10)*2:60+(wt-20)*1;document.getElementById('fluidV').textContent=fluid+' ml/hr';document.getElementById('fluidB').textContent=(fluid*24)+' ml/day';
let ibw=sex==='Male'?50+0.91*(ht-152.4):45.5+0.91*(ht-152.4);document.getElementById('ibwV').textContent=ibw.toFixed(1)+' kg';
}
if(cr&&age&&wt){let crcl=((140-age)*wt/(72*cr))*(sex==='Female'?0.85:1);document.getElementById('gfrV').textContent=crcl.toFixed(1)+' ml/min';let gb=document.getElementById('gfrB');if(crcl>=90)gb.textContent='G1 Normal ✅ >90';else if(crcl>=60)gb.textContent='G2 Mild ↓ 60-89';else if(crcl>=45)gb.textContent='G3a Mild-Mod ↓';else if(crcl>=30)gb.textContent='G3b Mod-Sev ⚠️';else if(crcl>=15)gb.textContent='G4 Severe ❌';else gb.textContent='G5 Failure ❌ <15';}
if(na&&cl&&hco3){let ag=na-(cl+hco3);document.getElementById('agV').textContent=ag+' mEq/l';document.getElementById('agB').textContent=ag>16?'High Gap ⚠️ >16':ag<8?'Low <8':'Normal ✅ 8-16';}
if(ca&&alb){document.getElementById('caV').textContent=(ca+0.8*(4-alb)).toFixed(2)+' mg/dl';}
if(mg&&alb){let albGL=alb*10;let cmg=mg+0.005*(40-albGL);document.getElementById('cmgV').textContent=cmg.toFixed(2)+' mg/dl';let cmb=document.getElementById('cmgB');cmb.textContent=cmg<1.7?'Low corrected <1.7':cmg<=2.2?'Normal corrected 1.7-2.2':'High corrected >2.2';}
if(na&&bun&&glu){document.getElementById('osmV').textContent=(2*na+glu/18+bun/2.8).toFixed(1)+' mOsm/kg';}
if(tc&&hdl){let nonhdl=tc-hdl;document.getElementById('nonhdlV').textContent=nonhdl.toFixed(1)+' mg/dl';let nb=document.getElementById('nonhdlB');nb.textContent=nonhdl<130?'Optimal ✅ <130':nonhdl<160?'Near Optimal 130-159':nonhdl<190?'Borderline High ⚠️ 160-189':nonhdl<220?'High ❌ 190-219':'Very High ❌ ≥220';let tchr=tc/hdl;document.getElementById('tchrV').textContent=tchr.toFixed(2);let tb=document.getElementById('tchrB');tb.textContent=tchr<3.5?'Ideal ✅ <3.5':tchr<=5?'Moderate ⚠️ 3.5-5':'High Risk ❌ >5';}
if(tc&&hdl&&tg){let vldl=tg/5;document.getElementById('vldlV').textContent=vldl.toFixed(1)+' mg/dl';let vb=document.getElementById('vldlB');vb.textContent=tg<150?'TG Normal ✅ <150':tg<200?'TG Borderline ⚠️ 150-199':tg<500?'TG High ⚠️ 200-499':'TG Very High ❌ ≥500';let lb=document.getElementById('ldlB');if(tg>400){document.getElementById('ldlV').textContent='Invalid TG>400';lb.textContent='Use direct LDL ⚠️ Friedewald invalid';}else{let ldl=tc-hdl-vldl;document.getElementById('ldlV').textContent=ldl.toFixed(1)+' mg/dl';lb.textContent=ldl<100?'Optimal ✅ <100':ldl<130?'Near Optimal 100-129':ldl<160?'Borderline High ⚠️ 130-159':ldl<190?'High ❌ 160-189':'Very High ❌ ≥190';}}
let t='';if(sbp&&dbp)t+=`BP ${sbp}/${dbp} → MAP ${document.getElementById('mapV').textContent}, PP ${document.getElementById('ppV').textContent}, SI ${document.getElementById('siV').textContent}<br>`;if(wt&&ht)t+=`BSA ${document.getElementById('bsaV').textContent} | BMI ${document.getElementById('bmiV').textContent} | Fluid ${document.getElementById('fluidV').textContent}<br>`;if(cr)t+=`Kidney: ${document.getElementById('gfrV').textContent} - ${document.getElementById('gfrB').textContent}<br>`;if(tc&&hdl)t+=`Lipid: LDL ${document.getElementById('ldlV').textContent} (${document.getElementById('ldlB').textContent}) | Non-HDL ${document.getElementById('nonhdlV').textContent} | TC/HDL ${document.getElementById('tchrV').textContent} (${document.getElementById('tchrB').textContent})<br>`;if(mg&&alb)t+=`Mg ${mg.toFixed(1)} → Corrected Mg ${document.getElementById('cmgV').textContent} (${document.getElementById('cmgB').textContent})<br>`;document.getElementById('interp').innerHTML=t||'Enter values...';
}
if('serviceWorker' in navigator){navigator.serviceWorker.register('/static/service-worker.js');}
</script></body></html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE.replace("{ADSENSE_CLIENT}", ADSENSE_CLIENT))

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'icon-192.svg', mimetype='image/svg+xml')

@app.route('/api/formulas')
def api_formulas():
    try:
        base = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(base, 'physiology.json'), encoding='utf-8') as f:
            return jsonify(json.load(f))
    except Exception as e:
        logging.exception('formulas load failed')
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/pro/calculate', methods=['POST'])
def api_pro():
    if request.headers.get('X-API-Key') != PRO_API_KEY:
        return jsonify({"status": "error", "message": "invalid PRO_API_KEY. Contact to buy clinic key."}), 401
    return api_calculate()

@app.route('/privacy')
def privacy():
    return render_template_string(f"<h2>{APP_NAME} - Privacy</h2><p>No login. Calculations run in browser. API does not store patient data. Ads by Google may use cookies. Contact: {CONTACT_EMAIL}</p><a href='/'>Back</a>")

@app.route('/terms')
def terms():
    return render_template_string(f"<h2>{APP_NAME} - Terms & Disclaimer</h2><p>Educational tool only, not medical advice. By {AUTHOR_NAME}. Verify all results clinically.</p><a href='/'>Back</a>")

@app.route('/contact')
def contact():
    return render_template_string(f"<h2>Contact - {AUTHOR_NAME}</h2><p>Email: {CONTACT_EMAIL}<br>PRO for Clinics / Institutions: bulk use, EMR integration, no ads — email to request clinic key.</p><a href='/'>Back</a>")

@app.route('/healthz')
def healthz():
    return jsonify({"status": "ok", "app": "Clinical & Research Variables Calculator"}), 200

@app.route('/api/calculate', methods=['POST'])
def api_calculate():
    data = request.get_json(silent=True) or {}
    # Lipid server-side support (Friedewald) + echo
    try:
        tc = float(data.get('tc')) if data.get('tc') not in (None, '') else None
        hdl = float(data.get('hdl')) if data.get('hdl') not in (None, '') else None
        tg = float(data.get('tg')) if data.get('tg') not in (None, '') else None
        out = dict(data)
        if tc is not None and hdl is not None:
            out['non_hdl'] = round(tc - hdl, 1)
            out['tc_hdl_ratio'] = round(tc / hdl, 2) if hdl else None
            if tg is not None:
                out['vldl'] = round(tg / 5, 1)
                out['ldl'] = None if tg > 400 else round(tc - hdl - tg / 5, 1)
        return jsonify({"status": "ok", "data": out})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.errorhandler(404)
def not_found(e):
    return jsonify({"status": "error", "message": "not found"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"status": "error", "message": "internal error"}), 500

@app.after_request
def add_security_headers(resp):
    resp.headers['X-Content-Type-Options'] = 'nosniff'
    resp.headers['X-Frame-Options'] = 'SAMEORIGIN'
    resp.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    return resp

if __name__ == '__main__':
    # Local run + Render/Heroku/Railway compatible
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', '0') == '1'
    app.run(host='0.0.0.0', port=port, debug=debug)
