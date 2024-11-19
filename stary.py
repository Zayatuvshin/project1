import streamlit as st
from datetime import datetime, time
from skyfield.api import load


# Custom CSS for background
st.markdown("""
    <style>
        /* Set the background image for the entire app */
        .stApp {
            background-image: url('https://i.pinimg.com/736x/e5/c1/00/e5c1001f423256cd16627b660495ef7a.jpg');  /* Replace with your image URL */
            background-size: cover;  /* Make the image cover the entire screen */
            background-position: center;
            background-attachment: fixed;
        }

        /* Apply golden color to the title */
        .stTitle {
            color: #FFD700 !important;  /* Golden color for the title */
        }

        /* Apply golden color to markdown text */
        .stMarkdown {
            color: #FFD700 !important;  /* Golden color for markdown text */
        }

        /* Apply golden color to other text (like natal chart text) */
        .stText, .stCode, .stJson, .stDataFrame, .stTable, .stMetric, .stLabel {
            color: #FFD700 !important;  /* Golden color for other text */
        }

        /* Apply golden color to input fields */
        .stTextInput, .stTextArea, .stNumberInput, .stSelectbox, .stMultiselect, .stSlider {
            color: #FFD700 !important;  /* Golden text inside input fields */
        }


    </style>
""", unsafe_allow_html=True)


sun_sign_interpretations = {
    "Aries": "You are energetic, passionate, and full of life. Aries people are natural leaders, eager to take on challenges.",
    "Taurus": "You are practical, determined, and love stability. Taureans value comfort, security, and enjoy the finer things in life.",
    "Gemini": "You are curious, communicative, and enjoy variety. Geminis are quick-witted, always seeking new experiences.",
    "Cancer": "You are nurturing, sensitive, and protective. Cancers are deeply connected to home and family, often seeking emotional security.",
    "Leo": "You are confident, generous, and love to be in the spotlight. Leos are natural performers, radiating warmth and charisma.",
    "Virgo": "You are detail-oriented, practical, and analytical. Virgos are known for their precision, reliability, and service-oriented nature.",
    "Libra": "You are diplomatic, charming, and seek balance. Librans value fairness, beauty, and harmonious relationships.",
    "Scorpio": "You are intense, passionate, and resourceful. Scorpios are deeply emotional and often seek transformation and growth.",
    "Sagittarius": "You are adventurous, optimistic, and freedom-loving. Sagittarians seek knowledge and are always ready for new horizons.",
    "Capricorn": "You are disciplined, ambitious, and practical. Capricorns are goal-oriented, hardworking, and often very successful.",
    "Aquarius": "You are an idealistic, forward-thinking individual. You value independence and have a strong sense of individuality. Aquarians are often seen as innovative and open-minded.",
    "Pisces": "You are compassionate, empathetic, and intuitive. Pisceans are dreamers, often connected to the emotional and spiritual realms."
}

