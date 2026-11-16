"""Site content data: homes, case studies, testimonials, team and Journal.

Everything marked placeholder=True is sample content written for the staging
build. The build refuses to produce a live (STAGING = False) site while any
placeholder remains, so replace each item with Staycay's real content and
set placeholder=False (or delete the field) as you go.
"""

# ---------------------------------------------------------------------------
# OUR HOMES — manually curated. Order here is the display order on Our Homes.
# featured=True puts a home on the homepage (first three featured are shown).
# categories drive the filter buttons on /our-homes/.
# booking_url is the home's page on Staycay's direct-booking platform.
# images: names from site/assets/img (without size suffix); first is the hero.
# ---------------------------------------------------------------------------
CATEGORIES = [
    ("couples", "Couples"),
    ("families", "Families"),
    ("groups", "Large groups"),
    ("dogs", "Dog friendly"),
    ("walkers", "Walkers' favourites"),
]

HOMES = [
    {
        "slug": "millstone-barn",
        "name": "Millstone Barn",
        "location": "Hathersage, Hope Valley",
        "region": "Peak District",
        "sleeps": 8, "bedrooms": 4, "bathrooms": 3, "dogs": "2 dogs welcome",
        "categories": ["families", "groups", "dogs", "walkers"],
        "featured": True,
        "summary": "A gritstone barn with long views across the Hope Valley, a wood-burner, and a terrace made for slow summer evenings.",
        "description": [
            "Millstone Barn sits at the end of a quiet lane above Hathersage, its thick gritstone walls and oak beams carefully restored and paired with a calm, contemporary interior.",
            "The open-plan kitchen and dining room opens onto a south-facing terrace with views up to Stanage Edge. In the evening, the sitting room gathers around a wood-burning stove, with deep sofas and shelves of local walking guides.",
            "Four bedrooms, three of them en suite, make it an easy choice for two families sharing or a group of friends heading out for the hills.",
        ],
        "features": ["Wood-burning stove", "South-facing terrace", "Fully equipped kitchen with range cooker", "Three en-suite bedrooms", "Fast Wi-Fi", "Off-road parking for three cars", "Boot room and drying space", "Walks from the door"],
        "nearby": "Hathersage village, with its outdoor pool, cafés and pubs, is a short walk away. Stanage Edge, Ladybower Reservoir and Castleton are all within a short drive.",
        "images": ["garden-cottage", "living", "kitchen", "bedroom", "bathroom", "hills"],
        "booking_url": "{BOOKING_BASE}/millstone-barn",
        "placeholder": True,
    },
    {
        "slug": "curlew-cottage",
        "name": "Curlew Cottage",
        "location": "Edale",
        "region": "Peak District",
        "sleeps": 4, "bedrooms": 2, "bathrooms": 1, "dogs": "1 dog welcome",
        "categories": ["couples", "dogs", "walkers"],
        "featured": True,
        "summary": "A snug stone cottage at the foot of Kinder Scout, with a roll-top bath, a crackling stove and walks from the front door.",
        "description": [
            "Curlew Cottage is a classic Edale stone cottage, updated with care: limewashed walls, natural linens and a woodburner that makes coming in from the hills a pleasure.",
            "Upstairs, the main bedroom looks out across the valley, and the bathroom has a deep roll-top bath. A second bedroom has twin beds that can be made up as a double.",
        ],
        "features": ["Wood-burning stove", "Roll-top bath", "Twin or double second bedroom", "Enclosed garden", "Fast Wi-Fi", "Walks from the door"],
        "nearby": "The Pennine Way starts a short walk away, and the village has a pub, café and railway station with trains to Sheffield and Manchester.",
        "images": ["armchair", "stove", "bedroom", "bathroom", "sheep-house"],
        "booking_url": "{BOOKING_BASE}/curlew-cottage",
        "placeholder": True,
    },
    {
        "slug": "the-old-dairy",
        "name": "The Old Dairy",
        "location": "Near Bakewell",
        "region": "Derbyshire",
        "sleeps": 6, "bedrooms": 3, "bathrooms": 2, "dogs": "No pets",
        "categories": ["families"],
        "featured": True,
        "summary": "A former farm dairy turned light-filled family home, with a big kitchen table and the Derbyshire Dales on the doorstep.",
        "description": [
            "The Old Dairy has been converted into a relaxed family home with a generous kitchen at its heart: a long oak table, a deep green kitchen and doors opening to the garden.",
            "Three bedrooms, including a bunk room the children will fight over, make it ideal for a family break within easy reach of Bakewell, Chatsworth and the Monsal Trail.",
        ],
        "features": ["Large kitchen and dining room", "Enclosed garden", "Bunk room", "Travel cot and high chair", "Fast Wi-Fi", "Parking for two cars"],
        "nearby": "Bakewell's shops and Monday market are a few minutes' drive away, with Chatsworth and the Monsal Trail close by.",
        "images": ["kitchen", "dining", "living", "bedroom", "lamp"],
        "booking_url": "{BOOKING_BASE}/the-old-dairy",
        "placeholder": True,
    },
    {
        "slug": "heather-lodge",
        "name": "Heather Lodge",
        "location": "Castleton",
        "region": "Peak District",
        "sleeps": 2, "bedrooms": 1, "bathrooms": 1, "dogs": "No pets",
        "categories": ["couples", "walkers"],
        "featured": False,
        "summary": "A quiet hideaway for two beneath Mam Tor, with a freestanding bath and a view of the hills from the bed.",
        "description": [
            "Heather Lodge is designed for two: one beautifully dressed bedroom, a freestanding bath with a view, and a sitting room with a stove for after a day on the ridge.",
            "It's a short walk into Castleton for dinner, and Mam Tor and the Great Ridge are right above you.",
        ],
        "features": ["Freestanding bath", "Wood-burning stove", "King-size bed", "Private patio", "Fast Wi-Fi", "Parking for one car"],
        "nearby": "Castleton's caverns, pubs and tearooms are a short walk away, with Mam Tor and the Great Ridge above the village.",
        "images": ["roses", "bathroom", "bedroom", "lamp", "hills"],
        "booking_url": "{BOOKING_BASE}/heather-lodge",
        "placeholder": True,
    },
    {
        "slug": "fern-house",
        "name": "Fern House",
        "location": "Ashford-in-the-Water",
        "region": "Peak District",
        "sleeps": 10, "bedrooms": 5, "bathrooms": 4, "dogs": "2 dogs welcome",
        "categories": ["groups", "families", "dogs"],
        "featured": False,
        "summary": "A handsome stone house for big gatherings, with a terrace for long lunches and space for everyone to spread out.",
        "description": [
            "Fern House is made for occasions: a big birthday, a family reunion, or friends who haven't all been in one place for years.",
            "There's a long dining table, two sitting rooms and a terrace for outdoor meals, with five bedrooms across two floors.",
        ],
        "features": ["Five bedrooms, four bathrooms", "Two sitting rooms", "Terrace with outdoor dining", "Wood-burning stove", "Fast Wi-Fi", "Parking for four cars"],
        "nearby": "Ashford-in-the-Water's sheepwash bridge and village pub are close by, with Bakewell a short drive away.",
        "images": ["farm-autumn", "terrace", "kitchen", "living", "bedroom"],
        "booking_url": "{BOOKING_BASE}/fern-house",
        "placeholder": True,
    },
    {
        "slug": "stanage-view",
        "name": "Stanage View",
        "location": "Bamford",
        "region": "Peak District",
        "sleeps": 6, "bedrooms": 3, "bathrooms": 2, "dogs": "1 dog welcome",
        "categories": ["families", "dogs", "walkers"],
        "featured": False,
        "summary": "A light, modern take on a Hope Valley home, looking up to Stanage Edge and a short walk from the station.",
        "description": [
            "Stanage View pairs local stone with a crisp, modern interior: an open kitchen, wide windows and a sitting room arranged around the view.",
            "With the station nearby, it's an easy car-free escape from Sheffield or Manchester.",
        ],
        "features": ["Open-plan kitchen and living space", "Views to Stanage Edge", "Wood-burning stove", "Garden", "Fast Wi-Fi", "Short walk to the station"],
        "nearby": "Ladybower Reservoir, Stanage Edge and Hathersage are all close by.",
        "images": ["flint-cottage", "living", "kitchen", "bedroom", "hills"],
        "booking_url": "{BOOKING_BASE}/stanage-view",
        "placeholder": True,
    },
]

