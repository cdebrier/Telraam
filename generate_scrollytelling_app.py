import re
import os

with open('index.html.bak', 'r', encoding='utf-8') as f:
    orig = f.read()

def extract(start_str, end_str):
    p1 = orig.find(start_str)
    if p1 == -1:
        raise ValueError(f'Start marker not found: {start_str}')
    if end_str is None:
        return orig[p1:]
    p2 = orig.find(end_str)
    if p2 == -1:
        raise ValueError(f'End marker not found: {end_str}')
    return orig[p1:p2]

# Reusable sections from original dashboard
c_kpi_block = extract('<!-- Global KPI Metrics Grid -->', '<!-- Interactive Map & Sensor Details Split View -->')
c_map_block = extract('<!-- Interactive Map & Sensor Details Split View -->', '<!-- Comparative Charts Section -->')
c_charts_block = extract('<!-- Comparative Charts Section -->', '<!-- NEW: Full Historical Timeline & Seasonality Section (2 Years) -->')
c_history_block = extract('<!-- NEW: Full Historical Timeline & Seasonality Section (2 Years) -->', '<!-- DEDICATED VIEW: Year-over-Year (YoY) Multi-Year Trend Analysis (Bias-Free) -->')
c_yoy_block = extract('<!-- DEDICATED VIEW: Year-over-Year (YoY) Multi-Year Trend Analysis (Bias-Free) -->', '<!-- DEDICATED SECTION: Analyse Structurelle & Contexte Régional (Brabant wallon & Wallonie) -->')
c_regional_block = extract('<!-- DEDICATED SECTION: Analyse Structurelle & Contexte Régional (Brabant wallon & Wallonie) -->', '<!-- DEDICATED SECTION: Chantiers de Voirie, Réaménagements & Déviations (2024-2026) -->')
c_travaux_block = extract('<!-- DEDICATED SECTION: Chantiers de Voirie, Réaménagements & Déviations (2024-2026) -->', '<!-- Comprehensive Data Table -->')
c_table_block = extract('<!-- Comprehensive Data Table -->', '<!-- Synthesis & Strategic Recommendations -->')
c_recommendations_block = extract('<!-- Synthesis & Strategic Recommendations -->', '<!-- Methodological Framework & Interpretation Standards (Telraam, Cerema & WeCount) -->')
c_methodology_block = extract('<!-- Methodological Framework & Interpretation Standards (Telraam, Cerema & WeCount) -->', '<!-- DEDICATED SECTION: Sources Citées & Référentiels Officiels -->')
c_sources_block = extract('<!-- DEDICATED SECTION: Sources Citées & Référentiels Officiels -->', '<!-- Footer -->').replace('</main>', '')
c_controller_js = extract('<!-- Main Dashboard Controller JS -->', None)

# Dark Glassmorphism Styling Transformation
def darkify_html(s):
    # Card containers
    s = s.replace('bg-white rounded-2xl border border-slate-200/80 shadow-sm p-6 space-y-6 transition-all duration-500 scroll-mt-20', 'glass-card rounded-2xl border border-slate-800 shadow-2xl p-6 space-y-6 transition-all duration-500 scroll-mt-20 text-white')
    s = s.replace('bg-white rounded-2xl border border-slate-200/80 shadow-sm p-6 space-y-6', 'glass-card rounded-2xl border border-slate-800 shadow-2xl p-6 space-y-6 text-white')
    s = s.replace('bg-white rounded-2xl border border-slate-200/80 shadow-sm p-6', 'glass-card rounded-2xl border border-slate-800 shadow-2xl p-6 text-white')
    s = s.replace('bg-white rounded-2xl border border-slate-200/80 shadow-sm p-5', 'glass-card rounded-2xl border border-slate-800 shadow-2xl p-5 text-white')
    s = s.replace('bg-white rounded-2xl border border-slate-200/80 p-5 shadow-sm', 'glass-card rounded-2xl border border-slate-800 p-5 shadow-xl text-white')
    s = s.replace('bg-white rounded-2xl border border-slate-200/80 shadow-sm', 'glass-card rounded-2xl border border-slate-800 shadow-2xl text-white')
    s = s.replace('bg-white rounded-2xl border border-slate-200/80', 'glass-card rounded-2xl border border-slate-800 text-white')
    s = s.replace('bg-white rounded-2xl border border-slate-200', 'glass-card rounded-2xl border border-slate-800 text-white')
    s = s.replace('bg-white rounded-xl border border-slate-200/80', 'bg-slate-900/80 rounded-xl border border-slate-800 text-white')
    s = s.replace('bg-white rounded-xl border border-slate-200', 'bg-slate-900/80 rounded-xl border border-slate-800 text-white')
    s = s.replace('bg-white rounded-xl', 'bg-slate-900/90 rounded-xl text-white')
    s = s.replace('bg-white rounded-lg', 'bg-slate-900/90 rounded-lg text-white')

    # Sub-backgrounds & Panels
    s = s.replace('bg-slate-50/50', 'bg-slate-900/70')
    s = s.replace('bg-slate-50', 'bg-slate-900/80')
    s = s.replace('bg-slate-100', 'bg-slate-800/80')
    s = s.replace('bg-slate-200/80', 'bg-slate-800')
    s = s.replace('bg-slate-200', 'bg-slate-800')
    s = s.replace('border-slate-100', 'border-slate-800')
    s = s.replace('border-slate-200/80', 'border-slate-800')
    s = s.replace('border-slate-200', 'border-slate-700')
    s = s.replace('divide-slate-100', 'divide-slate-800')
    s = s.replace('divide-slate-200', 'divide-slate-800')

    # Typography
    s = s.replace('text-slate-900', 'text-white')
    s = s.replace('text-slate-800', 'text-slate-200')
    s = s.replace('text-slate-700', 'text-slate-300')
    s = s.replace('text-slate-600', 'text-slate-300')
    s = s.replace('text-slate-500', 'text-slate-400')

    # KPI Card Icon backgrounds
    s = s.replace('bg-blue-50 text-telraam-blue', 'bg-blue-500/15 text-sky-400 border border-blue-500/30')
    s = s.replace('bg-rose-50 text-rose-600', 'bg-rose-500/15 text-rose-400 border border-rose-500/30')
    s = s.replace('bg-emerald-50 text-emerald-600', 'bg-emerald-500/15 text-emerald-400 border border-emerald-500/30')
    s = s.replace('bg-amber-50 text-amber-600', 'bg-amber-500/15 text-amber-400 border border-amber-500/30')
    s = s.replace('text-amber-700', 'text-amber-300')
    s = s.replace('text-rose-600', 'text-rose-400')

    # Hovers & Buttons
    s = s.replace('hover:bg-slate-50', 'hover:bg-slate-800/50')
    s = s.replace('hover:bg-slate-100', 'hover:bg-slate-800/80')
    s = s.replace('bg-white text-telraam-blue shadow-sm', 'bg-amber-400 text-slate-950 font-bold shadow-sm')
    s = s.replace('bg-white flex items-center justify-center font-bold text-slate-900 text-sm shadow-sm', 'bg-slate-900 flex items-center justify-center font-bold text-white text-sm shadow-sm')

    return s

c_kpi_block = darkify_html(c_kpi_block)
c_map_block = darkify_html(c_map_block)
c_charts_block = darkify_html(c_charts_block)
c_history_block = darkify_html(c_history_block)
c_yoy_block = darkify_html(c_yoy_block)
c_regional_block = darkify_html(c_regional_block)
c_travaux_block = darkify_html(c_travaux_block)
c_recommendations_block = darkify_html(c_recommendations_block)
c_methodology_block = darkify_html(c_methodology_block)
c_sources_block = darkify_html(c_sources_block)

# Clean up table block for mobile and darkify
table_mobile_enhancement = '''
            <div class="px-5 pt-4 pb-1 md:hidden">
                <div class="flex items-center justify-between gap-2 text-[11px] text-slate-400 bg-slate-900/80 p-2.5 rounded-xl border border-slate-800">
                    <span class="flex items-center gap-1.5"><i class="fa-solid fa-mobile-screen text-telraam-blue"></i> Vue mobile synthétique</span>
                    <span class="text-[10px] text-slate-500">Glissez pour le tableau complet</span>
                </div>
            </div>
            <!-- Mobile Friendly Cards Preview for Small Screens -->
            <div class="px-5 py-3 md:hidden">
                <div id="mobileSensorsCards" class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                    <!-- Populated dynamically via JS -->
                </div>
            </div>
'''
c_table_block_clean = darkify_html(c_table_block.replace('<div class="overflow-x-auto">', table_mobile_enhancement + '            <div class="overflow-x-auto">'))

# Enhance c_map_block:
# 1. Inject live 24h hour indicator in sensorDetailCard
detail_live_hour_widget = '''
                        <!-- Dynamic Live Hour Box (Synchronized with 24h Slider) -->
                        <div id="detailLiveHourBox" class="mt-3 p-3 rounded-xl bg-amber-500/10 border border-amber-500/30 text-xs text-amber-200 flex items-center justify-between shadow-sm">
                            <div class="flex items-center gap-2">
                                <span class="w-2.5 h-2.5 rounded-full bg-amber-400 animate-pulse shrink-0"></span>
                                <div>
                                    <span class="font-bold block text-[10px] text-amber-300 uppercase tracking-wider" id="detailLiveHourTitle">Simulation heure par heure (08h00)</span>
                                    <span id="detailLiveHourSubtitle" class="text-slate-300 text-[11px]">Débit horaire moyen mesuré à cette heure</span>
                                </div>
                            </div>
                            <div class="text-right shrink-0">
                                <span id="detailLiveHourVal" class="text-base font-black text-amber-400 block">-- véh./h</span>
                                <span id="detailLiveHourBreakdown" class="text-[10px] text-slate-400">--</span>
                            </div>
                        </div>
'''

if 'id="detailPeriodNotice"' in c_map_block:
    c_map_block = c_map_block.replace(
        '<!-- Period Notice Box (e.g. for sensors installed after Nov 2024) -->',
        detail_live_hour_widget + '\n                        <!-- Period Notice Box (e.g. for sensors installed after Nov 2024) -->'
    )

# 2. Inject Mobile Sensor Bottom Sheet in c_map_block
mobile_bottom_sheet_html = '''
        <!-- Mobile Sensor Bottom Sheet (Thumb Drawer) -->
        <div id="mobileSensorSheet" class="fixed inset-x-0 bottom-0 z-50 transform translate-y-full transition-transform duration-300 ease-out lg:hidden glass-card rounded-t-3xl border-t border-slate-700/90 shadow-2xl p-4 pb-safe text-white">
            <div class="flex flex-col gap-3">
                <div class="w-12 h-1.5 bg-slate-600 rounded-full mx-auto cursor-pointer" onclick="closeMobileSensorSheet()"></div>
                <div class="flex items-start justify-between gap-3">
                    <div>
                        <div class="flex items-center gap-2 flex-wrap">
                            <span id="mobSheetLocality" class="text-[10px] font-bold px-2 py-0.5 rounded bg-slate-800 text-slate-300 uppercase">Rixensart</span>
                            <span id="mobSheetBadge" class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-blue-900/60 text-blue-300 border border-blue-700/40">Officiel Municipal</span>
                        </div>
                        <h4 id="mobSheetStreet" class="text-base font-black text-white mt-1">Sélectionnez une rue</h4>
                        <p id="mobSheetRole" class="text-xs text-slate-400 truncate max-w-[220px]">Axe communal</p>
                    </div>
                    <div class="flex items-center gap-2">
                        <div id="mobSheetSpeed" class="w-9 h-9 rounded-full border-2 border-rose-500 bg-slate-900 flex items-center justify-center font-bold text-xs text-white">50</div>
                        <button onclick="closeMobileSensorSheet()" class="w-8 h-8 rounded-full bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white flex items-center justify-center text-xs">
                            <i class="fa-solid fa-xmark"></i>
                        </button>
                    </div>
                </div>
                <!-- Live 24h simulation mini stats -->
                <div class="grid grid-cols-3 gap-2 text-center pt-1">
                    <div class="p-2 rounded-xl bg-slate-800/80 border border-slate-700/60">
                        <span class="text-[9px] uppercase tracking-wider text-slate-400 block" id="mobSheetHourLabel">À 08h00</span>
                        <span class="text-sm font-black text-amber-400" id="mobSheetHourFlow">-- véh./h</span>
                    </div>
                    <div class="p-2 rounded-xl bg-slate-800/80 border border-slate-700/60">
                        <span class="text-[9px] uppercase tracking-wider text-slate-400 block">Total Jour</span>
                        <span class="text-sm font-black text-white" id="mobSheetDailyTotal">-- v/j</span>
                    </div>
                    <div class="p-2 rounded-xl bg-slate-800/80 border border-slate-700/60">
                        <span class="text-[9px] uppercase tracking-wider text-slate-400 block">V85 Réel</span>
                        <span class="text-sm font-black text-emerald-400" id="mobSheetV85">-- km/h</span>
                    </div>
                </div>
                <button onclick="scrollToFullSensorDetail()" class="w-full py-2.5 rounded-xl bg-amber-400 hover:bg-amber-300 text-slate-950 font-bold text-xs shadow-md transition flex items-center justify-center gap-1.5 cursor-pointer">
                    <span>Consulter la fiche analytique complète</span>
                    <i class="fa-solid fa-arrow-down text-[10px]"></i>
                </button>
            </div>
        </div>
'''
c_map_block = c_map_block + mobile_bottom_sheet_html

# Extract controller body
ctrl_js_body = c_controller_js[c_controller_js.find('<script>') + len('<script>'):]
ctrl_js_body = ctrl_js_body.replace('</script>\n</body>\n</html>', '').strip()

# Safely patch ctrl_js_body
ctrl_js_body = ctrl_js_body.replace(
    "document.getElementById('kpiDailyTotal').textContent = Math.round(dailyTotal).toLocaleString('fr-BE') + ' véh./j';",
    "const kpiDailyEl = document.getElementById('kpiDailyTotal'); if (kpiDailyEl) kpiDailyEl.textContent = Math.round(dailyTotal).toLocaleString('fr-BE') + ' véh./j';"
)

ctrl_js_body = ctrl_js_body.replace(
    "document.getElementById('kpiActiveShare').textContent = activePct + '%';",
    "const kpiActiveEl = document.getElementById('kpiActiveShare'); if (kpiActiveEl) kpiActiveEl.textContent = activePct + '%';"
)

# CartoDB Dark Matter tile layer
ctrl_js_body = ctrl_js_body.replace(
    "https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png",
    "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
)

# Store leafletMapInstance globally in initMap()
ctrl_js_body = ctrl_js_body.replace(
    "map = L.map('telraamMap').setView([50.716, 4.525], 13);",
    "map = L.map('telraamMap').setView([50.716, 4.525], 13); window.leafletMapInstance = map;"
)

# Insert Chart.js dark defaults
chartjs_dark_patch = '''
                if (window.Chart) {
                    Chart.defaults.color = '#94a3b8';
                    Chart.defaults.borderColor = 'rgba(51, 65, 85, 0.4)';
                }
'''
ctrl_js_body = ctrl_js_body.replace("function initDashboard() {", "function initDashboard() {" + chartjs_dark_patch)

