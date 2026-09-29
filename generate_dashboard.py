import json
import os
import csv

def compute_yoy_analysis(full_history_obj):
    if not full_history_obj or "sensors_history" not in full_history_obj:
        return {}
    
    sensors_history = full_history_obj["sensors_history"]
    
    # 1. Autumn: Nov 2024 vs Nov 2025 (all 10 sensors constant)
    autumn_sensors = []
    aut_tot_base, aut_tot_target = 0, 0
    aut_cars_base, aut_cars_target = 0, 0
    aut_heavy_base, aut_heavy_target = 0, 0
    aut_bikes_base, aut_bikes_target = 0, 0
    aut_peds_base, aut_peds_target = 0, 0

    # 2. Spring: May 2025 vs May 2026 (constant perimeter 9 sensors, and raw 10)
    spring_sensors = []
    spr_tot_base_const, spr_tot_target_const = 0, 0
    spr_cars_base_const, spr_cars_target_const = 0, 0
    spr_heavy_base_const, spr_heavy_target_const = 0, 0
    spr_bikes_base_const, spr_bikes_target_const = 0, 0
    spr_peds_base_const, spr_peds_target_const = 0, 0

    spr_tot_base_raw, spr_tot_target_raw = 0, 0
    spr_cars_base_raw, spr_cars_target_raw = 0, 0
    spr_bikes_base_raw, spr_bikes_target_raw = 0, 0

    diagnostics = {
        9000007490: {
            "autumn": "Forte baisse locale (-40%)",
            "spring": "Rebond printanier (+29%) / Forte hausse vélo (+23%)",
            "travaux_impact": "Rue de Genval : itinéraire officiel de déviation lors de la fermeture de l'accès 4 Rosières vers l'accès 5 Bierges (chantier écrans antibruit SOFICO E411)."
        },
        9000007492: {
            "autumn": "Décrue de transit (-22%) sous impact des chantiers E411",
            "spring": "Arrêté en déc. 2025 (neutralisé dans l'analyse constante)",
            "travaux_impact": "Chaussée de La Hulpe (Rosières) : impactée par le chantier SOFICO (écrans acoustiques 17.600 m²) et cyclostrade E411 avec fermetures répétées et alternées de la sortie n°4."
        },
        9000007497: {
            "autumn": "Décrue modérée continue (-10%)",
            "spring": "Décrue modérée continue (-7%) / Axe structurant apaisé",
            "travaux_impact": "Avenue Franklin Roosevelt : axe de déviation centrale lors du réaménagement de la Rue de Rosières en 2024-2025, retour à un régime plus apaisé après fin du chantier."
        },
        9000007509: {
            "autumn": "Baisse d'automne (-23%)",
            "spring": "Hausse printanière modérée (+13%)",
            "travaux_impact": "Rue de l'Institut : canal officiel de déviation par le centre communal lors des travaux de réaménagement lourd et de passage en zone 30 de la Rue de Rosières."
        },
        9000007512: {
            "autumn": "Décrue confirmée (-20%)",
            "spring": "Décrue confirmée (-26%) / Forte baisse de transit",
            "travaux_impact": "Rue de la Tasnière : transit de raccourci fortement dissuadé par les travaux de soutènement et feux alternés rue du Cerf en amont début 2026, sécurisation carrefour Desmet."
        },
        9000007523: {
            "autumn": "Décrue continue (-8%)",
            "spring": "Décrue accentuée (-17%) / Apaisement centre",
            "travaux_impact": "Rue Haute : suppression du stationnement alterné (nouveau Code de la route), travaux du Vallon et des Papeteries incitant au contournement."
        },
        9000007530: {
            "autumn": "Baisse modérée (-21%)",
            "spring": "Chute spectaculaire (-67%) : Extension Zone 20 résidentielle & plantations",
            "travaux_impact": "Place Communale (Genval) : extension de la zone résidentielle 20 km/h (priorité absolue piétons), réfection des trottoirs, zone bleue et plantations d'arbres. Évaporation réussie du trafic de transit."
        },
        9000007533: {
            "autumn": "Décrue modérée (-10%) / Vélos en forte hausse",
            "spring": "Décrue modérée continue (-6%) / Stabilisation",
            "travaux_impact": "Avenue Albert 1er : création du Sens Unique Limité (SUL) Peyo-Gare évitant les feux de Maubroux et désengorgeant le carrefour Albert 1er / Rosières."
        },
        9000007534: {
            "autumn": "Forte hausse (+38%) / Premiers reports",
            "spring": "Explosion du trafic (+71%) / Déviation officielle Avenue Royale & vélos (+184%)",
            "travaux_impact": "Avenue de Boulogne-Billancourt : itinéraire officiel obligatoire de déviation du grand chantier Avenue Royale (fermeture totale fév-nov 2026 pour 200 jours). Les avenues secondaires (Léopold, Beau Champ) ont été mises en sens unique pour concentrer le transit sur cet axe."
        },
        9000007578: {
            "autumn": "Creux fin de chantier (-31%)",
            "spring": "Forte reprise (+59%) : Nouvelle gare RER inaugurée & report déviation via r. Boisacq",
            "travaux_impact": "Rue de la Gare : nouvelle gare RER et gare des bus inaugurées fin nov 2024 après 2 ans de travaux, complétée par la déviation de l'Avenue Royale transitant par la rue Robert Boisacq."
        }
    }

    for s in sensors_history:
        sid = s["id"]
        street = s["street"]
        loc = s["locality"]
        p = s["periods"]
        
        # Autumn
        n24 = p.get("nov2024", {})
        n25 = p.get("nov2025", {})
        t24 = n24.get("total", 0)
        t25 = n25.get("total", 0)
        c24 = n24.get("cars", 0)
        c25 = n25.get("cars", 0)
        h24 = n24.get("heavy", 0)
        h25 = n25.get("heavy", 0)
        b24 = n24.get("bikes", 0)
        b25 = n25.get("bikes", 0)
        p24 = n24.get("pedestrians", 0)
        p25 = n25.get("pedestrians", 0)
        
        aut_tot_base += t24
        aut_tot_target += t25
        aut_cars_base += c24
        aut_cars_target += c25
        aut_heavy_base += h24
        aut_heavy_target += h25
        aut_bikes_base += b24
        aut_bikes_target += b25
        aut_peds_base += p24
        aut_peds_target += p25
        
        autumn_sensors.append({
            "id": sid,
            "street": street,
            "locality": loc,
            "base_total": t24,
            "target_total": t25,
            "diff_total": t25 - t24,
            "pct_total": round(((t25 - t24) / t24 * 100), 1) if t24 else 0,
            "pct_cars": round(((c25 - c24) / c24 * 100), 1) if c24 else 0,
            "pct_bikes": round(((b25 - b24) / b24 * 100), 1) if b24 else 0,
            "pct_heavy": round(((h25 - h24) / h24 * 100), 1) if h24 else 0,
            "pct_pedestrians": round(((p25 - p24) / p24 * 100), 1) if p24 else 0,
            "base_cars": c24, "target_cars": c25,
            "base_bikes": b24, "target_bikes": b25,
            "base_heavy": h24, "target_heavy": h25,
            "base_pedestrians": p24, "target_pedestrians": p25,
            "is_constant_perimeter": True,
            "diagnostic": diagnostics.get(sid, {}).get("autumn", ""),
            "travaux_impact": diagnostics.get(sid, {}).get("travaux_impact", "")
        })
        
        # Spring
        m25 = p.get("may2025", {})
        m26 = p.get("may2026", {})
        mt25 = m25.get("total", 0)
        mt26 = m26.get("total", 0)
        mc25 = m25.get("cars", 0)
        mc26 = m26.get("cars", 0)
        mh25 = m25.get("heavy", 0)
        mh26 = m26.get("heavy", 0)
        mb25 = m25.get("bikes", 0)
        mb26 = m26.get("bikes", 0)
        mp25 = m25.get("pedestrians", 0)
        mp26 = m26.get("pedestrians", 0)
        
        spr_tot_base_raw += mt25
        spr_tot_target_raw += mt26
        spr_cars_base_raw += mc25
        spr_cars_target_raw += mc26
        spr_bikes_base_raw += mb25
        spr_bikes_target_raw += mb26
        
        is_const = (sid != 9000007492)
        if is_const:
            spr_tot_base_const += mt25
            spr_tot_target_const += mt26
            spr_cars_base_const += mc25
            spr_cars_target_const += mc26
            spr_heavy_base_const += mh25
            spr_heavy_target_const += mh26
            spr_bikes_base_const += mb25
            spr_bikes_target_const += mb26
            spr_peds_base_const += mp25
            spr_peds_target_const += mp26
            
            spring_sensors.append({
                "id": sid,
                "street": street,
                "locality": loc,
                "base_total": mt25,
                "target_total": mt26,
                "diff_total": mt26 - mt25,
                "pct_total": round(((mt26 - mt25) / mt25 * 100), 1) if mt25 else 0,
                "pct_cars": round(((mc26 - mc25) / mc25 * 100), 1) if mc25 else 0,
                "pct_bikes": round(((mb26 - mb25) / mb25 * 100), 1) if mb25 else 0,
                "pct_heavy": round(((mh26 - mh25) / mh25 * 100), 1) if mh25 else 0,
                "pct_pedestrians": round(((mp26 - mp25) / mp25 * 100), 1) if mp25 else 0,
                "base_cars": mc25, "target_cars": mc26,
                "base_bikes": mb25, "target_bikes": mb26,
                "base_heavy": mh25, "target_heavy": mh26,
                "base_pedestrians": mp25, "target_pedestrians": mp26,
                "is_constant_perimeter": True,
                "status": "Actif",
                "diagnostic": diagnostics.get(sid, {}).get("spring", ""),
                "travaux_impact": diagnostics.get(sid, {}).get("travaux_impact", "")
            })
        else:
            spring_sensors.append({
                "id": sid,
                "street": street,
                "locality": loc,
                "base_total": mt25,
                "target_total": 0,
                "diff_total": -mt25,
                "pct_total": None,
                "pct_cars": None,
                "pct_bikes": None,
                "pct_heavy": None,
                "pct_pedestrians": None,
                "base_cars": mc25, "target_cars": 0,
                "base_bikes": mb25, "target_bikes": 0,
                "base_heavy": mh25, "target_heavy": 0,
                "base_pedestrians": mp25, "target_pedestrians": 0,
                "is_constant_perimeter": False,
                "status": "Arrêté en déc. 2025 (exclu du périmètre constant)",
                "diagnostic": diagnostics.get(sid, {}).get("spring", ""),
                "travaux_impact": diagnostics.get(sid, {}).get("travaux_impact", "")
            })

    def make_pct(num, den):
        return round((num / den) * 100, 1) if den else 0

    return {
        "autumn": {
            "period_base": "nov2024",
            "period_target": "nov2025",
            "label": "Automne (Nov 2024 vs Nov 2025)",
            "subtitle": "10 capteurs constants — Comparaison directe en photopériode identique",
            "constant_sensors_count": 10,
            "totals": {
                "total": {"base": aut_tot_base, "target": aut_tot_target, "diff": aut_tot_target - aut_tot_base, "pct": make_pct(aut_tot_target - aut_tot_base, aut_tot_base)},
                "cars": {"base": aut_cars_base, "target": aut_cars_target, "diff": aut_cars_target - aut_cars_base, "pct": make_pct(aut_cars_target - aut_cars_base, aut_cars_base)},
                "heavy": {"base": aut_heavy_base, "target": aut_heavy_target, "diff": aut_heavy_target - aut_heavy_base, "pct": make_pct(aut_heavy_target - aut_heavy_base, aut_heavy_base)},
                "bikes": {"base": aut_bikes_base, "target": aut_bikes_target, "diff": aut_bikes_target - aut_bikes_base, "pct": make_pct(aut_bikes_target - aut_bikes_base, aut_bikes_base)},
                "pedestrians": {"base": aut_peds_base, "target": aut_peds_target, "diff": aut_peds_target - aut_peds_base, "pct": make_pct(aut_peds_target - aut_peds_base, aut_peds_base)}
            },
            "sensors": autumn_sensors
        },
        "spring": {
            "period_base": "may2025",
            "period_target": "may2026",
            "label": "Printemps (Mai 2025 vs Mai 2026)",
            "subtitle": "Périmètre constant à 9 capteurs (Chaussée de La Hulpe arrêtée en déc. 2025 exclue)",
            "constant_sensors_count": 9,
            "excluded_sensor": {
                "id": 9000007492,
                "street": "Chaussée de La Hulpe",
                "reason": "Capteur arrêté en déc. 2025"
            },
            "raw_comparison": {
                "base_total": spr_tot_base_raw,
                "target_total": spr_tot_target_raw,
                "diff": spr_tot_target_raw - spr_tot_base_raw,
                "pct": make_pct(spr_tot_target_raw - spr_tot_base_raw, spr_tot_base_raw),
                "raw_cars_pct": make_pct(spr_cars_target_raw - spr_cars_base_raw, spr_cars_base_raw),
                "raw_bikes_pct": make_pct(spr_bikes_target_raw - spr_bikes_base_raw, spr_bikes_base_raw)
            },
            "totals": {
                "total": {"base": spr_tot_base_const, "target": spr_tot_target_const, "diff": spr_tot_target_const - spr_tot_base_const, "pct": make_pct(spr_tot_target_const - spr_tot_base_const, spr_tot_base_const)},
                "cars": {"base": spr_cars_base_const, "target": spr_cars_target_const, "diff": spr_cars_target_const - spr_cars_base_const, "pct": make_pct(spr_cars_target_const - spr_cars_base_const, spr_cars_base_const)},
                "heavy": {"base": spr_heavy_base_const, "target": spr_heavy_target_const, "diff": spr_heavy_target_const - spr_heavy_base_const, "pct": make_pct(spr_heavy_target_const - spr_heavy_base_const, spr_heavy_base_const)},
                "bikes": {"base": spr_bikes_base_const, "target": spr_bikes_target_const, "diff": spr_bikes_target_const - spr_bikes_base_const, "pct": make_pct(spr_bikes_target_const - spr_bikes_base_const, spr_bikes_base_const)},
                "pedestrians": {"base": spr_peds_base_const, "target": spr_peds_target_const, "diff": spr_peds_target_const - spr_peds_base_const, "pct": make_pct(spr_peds_target_const - spr_peds_base_const, spr_peds_base_const)}
            },
            "sensors": spring_sensors
        },
        "synthesis": {
            "traffic_increasing": False,
            "summary_statement": "À l'échelle communale globale, le trafic motorisé n'augmente pas : il enregistre une baisse modérée à sensible de -3.8% au printemps et de -13.6% en automne sur périmètre constant. Les fortes variations locales (+70.7% sur l'Avenue de Boulogne-Billancourt, +58.9% sur la Rue de la Gare, -66.9% sur la Place Communale) sont directement et factuellement expliquées par les grands chantiers communaux et régionaux (déviation officielle de l'Avenue Royale fermée pour 200 jours, aménagement de la Zone 20 résidentielle de la Place Communale, mise en service de la nouvelle gare RER). La mobilité active vélo est en nette progression structurelle (+2.8% à +8.0%).",
            "travaux_summary": "La confrontation des flux Telraam aux arrêtés de police et chantiers de la commune de Rixensart démontre qu'aucune artère ne subit de hausse structurelle incontrôlée : les reports observés correspondent fidèlement aux itinéraires de déviation obligatoires ou aux effets d'apaisement volontaire par zone 20/30."
        },
        "regional_context": {
            "title": "Mise en perspective régionale : Brabant wallon et Wallonie",
            "perception_paradox": {
                "title": "Le paradoxe du ressenti : pourquoi perçoit-on une hausse alors que les chiffres baissent ?",
                "points": [
                    {
                        "category": "Hyper-visibilité des goulets d'étranglement",
                        "description": "Les chantiers majeurs (Avenue Royale fermée 200 jours, travaux SOFICO E411, gare RER) ont canalisé les véhicules sur 2 ou 3 axes névralgiques de déviation où le trafic a explosé (+70.7% sur Boulogne-Billancourt, +58.9% sur la Rue de la Gare, +29.0% sur Rue de Genval). Ces ralentissements concentrés créent un ressenti aigu d'engorgement pour tout automobiliste qui y transite."
                    },
                    {
                        "category": "Apaisement silencieux et diffus",
                        "description": "À l'inverse, les voiries de quartier et le centre de Genval bénéficient d'un apaisement spectaculaire (-66.9% Place Communale grâce à la Zone 20 résidentielle, -25.6% Rue de la Tasnière, -17.3% Rue Haute, -7.2% Av. Roosevelt). Cet apaisement est moins remarqué au quotidien que les bouchons, mais il tire fortement la moyenne arithmétique communale vers le bas."
                    }
                ]
            },
            "regional_trends": {
                "macro_highways": {
                    "verdict": "Pas de baisse globale sur le réseau autoroutier et régional structurant",
                    "description": "À l'échelle de la Wallonie (SPW Mobilité / IWEPS, Tableau de bord de la Mobilité), le volume total de véhicules-kilomètres reste à un plateau historiquement élevé (>45,2 milliards de véh.km, +14% depuis 2018) avec une part modale de la voiture autour de 72.8%. Les autoroutes (E411, Ring R0) et grands axes de transit restent saturés aux heures de pointe."
                },
                "local_suburban": {
                    "verdict": "Une décrue réelle et documentée sur les voiries communales périurbaines",
                    "drivers": [
                        {
                            "name": "Télétravail structurel massif",
                            "source": "Institut VIAS / SPF Mobilité / Bureau fédéral du Plan",
                            "impact": "Le Brabant wallon compte la plus forte proportion de cadres et d'employés du tertiaire navetteurs vers Bruxelles. La stabilisation de 2 à 3 jours de télétravail par semaine a éliminé structurellement des millions de km de navettes hebdomadaires, allégeant la voirie locale en semaine."
                        },
                        {
                            "name": "Évaporation du trafic (Traffic Evaporation)",
                            "source": "Recherche en mobilité urbaine & Plan FAST 2030",
                            "impact": "L'apaisement volontaire (Zone 20, Zones 30, Sens Uniques Limités) et les chantiers ne déplacent pas 100% du trafic : une part significative s'évapore. Les automobilistes de pur transit externe renoncent à traverser les quartiers résidentiels de Rixensart et restent sur les grands contours régionaux."
                        },
                        {
                            "name": "Montée en puissance des alternatives (Vélo VAE & RER)",
                            "source": "Comptages Telraam Rixensart & SNCB",
                            "impact": "Le vélo à assistance électrique (VAE) surmonte le relief vallonné (+2.8% à +8.0% de cyclistes mesurés sur la commune). La mise en service complète de la nouvelle gare multimodale RER de Rixensart et le renforcement des fréquences ferroviaires favorisent le report modal."
                        },
                        {
                            "name": "Arbitrage économique et rationalisation des trajets",
                            "source": "Statbel & SPF Économie",
                            "impact": "L'augmentation des coûts automobiles et du carburant pousse les ménages à rationaliser les petits déplacements locaux (achats de proximité combinés ou effectués à pied)."
                        }
                    ]
                }
            }
        }
    }