# ---------------------------------------------------------------------------
# TESTIMONIALS — owner quotes. Use real, approved quotes only.
# contexts: where each quote may appear (home, owners, full-management,
# bookings-revenue, about)
# ---------------------------------------------------------------------------
TESTIMONIALS = [
    {
        "quote": "We'd been running the barn ourselves from two hours away. Handing it to Staycay was the best decision we've made. It's busier, it's better looked after, and we finally get our weekends back.",
        "name": "Owner", "detail": "Stone barn, Hope Valley",
        "contexts": ["home", "owners", "full-management"],
        "placeholder": True,
    },
    {
        "quote": "They took the time to understand what we wanted from the cottage, including the weeks we wanted to keep for ourselves, and built everything around that.",
        "name": "Owner", "detail": "Cottage, Edale",
        "contexts": ["home", "owners", "about", "full-management"],
        "placeholder": True,
    },
    {
        "quote": "We look after the house ourselves, so bookings and pricing were all we needed help with. The calendar has never looked healthier.",
        "name": "Owner", "detail": "Family home, Derbyshire Dales",
        "contexts": ["home", "owners", "bookings-revenue"],
        "placeholder": True,
    },
]

# ---------------------------------------------------------------------------
# CASE STUDIES — every figure must be verified and approved by Staycay.
# growth: optional growth-over-time chart, list of (label, value, display)
# ---------------------------------------------------------------------------
CASE_STUDIES = [
    {
        "slug": "hope-valley-stone-barn",
        "title": "From self-managed to fully managed: a stone barn in the Hope Valley",
        "short": "How a remote owner went from juggling cleaners and messages to a busier, better-reviewed barn.",
        "service": "Full Management",
        "location": "Hope Valley, Peak District",
        "image": "flint-cottage",
        "images": ["armchair-wide", "kitchen"],
        "stats": [("+38%", "gross booking revenue, year one"), ("4.9", "average guest rating"), ("0", "hours a week the owners now spend on it")],
        "challenge": [
            "The owners had bought the barn as a holiday let and a family bolthole, but lived two hours away. They were managing guest messages, cleaners and maintenance themselves, often late at night.",
            "Pricing hadn't changed since launch, the photography was taken on a phone, and occupancy dipped sharply outside the summer holidays.",
        ],
        "approach": [
            "We started with a full property inspection and a refresh of linens, dressing and guest information, then commissioned professional photography and rewrote the listing.",
            "Pricing moved to a dynamic strategy built around local demand: events, school holidays and midweek walkers' breaks. We took over guest communication, housekeeping and maintenance.",
        ],
        "before": ["Owner handling every message and changeover", "Fixed nightly rate all year", "Phone photography, generic listing", "Quiet midweek and winter periods"],
        "after": ["Staycay handles guests, housekeeping and maintenance", "Dynamic pricing reviewed weekly", "Professional photography and new listing copy", "Midweek and winter breaks actively marketed"],
        "growth": [("Year before", 62, "£62k"), ("Year one", 86, "£86k"), ("Year two", 94, "£94k")],
        "growth_caption": "Gross booking revenue by year (sample figures).",
        "quote": 0,
        "contexts": ["home", "owners", "full-management", "property-care"],
        "placeholder": True,
    },
    {
        "slug": "derbyshire-dales-bookings-revenue",
        "title": "Filling the calendar: bookings and revenue support for a Derbyshire family home",
        "short": "An owner who loves looking after the house, and needed help with pricing and bookings.",
        "service": "Bookings & Revenue Management",
        "location": "Derbyshire Dales",
        "image": "castlecombe-wide",
        "images": ["dining", "bedroom"],
        "stats": [("+24%", "nights booked, year one"), ("+17%", "average nightly rate"), ("6 wks", "from appraisal to first booking")],
        "challenge": [
            "The owner lives locally and takes real pride in housekeeping and guest welcome, but found pricing and channel management time-consuming and hard to get right.",
        ],
        "approach": [
            "We rebuilt the listing, set up distribution across the right channels, and introduced dynamic pricing with minimum-stay rules tuned to the season. The owner kept the housekeeping and the welcome.",
        ],
        "before": ["Listed on one channel", "Prices set once a year", "Long gaps between stays"],
        "after": ["Distribution across the right channels", "Pricing reviewed against local demand", "Smarter minimum stays to close gaps"],
        "growth": [],
        "growth_caption": "",
        "quote": 2,
        "contexts": ["owners", "bookings-revenue", "performance"],
        "placeholder": True,
    },
]

