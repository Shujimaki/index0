from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

# --- COMPLETE PHILIPPINE GEOGRAPHIC DATASET (Region -> Province -> Cities) ---

PHILIPPINE_GEOGRAPHY = {
    "ncr": {
        "name": "National Capital Region (NCR)",
        "provinces": {
            "metro_manila": {
                "name": "Metro Manila",
                "cities": [
                    {"value": "caloocan", "name": "Caloocan"},
                    {"value": "las_pinas", "name": "Las Piñas"},
                    {"value": "makati", "name": "Makati"},
                    {"value": "malabon", "name": "Malabon"},
                    {"value": "mandaluyong", "name": "Mandaluyong"},
                    {"value": "manila", "name": "Manila"},
                    {"value": "marikina", "name": "Marikina"},
                    {"value": "muntinlupa", "name": "Muntinlupa"},
                    {"value": "navotas", "name": "Navotas"},
                    {"value": "paranaque", "name": "Parañaque"},
                    {"value": "pasay", "name": "Pasay"},
                    {"value": "pasig", "name": "Pasig"},
                    {"value": "quezon_city", "name": "Quezon City"},
                    {"value": "san_juan", "name": "San Juan"},
                    {"value": "taguig", "name": "Taguig"},
                    {"value": "valenzuela", "name": "Valenzuela"},
                ]
            }
        }
    },
    "car": {
        "name": "Cordillera Administrative Region (CAR)",
        "provinces": {
            "abra": {"name": "Abra", "cities": [{"value": "none", "name": "None"}]},
            "apayao": {"name": "Apayao", "cities": [{"value": "none", "name": "None"}]},
            "benguet": {"name": "Benguet", "cities": [{"value": "baguio", "name": "Baguio"}]},
            "ifugao": {"name": "Ifugao", "cities": [{"value": "none", "name": "None"}]},
            "kalinga": {"name": "Kalinga", "cities": [{"value": "tabuk_city", "name": "Tabuk City"}]},
            "mountain_province": {"name": "Mountain Province", "cities": [{"value": "none", "name": "None"}]},
        }
    },
    "ilocos_region_i": {
        "name": "Ilocos Region (Region I)",
        "provinces": {
            "ilocos_norte": {"name": "Ilocos Norte", "cities": [{"value": "batac_city", "name": "Batac City"}, {"value": "laoag_city", "name": "Laoag City"}]},
            "ilocos_sur": {"name": "Ilocos Sur", "cities": [{"value": "candon_city", "name": "Candon City"}, {"value": "vigan_city", "name": "Vigan City"}]},
            "la_union": {"name": "La Union", "cities": [{"value": "san_fernando_city", "name": "San Fernando City"}]},
            "pangasinan": {"name": "Pangasinan", "cities": [{"value": "alaminos_city", "name": "Alaminos City"}, {"value": "dagupan_city", "name": "Dagupan City"}, {"value": "san_carlos_city", "name": "San Carlos City"}, {"value": "urdaneta_city", "name": "Urdaneta City"}]},
        }
    },
    "cagayan_valley_ii": {
        "name": "Cagayan Valley (Region II)",
        "provinces": {
            "batanes": {"name": "Batanes", "cities": [{"value": "none", "name": "None"}]},
            "cagayan": {"name": "Cagayan", "cities": [{"value": "tuguegarao_city", "name": "Tuguegarao City"}]},
            "isabela": {"name": "Isabela", "cities": [{"value": "cauayan_city", "name": "Cauayan City"}, {"value": "ilagan_city", "name": "Ilagan City"}, {"value": "santiago_city", "name": "Santiago City"}]},
            "nueva_vizcaya": {"name": "Nueva Vizcaya", "cities": [{"value": "none", "name": "None"}]},
            "quirino": {"name": "Quirino", "cities": [{"value": "none", "name": "None"}]},
        }
    },
    "central_luzon_iii": {
        "name": "Central Luzon (Region III)",
        "provinces": {
            "aurora": {"name": "Aurora", "cities": [{"value": "none", "name": "None"}]},
            "bataan": {"name": "Bataan", "cities": [{"value": "balanga_city", "name": "Balanga City"}]},
            "bulacan": {"name": "Bulacan", "cities": [{"value": "malolos_city", "name": "Malolos City"}, {"value": "meycauayan_city", "name": "Meycauayan City"}, {"value": "san_jose_del_monte_city", "name": "San Jose del Monte City"}]},
            "nueva_ecija": {"name": "Nueva Ecija", "cities": [{"value": "cabanatuan_city", "name": "Cabanatuan City"}, {"value": "gapan_city", "name": "Gapan City"}, {"value": "munoz_city", "name": "Muñoz City"}, {"value": "palayan_city", "name": "Palayan City"}, {"value": "san_jose_city", "name": "San Jose City"}]},
            "pampanga": {"name": "Pampanga", "cities": [{"value": "angeles_city", "name": "Angeles City"}, {"value": "mabalacat_city", "name": "Mabalacat City"}, {"value": "san_fernando_city", "name": "San Fernando City"}]},
            "tarlac": {"name": "Tarlac", "cities": [{"value": "tarlac_city", "name": "Tarlac City"}]},
            "zambales": {"name": "Zambales", "cities": [{"value": "olonganpo_city", "name": "Olongapo City"}]},
        }
    },
    "calabarzon_iva": {
        "name": "CALABARZON (Region IV-A)",
        "provinces": {
            "batangas": {"name": "Batangas", "cities": [{"value": "batangas_city", "name": "Batangas City"}, {"value": "lipa_city", "name": "Lipa City"}, {"value": "santo_tomas_city", "name": "Santo Tomas City"}, {"value": "tanauan_city", "name": "Tanauan City"}]},
            "cavite": {"name": "Cavite", "cities": [{"value": "bacoor_city", "name": "Bacoor City"}, {"value": "cavite_city", "name": "Cavite City"}, {"value": "dasmarinas_city", "name": "Dasmariñas City"}, {"value": "general_trias_city", "name": "General Trias City"}, {"value": "imus_city", "name": "Imus City"}, {"value": "tagaytay_city", "name": "Tagaytay City"}, {"value": "trece_martires_city", "name": "Trece Martires City"}]},
            "laguna": {"name": "Laguna", "cities": [{"value": "binan_city", "name": "Biñan City"}, {"value": "cabuyao_city", "name": "Cabuyao City"}, {"value": "calamba_city", "name": "Calamba City"}, {"value": "san_pablo_city", "name": "San Pablo City"}, {"value": "san_pedro_city", "name": "San Pedro City"}, {"value": "santa_rosa_city", "name": "Santa Rosa City"}]},
            "quezon": {"name": "Quezon", "cities": [{"value": "lucena_city", "name": "Lucena City"}, {"value": "tayabas_city", "name": "Tayabas City"}]},
            "rizal": {"name": "Rizal", "cities": [{"value": "antipolo_city", "name": "Antipolo City"}]},
        }
    },
    "mimaropa_ivb": {
        "name": "MIMAROPA (Region IV-B)",
        "provinces": {
            "marinduque": {"name": "Marinduque", "cities": [{"value": "none", "name": "None"}]},
            "occidental_mindoro": {"name": "Occidental Mindoro", "cities": [{"value": "none", "name": "None"}]},
            "oriental_mindoro": {"name": "Oriental Mindoro", "cities": [{"value": "calapan_city", "name": "Calapan City"}]},
            "palawan": {"name": "Palawan", "cities": [{"value": "puerto_princesa_city", "name": "Puerto Princesa City"}]},
            "romblon": {"name": "Romblon", "cities": [{"value": "none", "name": "None"}]},
        }
    },
    "bicol_region_v": {
        "name": "Bicol Region (Region V)",
        "provinces": {
            "albay": {"name": "Albay", "cities": [{"value": "legazpi_city", "name": "Legazpi City"}, {"value": "ligao_city", "name": "Ligao City"}, {"value": "tabaco_city", "name": "Tabaco City"}]},
            "camarines_norte": {"name": "Camarines Norte", "cities": [{"value": "none", "name": "None"}]},
            "camarines_sur": {"name": "Camarines Sur", "cities": [{"value": "iriga_city", "name": "Iriga City"}, {"value": "naga_city", "name": "Naga City"}]},
            "catanduanes": {"name": "Catanduanes", "cities": [{"value": "none", "name": "None"}]},
            "masbate": {"name": "Masbate", "cities": [{"value": "masbate_city", "name": "Masbate City"}]},
            "sorsogon": {"name": "Sorsogon", "cities": [{"value": "sorsogon_city", "name": "Sorsogon City"}]},
        }
    },
    "western_visayas_vi": {
        "name": "Western Visayas (Region VI)",
        "provinces": {
            "aklan": {"name": "Aklan", "cities": [{"value": "none", "name": "None"}]},
            "antique": {"name": "Antique", "cities": [{"value": "none", "name": "None"}]},
            "capiz": {"name": "Capiz", "cities": [{"value": "roxas_city", "name": "Roxas City"}]},
            "guimaras": {"name": "Guimaras", "cities": [{"value": "none", "name": "None"}]},
            "iloilo": {"name": "Iloilo", "cities": [{"value": "iloilo_city", "name": "Iloilo City"}, {"value": "passi_city", "name": "Passi City"}]},
            "negros_occidental": {"name": "Negros Occidental", "cities": [{"value": "bacolod_city", "name": "Bacolod City"}, {"value": "bago_city", "name": "Bago City"}, {"value": "cadiz_city", "name": "Cadiz City"}, {"value": "escalante_city", "name": "Escalante City"}, {"value": "himamaylan_city", "name": "Himamaylan City"}, {"value": "kabankalan_city", "name": "Kabankalan City"}, {"value": "la_carlota_city", "name": "La Carlota City"}, {"value": "sagay_city", "name": "Sagay City"}, {"value": "san_carlos_city", "name": "San Carlos City"}, {"value": "silay_city", "name": "Silay City"}, {"value": "sipalay_city", "name": "Sipalay City"}, {"value": "talisay_city", "name": "Talisay City"}, {"value": "victorias_city", "name": "Victorias City"}]},
        }
    },
    "central_visayas_vii": {
        "name": "Central Visayas (Region VII)",
        "provinces": {
            "bohol": {"name": "Bohol", "cities": [{"value": "tagbilaran_city", "name": "Tagbilaran City"}]},
            "cebu": {"name": "Cebu", "cities": [{"value": "bogo_city", "name": "Bogo City"}, {"value": "carcar_city", "name": "Carcar City"}, {"value": "cebu_city", "name": "Cebu City"}, {"value": "danao_city", "name": "Danao City"}, {"value": "lapu_lapu_city", "name": "Lapu-Lapu City"}, {"value": "mandaue_city", "name": "Mandaue City"}, {"value": "naga_city", "name": "Naga City"}, {"value": "toledo_city", "name": "Toledo City"}]},
            "negros_oriental": {"name": "Negros Oriental", "cities": [{"value": "bais_city", "name": "Bais City"}, {"value": "bayawan_city", "name": "Bayawan City"}, {"value": "canlaon_city", "name": "Canlaon City"}, {"value": "dumaguete_city", "name": "Dumaguete City"}, {"value": "tanjay_city", "name": "Tanjay City"}]},
            "siquijor": {"name": "Siquijor", "cities": [{"value": "none", "name": "None"}]},
        }
    },
    "eastern_visayas_viii": {
        "name": "Eastern Visayas (Region VIII)",
        "provinces": {
            "biliran": {"name": "Biliran", "cities": [{"value": "none", "name": "None"}]},
            "eastern_samar": {"name": "Eastern Samar", "cities": [{"value": "borongan_city", "name": "Borongan City"}]},
            "leyte": {"name": "Leyte", "cities": [{"value": "baybay_city", "name": "Baybay City"}, {"value": "ormoc_city", "name": "Ormoc City"}, {"value": "tacloban_city", "name": "Tacloban City"}]},
            "northern_samar": {"name": "Northern Samar", "cities": [{"value": "none", "name": "None"}]},
            "samar": {"name": "Samar", "cities": [{"value": "calbayog_city", "name": "Calbayog City"}, {"value": "catbalogan_city", "name": "Catbalogan City"}]},
            "southern_leyte": {"name": "Southern Leyte", "cities": [{"value": "maasin_city", "name": "Maasin City"}]},
        }
    },
    "zamboanga_peninsula_ix": {
        "name": "Zamboanga Peninsula (Region IX)",
        "provinces": {
            "zamboanga_del_norte": {"name": "Zamboanga del Norte", "cities": [{"value": "dapitan_city", "name": "Dapitan City"}, {"value": "dipolog_city", "name": "Dipolog City"}]},
            "zamboanga_del_sur": {"name": "Zamboanga del Sur", "cities": [{"value": "pagadian_city", "name": "Pagadian City"}, {"value": "zamboanga_city", "name": "Zamboanga City"}]},
            "zamboanga_sibugay": {"name": "Zamboanga Sibugay", "cities": [{"value": "none", "name": "None"}]},
        }
    },
    "northern_mindanao_x": {
        "name": "Northern Mindanao (Region X)",
        "provinces": {
            "bukidnon": {"name": "Bukidnon", "cities": [{"value": "malaybalay_city", "name": "Malaybalay City"}, {"value": "valencia_city", "name": "Valencia City"}]},
            "camiguin": {"name": "Camiguin", "cities": [{"value": "none", "name": "None"}]},
            "lanao_del_norte": {"name": "Lanao del Norte", "cities": [{"value": "iligan_city", "name": "Iligan City"}]},
            "misamis_occidental": {"name": "Misamis Occidental", "cities": [{"value": "oroquieta_city", "name": "Oroquieta City"}, {"value": "ozamiz_city", "name": "Ozamiz City"}, {"value": "tangub_city", "name": "Tangub City"}]},
            "misamis_oriental": {"name": "Misamis Oriental", "cities": [{"value": "cagayan_de_oro_city", "name": "Cagayan de Oro City"}, {"value": "el_salvador_city", "name": "El Salvador City"}, {"value": "gingoog_city", "name": "Gingoog City"}]},
        }
    },
    "davao_region_xi": {
        "name": "Davao Region (Region XI)",
        "provinces": {
            "davao_de_oro": {"name": "Davao de Oro", "cities": [{"value": "none", "name": "None"}]},
            "davao_del_norte": {"name": "Davao del Norte", "cities": [{"value": "panabo_city", "name": "Panabo City"}, {"value": "samal_city", "name": "Samal City"}, {"value": "tagum_city", "name": "Tagum City"}]},
            "davao_del_sur": {"name": "Davao del Sur", "cities": [{"value": "davao_city", "name": "Davao City"}, {"value": "digos_city", "name": "Digos City"}]},
            "davao_oriental": {"name": "Davao Oriental", "cities": [{"value": "mati_city", "name": "Mati City"}]},
            "davao_occidental": {"name": "Davao Occidental", "cities": [{"value": "none", "name": "None"}]},
        }
    },
    "soccsksargen_xii": {
        "name": "SOCCSKSARGEN (Region XII)",
        "provinces": {
            "cotabato_north": {"name": "Cotabato (North)", "cities": [{"value": "kidapawan_city", "name": "Kidapawan City"}]},
            "sarangani": {"name": "Sarangani", "cities": [{"value": "none", "name": "None"}]},
            "south_cotabato": {"name": "South Cotabato", "cities": [{"value": "general_santos_city", "name": "General Santos City"}, {"value": "koronadal_city", "name": "Koronadal City"}]},
            "sultan_kudarat": {"name": "Sultan Kudarat", "cities": [{"value": "tacurong_city", "name": "Tacurong City"}]},
        }
    },
    "caraga_xiii": {
        "name": "Caraga (Region XIII)",
        "provinces": {
            "agusan_del_norte": {"name": "Agusan del Norte", "cities": [{"value": "butuan_city", "name": "Butuan City"}, {"value": "cabadbaran_city", "name": "Cabadbaran City"}]},
            "agusan_del_sur": {"name": "Agusan del Sur", "cities": [{"value": "bayugan_city", "name": "Bayugan City"}]},
            "dinagat_islands": {"name": "Dinagat Islands", "cities": [{"value": "none", "name": "None"}]},
            "surigao_del_norte": {"name": "Surigao del Norte", "cities": [{"value": "surigao_city", "name": "Surigao City"}]},
            "surigao_del_sur": {"name": "Surigao del Sur", "cities": [{"value": "bislig_city", "name": "Bislig City"}, {"value": "tandag_city", "name": "Tandag City"}]},
        }
    },
    "barmm": {
        "name": "BARMM (Bangsamoro Autonomous Region in Muslim Mindanao)",
        "provinces": {
            "basilan": {"name": "Basilan", "cities": [{"value": "isabela_city", "name": "Isabela City"}]},
            "lanao_del_sur": {"name": "Lanao del Sur", "cities": [{"value": "marawi_city", "name": "Marawi City"}]},
            "maguindanao_del_norte": {"name": "Maguindanao del Norte", "cities": [{"value": "cotabato_city", "name": "Cotabato City"}, {"value": "none_1", "name": "None"}]},
            "maguindanao_del_sur": {"name": "Maguindanao del Sur", "cities": [{"value": "none_2", "name": "None"}]},
            "sulu": {"name": "Sulu", "cities": [{"value": "none_3", "name": "None"}]},
            "tawi_tawi": {"name": "Tawi-Tawi", "cities": [{"value": "none_4", "name": "None"}]},
        }
    }
}

