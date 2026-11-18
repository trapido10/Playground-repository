


import json
import os
import random
import streamlit as st

DATA_FILE = "dnd_data.json"

# Default data used if dnd_data.json doesn't exist
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
    ]
}

@st.cache_data
def load_data():
    """Loads data from JSON, or creates the file with defaults if it doesn't exist."""
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_DATA, f, indent=4)
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

data = load_data()

# Page configuration
st.set_page_config(page_title="D&D Campaign Generator", page_icon="🎲", layout="centered")

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 4rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🎲 D&D Campaign Generator")
st.write("Instantly generate immersive NPCs and taverns for your tabletop sessions right in your browser.")

# Sidebar navigation
st.sidebar.title("Navigation")
app_mode = st.sidebar.radio("Choose Generator:", ["Generate NPC", "Generate Tavern", "View Data Source"])

def display_npc(npc):
    st.markdown(f"### {npc['Name']}")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Race:** {npc['Race']}")
        st.markdown(f"**Occupation:** {npc['Occupation']}")
    with col2:
        st.markdown(f"**Appearance:** {npc['Appearance']}")
        st.markdown(f"**Quirk:** {npc['Quirk']}")
    st.info(f"**Secret:** {npc['Secret']}")

if app_mode == "Generate NPC":
    st.header("👤 NPC Generator")
    
    races = list(data["names"].keys())
    selected_race = st.selectbox("Choose Race (or select Random):", ["Random"] + races)
    
    if st.button("Generate NPC", type="primary"):
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
        display_npc(npc)

elif app_mode == "Generate Tavern":
    st.header("🍺 Tavern Generator")
    
    if st.button("Generate Tavern", type="primary"):
        tavern_name = f"The {random.choice(data['tavern_adjectives'])} {random.choice(data['tavern_nouns'])}"
        atmosphere = random.choice(data["tavern_atmospheres"])
        drink = random.choice(data["signature_drinks"])
        
        barkeep_race = random.choice(list(data["names"].keys()))
        barkeep = {
            "Name": f"{random.choice(data['names'][barkeep_race]['first'])} {random.choice(data['names'][barkeep_race]['last'])}",
            "Race": barkeep_race,
            "Occupation": "Tavern Proprietor",
            "Appearance": random.choice(data["appearances"]),
            "Quirk": random.choice(data["quirks"]),
            "Secret": random.choice(data["secrets"])
        }
        
        st.subheader(f"🏠 {tavern_name}")
        st.markdown(f"*Atmosphere:* {atmosphere}")
        st.markdown(f"*Signature Drink:* **{drink}**")
        
        st.markdown("---")
        st.markdown("#### Barkeep")
        display_npc(barkeep)
        
        st.markdown("---")
        st.markdown("#### Notable Patrons")
        for _ in range(2):
            patron_race = random.choice(list(data["names"].keys()))
            patron = {
                "Name": f"{random.choice(data['names'][patron_race]['first'])} {random.choice(data['names'][patron_race]['last'])}",
                "Race": patron_race,
                "Occupation": random.choice(data["occupations"]),
                "Appearance": random.choice(data["appearances"]),
                "Quirk": random.choice(data["quirks"]),
                "Secret": random.choice(data["secrets"])
            }
            display_npc(patron)
            st.markdown("")

elif app_mode == "View Data Source":
    st.header("📂 Customization Data (`dnd_data.json`)")
    st.write("You can open `dnd_data.json` in your local code editor to add your own homebrew names, quirks, or secrets!")
    st.json(data)
