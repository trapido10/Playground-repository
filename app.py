import json
import os
import random
import streamlit as st

DATA_FILE = "dnd_data.json"

DEFAULT_DATA = {
    "names": {
        "Human": {
            "first": ["Bram", "Clara", "Garrick", "Elena", "Marcus", "Talia", "Oswin", "Sera"],
            "last": ["Vance", "Miller", "Thorne", "Kestrel", "Barrow", "Ashford", "Reed"]
        },
        "Dwarf": {
            "first": ["Thorin", "Hilda", "Brok", "Dagna", "Korgan", "Brynja", "Rurik", "Marda"],
            "last": ["Ironfoot", "Stonehelm", "Coppervein", "Deepdelver", "Fireforge", "Anvilmar"]
        },
        "Elf": {
            "first": ["Aelar", "Sylia", "Theren", "Lia", "Faelar", "Naivara", "Erevan", "Keyleth"],
            "last": ["Moonwhisper", "Starbreeze", "Galanodel", "Silverfrond", "Nightbreeze"]
        },
        "Tiefling": {
            "first": ["Mordai", "Kallista", "Zariel", "Orianna", "Damakos", "Makaria", "Vesper"],
            "last": ["Cinder", "Dusk", "Hollow", "Shadowbane", "Ash", "Creed", "Torment"]
        }
    },
    "occupations": [
        "Blacksmith", "Herbalist", "Bounty Hunter", "Disgraced Noble", 
        "Smuggler", "Alchemist", "Town Guard", "Traveling Bard", 
        "Archivist", "Innkeeper", "Fence", "Retired Adventurer"
    ],
    "appearances": [
        "Missing left pinky finger", "Nervous facial tic", "Impeccably tailored clothes",
        "Covered in soot and oil", "Piercing heterochromatic eyes", "Heavy jagged scar across the jaw",
        "Wears way too many silver rings", "Walks with a pronounced limp", "Smells strongly of lavender"
    ],
    "quirks": [
        "Speaks in the third person", "Constantly flips a tarnished copper coin",
        "Never makes direct eye contact", "Laughs at wildly inappropriate moments",
        "Whispers the last word of every sentence", "Aggressively takes notes in a tiny journal",
        "Insists on standing too close when talking", "Clears throat twice before answering any question"
    ],
    "secrets": [
        "Actually a doppelganger replacing the real person",
        "Owes a massive blood debt to the local thieves' guild",
        "Secretly funding a local cult",
        "In possession of a stolen royal signet ring",
        "Witnessed a murder by a high-ranking official",
        "Is an undercover spy for a rival kingdom",
        "Has a map to a nearby dungeon hidden in their boot"
    ],
    "tavern_adjectives": [
        "Rusty", "Prancing", "Gilded", "Sunken", "Drunken", "Laughing", 
        "Broken", "Crimson", "Whispering", "Salty", "Sleeping", "Blazing"
    ],
    "tavern_nouns": [
        "Pony", "Anchor", "Goblin", "Flagon", "Dragon", "Dagger", 
        "Stag", "Crow", "Cauldron", "Lantern", "Kraken", "Wyvern"
    ],
    "tavern_atmospheres": [
        "Thick with pipe smoke and the smell of roasting mutton; a bard plays a melancholy lute in the corner.",
        "Rowdy and deafening; two half-orcs are arm-wrestling on a table surrounded by cheering patrons.",
        "Eerily quiet; hooded figures sit in dark booths and stop talking the moment the door opens.",
        "Warm, brightly lit, and surprisingly clean; locals are celebrating a recent harvest.",
        "Run-down and drafty; rainwater drips into buckets and the floorboards groan under every step."
    ],
    "signature_drinks": [
        "Dwarven Ember-Ale (served warm, leaves a spicy aftertaste)",
        "Wyvern's Breath (a glowing green absinthe that numbs the tongue)",
        "Grog of the Sunken Ship (cheap, watered-down rum with a lime wedge)",
        "Elven Starlight Wine (sweet, shimmering, and wildly overpriced)",
        "Mudwater Stout (thick enough to chew, brewed in the cellar)"
    ],
    "shop_types": [
        "Blacksmith & Armory",
        "Alchemist & Herbalist",
        "General Provisioner",
        "Arcane Curiosities"
    ],
    "shop_adjectives": ["Rusty", "Gilded", "Hidden", "Whispering", "Crimson", "Hollow", "Silver", "Sunken"],
    "shop_nouns": ["Anvil", "Pouch", "Cauldron", "Tome", "Shelf", "Cart", "Flagon", "Chest"],
    "master_inventory": {
        "Blacksmith & Armory": [
            {"item": "Balanced Dagger", "price": "12 gp", "tier": "Common", "desc": "Finely weighted for throwing."},
            {"item": "Reinforced Shield", "price": "15 gp", "tier": "Common", "desc": "Dented iron banding, sturdy construction."},
            {"item": "Whetstone of Keening", "price": "5 gp", "tier": "Common", "desc": "Puts a razor edge on blades."},
            {"item": "Iron Spikes (10 pack)", "price": "1 gp", "tier": "Common", "desc": "Crucial for wedging doors open."},
            {"item": "Mithril-Plated Greaves", "price": "85 gp", "tier": "Uncommon", "desc": "Lighter and surprisingly tough."},
            {"item": "Flame-Etched Longsword", "price": "150 gp", "tier": "Rare", "desc": "Emits a faint ambient warmth."}
        ],
        "Alchemist & Herbalist": [
            {"item": "Draft of Swift Footing", "price": "25 gp", "tier": "Uncommon", "desc": "Adds 10 ft to movement for 1 minute."},
            {"item": "Soothing Balm", "price": "10 gp", "tier": "Common", "desc": "Smells like pine; heals minor cuts."},
            {"item": "Glowing Moss Vial", "price": "8 gp", "tier": "Common", "desc": "Emits soft green light for 2 hours."},
            {"item": "Smelling Salts", "price": "3 gp", "tier": "Common", "desc": "Instantly wakes an unconscious ally."},
            {"item": "Troll-Blood Extract", "price": "120 gp", "tier": "Rare", "desc": "Accelerates natural tissue regeneration."}
        ],
        "General Provisioner": [
            {"item": "Rope, Hempens (50 ft)", "price": "1 gp", "tier": "Common", "desc": "Sturdy and slightly frayed at one end."},
            {"item": "Iron Rations (5 days)", "price": "2 gp", "tier": "Common", "desc": "Hardtack, dried fruit, and salted beef."},
            {"item": "Tallow Candles (10 pack)", "price": "1 sp", "tier": "Common", "desc": "Smells faintly of mutton fat."},
            {"item": "Waterskin (Full)", "price": "2 sp", "tier": "Common", "desc": "Holds clean river water."},
            {"item": "Everburn Torch", "price": "50 gp", "tier": "Uncommon", "desc": "Magical flame that never consumes fuel."}
        ],
        "Arcane Curiosities": [
            {"item": "Unlabeled Glass Prism", "price": "30 gp", "tier": "Uncommon", "desc": "Refracts light into shifting colors."},
            {"item": "Chalk of Warding", "price": "10 gp", "tier": "Common", "desc": "Emits a faint static hum when touched."},
            {"item": "Whispering Seashell", "price": "15 gp", "tier": "Common", "desc": "Plays distant crashing waves."},
            {"item": "Faded Parchment Map", "price": "20 gp", "tier": "Common", "desc": "Points to an unverified ruin."},
            {"item": "Ring of Minor Shielding", "price": "200 gp", "tier": "Rare", "desc": "Absorbs the first 5 damage taken."}
        ]
    },
    "enemy_roster": [
        {"name": "Goblin Skirmisher", "cr": "1/4", "hp": "7 (2d6)", "ac": "15", "speed": "30 ft.", "attack": "Scimitar (+4 to hit, 1d6 + 2 slashing)", "trait": "Nimble Escape: Can take the Disengage or Hide action as a bonus action."},
        {"name": "Restless Skeleton", "cr": "1/4", "hp": "13 (2d8 + 4)", "ac": "13", "speed": "30 ft.", "attack": "Shortsword (+4 to hit, 1d6 + 2 piercing)", "trait": "Bone Resilience: Vulnerable to bludgeoning damage; immune to poison condition."},
        {"name": "Bandit Thug", "cr": "1/8", "hp": "11 (2d8 + 2)", "ac": "12", "speed": "30 ft.", "attack": "Spear (+3 to hit, 1d6 + 1 piercing)", "trait": "Desperate Strike: Deals +2 damage if an ally is within 5 feet of the target."},
        {"name": "Tunnel Kobold", "cr": "1/8", "hp": "5 (2d4)", "ac": "12", "speed": "30 ft.", "attack": "Dagger (+4 to hit, 1d4 + 2 piercing)", "trait": "Pack Tactics: Has advantage on attack rolls if at least one ally is within 5 feet."},
        {"name": "Feral Wolf", "cr": "1/4", "hp": "11 (2d8 + 2)", "ac": "13", "speed": "40 ft.", "attack": "Bite (+4 to hit, 1d6 + 2 piercing + DC 11 Strength save or fall prone)", "trait": "Keen Hearing and Smell: Advantage on Wisdom (Perception) checks relying on hearing/smell."},
        {"name": "Cult Initiate", "cr": "1/8", "hp": "9 (2d8)", "ac": "12", "speed": "30 ft.", "attack": "Dagger (+3 to hit, 1d4 + 1 piercing)", "trait": "Fanatical Devotion: Has advantage on saving throws against being charmed or frightened."}
    ]
}