# 1. List of Regions for the first dropdown
REGIONS_LIST = [
    {"value": code, "name": data["name"]} 
    for code, data in PHILIPPINE_GEOGRAPHY.items()
]

# --- FLASK APPLICATION AND ROUTES ---

@app.route('/', methods=['GET'])
def auth_page():
    """Renders the combined Login/Registration page."""
    context = {
        # Note: Ensure you have a 'yaniglogo.png' in a '/static/' folder, or change this URL
        'logo_url': '/static/yaniglogo.png',
        'regions': REGIONS_LIST,
    }
    return render_template('auth_page.html', **context)


@app.route('/api/provinces/<region_code>')
def get_provinces_by_region(region_code):
    """API endpoint to return a JSON list of provinces for a given region code."""
    region_data = PHILIPPINE_GEOGRAPHY.get(region_code)
    
    if region_data:
        provinces = [
            {"value": code, "name": data["name"]} 
            for code, data in region_data["provinces"].items()
        ]
        return jsonify(provinces)
    else:
        return jsonify([])


@app.route('/api/cities/<region_code>/<province_code>')
def get_cities_by_province(region_code, province_code):
    """API endpoint to return a JSON list of cities for a given province and region."""
    region_data = PHILIPPINE_GEOGRAPHY.get(region_code)
    
    if region_data and province_code in region_data["provinces"]:
        return jsonify(region_data["provinces"][province_code]["cities"])
    else:
        return jsonify([])

# --- AUTH ROUTES (for submission handling) ---
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    # Add your actual login logic here
    print(f"Login attempt: User={username}")
    return redirect(url_for('auth_page'))

@app.route('/register', methods=['POST'])
def register():
    data = {
        'name': request.form.get('name'),
        'region': request.form.get('region'),
        'province': request.form.get('province'),
        'city': request.form.get('city'),
    }
    # Add your actual registration logic here
    print(f"Registration successful for: {data.get('name')}. Location: {data.get('city')}, {data.get('province')}, {data.get('region')}")
    return redirect(url_for('auth_page'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)