"""
build_raw_content.py — генерирует 36 исходных файлов в raw/ с оригинальными
(pre-substitution) названиями. Контент написан своими словами на базе
общеизвестных фактов о вселенной Star Wars — это заготовка, которую
substitute.py превратит в вымышленный мир «Veylarian Chronicles».

Если хочешь более реалистичный сценарий «скрейпинга», используй scrape.py —
он фетчит страницы с starwars.fandom.com через requests+BeautifulSoup.
Для сдачи задания достаточно этого скрипта.
"""

from __future__ import annotations
from pathlib import Path

RAW_DIR = Path(__file__).parent.parent / "raw"


# Каждая запись: (filename без .md, markdown-контент)
# Контент — краткое досье на сущность: 100-180 слов, факты без цитирования.
ENTRIES: list[tuple[str, str]] = [
    # ============ ПЕРСОНАЖИ (15) ============
    ("luke_skywalker", """# Luke Skywalker

## Overview
Luke Skywalker is a human male born on Tatooine, raised by his aunt and uncle on a moisture farm. He is the son of Anakin Skywalker and Padmé Amidala, and the twin brother of Leia Organa.

## Role
Luke Skywalker became one of the most influential Jedi of his generation. He played a pivotal role in the Rebel Alliance's victory over the Galactic Empire during the Galactic Civil War.

## Key Abilities
He is exceptionally strong with the Force, skilled as a pilot, and later constructed his own green-bladed lightsaber after losing the one inherited from his father.

## Relationships
- Father: Anakin Skywalker (later known as Darth Vader)
- Sister: Leia Organa
- Mentor: Obi-Wan Kenobi, later Yoda
- Close allies: Han Solo, Chewbacca, R2-D2, C-3PO

## Notable Events
Luke destroyed the first Death Star at the Battle of Yavin, trained as a Jedi on Dagobah under Master Yoda, and ultimately brought his father back from the dark side.
"""),

    ("darth_vader", """# Darth Vader

## Overview
Darth Vader is a Sith Lord who served as the enforcer of Emperor Palpatine and a key figure of the Galactic Empire. He was originally Anakin Skywalker, a Jedi Knight who fell to the dark side of the Force.

## Appearance
Vader wears a full black life-support suit and helmet after being severely injured on Mustafar. His breathing apparatus is one of his most recognizable traits. He wields a red-bladed lightsaber.

## Role
As the Emperor's apprentice, Darth Vader hunted surviving Jedi and led Imperial military operations. He commanded Star Destroyers and oversaw the construction of the Death Star.

## Family
- Wife: Padmé Amidala (deceased)
- Son: Luke Skywalker
- Daughter: Leia Organa
- Former Master: Obi-Wan Kenobi

## Fate
Darth Vader eventually turned back to the light side of the Force to save his son Luke from the Emperor, killing Palpatine and restoring balance to the Force at the cost of his own life.
"""),

    ("anakin_skywalker", """# Anakin Skywalker

## Overview
Anakin Skywalker was a human male born on Tatooine to Shmi Skywalker. Discovered by Jedi Master Qui-Gon Jinn, he was trained in the Jedi Order due to his extraordinary connection to the Force.

## Early Life
Anakin was a slave on Tatooine before being freed and brought to the Jedi Temple on Coruscant. Qui-Gon believed Anakin was the Chosen One prophesied to bring balance to the Force.

## Training
He was apprenticed to Obi-Wan Kenobi and became a skilled pilot, swordsman, and mechanic. During the Clone Wars, he served as a Jedi Knight and general of the Grand Army of the Republic.

## Relationships
- Mentor: Qui-Gon Jinn (briefly), then Obi-Wan Kenobi
- Wife: Padmé Amidala (secret marriage)
- Children: Luke Skywalker and Leia Organa

## Fall
Manipulated by Chancellor Palpatine and fearing the death of his wife, Anakin fell to the dark side of the Force and became Darth Vader.
"""),

    ("leia_organa", """# Leia Organa

## Overview
Princess Leia Organa is a human female who served as a member of the Imperial Senate, a leader of the Rebel Alliance, and later a general of the New Republic. She is the daughter of Anakin Skywalker and Padmé Amidala.

## Early Life
Adopted at birth by Bail Organa of Alderaan, Leia grew up as a princess and was raised to believe Bail and Breha Organa were her biological parents. Her twin brother Luke Skywalker was raised separately on Tatooine.

## Role in the Rebellion
Leia was instrumental in the Rebel Alliance's efforts against the Galactic Empire. She was captured aboard the Tantive IV while carrying stolen Death Star plans and later rescued by Luke Skywalker and Han Solo.

## Relationships
- Biological parents: Anakin Skywalker, Padmé Amidala
- Twin brother: Luke Skywalker
- Husband: Han Solo
- Adoptive father: Bail Organa

## Force Abilities
Leia inherited strong Force sensitivity from her father, though she trained only briefly as a Jedi.
"""),

    ("han_solo", """# Han Solo

## Overview
Han Solo is a human male smuggler and pilot, captain of the Millennium Falcon. He originally operated as an independent freighter pilot but joined the Rebel Alliance during the Galactic Civil War.

## Background
Han grew up on the streets of Corellia. He served briefly in the Imperial Navy before deserting to save a Wookiee named Chewbacca, who became his lifelong co-pilot and best friend.

## Ship
The Millennium Falcon is a heavily modified YT-1300 light freighter, famous for its speed. Han won the ship from Lando Calrissian in a card game.

## Role in the Rebellion
Hired by Obi-Wan Kenobi and Luke Skywalker to transport them to Alderaan, Han became a reluctant hero and key figure in the Rebel Alliance, participating in the Battle of Yavin and Battle of Endor.

## Family
- Wife: Leia Organa
- Son: Ben Solo
- Closest friend: Chewbacca
"""),

    ("yoda", """# Yoda

## Overview
Yoda was a legendary Jedi Master and Grand Master of the Jedi Order. A member of a mysterious species, he lived for approximately 900 years and trained Jedi for centuries, including Luke Skywalker and Count Dooku.

## Appearance
Yoda was short in stature, with green skin, long ears, and white hair in his later years. Despite his small size, he was one of the most powerful Force users ever known.

## Role in the Order
As Grand Master, Yoda led the Jedi Council on Coruscant and served as a general during the Clone Wars.

## Exile
After Order 66 and the rise of the Galactic Empire, Yoda went into exile on the swamp planet Dagobah, where he lived in seclusion until Luke Skywalker arrived for training.

## Training Luke
Yoda trained Luke Skywalker in the ways of the Force on Dagobah, teaching him Jedi philosophy and combat techniques until his death at approximately 900 years old.
"""),

    ("obi_wan_kenobi", """# Obi-Wan Kenobi

## Overview
Obi-Wan Kenobi was a human male Jedi Master who played a central role in the Clone Wars and the early Galactic Civil War. He trained Anakin Skywalker and later Luke Skywalker.

## Training
Apprenticed to Qui-Gon Jinn, Obi-Wan was knighted after his master's death on Naboo and took on Anakin Skywalker as his own Padawan.

## Clone Wars
During the Clone Wars, Obi-Wan served as a Jedi general, known for his skill in lightsaber combat and diplomatic negotiations. He was a member of the Jedi Council.

## Exile
After the fall of the Jedi Order and his duel with the fallen Anakin on Mustafar, Obi-Wan went into hiding on Tatooine, watching over Luke Skywalker from a distance.

## Final Role
Obi-Wan revealed the truth about the Force to Luke and guided him to Yoda for further training. He died during a duel with Darth Vader aboard the Death Star but continued to guide Luke as a Force ghost.
"""),

    ("emperor_palpatine", """# Emperor Palpatine

## Overview
Emperor Palpatine, also known as Darth Sidious, was the Sith Lord who orchestrated the fall of the Jedi Order, the destruction of the Galactic Republic, and the rise of the Galactic Empire. He ruled as Emperor for over two decades.

## Rise to Power
Originally a senator from Naboo, Palpatine manipulated galactic politics to become Chancellor of the Republic. He secretly controlled both sides of the Clone Wars as the Sith mastermind Darth Sidious.

## The Empire
As Emperor, Palpatine dissolved the Senate, expanded the Imperial military, and oversaw the construction of the Death Star. He ruled through fear and the loyalty of Darth Vader, his apprentice.

## Force Abilities
Palpatine was a master of the dark side of the Force, capable of generating Force lightning and deep manipulation through the Force. He wielded a red-bladed lightsaber in combat.

## Death
Palpatine was killed aboard the second Death Star when Darth Vader, turning back to the light side, threw him into the station's reactor shaft.
"""),

    ("chewbacca", """# Chewbacca

## Overview
Chewbacca is a male Wookiee from the planet Kashyyyk. He serves as co-pilot of the Millennium Falcon and is the lifelong companion of Han Solo.

## Background
Chewbacca fought in the Clone Wars as a warrior of Kashyyyk and was later enslaved by the Galactic Empire. He was freed by Han Solo, who was at the time an Imperial officer. Chewbacca pledged a life debt to Han from that moment on.

## Abilities
Chewbacca is physically powerful, standing over two meters tall, and is highly skilled as a pilot, mechanic, and warrior. He is fluent in several languages but speaks primarily in the Wookiee language Shyriiwook.

## Weapons
His signature weapon is a bowcaster, a traditional Wookiee ranged weapon.

## Role in the Rebellion
Chewbacca fought alongside the Rebel Alliance in numerous operations, including the Battle of Endor, where he helped disable the shield generator protecting the second Death Star.
"""),

    ("r2_d2", """# R2-D2

## Overview
R2-D2 is an astromech droid of the R2 series, manufactured by Industrial Automaton. Despite his small size, he played a central role in many of the galaxy's most pivotal events.

## Service History
R2-D2 served Queen Padmé Amidala of Naboo, then Anakin Skywalker and Obi-Wan Kenobi during the Clone Wars. After the fall of the Republic, he accompanied Bail Organa and eventually came into the service of Luke Skywalker.

## Design
Standing about one meter tall, R2-D2 is equipped with numerous tools including a fusion welder, computer interface arm, holographic projector, and astrogation computer. He communicates through beeps and whistles.

## Notable Deeds
R2-D2 carried the Death Star plans that were recovered by the Rebel Alliance, delivered Princess Leia's distress message to Obi-Wan Kenobi, and provided critical support during the Battle of Yavin aboard Luke Skywalker's X-wing.

## Companion
R2-D2 is frequently paired with the protocol droid C-3PO.
"""),

    ("c_3po", """# C-3PO

## Overview
C-3PO is a protocol droid fluent in over six million forms of communication. He was built by Anakin Skywalker on Tatooine as a young boy and later served the Skywalker family across multiple generations.

## Purpose
Protocol droids are designed for etiquette, translation, and diplomatic functions. C-3PO frequently served as an interpreter during tense negotiations.

## Appearance
C-3PO has a golden humanoid chassis, though one of his legs was silver for a period. He is notably anxious in personality, often worrying about odds of survival in dangerous situations.

## Service History
C-3PO served Padmé Amidala, Bail Organa on Alderaan, and later Princess Leia Organa and the Rebel Alliance. He is constantly accompanied by R2-D2.

## Role in Key Events
On Endor, the Ewoks mistook C-3PO for a deity due to his golden appearance, which helped the Rebel Alliance secure their cooperation during the Battle of Endor.
"""),

    ("boba_fett", """# Boba Fett

## Overview
Boba Fett is an unaltered genetic clone of the bounty hunter Jango Fett, raised by his father as a son rather than as a soldier. He became one of the galaxy's most feared and respected bounty hunters.

## Origin
Created on Kamino as part of the clone army program, Boba witnessed his father's death at the hands of Jedi Master Mace Windu during the Battle of Geonosis.

## Equipment
Boba wears distinctive Mandalorian-style armor inherited from his father, including a jetpack, wrist-mounted weapons, and a T-visor helmet. He pilots a ship called Slave I.

## Employment
Boba Fett was hired by Darth Vader and the Galactic Empire multiple times. He was instrumental in capturing Han Solo, who had been frozen in carbonite, and delivering him to Jabba the Hutt on Tatooine.

## Reputation
Boba Fett is considered one of the most skilled bounty hunters in the galaxy, known for his efficiency, silence, and relentless pursuit of targets.
"""),

    ("mace_windu", """# Mace Windu

## Overview
Mace Windu was a human male Jedi Master who served as a senior member of the Jedi Council during the final years of the Galactic Republic. He was known for his purple-bladed lightsaber, a rare color in the Jedi Order.

## Role in the Council
Second only to Yoda in authority on the Jedi Council, Mace Windu was a respected voice in Jedi policy and strategy during the Clone Wars.

## Combat Skills
Mace Windu created and mastered the lightsaber combat form known as Vaapad, which drew on the user's inner darkness while maintaining Jedi discipline. He was considered one of the greatest duelists in the Jedi Order.

## Clone Wars
He served as a Jedi general and led the assault on Geonosis that triggered the Clone Wars. He killed the bounty hunter Jango Fett during that battle.

## Final Duel
Mace Windu confronted Chancellor Palpatine, revealing him as the Sith Lord Darth Sidious. During the duel, Anakin Skywalker intervened on Palpatine's side, leading to Mace Windu's death.
"""),

    ("qui_gon_jinn", """# Qui-Gon Jinn

## Overview
Qui-Gon Jinn was a human male Jedi Master known for his independent thinking and strong connection to the Living Force. He was the master of Obi-Wan Kenobi.

## Philosophy
Qui-Gon often disagreed with the Jedi Council, favoring intuition and present-focused Force sensitivity over strict doctrine. He was never elevated to the Council despite his skill.

## Discovery of Anakin
On a mission to Tatooine, Qui-Gon discovered a young slave named Anakin Skywalker with an unprecedented connection to the Force. He believed Anakin was the Chosen One prophesied to bring balance to the Force.

## Combat
Qui-Gon wielded a green-bladed lightsaber and was a skilled practitioner of lightsaber Form IV.

## Death
Qui-Gon was killed on Naboo by the Sith apprentice Darth Maul during the Battle of Naboo. With his dying words, he asked Obi-Wan Kenobi to train Anakin Skywalker. He later became one of the first Jedi to retain consciousness after death through the Force.
"""),

    ("padme_amidala", """# Padmé Amidala

## Overview
Padmé Amidala was a human female politician from Naboo who served as Queen of Naboo and later as a Senator in the Galactic Senate. She was the wife of Anakin Skywalker and mother of Luke Skywalker and Leia Organa.

## Political Career
Elected Queen of Naboo at a young age, Padmé led her planet during the Trade Federation's invasion. After her term ended, she became the Senator representing Naboo in the Galactic Senate on Coruscant.

## Marriage
Padmé secretly married Anakin Skywalker during the Clone Wars, in violation of Jedi Order rules forbidding attachment.

## Beliefs
She was a fierce advocate for democracy and diplomatic solutions, opposing the militarization of the Republic even as the Clone Wars escalated.

## Death
Padmé died shortly after giving birth to twins Luke and Leia. Her body was returned to Naboo for a state funeral, where she was mourned as one of the planet's most beloved leaders.
"""),

    # ============ ПЛАНЕТЫ (8) ============
    ("tatooine", """# Tatooine

## Overview
Tatooine is a desert planet located in the Outer Rim Territories, orbiting a pair of suns. Its surface is covered almost entirely in sand, rock, and harsh desert terrain.

## Climate
The planet is notoriously hot and dry, with vast deserts, canyons, and few bodies of water. Moisture farming is a major activity, as water must be extracted from the atmosphere.

## Inhabitants
Tatooine is home to various native species including the Jawas and the Tusken Raiders, as well as human settlers, smugglers, and criminals. The Hutts, a species of crime lords, hold significant power on the planet.

## Settlements
Major settlements include Mos Eisley, a lawless spaceport, and Mos Espa. The planet also features scattered moisture farms.

## Notable Residents
Tatooine was the birthplace of Anakin Skywalker, the home of Luke Skywalker during his childhood, and the place where Obi-Wan Kenobi lived in exile after the fall of the Jedi Order.
"""),

    ("coruscant", """# Coruscant

## Overview
Coruscant is a planet-wide city located in the galactic core, serving as the capital of the Galactic Republic and later the Galactic Empire. Its entire surface is covered by a massive urban sprawl of buildings, skyscrapers, and transport systems.

## Government
Coruscant hosted the Galactic Senate and the office of the Chancellor. After the fall of the Republic, it became the seat of the Galactic Empire.

## Jedi Temple
The Jedi Temple on Coruscant was the headquarters of the Jedi Order. It housed the Jedi Council chambers, training halls, and a vast library of knowledge.

## Levels
Coruscant's city extends downward through thousands of levels. The upper levels are wealthy and well-lit, while the lower levels are dangerous, poorly regulated zones filled with crime and poverty.

## Population
Home to over a trillion inhabitants of many species, Coruscant is one of the most populous planets in the galaxy.
"""),

    ("naboo", """# Naboo

## Overview
Naboo is a lush, green planet in the Mid Rim, known for its rolling hills, plains, lakes, and classical architecture. It is the homeworld of Padmé Amidala and Emperor Palpatine.

## Inhabitants
Naboo is home to two intelligent species: the human Naboo, who live on the surface in cities like Theed, and the Gungans, an amphibious species who live in underwater cities.

## Government
Naboo's human population is led by an elected monarch, typically a young person chosen for wisdom and character. Notable queens include Padmé Amidala.

## History
The Trade Federation invaded Naboo, blockading and occupying the planet. The crisis was resolved with the help of the Jedi and the Gungan Grand Army, leading to the Battle of Naboo.

## Culture
Naboo is known for its art, architecture, and peaceful lifestyle. Theed, its capital, features grand palaces, plazas, and waterfalls.
"""),

    ("hoth", """# Hoth

## Overview
Hoth is a remote ice planet in the Outer Rim, covered entirely by snow and ice. Its frigid temperatures make it nearly uninhabitable.

## Climate
Temperatures on Hoth fall far below freezing. Massive blizzards and ice storms sweep across the planet's surface, and nighttime temperatures are lethal to most species without protective gear.

## Wildlife
Native creatures include the tauntaun, a reptomammal used as a mount by the Rebel Alliance, and the wampa, a large predator that hunts in the ice caves.

## Rebel Base
The Rebel Alliance established Echo Base on Hoth, concealed within massive ice caverns. The location was chosen for its isolation and the planet's low value as a strategic target.

## Battle of Hoth
The Galactic Empire discovered Echo Base and launched a ground assault using AT-AT walkers. The Rebel Alliance was forced to evacuate, though they successfully delayed the Imperial advance long enough for most of their forces to escape.
"""),

    ("endor", """# Endor

## Overview
Endor is a forest moon in the Outer Rim, covered in vast ancient woodlands. It is home to the Ewoks, a species of small, furry bipeds.

## Environment
The moon features towering trees, dense forest canopies, rivers, and rocky outcrops. The Ewoks build their villages high in the trees, connected by wooden walkways.

## Ewoks
The Ewoks are a primitive species skilled in woodcraft, trapping, and stone-age combat. Despite their low technology, they are brave warriors who fiercely defend their home.

## Imperial Presence
The Galactic Empire built a shield generator on Endor's surface to protect the second Death Star in orbit.

## Battle of Endor
The Rebel Alliance launched a combined operation on Endor: a ground team led by Han Solo attacked the shield generator with Ewok support, while Rebel fleet ships engaged the Imperial Navy in orbit. The resulting victory destroyed the second Death Star and killed Emperor Palpatine.
"""),

    ("dagobah", """# Dagobah

## Overview
Dagobah is a remote swamp planet in the Outer Rim, covered in bogs, mist, dense jungle, and twisted trees. The planet is rarely visited and has no settlements.

## Environment
Dagobah's surface is a perpetual mix of fog, humidity, and murky water. Visibility is low, and the local wildlife includes creatures adapted to the swamp ecosystem.

## Force Properties
Dagobah is strong in the Force, with a dark side cave that tests those who enter it. The cave reveals truths about the visitor through visions.

## Yoda's Exile
After the fall of the Jedi Order, Yoda went into hiding on Dagobah, where he lived in a small hut built from local materials. He lived alone on the planet for over two decades.

## Luke's Training
Luke Skywalker traveled to Dagobah to train under Yoda in the ways of the Force. His training included physical exercises, meditation, and confronting his own fears in the dark side cave.
"""),

    ("mustafar", """# Mustafar

## Overview
Mustafar is a volcanic planet in the Outer Rim, known for its constant eruptions, rivers of lava, and smoke-filled skies. Its surface is extremely hostile to most life.

## Environment
The planet is dominated by active volcanoes, flowing lava fields, and ash clouds. The atmosphere is thick with volcanic particulates, and the heat is extreme.

## Mining Operations
Mustafar was used for mining operations, extracting valuable minerals from its volcanic deposits. Mining facilities were built using heat-resistant materials and magnetic shielding.

## Duel on Mustafar
At the end of the Clone Wars, Obi-Wan Kenobi confronted Anakin Skywalker on Mustafar after Anakin's fall to the dark side. Their duel ended with Anakin being severely injured and mutilated by the planet's lava, leading to his transformation into Darth Vader.

## Vader's Fortress
Darth Vader later constructed a personal fortress on Mustafar, drawn to the planet by both its strategic location and its strong connection to the dark side of the Force.
"""),

    ("kamino", """# Kamino

## Overview
Kamino is a remote ocean planet in the Outer Rim, covered entirely by water. Its cities are built on stilts rising above the storm-swept seas.

## Inhabitants
The Kaminoans are a tall, slender species with long necks and elongated faces. They are known for their advanced cloning technology and their careful, reserved demeanor.

## Cloning Facilities
Kamino is the galactic center for cloning technology. The Kaminoans produced the Clone Army used by the Galactic Republic during the Clone Wars, using the bounty hunter Jango Fett as the genetic template.

## Climate
Kamino experiences constant heavy rain and storms, with massive waves crashing against the supports of its cities. The weather is rarely calm.

## Strategic Importance
The discovery of Kamino and its clone army triggered the outbreak of the Clone Wars. After the rise of the Empire, Kamino's cloning facilities declined in importance as the Empire transitioned to recruited stormtroopers.
"""),

    # ============ КОРАБЛИ И ТЕХНОЛОГИИ (6) ============
    ("death_star", """# Death Star

## Overview
The Death Star is a moon-sized battle station built by the Galactic Empire, designed as the ultimate weapon of intimidation and power projection. Two versions of the Death Star were constructed during the Galactic Civil War.

## Weapon
The Death Star's primary weapon is a superlaser capable of destroying an entire planet with a single shot. The weapon is powered by multiple focusing kyber crystals and requires significant recharge time between shots.

## Defenses
The station is protected by thousands of turbolaser batteries, ion cannons, TIE fighters, and a planetary shield. Its hull is kilometers thick.

## First Death Star
Used to destroy Alderaan as a demonstration of power, the first Death Star was ultimately destroyed at the Battle of Yavin when Luke Skywalker fired proton torpedoes into a thermal exhaust port, triggering a chain reaction.

## Second Death Star
A larger and more powerful version, the second Death Star was destroyed at the Battle of Endor when the Rebel Alliance disabled its shield generator and fighters penetrated to its reactor core.
"""),

    ("millennium_falcon", """# Millennium Falcon

## Overview
The Millennium Falcon is a heavily modified YT-1300 light freighter, one of the most famous starships of the Galactic Civil War era. It is captained by Han Solo with Chewbacca as co-pilot.

## Modifications
Though the YT-1300 model is commercially unremarkable, the Millennium Falcon has been extensively modified with a military-grade hyperdrive, upgraded weapons, reinforced hull plating, and smuggling compartments.

## Speed
The ship is famed for its speed. Han Solo claims the Falcon made the Kessel Run in less than twelve parsecs, using a dangerous shortcut through hazardous space.

## History
The ship was originally owned by Lando Calrissian, who lost it to Han Solo in a game of sabacc. The Falcon has changed hands several times but always returns to Han.

## Notable Battles
The Millennium Falcon participated in the Battle of Yavin, the escape from Hoth, and the Battle of Endor, where Lando Calrissian piloted it to destroy the second Death Star's reactor core.
"""),

    ("x_wing_starfighter", """# X-wing starfighter

## Overview
The X-wing starfighter, officially the T-65 X-wing, is a single-pilot starfighter produced by Incom Corporation. It became the signature fighter of the Rebel Alliance during the Galactic Civil War.

## Design
The fighter is named for its wings, which split into an X-shape during combat to allow wider firing angles and better heat dissipation. Each wingtip mounts a laser cannon.

## Armament
X-wing starfighters are equipped with four laser cannons and two proton torpedo launchers. They also feature a hyperdrive, allowing for independent travel between star systems.

## Astromech
Each X-wing carries an astromech droid that assists with navigation, repairs, and system monitoring. Luke Skywalker's astromech was R2-D2.

## Notable Engagements
X-wing starfighters played central roles in the Battle of Yavin (destroying the first Death Star), the Battle of Hoth evacuation, and the Battle of Endor. They became symbols of the Rebel Alliance's resistance.
"""),

    ("tie_fighter", """# TIE fighter

## Overview
The TIE fighter is the standard starfighter of the Galactic Empire, produced in massive numbers and deployed from Star Destroyers and other Imperial vessels. Its name comes from its twin ion engines.

## Design
The TIE fighter features a spherical cockpit flanked by two hexagonal solar collection panels. It has no hyperdrive and minimal life support, relying on its carrier ship for deep-space operations.

## Tactics
TIE fighters rely on speed, agility, and overwhelming numbers rather than individual durability. They are unshielded and lightly armored, making them vulnerable but cheap to produce and easy to replace.

## Variants
Variants include the TIE interceptor (faster and more maneuverable), the TIE bomber (equipped for heavy ordnance), and TIE Advanced x1 (flown by Darth Vader), which has a hyperdrive and improved shielding.

## Pilots
TIE fighter pilots are typically trained at Imperial academies and deployed in squadrons. Their survival rate is notoriously low due to the fighter's fragility.
"""),

    ("imperial_star_destroyer", """# Imperial Star Destroyer

## Overview
The Imperial Star Destroyer is the primary capital ship of the Galactic Empire. Its distinctive wedge-shaped silhouette became a symbol of Imperial power across the galaxy.

## Dimensions
Imperial-class Star Destroyers measure approximately 1,600 meters in length. They house thousands of crew and can carry multiple squadrons of TIE fighters, AT-AT walkers, and landing craft.

## Armament
Star Destroyers carry dozens of turbolaser batteries, ion cannons, tractor beam projectors, and point-defense weapons. They are capable of engaging both capital ships and ground targets from orbit.

## Role
Star Destroyers serve as both warships and mobile bases. They enforce Imperial authority across sectors, ferry troops, and engage enemy fleets. The Executor, Darth Vader's personal flagship, was a Super Star Destroyer far larger than standard models.

## Weakness
Despite their power, Star Destroyers rely on shield generators mounted on their upper hulls. Fighter attacks targeting these generators, as occurred at the Battle of Endor, could disable the ships.
"""),

    ("lightsaber", """# Lightsaber

## Overview
The lightsaber is the signature weapon of the Jedi and Sith, consisting of a hilt that emits a blade of contained plasma. It is simultaneously elegant and devastatingly powerful.

## Construction
A lightsaber is powered by a kyber crystal, a Force-attuned crystal that focuses the plasma blade. Construction of a lightsaber is traditionally a rite of passage for a Jedi Padawan, involving personal attunement to the crystal.

## Blade Colors
The color of a lightsaber blade is determined by the kyber crystal. Common Jedi colors include blue and green, while yellow is associated with Jedi Sentinels. Sith lightsabers are red, produced by "bleeding" a kyber crystal through dark side intent.

## Combat Forms
Multiple lightsaber combat forms exist, each with different philosophies. Form V emphasizes power, Form IV emphasizes acrobatics, and Form III emphasizes pure defense.

## Cultural Significance
The lightsaber is one of the most iconic weapons in the galaxy. Only those who can wield the Force can use it effectively, as mastery requires Force-enhanced reflexes and awareness.
"""),

    # ============ ФРАКЦИИ И ОРДЕНА (4) ============
    ("jedi_order", """# Jedi Order

## Overview
The Jedi Order is an ancient monastic and peacekeeping organization of Force users dedicated to the light side of the Force. The Jedi served the Galactic Republic as guardians of peace and justice for thousands of years.

## Structure
The Order was led by the Jedi Council, composed of twelve Jedi Masters, with Yoda serving as Grand Master. The headquarters was the Jedi Temple on Coruscant.

## Training
Prospective Jedi were identified as young children through their Force sensitivity. They progressed through ranks of Youngling, Padawan, Jedi Knight, and Jedi Master.

## Code
The Jedi Code emphasized peace, serenity, harmony, and service. Jedi were forbidden from forming attachments, including marriage, and were expected to control their emotions to avoid the dark side.

## Fall of the Jedi
At the end of the Clone Wars, the Jedi Order was nearly destroyed by Order 66, an Imperial directive that caused the clone troopers to turn on their Jedi generals. Only a handful of Jedi survived, including Yoda and Obi-Wan Kenobi.
"""),

    ("sith_order", """# Sith Order

## Overview
The Sith Order is an ancient organization of Force users dedicated to the dark side. For millennia, the Sith were enemies of the Jedi, driven by pursuit of power, passion, and domination.

## Rule of Two
For the thousand years preceding the Galactic Civil War, the Sith followed the Rule of Two: at any time, there would exist only one master and one apprentice. This rule was established to prevent the infighting that had nearly destroyed the Sith in ancient times.

## Philosophy
The Sith embrace passion, strength, power, and victory. Where the Jedi seek peace through emotional discipline, the Sith seek strength through emotional intensity, particularly anger, hatred, and fear.

## Notable Sith
During the fall of the Republic, Darth Sidious (Emperor Palpatine) served as master, with apprentices including Darth Maul, Count Dooku, and finally Darth Vader.

## Weapons
Sith wielded red-bladed lightsabers, produced by corrupting a kyber crystal through the dark side. Their use of the Force included abilities like Force lightning and Force choke.
"""),

    ("galactic_empire", """# Galactic Empire

## Overview
The Galactic Empire was an authoritarian galactic government established by Emperor Palpatine at the end of the Clone Wars. It replaced the Galactic Republic and ruled the galaxy for over two decades.

## Rise
The Empire was declared by Chancellor Palpatine after the elimination of the Jedi Order through Order 66. Palpatine cited the threat of Jedi treason and the need for a stronger, more centralized government.

## Government
The Empire was ruled by the Emperor with absolute authority. The Imperial Senate remained briefly as a facade of representation but was dissolved around the time of the Battle of Yavin. Regional Governors, or Moffs, administered sectors of the galaxy.

## Military
The Imperial military included the Imperial Navy (Star Destroyers and TIE fighters), Imperial Army (stormtroopers and walkers), and specialized units. At its peak, the Empire deployed over twenty-five thousand Star Destroyers.

## Fall
The Empire collapsed after the Battle of Endor, in which Emperor Palpatine and Darth Vader were killed and the second Death Star was destroyed. Remnant Imperial forces fought on for several years before formal surrender.
"""),

    ("rebel_alliance", """# Rebel Alliance

## Overview
The Rebel Alliance, formally the Alliance to Restore the Republic, was a resistance movement opposing the Galactic Empire. It fought the Galactic Civil War against Imperial forces and ultimately triumphed.

## Formation
The Rebel Alliance was formed by disparate resistance groups unified under a common cause. Founders included Bail Organa of Alderaan, Mon Mothma of Chandrila, and others who opposed Imperial tyranny.

## Leadership
Mon Mothma served as the Alliance's chief political leader. Military operations were coordinated by commanders including General Dodonna, Admiral Ackbar, and later Princess Leia Organa and General Han Solo.

## Forces
The Rebel Alliance fielded X-wing starfighters, Y-wing bombers, A-wings, B-wings, corvettes, and cruisers. Its ground forces were drawn from volunteers across many worlds.

## Major Victories
Key victories included the Battle of Scarif (capturing the Death Star plans), the Battle of Yavin (destroying the first Death Star), and the Battle of Endor (destroying the second Death Star and killing Emperor Palpatine).
"""),

    # ============ КОНЦЕПЦИИ (3) ============
    ("the_force", """# The Force

## Overview
The Force is an energy field that connects all living things in the galaxy. It is the source of power for Jedi and Sith alike, and understanding of the Force has shaped galactic civilization for tens of thousands of years.

## Two Sides
The Force has two aspects: the light side, associated with peace, serenity, and selflessness, and the dark side, associated with passion, anger, and hatred. The light side is practiced by the Jedi, the dark side by the Sith.

## Abilities
Force users can perform feats beyond normal physical limits, including telekinesis, enhanced reflexes, mind influence, precognition, and healing. Dark side practitioners can additionally produce Force lightning and other destructive abilities.

## Sensitivity
Only certain individuals are strong enough with the Force to use it actively. Force sensitivity is partly hereditary but can appear in unexpected lineages. The Jedi traditionally identified Force-sensitive children early in life.

## Philosophy
The Jedi view the Force as a gift to be used in service of others, while the Sith view it as a power to be harnessed for personal dominion. Balance between the two remains a subject of philosophical dispute.
"""),

    ("kyber_crystal", """# Kyber crystal

## Overview
A kyber crystal is a rare, Force-attuned crystal used primarily to power lightsabers. Kyber crystals also serve as focusing elements for much larger weapons, including the superlaser of the Death Star.

## Origin
Kyber crystals are found on various planets across the galaxy, most notably Ilum and later Jedha. They grow naturally, attuned to the Force from the moment of formation.

## Personal Attunement
Kyber crystals are colorless until bonded to a Force user. Upon bonding, the crystal takes on a color that reflects the user and their relationship to the Force. Jedi crystals typically appear blue or green; yellow occurs among Jedi Sentinels.

## Corruption
A Sith produces a red crystal through a process called "bleeding," in which the user's dark side intent corrupts the crystal's natural resonance. This process is painful for the crystal and requires deep focus on hatred and anger.

## Military Use
The Galactic Empire harvested kyber crystals in massive quantities to power the Death Star's superlaser. This required the enslavement of mining populations on Jedha and elsewhere.
"""),

    ("hyperdrive", """# Hyperdrive

## Overview
The hyperdrive is a faster-than-light propulsion technology that allows starships to travel between star systems in reasonable timeframes. It is the foundation of galactic civilization, trade, and warfare.

## Function
The hyperdrive propels a ship into hyperspace, an alternate dimension where travel between widely separated points becomes possible. Ships follow established hyperspace lanes that have been mapped and verified as safe.

## Classes
Hyperdrives are rated by class, with lower numbers indicating faster drives. A Class 1.0 hyperdrive is military-grade, while civilian ships typically have Class 2.0 or slower drives. The Millennium Falcon is famously equipped with a Class 0.5 hyperdrive.

## Navigation
Hyperspace navigation requires precise calculations to avoid mass shadows, which can pull ships out of hyperspace and destroy them. Astromech droids typically handle these calculations aboard small starfighters.

## Limitations
A hyperdrive cannot be used within a planet's gravity well. Ships must first travel to a safe distance from planetary masses before engaging the hyperdrive. Some Imperial ships are equipped with interdictor technology that can artificially pull enemy ships out of hyperspace.
"""),
]


def main() -> None:
    RAW_DIR.mkdir(exist_ok=True)
    for filename, content in ENTRIES:
        path = RAW_DIR / f"{filename}.md"
        path.write_text(content.strip() + "\n", encoding="utf-8")
    print(f"Создано {len(ENTRIES)} файлов в {RAW_DIR}")


if __name__ == "__main__":
    main()
