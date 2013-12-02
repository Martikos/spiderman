import pprint
from difflib import SequenceMatcher

# http://python-cluster.sourceforge.net/
from cluster import HierarchicalClustering

# input urls to be clustered

urls = [
    '365 DAYS of AWESOME (GOPRO 2012)',
    'GoPro HERO3+ vs. HERO3 Comparison and Review',
    'GoPro Hero 3 Black: How To Start Using',
    'GoPro: Lost in Peru',
    'GoPro Hero 3 Black Edition Slow Motion 240fps Test NO TWIXTOR',
    'Honda World Motocross skids and wheelies - Nils factory visit',
    'TEAM ROCKSTAR  BUD RACING KAWASAKI (2013 official)',
    'GoPro Mounts Tips & Tricks part 1 of 3 HD',
    'GoPro HD Hero3 Black vs. Silver vs. Hero2 Visual Comparison',
    'GoPro: Slowing Down the Summer',
    'GoPro Hero3 Burst Tutorial: How To Make A Sequence In Photoshop',
    'GoPro Hero 3 Wifi Range Test With Smartphone App',
    'How GoPro Made A Billionaire',
    'CANADIAN SUMMER PARTY (GoPro Hero3 Black)',
    'Tip #17 GoPro - how to film steady with GoPole pole (with dachshunds)',
    'GoPro HD Hero3 White vs Sony HDR-AS10 - The ULTIMATE Action Cam REVIEW',
    'Who is JOB 3.0 - Sewer Surfing w/ Poopies - Ep 6',
    'GoPro: Director"s Cut - Shark Riders',
    'AWESOME HD GOPRO HERO3 2013 - Extreme Sports 2013',
    'Tip #245 GoPro - Hero 3+ vs Hero 3 Black Comparison',
    'GoPro: Combing Valparaiso"s Hills',
    'GoPro: Red Bull Rampage - 2012',
    'GoPro Hero 3 Slow Mo Tutorial using FREE software',
    'GoPro HD: Bombsquad Goes Norway with Neil Amonson',
    'GoPro Hero 3 Wifi connectivity with an iPhone - Setup demo',
    'GoPro + F18 = AWESOME',
    'GoPro Hero 3: Black Edition (Why I am returning it)',
    'Tip #80 GoPro - Wi-Fi vs Water',
    'Bigest wave in the world surfed, Carlos Burle, World record 100ft at 02:50min rogue wave',
    'GoPro HD: Skateboard Big Air with Andy Mac - X Games 16',
    'Action Cam Battle: Hero 3 Black vs Contour+2 vs Sony Action Cam vs Drift Ghost',
    'Motocross is Beautiful 2013',
    'DC SHOES: KEN BLOCK"S GYMKHANA FIVE: ULTIMATE URBAN PLAYGROUND; SAN FRANCISCO',
    'GoPro HD HERO Camera: Crankworx Whistler - Mike Montgomery"s Slopestyle Run',
    'Skydive Dubai - May 2011',
    '2012 X-Games 18 motocross best trick',
    'Tip #120 GoPro - How to avoid the water spot on lens',
    '52 GoPro Cameras, puppies, and girls! BTS with Orapup!',
    'Lost GoPro HD Hero Cam found after 2.5 months at Sea.mp4',
    'Tip #100 GoPro - My favorite mount for GoPro - Phantom!',
    '1080p 60fps 60p GoPro Hero3 vs Sony Action Cam Comparison',
    'GoPro F18 Fighter Jet',
    'GoPro: Alana Blanchard Surfer Girl On Network A',
    'How To Make A GoPro Pan Tilt Time-Lapse Rig',
    'GoPro Hero 3 Time Lapse Tutorial',
    'GoPro HD: Ryan Villopoto Full Moto 2 - Muddy Creek Lucas Oil Pro Motocross Championship 2013',
    'Hawaii Adventure - GoPro Hero 3',
    'GoPro Hero 3 Black Edition LCD TOUCH BacPac UNBOXING & DEMO',
    'GoPro: Jeb Corliss Flies Through Tianmen Cave',
    'GoPro Hero3 Black vs Sony Action Cam VIDEO comparison',
    'Gopro Hero3 240fps Slow motion test',
    'PEOPLE ARE AWESOME AMAZINGTAGES',
    'GoPro Studio 2.0 Basics: GoPro Tips and Tricks',
    'How to Build GoPro Steadycam for Under $20',
    'Barracuda 33 kg attaque - Chasse sous-marine GoPro HD - Spearfishing',
    '2013 AMA 450 Supercross Rd 14 Minneapolis HD 720p',
    'Tip #175 GoPro - Build a Helmet Arm Extension Mount!',
    'Tip #205 GoPro - What Resolutions MicBergsma Uses?',
    'PEOPLE ARE AWESOME 2013-EXTREME PEOPLE 2013 GOPRO HERO 3',
    'Ryan Villopoto - A Champion - Part 2',
    'cliff jumps',
    'Tips for Saving Battery life: GoPro Tips and Tricks',
    'Ryan Villopoto - A Champion - Part 1',
    'GoPro Hero3+ Normal versus "SuperView" modes compared',
    'Tip #254 GoPro - This is how I pack / travel with GoPro stuff',
    'My Vacation in Australia GoPro HD Hero 2',
    'Dirt Shark - "RAIL THE FARM" VILLOPOTO WEIMER CIANCIARULO',
    'USA Roadtrip 2012 - Our First Month With GoPro',
    'Sony Action Cam Review - Can it best GoPro at their own game?',
    'How to use Macro filters with a Hero3 and min focus tests',
    '2013 Pro Motocross Prep at Lake Elsinore',
    'Ironman Triathlon Motivation - Kona World Championships NBC Highlights',
    'GoPro Hero3 Pelican 1500 Case',
    'GoPro Hero3 Black VS iON Air Pro HD - Action Cam SHOOT-OUT!',
    'CBR 600 RR vs R6 vs C 63 AMG Coupe TOP SPEED [1080p - GoPro Hero]',
    'Tip #265 GoPro - SRP Polarzier filter - Why do I use them?',
    'GoPro HD: Dreams with Kelia Moniz - Roxy Wahine Classic 2011',
    'GoPro Hero 3 : LCD Touch BacPac - Unbox & Full Review',
    'Tip #226 GoPro - New Version 3rd Person View Mount',
    'Go Pro Hero3 Black Edition in Pelican 1400 Case Setup & Short Review',
    'GoPro HD: Ryan Villopoto Main Event 2013 Daytona Supercross',
    'James Stewart"s Supercross Training for 2013 Season',
    'Tip #154 GoPro - My GoPro Rig Setup',
    'GoPro HD Hero: Top Dragster 6.60 @ 208 mph!',
    'Flying Underwater - Dive Wing Hawaii with GoPro Hero 3 Black and Hero 2',
    'GoPro HD: Avalanche Cliff Jump with Matthias Giraud',
    'Protune Video - How to use it and what it does - GoPro Hero3',
    'GoPro Hero 3 Black Custom Case (Pelican 1500)',
    'New GoPro HERO3+ All you need to know',
    'IRONMAN - Be Inspired',
    'GoPro HERO3 Kit (Pelican 1500 Case)',
    'GoPro: DeepFlight Submersible - Searching for Whale Song',
    'GoPro: Lion Hug',
    'GoPro HD: Shark Riders - Introducing GoPro"s New Dive Housing',
    'Hawaii The Big Island - GoPro HERO3: Black Edition',
    'GoPro Hero 3 - Everything You Need To Know',
    'GoPro Hero 3 - Mounting Tips & Tricks!',
    'PEOPLE ARE AWESOME 2013 [NEW VERSION]',
    'All 2013 AMA Supercross Crashes',
    'GoPro HD: Jeb Corliss and Roberta Mancino - Wingsuit Flyers',
    'GoPro HD: Antonio Cairoli 2013 FIM MX World Motocross in Qatar',
    'GoPro DIY Pan Tilt Time-lapse Rig Demonstration',
    'Red Bull Rampage 2012 USA Full Recap',
    'Tip #122 GoPro Hero 3 - Test mounts with Floaty backdoor in water',
    'GoPro Hero3 vs Hero3+ (Black Edition) Review / Comparison - Should You Upgrade?',
    'GoPro: Masters of Indo',
    'Sony Action Cam vs GoPro Hero3 Black Comparison Video COMPLETE!!!',
    'Tip #263 GoPro - SRP Macro Filter to get amazing close-up!',
    'GoPro Pelican 1450 Case - Setup and Review',
    'GoPro HERO3: Black Edition vs HERO2 (Underwater Comparison)',
    'Which GoPro Should you buy? Hero3 Black, Silver or White Edition or Hero2',
    'Tip #271 GoPro - Explaining about BlurFix3+ 55 Adapter',
    'People Are Awesome 2013 - Ultimate Version',
    'ULTIMATE GoPro Hero3+ BLACK vs Hero3+ SILVER ++',
    '2013 AMA Supercross Rd 4 Oakland - 450 Full Event - HD 720p',
    'Nuclear Tower & USA Base Jumps | Base Dreams | Ep 2',
    'Motos esportivas acelerando em Curitiba - Parte 14',
    'WettieTV - Interpacific Spearfishing Champs 2013',
    'Between a rock and a hard place: sailing boat crash...',
    'Cat with GoPro',
    '10 Angry Goalkeepers',
    'GoPro Hero 3+ and DJI Phantom ~ Hawaii Adventures ~ Cliff Jumping and Sunset Flights',
    'How to make an LED Light / GoPro Hero Camera Rig - To get decent video in Caves.',
    'Olivia Testing A Steadicam Glidecam setup',
    'GoPro HERO 3 vs Contour+ 2 review - Auto Express',
    'FPV QUADCOPTER  GOPRO HD 2',
    '2013 Monster Energy AMA Supercross, an FIM World Championship - St Louis - (USA)',
    'James Bubba Stewart fights from last place to first',
    'Marlin Sinks Fishing Boat? Vessel Capsizes After Hooking Huge Fish',
    'Scout sniper Marines during Operation Helmand Viper. Afghanistan COMBAT FOOTAGE!',
    'GoPro: Lost in Peru',
    'GoPro HD Hero3 White vs Sony HDR-AS10 - The ULTIMATE Action Cam REVIEW',
    'Who is JOB 3.0 - Sewer Surfing w/ Poopies - Ep 6',
    'GoPro: Directors Cut - Shark Riders',
    'Tip #17 GoPro - how to film steady with GoPole pole (with dachshunds)',
    'GoPro Hero 3 Wifi Range Test With Smartphone App',
    'GoPro + F18 = AWESOME',
    'RotoR Helmet Swivel Mount 360 Official Tutorial GoPro Accessory Set Up Review How To Film Yourself',
    'GoPro HD HERO Camera: Crankworx Whistler - Mike Montgomery Slopestyle Run',
    'Bigest wave in the world surfed, Carlos Burle, World record 100ft at 02:50min rogue wave',
    'Action Cam Battle: Hero 3 Black vs Contour+2 vs Sony Action Cam vs Drift Ghost',
    '1080p 60fps 60p GoPro Hero3 vs Sony Action Cam Comparison',
    'GoPro HD: Ryan Villopoto Full Moto 2 - Muddy Creek Lucas Oil Pro Motocross Championship 2013',
    'GoPro Hero 3 Black Edition LCD TOUCH BacPac UNBOXING & DEMO',
    'GoPro Hero3 Black vs Sony Action Cam VIDEO comparison',
    'Tip #254 GoPro - This is how I pack / travel with GoPro stuff',
    'GoPro HD: Dreams with Kelia Moniz - Roxy Wahine Classic 2011',
    'Tip #226 GoPro - New Version 3rd Person View Mount',
    'GoPro HERO3 Kit (Pelican 1500 Case)',
    'GoPro: Lion Hug',
    'GoPro Hero 3 - Mounting Tips & Tricks!',
    'PEOPLE ARE AWESOME 2013 [NEW VERSION]',
    'GoPro DIY Pan Tilt Time-lapse Rig Demonstration',
    'GoPro Hero3 vs Hero3+ (Black Edition) Review / Comparison - Should You Upgrade?',
    'GoPro Pelican 1450 Case - Setup and Review',
    'GoPro: Driftstyle stunt ride',
    'EASY DIY: telescopic Go Pro Pole',
    'Gopro Hero3+ vs Hero3',
    'Tip #214 GoPro - New GoPro Studio 2.0 is up for free!',
    'Tip #258 GoPro Hero3+ vs Hero3 App Wi-fi Speed Comparison',
    'Airplane bird strike at 120 frames per second with a GoPro Hero2 camera',
    'GoPro - Custom Pelican 1200 Case - Homemade GoPoles & Accessories',
    '2013 Monster Energy Cup Main Event 2.',
    'Must Have Essential Accessories for a GoPro HERO 3+ (Travel Case, Batteries, Tripod, & GoPro Mounts)',
    'WINGSUIT RACING - Human Flight at 140mph!',
    'Gopro Hero3 test Slow motion, M60 airsoft, 800 billes minute',
    'Fearless at the (Indy) 500 Record Jump',
    'GoPro Hero 3 Trampoline Test Edit',
    'Crashes: James Stewart and Ricky Carmichael"s Most Memorable',
    'How I GoPro',
    'Ultimate Steadicam Tutorial - Glidecam, Hague, Merlin, etc.',
    'World"s 1st epic FPV quadcopter rescue',
    'Bethany Hamilton & Alana Blanchard',
    'GoPro HERO3 Black Edition / Sony Action Cam HDR AS15 comparision test by Sewi',
    'Inspirational Triathlon Training Video',
    'Interrail 2012 - The Art of Travelling Teaser.  GoPro Camera',
    'GoPro Hero 2 Pelican 1500 Case',
    'Sniper Kill Shot !! Barret M107',
    'HOW TO BALANCE a Flycam | Glidecam | Stabilizer | Steadycam  + TIPS on Achieving Best Results',
    'Ricky Carmichael Suzuki RMZ 450',
    'FlyCam 3-Axis Steadicam Rig for DSLR',
    'How to Build a Single Bolt 360 Swivel GoPro Helmet Mount',
    '2012 Ironman World Championship, Kona',
    'This Is Skiing | HD',
    'avalanche in revelstoke',
    'The Pelican Store: Kaizen Foam Introduction',
    'Helmet Cam Footage US Navy Seals (or Marines??) in Combat.',
    'Tip #13 GoPro - BlurFix Flat lens on window',
    'Snow Kayak Race in Estonia - Red Bull Snow Kayak 2013',
    'GoPro HERO3 vs. HERO2 Head-to-Head',
    'GoPro HERO3 Black Edition.  My Jamaican Vacation...Sun, Sand and Scuba...and hot women.',
    'Pelican 1200 cace review + gopro cace',
    'Giant Barracuda Charging group of divers',
    'Octopus Caught While Kayak Fishing',
    'GoPro Afghanistan: 6 Months in 2 Minutes',
    'Best DSLR DIY Merlin Style Steady-Cam (Silver Flyer... Black Edition)',
    'Best of Red Bull Rampage 2013',
    'Pelican 1500 & 1600 Case Review',
    'Biggest Crashes from Muddy Creek - Villopoto / Canard / Roczen / Tomac',
    'How to make a 2 Hour Panning Timer for the GoPro HERO - Hero1, Hero2 or HERO3',
    'SteadiCam Stabilization for GoPro Cameras',
    'The GoPro App Tutorial: Control. View. Share.',
    'Top 10 Bike Fails Loading Unloading',
    'Fun at illegal water slide in Australia HD',
    'Action Camera a confronto: GoPro, Drift, Midland e Sony - TVtech',
    'Adam Cianciarulo AC92 + Ryan Villopoto RV2',
    'Attaque d"Orque incroyable en live !',
    'Pelican 1200 case (GoPro)',
    'River Running Kayaks - Find the perfect boat for you!',
    'first try on the go pro hero 3 white edition',
    'GoPro Hero 3+ and DJI Phantom ~ Hawaii Adventures ~ Cliff Jumping and Sunset Flights',
    'Biggest Teahupoo Ever, Shot on the PHANTOM CAMERA. [Original 720p video]',
    'Sony HDR AS15 vs GoPro Hero 3 Black Edition',
    'Danish forces kill 5 taliban part 2/2 (subtitled)',
    '2013 AMA Supercross Round 10 Daytona - 450 Main Event',
    'Slow Motion Tutorial - GoPro Hero 3',
    'Motorcycle Accidents Compilation Stunt Bike Crashes Motorbike Accidents 2013 #3 HD New August',
    'Mexico vs New Zealand ( 5-1 ) Completo Todos Los Goles ( Azteca ) 13_11_2013',
    'GoPro #03 - Sinnvolles die GoPro Hero3',
    'Insane Downhill Bike Race In Chile valparaiso polc 2011',
    'GoPro HD HERO2 and HERO Comparison Video',
    'MY DIY CAMERA SLIDER (DOLLY)',
    'Soca river white water kayaking, Bunker section. Slovenia 14-08-2011',
    'Downhill extreme: Rollerman overtaking motorcycle!',
    'How To Balance A Glidecam HD-2000 & Canon 7D In 15 Minutes Or Less',
    'DJI Phantom Triple LiPo Battery Load - Over 20 Mins Flight Time (T-Motor Anti Gravity upgrade)',
    'Side by Side: GoPro Hero3+ SILVER vs Hero3 SILVER ++',
    'GoPro Aerial Ladder Climb',
    'Gopro Cineform Tutorial Slow Motion & Zeitraffer',
    'Pesca de Prancha Extrema - Barracuda',
    'GoPro: Red Bull Harescramble 2013 Erzberg Rodeo',
    'VES - Vent Enter Search - Colorado Springs Apartment Fire - IRONSandLADDERS',
    '2012 in PICTURES (funny moments of canoe / kayak)',
    'EMeRGed- The George Washington University Emergency Medical Response Group (EMeRG / GW EMS)',
    'Segway HandsFree - Steady camera devices',
    'Attaquer par des lions, dans un cirque']


# distance function compares two urls and finds the distance
# uses SequenceMatcher from python standard module difflib
def distance(url1, url2):
    ratio = SequenceMatcher(None, url1, url2).ratio()
    return 1.0 - ratio


# Perform clustering
new_urls = []
for url in urls:
    try:
        new_urls.append(str(url.lower()))
    except:
        pass



url_objects = []
for url in urls: 
    url_objects.append({
        'distance': distance('GoPro:', url),
        'url': url
    })

newlist = sorted(url_objects, key=lambda k: k['distance']) 
for item in newlist:
    print item

# hc = HierarchicalClustering(new_urls, distance)
# clusters = hc.getlevel(0.2)

# pprint.pprint(clusters)