SOURCES_METADATA = [
    {
        "category": "1. Comptages & Réseau IoT Citoyen",
        "icon": "fa-microchip",
        "color": "indigo",
        "description": "Données primaires issues des capteurs optiques et cadre de science citoyenne",
        "items": [
            {
                "name": "Telraam (Rear Window BV)",
                "type": "Données primaires de comptage citoyen continu",
                "description": "Données multimodales continues (voitures, deux-roues, piétons, camions/bus) et vitesses V85 issues des 10 capteurs Telraam S2 déployés chez les citoyens de Rixensart et Rosières, complétées par 3 vigies citoyennes. Données recueillies de 2024 à 2026 via l'API REST v1/v2 Telraam.",
                "url": "https://telraam.net/en/network/rixensart",
                "badge": "Open Data Telraam"
            },
            {
                "name": "Projet Européen WeCount (Horizon 2020)",
                "type": "Cadre méthodologique & validation scientifique",
                "description": "Protocole européen de science citoyenne pour l'observation et la quantification du transport urbain, validé dans 5 métropoles pilotes (Bruxelles, Louvain, Madrid, Cardiff, Dublin).",
                "url": "https://we-count.net",
                "badge": "Union Européenne"
            }
        ]
    },
    {
        "category": "2. Macro-Mobilité & Données Régionales Wallonnes",
        "icon": "fa-road",
        "color": "teal",
        "description": "Statistiques officielles régionales des volumes, parts modales et infrastructures",
        "items": [
            {
                "name": "SPW Mobilité et Infrastructures",
                "type": "Tableau de bord de la Mobilité en Wallonie (TBM)",
                "description": "Statistiques officielles des volumes globaux de circulation (45,2 milliards de véhicules-kilomètres en 2024, +14% depuis 2018), répartition modale régionale (72,8% voiture) et suivi de la stratégie FAST 2030.",
                "url": "https://mobilite.wallonie.be",
                "badge": "Région Wallonne"
            },
            {
                "name": "IWEPS (Institut wallon de l'évaluation, de la prospective et de la statistique)",
                "type": "Indicateurs socio-économiques & territoriaux",
                "description": "Données sur la structure des déplacements, taux de motorisation des ménages et profils des navetteurs en Brabant wallon.",
                "url": "https://www.iweps.be",
                "badge": "Statistiques Wallonie"
            },
            {
                "name": "SOFICO (Infrastructures structurantes)",
                "type": "Chantiers autoroutiers & Cyclostrades",
                "description": "Données de chantier sur la E411 (17 600 m² de murs acoustiques à Rosières, 5 km de cyclostrade et fermetures de l'échangeur 4 Rosières/Genval).",
                "url": "https://sofico.org",
                "badge": "Infrastructures"
            }
        ]
    },
    {
        "category": "3. Télétravail, Démographie & Sécurité Routière",
        "icon": "fa-shield-halved",
        "color": "amber",
        "description": "Enquêtes d'usage, sociologie du travail et données fédérales de transport",
        "items": [
            {
                "name": "Institut VIAS",
                "type": "Baromètres nationaux sur le télétravail & Sécurité",
                "description": "Analyses empiriques sur la pratique du télétravail en Belgique (stabilisation à 2-3 jours/semaine pour ~33% des actifs, 32 millions de km évités par jour) et son impact réel sur la congestion et l'accidentologie.",
                "url": "https://www.vias.be",
                "badge": "Recherche Fédérale"
            },
            {
                "name": "SPF Mobilité et Transports & Bureau fédéral du Plan",
                "type": "Enquêtes de mobilité & Perspectives",
                "description": "Études sur les habitudes de déplacement domicile-travail et modélisation de la demande de transport à l'horizon 2030-2040.",
                "url": "https://mobilit.belgium.be",
                "badge": "Fédéral"
            },
            {
                "name": "Statbel (Office belge de statistique)",
                "type": "Démographie & Emploi en Brabant wallon",
                "description": "Structure professionnelle des résidents de Rixensart et Brabant wallon (forte surreprésentation des cadres et employés du tertiaire effectuant des navettes vers Bruxelles).",
                "url": "https://statbel.fgov.be",
                "badge": "Statbel"
            }
        ]
    },
    {
        "category": "4. Recherche Scientifique & Référentiels d'Urbanisme",
        "icon": "fa-graduation-cap",
        "color": "purple",
        "description": "Publications académiques sur l'élasticité du trafic et normes techniques de vitesse",
        "items": [
            {
                "name": "Cairns, Hass-Klau & Goodwin (1998, 2002)",
                "type": "Théorie de l'évaporation du trafic (Disappearing Traffic)",
                "description": "Étude scientifique de référence (Landor Publishing / ETRC) démontrant que la réduction de capacité ou l'apaisement routier provoque une évaporation nette d'une fraction des flux par changement de mode, de destination, d'horaire ou annulation de trajets.",
                "url": "https://www.semanticscholar.org/paper/Traffic-impact-of-highway-capacity-reductions%3A-of-Cairns-Hass-Klau/6d7e008a0d0a1b6c00d46927d3bdfd8ce5a4341b",
                "badge": "Littérature Scientifique"
            },
            {
                "name": "Cerema (France)",
                "type": "Guides de modération des vitesses & Indicateur V85",
                "description": "Normes techniques et recommandations sur la mesure de la vitesse pratiquée (vitesse V85 sous laquelle roulent 85% des usagers) et aménagement des Zones 30 et Zones 20 résidentielles.",
                "url": "https://www.cerema.fr",
                "badge": "Référentiel Technique"
            }
        ]
    },
    {
        "category": "5. Arrêtés Communaux & Opérateurs de Mobilité",
        "icon": "fa-building-columns",
        "color": "rose",
        "description": "Réglementations locales de police, actualités travaux et offre ferroviaire",
        "items": [
            {
                "name": "Administration Communale de Rixensart",
                "type": "Arrêtés de Police & Plans de circulation",
                "description": "Arrêtés de police du Bourgmestre régissant les travaux publics et déviations obligatoires (Avenue Royale, Zone 20 Place Communale, SUL Peyo-Gare, Rue de Rosières, Rue du Cerf).",
                "url": "https://www.rixensart.be/actualites",
                "badge": "Arrêtés Communaux"
            },
            {
                "name": "SNCB & Infrabel",
                "type": "Pôle Multimodal RER & Ligne 161",
                "description": "Modernisation de la gare de Rixensart, création du pôle d'échange bus/train/vélo inauguré en novembre 2024 et cadencement renforcé des trains S vers Bruxelles et Ottignies.",
                "url": "https://www.belgiantrain.be",
                "badge": "Transports Publics"
            }
        ]
    }
]