moon_sign_interpretations = {
    "Aries": "You feel things intensely and react quickly. With an Aries Moon, your emotions can be fiery and impulsive, often leading you to take immediate action in response to how you feel. You need independence and excitement, and you might have a strong desire to pioneer new emotional experiences.",
    "Taurus": "You find comfort in stability and security. A Taurus Moon seeks emotional safety and peace, often turning to routines, material comforts, and familiar surroundings for emotional reassurance. You are steady and reliable, but may resist change in your emotional life.",
    "Gemini": "Your emotions are often influenced by your thoughts, and you tend to intellectualize your feelings. A Gemini Moon loves variety and communication, and you may feel a need to talk things through in order to understand and process your emotions. You crave mental stimulation and change.",
    "Cancer": "Your emotions are deep and nurturing. A Cancer Moon feels a strong connection to home, family, and past memories. You are compassionate and empathetic, often seeking emotional security and a sense of belonging. At times, you may retreat into your shell when overwhelmed by emotions.",
    "Leo": "You seek emotional validation and love to express yourself creatively. A Leo Moon craves attention, recognition, and admiration from others. You have a generous heart and want to be loved and appreciated. Your emotional well-being is closely tied to your sense of self-worth and being admired.",
    "Virgo": "Your emotions are often practical and reserved. A Virgo Moon tends to overthink and analyze feelings, often striving to fix or improve emotional situations. You may feel emotionally fulfilled when you are helping others, organizing, or maintaining order in your life, though you may struggle with self-criticism.",
    "Libra": "You seek emotional harmony and balance in your relationships. A Libra Moon finds comfort in partnerships and may have a deep need for fairness and cooperation in their emotional life. You are diplomatic and charming, but may sometimes struggle with indecision or fear of conflict in emotional matters.",
    "Scorpio": "Your emotions run deep, and you feel things with great intensity. A Scorpio Moon is passionate, secretive, and protective of their inner world. You may experience powerful emotional highs and lows, and have an innate desire to transform emotionally. Trust is vital to you in relationships.",
    "Sagittarius": "You need freedom and exploration to feel emotionally fulfilled. A Sagittarius Moon craves adventure and new experiences. You may seek emotional satisfaction through learning, travel, or philosophical pursuits. While you are optimistic, you can sometimes avoid emotional depth or commitment in relationships.",
    "Capricorn": "Your emotions are grounded in practicality and responsibility. A Capricorn Moon seeks emotional security through achievement, stability, and structure. You may struggle with vulnerability, preferring to keep your feelings under control. You find comfort in being productive and accomplishing your goals.",
    "Aquarius": "Your emotions are intellectual and detached. An Aquarius Moon values independence and individuality, and may find it challenging to connect emotionally with others in traditional ways. You seek emotional fulfillment through unique or progressive experiences and value friendships that allow for mental stimulation.",
    "Pisces": "Your emotions are sensitive, intuitive, and deeply empathetic. A Pisces Moon feels things on a profound level and often picks up on the emotions of others. You have a strong creative or spiritual side, and your emotional life is often linked to your imagination and compassion. You may need time alone to recharge and process your feelings."
}


mercury_sign_interpretations = {
    "Aries": "You are quick-witted and sharp with your words. With Mercury in Aries, you tend to think on your feet and express your ideas rapidly. You may come across as direct and sometimes impatient, but your enthusiasm and energy in conversation are infectious.",
    "Taurus": "You have a steady, practical approach to thinking and communicating. A Taurus Mercury takes their time to process information, often valuing security and consistency in their thoughts. You may have a love for comfort and simplicity in your speech.",
    "Gemini": "Your mind is constantly active and curious. A Mercury in Gemini loves variety and may quickly adapt to new ideas and information. You are a natural communicator and love to share ideas, often moving from one topic to another with ease.",
    "Cancer": "Your thoughts are deeply influenced by emotions and intuition. A Cancer Mercury communicates in a nurturing and sensitive way, and you tend to connect with others on a personal level. Your memory is strong, and you often reflect on past experiences when thinking.",
    "Leo": "You express yourself with confidence and flair. A Leo Mercury loves to be heard and tends to speak from the heart. You have a natural ability to captivate others with your words, and you may enjoy storytelling and creative expression.",
    "Virgo": "You are analytical and detail-oriented in your thinking and communication. A Virgo Mercury is precise and enjoys organization. You may often find yourself critiquing information or providing practical advice, and you can sometimes overthink things.",
    "Libra": "You value balance and fairness in communication. A Libra Mercury seeks harmony in conversations and enjoys discussing ideas with others. You have a diplomatic approach and may struggle with making decisions because you can see multiple perspectives.",
    "Scorpio": "You have a probing mind and a knack for uncovering hidden truths. A Scorpio Mercury is intense and often communicates with purpose and depth. You may have a sharp intuition and are often interested in uncovering secrets or solving complex problems.",
    "Sagittarius": "Your thoughts are philosophical and open-minded. A Sagittarius Mercury loves to explore new ideas and share knowledge. You tend to communicate with a sense of optimism and can sometimes be blunt, but you’re always eager to learn and expand your horizons.",
    "Capricorn": "You think practically and strategically. A Capricorn Mercury is disciplined and focused on long-term goals. Your communication is often clear, structured, and serious, and you are good at making plans and working towards them step by step.",
    "Aquarius": "You are innovative and progressive in your thinking. A Mercury in Aquarius tends to think outside the box and is open to new ideas. You enjoy intellectual conversations and can sometimes be ahead of your time, preferring to focus on the bigger picture rather than the details.",
    "Pisces": "You have an imaginative and intuitive mind. A Mercury in Pisces is highly creative, often thinking in abstract or symbolic ways. You may struggle with practical communication but have a unique ability to tap into the subconscious or express yourself artistically."
}