# ---------------------------------------------------------------------------
# TEAM — real names, roles, short bios and photography to be supplied.
# ---------------------------------------------------------------------------
TEAM = [
    {"name": "Team member name", "role": "Founder & Director", "bio": "A short biography: background, why they started Staycay and their connection to the Peak District.", "photo": None, "placeholder": True},
    {"name": "Team member name", "role": "Owner Relationships", "bio": "A short biography: who owners speak to day to day and what they look after.", "photo": None, "placeholder": True},
    {"name": "Team member name", "role": "Property Care Lead", "bio": "A short biography: housekeeping standards, inspections and the local team.", "photo": None, "placeholder": True},
    {"name": "Team member name", "role": "Guest Experience", "bio": "A short biography: looking after guests before, during and after their stay.", "photo": None, "placeholder": True},
]

# ---------------------------------------------------------------------------
# JOURNAL — owner SEO and guest/destination articles.
# category: "owners" or "explore"
# ---------------------------------------------------------------------------
JOURNAL_CATEGORIES = {"owners": "For owners", "explore": "Explore the Peak"}

ARTICLES = [
    {
        "slug": "what-does-a-holiday-let-management-company-do",
        "title": "What does a holiday let management company actually do?",
        "seo_title": "What Does a Holiday Let Management Company Do?",
        "description": "A plain-English guide to what holiday let management covers, from guests and housekeeping to pricing and maintenance, and how to tell whether you need it.",
        "category": "owners",
        "date": "2026-10-14",
        "read": "6 min read",
        "image": "armchair-wide",
        "excerpt": "From guest messages at midnight to pricing for bank holidays, here's what a good manager takes off your plate, and what to look for when choosing one.",
        "body": """
<p>If you own a holiday home, you'll know that the work doesn't stop when the booking comes in. Someone has to answer the questions, arrange the changeover, check the property, fix the boiler on a Saturday and decide what to charge for the half-term week. A holiday let management company takes on some or all of that work for you.</p>
<p>Here's what that usually covers, and how to decide which level of help suits you and your home.</p>
<h2>Guests, from enquiry to review</h2>
<p>The most visible part of the job is looking after guests: answering enquiries, confirming bookings, sending arrival information, being on hand during the stay and following up afterwards. Good guest communication is quick, warm and specific to your home. It's also where many owners feel the strain first, because guests expect replies at any hour.</p>
<h2>Housekeeping and changeovers</h2>
<p>Every stay ends with a changeover: cleaning, fresh linen, restocking and a final check. In a busy season that can mean several turnarounds a week, often on tight timings. A manager organises and checks this work so the home is ready, and consistent, for every arrival.</p>
<h2>Property care and maintenance</h2>
<p>Holiday homes work hard. Regular inspections catch small problems before they turn into bad reviews, and a manager with a network of trusted local trades can get things fixed quickly. You stay in control of significant decisions and spend.</p>
<h2>Pricing, revenue and distribution</h2>
<p>This is where the difference between a good year and a great one is often made. Rates should move with demand: school holidays, local events, weekends, short-notice gaps. Listings need to be in the right places, with minimum stays and availability set to reduce empty nights. Revenue management is a specialist skill, and some owners use a manager for this alone.</p>
<h2>Presentation and marketing</h2>
<p>Guests choose with their eyes. Professional photography, a well-written description and a home that is dressed with care all affect how often you're booked and what you can charge.</p>
<h2>Full management or bookings-only?</h2>
<p>Broadly, there are two models. <strong>Full management</strong> covers everything above, so the home earns without you running it day to day. <strong>Bookings and revenue management</strong> suits owners who are happy to look after the property themselves but want expert help with pricing, listings and bookings.</p>
<p>We've written more about <a href="/journal/full-management-or-bookings-only/">choosing between the two</a>.</p>
<h2>What to look for in a manager</h2>
<ul>
<li><strong>Local knowledge.</strong> Someone who knows the area, its seasons and its guests will price and present your home better.</li>
<li><strong>Standards you can see.</strong> Ask how they inspect properties and what happens when something goes wrong.</li>
<li><strong>Clear reporting.</strong> You should always know how your home is performing.</li>
<li><strong>Selectiveness.</strong> A manager who takes on every property can't give each one the same attention.</li>
</ul>
""",
        "placeholder": True,
    },
    {
        "slug": "full-management-or-bookings-only",
        "title": "Full management or bookings-only? Choosing the right support for your holiday home",
        "seo_title": "Full Management or Bookings-Only Holiday Let Support?",
        "description": "How to decide between full holiday let management and a bookings and revenue service, with the questions to ask yourself before you choose.",
        "category": "owners",
        "date": "2026-10-28",
        "read": "5 min read",
        "image": "castlecombe-wide",
        "excerpt": "Some owners want everything handled. Others love looking after their home but want help with pricing and bookings. Here's how to work out which you are.",
        "body": """
<p>There's no single right way to run a holiday home. The best set-up depends on where you live, how much time you have, and which parts of the job you actually enjoy.</p>
<h2>When full management makes sense</h2>
<ul>
<li>You live some distance from the property, or abroad.</li>
<li>You don't want to be on call for guests, cleaners or contractors.</li>
<li>You want consistent standards without checking them yourself.</li>
<li>You see the home as an investment and want it run that way.</li>
</ul>
<h2>When bookings and revenue management is enough</h2>
<ul>
<li>You live nearby and enjoy looking after the home and welcoming guests.</li>
<li>You already have reliable housekeeping in place.</li>
<li>You want expert help with pricing, listings and filling the calendar.</li>
</ul>
<h2>Questions to ask yourself</h2>
<p>How many hours a week do you spend on the property now? What happens when you're on holiday? Are you confident your nightly rates are right for every week of the year? Your answers usually make the choice clear.</p>
<p>If they don't, that's what an appraisal is for. We'll look at your home and how you'd like to run it, and recommend the service that fits.</p>
""",
        "placeholder": True,
    },
    {
        "slug": "a-slow-weekend-in-the-hope-valley",
        "title": "A slow weekend in the Hope Valley",
        "description": "Gritstone edges, village pubs and a reservoir walk: an unhurried weekend itinerary for the Hope Valley in the Peak District.",
        "category": "explore",
        "date": "2026-11-04",
        "read": "4 min read",
        "image": "hills",
        "excerpt": "Gritstone edges, an open-air pool, village pubs and a reservoir walk: our favourite way to spend two unhurried days in the Hope Valley.",
        "body": """
<p>The Hope Valley is the Peak District at its most generous: big views, easy-going villages and walks for every kind of weekend. Here's how we'd spend two slow days.</p>
<h2>Saturday: Hathersage and Stanage Edge</h2>
<p>Start with breakfast in Hathersage, then head up to Stanage Edge, the long gritstone escarpment above the village. The walk along the top is one of the finest in the Peak, with views across the valley in every direction.</p>
<p>Back in the village, Hathersage's heated open-air pool is a local favourite in the warmer months. In the evening, choose a pub with a fire and stay for dinner.</p>
<h2>Sunday: Castleton and Ladybower</h2>
<p>Drive the short way to Castleton for a morning on Mam Tor and the Great Ridge, or explore the village's show caves if the weather turns. In the afternoon, take a gentle walk around part of Ladybower Reservoir before heading home.</p>
<h2>Where to stay</h2>
<p>Several of <a href="/our-homes/">our homes</a> are in and around the Hope Valley, from cottages for two to barns for the whole family.</p>
""",
        "placeholder": True,
    },
]
