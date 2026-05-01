"""Discoverable features placed on the map at world-gen time.

Each Feature is a static definition (id, biome affinity, rarity, flavor).
A FeatureInstance is a placement of one feature at a specific tile.
"""
from __future__ import annotations

import random
from dataclasses import dataclass
from enum import Enum

from .biomes import Biome


class Rarity(Enum):
    COMMON = ("common", "white", 6)
    UNCOMMON = ("uncommon", "cyan", 3)
    RARE = ("rare", "magenta", 1)
    UNIQUE = ("unique", "bright_yellow", 1)  # placed at most once per world

    @property
    def label(self) -> str:
        return self.value[0]

    @property
    def color(self) -> str:
        return self.value[1]

    @property
    def weight(self) -> int:
        return self.value[2]


@dataclass(frozen=True)
class Feature:
    id: str
    name: str
    glyph: str
    color: str
    biome: Biome | None  # None = may appear in any biome
    rarity: Rarity
    short: str  # one-line tease shown when you arrive on the tile
    flavor: str  # longer description shown by `examine`


F = Feature


# ---- the catalogue ---------------------------------------------------------
# A broad catalogue of discoveries. Worlds still place only ~width*height/40
# instances, so any given map stays sparse even though the global pool is much
# larger.

CATALOGUE: tuple[Feature, ...] = (
    # FOREST
    F(
        "hollow_tree", "the hollow tree", "Y", "green", Biome.FOREST,
        Rarity.COMMON,
        "A tree split open from the inside, its hollow lined with soft white fur.",
        "The fur is warm and breathes very slowly. You decide not to reach inside.",
    ),
    F(
        "listening_grove", "the listening grove", "ψ", "green", Biome.FOREST,
        Rarity.UNCOMMON,
        "A clearing where the trees lean toward a single empty spot in the centre.",
        "Standing at the centre, you hear, faintly, your own thoughts spoken back to you in a voice that is almost yours.",
    ),
    F(
        "paper_birch", "the paper-skin birch", "Ϋ", "bright_white", Biome.FOREST,
        Rarity.COMMON,
        "A birch whose bark peels away in long, written sheets.",
        "The script is in no language you know, but the handwriting is unmistakably your own.",
    ),
    F(
        "moth_shrine", "the moth shrine", "✦", "magenta", Biome.FOREST,
        Rarity.RARE,
        "A cairn of antlers blanketed in pale, motionless moths.",
        "The moths do not stir when you approach. Each carries a single human eyelash on its back.",
    ),

    # RAINFOREST
    F(
        "orchid_well", "the orchid well", "❀", "magenta", Biome.RAINFOREST,
        Rarity.COMMON,
        "A round stone well choked with orchids that bloom upside down into its throat.",
        "The mossy coping is carved with survey marks from an expedition that, if the dates are true, should have been here before the country was named.",
    ),
    F(
        "rain_drum", "the rain drum", "◔", "yellow", Biome.RAINFOREST,
        Rarity.UNCOMMON,
        "A hollow log suspended by vines, beating softly though nothing touches it.",
        "Each slow knock matches a droplet falling from the canopy. Somebody once used it to warn a village that has been leaf-mulch for centuries.",
    ),
    F(
        "monkey_mask", "the lacquered monkey mask", "☉", "bright_yellow", Biome.RAINFOREST,
        Rarity.UNCOMMON,
        "A red wooden mask hangs from a vine at eye level, grinning with human teeth.",
        "The lacquer is fresh despite the damp. Inside, in charcoal, someone has written tomorrow's date and a single instruction: arrive masked.",
    ),
    F(
        "canopy_steps", "the canopy steps", "⇡", "green", Biome.RAINFOREST,
        Rarity.RARE,
        "A staircase of living roots climbs toward a platform hidden in leaves.",
        "At the top sits a table set for four astronomers. Their charts describe stars that only appear when clouds are thick enough to hide them.",
    ),

    # TAIGA
    F(
        "amber_hive", "the amber hive", "⬡", "yellow", Biome.TAIGA,
        Rarity.COMMON,
        "A beehive frozen in a bulb of amber larger than a coffin.",
        "The bees inside are perfectly preserved, each carrying a dusting of gold pollen from flowers that no longer grow this far north.",
    ),
    F(
        "needle_bell", "the needle bell", "◌", "bright_white", Biome.TAIGA,
        Rarity.UNCOMMON,
        "An iron bell hangs in a pine, its mouth packed tight with spruce needles.",
        "Pilgrims once rang it before crossing the winter road. Someone has carved a fresh tally mark in the bark for every year the road fails to return.",
    ),
    F(
        "ghost_sled", "the ghost sled", "═", "white", Biome.TAIGA,
        Rarity.COMMON,
        "A mail sled sits half-buried in snow, its runners polished by recent use.",
        "The leather satchel still inside contains letters addressed to people who are now grandparents, all stamped as if posted tomorrow.",
    ),
    F(
        "wolf_altar", "the wolf altar", "⋈", "grey50", Biome.TAIGA,
        Rarity.RARE,
        "A flat stump ringed with old teeth and fresh pine boughs.",
        "Hunters once left tribute here before winter drives. The newest offering is a silver whistle engraved with the words DO NOT USE TWICE.",
    ),

    # PLAINS
    F(
        "weather_kite", "the weather kite", "△", "bright_white", Biome.PLAINS,
        Rarity.COMMON,
        "A white kite hovers overhead on a line anchored to a bronze peg.",
        "Its fabric is stitched with pressure maps and saints' names. The string hums when storms pass three days away.",
    ),
    F(
        "mile_stone", "the mile stone", "▮", "white", Biome.PLAINS,
        Rarity.COMMON,
        "A road marker stands alone where no road survives.",
        "It lists distances to towns that are now myths, and one to a city simply named HERE measured as two miles further on.",
    ),
    F(
        "bone_windmill", "the bone windmill", "☸", "bright_white", Biome.PLAINS,
        Rarity.UNCOMMON,
        "The frame of a windmill turns slowly though it has no cloth sails left.",
        "Its vanes have been rebuilt from long pale ribs. Whoever does the repairs leaves a single coin in the hopper, paid into the wind for grain that no longer comes.",
    ),
    F(
        "camp_rings", "the camp rings", "◎", "yellow", Biome.PLAINS,
        Rarity.RARE,
        "Seven perfect ash circles lie in the grass, each still warm at the centre.",
        "An army camped here often enough to wear memory into the ground. Their fire pits relight themselves on the anniversary of a battle nobody won.",
    ),

    # SAVANNAH
    F(
        "termite_throne", "the termite throne", "♜", "yellow", Biome.SAVANNAH,
        Rarity.COMMON,
        "A termite mound has grown around an abandoned wooden chair.",
        "The arms are polished smooth by generations of kings, judges, or pranksters. The termites have left the seat itself untouched."
    ),
    F(
        "sun_ladder", "the sun ladder", "╫", "bright_yellow", Biome.SAVANNAH,
        Rarity.UNCOMMON,
        "A charred ladder leans against a flat-topped tree and rises far past its branches.",
        "Nomads once climbed it at dawn to salute the first light. The upper rungs now disappear into heat haze thick as cloth.",
    ),
    F(
        "lion_bells", "the lion bells", "♪", "yellow", Biome.SAVANNAH,
        Rarity.UNCOMMON,
        "Brass bells hang from an acacia, each one tied with old leather.",
        "Herders used them to tell lions from spirits at night. The bells ring only when nothing visible walks beneath them.",
    ),
    F(
        "ash_watering_hole", "the ash watering hole", "◒", "bright_black", Biome.SAVANNAH,
        Rarity.RARE,
        "A shallow pool reflects the sky correctly but the trees around it as burnt stumps.",
        "An entire village was said to have walked into this water during a fire and emerged years later speaking politely of a city under the soil.",
    ),

    # DESERT
    F(
        "salt_pillar", "the salt pillar", "‖", "yellow", Biome.DESERT,
        Rarity.COMMON,
        "A column of salt taller than a person, the wind has never touched.",
        "Up close, the pillar is smooth as glass and faintly warm. It hums on the same note as your bones.",
    ),
    F(
        "buried_compass", "the buried compass", "✜", "yellow", Biome.DESERT,
        Rarity.UNCOMMON,
        "Half-uncovered by the wind: a brass compass, its needle spinning lazily.",
        "The needle ignores north. It points, slowly and definitely, at you, no matter where you stand.",
    ),
    F(
        "glass_field", "the glass field", "♦", "cyan", Biome.DESERT,
        Rarity.UNCOMMON,
        "A patch of desert fused into pale green glass, the shape of a wide hand.",
        "Looking down through the glass, you see, very far below, something that looks back up.",
    ),
    F(
        "salt_chorus", "the salt chorus", "♪", "bright_yellow", Biome.DESERT,
        Rarity.RARE,
        "A ring of salt formations that whistle in slight disagreement.",
        "Stand at the centre and the whistles align into a chord. The chord is the first note of a song you almost remember.",
    ),

    # BADLANDS
    F(
        "red_obelisk", "the red obelisk", "▵", "bright_red", Biome.BADLANDS,
        Rarity.COMMON,
        "A narrow spire of baked clay stands where erosion should have claimed it long ago.",
        "Its four sides bear the same warning in four extinct alphabets. The warning appears to be about rain."
    ),
    F(
        "clay_faces", "the clay faces", "◐", "bright_red", Biome.BADLANDS,
        Rarity.UNCOMMON,
        "Dozens of faces have weathered out of the canyon wall, eyes shut against the sun.",
        "Miners once carved portraits of their dead into fresh clay and let wind decide who would be remembered. These have survived too well.",
    ),
    F(
        "echo_cistern", "the echo cistern", "◍", "cyan", Biome.BADLANDS,
        Rarity.RARE,
        "A stone cistern lies dry at the bottom of a gully, yet it echoes as if full.",
        "Speak into it and you hear replies from earlier droughts: bargaining, prayer, and a child's patient instructions on where water used to be."
    ),

    # TUNDRA
    F(
        "frozen_lantern", "the frozen lantern", "¤", "bright_white", Biome.TUNDRA,
        Rarity.COMMON,
        "A lantern, still lit, encased in a teardrop of clear ice.",
        "The flame inside has no fuel and does not flicker. The ice is cold; the lantern is not.",
    ),
    F(
        "breath_stones", "the breath-stones", "○", "bright_white", Biome.TUNDRA,
        Rarity.COMMON,
        "A ring of stones, each rimed in frost only on one side.",
        "The frost-free side of each stone is the side facing the next, as if they were exhaling at one another.",
    ),
    F(
        "ice_fish", "the suspended fish", "≺", "cyan", Biome.TUNDRA,
        Rarity.UNCOMMON,
        "A silver fish frozen mid-leap, three feet above the ground, with no ice around it.",
        "It is not held up by anything. When you walk around it, it turns to keep facing you.",
    ),
    F(
        "white_door", "the white door", "▯", "bright_white", Biome.TUNDRA,
        Rarity.RARE,
        "A door of pale wood, freestanding in the snow. No frame, no hinges visible.",
        "It opens. Behind it is more snow, identical, except for footprints leading away that are not yours.",
    ),

    # ICEFIELD
    F(
        "blue_cathedral", "the blue cathedral", "⛧", "bright_cyan", Biome.ICEFIELD,
        Rarity.COMMON,
        "Ridges of blue ice rise like nave walls around a silent central aisle.",
        "Choirs once sang here for ships trapped on the polar route. The acoustics are perfect enough that your breathing returns as harmony.",
    ),
    F(
        "anchor_in_ice", "the buried anchor", "⚓", "bright_white", Biome.ICEFIELD,
        Rarity.UNCOMMON,
        "An iron anchor is frozen upright in the ice as if dropped into water yesterday.",
        "The chain descends into a crack too narrow to admit a hand. Something below tugs on it once, politely, while you watch.",
    ),
    F(
        "frost_mirror", "the frost mirror", "▣", "cyan", Biome.ICEFIELD,
        Rarity.UNCOMMON,
        "A sheet of polished ice reflects the sky but not the land around it.",
        "Explorers used mirrors like this to navigate whiteouts. In this one, behind your shoulder, an expedition continues in good order."
    ),
    F(
        "whale_road", "the whale road", "⇔", "bright_white", Biome.ICEFIELD,
        Rarity.RARE,
        "A procession of enormous parallel grooves runs straight across the ice.",
        "A whaling guild mapped these routes when the sea used to be higher. The final groove bends upward toward the stars."
    ),

    # HILLS
    F(
        "cairn", "the watchful cairn", "▲", "bright_black", Biome.HILLS,
        Rarity.COMMON,
        "A neat cairn of stones, balanced beyond any plausible patience.",
        "Each stone, lifted, is dry on the bottom even after rain. They have not been still as long as they look.",
    ),
    F(
        "hill_eye", "the hill that opens", "◉", "bright_black", Biome.HILLS,
        Rarity.UNCOMMON,
        "A hill with a perfectly round, dry pond at its summit.",
        "When you turn your back to it, you feel observed. When you turn around, the pond is closed.",
    ),
    F(
        "kite_string", "the kite string", "│", "bright_white", Biome.HILLS,
        Rarity.RARE,
        "A taut white string rises from a stake in the ground, vanishing into the sky.",
        "Following it with your eyes makes your neck hurt and your name harder to remember.",
    ),

    # MARSH
    F(
        "reed_organ", "the reed organ", "♬", "green", Biome.MARSH,
        Rarity.COMMON,
        "A stand of reeds has been cut and bound into the shape of a pipe organ.",
        "When fog rolls in, the marsh plays itself. Old ferry schedules have been tucked between the pipes like hymns."
    ),
    F(
        "peat_door", "the peat door", "▯", "bright_black", Biome.MARSH,
        Rarity.UNCOMMON,
        "A wooden door lies half-submerged in black peat, still hanging from its frame.",
        "Bog bodies were once brought through it into a chapel on piles. The chapel is gone; the threshold remains unwilling to admit it.",
    ),
    F(
        "lantern_posts", "the lantern posts", "†", "yellow", Biome.MARSH,
        Rarity.COMMON,
        "A line of rotting posts crosses the reeds, each topped with a dark lantern.",
        "They marked the safe route to a vanished hospice. One lantern flares whenever you think about taking a wrong step.",
    ),
    F(
        "drowned_bell", "the drowned bell", "◉", "bright_yellow", Biome.MARSH,
        Rarity.RARE,
        "A bronze bell rests in knee-deep water, half swallowed by sedge.",
        "The village that owned it rang it while evacuating from a flood and never stopped; even now the metal trembles like a memory of sound."
    ),

    # BEACH
    F(
        "tide_clock", "the tide-clock", "⊙", "cyan", Biome.BEACH,
        Rarity.COMMON,
        "A barnacled brass dial, half-buried in wet sand, ticking against the tide.",
        "The dial has no numerals. Its hand is currently pointing at you, and slowly catching up.",
    ),
    F(
        "singing_shells", "the singing shells", "⌒", "cyan", Biome.BEACH,
        Rarity.COMMON,
        "A scatter of shells that hum faintly when the wind moves over them.",
        "Held to the ear, each shell plays a different name. None of them are yours; you remember them all.",
    ),
    F(
        "drifting_boat", "the drifting boat", "⌣", "bright_white", Biome.BEACH,
        Rarity.UNCOMMON,
        "A small wooden boat, beached, with no oars and a single dry footprint inside.",
        "The footprint is bare, child-sized, and faces the prow as though looking out to sea.",
    ),
    F(
        "whale_bones", "the whale-bone gate", "☋", "bright_white", Biome.BEACH,
        Rarity.UNCOMMON,
        "Two vast ribs have been planted in the sand to form a doorway toward the surf.",
        "A harbour town once walked its dead through this gate before committing them to the tide. The path beyond it remains trampled by invisible feet.",
    ),
    F(
        "salt_marionette", "the salt marionette", "☿", "magenta", Biome.BEACH,
        Rarity.RARE,
        "A child-sized puppet hangs from driftwood strings over the tideline.",
        "Its joints are crusted with salt and pearl. Tide-priests used it to teach storms good manners, with mixed success."
    ),

    # ISLAND
    F(
        "storm_orchard", "the storm orchard", "♧", "green", Biome.ISLAND,
        Rarity.COMMON,
        "Three fruit trees grow in a perfect row, all bent inland by old weather.",
        "Each year they ripen with fruit tasting of a different mainland the island has drifted past in its sleep.",
    ),
    F(
        "pilot_fire", "the pilot fire", "✺", "bright_yellow", Biome.ISLAND,
        Rarity.UNCOMMON,
        "A watchfire burns in a stone basket, untouched by wind.",
        "No fuel feeds it now. Once it guided smugglers through reefs; now it seems to be signalling patiently to something under the waves."
    ),
    F(
        "one_house", "the one house", "⌂", "white", Biome.ISLAND,
        Rarity.RARE,
        "A single house stands here with every window open and the table laid for six.",
        "Islanders tell of families who woke to find their whole village condensed into one address overnight. Nobody agrees whether this is mercy."
    ),

    # FJORD
    F(
        "chain_buoy", "the chain buoy", "⊕", "cyan", Biome.FJORD,
        Rarity.COMMON,
        "A red buoy rises and falls on a chain far thicker than a ship needs.",
        "Harbour records mention it only as NOT TO BE CUT. The chain descends into black water with the confidence of a railway line.",
    ),
    F(
        "cliff_funeral", "the cliff funeral", "⚑", "white", Biome.FJORD,
        Rarity.UNCOMMON,
        "Strips of pale cloth are tied to iron spikes hammered high into the rock.",
        "Families climbed here to say goodbye to sailors the sea refused to return. New cloth keeps appearing on calm mornings; nobody is ever seen tying it."
    ),
    F(
        "black_steps", "the black steps", "⋮", "bright_black", Biome.FJORD,
        Rarity.RARE,
        "A staircase of wet stone descends into the fjord until the water swallows it whole.",
        "Tax collectors built it to reach warehouses inside the cliff. The ledgers they carried are said to have learned to float without getting wet."
    ),

    # FARMLAND
    F(
        "scarecrow_king", "the scarecrow king", "♔", "yellow", Biome.FARMLAND,
        Rarity.COMMON,
        "A scarecrow in a rusted crown watches over several empty fields.",
        "Children from five farms once elected a king each harvest. This one won so often they buried him standing up to save time.",
    ),
    F(
        "sunken_granary", "the sunken granary", "▥", "bright_yellow", Biome.FARMLAND,
        Rarity.UNCOMMON,
        "The roof of a granary protrudes from the earth as if the building has been planted.",
        "The village stored seed here during famine years. Open cracks in the boards glow green with shoots that never break the surface."
    ),
    F(
        "clock_well", "the clock well", "⊚", "cyan", Biome.FARMLAND,
        Rarity.RARE,
        "A stone well carries twelve iron handles spaced like numerals.",
        "Turn one and the bucket rises full of water from a different season. Farmers argued for generations over which month tasted sweetest."
    ),

    # RURAL
    F(
        "empty_inn", "the empty inn", "☷", "white", Biome.RURAL,
        Rarity.COMMON,
        "A roadside inn stands open, tables set, kettles cold.",
        "Travellers' initials cover the beams up to a year that has not happened yet. Yours is already there, in your own hand, beside a date you don't remember choosing.",
    ),
    F(
        "saint_of_fences", "the saint of fences", "✝", "bright_white", Biome.RURAL,
        Rarity.UNCOMMON,
        "A weathered figure made of gate latches and horseshoes stands in a hedgerow shrine.",
        "Farmhands once prayed here for straight posts and honest neighbours. The petitions left at its feet are mostly about the latter, and increasingly underlined."
    ),
    F(
        "mail_tree", "the mail tree", "✉", "white", Biome.RURAL,
        Rarity.UNCOMMON,
        "Letters have been tucked into the splits of an old oak until the bark looks paper-scaled.",
        "Riders used the tree as a rural post office during floods. Several envelopes are addressed simply to Whoever Still Lives Nearby."
    ),

    # CITY
    F(
        "tram_without_tracks", "the tram without tracks", "═", "yellow", Biome.CITY,
        Rarity.COMMON,
        "A green tram car stands at a perfect stop though no rails reach it.",
        "Conductors kept it running after the streets were bombed out, convinced the route mattered more than the ground. A bell rings when you draw near."
    ),
    F(
        "window_market", "the window market", "▣", "magenta", Biome.CITY,
        Rarity.UNCOMMON,
        "Goods sit on windowsills all along a narrow lane: bread, needles, mirrors, a violin.",
        "Quarantined households once traded through these openings. The notes beside the objects are freshly written and far too polite."
    ),
    F(
        "ink_fountain", "the ink fountain", "✒", "cyan", Biome.CITY,
        Rarity.UNCOMMON,
        "A public fountain runs with black ink instead of water.",
        "Clerks from a vanished ministry filled their pens here. The edicts it wrote were binding enough that nearby pigeons still obey traffic law."
    ),
    F(
        "subway_stairs", "the subway stairs", "⇣", "bright_white", Biome.CITY,
        Rarity.RARE,
        "A stairwell descends beneath the street and keeps descending beyond sight.",
        "During the siege, whole neighbourhoods lived below ground. Posters on the tiled walls advertise a final train that is, according to every clock, three minutes late."
    ),

    # RUINS
    F(
        "counting_wall", "the counting wall", "▓", "magenta", Biome.RUINS,
        Rarity.COMMON,
        "A wall of fused stone marked with thousands of identical tally strokes.",
        "You count the marks and lose your place. Whatever total you arrive at, the wall has one more.",
    ),
    F(
        "kneeling_statue", "the kneeling statue", "Ω", "magenta", Biome.RUINS,
        Rarity.UNCOMMON,
        "A statue of someone kneeling, hands cupped, eyes worn smooth by weather.",
        "The cupped hands hold a small puddle of clean water that has not evaporated in any sun.",
    ),
    F(
        "locked_door", "the locked door", "‡", "magenta", Biome.RUINS,
        Rarity.UNCOMMON,
        "A doorway in a low ruin, sealed with a slab of unmarked metal warm to the touch.",
        "There is a keyhole at exactly your eye level. Looking through it, you see your own back.",
    ),
    F(
        "library_pit", "the library pit", "▤", "magenta", Biome.RUINS,
        Rarity.RARE,
        "A circular pit lined with shelves, all empty, descending out of sight.",
        "Dropping a pebble in, you never hear it land. After a long while, something throws a pebble back.",
    ),

    # VOLCANO
    F(
        "glass_monastery", "the glass monastery", "⌂", "bright_white", Biome.VOLCANO,
        Rarity.COMMON,
        "A cluster of cells fused from volcanic glass clings to the slope.",
        "Anchorites lived here to listen to the mountain think. Their prayer books were written on thin obsidian sheets still warm to the touch."
    ),
    F(
        "ash_clock", "the ash clock", "◴", "bright_red", Biome.VOLCANO,
        Rarity.UNCOMMON,
        "A bronze clock face lies half-buried in ash, its hands moving at different speeds.",
        "The city below trusted the mountain enough to set its public time by this instrument. It ran beautifully until noon lasted three days."
    ),
    F(
        "lava_orchard", "the lava orchard", "♨", "bright_yellow", Biome.VOLCANO,
        Rarity.UNCOMMON,
        "Trees of blackened stone hold fruit-shaped bulbs of red glass.",
        "Farmers planted them after the eruption to prove the valley would feed them again. Some fruit are still cooling centuries later."
    ),
    F(
        "smoke_prison", "the smoke prison", "▧", "bright_black", Biome.VOLCANO,
        Rarity.RARE,
        "Iron bars stand around a vent in the ground, locking up only smoke.",
        "The wardens believed the first plume after an eruption carried the names of the guilty. They were so committed to the idea they built a jail for it."
    ),

    # SEA
    F(
        "light_in_water", "the light in the water", "∗", "bright_cyan", Biome.SEA,
        Rarity.RARE,
        "Just offshore, a pale light hangs a few feet beneath the surface.",
        "It is the size and shape of a window. When you blink, it blinks back.",
    ),
    F(
        "buoy_of_teeth", "the buoy of teeth", "⊗", "white", Biome.SEA,
        Rarity.COMMON,
        "A navigation buoy has been ringed with careful rows of white teeth.",
        "Sailors added one for each wreck they survived. The newest tooth is gold-capped and still set in a little gum."
    ),
    F(
        "rope_bridge_below", "the rope bridge below", "≋", "cyan", Biome.SEA,
        Rarity.UNCOMMON,
        "Far beneath the clear water, a rope bridge spans between two unseen rocks.",
        "It belongs to an older shoreline drowned by earthquake or deliberate engineering. Something crossed it often enough to polish the planks."
    ),
    F(
        "drowned_observatory", "the drowned observatory", "⌬", "bright_white", Biome.SEA,
        Rarity.UNCOMMON,
        "A brass dome protrudes from the shallows, its shutter slits just above waterline.",
        "Astronomers built it to chart reflected stars. Their notebooks insist the sea has constellations of its own, seasonal and hungry."
    ),

    # OCEAN
    F(
        "white_sail", "the white sail", "△", "bright_white", Biome.OCEAN,
        Rarity.COMMON,
        "A single white sail moves on the horizon with no hull beneath it.",
        "Long-distance traders followed it for luck until too many of them arrived exactly where they had started, decades older."
    ),
    F(
        "compass_reef", "the compass reef", "✜", "cyan", Biome.OCEAN,
        Rarity.UNCOMMON,
        "Coral has grown into a perfect sixteen-point compass rose just below the surface.",
        "Pilots once sounded the reef before crossing the open ocean. The points no longer indicate direction so much as preference."
    ),
    F(
        "sleeping_colossus", "the sleeping colossus", "Ω", "bright_blue", Biome.OCEAN,
        Rarity.RARE,
        "The sea swells over a shape so large it changes the rhythm of the waves.",
        "Old naval charts mark it as a saint, a machine, and a continent depending on the edition. All agree it sometimes turns in its sleep."
    ),

    # DEEP SEA
    F(
        "trench_signal", "the trench signal", "☊", "bright_cyan", Biome.DEEP_SEA,
        Rarity.COMMON,
        "A pulse of blue light rises from impossible depth in measured intervals.",
        "Cables were once lowered here to answer it. Every message returned translated into weather reports for the moon."
    ),
    F(
        "midnight_archive", "the midnight archive", "▤", "bright_black", Biome.DEEP_SEA,
        Rarity.UNCOMMON,
        "Below the dark surface you glimpse shelves arranged in strict descending rows.",
        "A kingdom tried to save its records from fire by sinking them in sealed iron stacks. The books are said to have learned to breathe water."
    ),
    F(
        "sun_below", "the sun below", "☼", "bright_yellow", Biome.DEEP_SEA,
        Rarity.RARE,
        "Far beneath the black water burns a steady golden disc.",
        "Every culture with sailors has a story about the second sun. None agree whether it drowned, was buried, or came here on purpose."
    ),

    # ANY-BIOME
    F(
        "sleeping_traveller", "the sleeping traveller", "&", "white", None,
        Rarity.UNCOMMON,
        "A figure curled on the ground in a long coat, breathing slowly.",
        "You cannot see their face. Their coat is identical to the one you are wearing, down to the mend on the cuff.",
    ),
    F(
        "wrong_signpost", "the wrong signpost", "†", "white", None,
        Rarity.COMMON,
        "A weathered signpost with four arms, all pointing the same direction.",
        "Each arm names a different place. The direction they point is, very specifically, away from you.",
    ),
    F(
        "paper_lantern", "the paper lantern", "¤", "yellow", None,
        Rarity.COMMON,
        "A paper lantern, lit, hanging from nothing at head height.",
        "The flame has no wick. The paper is warm and bears, in pencil, a date several years from now.",
    ),
    F(
        "memory_stone", "the memory stone", "•", "bright_white", None,
        Rarity.UNCOMMON,
        "A smooth river stone resting where no river runs.",
        "Holding it, you remember a room you have never been in with great and unwelcome clarity.",
    ),
    F(
        "ghost_track", "the wrong tracks", "≡", "grey50", None,
        Rarity.COMMON,
        "Footprints in the ground that match yours exactly, walking in a slow circle.",
        "There is one more set than there should be. They join your own a few paces back.",
    ),

    # UNIQUES (at most one per world)
    F(
        "the_listener", "THE LISTENER", "Ξ", "bright_yellow", None,
        Rarity.UNIQUE,
        "A tall, thin shape in the middle distance that does not approach and does not leave.",
        "It has been here longer than the world. It is, you understand without being told, the reason the trees lean inward and the salt sings.",
    ),
    F(
        "the_door_home", "THE DOOR HOME", "Π", "bright_yellow", None,
        Rarity.UNIQUE,
        "A doorframe of dark wood, standing alone, its threshold worn by long use.",
        "Through it you can see, very faintly, your own kitchen. The light is on. Someone is moving inside.",
    ),
)