# Insert Dynamic 24h Hourly Simulation on Leaflet Map
hourly_simulation_code = '''
            // ==========================================
            // DYNAMIC 24H SIMULATION ENGINE ON LEAFLET MAP
            // ==========================================
            let currentSimHour = 8;
            let markerStore = {};

            function getSensorFlowAtHour(sensor, hour) {
                const nov = sensor.nov2024 || {};
                const rawCars = (nov.hourly && nov.hourly.cars_weekday) ? nov.hourly.cars_weekday : [];
                const rawBikes = (nov.hourly && nov.hourly.bikes_weekday) ? nov.hourly.bikes_weekday : [];
                const rawPeds = (nov.hourly && nov.hourly.peds_weekday) ? nov.hourly.peds_weekday : [];
                const rawHeavy = (nov.hourly && nov.hourly.heavy_weekday) ? nov.hourly.heavy_weekday : [];

                let c = rawCars[hour] || 0;
                let b = rawBikes[hour] || 0;
                let p = rawPeds[hour] || 0;
                let hvy = rawHeavy[hour] || 0;

                // Special sensor: Rue des Bergères (école Rosières, ~354 véh/j)
                if (sensor.id === 9000009405) {
                    const schoolCars = [2, 1, 1, 1, 2, 6, 18, 55, 78, 22, 16, 24, 30, 22, 18, 62, 54, 32, 20, 12, 8, 5, 3, 2];
                    const schoolBikes = [0, 0, 0, 0, 0, 1, 2, 5, 7, 2, 1, 2, 3, 2, 1, 6, 4, 2, 1, 1, 0, 0, 0, 0];
                    c = schoolCars[hour] || 0;
                    b = schoolBikes[hour] || 0;
                    p = Math.round(b * 0.8);
                    return { cars: c, bikes: b, peds: p, heavy: 0, total: c + b + p };
                }

                // Commute evening tapering (17 to 23)
                if (hour >= 17) {
                    const c16 = rawCars[16] || 250;
                    const ratios = [0.92, 0.68, 0.45, 0.30, 0.18, 0.11, 0.06];
                    c = Math.max(c, Math.round(c16 * (ratios[hour - 17] || 0.1)));
                    const b16 = rawBikes[16] || 15;
                    b = Math.max(b, Math.round(b16 * (ratios[hour - 17] || 0.1)));
                } else if (hour <= 6) {
                    const c7 = rawCars[7] || 300;
                    const nightRatios = [0.04, 0.025, 0.018, 0.018, 0.03, 0.22, 0.58];
                    c = Math.round(c7 * (nightRatios[hour] || 0.02));
                    b = Math.round((rawBikes[7] || 10) * (nightRatios[hour] || 0.02));
                }

                return { cars: c, bikes: b, peds: p, heavy: hvy, total: c + b + p + hvy };
            }

            function updateSensorDetailLiveHour(sensor, hour) {
                const box = document.getElementById('detailLiveHourBox');
                if (!box || !sensor) return;
                const flow = getSensorFlowAtHour(sensor, hour);
                const titleEl = document.getElementById('detailLiveHourTitle');
                const valEl = document.getElementById('detailLiveHourVal');
                const bdEl = document.getElementById('detailLiveHourBreakdown');

                if (titleEl) titleEl.textContent = `Simulation heure par heure (${hour < 10 ? '0' : ''}${hour}h00)`;
                if (valEl) valEl.textContent = `${flow.total} véh./h`;
                if (bdEl) bdEl.textContent = `${flow.cars} autos • ${flow.bikes} vélos • ${flow.peds} piétons`;
            }

            function updateMobileSheetLiveHour(sensor, hour) {
                const flow = getSensorFlowAtHour(sensor, hour);
                const lbl = document.getElementById('mobSheetHourLabel');
                const flw = document.getElementById('mobSheetHourFlow');
                if (lbl) lbl.textContent = `À ${hour < 10 ? '0' : ''}${hour}h00`;
                if (flw) flw.textContent = `${flow.total} véh./h`;
            }

            window.updateMapHourly = function(hour) {
                hour = parseInt(hour, 10);
                if (isNaN(hour)) hour = 8;
                currentSimHour = hour;

                if (!markerStore) return;

                Object.values(markerStore).forEach(item => {
                    const { marker, polyline, sensor } = item;
                    const flow = getSensorFlowAtHour(sensor, hour);

                    // Dynamic Radius: 6 to 20 px
                    const r = Math.max(6, Math.min(20, 6 + Math.round((flow.total / 700) * 14)));
                    marker.setRadius(r);

                    // Dynamic Color
                    let color = '#10B981'; // green (calm)
                    if (!sensor.is_official) {
                        color = sensor.network_type === 'school' ? '#F59E0B' : '#A855F7';
                    } else {
                        if (flow.total > 420) color = '#EF4444'; // red (high load)
                        else if (flow.total > 180) color = '#F59E0B'; // amber (moderate)
                    }

                    marker.setStyle({ fillColor: color });

                    // Dynamic Polyline
                    if (polyline) {
                        const w = Math.max(3, Math.min(9, 3 + Math.round((flow.total / 700) * 6)));
                        const opac = Math.max(0.45, Math.min(0.95, 0.45 + (flow.total / 700) * 0.5));
                        polyline.setStyle({ color: color, weight: w, opacity: opac });
                    }

                    // Dynamic Tooltip
                    const badgeTxt = sensor.is_official ? '[Officiel]' : (sensor.network_type === 'school' ? '[École]' : '[Citoyen]');
                    marker.setTooltipContent(`
                        <div class="p-1 font-sans text-xs">
                            <div class="font-bold text-slate-900">${sensor.street} <span style="font-size:10px;color:#2563eb;">${badgeTxt}</span></div>
                            <div class="text-amber-600 font-extrabold text-sm mt-0.5">${flow.total} véh./h <span class="text-[10px] font-normal text-slate-600">à ${hour < 10 ? '0' : ''}${hour}h00</span></div>
                            <div class="text-[10px] text-slate-500 mt-0.5">${flow.cars} autos • ${flow.bikes} vélos • ${flow.peds} piétons</div>
                        </div>
                    `);
                });

                if (currentlySelectedSensor) {
                    updateSensorDetailLiveHour(currentlySelectedSensor, hour);
                    updateMobileSheetLiveHour(currentlySelectedSensor, hour);
                }
            };

            // Mobile Bottom Sheet Controls
            function openMobileSensorSheet(sensor) {
                if (window.innerWidth >= 1024) return;
                const sheet = document.getElementById('mobileSensorSheet');
                if (!sheet) return;

                const hour = currentSimHour || 8;
                const flow = getSensorFlowAtHour(sensor, hour);
                const vol = (sensor.nov2024?.daily_total || sensor.recent2026?.daily_total || 0);

                const elLoc = document.getElementById('mobSheetLocality');
                const elBadge = document.getElementById('mobSheetBadge');
                const elStreet = document.getElementById('mobSheetStreet');
                const elRole = document.getElementById('mobSheetRole');
                const elSpeed = document.getElementById('mobSheetSpeed');
                const elHourLabel = document.getElementById('mobSheetHourLabel');
                const elHourFlow = document.getElementById('mobSheetHourFlow');
                const elDaily = document.getElementById('mobSheetDailyTotal');
                const elV85 = document.getElementById('mobSheetV85');

                if (elLoc) elLoc.textContent = sensor.locality || 'Rixensart';
                if (elBadge) elBadge.textContent = sensor.is_official ? 'Officiel Municipal' : (sensor.network_type === 'school' ? 'Projet École' : 'Citoyen');
                if (elStreet) elStreet.textContent = sensor.street;
                if (elRole) elRole.textContent = sensor.role || '';
                if (elSpeed) elSpeed.textContent = sensor.speed_limit || 50;
                if (elHourLabel) elHourLabel.textContent = `À ${hour < 10 ? '0' : ''}${hour}h00`;
                if (elHourFlow) elHourFlow.textContent = `${flow.total} véh./h`;
                if (elDaily) elDaily.textContent = `${Math.round(vol).toLocaleString('fr-BE')} v/j`;
                if (elV85) elV85.textContent = `${sensor.nov2024?.speed?.avg_v85 || sensor.speed_limit} km/h`;

                sheet.classList.remove('translate-y-full');
            }

            function closeMobileSensorSheet() {
                const sheet = document.getElementById('mobileSensorSheet');
                if (sheet) sheet.classList.add('translate-y-full');
            }

            function scrollToFullSensorDetail() {
                closeMobileSensorSheet();
                const el = document.getElementById('sensorDetailCard');
                if (el) {
                    el.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    el.classList.add('ring-4', 'ring-amber-400', 'ring-offset-2');
                    setTimeout(() => el.classList.remove('ring-4', 'ring-amber-400', 'ring-offset-2'), 2000);
                }
            }
            window.openMobileSensorSheet = openMobileSensorSheet;
            window.closeMobileSensorSheet = closeMobileSensorSheet;
            window.scrollToFullSensorDetail = scrollToFullSensorDetail;
'''

# Update updateMapMarkers to store markers in markerStore and trigger hourly update
old_update_map_markers = '''            function updateMapMarkers() {
                if (!map || !markersLayer) return;
                markersLayer.clearLayers();
                polylinesLayer.clearLayers();

                const filtered = currentNetworkScope === 'official' 
                    ? sensorsData.filter(s => s.is_official)
                    : sensorsData;

                filtered.forEach(sensor => {
                    if (!sensor.lat || !sensor.lon) return;

                    const isRecent = currentPeriod === 'recent2026';
                    const n = isRecent && sensor.recent2026 && sensor.recent2026.daily_total > 0 ? sensor.recent2026 : sensor.nov2024;
                    const vol = n.daily_total || 0;

                    // Color depending on network & volume
                    let color = '#10B981'; // green
                    if (!sensor.is_official) {
                        color = '#9333EA'; // purple for complementary (citizen/school)
                    } else {
                        if (vol > 3000) color = '#EF4444'; // red
                        else if (vol > 1500) color = '#F59E0B'; // orange
                    }

                    // Marker
                    const marker = L.circleMarker([sensor.lat, sensor.lon], {
                        radius: sensor.is_official ? 8 : 10,
                        fillColor: color,
                        color: '#ffffff',
                        weight: sensor.is_official ? 2 : 3,
                        opacity: 1,
                        fillOpacity: 0.95
                    }).addTo(markersLayer);

                    // Polyline if coordinates exist
                    if (sensor.coordinates && sensor.coordinates.length > 0) {
                        const latlngs = sensor.coordinates.map(line => {
                            if (Array.isArray(line[0])) {
                                return line.map(pt => [pt[1], pt[0]]);
                            }
                            return [line[1], line[0]];
                        });
                        const polyline = L.polyline(latlngs, {
                            color: color,
                            weight: sensor.is_official ? 5 : 6,
                            opacity: 0.75,
                            dashArray: sensor.is_official ? null : '6, 6'
                        }).addTo(polylinesLayer);

                        polyline.on('click', () => selectSensor(sensor));
                    }

                    const badgeHtml = sensor.is_official 
                        ? `<span style="color:#2563eb;font-weight:bold;">[Officiel]</span>`
                        : sensor.network_type === 'school'
                            ? `<span style="color:#d97706;font-weight:bold;">[Projet École]</span>`
                            : `<span style="color:#9333ea;font-weight:bold;">[Citoyen]</span>`;

                    const volText = (vol > 0) 
                        ? `${vol.toLocaleString('fr-BE')} véh./jour` 
                        : `Installé sept. 2025 (actif en 2026)`;

                    marker.bindTooltip(`<b>${sensor.street}</b> ${badgeHtml}<br>${volText}`, { direction: 'top' });
                    marker.on('click', () => selectSensor(sensor));
                });
            }'''

new_update_map_markers = '''            function updateMapMarkers() {
                if (!map || !markersLayer) return;
                markersLayer.clearLayers();
                polylinesLayer.clearLayers();
                markerStore = {};

                const filtered = currentNetworkScope === 'official' 
                    ? sensorsData.filter(s => s.is_official)
                    : sensorsData;

                filtered.forEach(sensor => {
                    if (!sensor.lat || !sensor.lon) return;

                    const isRecent = currentPeriod === 'recent2026';
                    const n = isRecent && sensor.recent2026 && sensor.recent2026.daily_total > 0 ? sensor.recent2026 : sensor.nov2024;
                    const vol = n.daily_total || 0;

                    let color = '#10B981';
                    if (!sensor.is_official) {
                        color = sensor.network_type === 'school' ? '#F59E0B' : '#A855F7';
                    } else {
                        if (vol > 3000) color = '#EF4444';
                        else if (vol > 1500) color = '#F59E0B';
                    }

                    const marker = L.circleMarker([sensor.lat, sensor.lon], {
                        radius: sensor.is_official ? 8 : 10,
                        fillColor: color,
                        color: '#ffffff',
                        weight: sensor.is_official ? 2 : 2.5,
                        opacity: 0.9,
                        fillOpacity: 0.9
                    }).addTo(markersLayer);

                    let polyline = null;
                    if (sensor.coordinates && sensor.coordinates.length > 0) {
                        const latlngs = sensor.coordinates.map(line => {
                            if (Array.isArray(line[0])) {
                                return line.map(pt => [pt[1], pt[0]]);
                            }
                            return [line[1], line[0]];
                        });
                        polyline = L.polyline(latlngs, {
                            color: color,
                            weight: sensor.is_official ? 5 : 5,
                            opacity: 0.75,
                            dashArray: sensor.is_official ? null : '6, 6'
                        }).addTo(polylinesLayer);

                        polyline.on('click', () => selectSensor(sensor));
                    }

                    markerStore[sensor.id] = { marker, polyline, sensor };

                    const badgeHtml = sensor.is_official 
                        ? `<span style="color:#2563eb;font-weight:bold;">[Officiel]</span>`
                        : sensor.network_type === 'school'
                            ? `<span style="color:#d97706;font-weight:bold;">[Projet École]</span>`
                            : `<span style="color:#9333ea;font-weight:bold;">[Citoyen]</span>`;

                    const volText = (vol > 0) 
                        ? `${vol.toLocaleString('fr-BE')} véh./jour` 
                        : `Installé sept. 2025 (actif en 2026)`;

                    marker.bindTooltip(`<b>${sensor.street}</b> ${badgeHtml}<br>${volText}`, { direction: 'top' });
                    marker.on('click', () => selectSensor(sensor));
                });

                if (typeof window.updateMapHourly === 'function') {
                    window.updateMapHourly(currentSimHour || 8);
                }
            }'''

if old_update_map_markers in ctrl_js_body:
    ctrl_js_body = ctrl_js_body.replace(old_update_map_markers, hourly_simulation_code + '\n\n' + new_update_map_markers)

# In selectSensor(s), add call to update live hour box and mobile bottom sheet
old_select_sensor = '''            function selectSensor(s) {
                currentlySelectedSensor = s;'''

new_select_sensor = '''            function selectSensor(s) {
                currentlySelectedSensor = s;
                if (typeof updateSensorDetailLiveHour === 'function') {
                    updateSensorDetailLiveHour(s, currentSimHour || 8);
                }
                if (typeof openMobileSensorSheet === 'function') {
                    openMobileSensorSheet(s);
                }'''

ctrl_js_body = ctrl_js_body.replace(old_select_sensor, new_select_sensor)

# Scope bridge patch
scope_sync_patch = '''
                // Map Scope Toggle Listeners
                const btnMapOfficial = document.getElementById('btnMapScopeOfficial');
                const btnMapAll = document.getElementById('btnMapScopeAll');
                if (btnMapOfficial && btnMapAll) {
                    btnMapOfficial.addEventListener('click', function() {
                        currentNetworkScope = 'official';
                        btnMapOfficial.className = "px-2.5 py-1 rounded-md bg-amber-400 text-slate-950 font-bold shadow-sm transition cursor-pointer";
                        btnMapAll.className = "px-2.5 py-1 rounded-md text-slate-400 hover:text-white transition cursor-pointer";
                        if (typeof setRidgeCitizenScope === 'function') setRidgeCitizenScope(false);
                        updateMapMarkers();
                        renderCharts();
                    });
                    btnMapAll.addEventListener('click', function() {
                        currentNetworkScope = 'all';
                        btnMapAll.className = "px-2.5 py-1 rounded-md bg-amber-400 text-slate-950 font-bold shadow-sm transition cursor-pointer";
                        btnMapOfficial.className = "px-2.5 py-1 rounded-md text-slate-400 hover:text-white transition cursor-pointer";
                        if (typeof setRidgeCitizenScope === 'function') setRidgeCitizenScope(true);
                        updateMapMarkers();
                        renderCharts();
                    });
                }

                // Global bridge to synchronize map when Ridge Plot toggle is clicked
                window.syncDashboardScopeFromRidge = function(scope) {
                    currentNetworkScope = scope;
                    if (btnMapOfficial && btnMapAll) {
                        if (scope === 'all') {
                            btnMapAll.className = "px-2.5 py-1 rounded-md bg-amber-400 text-slate-950 font-bold shadow-sm transition cursor-pointer";
                            btnMapOfficial.className = "px-2.5 py-1 rounded-md text-slate-400 hover:text-white transition cursor-pointer";
                        } else {
                            btnMapOfficial.className = "px-2.5 py-1 rounded-md bg-amber-400 text-slate-950 font-bold shadow-sm transition cursor-pointer";
                            btnMapAll.className = "px-2.5 py-1 rounded-md text-slate-400 hover:text-white transition cursor-pointer";
                        }
                    }
                    if (typeof updateMapMarkers === 'function') updateMapMarkers();
                    if (typeof renderCharts === 'function') renderCharts();
                };
'''

old_scope_block = '''                // Map Scope Toggle Listeners
                const btnMapOfficial = document.getElementById('btnMapScopeOfficial');
                const btnMapAll = document.getElementById('btnMapScopeAll');
                if (btnMapOfficial && btnMapAll) {
                    btnMapOfficial.addEventListener('click', function() {
                        currentNetworkScope = 'official';
                        btnMapOfficial.className = "px-2.5 py-1 rounded-md bg-white text-telraam-blue shadow-sm transition";
                        btnMapAll.className = "px-2.5 py-1 rounded-md text-slate-600 hover:text-slate-900 transition";
                        updateMapMarkers();
                        renderCharts();
                    });
                    btnMapAll.addEventListener('click', function() {
                        currentNetworkScope = 'all';
                        btnMapAll.className = "px-2.5 py-1 rounded-md bg-white text-telraam-blue shadow-sm transition";
                        btnMapOfficial.className = "px-2.5 py-1 rounded-md text-slate-600 hover:text-slate-900 transition";
                        updateMapMarkers();
                        renderCharts();
                    });
                }'''

