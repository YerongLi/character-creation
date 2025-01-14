completion_prompt = """
Instruction:
For each of the following examples, generate detailed character personas that fit the context. Each character should have a name and a detailed persona with their job and relevant personality traits. You can generate the personas for any individuals who would logically be part of the scene and contribute to it in some way.

Example 1:
On November 18, 1986, friends dropped Helle off at the couple's Newtown residence after she had worked a long flight from Frankfurt, West Germany. She was never seen again. That night, a snowstorm hit the area. The next morning, Richard said he was taking Helle and their children to his sister's house in Westport. When he arrived, Helle was not with him. Over the next few weeks, Richard gave Helle's friends a variety of stories as to why they were unable to reach her: that she was visiting her mother in Denmark, that she was visiting the Canary Islands with a friend, or that he simply did not know her whereabouts. Helle's friends were aware that Richard had a volatile temper and grew concerned. Helle had told some of them, "If something happens to me, don't assume it was an accident." On December 1, the private investigator Keith Mayo reported her missing to the Newtown Police. Richard Crafts was known to local law enforcement for his work as a volunteer police officer in Newtown, and in 1986 Crafts was working as a part-time police officer in the nearby town of Southbury. According to Mayo, Newtown Police initially dismissed his concerns, saying that Helle would probably return.

Character Personas:
[
  {
    "name": "Helle Anderson",
    "personas": [
      "I am a 37-year-old flight attendant who is dedicated to my demanding job and works long international flights.",
      "I am cautious and perceptive, always aware of potential dangers and prepared to address challenges."
    ]
  },
  {
    "name": "Richard Crafts",
    "personas": [
      "I am a retired FBI agent and part-time police officer who is experienced and knowledgeable in law enforcement.",
      "I am assertive and confident, often using my skills to navigate complex situations.",
      "I am known for my strong personality, which some might describe as intense or difficult to handle."
    ]
  },
  {
    "name": "Anna Peterson",
    "personas": [
      "I am the family's nanny, caring and attentive to the children I look after.",
      "I am observant and detail-oriented, always paying attention to my surroundings.",
      "I am reliable and trustworthy, often acting as a steady presence in the household."
    ]
  },
  {
    "name": "Sarah Mitchell",
    "personas": [
      "I am a 37-year-old receptionist at the airport and one of Helle’s close friends, supportive and loyal to her in both good and challenging times.",
      "I am perceptive and empathetic, quickly noticing when something feels off or wrong.",
      "I am proactive and determined, ready to act on my concerns when I feel someone I care about is in danger."
    ]
  },
  {
    "name": "John Harris",
    "personas": [
      "I am the couple’s neighbor, unemployed, and spend most of my time at home.",
      "I am in my mid-50s, I get up early in the morning and start my day by exercising, mostly walking or light jogging.",
      "I am observant of my surroundings but keep to myself, rarely getting involved with the personal matters of my neighbors unless I feel it's necessary."
    ]
  },
  {
    "name": "Mark Thompson",
    "personas": [
      "I am a colleague of Richard’s from law enforcement, experienced in the field and highly reliable.",
      "I have a criminal record, having been involved in some shady activities in the past, though I have managed to keep that part of my life hidden from most people.",
      "I tend to keep a professional distance from others, focusing on my work while being aware of my own history."
    ]
  },
  {
    "name": "Linda Scott",
    "personas": [
      "I am a 30-year-old mother of one child, working in law enforcement as a colleague of Richard’s.",
      "I have recently gone through a divorce, which has been difficult but also a time of personal growth for me.",
      "I am analytical and methodical in my approach to solving cases, and I often question decisions when I notice inconsistencies, especially if they remind me of my own recent experiences."
    ]
  }
]

Example 2:
On a recent afternoon in Chicago, two tow trucks arrived at the scene of a broken-down Toyota Corolla. The drivers, each claiming the tow, began ramming their vehicles into each other in a violent confrontation. The situation escalated when one driver shattered the windshield of the other truck. The incident disrupted traffic, with pedestrians recording the altercation. Law enforcement arrived to separate the drivers and restore order.

Evidence:
- Two tow trucks arrived for the same broken-down car.
- Drivers rammed their vehicles into each other.
- One truck's windshield was shattered.
- Pedestrians filmed the incident.
- Police intervened to separate the drivers.

Character Personas:
[
  {
    "name": "Jeremy Howard",
    "personas": [
      "I am a strong and assertive tow truck driver, often used to taking charge in difficult situations.",
      "I have a deep sense of pride in my work as a tow truck driver and don't easily back down from challenges.",
      "I value my reputation in the industry and believe in getting the job done, even if it means confronting others."
    ]
  },
  {
    "name": "Dylan Carter",
    "personas": [
      "I am a quick-witted and sometimes aggressive tow truck driver, not afraid to speak my mind and stand my ground.",
      "I have a competitive nature, especially when it comes to situations like this, and I don’t like to lose.",
      "I pride myself on being resourceful, using whatever means necessary to achieve my goals as a tow truck driver."
    ]
  },
  {
    "name": "Ella Davis",
    "personas": [
      "I am a Subway employee in my mid-20s, used to managing difficult customers, but this was something else.",
      "I’m detail-oriented and observant, often noticing things happening around me even when I’m busy.",
      "I am calm under pressure, but I was shocked by the intense situation that unfolded right outside my workplace."
    ]
  },
  {
    "name": "Mia Thompson",
    "personas": [
      "I am an 18-year-old university student, usually minding my own business.",
      "I am often curious about what’s going on around me and love documenting interesting moments, especially when they’re out of the ordinary.",
      "I have a strong sense of justice and couldn’t help but feel unsettled by the aggressive behavior of the tow truck drivers."
    ]
  },
  {
    "name": "Ethan Parker",
    "personas": [
      "I am a 19-year-old university student, observant and easygoing. I usually enjoy watching things unfold, especially when I’m not directly involved.",
      "I tend to stay neutral in conflicts, but this situation was intense enough to make me feel uncomfortable.",
      "I’m social, but I knew this event would be something worth remembering and sharing with others later."
    ]
  }
]

Example 3:
{scene}

Character Personas:
"""
def read_and_fill_prompt():
    # Open files 1.txt, 2.txt, etc., and loop through each file
    file_numbers = [1, 2, 3, 4, 5, 6]  # Adjust this as necessary for your files
    for i in file_numbers:
        # Read the scene content from the file
        with open(f'{i}.txt', 'r') as file:
            scene_content = file.read()

        # Fill the scene content into the prompt template
        filled_prompt = completion_prompt_template.replace("{scene}", scene_content)
        
        # Print the filled prompt
        print(filled_prompt)
        
        # Wait for user to press Enter to continue
        input("Press Enter to continue to the next scene...")

# Call the function to start the process
read_and_fill_prompt()