_BY_ID = {f.id: f for f in CATALOGUE}
if len(_BY_ID) != len(CATALOGUE):
    raise RuntimeError("duplicate feature ids in catalogue")


@dataclass(frozen=True)
class FeatureInstance:
    feature_id: str
    x: int
    y: int


def by_id(fid: str) -> Feature:
    return _BY_ID[fid]


def place(seed: int, width: int, height: int, tiles: tuple[tuple[Biome, ...], ...]
          ) -> tuple[FeatureInstance, ...]:
    """Place ~width*height/40 feature instances. Deterministic per seed.

    The codex (distinct feature ids placed) is capped at 25 per world: once
    that many unique discoveries exist, further placements are restricted to
    repeats of features already on the map.
    """
    rng = random.Random(seed ^ 0xFEA7)
    n = max(8, (width * height) // 40)
    codex_cap = 25
    placed: list[FeatureInstance] = []
    used_tiles: set[tuple[int, int]] = set()
    used_uniques: set[str] = set()
    distinct_ids: set[str] = set()

    # build weighted pools: per biome + any-biome
    biome_pool: dict[Biome | None, list[Feature]] = {}
    for f in CATALOGUE:
        biome_pool.setdefault(f.biome, []).extend([f] * f.rarity.weight)

    attempts = 0
    while len(placed) < n and attempts < n * 20:
        attempts += 1
        x, y = rng.randrange(width), rng.randrange(height)
        if (x, y) in used_tiles:
            continue
        b = tiles[y][x]
        # 70% chance to draw from biome-specific, else any-biome
        pool: list[Feature] = []
        if rng.random() < 0.7:
            pool = biome_pool.get(b, [])
        if not pool:
            pool = biome_pool.get(None, [])
        if not pool:
            continue
        if len(distinct_ids) >= codex_cap:
            # codex is full; only allow repeats of features already on the map
            constrained = [f for f in pool if f.id in distinct_ids]
            if not constrained:
                continue
            feat = rng.choice(constrained)
        else:
            feat = rng.choice(pool)
        if feat.rarity is Rarity.UNIQUE:
            if feat.id in used_uniques:
                continue
            used_uniques.add(feat.id)
        used_tiles.add((x, y))
        distinct_ids.add(feat.id)
        placed.append(FeatureInstance(feat.id, x, y))

    return tuple(placed)