st.markdown("### Welcome to the **Personalized Natal Chart Horoscope Generator**! 🌟")


# Function to convert Right Ascension to Zodiac Sign
def ra_to_zodiac(ra):
    zodiac_signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
                    'Libra', 'Scorpio', 'Sagittarius', 'Capricorn',
                    'Aquarius', 'Pisces']
    degrees = ra._degrees % 360  # Use `_degrees` to get RA in degrees
    sign_index = int(degrees // 30)  # Each sign spans 30 degrees
    return zodiac_signs[sign_index]


# Streamlit inputs
st.title("Stary Natal Reporter")

current_year = datetime.now().year

# Collect birth date and time
birth_date = st.date_input(
    "Enter your birth date",
    value=datetime.today(),
    min_value=datetime(1900, 1, 1),  # Minimum year is 1900
    max_value=datetime(current_year, 12, 31)  # Maximum year is current year
)
default_time = time(12, 0)  # 12:00 PM

# Collect birth time from user, with a default value of 12:00 PM
birth_time = st.time_input("Enter your birth time", value=default_time)


# Collect location (latitude, longitude)
latitude = st.number_input("Enter your latitude (e.g., 37.7749 for San Francisco)", value=37.7749)
longitude = st.number_input("Enter your longitude (e.g., -122.4194 for San Francisco)", value=-122.4194)

# Combine the birth date and time
birth_datetime = datetime.combine(birth_date, birth_time)

# Display the collected information
st.write(f"Birth Date and Time: {birth_datetime}")
st.write(f"Latitude: {latitude}, Longitude: {longitude}")

# Skyfield calculations
# Load planetary ephemeris
ephemeris = load('de421.bsp')
earth = ephemeris['earth']

# Time calculation
ts = load.timescale()
time = ts.utc(birth_datetime.year, birth_datetime.month, birth_datetime.day, birth_datetime.hour, birth_datetime.minute)

# Define planets and their corresponding targets
planets = {
    'Sun': 'SUN',
    'Moon': 'MOON',
    'Mercury': 'MERCURY',
    'Venus': 'VENUS',
    'Mars': 'MARS',
    'Jupiter': 'JUPITER BARYCENTER',
    'Saturn': 'SATURN BARYCENTER',
    'Uranus': 'URANUS BARYCENTER',
    'Neptune': 'NEPTUNE BARYCENTER',
    'Pluto': 'PLUTO BARYCENTER'
}

# Calculate planetary positions
positions = {}
for planet, target in planets.items():
    obj = ephemeris[target]
    astrometric = earth.at(time).observe(obj)
    ra, dec, _ = astrometric.radec()
    positions[planet] = ra_to_zodiac(ra)

# Display results
st.subheader("Your Natal Chart:")
for planet, sign in positions.items():
    st.write(f"{planet}: {sign}")
    
    if planet == 'Sun': 
        if sign in sun_sign_interpretations:
            st.write(f"Interpretation: {sun_sign_interpretations[sign]}")
    if planet == 'Moon': 
        if sign in moon_sign_interpretations:
            st.write(f"Interpretation: {moon_sign_interpretations[sign]}")
    if planet == 'Mercury':  
        if sign in mercury_sign_interpretations:
            st.write(f"Interpretation: {mercury_sign_interpretations[sign]}")

st.markdown("""
    ---
    **If you would like further interpretation, feel free to do Google research or contact me via email for a personalized natal chart report. Thank you! :)**
""")