@st.cache_data
def load_data():
    if not os.path.exists(DATA_FILE):
        data = DEFAULT_DATA
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        return data
    
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    updated = False
    for key, val in DEFAULT_DATA.items():
        if key not in data:
            data[key] = val
            updated = True
            
    if updated:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
            
    return data

data = load_data()

# Page configuration
st.set_page_config(page_title="The Land of S'rai - DM Toolkit", layout="centered")

# --- CUSTOM MEDIEVAL FOREST & WOOD CSS (CONDENSED) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@700;900&family=Inter:wght@400;500;600;700&display=swap');

.block-container {
    padding-top: 1.2rem !important;
    padding-bottom: 1.2rem !important;
}

.stApp {
    background: radial-gradient(circle at top, #1f3322 0%, #0f1a11 65%, #080e09 100%);
    color: #f4ecdc;
    font-family: 'Inter', sans-serif;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #24170e 0%, #170e08 100%);
    border-right: 3px solid #6e4e2e;
    box-shadow: 4px 0 15px rgba(0,0,0,0.7);
}
section[data-testid="stSidebar"] * {
    color: #e6d5b8 !important;
    font-family: 'Inter', sans-serif;
}

h1, h2, h3 {
    font-family: 'Cinzel Decorative', cursive !important;
    color: #d4af37 !important;
    text-shadow: 2px 3px 6px rgba(0, 0, 0, 0.85);
    letter-spacing: 0.5px;
    margin-top: 0.3rem !important;
    margin-bottom: 0.3rem !important;
}

.hero-plaque {
    background: linear-gradient(135deg, #2d1d12 0%, #1d120a 100%);
    border: 2px solid #8c6239;
    border-radius: 6px;
    padding: 14px 18px;
    text-align: center;
    box-shadow: inset 0 0 15px rgba(0,0,0,0.8), 0 6px 14px rgba(0,0,0,0.6);
    margin-bottom: 12px;
}
.hero-plaque h1 {
    margin: 0 !important;
    font-size: 1.8rem;
    color: #e5c158 !important;
}
.hero-subtitle {
    color: #b8c9b0;
    font-size: 0.85rem;
    margin-top: 3px;
    font-family: 'Inter', sans-serif;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

div.stButton > button {
    background: linear-gradient(180deg, #3b5938 0%, #233821 100%);
    color: #f3e8d2 !important;
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    font-size: 0.92rem;
    border: 1px solid #9c7a44;
    border-radius: 5px;
    padding: 0.4rem 1.1rem;
    box-shadow: 0 3px 8px rgba(0,0,0,0.5);
    transition: all 0.15s ease-in-out;
}
div.stButton > button:hover {
    background: linear-gradient(180deg, #4b7047 0%, #2e4a2b 100%);
    border-color: #d4af37;
}

.npc-card, .shop-card, .enemy-card {
    background: linear-gradient(180deg, #241911 0%, #1b120c 100%);
    border: 1px solid #7c5832;
    border-left: 4px solid #4c7c44;
    border-radius: 5px;
    padding: 10px 14px;
    margin-bottom: 8px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.55);
    font-family: 'Inter', sans-serif;
}
.npc-top-row {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    border-bottom: 1px solid #4d351d;
    padding-bottom: 3px;
    margin-bottom: 5px;
}
.npc-header, .shop-header {
    font-family: 'Inter', sans-serif;
    font-weight: 700;
    font-size: 1.02rem;
    color: #e5c158;
}
.npc-meta {
    color: #9cb895;
    font-weight: 600;
    font-size: 0.85rem;
}
.npc-detail {
    color: #f4ecdc;
    margin: 2px 0;
    line-height: 1.3;
    font-size: 0.88rem;
}
.npc-secret {
    margin-top: 5px;
    padding: 5px 8px;
    background: rgba(12, 20, 14, 0.85);
    border-left: 2px solid #8c6239;
    border-radius: 3px;
    color: #e0cfa8;
    font-size: 0.85rem;
    line-height: 1.3;
}

.tavern-card {
    background: linear-gradient(180deg, #182619 0%, #101911 100%);
    border: 1px solid #8c6239;
    border-radius: 6px;
    padding: 12px 16px;
    margin-bottom: 10px;
    box-shadow: 0 6px 14px rgba(0,0,0,0.65);
}
.tavern-title {
    font-family: 'Inter', sans-serif;
    font-weight: 700;
    font-size: 1.18rem;
    color: #e5c158;
    margin-bottom: 3px;
}
.tavern-desc {
    color: #e2ebd9;
    font-size: 0.89rem;
    line-height: 1.35;
    margin-bottom: 6px;
}
.tavern-drink {
    background: #24170e;
    border: 1px solid #6e4e2e;
    padding: 5px 8px;
    border-radius: 4px;
    color: #f5d78a;
    font-size: 0.85rem;
    font-weight: 500;
}

div[data-baseweb="select"] > div {
    background-color: #24170e !important;
    border: 1px solid #8c6239 !important;
    color: #f4ecdc !important;
}
</style>
""", unsafe_allow_html=True)

# --- HERO LANDING HEADER ---
st.markdown("""
<div class="hero-plaque">
    <h1>⚔️ The Land of S'rai 🌲</h1>
    <div class="hero-subtitle">Dungeon Master Campaign & Encounter Toolkit</div>
</div>
""", unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION ---
st.sidebar.markdown("## DM Controls")
app_mode = st.sidebar.radio("Select Tool:", ["NPC Generator", "Tavern Generator", "Shop Generator", "Enemy Generator", "Campaign Data"])

patron_count = 2
if app_mode == "Tavern Generator":
    st.sidebar.markdown("---")
    patron_count = st.sidebar.slider("Tavern Patrons", min_value=1, max_value=4, value=2)

st.sidebar.markdown("---")
st.sidebar.caption("Edit `dnd_data.json` to customize names, traits, and inventory.")

# --- HTML RENDERERS ---
def render_npc_card(npc):
    st.markdown(f"""
    <div class="npc-card">
        <div class="npc-top-row">
            <span class="npc-header">{npc['Name']}</span>
            <span class="npc-meta">{npc['Race']} | {npc['Occupation']}</span>
        </div>
        <div class="npc-detail"><strong>Appearance:</strong> {npc['Appearance']}</div>
        <div class="npc-detail"><strong>Quirk:</strong> {npc['Quirk']}</div>
        <div class="npc-secret"><strong>Secret:</strong> {npc['Secret']}</div>
    </div>
    """, unsafe_allow_html=True)

# --- APP VIEWS ---
if app_mode == "NPC Generator":
    st.subheader("NPC Generator")
    races = list(data["names"].keys())
    selected_race = st.selectbox("Filter by Race:", ["Random"] + races)
    
    if st.button("Generate NPC"):
        chosen_race = None if selected_race == "Random" else selected_race
        race = chosen_race if chosen_race in races else random.choice(races)
        first_name = random.choice(data["names"][race]["first"])
        last_name = random.choice(data["names"][race]["last"])
        
        npc = {
            "Name": f"{first_name} {last_name}",
            "Race": race,
            "Occupation": random.choice(data["occupations"]),
            "Appearance": random.choice(data["appearances"]),
            "Quirk": random.choice(data["quirks"]),
            "Secret": random.choice(data["secrets"])
        }
        render_npc_card(npc)

elif app_mode == "Tavern Generator":
    st.subheader("Tavern Generator")
    
    if st.button("Generate Tavern"):
        tavern_name = f"The {random.choice(data['tavern_adjectives'])} {random.choice(data['tavern_nouns'])}"
        atmosphere = random.choice(data["tavern_atmospheres"])
        drink = random.choice(data["signature_drinks"])
        
        st.markdown(f"""
        <div class="tavern-card">
            <div class="tavern-title">{tavern_name}</div>
            <div class="tavern-desc">{atmosphere}</div>
            <div class="tavern-drink"><strong>House Specialty:</strong> {drink}</div>
        </div>
        """, unsafe_allow_html=True)
        
        barkeep_race = random.choice(list(data["names"].keys()))
        barkeep = {
            "Name": f"{random.choice(data['names'][barkeep_race]['first'])} {random.choice(data['names'][barkeep_race]['last'])}",
            "Race": barkeep_race,
            "Occupation": "Tavern Keeper",
            "Appearance": random.choice(data["appearances"]),
            "Quirk": random.choice(data["quirks"]),
            "Secret": random.choice(data["secrets"])
        }
        
        st.markdown("**Staff**")
        render_npc_card(barkeep)
        
        st.markdown(f"**Patrons ({patron_count})**")
        cols = st.columns(2) if patron_count > 1 else [st.container()]
        
        for i in range(patron_count):
            patron_race = random.choice(list(data["names"].keys()))
            patron = {
                "Name": f"{random.choice(data['names'][patron_race]['first'])} {random.choice(data['names'][patron_race]['last'])}",
                "Race": patron_race,
                "Occupation": random.choice(data["occupations"]),
                "Appearance": random.choice(data["appearances"]),
                "Quirk": random.choice(data["quirks"]),
                "Secret": random.choice(data["secrets"])
            }
            with cols[i % 2]:
                render_npc_card(patron)

elif app_mode == "Shop Generator":
    st.subheader("Shop Generator")
    shop_types = data.get("shop_types", ["General Provisioner"])
    selected_shop_type = st.selectbox("Shop Category:", ["Random"] + shop_types)
    
    if st.button("Generate Shop"):
        shop_type = random.choice(shop_types) if selected_shop_type == "Random" else selected_shop_type
        shop_name = f"The {random.choice(data['shop_adjectives'])} {random.choice(data['shop_nouns'])}"
        
        st.markdown(f"""
        <div class="shop-card">
            <div class="npc-top-row" style="border-bottom:none; margin-bottom:0; padding-bottom:0;">
                <span class="shop-header">{shop_name}</span>
                <span class="npc-meta">{shop_type}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        keeper_race = random.choice(list(data["names"].keys()))
        keeper = {
            "Name": f"{random.choice(data['names'][keeper_race]['first'])} {random.choice(data['names'][keeper_race]['last'])}",
            "Race": keeper_race,
            "Occupation": "Shopkeeper",
            "Appearance": random.choice(data["appearances"]),
            "Quirk": random.choice(data["quirks"]),
            "Secret": random.choice(data["secrets"])
        }
        
        st.markdown("**Proprietor**")
        render_npc_card(keeper)
        
        st.markdown("**Randomized Inventory**")
        master_pool = data.get("master_inventory", {}).get(shop_type, [])
        stock_count = min(len(master_pool), random.randint(5, 7))
        current_stock = random.sample(master_pool, stock_count)
        
        for item in current_stock:
            st.markdown(f"- **{item['item']}** ({item['price']}) [{item['tier']}] — *{item['desc']}*")

elif app_mode == "Enemy Generator":
    st.subheader("Low-Level Enemy Generator")
    
    roster = data.get("enemy_roster", [])
    selected_enemy_type = st.selectbox("Enemy Type:", ["Random"] + [e["name"] for e in roster])
    
    if st.button("Generate Enemy"):
        if selected_enemy_type == "Random":
            enemy = random.choice(roster)
        else:
            enemy = next((e for e in roster if e["name"] == selected_enemy_type), roster[0])
            
        st.markdown(f"""
        <div class="enemy-card">
            <div class="npc-top-row">
                <span class="shop-header">{enemy['name']}</span>
                <span class="npc-meta">CR {enemy['cr']}</span>
            </div>
            <div class="npc-detail"><strong>Armor Class:</strong> {enemy['ac']} &nbsp;|&nbsp; <strong>Hit Points:</strong> {enemy['hp']} &nbsp;|&nbsp; <strong>Speed:</strong> {enemy['speed']}</div>
            <div class="npc-detail"><strong>Primary Attack:</strong> {enemy['attack']}</div>
            <div class="npc-secret"><strong>Special Trait:</strong> {enemy['trait']}</div>
        </div>
        """, unsafe_allow_html=True)

elif app_mode == "Campaign Data":
    st.subheader("Campaign Data (dnd_data.json)")
    st.write("Active configuration data for The Land of S'rai:")
    st.json(data)