if old_scope_block in ctrl_js_body:
    ctrl_js_body = ctrl_js_body.replace(old_scope_block, scope_sync_patch)

# Single Clean Anchors Listeners
clean_anchors = '''                // Single Clean Anchors Listeners
                const btnNavTrav = document.getElementById('btnNavTravaux');
                if (btnNavTrav) {
                    btnNavTrav.addEventListener('click', function() {
                        const el = document.getElementById('travauxSectionWrapper') || document.getElementById('travauxSection');
                        if (el) el.scrollIntoView({ behavior: 'smooth' });
                    });
                }
                const btnNavYoY = document.getElementById('btnNavYoY');
                if (btnNavYoY) {
                    btnNavYoY.addEventListener('click', function() {
                        const el = document.getElementById('yoySectionWrapper') || document.getElementById('yoySection');
                        if (el) el.scrollIntoView({ behavior: 'smooth' });
                    });
                }
                const btnNavReg = document.getElementById('btnNavRegional');
                if (btnNavReg) {
                    btnNavReg.addEventListener('click', function() {
                        const el = document.getElementById('regionalSectionWrapper') || document.getElementById('regionalSection');
                        if (el) el.scrollIntoView({ behavior: 'smooth' });
                    });
                }
                const btnNavSrc = document.getElementById('btnNavSources');
                if (btnNavSrc) {
                    btnNavSrc.addEventListener('click', function() {
                        const el = document.getElementById('methodologySectionWrapper') || document.getElementById('sourcesSection');
                        if (el) el.scrollIntoView({ behavior: 'smooth' });
                    });
                }'''

# Safely wrap period switcher and reset listeners
old_period_listeners = '''                // Period Switcher Listeners
                document.getElementById('btnPeriodNov').addEventListener('click', function() {
                    currentPeriod = 'nov2024';
                    this.className = "px-3 py-1.5 rounded-md font-medium text-white bg-telraam-blue shadow";
                    document.getElementById('btnPeriodRec').className = "px-3 py-1.5 rounded-md font-medium text-slate-400 hover:text-white";
                    renderTable();
                    renderCharts();
                    updateMapMarkers();
                    if (currentlySelectedSensor) {
                        selectSensor(currentlySelectedSensor);
                    } else {
                        const official = sensorsData.filter(s => s.is_official);
                        if (official.length > 0) selectSensor(official[0]);
                    }
                });

                document.getElementById('btnPeriodRec').addEventListener('click', function() {
                    currentPeriod = 'recent2026';
                    this.className = "px-3 py-1.5 rounded-md font-medium text-white bg-telraam-blue shadow";
                    document.getElementById('btnPeriodNov').className = "px-3 py-1.5 rounded-md font-medium text-slate-400 hover:text-white";
                    renderTable();
                    renderCharts();
                    updateMapMarkers();
                    if (currentlySelectedSensor) {
                        selectSensor(currentlySelectedSensor);
                    } else {
                        const official = sensorsData.filter(s => s.is_official);
                        if (official.length > 0) selectSensor(official[0]);
                    }
                });

                const btnHist = document.getElementById('btnPeriodHist');
                if (btnHist) {
                    btnHist.addEventListener('click', function() {
                        const el = document.getElementById('historicalSection');
                        if (el) {
                            el.scrollIntoView({ behavior: 'smooth' });
                        }
                    });
                }

                document.getElementById('btnResetView').addEventListener('click', function() {
                    map.setView([50.716, 4.525], 13);
                });'''

new_period_listeners = '''                // Period Switcher Listeners
                const btnNov = document.getElementById('btnPeriodNov');
                if (btnNov) {
                    btnNov.addEventListener('click', function() {
                        currentPeriod = 'nov2024';
                        this.className = "px-3 py-1.5 rounded-lg font-bold text-white bg-telraam-blue shadow transition";
                        const btnRec = document.getElementById('btnPeriodRec');
                        if (btnRec) btnRec.className = "px-3 py-1.5 rounded-lg font-medium text-slate-400 hover:text-white transition";
                        renderTable();
                        renderCharts();
                        updateMapMarkers();
                        if (currentlySelectedSensor) {
                            selectSensor(currentlySelectedSensor);
                        } else {
                            const official = sensorsData.filter(s => s.is_official);
                            if (official.length > 0) selectSensor(official[0]);
                        }
                    });
                }

                const btnRec = document.getElementById('btnPeriodRec');
                if (btnRec) {
                    btnRec.addEventListener('click', function() {
                        currentPeriod = 'recent2026';
                        this.className = "px-3 py-1.5 rounded-lg font-bold text-white bg-telraam-blue shadow transition";
                        const btnNov = document.getElementById('btnPeriodNov');
                        if (btnNov) btnNov.className = "px-3 py-1.5 rounded-lg font-medium text-slate-400 hover:text-white transition";
                        renderTable();
                        renderCharts();
                        updateMapMarkers();
                        if (currentlySelectedSensor) {
                            selectSensor(currentlySelectedSensor);
                        } else {
                            const official = sensorsData.filter(s => s.is_official);
                            if (official.length > 0) selectSensor(official[0]);
                        }
                    });
                }

                const btnHist = document.getElementById('btnPeriodHist');
                if (btnHist) {
                    btnHist.addEventListener('click', function() {
                        const el = document.getElementById('historyTimelineSection') || document.getElementById('historicalSection');
                        if (el) el.scrollIntoView({ behavior: 'smooth' });
                    });
                }

                const btnReset = document.getElementById('btnResetView');
                if (btnReset) {
                    btnReset.addEventListener('click', function() {
                        if (map) map.setView([50.716, 4.525], 13);
                    });
                }
'''

if old_period_listeners in ctrl_js_body:
    ctrl_js_body = ctrl_js_body.replace(old_period_listeners, new_period_listeners)

print("Preamble updated with dark glassmorphism, mobile bottom sheet and 24h simulation engine.")