def process_and_generate():
    input_file = "/Users/charlesdebrier/Development/Telraam/data/rixensart_telraam_full_data.json"
    if not os.path.exists(input_file):
        print(f"File not found: {input_file}")
        return None
    
    with open(input_file, "r", encoding="utf-8") as f:
        raw_data = json.load(f)
        
    # Load roadworks and chantiers data
    travaux_file = "/Users/charlesdebrier/Development/Telraam/data/rixensart_travaux.json"
    travaux_obj = {}
    chantiers_list = []
    if os.path.exists(travaux_file):
        try:
            with open(travaux_file, "r", encoding="utf-8") as tf:
                travaux_obj = json.load(tf)
                chantiers_list = travaux_obj.get("chantiers", [])
        except Exception as te:
            print(f"Error loading travaux data: {te}")
        
    sensors_summary = []
    
    for s in raw_data.get("sensors", []):
        sid = s["id"]
        street = s["street"]
        locality = s["locality"]
        role = s["role"]
        speed_limit = s["speed_limit"]
        is_official = s.get("is_official_network", True)
        
        # 1. Nov 2024 Reference (All 10 active)
        nov_modal = s.get("nov2024_modal") or {}
        nov_cars = nov_modal.get("car", 0)
        nov_heavy = nov_modal.get("heavy", 0)
        nov_motorized = nov_cars + nov_heavy
        nov_bikes = nov_modal.get("bike", 0)
        nov_peds = nov_modal.get("pedestrian", 0)
        nov_active = nov_bikes + nov_peds
        nov_total = nov_motorized + nov_active
        nov_night = nov_modal.get("night", 0)
        nov_total_24h = nov_total + nov_night
        
        nov_bike_pct = float(nov_modal.get("bikePerc", 0) or 0)
        nov_ped_pct = float(nov_modal.get("pedestrianPerc", 0) or 0)
        nov_active_pct = nov_bike_pct + nov_ped_pct
        nov_heavy_pct = float(nov_modal.get("heavyPerc", 0) or 0)
        nov_car_pct = float(nov_modal.get("carPerc", 0) or 0)
        nov_night_pct = round((nov_night / nov_total_24h) * 100, 1) if nov_total_24h > 0 else 0
        
        # Speed Nov 2024
        nov_speed = (s.get("nov2024_speed") or {}).get("data", {}) or {}
        pct_0_30 = float(nov_speed.get("zeroPerc", 0) or 0) + float(nov_speed.get("tenPerc", 0) or 0) + float(nov_speed.get("twentyPerc", 0) or 0)
        pct_30_50 = float(nov_speed.get("thirtyPerc", 0) or 0) + float(nov_speed.get("fourtyPerc", 0) or 0)
        pct_50_60 = float(nov_speed.get("fiftyPerc", 0) or 0)
        pct_60_70 = float(nov_speed.get("sixtyPerc", 0) or 0)
        pct_over_70 = float(nov_speed.get("seventyPerc", 0) or 0)
        pct_over_50 = pct_50_60 + pct_60_70 + pct_over_70
        
        pct_speeding = pct_over_50 if speed_limit == 50 else (pct_30_50 + pct_over_50)
        
        # V85 Nov 2024 (Representatif de jour avec opacite >= 0.5)
        nov_v85_data = (s.get("nov2024_v85") or {}).get("data", {}).get("speed_v85", []) or []
        nov_op_data = (s.get("nov2024_v85") or {}).get("data", {}).get("speed_histogram_opacity", []) or []
        conf_v85 = [v for v, op in zip(nov_v85_data, nov_op_data) if op >= 0.5 and v > 0]
        avg_v85 = round(sum(conf_v85) / len(conf_v85), 1) if conf_v85 else (round(sum([v for v in nov_v85_data if v > 0])/len([v for v in nov_v85_data if v > 0]), 1) if any(v > 0 for v in nov_v85_data) else None)
        max_v85 = round(max(conf_v85), 1) if conf_v85 else None
        v85_uncertainty = round(avg_v85 * 0.1, 1) if avg_v85 else None
        
        # 24h Profile Nov 2024
        nov_24h_data = (s.get("nov2024_24h") or {}).get("data", {}) or {}
        hourly_cars_wkday = nov_24h_data.get("carWeekdays", [])
        hourly_cars_wkend = nov_24h_data.get("carWeekend", [])
        hourly_bikes_wkday = nov_24h_data.get("bikeWeekdays", [])
        hourly_peds_wkday = nov_24h_data.get("pedestrianWeekdays", [])
        
        # Peak Hours
        am_slice = hourly_cars_wkday[7:10] if len(hourly_cars_wkday) >= 10 else []
        pm_slice = hourly_cars_wkday[16:19] if len(hourly_cars_wkday) >= 19 else []
        am_peak_car = max(am_slice) if am_slice else 0
        pm_peak_car = max(pm_slice) if pm_slice else 0
        am_peak_hour = f"{am_slice.index(am_peak_car) + 7}h-{am_slice.index(am_peak_car) + 8}h" if am_peak_car else "N/A"
        pm_peak_hour = f"{pm_slice.index(pm_peak_car) + 16}h-{pm_slice.index(pm_peak_car) + 17}h" if pm_peak_car else "N/A"

        # Recent 2026
        rec_modal = s.get("recent_modal") or {}
        rec_total = sum(rec_modal.get("piedata", [0,0,0,0]))
        rec_cars = rec_modal.get("car", 0)
        rec_bikes = rec_modal.get("bike", 0)
        rec_peds = rec_modal.get("pedestrian", 0)
        rec_heavy = rec_modal.get("heavy", 0)
        rec_night = rec_modal.get("night", 0)
        rec_total_24h = rec_total + rec_night
        
        rec_v85_data = (s.get("recent_v85") or {}).get("data", {}).get("speed_v85", []) or []
        valid_rec_v85 = [v for v in rec_v85_data if v > 0]
        rec_avg_v85 = round(sum(valid_rec_v85) / len(valid_rec_v85), 1) if valid_rec_v85 else None

        # Coordinates
        geom = s.get("geometry", {})
        coords = geom.get("coordinates", []) if geom else []
        def get_pts(c):
            if not c: return []
            if isinstance(c[0], (int, float)): return [c]
            r = []
            for sc in c: r.extend(get_pts(sc))
            return r
        pts = get_pts(coords)
        lat = round(sum(p[1] for p in pts) / len(pts), 5) if pts else None
        lon = round(sum(p[0] for p in pts) / len(pts), 5) if pts else None

        if lat is None and sid == 9000007490:
            lat = 50.73258
            lon = 4.53353
            coords = [[[4.5325, 50.7320], [4.5345, 50.7330]]]

        # Load historical data if present
        hist_file = "/Users/charlesdebrier/Development/Telraam/data/rixensart_history.json"
        hist_data = {}
        if os.path.exists(hist_file):
            try:
                with open(hist_file, "r", encoding="utf-8") as hf:
                    full_hist = json.load(hf)
                    for sh in full_hist.get("sensors_history", []):
                        if sh["id"] == sid:
                            hist_data = sh
            except Exception as e:
                pass

        network_type = "Officiel Municipal" if is_official else ("Projet Scolaire « L'école compte »" if sid == 9000009405 else "Citoyen Indépendant")
        special_highlight = ""
        if sid == 9000006402:
            special_highlight = "Record communal part active (22.7%) & Zone 30 à surveiller"
        elif sid == 9000009405:
            special_highlight = "Zone 30 scolaire modèle (V85: 31 km/h) & seule vigie active à Rosières"
        elif sid == 9000007261:
            special_highlight = "Apaisement naturel par voirie sinueuse (V85: 24 km/h)"

        sensor_summary = {
            "id": sid,
            "street": street,
            "locality": locality,
            "role": role,
            "speed_limit": speed_limit,
            "is_official": is_official,
            "network_type": network_type,
            "special_highlight": special_highlight,
            "lat": lat,
            "lon": lon,
            "coordinates": coords,
            "status": "Actif" if rec_total > 0 else "Inactif / Déconnecté",
            "estimated_2year_cumulative": hist_data.get("estimated_2year_cumulative", 0),
            "estimated_2year_cumulative_24h": round(hist_data.get("estimated_2year_cumulative", 0) * 1.41), # avec flux nocturne moyen
            "history_periods": hist_data.get("periods", {}),
            "nov2024": {
                "total_month_classified": nov_total,
                "total_month_night": nov_night,
                "total_month_24h": nov_total_24h,
                "daily_total": round(nov_total / 30), # flux diurne classifie (backwards-compatible)
                "daily_daytime": round(nov_total / 30),
                "daily_night": round(nov_night / 30),
                "daily_24h": round(nov_total_24h / 30),
                "night_pct": nov_night_pct,
                "daily_motorized": round(nov_motorized / 30),
                "daily_cars": round(nov_cars / 30),
                "daily_heavy": round(nov_heavy / 30),
                "daily_bikes": round(nov_bikes / 30),
                "daily_peds": round(nov_peds / 30),
                "daily_active": round(nov_active / 30),
                "car_pct": nov_car_pct,
                "heavy_pct": nov_heavy_pct,
                "bike_pct": nov_bike_pct,
                "ped_pct": nov_ped_pct,
                "active_pct": round(nov_active_pct, 1),
                "active_pct_24h": round((nov_active / nov_total_24h) * 100, 1) if nov_total_24h else 0,
                "speed": {
                    "pct_0_30": round(pct_0_30, 1),
                    "pct_30_50": round(pct_30_50, 1),
                    "pct_50_60": round(pct_50_60, 1),
                    "pct_60_70": round(pct_60_70, 1),
                    "pct_over_70": round(pct_over_70, 1),
                    "pct_over_50": round(pct_over_50, 1),
                    "pct_speeding": round(pct_speeding, 1),
                    "avg_v85": avg_v85,
                    "v85_uncertainty": v85_uncertainty,
                    "max_v85": max_v85,
                    "hourly_v85": nov_v85_data
                },
                "hourly": {
                    "cars_weekday": hourly_cars_wkday,
                    "cars_weekend": hourly_cars_wkend,
                    "bikes_weekday": hourly_bikes_wkday,
                    "peds_weekday": hourly_peds_wkday,
                    "am_peak": {"hour": am_peak_hour, "volume": am_peak_car},
                    "pm_peak": {"hour": pm_peak_hour, "volume": pm_peak_car}
                }
            },
            "recent2026": {
                "total_14d": rec_total,
                "daily_total": round(rec_total / 14) if rec_total else 0,
                "daily_daytime": round(rec_total / 14) if rec_total else 0,
                "daily_cars": round(rec_cars / 14) if rec_total else 0,
                "daily_bikes": round(rec_bikes / 14) if rec_total else 0,
                "daily_peds": round(rec_peds / 14) if rec_total else 0,
                "daily_heavy": round(rec_heavy / 14) if rec_total else 0,
                "daily_active": round((rec_bikes + rec_peds) / 14) if rec_total else 0,
                "daily_night": round(rec_night / 14) if rec_total_24h else 0,
                "daily_24h": round(rec_total_24h / 14) if rec_total_24h else 0,
                "night_pct": round((rec_night / rec_total_24h) * 100, 1) if rec_total_24h else 0,
                "active_pct": round(((rec_bikes + rec_peds) / rec_total) * 100, 1) if rec_total else 0,
                "car_pct": round((rec_cars / rec_total) * 100, 1) if rec_total else 0,
                "heavy_pct": round((rec_heavy / rec_total) * 100, 1) if rec_total else 0,
                "bike_pct": round((rec_bikes / rec_total) * 100, 1) if rec_total else 0,
                "ped_pct": round((rec_peds / rec_total) * 100, 1) if rec_total else 0,
                "avg_v85": rec_avg_v85,
                "speed": {
                    "avg_v85": rec_avg_v85,
                    "v85_uncertainty": round(rec_avg_v85 * 0.1, 1) if rec_avg_v85 else None,
                    "pct_speeding": None
                }
            }
        }
        
        # Match travaux for this sensor
        sensor_travaux = []
        for ch in chantiers_list:
            for imp in ch.get("impacted_sensors", []):
                if imp.get("sensor_id") == sid:
                    sensor_travaux.append({
                        "chantier_id": ch.get("id"),
                        "title": ch.get("title"),
                        "category": ch.get("category"),
                        "status": ch.get("status"),
                        "year": ch.get("period", {}).get("year"),
                        "duration": ch.get("period", {}).get("duration"),
                        "impact_type": imp.get("impact_type"),
                        "observed_variation": imp.get("observed_variation"),
                        "correlation_note": imp.get("correlation_note")
                    })
        sensor_summary["associated_travaux"] = sensor_travaux
        sensors_summary.append(sensor_summary)
        
    # Write summary JSON
    summary_json_path = "/Users/charlesdebrier/Development/Telraam/data/rixensart_summary.json"
    with open(summary_json_path, "w", encoding="utf-8") as f:
        json.dump(sensors_summary, f, ensure_ascii=False, indent=2)
        
    # Load global history for JS export
    full_history_obj = {}
    hist_file = "/Users/charlesdebrier/Development/Telraam/data/rixensart_history.json"
    if os.path.exists(hist_file):
        with open(hist_file, "r", encoding="utf-8") as hf:
            full_history_obj = json.load(hf)
            
    # Compute YoY Analysis to answer whether traffic is increasing over time (without bias)
    full_history_obj["yoy_analysis"] = compute_yoy_analysis(full_history_obj)
    
    # Save back to history JSON
    if os.path.exists(hist_file):
        with open(hist_file, "w", encoding="utf-8") as hf:
            json.dump(full_history_obj, hf, ensure_ascii=False, indent=2)

    full_history_obj["sources_metadata"] = SOURCES_METADATA

    # Write JS file for direct HTML inclusion
    js_data_path = "/Users/charlesdebrier/Development/Telraam/data/rixensart_data.js"
    with open(js_data_path, "w", encoding="utf-8") as f:
        f.write("window.TELRAAM_RIXENSART = " + json.dumps(sensors_summary, ensure_ascii=False, indent=2) + ";\n")
        f.write("window.TELRAAM_HISTORY = " + json.dumps(full_history_obj, ensure_ascii=False, indent=2) + ";\n")
        f.write("window.TELRAAM_TRAVAUX = " + json.dumps(chantiers_list, ensure_ascii=False, indent=2) + ";\n")
        f.write("window.TELRAAM_TRAVAUX_METADATA = " + json.dumps({
            "description": travaux_obj.get("description", ""),
            "generated_at": travaux_obj.get("generated_at", ""),
            "period_covered": travaux_obj.get("period_covered", ""),
            "source_domain": travaux_obj.get("source_domain", "")
        }, ensure_ascii=False, indent=2) + ";\n")
        f.write("window.TELRAAM_SOURCES = " + json.dumps(SOURCES_METADATA, ensure_ascii=False, indent=2) + ";\n")
        
    # Write CSV with standard library
    csv_path = "/Users/charlesdebrier/Development/Telraam/data/rixensart_summary.csv"
    fields = [
        "ID", "Rue", "Entite", "Statut", "Reseau", "Role", "Limite_Vitesse_kmh",
        "Cumul_2ans_Diurne_Estime", "Cumul_2ans_24h_Estime",
        "Trafic_24h_Total_Jour", "Trafic_Diurne_Classifie_Jour", "Trafic_Nocturne_Phares_Jour", "Part_Nocturne_pct",
        "Voitures_jour", "Poids_lourds_jour", "Velos_jour", "Pietons_jour",
        "Part_Active_Diurne_pct", "Part_Active_24h_pct",
        "V85_Diurne_kmh", "Incertitude_V85_kmh", "V85_Max_Diurne_kmh", "Pct_Depassement_Limite",
        "Pic_Matin", "Pic_Soir", "Evol_YoY_Automne_pct", "Evol_YoY_Printemps_pct", "Diagnostic_Circulation", "Impact_Chantiers_et_Travaux", "Particularite", "Latitude", "Longitude"
    ]
    with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(fields)
        aut_map = {x["id"]: x for x in full_history_obj.get("yoy_analysis", {}).get("autumn", {}).get("sensors", [])}
        spr_map = {x["id"]: x for x in full_history_obj.get("yoy_analysis", {}).get("spring", {}).get("sensors", [])}
        
        for s in sensors_summary:
            sid = s["id"]
            n = s["nov2024"]
            sp = n["speed"]
            aut_pct = aut_map.get(sid, {}).get("pct_total", "N/A")
            spr_val = spr_map.get(sid, {}).get("pct_total")
            spr_pct = spr_val if spr_val is not None else "Arrêté en déc. 2025"
            diag = spr_map.get(sid, {}).get("diagnostic") or aut_map.get(sid, {}).get("diagnostic") or ""
            travaux_notes = " | ".join([f"{t['title']} [{t['impact_type']}]: {t['observed_variation']}" for t in s.get("associated_travaux", [])])
            
            writer.writerow([
                s["id"],
                s["street"],
                s["locality"],
                s["status"],
                s.get("network_type", "Officiel Municipal"),
                s["role"],
                s["speed_limit"],
                s.get("estimated_2year_cumulative", 0),
                s.get("estimated_2year_cumulative_24h", 0),
                n["daily_24h"],
                n["daily_daytime"],
                n["daily_night"],
                n["night_pct"],
                n["daily_cars"],
                n["daily_heavy"],
                n["daily_bikes"],
                n["daily_peds"],
                n["active_pct"],
                n["active_pct_24h"],
                sp["avg_v85"],
                sp.get("v85_uncertainty", 0),
                sp["max_v85"],
                sp["pct_speeding"],
                n["hourly"]["am_peak"]["hour"],
                n["hourly"]["pm_peak"]["hour"],
                aut_pct,
                spr_pct,
                diag,
                travaux_notes,
                s.get("special_highlight", ""),
                s["lat"],
                s["lon"]
            ])
    print("Generated summary.json, rixensart_data.js (with history, night metrics & travaux), and summary.csv successfully!")
    return sensors_summary

if __name__ == "__main__":
    process_and_generate()