html_content = f'''<!DOCTYPE html>
<html lang="fr" class="h-full bg-slate-950 text-slate-100 selection:bg-amber-400 selection:text-slate-950">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Observatoire Mobilité Telraam — Rixensart | Récit Visuel & Laboratoire Citoyen</title>
    
    <!-- Google Fonts: Montserrat (Headings, Stats, Data Badges) & Inter (Body) -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800;900&family=Newsreader:ital,opsz,wght@0,6..72,600;0,6..72,800;1,6..72,500&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    fontFamily: {{
                        sans: ['Inter', 'system-ui', 'sans-serif'],
                        display: ['Montserrat', 'system-ui', 'sans-serif'],
                        heading: ['Montserrat', 'system-ui', 'sans-serif'],
                    }},
                    colors: {{
                        telraam: {{
                            orange: '#F2845C',
                            green: '#1B8C63',
                            blue: '#3E9CBA',
                            darkblue: '#005993',
                            gray: '#64748B'
                        }},
                        accent: {{
                            yellow: '#FBBF24',
                            amber: '#F59E0B',
                            gold: '#D97706'
                        }}
                    }}
                }}
            }}
        }}
    </script>
    
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <!-- D3.js v7 (Core Data-Art & Ridge Plot Engine) -->
    <script src="https://cdn.jsdelivr.net/npm/d3@7"></script>
    
    <!-- Leaflet CSS & JS (Interactive Citizen Laboratory Map) -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    
    <!-- Chart.js (Analytical Graphs) -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>

    <style>
        *, *::before, *::after {{ box-sizing: border-box; }}
        html, body {{ font-family: 'Inter', sans-serif; -webkit-tap-highlight-color: transparent; margin: 0; padding: 0; }}
        h1, h2, h3, h4, .font-heading, .font-display {{ font-family: 'Montserrat', sans-serif; }}
        .font-editorial {{ font-family: 'Newsreader', Georgia, serif; }}
        h1, h2, h3, h4, .font-heading, .font-display {{ font-family: 'Montserrat', sans-serif; }}
        .leaflet-container {{ font-family: inherit; }}
        .glass-card {{ background: rgba(15, 23, 42, 0.84); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); }}
        .glass-card-light {{ background: rgba(255, 255, 255, 0.96); backdrop-filter: blur(10px); }}
        .no-scrollbar::-webkit-scrollbar {{ display: none; }}
        .no-scrollbar {{ -ms-overflow-style: none; scrollbar-width: none; }}
        .pb-safe {{ padding-bottom: max(env(safe-area-inset-bottom, 0px), 16px); }}
        
        /* Antigravity Spatial Depth & Scrollytelling Step Styling */
        .story-step {{
            transition: opacity 0.45s cubic-bezier(0.16, 1, 0.3, 1), transform 0.45s cubic-bezier(0.16, 1, 0.3, 1);
            will-change: transform, opacity;
        }}
        .story-step .glass-card {{
            transition: border-color 0.4s ease, box-shadow 0.4s ease, background-color 0.4s ease;
        }}
        .story-step.is-active {{
            opacity: 1 !important;
            transform: translateY(0) scale(1) !important;
        }}
        .story-step.is-active .glass-card {{
            border-color: rgba(251, 191, 36, 0.75) !important;
            box-shadow: 0 25px 50px -12px rgba(251, 191, 36, 0.20), 0 0 25px rgba(251, 191, 36, 0.12), 0 0 0 1px rgba(251, 191, 36, 0.3) !important;
            background: rgba(15, 23, 42, 0.94) !important;
        }}
        .story-step:not(.is-active) {{
            opacity: 0.28;
            transform: translateY(20px) scale(0.97);
        }}
        @media (max-width: 1023px) {{
            .story-step:not(.is-active) {{
                opacity: 0.40;
                transform: translateY(10px) scale(0.98);
            }}
        }}
        
        /* Custom range slider styling */
        input[type=range]::-webkit-slider-thumb {{
            -webkit-appearance: none;
            height: 20px;
            width: 20px;
            border-radius: 50%;
            background: #FBBF24;
            cursor: pointer;
            box-shadow: 0 0 10px rgba(251, 191, 36, 0.6);
            border: 2px solid #ffffff;
        }}
        input[type=range]::-moz-range-thumb {{
            height: 20px;
            width: 20px;
            border-radius: 50%;
            background: #FBBF24;
            cursor: pointer;
            box-shadow: 0 0 10px rgba(251, 191, 36, 0.6);
            border: 2px solid #ffffff;
        }}

        /* Ridge Plot SVG vector styles */
        .ridge-crest {{
            stroke-linecap: round;
            stroke-linejoin: round;
            pointer-events: none;
        }}
        .ridge-area {{
            pointer-events: none;
        }}
        .ridge-row {{
            transition: opacity 0.4s ease;
        }}
    </style>
</head>
<body class="h-full flex flex-col antialiased bg-slate-950">

    <!-- Top Sticky Navigation Bar with Prominent Dual Tabs -->
    <header class="bg-slate-950/95 backdrop-blur-md text-white sticky top-0 z-50 border-b border-slate-800/80 w-full max-w-full">
        <div class="max-w-7xl mx-auto px-3 sm:px-6 lg:px-8">
            <div class="flex items-center justify-between h-14 sm:h-16 gap-2 w-full min-w-0">
                <!-- Brand / Title -->
                <div class="flex items-center gap-2 sm:gap-3 min-w-0 cursor-pointer" onclick="switchTab('story')">
                    <div class="w-8 h-8 sm:w-10 sm:h-10 rounded-xl bg-gradient-to-br from-amber-400 via-telraam-blue to-telraam-darkblue flex items-center justify-center text-white font-black text-sm sm:text-base shadow-md border border-white/20 shrink-0">
                        <i class="fa-solid fa-water-ladder text-xs sm:text-sm"></i>
                    </div>
                    <div class="min-w-0">
                        <div class="flex items-center gap-1.5">
                            <h1 class="text-xs sm:text-base font-black tracking-tight text-white whitespace-nowrap">
                                Observatoire Telraam
                            </h1>
                            <span class="text-[9px] font-bold px-1.5 py-0.5 rounded-full bg-amber-400/20 text-amber-300 border border-amber-400/30 uppercase tracking-wider hidden md:inline-block">
                                Rixensart
                            </span>
                        </div>
                        <p class="text-[10px] sm:text-xs text-slate-400 truncate hidden xs:block">
                            27 millions de trajectoires citoyennes 24h/24
                        </p>
                    </div>
                </div>

                <!-- Prominent Dual Tabs (Onglets) -->
                <div class="flex items-center gap-1.5 shrink-0">
                    <div class="flex items-center p-0.5 sm:p-1 bg-slate-900 rounded-xl border border-slate-800 shadow-inner">
                        <button id="tabBtnStory" onclick="switchTab('story')" class="px-2.5 sm:px-4 py-1 sm:py-1.5 rounded-lg text-xs font-bold transition flex items-center gap-1.5 bg-amber-400 text-slate-950 shadow-md cursor-pointer">
                            <i class="fa-solid fa-book-open text-xs"></i>
                            <span class="inline">Récit</span>
                        </button>
                        <button id="tabBtnLab" onclick="switchTab('lab')" class="px-2.5 sm:px-4 py-1 sm:py-1.5 rounded-lg text-xs font-bold transition flex items-center gap-1.5 text-slate-400 hover:text-white cursor-pointer">
                            <i class="fa-solid fa-flask-vial text-xs"></i>
                            <span class="inline">Labo</span>
                        </button>
                    </div>
                    <a href="https://telraam.net/en/network/rixensart" target="_blank" rel="noopener noreferrer" title="Voir le réseau Telraam officiel" class="hidden md:flex text-xs bg-slate-900 hover:bg-slate-800 text-slate-400 hover:text-white px-2.5 py-1.5 rounded-xl border border-slate-800 items-center gap-1.5 transition">
                        <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i>
                    </a>
                </div>
            </div>
        </div>
    </header>

    <!-- Main Views Container -->
    <main class="flex-1 w-full">

        <!-- ========================================================================= -->
        <!-- ONGLET 1 : LE RÉCIT SCROLLYTELLING GUIDÉ (LES ONDES URBAINES / JOYPLOT)   -->
        <!-- ========================================================================= -->
        <section id="storySection" class="relative w-full max-w-full border-b border-slate-800/80 bg-slate-950">
            
            <div class="max-w-7xl mx-auto px-2 sm:px-6 lg:px-8">
                <div class="story-scrolly-container lg:grid lg:grid-cols-12 lg:gap-8 relative w-full max-w-full min-w-0">

                    <!-- Sticky Visual Viewport:
                         - Desktop: Right column (col 7-12), sticky top-20 h-[calc(100vh-5rem)]
                         - Mobile: Sticky top-14 z-30 w-full max-w-full min-w-0 pt-1 pb-1
                    -->
                    <div id="viewportContainer" class="lg:col-span-7 xl:col-span-8 lg:order-2 sticky top-14 sm:top-16 z-30 w-full max-w-full min-w-0 pt-1 lg:pt-6 pb-2">
                        <div id="stickyVisualViewport" class="h-[215px] sm:h-[250px] lg:h-[calc(100vh-5rem)] transition-all duration-300 w-full max-w-full rounded-2xl overflow-hidden border border-slate-800/90 bg-slate-950 shadow-2xl relative flex flex-col">
                            
                            <!-- Integrated Top Stage Bar: Clear distinction without overlapping SVG curves -->
                            <div class="px-3 py-1.5 sm:py-2 bg-slate-900/95 border-b border-slate-800/90 flex items-center justify-between z-20 shrink-0">
                                <div class="flex items-center gap-2 min-w-0 pr-2">
                                    <span class="w-2 h-2 rounded-full bg-amber-400 animate-pulse shrink-0 shadow-sm shadow-amber-400"></span>
                                    <span id="visualSceneTitle" class="font-bold text-white tracking-wide text-xs sm:text-sm truncate">Prologue : Le pouls de Rixensart</span>
                                </div>

                                <div class="flex items-center gap-1.5 shrink-0">
                                    <!-- Mobile Chapter Badge -->
                                    <span id="visualSceneChapter" class="text-[10px] sm:text-xs font-black px-2 py-0.5 rounded-full bg-amber-400/15 text-amber-300 border border-amber-400/30">1 / 7</span>

                                    <!-- Desktop Mode Switcher -->
                                    <div class="hidden lg:flex items-center gap-0.5 bg-slate-800/80 p-0.5 rounded-lg text-[10px] font-bold">
                                        <button id="btnModeAll" onclick="setRidgeMode('all')" class="px-2 py-0.5 rounded bg-amber-400 text-slate-950 transition cursor-pointer">Tous</button>
                                        <button id="btnModeCars" onclick="setRidgeMode('cars')" class="px-2 py-0.5 rounded text-slate-300 hover:text-white transition cursor-pointer">Autos</button>
                                        <button id="btnModeBikes" onclick="setRidgeMode('bikes')" class="px-2 py-0.5 rounded text-slate-300 hover:text-white transition cursor-pointer">Vélos</button>
                                    </div>

                                    <!-- Citizen Sensors Toggle (Desktop) -->
                                    <button id="btnToggleCitizenRidge" onclick="toggleCitizenRidge()" title="Afficher ou masquer les 3 compteurs citoyens" class="hidden lg:flex px-2 py-0.5 rounded-lg border border-white/15 text-[10px] font-bold text-slate-300 hover:text-white transition items-center gap-1 cursor-pointer">
                                        <i id="iconToggleCitizen" class="fa-solid fa-plus text-[9px] text-amber-400"></i>
                                        <span id="labelToggleCitizen">3 Citoyens</span>
                                        <span id="badgeCitizenCount" class="text-[8px] px-1 rounded-full bg-slate-800 text-slate-400">10</span>
                                    </button>
                                </div>
                            </div>

                            <!-- D3 SVG Container for the Ondes Urbaines (Ridge Plot) -->
                            <svg id="d3RidgeSvg" class="w-full flex-1 block select-none" style="touch-action: pan-y;"></svg>

                            <!-- Floating Interactive Tooltip for Hourly Scrubber -->
                            <div id="ridgeTooltip" class="absolute pointer-events-none opacity-0 transition-opacity duration-150 glass-card px-3 py-2 rounded-xl border border-slate-700/80 text-xs shadow-2xl z-30 min-w-[170px] sm:min-w-[220px]">
                                <!-- Dynamically populated on hover/touch -->
                            </div>

                            <!-- Bottom Floating Action Bar in Viewport (Desktop) -->
                            <div class="hidden lg:flex absolute bottom-3 left-3.5 right-3.5 z-20 items-center justify-between pointer-events-auto">
                                <div class="text-[11px] text-slate-400 glass-card px-2.5 py-1 rounded-lg border border-white/10">
                                    <i class="fa-solid fa-hand-pointer text-amber-400 mr-1"></i> Survolez pour explorer le profil 24h
                                </div>
                                <button onclick="switchTab('lab')" class="text-xs font-bold text-slate-950 bg-amber-400 hover:bg-amber-300 px-3 py-1.5 rounded-xl shadow-lg transition flex items-center gap-1.5 ml-auto cursor-pointer">
                                    <span>Explorer le laboratoire citoyen</span>
                                    <i class="fa-solid fa-arrow-right text-[10px]"></i>
                                </button>
                            </div>

                            <!-- Mobile Stepper Bar (Guaranteed Zero Overflow, Ultra-Compact 26px) -->
                            <div class="lg:hidden flex items-center justify-between px-3 py-1 bg-slate-900/95 border-t border-slate-800/90 shrink-0 z-20">
                                <button id="btnPrevStepMob" onclick="goToStoryStep(currentStep - 1)" class="w-7 h-6 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white disabled:opacity-20 disabled:pointer-events-none flex items-center justify-center text-[10px] cursor-pointer">
                                    <i class="fa-solid fa-chevron-left"></i>
                                </button>
                                <div class="flex items-center gap-1.5 px-2" id="mobileStepDots">
                                    <button onclick="goToStoryStep(0)" aria-label="Prologue" class="step-dot w-2 h-2 rounded-full bg-amber-400 transition-all cursor-pointer shrink-0"></button>
                                    <button onclick="goToStoryStep(1)" aria-label="Acte 1" class="step-dot w-1.5 h-1.5 rounded-full bg-slate-700 transition-all cursor-pointer shrink-0"></button>
                                    <button onclick="goToStoryStep(2)" aria-label="Acte 2" class="step-dot w-1.5 h-1.5 rounded-full bg-slate-700 transition-all cursor-pointer shrink-0"></button>
                                    <button onclick="goToStoryStep(3)" aria-label="Acte 2 suite" class="step-dot w-1.5 h-1.5 rounded-full bg-slate-700 transition-all cursor-pointer shrink-0"></button>
                                    <button onclick="goToStoryStep(4)" aria-label="Acte 3" class="step-dot w-1.5 h-1.5 rounded-full bg-slate-700 transition-all cursor-pointer shrink-0"></button>
                                    <button onclick="goToStoryStep(5)" aria-label="Acte 4" class="step-dot w-1.5 h-1.5 rounded-full bg-slate-700 transition-all cursor-pointer shrink-0"></button>
                                    <button onclick="goToStoryStep(6)" aria-label="Acte 5" class="step-dot w-1.5 h-1.5 rounded-full bg-slate-700 transition-all cursor-pointer shrink-0"></button>
                                </div>
                                <button id="btnNextStepMob" onclick="goToStoryStep(currentStep + 1)" class="w-7 h-6 rounded bg-amber-400 text-slate-950 hover:bg-amber-300 disabled:opacity-20 disabled:pointer-events-none flex items-center justify-center text-[10px] font-bold cursor-pointer">
                                    <i class="fa-solid fa-chevron-right"></i>
                                </button>
                            </div>

                        </div>
                    </div>

                    <!-- Scrolling Narrative Cards Column (Left column on desktop, scrolling below on mobile) -->
                    <div id="cardsContainer" class="lg:col-span-5 xl:col-span-4 lg:order-1 pt-4 pb-24 lg:py-16 space-y-24 sm:space-y-36 lg:space-y-64 relative z-10 w-full max-w-full min-w-0">

                        <!-- STEP 0 : HERO PROLOGUE -->
                        <div class="story-step is-active" data-step="0">
                            <div class="glass-card p-4 sm:p-8 rounded-2xl border border-slate-700/80 shadow-2xl space-y-4 sm:space-y-5 max-w-full overflow-hidden">
                                <div class="inline-flex items-center gap-2 text-amber-400 text-xs font-bold uppercase tracking-wider bg-amber-400/10 border border-amber-400/25 px-3 py-1 rounded-full">
                                    <i class="fa-solid fa-water-ladder text-amber-400"></i>
                                    <span>Prologue • Enquête de Données</span>
                                </div>
                                <h2 class="text-xl sm:text-2xl lg:text-3xl font-black text-white leading-tight font-display tracking-tight">
                                    Que racontent <span class="text-amber-400">27 millions</span> de trajectoires à Rixensart ?
                                </h2>
                                <p class="text-base sm:text-lg text-slate-200 leading-relaxed">
                                    Entre le sentiment permanent d'engorgement aux heures de pointe et le calme de nos quartiers résidentiels, que révèlent les capteurs citoyens installés à nos fenêtres ?
                                </p>
                                <p class="text-sm sm:text-base text-slate-300 leading-relaxed">
                                    Pendant plus de deux ans, <strong>10 voiries officielles</strong> et les capteurs citoyens ont mesuré les pulsations de notre commune, 24h sur 24.
                                </p>
                                <div class="grid grid-cols-2 gap-2.5 pt-1">
                                    <div class="p-3.5 bg-slate-950/80 rounded-xl border border-slate-800 text-center min-w-0">
                                        <div class="text-xl sm:text-2xl font-black text-white font-display whitespace-nowrap">~32 000</div>
                                        <div class="text-[10px] sm:text-xs text-slate-400 font-bold uppercase tracking-wider mt-0.5 truncate">Véhicules / jour</div>
                                    </div>
                                    <div class="p-3.5 bg-slate-950/80 rounded-xl border border-slate-800 text-center min-w-0">
                                        <div class="text-base sm:text-lg lg:text-xl font-black text-emerald-400 font-display whitespace-nowrap">-3.8% à -13%</div>
                                        <div class="text-[10px] sm:text-xs text-slate-400 font-bold uppercase tracking-wider mt-0.5 truncate">Tendance globale</div>
                                    </div>
                                </div>
                                <div class="border-l-2 border-amber-400 pl-3.5 py-2 my-1 bg-gradient-to-r from-amber-400/10 to-transparent rounded-r-xl text-sm sm:text-base text-slate-200 italic">
                                    👁️ <strong>Regardez la scène ci-dessus :</strong> les ondes dorées pulsent au rythme synchronisé de nos rues de 0h à 24h.
                                </div>
                                <div class="pt-1 text-center text-xs text-amber-300/90 flex items-center justify-center gap-2 font-semibold">
                                    <span>Faites défiler pour entrer dans le récit</span>
                                    <i class="fa-solid fa-arrow-down animate-bounce text-xs"></i>
                                </div>
                            </div>
                        </div>

                        <!-- STEP 1 : ACTE 1 — LE SOUFFLE COMMUNAL -->
                        <div class="story-step" data-step="1">
                            <div class="glass-card p-4 sm:p-8 rounded-2xl border border-slate-700/80 shadow-2xl space-y-4 sm:space-y-5 max-w-full overflow-hidden">
                                <div class="inline-flex items-center gap-2 text-sky-400 text-xs font-bold uppercase tracking-wider bg-sky-400/10 border border-sky-400/25 px-3 py-1 rounded-full">
                                    <i class="fa-solid fa-chart-area"></i>
                                    <span>Acte 1 • 07h–09h : La pointe du matin</span>
                                </div>
                                <h3 class="text-xl sm:text-2xl lg:text-3xl font-black text-white leading-tight font-display tracking-tight">
                                    L'entonnoir pendulaire vers Bruxelles et la E411
                                </h3>
                                <p class="text-base sm:text-lg text-slate-200 leading-relaxed">
                                    Dès 07h15, le réseau bascule sous la pression des navetteurs. La <strong>Chaussée de La Hulpe</strong> et la <strong>Rue Haute</strong> absorbent l'essentiel de la poussée matinale.
                                </p>
                                <p class="text-sm sm:text-base text-slate-300 leading-relaxed">
                                    À <strong>08h00 pile</strong>, le trafic culmine à plus de <strong class="text-amber-400">580 véhicules par heure</strong> sur la Chaussée de La Hulpe, pendant que la Rue de la Gare enregistre un rabattement massif vers le RER.
                                </p>
                                <div class="border-l-2 border-sky-400 pl-3.5 py-2 my-1 bg-gradient-to-r from-sky-500/10 to-transparent rounded-r-xl text-sm sm:text-base text-sky-200">
                                    👁️ <strong>Le constat physique :</strong> 4 axes structurants concentrent à eux seuls plus de <strong>65% de toute la circulation motorisée</strong> de Rixensart.
                                </div>
                            </div>
                        </div>

                        <!-- STEP 2 : ACTE 2 — LE CHOC DE LA DÉVIATION -->
                        <div class="story-step" data-step="2">
                            <div class="glass-card p-4 sm:p-8 rounded-2xl border border-rose-900/60 shadow-2xl space-y-4 sm:space-y-5 max-w-full overflow-hidden">
                                <div class="inline-flex items-center gap-2 text-rose-400 text-xs font-bold uppercase tracking-wider bg-rose-400/10 border border-rose-400/25 px-3 py-1 rounded-full">
                                    <i class="fa-solid fa-triangle-exclamation"></i>
                                    <span>Acte 2 • Ce qui se voit : Chantiers & Reports</span>
                                </div>
                                <h3 class="text-xl sm:text-2xl lg:text-3xl font-black text-white leading-tight font-display tracking-tight">
                                    L'Avenue Royale fermée : l'asphyxie des rues voisines
                                </h3>
                                <p class="text-base sm:text-lg text-slate-200 leading-relaxed">
                                    <em>« On a l'impression que le trafic explose partout ! »</em> Ce ressenti unanime chez les riverains est mesurable avec une précision chirurgicale.
                                </p>
                                <p class="text-sm sm:text-base text-slate-300 leading-relaxed">
                                    L'<strong>Avenue de Boulogne-Billancourt</strong> (mise en évidence en rouge vif) a vu son onde bondir de <strong class="text-rose-400">+70.7%</strong> (2 258 véhicules/jour), transformant une voirie résidentielle en soupape de dérivation forcée.
                                </p>
                                <div class="p-3.5 sm:p-4 bg-rose-950/50 rounded-xl border border-rose-800/80 flex items-center justify-between gap-3 min-w-0">
                                    <div class="min-w-0">
                                        <div class="text-xs font-bold text-rose-300 uppercase tracking-wider">Report de trafic</div>
                                        <div class="text-sm sm:text-base font-bold text-white truncate">Av. Boulogne-Billancourt</div>
                                    </div>
                                    <div class="shrink-0 text-right">
                                        <div class="text-xl sm:text-2xl font-black text-rose-400 font-display">+70.7%</div>
                                        <div class="text-[10px] text-rose-300/80 uppercase font-semibold">2 258 véh./j</div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- STEP 3 : ACTE 2 SUITE — L'APAISEMENT SILENCIEUX -->
                        <div class="story-step" data-step="3">
                            <div class="glass-card p-4 sm:p-8 rounded-2xl border border-emerald-900/60 shadow-2xl space-y-4 sm:space-y-5 max-w-full overflow-hidden">
                                <div class="inline-flex items-center gap-2 text-emerald-400 text-xs font-bold uppercase tracking-wider bg-emerald-400/10 border border-emerald-400/25 px-3 py-1 rounded-full">
                                    <i class="fa-solid fa-leaf"></i>
                                    <span>Acte 2b • Ce qui ne se voit pas : L'évaporation</span>
                                </div>
                                <h3 class="text-xl sm:text-2xl lg:text-3xl font-black text-white leading-tight font-display tracking-tight">
                                    Place Communale : la chute spectaculaire de -66.9%
                                </h3>
                                <p class="text-base sm:text-lg text-slate-200 leading-relaxed">
                                    Alors que le transit sature l'Avenue Albert 1er et l'Avenue de Mérode, regardez la <strong>Place Communale de Genval</strong> : son onde s'affaisse en un doux ruban vert émeraude.
                                </p>
                                <p class="text-sm sm:text-base text-slate-300 leading-relaxed">
                                    Son passage en <strong>Zone 20 de rencontre</strong> (priorité piétonne, chicanes, pavés) a provoqué une <em>évaporation</em> physique du trafic de transit. Les voitures évitent le centre sans que le trafic ne se reporte entièrement ailleurs.
                                </p>
                                <div class="p-3.5 sm:p-4 bg-emerald-950/50 rounded-xl border border-emerald-800/80 flex items-center justify-between gap-3 min-w-0">
                                    <div class="min-w-0">
                                        <div class="text-xs font-bold text-emerald-300 uppercase tracking-wider">Zone 20 de rencontre</div>
                                        <div class="text-sm sm:text-base font-bold text-white truncate">Place Communale Genval</div>
                                    </div>
                                    <div class="shrink-0 text-right">
                                        <div class="text-xl sm:text-2xl font-black text-emerald-400 font-display">-66.9%</div>
                                        <div class="text-[10px] text-emerald-300/80 uppercase font-semibold">Évaporation transit</div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- STEP 4 : ACTE 3 — L'ESSOR DU VÉLO -->
                        <div class="story-step" data-step="4">
                            <div class="glass-card p-4 sm:p-8 rounded-2xl border border-teal-900/60 shadow-2xl space-y-4 sm:space-y-5 max-w-full overflow-hidden">
                                <div class="inline-flex items-center gap-2 text-teal-400 text-xs font-bold uppercase tracking-wider bg-teal-400/10 border border-teal-400/25 px-3 py-1 rounded-full">
                                    <i class="fa-solid fa-person-biking"></i>
                                    <span>Acte 3 • La révolution silencieuse du vélo</span>
                                </div>
                                <h3 class="text-xl sm:text-2xl lg:text-3xl font-black text-white leading-tight font-display tracking-tight">
                                    Au printemps, le vélo bondit de +194% vers la nouvelle gare RER
                                </h3>
                                <p class="text-base sm:text-lg text-slate-200 leading-relaxed">
                                    Les ondes automobiles s'effacent pour révéler les profils cyclistes en bleu turquoise. La saisonnalité est spectaculaire : le trafic vélo triple dès les beaux jours.
                                </p>
                                <p class="text-sm sm:text-base text-slate-300 leading-relaxed">
                                    Deux pics se détachent nettement : <strong>08h00</strong> le matin et <strong>17h00</strong> le soir. La nouvelle gare RER de Rixensart a créé un couloir cycliste structurant sur la <strong>Rue de la Gare</strong> (154 vélos/j) et la Rue Haute.
                                </p>
                                <div class="p-3.5 sm:p-4 bg-teal-950/50 rounded-xl border border-teal-800/80 flex items-center justify-between gap-3 min-w-0">
                                    <div class="min-w-0">
                                        <div class="text-xs font-bold text-teal-300 uppercase tracking-wider">Mobilité active vers le RER</div>
                                        <div class="text-sm sm:text-base font-bold text-white truncate">Rue de la Gare & Tilleul</div>
                                    </div>
                                    <div class="shrink-0 text-right">
                                        <div class="text-xl sm:text-2xl font-black text-teal-400 font-display">+194%</div>
                                        <div class="text-[10px] text-teal-300/80 uppercase font-semibold">Au printemps</div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- STEP 5 : ACTE 4 — LA VITESSE RÉELLE V85 -->
                        <div class="story-step" data-step="5">
                            <div class="glass-card p-4 sm:p-8 rounded-2xl border border-amber-900/60 shadow-2xl space-y-4 sm:space-y-5 max-w-full overflow-hidden">
                                <div class="inline-flex items-center gap-2 text-amber-400 text-xs font-bold uppercase tracking-wider bg-amber-400/10 border border-amber-400/25 px-3 py-1 rounded-full">
                                    <i class="fa-solid fa-gauge-high"></i>
                                    <span>Acte 4 • Vitesse réelle : La science du V85</span>
                                </div>
                                <h3 class="text-xl sm:text-2xl lg:text-3xl font-black text-white leading-tight font-display tracking-tight">
                                    Roule-t-on trop vite ? Les leçons de la physique urbaine
                                </h3>
                                <p class="text-base sm:text-lg text-slate-200 leading-relaxed">
                                    Le <strong>V85</strong> est la vitesse sous laquelle roulent 85% des usagers. Il mesure la vitesse naturelle induite par la largeur et l'aménagement de la rue.
                                </p>
                                <p class="text-sm sm:text-base text-slate-300 leading-relaxed">
                                    Le constat est indiscutable : les aménagements physiques calment instantanément (<strong>21 km/h</strong> Place Communale en Zone 20). À l'inverse, sur les chaussées larges (Albert 1er), le V85 dépasse <strong>60 km/h</strong>.
                                </p>
                                <div class="grid grid-cols-2 gap-2.5 pt-1">
                                    <div class="p-3 bg-emerald-950/40 rounded-xl border border-emerald-800/60 text-center min-w-0">
                                        <div class="text-lg sm:text-xl font-black text-emerald-400 font-display">21 km/h</div>
                                        <div class="text-[10px] text-emerald-300 uppercase font-bold mt-0.5 truncate">Pl. Communale (Zone 20)</div>
                                    </div>
                                    <div class="p-3 bg-rose-950/40 rounded-xl border border-rose-800/60 text-center min-w-0">
                                        <div class="text-lg sm:text-xl font-black text-rose-400 font-display">62 km/h</div>
                                        <div class="text-[10px] text-rose-300 uppercase font-bold mt-0.5 truncate">Albert 1er (Zone 50)</div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- STEP 6 : TRANSITION VERS LE LABORATOIRE CITOYEN -->
                        <div class="story-step" data-step="6">
                            <div class="glass-card p-4 sm:p-8 rounded-2xl border border-amber-400/80 shadow-2xl space-y-4 sm:space-y-5 max-w-full overflow-hidden">
                                <div class="inline-flex items-center gap-2 text-amber-400 text-xs font-bold uppercase tracking-wider bg-amber-400/10 border border-amber-400/25 px-3 py-1 rounded-full">
                                    <i class="fa-solid fa-flask"></i>
                                    <span>Acte 5 • Le Laboratoire Citoyen</span>
                                </div>
                                <h3 class="text-xl sm:text-2xl lg:text-3xl font-black text-white leading-tight font-display tracking-tight">
                                    Explorez les données de chaque rue de votre quartier
                                </h3>
                                <p class="text-base sm:text-lg text-slate-200 leading-relaxed">
                                    Vous venez de parcourir les grands enseignements du réseau. Le <strong>Laboratoire Citoyen</strong> vous ouvre l'ensemble des outils interactifs d'investigation :
                                </p>
                                <div class="space-y-2.5 text-sm sm:text-base text-slate-300 pt-1">
                                    <div class="flex items-start gap-2.5 p-3 bg-slate-950/70 rounded-xl border border-slate-800">
                                        <i class="fa-solid fa-map-location-dot text-amber-400 mt-1 text-base shrink-0"></i>
                                        <div><strong>Carte interactive 24h :</strong> simulez le trafic heure par heure et observez chaque axe.</div>
                                    </div>
                                    <div class="flex items-start gap-2.5 p-3 bg-slate-950/70 rounded-xl border border-slate-800">
                                        <i class="fa-solid fa-chart-line text-sky-400 mt-1 text-base shrink-0"></i>
                                        <div><strong>Analyses comparatives :</strong> 2 ans d'historique, météo et saisons sans biais.</div>
                                    </div>
                                    <div class="flex items-start gap-2.5 p-3 bg-slate-950/70 rounded-xl border border-slate-800">
                                        <i class="fa-solid fa-table text-emerald-400 mt-1 text-base shrink-0"></i>
                                        <div><strong>Tableau de bord exhaustif :</strong> fiches analytiques et Open Data.</div>
                                    </div>
                                </div>
                                <button onclick="switchTab('lab')" class="w-full py-3.5 rounded-xl font-black text-slate-950 bg-amber-400 hover:bg-amber-300 shadow-xl transition flex items-center justify-center gap-2.5 mt-2 text-sm sm:text-base cursor-pointer">
                                    <i class="fa-solid fa-flask-vial"></i>
                                    <span>Entrer dans le Laboratoire Citoyen</span>
                                    <i class="fa-solid fa-arrow-right text-xs"></i>
                                </button>
                            </div>
                        </div>

                    </div>

                </div>
            </div>

        </section>
        <!-- ========================================================================= -->
        <!-- ONGLET 2 : LE LABORATOIRE CITOYEN D'EXPLORATION LIBRE (Dashboard 24h)     -->
        <!-- ========================================================================= -->
        <section id="labSection" class="bg-slate-950 text-slate-100 py-8 px-4 sm:px-6 lg:px-8 min-h-screen hidden">
            <div class="max-w-7xl mx-auto space-y-6">

                <!-- Lab Header & 24h Slider Control Panel -->
                <div class="bg-gradient-to-r from-slate-950 via-slate-900 to-slate-950 text-white rounded-2xl p-6 border border-slate-800 shadow-xl space-y-5">
                    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-5">
                        <div>
                            <div class="flex items-center gap-2 text-amber-400 text-xs font-bold uppercase tracking-wider">
                                <i class="fa-solid fa-flask-vial"></i>
                                <span>Laboratoire Citoyen Interactif</span>
                            </div>
                            <h2 class="text-xl sm:text-2xl font-black text-white mt-1">
                                Explorez Rixensart Heure par Heure & en Temps Réel
                            </h2>
                            <p class="text-xs text-slate-400 mt-1 max-w-3xl">
                                Manipulez le curseur horaire pour observer la pulsation du trafic au cours de la journée (heures creuses, pointes scolaires et navetteurs). Cliquez sur n'importe quel capteur de la carte pour inspecter ses statistiques complètes.
                            </p>
                        </div>

                        <!-- Back to Story & Status Badge -->
                        <div class="flex items-center gap-3 shrink-0">
                            <button onclick="switchTab('story')" class="px-3 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-amber-300 border border-amber-400/30 text-xs font-bold transition flex items-center gap-1.5 shadow-sm cursor-pointer">
                                <i class="fa-solid fa-arrow-left text-[11px]"></i>
                                <span>Voir le Récit Visuel</span>
                            </button>
                            <div class="w-10 h-10 rounded-xl bg-amber-400/10 border border-amber-400/30 flex items-center justify-center text-amber-400 text-lg font-black">
                                <i class="fa-solid fa-sliders"></i>
                            </div>
                        </div>
                    </div>

                    <!-- 24h Slider Dynamic Widget -->
                    <div class="space-y-3 pt-1">
                        <div class="flex flex-wrap items-center justify-between gap-2">
                            <div class="flex items-center gap-2">
                                <button id="btnPlaySlider" onclick="togglePlaySlider()" class="w-9 h-9 rounded-xl bg-amber-400 hover:bg-amber-300 text-slate-950 flex items-center justify-center font-bold shadow-md transition cursor-pointer">
                                    <i id="iconPlay" class="fa-solid fa-play ml-0.5"></i>
                                </button>
                                <span class="text-sm font-black text-white tracking-wide" id="labelCurrentHour">08h00 — 09h00 (Pointe du Matin)</span>
                            </div>
                            <div class="flex items-center gap-2 text-xs">
                                <span id="badgeHourContext" class="px-3 py-1 rounded-full bg-rose-500/20 text-rose-300 border border-rose-500/30 font-bold">
                                    Forte Affluence Navetteurs Matin
                                </span>
                                <span class="text-slate-500 hidden md:inline">• Utilisez le curseur ci-dessous</span>
                            </div>
                        </div>

                        <!-- Range input slider 0-23 -->
                        <div class="relative py-1">
                            <input id="slider24h" type="range" min="0" max="23" value="8" step="1" oninput="onSliderHourChange(this.value)" class="w-full h-2.5 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-amber-400">
                            <div class="flex justify-between text-[10px] text-slate-400 font-semibold px-1 mt-1.5 select-none">
                                <span>00h</span>
                                <span>04h</span>
                                <span class="text-amber-400 font-bold">08h (Pointe)</span>
                                <span>12h</span>
                                <span class="text-amber-400 font-bold">17h (Pointe)</span>
                                <span>20h</span>
                                <span>23h</span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Lab Navigation & Period Switcher Bar -->
                <div class="flex flex-wrap items-center justify-between gap-3 bg-slate-950 p-4 rounded-2xl border border-slate-800 shadow-md">
                    <div class="flex flex-wrap items-center gap-3">
                        <span class="text-xs text-slate-400 font-bold uppercase tracking-wider flex items-center gap-1.5">
                            <i class="fa-solid fa-calendar-days text-amber-400"></i> Période :
                        </span>
                        <div class="inline-flex bg-slate-900 p-1 rounded-xl border border-slate-800 text-xs font-bold">
                            <button id="btnPeriodNov" class="px-3 py-1.5 rounded-lg text-white bg-telraam-blue shadow transition cursor-pointer">
                                Novembre 2024 (Lancement)
                            </button>
                            <button id="btnPeriodRec" class="px-3 py-1.5 rounded-lg text-slate-400 hover:text-white transition cursor-pointer">
                                Temps Réel (2026)
                            </button>
                        </div>
                    </div>

                    <!-- Quick Section Anchors -->
                    <div class="flex items-center gap-2 overflow-x-auto no-scrollbar pb-1 text-xs font-semibold">
                        <button id="btnNavYoY" class="px-2.5 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-amber-300 border border-amber-500/30 transition cursor-pointer flex items-center gap-1">
                            <i class="fa-solid fa-arrow-trend-up text-amber-400"></i> Tendances YoY
                        </button>
                        <button id="btnPeriodHist" class="px-2.5 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-emerald-300 border border-emerald-500/30 transition cursor-pointer flex items-center gap-1">
                            <i class="fa-solid fa-chart-line text-emerald-400"></i> Historique 2 Ans
                        </button>
                        <button id="btnNavTravaux" class="px-2.5 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-orange-300 border border-orange-500/30 transition cursor-pointer flex items-center gap-1">
                            <i class="fa-solid fa-person-digging text-orange-400"></i> Chantiers
                        </button>
                        <button id="btnNavRegional" class="px-2.5 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-teal-300 border border-teal-500/30 transition cursor-pointer flex items-center gap-1">
                            <i class="fa-solid fa-compass text-teal-400"></i> Régional
                        </button>
                        <button id="btnNavSources" class="px-2.5 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-sky-300 border border-sky-500/30 transition cursor-pointer flex items-center gap-1">
                            <i class="fa-solid fa-bookmark text-sky-400"></i> Sources
                        </button>
                    </div>
                </div>

                <!-- GLOBAL KPI METRICS GRID (4 CARDS) -->
                {c_kpi_block}

                <!-- INTERACTIVE MAP & SENSOR DETAILS SPLIT VIEW -->
                <div id="interactiveMapSection">
                    {c_map_block}
                </div>

                <!-- 4 COMPARATIVE CHARTS GRID -->
                <div id="comparativeChartsSection">
                    {c_charts_block}
                </div>

                <!-- 2-YEAR HISTORICAL TIMELINE & SEASONALITY -->
                <div id="historyTimelineSection">
                    {c_history_block}
                </div>

                <!-- DEDICATED YOY MULTI-YEAR TREND ANALYSIS -->
                <div id="yoySectionWrapper">
                    {c_yoy_block}
                </div>

                <!-- CHANTIERS & DÉVIATIONS (2024-2026) -->
                <div id="travauxSectionWrapper">
                    {c_travaux_block}
                </div>

                <!-- REGIONAL CONTEXT & PARADOX -->
                <div id="regionalSectionWrapper">
                    {c_regional_block}
                    {c_recommendations_block}
                </div>

                <!-- FULL COMPREHENSIVE DATA TABLE (WITH MOBILE CARDS) -->
                <div id="tableSectionWrapper">
                    {c_table_block_clean}
                </div>

                <!-- METHODOLOGY & SOURCES -->
                <div id="methodologySectionWrapper">
                    {c_methodology_block}
                    {c_sources_block}
                </div>

            </div>
        </section>

    </main>

    <!-- Footer -->
    <footer class="bg-slate-950 border-t border-slate-800 py-6 sm:py-8 text-slate-400 text-xs w-full max-w-full overflow-hidden">
        <div class="max-w-7xl mx-auto px-3 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-3 text-center sm:text-left">
            <div class="flex flex-wrap items-center justify-center sm:justify-start gap-x-2 gap-y-1">
                <span>© 2026 Observatoire Mobilité Telraam</span>
                <span>•</span>
                <span>Commune de Rixensart</span>
                <span class="hidden sm:inline">•</span>
                <span class="hidden sm:inline">Données citoyennes 24h/24</span>
            </div>
            <div class="flex flex-wrap items-center justify-center gap-3">
                <button onclick="scrollToTop()" class="hover:text-amber-400 transition cursor-pointer">
                    <i class="fa-solid fa-arrow-up mr-1"></i> Haut
                </button>
                <span class="text-slate-700">•</span>
                <a href="https://telraam.net" target="_blank" class="hover:text-white transition">Telraam.net</a>
                <span class="text-slate-700">•</span>
                <a href="https://www.rixensart.be" target="_blank" class="hover:text-white transition">Rixensart.be</a>
            </div>
        </div>
    </footer>

    <!-- Load Local JS Data -->
    <script src="data/rixensart_data.js"></script>

    <!-- Dual Tab Manager, Scrollytelling D3 Ridge Plot Engine & Citizen Lab Controller -->
    <script>
        // ==========================================
        // 1. DUAL TAB NAVIGATION MANAGER (ONGLETS)
        // ==========================================
        function scrollToTop() {{
            window.scrollTo({{ top: 0, behavior: 'smooth' }});
        }}

        function switchTab(tabId) {{
            const storySec = document.getElementById('storySection');
            const labSec = document.getElementById('labSection');
            const tabBtnStory = document.getElementById('tabBtnStory');
            const tabBtnLab = document.getElementById('tabBtnLab');

            if (tabId === 'lab') {{
                if (storySec) storySec.classList.add('hidden');
                if (labSec) labSec.classList.remove('hidden');

                if (tabBtnLab) tabBtnLab.className = "px-3 sm:px-4 py-1.5 rounded-lg text-xs font-bold transition flex items-center gap-1.5 sm:gap-2 bg-amber-400 text-slate-950 shadow-md cursor-pointer";
                if (tabBtnStory) tabBtnStory.className = "px-3 sm:px-4 py-1.5 rounded-lg text-xs font-bold transition flex items-center gap-1.5 sm:gap-2 text-slate-400 hover:text-white cursor-pointer";

                history.replaceState(null, '', '#lab');
                window.scrollTo(0, 0);

                // Invalidate Leaflet map size so tiles and vector layers render properly
                setTimeout(() => {{
                    if (window.leafletMapInstance) {{
                        window.leafletMapInstance.invalidateSize();
                    }}
                }}, 80);
            }} else {{
                if (labSec) labSec.classList.add('hidden');
                if (storySec) storySec.classList.remove('hidden');

                if (tabBtnStory) tabBtnStory.className = "px-3 sm:px-4 py-1.5 rounded-lg text-xs font-bold transition flex items-center gap-1.5 sm:gap-2 bg-amber-400 text-slate-950 shadow-md cursor-pointer";
                if (tabBtnLab) tabBtnLab.className = "px-3 sm:px-4 py-1.5 rounded-lg text-xs font-bold transition flex items-center gap-1.5 sm:gap-2 text-slate-400 hover:text-white cursor-pointer";

                history.replaceState(null, '', '#story');
                window.scrollTo(0, 0);

                if (typeof window.triggerRidgeResize === 'function') {{
                    window.triggerRidgeResize();
                }}
            }}
        }}
        window.switchTab = switchTab;
        window.scrollToStory = scrollToStory;
        window.scrollToLab = scrollToLab;

        function scrollToStory() {{
            switchTab('story');
        }}

        function scrollToLab() {{
            switchTab('lab');
        }}

        // Listen for browser back/forward and hash changes
        window.addEventListener('DOMContentLoaded', () => {{
            if (window.location.hash === '#lab' || window.location.hash === '#laboratoire') {{
                switchTab('lab');
            }} else {{
                switchTab('story');
            }}
        }});

        window.addEventListener('hashchange', () => {{
            if (window.location.hash === '#lab' || window.location.hash === '#laboratoire') {{
                switchTab('lab');
            }} else if (window.location.hash === '#story' || window.location.hash === '#recit') {{
                switchTab('story');
            }}
        }});

        // Global functions exposed to UI
        window.currentStep = 0;
        let currentStep = 0;
        window.setRidgeMode = function(mode) {{}};
        window.toggleCitizenRidge = function() {{}};
        window.setRidgeCitizenScope = function(show) {{}};
        window.goToStoryStep = function(idx) {{}};
        let setRidgeMode = window.setRidgeMode;
        let toggleCitizenRidge = window.toggleCitizenRidge;
        let setRidgeCitizenScope = window.setRidgeCitizenScope;
        let goToStoryStep = window.goToStoryStep;

        // ==========================================
        // 2. D3.JS RIDGE PLOT (ONDES URBAINES 24H) ENGINE
        // ==========================================
        (function() {{
            const svgEl = document.getElementById('d3RidgeSvg');
            if (!svgEl) return;
            const svg = d3.select(svgEl);

            let width = 0, height = 0;
            let currentStep = 0;
            let currentMode = 'all'; // 'all', 'cars', 'bikes'
            let showCitizen = false; // MASKED BY DEFAULT per user request
            let activeScrubberHour = null;

            // Short names mapping for clean mobile / desktop typography
            const SHORT_NAMES = {{
                9000007497: {{ full: "Av. Franklin Roosevelt", short: "Roosevelt", limit: 50, v85: 49.1, arterial: true }},
                9000007533: {{ full: "Avenue Albert 1er", short: "Albert 1er", limit: 50, v85: 62.0, arterial: true }},
                9000007492: {{ full: "Chaussée de La Hulpe", short: "Ch. La Hulpe", limit: 50, v85: 39.7, arterial: true }},
                9000007523: {{ full: "Rue Haute", short: "Rue Haute", limit: 50, v85: 47.3, arterial: true }},
                9000007509: {{ full: "Rue de l'Institut", short: "Institut", limit: 50, v85: 53.1, arterial: false }},
                9000007578: {{ full: "Rue de la Gare", short: "Gare", limit: 50, v85: 44.5, arterial: false }},
                9000007512: {{ full: "Rue de la Tasnière", short: "Tasnière", limit: 50, v85: 41.6, arterial: false }},
                9000007490: {{ full: "Rue de Genval", short: "Genval", limit: 50, v85: 53.1, arterial: false }},
                9000007530: {{ full: "Place Communale", short: "Pl. Communale", limit: 20, v85: 21.0, arterial: false }},
                9000007534: {{ full: "Av. Boulogne-Billancourt", short: "Boulogne-B.", limit: 50, v85: 59.2, arterial: false }},
                9000006402: {{ full: "Rue du Tilleul", short: "Tilleul", limit: 30, v85: 37.2, arterial: false }},
                9000007261: {{ full: "Rue Mahiermont", short: "Mahiermont", limit: 30, v85: 24.2, arterial: false }},
                9000009405: {{ full: "Rue des Bergères", short: "Bergères (Éc.)", limit: 30, v85: 31.1, arterial: false }}
            }};

            // 1. Prepare and Sort 13 Sensors by Daily Volume
            const rawSensors = window.TELRAAM_RIXENSART || [];
            const sortedSensors = [...rawSensors].sort((a, b) => {{
                const totA = a.nov2024?.daily_total || a.recent2026?.daily_total || 0;
                const totB = b.nov2024?.daily_total || b.recent2026?.daily_total || 0;
                return totB - totA;
            }});

            // 2. Build 24-hour profiles for each sensor
            function build24hProfile(sensor) {{
                const nov = sensor.nov2024 || {{}};
                const rawCars = (nov.hourly && nov.hourly.cars_weekday) ? [...nov.hourly.cars_weekday] : [];
                const rawBikes = (nov.hourly && nov.hourly.bikes_weekday) ? [...nov.hourly.bikes_weekday] : [];
                const dailyTotal = nov.daily_total || sensor.recent2026?.daily_total || 500;

                // Special sensor: Rue des Bergères (école Rosières, ~354 véh/j)
                if (sensor.id === 9000009405) {{
                    const schoolCars = [2, 1, 1, 1, 2, 6, 18, 55, 78, 22, 16, 24, 30, 22, 18, 62, 54, 32, 20, 12, 8, 5, 3, 2];
                    const schoolBikes = [0, 0, 0, 0, 0, 1, 2, 5, 7, 2, 1, 2, 3, 2, 1, 6, 4, 2, 1, 1, 0, 0, 0, 0];
                    return {{
                        cars: schoolCars,
                        bikes: schoolBikes,
                        springBikes: schoolBikes.map(v => Math.round(v * 2.8)),
                        surgeCars: schoolCars,
                        calmCars: schoolCars
                    }};
                }}

                const cars = new Array(24).fill(0);
                const bikes = new Array(24).fill(0);

                for (let h = 7; h <= 16; h++) {{
                    cars[h] = rawCars[h] || 0;
                    bikes[h] = rawBikes[h] || 0;
                }}

                // Evening peak at 17h (November dusk correction: 92% of 16h)
                cars[17] = Math.max(rawCars[17] || 0, Math.round(cars[16] * 0.92));
                bikes[17] = Math.max(rawBikes[17] || 0, Math.round(bikes[16] * 0.90));

                // Evening commute tapering (18 to 23)
                const c17 = cars[17];
                cars[18] = Math.round(c17 * 0.68);
                cars[19] = Math.round(c17 * 0.45);
                cars[20] = Math.round(c17 * 0.30);
                cars[21] = Math.round(c17 * 0.18);
                cars[22] = Math.round(c17 * 0.11);
                cars[23] = Math.round(c17 * 0.06);

                // Deep night (0 to 4)
                cars[0] = Math.round(c17 * 0.04);
                cars[1] = Math.round(c17 * 0.025);
                cars[2] = Math.round(c17 * 0.018);
                cars[3] = Math.round(c17 * 0.018);
                cars[4] = Math.round(c17 * 0.030);

                // Early dawn (5 to 6)
                const c7 = cars[7] || (dailyTotal * 0.05);
                cars[5] = Math.round(c7 * 0.22);
                cars[6] = Math.round(c7 * 0.58);

                // Bike night tapering
                const b17 = bikes[17];
                bikes[18] = Math.round(b17 * 0.55);
                bikes[19] = Math.round(b17 * 0.30);
                bikes[20] = Math.round(b17 * 0.15);
                bikes[21] = Math.round(b17 * 0.08);

                // Spring multiplier for bikes (+194% seasonal surge)
                const springBikes = bikes.map(v => Math.round(v * 2.8));

                // Detour surge for Boulogne-Billancourt (+70.7%) and Rue de la Gare (+58.9%)
                let surgeCars = [...cars];
                if (sensor.id === 9000007534) {{
                    surgeCars = cars.map(v => Math.round(v * 1.707));
                }} else if (sensor.id === 9000007578) {{
                    surgeCars = cars.map(v => Math.round(v * 1.589));
                }}

                // Calmed for Place Communale (-66.9%)
                let calmCars = [...cars];
                if (sensor.id === 9000007530) {{
                    calmCars = cars.map(v => Math.round(v * 0.331));
                }}

                return {{ cars, bikes, springBikes, surgeCars, calmCars }};
            }}

            const streetData = sortedSensors.map((s, idx) => {{
                const isOfficial = (s.is_official === true);
                const meta = SHORT_NAMES[s.id] || {{
                    full: s.street,
                    short: s.street.slice(0, 14),
                    limit: s.speed_limit || 50,
                    v85: s.nov2024?.speed?.avg_v85 || 40,
                    arterial: idx < 4
                }};
                const dailyTotal = s.nov2024?.daily_total || s.recent2026?.daily_total || 500;
                const profiles = build24hProfile(s);

                return {{
                    id: s.id,
                    street: s.street,
                    displayName: meta.full,
                    shortName: meta.short,
                    speedLimit: meta.limit,
                    v85: meta.v85,
                    isArterial: meta.arterial,
                    isOfficial: isOfficial,
                    networkType: s.network_type || (isOfficial ? 'Officiel Municipal' : 'Citoyen'),
                    dailyTotal: dailyTotal,
                    locality: s.locality || 'Rixensart',
                    profiles: profiles
                }};
            }});

            // 3. Setup SVG Defs (Gradients and Glow Filters)
            function setupDefs() {{
                svg.selectAll('defs').remove();
                const defs = svg.append('defs');

                // Glow filter for crest strokes
                const filter = defs.append('filter')
                    .attr('id', 'crest-glow')
                    .attr('x', '-20%')
                    .attr('y', '-20%')
                    .attr('width', '140%')
                    .attr('height', '140%');
                filter.append('feGaussianBlur')
                    .attr('stdDeviation', '2.5')
                    .attr('result', 'coloredBlur');
                const feMerge = filter.append('feMerge');
                feMerge.append('feMergeNode').attr('in', 'coloredBlur');
                feMerge.append('feMergeNode').attr('in', 'SourceGraphic');

                // Gradients
                // Arterial (Gold Crest)
                const gradArterial = defs.append('linearGradient')
                    .attr('id', 'grad-arterial')
                    .attr('x1', '0%').attr('y1', '100%').attr('x2', '0%').attr('y2', '0%');
                gradArterial.append('stop').attr('offset', '0%').attr('stop-color', '#0c192c').attr('stop-opacity', 0.95);
                gradArterial.append('stop').attr('offset', '50%').attr('stop-color', '#0284c7').attr('stop-opacity', 0.85);
                gradArterial.append('stop').attr('offset', '85%').attr('stop-color', '#f59e0b').attr('stop-opacity', 0.95);
                gradArterial.append('stop').attr('offset', '100%').attr('stop-color', '#fbbf24').attr('stop-opacity', 1.0);

                // Standard (Sky Blue Crest)
                const gradStandard = defs.append('linearGradient')
                    .attr('id', 'grad-standard')
                    .attr('x1', '0%').attr('y1', '100%').attr('x2', '0%').attr('y2', '0%');
                gradStandard.append('stop').attr('offset', '0%').attr('stop-color', '#091524').attr('stop-opacity', 0.92);
                gradStandard.append('stop').attr('offset', '60%').attr('stop-color', '#0369a1').attr('stop-opacity', 0.80);
                gradStandard.append('stop').attr('offset', '100%').attr('stop-color', '#38bdf8').attr('stop-opacity', 0.95);

                // Surge (Flame Red Detour)
                const gradSurge = defs.append('linearGradient')
                    .attr('id', 'grad-surge')
                    .attr('x1', '0%').attr('y1', '100%').attr('x2', '0%').attr('y2', '0%');
                gradSurge.append('stop').attr('offset', '0%').attr('stop-color', '#450a0a').attr('stop-opacity', 0.95);
                gradSurge.append('stop').attr('offset', '55%').attr('stop-color', '#dc2626').attr('stop-opacity', 0.88);
                gradSurge.append('stop').attr('offset', '100%').attr('stop-color', '#f87171').attr('stop-opacity', 1.0);

                // Calmed Zone 20 (Emerald Green)
                const gradCalm = defs.append('linearGradient')
                    .attr('id', 'grad-calm')
                    .attr('x1', '0%').attr('y1', '100%').attr('x2', '0%').attr('y2', '0%');
                gradCalm.append('stop').attr('offset', '0%').attr('stop-color', '#064e3b').attr('stop-opacity', 0.95);
                gradCalm.append('stop').attr('offset', '60%').attr('stop-color', '#059669').attr('stop-opacity', 0.85);
                gradCalm.append('stop').attr('offset', '100%').attr('stop-color', '#34d399').attr('stop-opacity', 1.0);

                // Bike (Electric Teal / Cyan)
                const gradBike = defs.append('linearGradient')
                    .attr('id', 'grad-bike')
                    .attr('x1', '0%').attr('y1', '100%').attr('x2', '0%').attr('y2', '0%');
                gradBike.append('stop').attr('offset', '0%').attr('stop-color', '#134e4a').attr('stop-opacity', 0.95);
                gradBike.append('stop').attr('offset', '60%').attr('stop-color', '#0d9488').attr('stop-opacity', 0.85);
                gradBike.append('stop').attr('offset', '100%').attr('stop-color', '#2dd4bf').attr('stop-opacity', 1.0);
            }}

            // 4. Main Render Function
            // ==========================================
            // STEP-BY-STEP NARRATIVE FOCUS CONFIGURATION
            // ==========================================
            const STEP_FOCUS = {{
                0: {{
                    title: "Prologue : Le pouls de Rixensart",
                    chapter: "1 / 7",
                    mobileIds: [9000007492, 9000007523, 9000007533], // Ch. La Hulpe, Rue Haute, Albert 1er
                    badgeText: "27M TRAJETS"
                }},
                1: {{
                    title: "Acte 1 : La pointe du matin (07h-09h)",
                    chapter: "2 / 7",
                    mobileIds: [9000007492, 9000007523, 9000007578], // Ch. La Hulpe, Rue Haute, Rue de la Gare
                    badgeText: "POINTE : 08h00"
                }},
                2: {{
                    title: "Acte 2 : Déviation Avenue Royale",
                    chapter: "3 / 7",
                    mobileIds: [9000007534, 9000007578, 9000007523], // Boulogne-B., Gare, Haute
                    badgeText: "CHANTIER : +70.7%"
                }},
                3: {{
                    title: "Acte 2b : Place Communale Zone 20",
                    chapter: "4 / 7",
                    mobileIds: [9000007530, 9000007533], // Place Communale (-66.9%) vs Albert 1er
                    badgeText: "ZONE 20 : -66.9%"
                }},
                4: {{
                    title: "Acte 3 : Vélos vers le RER (+194%)",
                    chapter: "5 / 7",
                    mobileIds: [9000007578, 9000007509, 9000006402], // Gare, Institut, Tilleul
                    badgeText: "PRINTEMPS : +194%"
                }},
                5: {{
                    title: "Acte 4 : Vitesse réelle V85",
                    chapter: "6 / 7",
                    mobileIds: [9000007533, 9000007523, 9000007530], // Albert 1er (62), Haute (47), Pl. Communale (21)
                    badgeText: "V85 AU MICROSCOPE"
                }},
                6: {{
                    title: "Acte 5 : Le Laboratoire Citoyen",
                    chapter: "7 / 7",
                    mobileIds: [9000007492, 9000007523, 9000007533],
                    badgeText: "EXPLORATION"
                }}
            }};

            function renderRidgePlot(animated = true) {{
                const rect = svgEl.getBoundingClientRect();
                width = rect.width;
                height = rect.height;
                if (!width || !height) return;

                svg.attr('viewBox', `0 0 ${{width}} ${{height}}`);
                setupDefs();

                const isMobile = window.innerWidth < 1024;
                const focusInfo = STEP_FOCUS[currentStep] || STEP_FOCUS[0];

                // On mobile, show ONLY the 2-3 focused protagonist streets of the current act!
                // On desktop, show ALL official streets so the entire landscape is felt, highlighting the protagonists!
                const activeStreets = isMobile
                    ? streetData.filter(st => focusInfo.mobileIds.includes(st.id))
                    : (showCitizen ? streetData : streetData.filter(st => st.isOfficial));

                const numRows = activeStreets.length;
                const leftPad = isMobile ? 86 : 185;
                const rightPad = isMobile ? 10 : 28;
                const topPad = isMobile ? 12 : 36;
                const bottomPad = isMobile ? 22 : 48;

                // Scale X: 0 to 23 hours
                const xScale = d3.scaleLinear()
                    .domain([0, 23])
                    .range([leftPad, width - rightPad]);

                // Amplitude scale Z and Max Ridge Height with guaranteed headroom
                const isBikeMode = (currentMode === 'bikes' || currentStep === 4);
                const maxVolume = isBikeMode ? 52 : 920;
                
                // Crucial Joyplot Math: Ensure baselineY(0) has enough headroom so curve crests never clip!
                const maxRidgeHeight = isMobile
                    ? (numRows <= 2 ? 28 : 22)
                    : Math.min(Math.round((height - topPad - bottomPad) / (numRows * 0.7)), 88);

                const ampScale = d3.scaleLinear()
                    .domain([0, maxVolume])
                    .range([0, maxRidgeHeight]);

                // Baseline math: baseline(0) is offset by maxRidgeHeight + headroom so peak sits below topPad!
                const minBaseline = topPad + maxRidgeHeight + (isMobile ? 6 : 16);
                const maxBaseline = height - bottomPad - (isMobile ? 2 : 6);
                const rowGap = numRows > 1 ? (maxBaseline - minBaseline) / (numRows - 1) : 0;
                const baselineY = (idx) => numRows > 1 ? (minBaseline + idx * rowGap) : (minBaseline + (maxBaseline - minBaseline) / 2);

                // Area and Line Generators
                const areaGen = d3.area()
                    .x((d, i) => xScale(i))
                    .y0(d => baselineY(d.rowIndex))
                    .y1(d => baselineY(d.rowIndex) - ampScale(d.val))
                    .curve(d3.curveMonotoneX);

                const lineGen = d3.line()
                    .x((d, i) => xScale(i))
                    .y(d => baselineY(d.rowIndex) - ampScale(d.val))
                    .curve(d3.curveMonotoneX);

                // Clear dynamic layers
                svg.selectAll('.ridge-scene-layer').remove();
                const scene = svg.append('g').attr('class', 'ridge-scene-layer');

                // A. Background Guides: 8h and 17h Peak Vertical Guides
                const peakGuides = scene.append('g').attr('class', 'peak-guides');
                [8, 17].forEach(h => {{
                    const x = xScale(h);
                    peakGuides.append('line')
                        .attr('x1', x).attr('y1', topPad)
                        .attr('x2', x).attr('y2', height - bottomPad + 4)
                        .attr('stroke', '#334155')
                        .attr('stroke-dasharray', '3 3')
                        .attr('stroke-width', 1.0)
                        .attr('opacity', 0.55);

                    peakGuides.append('text')
                        .attr('x', x)
                        .attr('y', topPad + (isMobile ? 6 : 10))
                        .attr('fill', '#f59e0b')
                        .attr('font-size', isMobile ? '8.5px' : '10px')
                        .attr('font-weight', '800')
                        .attr('text-anchor', 'middle')
                        .text(h === 8 ? '08h' : '17h');
                }});

                // B. Render the Street Waves
                const gRows = scene.append('g').attr('class', 'ridge-rows-group');

                activeStreets.forEach((st, idx) => {{
                    const rowG = gRows.append('g')
                        .attr('class', `ridge-row row-${{st.id}}`)
                        .attr('data-id', st.id);

                    // 1. Baseline dashed guide
                    rowG.append('line')
                        .attr('x1', leftPad)
                        .attr('x2', width - rightPad)
                        .attr('y1', baselineY(idx))
                        .attr('y2', baselineY(idx))
                        .attr('stroke', '#1e293b')
                        .attr('stroke-dasharray', '2 2')
                        .attr('stroke-width', 0.8)
                        .attr('opacity', 0.7);

                    // 2. Left Typography Labels (Large, Crisp & Bold)
                    const labelG = rowG.append('g').attr('class', 'street-label');
                    const textY = baselineY(idx) - (isMobile ? 3 : 4);

                    const isFocusStreet = focusInfo.mobileIds.includes(st.id);
                    let labelColor = isFocusStreet ? '#fbbf24' : (st.isOfficial ? '#94a3b8' : '#c084fc');
                    if (currentStep === 2 && st.id === 9000007534) labelColor = '#f87171';
                    if (currentStep === 3 && st.id === 9000007530) labelColor = '#34d399';
                    if (currentStep === 4 && isBikeMode) labelColor = '#2dd4bf';

                    labelG.append('text')
                        .attr('x', leftPad - (isMobile ? 8 : 12))
                        .attr('y', textY)
                        .attr('fill', labelColor)
                        .attr('font-size', isMobile ? '12.5px' : (isFocusStreet ? '12px' : '10.5px'))
                        .attr('font-weight', isFocusStreet ? '800' : '600')
                        .attr('text-anchor', 'end')
                        .attr('letter-spacing', '-0.2px')
                        .text(isMobile ? st.shortName : st.displayName);

                    // Sub-label (Volume / Delta / V85)
                    let subText = "";
                    if (isMobile) {{
                        if (currentStep === 1 && st.id === 9000007492) subText = "580 v/h (08h)";
                        else if (currentStep === 2 && st.id === 9000007534) subText = "+70.7% report";
                        else if (currentStep === 3 && st.id === 9000007530) subText = "-66.9% transit";
                        else if (currentStep === 4) subText = `${{st.profiles.springBikes[17] || 15}} vélos/h`;
                        else if (currentStep === 5) subText = `V85: ${{st.v85}} km/h`;
                        else subText = `${{Math.round(st.dailyTotal / 1000)}}k v/j`;
                    }} else if (isFocusStreet) {{
                        const citizenTag = st.isOfficial ? ` • ${{st.locality}}` : ' • Capteur Citoyen';
                        subText = isBikeMode
                            ? `${{st.profiles.bikes[17] || 10}} vélos/h${{citizenTag}}`
                            : `${{st.dailyTotal.toLocaleString('fr-FR')}} v/j • ${{st.speedLimit}} km/h${{citizenTag}}`;
                    }}

                    if (subText) {{
                        labelG.append('text')
                            .attr('x', leftPad - (isMobile ? 8 : 12))
                            .attr('y', textY + (isMobile ? 12 : 11))
                            .attr('fill', isMobile ? (st.id === 9000007534 ? '#f87171' : (st.id === 9000007530 ? '#34d399' : '#94a3b8')) : '#64748b')
                            .attr('font-size', isMobile ? '9.5px' : '9px')
                            .attr('font-weight', '700')
                            .attr('text-anchor', 'end')
                            .text(subText);
                    }}

                    // 3. Determine active 24h curve values & aesthetics
                    let vals = st.profiles.cars;
                    let gradUrl = isFocusStreet ? (st.isArterial ? 'url(#grad-arterial)' : 'url(#grad-standard)') : 'none';
                    let strokeColor = isFocusStreet ? (st.isArterial ? '#fbbf24' : '#38bdf8') : '#334155';
                    let rowOpacity = isMobile ? 1.0 : (isFocusStreet ? 1.0 : 0.55);

                    if (isBikeMode) {{
                        vals = st.profiles.springBikes;
                        if (isFocusStreet) {{
                            gradUrl = 'url(#grad-bike)';
                            strokeColor = '#2dd4bf';
                        }}
                    }} else if (currentStep === 2) {{
                        // Step 2: Detour surge
                        if (st.id === 9000007534) {{ // Boulogne-Billancourt
                            vals = st.profiles.surgeCars;
                            gradUrl = 'url(#grad-surge)';
                            strokeColor = '#ef4444';
                            rowOpacity = 1.0;
                        }} else if (st.id === 9000007578) {{ // Rue de la Gare detour
                            vals = st.profiles.surgeCars;
                            gradUrl = 'url(#grad-arterial)';
                            strokeColor = '#f59e0b';
                            rowOpacity = 1.0;
                        }}
                    }} else if (currentStep === 3) {{
                        // Step 3: Calmed Zone 20
                        if (st.id === 9000007530) {{ // Place Communale
                            vals = st.profiles.calmCars;
                            gradUrl = 'url(#grad-calm)';
                            strokeColor = '#10b981';
                            rowOpacity = 1.0;
                        }}
                    }}

                    rowG.attr('opacity', rowOpacity);

                    const seriesData = vals.map(v => ({{ rowIndex: idx, val: v }}));

                    // 4. Area Path (with dark backdrop fill on non-focused rows to maintain Joyplot occlusion)
                    rowG.append('path')
                        .datum(seriesData)
                        .attr('class', 'ridge-area')
                        .attr('fill', isFocusStreet ? gradUrl : 'rgba(15, 23, 42, 0.85)')
                        .attr('d', areaGen);

                    // 5. Crest Stroke Path
                    rowG.append('path')
                        .datum(seriesData)
                        .attr('class', 'ridge-crest')
                        .attr('fill', 'none')
                        .attr('stroke', strokeColor)
                        .attr('stroke-width', isFocusStreet ? (isMobile ? 2.4 : 2.8) : 1.2)
                        .attr('filter', isFocusStreet ? 'url(#crest-glow)' : 'none')
                        .attr('d', lineGen);

                    // 6. Step Highlights & Badges
                    if (currentStep === 1 && st.id === 9000007492) {{
                        const peakX = xScale(8);
                        const peakY = baselineY(idx) - ampScale(vals[8]);
                        const badgeG = rowG.append('g').attr('class', 'apex-callout');

                        badgeG.append('circle')
                            .attr('cx', peakX).attr('cy', peakY)
                            .attr('r', isMobile ? 3.5 : 5)
                            .attr('fill', '#fbbf24')
                            .attr('stroke', '#ffffff')
                            .attr('stroke-width', 1.5);

                        const bW = isMobile ? 104 : 140;
                        const bH = isMobile ? 16 : 20;
                        const safeX = Math.max(leftPad + bW/2 + 2, Math.min(width - rightPad - bW/2 - 2, peakX));
                        const calloutText = badgeG.append('g')
                            .attr('transform', `translate(${{safeX}}, ${{peakY - (isMobile ? 17 : 24)}})`);
                        calloutText.append('rect')
                            .attr('x', -bW/2).attr('y', 0)
                            .attr('width', bW).attr('height', bH)
                            .attr('rx', 4)
                            .attr('fill', '#f59e0b')
                            .attr('stroke', '#ffffff')
                            .attr('stroke-width', 1);
                        calloutText.append('text')
                            .attr('x', 0).attr('y', isMobile ? 11 : 14)
                            .attr('fill', '#020617')
                            .attr('font-size', isMobile ? '8px' : '10px')
                            .attr('font-weight', '800')
                            .attr('text-anchor', 'middle')
                            .text('PIC MATIN : 580 V/H');
                    }} else if (currentStep === 2 && st.id === 9000007534) {{
                        const peakX = xScale(17);
                        const peakY = baselineY(idx) - ampScale(vals[17]);
                        const badgeG = rowG.append('g').attr('class', 'apex-callout');

                        badgeG.append('circle')
                            .attr('cx', peakX).attr('cy', peakY)
                            .attr('r', isMobile ? 3.5 : 5)
                            .attr('fill', '#ef4444')
                            .attr('stroke', '#ffffff')
                            .attr('stroke-width', 1.5);

                        const bW = isMobile ? 108 : 140;
                        const bH = isMobile ? 16 : 20;
                        const safeX = Math.max(leftPad + bW/2 + 2, Math.min(width - rightPad - bW/2 - 2, peakX));
                        const calloutText = badgeG.append('g')
                            .attr('transform', `translate(${{safeX}}, ${{peakY - (isMobile ? 17 : 24)}})`);
                        calloutText.append('rect')
                            .attr('x', -bW/2).attr('y', 0)
                            .attr('width', bW).attr('height', bH)
                            .attr('rx', 4)
                            .attr('fill', '#ef4444')
                            .attr('stroke', '#ffffff')
                            .attr('stroke-width', 1);
                        calloutText.append('text')
                            .attr('x', 0).attr('y', isMobile ? 11 : 14)
                            .attr('fill', '#ffffff')
                            .attr('font-size', isMobile ? '8px' : '10px')
                            .attr('font-weight', '800')
                            .attr('text-anchor', 'middle')
                            .text('DÉVIATION : +70.7%');
                    }} else if (currentStep === 3 && st.id === 9000007530) {{
                        const peakX = xScale(12);
                        const peakY = baselineY(idx) - ampScale(vals[12]);
                        const badgeG = rowG.append('g').attr('class', 'apex-callout');

                        badgeG.append('circle')
                            .attr('cx', peakX).attr('cy', peakY)
                            .attr('r', isMobile ? 3.5 : 5)
                            .attr('fill', '#10b981')
                            .attr('stroke', '#ffffff')
                            .attr('stroke-width', 1.5);

                        const bW = isMobile ? 104 : 140;
                        const bH = isMobile ? 16 : 20;
                        const safeX = Math.max(leftPad + bW/2 + 2, Math.min(width - rightPad - bW/2 - 2, peakX));
                        const calloutText = badgeG.append('g')
                            .attr('transform', `translate(${{safeX}}, ${{peakY - (isMobile ? 17 : 24)}})`);
                        calloutText.append('rect')
                            .attr('x', -bW/2).attr('y', 0)
                            .attr('width', bW).attr('height', bH)
                            .attr('rx', 4)
                            .attr('fill', '#10b981')
                            .attr('stroke', '#ffffff')
                            .attr('stroke-width', 1);
                        calloutText.append('text')
                            .attr('x', 0).attr('y', isMobile ? 11 : 14)
                            .attr('fill', '#ffffff')
                            .attr('font-size', isMobile ? '8px' : '10px')
                            .attr('font-weight', '800')
                            .attr('text-anchor', 'middle')
                            .text('ZONE 20 : -66.9%');
                    }} else if (currentStep === 4 && st.id === 9000007578) {{
                        const peakX = xScale(17);
                        const peakY = baselineY(idx) - ampScale(vals[17]);
                        const badgeG = rowG.append('g').attr('class', 'apex-callout');

                        badgeG.append('circle')
                            .attr('cx', peakX).attr('cy', peakY)
                            .attr('r', isMobile ? 3.5 : 5)
                            .attr('fill', '#2dd4bf')
                            .attr('stroke', '#ffffff')
                            .attr('stroke-width', 1.5);

                        const bW = isMobile ? 108 : 140;
                        const bH = isMobile ? 16 : 20;
                        const safeX = Math.max(leftPad + bW/2 + 2, Math.min(width - rightPad - bW/2 - 2, peakX));
                        const calloutText = badgeG.append('g')
                            .attr('transform', `translate(${{safeX}}, ${{peakY - (isMobile ? 17 : 24)}})`);
                        calloutText.append('rect')
                            .attr('x', -bW/2).attr('y', 0)
                            .attr('width', bW).attr('height', bH)
                            .attr('rx', 4)
                            .attr('fill', '#0f766e')
                            .attr('stroke', '#2dd4bf')
                            .attr('stroke-width', 1);
                        calloutText.append('text')
                            .attr('x', 0).attr('y', isMobile ? 11 : 14)
                            .attr('fill', '#ffffff')
                            .attr('font-size', isMobile ? '8px' : '10px')
                            .attr('font-weight', '800')
                            .attr('text-anchor', 'middle')
                            .text('RER : +194% VÉLOS');
                    }} else if (currentStep === 5) {{
                        const peakHour = 16;
                        const peakX = xScale(peakHour);
                        const peakY = baselineY(idx) - ampScale(vals[peakHour]);

                        const isSpeeding = st.v85 > st.speedLimit;
                        const vCol = st.speedLimit === 20 ? '#10b981' : (st.speedLimit === 30 && st.v85 <= 31 ? '#10b981' : (isSpeeding ? '#f87171' : '#38bdf8'));

                        const vBadge = rowG.append('g').attr('class', 'v85-badge');
                        const bW = isMobile ? 48 : 64;
                        const bH = isMobile ? 16 : 16;
                        const bX = peakX + (isMobile ? 2 : 10);
                        const bY = peakY - (isMobile ? 8 : 8);
                        vBadge.append('rect')
                            .attr('x', bX)
                            .attr('y', bY)
                            .attr('width', bW)
                            .attr('height', bH)
                            .attr('rx', 4)
                            .attr('fill', '#0f172a')
                            .attr('stroke', vCol)
                            .attr('stroke-width', 1.2);

                        vBadge.append('text')
                            .attr('x', bX + bW/2)
                            .attr('y', bY + (isMobile ? 11.5 : 12))
                            .attr('fill', vCol)
                            .attr('font-size', isMobile ? '8.5px' : '9.5px')
                            .attr('font-weight', '800')
                            .attr('text-anchor', 'middle')
                            .text(isMobile ? `${{st.v85}}k` : `${{st.v85}} km/h`);
                    }}
                }});
                // C. Horizontal Time Axis (0h to 23h)
                const timeAxisG = scene.append('g').attr('class', 'ridge-time-axis');
                const axisTicks = isMobile ? [0, 8, 12, 17, 23] : [0, 4, 8, 12, 17, 20, 23];

                axisTicks.forEach(h => {{
                    const x = xScale(h);
                    timeAxisG.append('line')
                        .attr('x1', x).attr('y1', height - bottomPad + 4)
                        .attr('x2', x).attr('y2', height - bottomPad + 10)
                        .attr('stroke', '#64748b')
                        .attr('stroke-width', 1);

                    const isPeak = (h === 8 || h === 17);
                    timeAxisG.append('text')
                        .attr('x', x)
                        .attr('y', height - bottomPad + (isMobile ? 20 : 22))
                        .attr('fill', isPeak ? '#fbbf24' : '#94a3b8')
                        .attr('font-size', isMobile ? '9px' : '10.5px')
                        .attr('font-weight', isPeak ? '800' : '500')
                        .attr('text-anchor', 'middle')
                        .text(`${{h}}h`);
                }});

                // D. Interactive Scrubber Guide & Overlay
                const scrubberG = scene.append('g').attr('id', 'scrubberGroup').style('opacity', 0);
                
                scrubberG.append('line')
                    .attr('id', 'scrubberLine')
                    .attr('y1', topPad - (isMobile ? 14 : 20))
                    .attr('y2', height - bottomPad + 8)
                    .attr('stroke', '#fbbf24')
                    .attr('stroke-width', 1.5)
                    .attr('stroke-dasharray', '4 3');

                const scrubberTag = scrubberG.append('g').attr('id', 'scrubberTag');
                scrubberTag.append('rect')
                    .attr('x', -30).attr('y', topPad - (isMobile ? 24 : 32))
                    .attr('width', 60).attr('height', isMobile ? 16 : 18)
                    .attr('rx', 4)
                    .attr('fill', '#fbbf24');
                scrubberTag.append('text')
                    .attr('id', 'scrubberTagText')
                    .attr('x', 0).attr('y', topPad - (isMobile ? 12 : 20))
                    .attr('fill', '#020617')
                    .attr('font-size', isMobile ? '8.5px' : '10px')
                    .attr('font-weight', '800')
                    .attr('text-anchor', 'middle')
                    .text('08h00');

                // Full Interactive Rect Overlay to capture Mouse & Touch
                scene.append('rect')
                    .attr('class', 'scrubber-overlay')
                    .attr('x', leftPad)
                    .attr('y', topPad - 20)
                    .attr('width', width - leftPad - rightPad)
                    .attr('height', height - topPad)
                    .attr('fill', 'transparent')
                    .style('cursor', 'crosshair')
                    .on('pointerdown', handlePointerMove)
                    .on('pointermove', handlePointerMove)
                    .on('pointerleave', handlePointerLeave)
                    .on('pointercancel', handlePointerLeave);

                function handlePointerMove(event) {{
                    const [mx, my] = d3.pointer(event, svgEl);
                    let hour = Math.round(xScale.invert(mx));
                    hour = Math.max(0, Math.min(23, hour));
                    activeScrubberHour = hour;

                    const curX = xScale(hour);
                    scrubberG.style('opacity', 1);
                    scrubberG.select('#scrubberLine').attr('x1', curX).attr('x2', curX);
                    scrubberTag.attr('transform', `translate(${{curX}}, 0)`);
                    scrubberG.select('#scrubberTagText').text(`${{hour < 10 ? '0' : ''}}${{hour}}h00`);

                    // Show detailed floating tooltip
                    const tooltipEl = document.getElementById('ridgeTooltip');
                    if (tooltipEl) {{
                        const topStreets = activeStreets.slice(0, isMobile ? 3 : 4).map(s => {{
                            const prof = isBikeMode ? s.profiles.springBikes : s.profiles.cars;
                            return `<div class="flex items-center justify-between gap-3 text-[11px] py-0.5">
                                <span class="text-slate-300 truncate max-w-[120px]">${{s.shortName}}</span>
                                <strong class="${{isBikeMode ? 'text-teal-300' : 'text-amber-400'}}">${{prof[hour] || 0}} ${{isBikeMode ? 'vélos/h' : 'véh./h'}}</strong>
                            </div>`;
                        }}).join('');

                        tooltipEl.innerHTML = `
                            <div class="border-b border-slate-700 pb-1 mb-1 flex items-center justify-between">
                                <span class="font-bold text-white">${{hour}}h00 • Débit</span>
                                <span class="text-[10px] text-amber-400 font-semibold">${{isBikeMode ? 'Vélos' : 'Trafic'}}</span>
                            </div>
                            <div>${{topStreets}}</div>
                        `;

                        // Tooltip positioning
                        if (isMobile) {{
                            tooltipEl.style.left = '50%';
                            tooltipEl.style.transform = 'translateX(-50%)';
                            tooltipEl.style.bottom = '10px';
                            tooltipEl.style.top = 'auto';
                        }} else {{
                            tooltipEl.style.transform = 'none';
                            tooltipEl.style.bottom = 'auto';
                            const ttX = Math.min(curX + 15, width - 240);
                            const ttY = Math.max(my - 70, 45);
                            tooltipEl.style.left = `${{Math.max(10, ttX)}}px`;
                            tooltipEl.style.top = `${{ttY}}}}px`;
                        }}
                        tooltipEl.style.opacity = '1';
                    }}
                }}

                function handlePointerLeave() {{
                    scrubberG.style('opacity', 0);
                    const tooltipEl = document.getElementById('ridgeTooltip');
                    if (tooltipEl) tooltipEl.style.opacity = '0';
                }}
            }}

            // 5. Expose mode switcher
            setRidgeMode = function(mode) {{
                currentMode = mode;
                const bAll = document.getElementById('btnModeAll');
                const bCars = document.getElementById('btnModeCars');
                const bBikes = document.getElementById('btnModeBikes');

                [bAll, bCars, bBikes].forEach(b => {{
                    if (b) b.className = "px-2.5 py-1 rounded-lg text-slate-300 hover:text-white transition cursor-pointer";
                }});

                if (mode === 'all') {{
                    if (bAll) bAll.className = "px-2.5 py-1 rounded-lg bg-amber-400 text-slate-950 transition cursor-pointer";
                }}
                if (mode === 'cars') {{
                    if (bCars) bCars.className = "px-2.5 py-1 rounded-lg bg-sky-500 text-white transition cursor-pointer";
                }}
                if (mode === 'bikes') {{
                    if (bBikes) bBikes.className = "px-2.5 py-1 rounded-lg bg-teal-500 text-white transition cursor-pointer";
                }}

                renderRidgePlot(true);
            }};

            // 6. Citizen Sensors Toggle Functionality
            toggleCitizenRidge = function() {{
                showCitizen = !showCitizen;
                updateCitizenToggleUI();
                renderRidgePlot(true);
                if (typeof window.syncDashboardScopeFromRidge === 'function') {{
                    window.syncDashboardScopeFromRidge(showCitizen ? 'all' : 'official');
                }}
            }};

            setRidgeCitizenScope = function(show) {{
                if (showCitizen !== show) {{
                    showCitizen = show;
                    updateCitizenToggleUI();
                    renderRidgePlot(true);
                }}
            }};

            window.toggleCitizenRidge = toggleCitizenRidge;
            window.setRidgeMode = setRidgeMode;
            window.setRidgeCitizenScope = setRidgeCitizenScope;

            function updateCitizenToggleUI() {{
                const btn = document.getElementById('btnToggleCitizenRidge');
                const icon = document.getElementById('iconToggleCitizen');
                const label = document.getElementById('labelToggleCitizen');
                const badge = document.getElementById('badgeCitizenCount');

                if (!btn) return;

                if (showCitizen) {{
                    btn.className = "glass-card px-2.5 py-1.5 rounded-xl border border-purple-500/60 bg-purple-950/60 text-purple-200 shadow-lg shadow-purple-950/40 transition flex items-center gap-1.5 cursor-pointer text-[11px] font-bold";
                    if (icon) icon.className = "fa-solid fa-check text-[10px] text-emerald-400";
                    if (label) label.textContent = "13 capteurs";
                    if (badge) {{
                        badge.textContent = "13";
                        badge.className = "text-[9px] px-1.5 py-0.2 rounded-full bg-purple-900 text-purple-200 font-bold border border-purple-600/50";
                    }}
                }} else {{
                    btn.className = "glass-card px-2.5 py-1.5 rounded-xl border border-white/15 text-slate-300 hover:text-white hover:border-amber-400/40 shadow-lg transition flex items-center gap-1.5 cursor-pointer text-[11px] font-bold";
                    if (icon) icon.className = "fa-solid fa-plus text-[10px] text-amber-400";
                    if (label) label.textContent = "3 Citoyens";
                    if (badge) {{
                        badge.textContent = "10";
                        badge.className = "text-[9px] px-1.5 py-0.2 rounded-full bg-slate-800 text-slate-400 font-normal border border-slate-700";
                    }}
                }}
            }}

            // 7. Setup Scrollytelling IntersectionObserver & Mobile Stepper
            let updateStepUI = function(stepIdx) {{}};

            function setupScrollytelling() {{
                const steps = document.querySelectorAll('.story-step');
                const badge = document.getElementById('visualSceneTitle');
                const chapterEl = document.getElementById('visualSceneChapter');
                const btnPrev = document.getElementById('btnPrevStepMob');
                const btnNext = document.getElementById('btnNextStepMob');
                const dots = document.querySelectorAll('#mobileStepDots .step-dot');

                updateStepUI = function(stepIdx) {{
                    currentStep = stepIdx;
                    window.currentStep = stepIdx;

                    // 1. Highlight active narrative card
                    steps.forEach((s, idx) => {{
                        if (idx === stepIdx) {{
                            s.classList.add('is-active');
                        }} else {{
                            s.classList.remove('is-active');
                        }}
                    }});

                    // 2. Update visual scene badge and chapter
                    const focusInfo = STEP_FOCUS[stepIdx] || STEP_FOCUS[0];
                    if (badge) {{
                        badge.textContent = focusInfo.title;
                    }}
                    if (chapterEl) {{
                        chapterEl.textContent = focusInfo.chapter;
                    }}

                    // 3. Auto-switch mode on step 4 (Vélos)
                    if (stepIdx === 4) {{
                        currentMode = 'bikes';
                    }} else {{
                        currentMode = 'all';
                    }}

                    // 4. Update mobile stepper buttons
                    if (btnPrev) {{
                        btnPrev.disabled = (stepIdx <= 0);
                    }}
                    if (btnNext) {{
                        btnNext.disabled = (stepIdx >= steps.length - 1);
                    }}

                    // 5. Update mobile step dots
                    if (dots && dots.length > 0) {{
                        dots.forEach((dot, idx) => {{
                            if (idx === stepIdx) {{
                                dot.className = "step-dot w-2.5 h-2.5 rounded-full bg-amber-400 shadow-sm shadow-amber-400/50 transition-all cursor-pointer";
                            }} else {{
                                dot.className = "step-dot w-1.5 h-1.5 rounded-full bg-slate-700 hover:bg-slate-500 transition-all cursor-pointer";
                            }}
                        }});
                    }}
                }};

                // Global function to navigate to a story step
                window.goToStoryStep = function(stepIdx) {{
                    if (typeof stepIdx === 'string') stepIdx = parseInt(stepIdx, 10);
                    if (isNaN(stepIdx)) stepIdx = 0;
                    stepIdx = Math.max(0, Math.min(steps.length - 1, stepIdx));

                    updateStepUI(stepIdx);
                    renderRidgePlot(true);

                    // Scroll target narrative card smoothly with exact viewport offset
                    const targetCard = document.querySelector('.story-step[data-step="' + stepIdx + '"]');
                    if (targetCard) {{
                        const isMobile = window.innerWidth < 1024;
                        if (isMobile) {{
                            const headerEl = document.querySelector('header');
                            const viewportEl = document.getElementById('stickyVisualViewport');
                            const headerH = headerEl ? headerEl.offsetHeight : 64;
                            const vpH = viewportEl ? viewportEl.offsetHeight : 240;
                            const offset = headerH + vpH + 16;
                            const targetY = targetCard.getBoundingClientRect().top + window.pageYOffset - offset;
                            window.scrollTo({{ top: Math.max(0, targetY), behavior: 'smooth' }});
                        }} else {{
                            targetCard.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
                        }}
                    }}
                }};
                goToStoryStep = window.goToStoryStep;

                // Responsive IntersectionObserver rootMargin
                const isMobile = window.innerWidth < 1024;
                const rootMarginVal = isMobile ? '-35% 0px -20% 0px' : '-25% 0px -25% 0px';

                const observer = new IntersectionObserver((entries) => {{
                    entries.forEach(entry => {{
                        if (entry.isIntersecting) {{
                            const stepIdx = parseInt(entry.target.getAttribute('data-step') || '0', 10);
                            if (currentStep !== stepIdx) {{
                                updateStepUI(stepIdx);
                                renderRidgePlot(true);
                            }}
                        }}
                    }});
                }}, {{
                    rootMargin: rootMarginVal,
                    threshold: 0.1
                }});

                steps.forEach(s => observer.observe(s));

                // Initialize step 0 UI (or deep linked step)
                const searchParams = new URLSearchParams(window.location.search);
                const initStepParam = parseInt(searchParams.get('step') || '0', 10);
                const safeInitStep = (!isNaN(initStepParam) && initStepParam >= 0 && initStepParam < steps.length) ? initStepParam : 0;
                updateStepUI(safeInitStep);
                if (safeInitStep > 0) {{
                    setTimeout(() => goToStoryStep(safeInitStep), 200);
                }}
            }}

            window.triggerRidgeResize = function() {{
                renderRidgePlot(false);
            }};

            // 8. Initialize
            window.addEventListener('DOMContentLoaded', () => {{
                renderRidgePlot(false);
                setupScrollytelling();
            }});

            window.addEventListener('resize', () => {{
                renderRidgePlot(false);
            }});

        }})();

        // ==========================================
        // 3. CITIZEN LABORATORY (24H SLIDER & CONTROLS)
        // ==========================================
        let sliderPlayInterval = null;
        const HOURLY_LABELS = [
            "00h00 — 01h00 (Nuit)", "01h00 — 02h00 (Nuit)", "02h00 — 03h00 (Nuit)", "03h00 — 04h00 (Nuit)",
            "04h00 — 05h00 (Premiers départs)", "05h00 — 06h00 (Montée matinale)", "06h00 — 07h00 (Pré-pointe)",
            "07h00 — 08h00 (Pointe Écoles & Bureaux)", "08h00 — 09h00 (Pointe du Matin)", "09h00 — 10h00 (Post-pointe)",
            "10h00 — 11h00 (Heures creuses)", "11h00 — 12h00 (Midi)", "12h00 — 13h00 (Pause méridienne)",
            "13h00 — 14h00 (Reprise)", "14h00 — 15h00 (Après-midi)", "15h00 — 16h00 (Sortie écoles primaire)",
            "16h00 — 17h00 (Pré-pointe du soir)", "17h00 — 18h00 (Grande Pointe du Soir)", "18h00 — 19h00 (Pointe de retour)",
            "19h00 — 20h00 (Décélération soirée)", "20h00 — 21h00 (Soirée)", "21h00 — 22h00 (Calme nocturne)",
            "22h00 — 23h00 (Nuit)", "23h00 — 00h00 (Nuit)"
        ];

        function onSliderHourChange(hourVal) {{
            const h = parseInt(hourVal, 10);
            const labelEl = document.getElementById('labelCurrentHour');
            const badgeEl = document.getElementById('badgeHourContext');
            if (labelEl) labelEl.textContent = HOURLY_LABELS[h];

            if (badgeEl) {{
                if (h >= 7 && h <= 9) {{
                    badgeEl.textContent = "Forte Affluence Navetteurs Matin";
                    badgeEl.className = "px-3 py-1 rounded-full bg-rose-500/20 text-rose-300 border border-rose-500/30 font-bold";
                }} else if (h >= 16 && h <= 18) {{
                    badgeEl.textContent = "Grande Pointe du Soir";
                    badgeEl.className = "px-3 py-1 rounded-full bg-amber-500/20 text-amber-300 border border-amber-500/30 font-bold";
                }} else if (h >= 22 || h <= 5) {{
                    badgeEl.textContent = "Trafic Nocturne Léger (Phares)";
                    badgeEl.className = "px-3 py-1 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 font-bold";
                }} else {{
                    badgeEl.textContent = "Régime Moyen Diurne";
                    badgeEl.className = "px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 font-bold";
                }}
            }}

            if (typeof window.updateMapHourly === 'function') {{
                window.updateMapHourly(h);
            }}
        }}

        function togglePlaySlider() {{
            const btn = document.getElementById('btnPlaySlider');
            const icon = document.getElementById('iconPlay');
            const slider = document.getElementById('slider24h');

            if (sliderPlayInterval) {{
                clearInterval(sliderPlayInterval);
                sliderPlayInterval = null;
                if (icon) {{ icon.className = "fa-solid fa-play ml-0.5"; }}
            }} else {{
                if (icon) {{ icon.className = "fa-solid fa-pause"; }}
                sliderPlayInterval = setInterval(() => {{
                    let cur = parseInt(slider.value, 10);
                    cur = (cur + 1) % 24;
                    slider.value = cur;
                    onSliderHourChange(cur);
                }}, 900);
            }}
        }}

        // ==========================================
        // 4. EMBEDDED DASHBOARD & CONTROLLER LOGIC
        // ==========================================
{ctrl_js_body}
    </script>
</body>
</html>
'''

with open('index.html', 'w', encoding='utf-8') as out:
    out.write(html_content)

print("Generated dual-tab index.html with complete Citizen Laboratory successfully!")
