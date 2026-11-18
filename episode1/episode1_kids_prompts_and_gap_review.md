# EPISODE 1 — KID PROMPTS (2026) + GAP REVIEW OF THE CAST BIBLE

Built from your **FINAL v3 script** and your **Cast + Location Bible (2026-11-18)**. Everything here is for local generation (ComfyUI → Krea2 / Qwen / MiniMax H3), with the identity-edit step after the face anchor, as in your bible.

---

## PART A — HOW TO USE THE PROMPTS

**Order per kid:** (1) Face Anchor → (2) Full-Body Kit Sheet → (3) optional 3/4 and Mud-State add-ons → feed the best frames to your identity-edit step and then to MiniMax H3 as references. **Do Adam first** (the emotional centre of Part 1 and of the foul).

**Your own lesson from the v91 dataset, applied here:** image models drift to blonde / European / light-skinned faces for Kerala subjects. So every prompt starts with the **absolute identity block** below, before anything else.

**GLOBAL IDENTITY BLOCK (paste at the start of every kid prompt):**
> A real 11-year-old Malayali boy from rural Kerala, South India, warm medium-to-dark brown skin with natural uneven texture and a few small marks, dark brown eyes, thick black hair, ordinary village-kid features and a child's proportions, no European features, no light skin, no blond or brown hair, no adult face

**GLOBAL STYLE TAIL (paste at the end of every prompt):**
> shot like a documentary still, natural skin texture with no smoothing, soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour

**GLOBAL NEGATIVE (only if your workflow takes one):**
> blonde, European features, pale skin, plastic smooth skin, beauty retouching, glamour lighting, text, watermark, logo, extra fingers, distorted hands, adult proportions, heavy makeup, cartoon, 3d render

**Shot templates**
- **FACE ANCHOR:** portrait 3:4, head and shoulders, **plain white round-neck T-shirt**, neutral expression, looking straight at the camera, plain light-grey seamless backdrop, flat even soft light, no hat, no props. *(Clean, identical setup for all kids so the identity-edit step has a neutral base. This matches the "clean frontal face anchor" in your bible.)*
- **FULL-BODY KIT SHEET:** 2:3 portrait, full body head to feet, standing straight, arms relaxed, front view, plain light-grey seamless backdrop, flat even soft light, wearing the match kit described, **mud-free** (clean base).
- **3/4 ADD-ON (append to any anchor):** `, head turned three-quarters to the left, same lighting, same backdrop`
- **MUD-STATE ADD-ON (append to the kit sheet for match shots):** `, shins, knees, forearms and the front of the jersey splashed with wet red-brown paddy mud, mud in the hair at the temples, a smear on one cheek, slightly out of breath, kit soaked and clinging`

*Note on a single "sheet" image: models often drift when asked for many views in one frame. For MiniMax H3 references, 4 separate clean images per kid (frontal face, 3/4 face, full body clean, full body mud-state) usually hold identity better than one crowded turnaround. If your workflow can do a turnaround in one pass, use it as a bonus, not the only reference.*

**All kits are mismatched on purpose** (your script: "none of them matching"). **No black jerseys** for Zidhan's kids, so they never read as Rockstar. **No printed text or numbers** on the kits unless you add them in post.

---

## PART B — THE 5 STARTERS

### 1. ADAM (tall, lean, sharp-featured; Jaisal's nephew; shy, desperate to play)
**Identity line:** a tall, lean boy, taller than his age, long neck, sharp angular features, high cheekbones, narrow chin, thick straight eyebrows, wide shy eyes, short black hair cut unevenly at home with a small cowlick at the crown, dark brown skin, slightly oversized hands and feet, a faint scrape on the left knee

**FACE ANCHOR**
> A real 11-year-old Malayali boy from rural Kerala, South India, warm medium-to-dark brown skin with natural uneven texture and a few small marks, dark brown eyes, thick black hair, ordinary village-kid features and a child's proportions, no European features, no light skin, no blond or brown hair, no adult face. A tall, lean boy, taller than his age, long neck, sharp angular features, high cheekbones, narrow chin, thick straight eyebrows, wide shy eyes, short black hair cut unevenly at home with a small cowlick at the crown. Portrait, head and shoulders, plain white round-neck T-shirt, neutral expression with a hint of shy hope, looking straight at the camera, plain light-grey seamless backdrop, flat even soft light. Shot like a documentary still, natural skin texture with no smoothing, soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour.

**FULL-BODY KIT SHEET**
> A real 11-year-old Malayali boy from rural Kerala, South India, warm medium-to-dark brown skin with natural uneven texture and a few small marks, dark brown eyes, thick black hair, ordinary village-kid features and a child's proportions, no European features, no light skin, no blond or brown hair, no adult face. A tall, lean boy, taller than his age, sharp angular features, high cheekbones, narrow chin, thick straight eyebrows, short uneven black hair with a small cowlick, slightly oversized hands and feet, a faint scrape on the left knee. Full body, head to feet, front view, standing straight, arms relaxed, in a faded red football jersey a size too big, grey cotton shorts, thin socks pulled up over **shin guards made of folded newspaper**, worn **rubber sandals** (no boots). Plain light-grey seamless backdrop, flat even soft light. Shot like a documentary still, natural skin texture with no smoothing, soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour.

---

### 2. ANTO (goalkeeper; stocky, sturdy, round solid face; calm and unbothered)
**Identity line:** a stocky, sturdy boy with a thick short neck, round solid face, full cheeks, broad flat nose, small steady eyes, close-cropped black hair, medium-dark brown skin

**FACE ANCHOR**
> A real 11-year-old Malayali boy from rural Kerala, South India, warm medium-to-dark brown skin with natural uneven texture and a few small marks, dark brown eyes, thick black hair, ordinary village-kid features and a child's proportions, no European features, no light skin, no blond or brown hair, no adult face. A stocky, sturdy boy with a thick short neck, round solid face, full cheeks, broad flat nose, small steady eyes, close-cropped black hair. Portrait, head and shoulders, plain white round-neck T-shirt, calm unbothered expression, looking straight at the camera, plain light-grey seamless backdrop, flat even soft light. Shot like a documentary still, natural skin texture with no smoothing, soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour.

**FULL-BODY KIT SHEET**
> A real 11-year-old Malayali boy from rural Kerala, South India, warm medium-to-dark brown skin with natural uneven texture and a few small marks, dark brown eyes, thick black hair, ordinary village-kid features and a child's proportions, no European features, no light skin, no blond or brown hair, no adult face. A stocky, sturdy boy with a thick short neck, round solid face, broad flat nose, close-cropped hair. Full body, head to feet, front view, standing planted with feet apart, arms relaxed, in an oversized faded green goalkeeper's jersey, long grey shorts, plain socks, worn canvas shoes, **no gloves**, bare hands with dusty palms. Plain light-grey seamless backdrop, flat even soft light. Shot like a documentary still, natural skin texture with no smoothing, soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour.

---

### 3. GOPU (captain; confident leader look, strong jaw)
**Identity line:** a boy with a square face, strong jaw, straight nose, thick dark eyebrows, steady direct eyes, short neatly side-parted black hair with a little coconut-oil sheen, medium-brown skin, a small mole beside the right eyebrow

**FACE ANCHOR**
> A real 11-year-old Malayali boy from rural Kerala, South India, warm medium-to-dark brown skin with natural uneven texture and a few small marks, dark brown eyes, thick black hair, ordinary village-kid features and a child's proportions, no European features, no light skin, no blond or brown hair, no adult face. A boy with a square face, strong jaw, straight nose, thick dark eyebrows, steady direct eyes, short neatly side-parted black hair with a little oil sheen, a small mole beside the right eyebrow. Portrait, head and shoulders, plain white round-neck T-shirt, calm confident expression with lips pressed lightly together, looking straight at the camera, plain light-grey seamless backdrop, flat even soft light. Shot like a documentary still, natural skin texture with no smoothing, soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour.

**FULL-BODY KIT SHEET**
> A real 11-year-old Malayali boy from rural Kerala, South India, warm medium-to-dark brown skin with natural uneven texture and a few small marks, dark brown eyes, thick black hair, ordinary village-kid features and a child's proportions, no European features, no light skin, no blond or brown hair, no adult face. A boy with a square face, strong jaw, straight nose, thick dark eyebrows, short side-parted black hair. Full body, head to feet, front view, standing upright with shoulders back, arms relaxed, in a faded yellow football jersey with a **strip of torn white cloth tied round the left upper arm as a captain's armband**, navy shorts, plain socks, scuffed football boots. Plain light-grey seamless backdrop, flat even soft light. Shot like a documentary still, natural skin texture with no smoothing, soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour.

---

### 4. BABU (long passer; lean, tall, narrow face)
**Identity line:** a lean, long-legged boy, tall but not as tall as Adam, narrow face, long straight nose, deep-set thoughtful eyes, slightly prominent ears, wavy black hair that falls over the forehead, dark brown skin

**FACE ANCHOR**
> A real 11-year-old Malayali boy from rural Kerala, South India, warm medium-to-dark brown skin with natural uneven texture and a few small marks, dark brown eyes, thick black hair, ordinary village-kid features and a child's proportions, no European features, no light skin, no blond or brown hair, no adult face. A lean boy with a narrow face, long straight nose, deep-set thoughtful eyes, slightly prominent ears, wavy black hair that falls over the forehead. Portrait, head and shoulders, plain white round-neck T-shirt, quiet focused expression, looking straight at the camera, plain light-grey seamless backdrop, flat even soft light. Shot like a documentary still, natural skin texture with no smoothing, soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour.

**FULL-BODY KIT SHEET**
> A real 11-year-old Malayali boy from rural Kerala, South India, warm medium-to-dark brown skin with natural uneven texture and a few small marks, dark brown eyes, thick black hair, ordinary village-kid features and a child's proportions, no European features, no light skin, no blond or brown hair, no adult face. A lean, long-legged boy with a narrow face, wavy black hair falling over the forehead, slightly prominent ears. Full body, head to feet, front view, standing relaxed with weight on one leg, in a white football jersey with a torn collar, faded blue shorts, socks of two different shades, worn boots. Plain light-grey seamless backdrop, flat even soft light. Shot like a documentary still, natural skin texture with no smoothing, soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour.

---

### 5. RAGU (striker; fast, wiry, quick eyes)
**Identity line:** a small wiry boy with sharp cheekbones, bright darting eyes, thin eyebrows, a lopsided half-grin showing a chipped front tooth, black hair cropped close with a faint shaved line over the left ear, medium-dark skin

**FACE ANCHOR**
> A real 11-year-old Malayali boy from rural Kerala, South India, warm medium-to-dark brown skin with natural uneven texture and a few small marks, dark brown eyes, thick black hair, ordinary village-kid features and a child's proportions, no European features, no light skin, no blond or brown hair, no adult face. A small wiry boy with sharp cheekbones, bright darting eyes, thin eyebrows, a lopsided half-grin showing a chipped front tooth, black hair cropped close with a faint shaved line over the left ear. Portrait, head and shoulders, plain white round-neck T-shirt, alert expression with a hint of mischief, looking straight at the camera, plain light-grey seamless backdrop, flat even soft light. Shot like a documentary still, natural skin texture with no smoothing, soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour.

**FULL-BODY KIT SHEET**
> A real 11-year-old Malayali boy from rural Kerala, South India, warm medium-to-dark brown skin with natural uneven texture and a few small marks, dark brown eyes, thick black hair, ordinary village-kid features and a child's proportions, no European features, no light skin, no blond or brown hair, no adult face. A small wiry boy with sharp cheekbones, bright darting eyes, close-cropped hair. Full body, head to feet, front view, standing on the balls of his feet with knees slightly bent as if about to sprint, in a faded orange football jersey, short green shorts, thin socks, lightweight worn boots. Plain light-grey seamless backdrop, flat even soft light. Shot like a documentary still, natural skin texture with no smoothing, soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour.

---

## PART C — THE 7 BENCH KIDS (generate only if a shot needs them, per your bible)

### 6. PACHU ("the stubborn one")
**Identity line:** a boy with a rounded determined face, heavy low eyebrows, a set jaw, lips pressed into a stubborn line, short tightly curled black hair, medium-dark skin

**FACE ANCHOR**
> A real 11-year-old Malayali boy from rural Kerala, South India, warm medium-to-dark brown skin with natural uneven texture and a few small marks, dark brown eyes, thick black hair, ordinary village-kid features and a child's proportions, no European features, no light skin, no blond or brown hair, no adult face. A boy with a rounded determined face, heavy low eyebrows, a set jaw, lips pressed into a stubborn line, short tightly curled black hair. Portrait, head and shoulders, plain white round-neck T-shirt, stubborn unimpressed expression, looking straight at the camera, plain light-grey seamless backdrop, flat even soft light. Shot like a documentary still, natural skin texture with no smoothing, soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour.

**FULL-BODY KIT SHEET**
> A real 11-year-old Malayali boy from rural Kerala, South India, warm medium-to-dark brown skin with natural uneven texture and a few small marks, dark brown eyes, thick black hair, ordinary village-kid features and a child's proportions, no European features, no light skin, no blond or brown hair, no adult face. A boy with a rounded determined face, heavy low eyebrows, short tightly curled hair. Full body, head to feet, front view, standing with **arms folded across his chest**, in a faded maroon football jersey, grey shorts, plain socks, scuffed boots. Plain light-grey seamless backdrop, flat even soft light. Shot like a documentary still, natural skin texture with no smoothing, soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour.

---

### 7. VELU (the loud little defender; smallest of the team)
**Identity line:** the smallest boy of the team, a wide mouth, a gap where a front baby tooth is missing, big ears, round bright eyes, short shaggy black hair, medium-brown skin, always looks mid-shout

**FACE ANCHOR**
> A real 11-year-old Malayali boy from rural Kerala, South India, warm medium-to-dark brown skin with natural uneven texture and a few small marks, dark brown eyes, thick black hair, ordinary village-kid features and a child's proportions, no European features, no light skin, no blond or brown hair, no adult face. The smallest boy of the team, wide mouth, a gap where a front baby tooth is missing, big ears, round bright eyes, short shaggy black hair. Portrait, head and shoulders, plain white round-neck T-shirt, cheeky open-mouthed grin as if mid-shout, looking straight at the camera, plain light-grey seamless backdrop, flat even soft light. Shot like a documentary still, natural skin texture with no smoothing, soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour.

**FULL-BODY KIT SHEET**
> A real 11-year-old Malayali boy from rural Kerala, South India, warm medium-to-dark brown skin with natural uneven texture and a few small marks, dark brown eyes, thick black hair, ordinary village-kid features and a child's proportions, no European features, no light skin, no blond or brown hair, no adult face. The smallest boy of the team, big ears, gap-toothed, short shaggy hair. Full body, head to feet, front view, standing with chest puffed and fists on hips, in a striped blue-and-white football jersey that hangs almost to his knees, dark shorts, mismatched socks, boots slightly too big. Plain light-grey seamless backdrop, flat even soft light. Shot like a documentary still, natural skin texture with no smoothing, soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour.

---

### 8. KUTTI (the fast one; lean sprinter)
**Identity line:** a lean long-limbed boy with a high forehead, angular face, quick relaxed eyes, a buzz cut, medium-brown skin, light and springy

**FACE ANCHOR**
> A real 11-year-old Malayali boy from rural Kerala, South India, warm medium-to-dark brown skin with natural uneven texture and a few small marks, dark brown eyes, thick black hair, ordinary village-kid features and a child's proportions, no European features, no light skin, no blond or brown hair, no adult face. A lean long-limbed boy with a high forehead, angular face, quick relaxed eyes, black hair in a buzz cut. Portrait, head and shoulders, plain white round-neck T-shirt, easy half-smile, looking straight at the camera, plain light-grey seamless backdrop, flat even soft light. Shot like a documentary still, natural skin texture with no smoothing, soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour.

**FULL-BODY KIT SHEET**
> A real 11-year-old Malayali boy from rural Kerala, South India, warm medium-to-dark brown skin with natural uneven texture and a few small marks, dark brown eyes, thick black hair, ordinary village-kid features and a child's proportions, no European features, no light skin, no blond or brown hair, no adult face. A lean long-limbed boy with a high forehead and a buzz cut. Full body, head to feet, front view, standing loose and springy, in a faded green football jersey with the sleeves rolled, light shorts, ankle socks, light worn boots. Plain light-grey seamless backdrop, flat even soft light. Shot like a documentary still, natural skin texture with no smoothing, soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour.

---

### 9. KARU (the jumpy one; wiry, mischievous)
**Identity line:** a wiry restless boy with unruly curly black hair, big bright eyes, a quick mischievous grin, thin arms, dark brown skin, a healing scab on one elbow

**FACE ANCHOR**
> A real 11-year-old Malayali boy from rural Kerala, South India, warm medium-to-dark brown skin with natural uneven texture and a few small marks, dark brown eyes, thick black hair, ordinary village-kid features and a child's proportions, no European features, no light skin, no blond or brown hair, no adult face. A wiry restless boy with unruly curly black hair, big bright eyes, a quick mischievous grin. Portrait, head and shoulders, plain white round-neck T-shirt, grinning as if he is about to jump, looking straight at the camera, plain light-grey seamless backdrop, flat even soft light. Shot like a documentary still, natural skin texture with no smoothing, soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour.

**FULL-BODY KIT SHEET**
> A real 11-year-old Malayali boy from rural Kerala, South India, warm medium-to-dark brown skin with natural uneven texture and a few small marks, dark brown eyes, thick black hair, ordinary village-kid features and a child's proportions, no European features, no light skin, no blond or brown hair, no adult face. A wiry restless boy with unruly curly hair and thin arms, a scab on one elbow. Full body, head to feet, front view, standing bouncing slightly on his toes, in a faded purple football jersey, brown shorts, socks sliding down, barefoot on one foot and a boot on the other as if mid-change. Plain light-grey seamless backdrop, flat even soft light. Shot like a documentary still, natural skin texture with no smoothing, soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour.

---

### 10. CHANDRU (the biggest kid; gentle giant)
**Identity line:** the biggest and heaviest boy of the team, broad wide-jawed face, thick neck, round chin, big hands, short black hair, gentle soft eyes that contrast with his size, medium-dark skin

**FACE ANCHOR**
> A real 11-year-old Malayali boy from rural Kerala, South India, warm medium-to-dark brown skin with natural uneven texture and a few small marks, dark brown eyes, thick black hair, ordinary village-kid features and a child's proportions, no European features, no light skin, no blond or brown hair, no adult face. The biggest, heaviest boy of the team, broad wide-jawed face, thick neck, round chin, gentle soft eyes, short black hair. Portrait, head and shoulders, plain white round-neck T-shirt (stretched across the shoulders), calm gentle expression, looking straight at the camera, plain light-grey seamless backdrop, flat even soft light. Shot like a documentary still, natural skin texture with no smoothing, soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour.

**FULL-BODY KIT SHEET**
> A real 11-year-old Malayali boy from rural Kerala, South India, warm medium-to-dark brown skin with natural uneven texture and a few small marks, dark brown eyes, thick black hair, ordinary village-kid features and a child's proportions, no European features, no light skin, no blond or brown hair, no adult face. The biggest, heaviest boy of the team, broad shoulders, thick neck, big hands, gentle eyes. Full body, head to feet, front view, standing solid with feet apart, in a stretched grey football jersey, long dark shorts, thick socks, large worn boots. Plain light-grey seamless backdrop, flat even soft light. Shot like a documentary still, natural skin texture with no smoothing, soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour.

---

### 11. MUSTHU (the organiser; observant, always arranging the others)
**Identity line:** a neat observant boy with a narrow face, small neat features, a tidy side parting, careful watchful eyes, medium-brown skin, one hand always half-raised as if pointing someone into place

**FACE ANCHOR**
> A real 11-year-old Malayali boy from rural Kerala, South India, warm medium-to-dark brown skin with natural uneven texture and a few small marks, dark brown eyes, thick black hair, ordinary village-kid features and a child's proportions, no European features, no light skin, no blond or brown hair, no adult face. A neat observant boy with a narrow face, small neat features, a tidy side parting in his black hair, careful watchful eyes. Portrait, head and shoulders, plain white round-neck T-shirt, attentive expression, looking straight at the camera, plain light-grey seamless backdrop, flat even soft light. Shot like a documentary still, natural skin texture with no smoothing, soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour.

**FULL-BODY KIT SHEET**
> A real 11-year-old Malayali boy from rural Kerala, South India, warm medium-to-dark brown skin with natural uneven texture and a few small marks, dark brown eyes, thick black hair, ordinary village-kid features and a child's proportions, no European features, no light skin, no blond or brown hair, no adult face. A neat observant boy with a narrow face and a tidy side parting. Full body, head to feet, front view, standing with **one hand half-raised, two fingers pointing as if directing someone**, in a faded sky-blue football jersey tucked in neatly, light shorts, clean socks, plain boots. Plain light-grey seamless backdrop, flat even soft light. Shot like a documentary still, natural skin texture with no smoothing, soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour.

---

### 12. TOMY (the quiet one who always knows)
**Identity line:** a quiet boy with an oval face, hooded calm eyes, **one eyebrow sitting slightly higher than the other**, a small closed-mouth half-smile, neatly combed black hair, medium-brown skin

**FACE ANCHOR**
> A real 11-year-old Malayali boy from rural Kerala, South India, warm medium-to-dark brown skin with natural uneven texture and a few small marks, dark brown eyes, thick black hair, ordinary village-kid features and a child's proportions, no European features, no light skin, no blond or brown hair, no adult face. A quiet boy with an oval face, hooded calm eyes, one eyebrow sitting slightly higher than the other, a small closed-mouth half-smile, neatly combed black hair. Portrait, head and shoulders, plain white round-neck T-shirt, knowing quiet expression, looking straight at the camera, plain light-grey seamless backdrop, flat even soft light. Shot like a documentary still, natural skin texture with no smoothing, soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour.

**FULL-BODY KIT SHEET**
> A real 11-year-old Malayali boy from rural Kerala, South India, warm medium-to-dark brown skin with natural uneven texture and a few small marks, dark brown eyes, thick black hair, ordinary village-kid features and a child's proportions, no European features, no light skin, no blond or brown hair, no adult face. A quiet boy with an oval face, hooded calm eyes, one eyebrow slightly higher than the other, neatly combed hair. Full body, head to feet, front view, standing still with hands loose, in a faded white-and-red striped football jersey, grey shorts, plain socks, worn boots. Plain light-grey seamless backdrop, flat even soft light. Shot like a documentary still, natural skin texture with no smoothing, soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour.

---

## PART D — THE ROCKSTAR BOYS (12–13; opponents, 3 faces plus the kit)

**Identity block for Rockstar kids (replace the age/size words in the global block):**
> A real 12-to-13-year-old Malayali boy from Kerala, South India, warm brown skin with natural texture, dark eyes, black hair, bigger and broader than an average boy his age but still clearly a child, no European features, no light skin, no blond hair

**Shared kit (all three):** matching **black football jersey with a cluster of printed silver stars on the chest**, black shorts, black socks, clean boots. They are the "rock band": neat, matching, a little too proud.

### R1. THE STRIKER (breaks clear; grabs Adam's shirt)
> *[Rockstar identity block]* Taller than the others, athletic build, a smirk, sharp jaw, trendy hair with the sides faded short and the top longer and swept up, confident eyes. Portrait head and shoulders, wearing the black star jersey, cocky half-smile, looking at the camera, plain light-grey seamless backdrop, flat even soft light. *[Global style tail]*

### R2. THE BIG DEFENDER (tallest and widest of the Rockstar boys)
> *[Rockstar identity block]* Tall and heavy-set, thick neck, broad flat face, heavy-lidded eyes, short cropped hair, a bored intimidating look. Portrait head and shoulders, wearing the black star jersey, heavy neutral stare, plain light-grey seamless backdrop, flat even soft light. *[Global style tail]*

### R3. THE CAPTAIN (smug leader)
> *[Rockstar identity block]* Medium height, neat features, a self-satisfied expression, perfectly combed hair, a thin captain's armband in black, a clean new look compared to Zidhan's kids. Portrait head and shoulders, wearing the black star jersey, chin slightly raised, plain light-grey seamless backdrop, flat even soft light. *[Global style tail]*

### R-TEAM SHOT (for the entrance and the speaker)
> Five Malayali boys aged 12 to 13 lined up on a muddy paddy-field pitch in Kerala, all in matching black football jerseys with printed silver stars, black shorts and clean boots, standing like a rock band, a bigger and broader group than ordinary kids their age, a speaker box on a stool on the sideline behind them, wet green paddy and coconut palms behind, harsh noon light. *[Global style tail]*

---

# PART E — DID WE MISS ANYTHING? (REVIEW OF YOUR CAST + LOCATION BIBLE)

I went through the bible against **FINAL v3**. Items are in priority order.

## E1. Conflicts to fix before generating

1. **T-shirt conflict (important).** The bible says Jaisal wears a **plain black tee** and Zidhan a **plain white tee**. The script says that in 1950 they walk through the village as "the only colour": **faded teal and mustard T-shirts with glossy printed graphics** that slowly drain. Decide one: I suggest the LoRA tells you the faces; the **outfits come from the prompt**: Jaisal in a **teal graphic tee**, Zidhan in a **mustard graphic tee**, in the 2026 scenes too (otherwise the colour has nothing to drain from). Design two graphic prints once and reuse them.
2. **Faces-echo is still in the script, but the bible says "completely different people" (D233).** Two spots in the script still carry the old idea: **Section 1 ("Faces echo")** and the **cast table's "Echo" column**, and one line in **Scene 23**: *"faces we know from black and white: Anto, Gopu, Babu, Ragu, Adam."* Under D233 that line is wrong (the 1950 men don't look like the kids). Delete the echo wording and change that line to just *"The kids lie in a mud-slicked heap."*
3. **Scene-number drift.** The bible's scene numbers don't match v3 (for example it cites "Sc. 30", and "Vaidyar Sc. 7–9, 21", and Sulaiman in "Sc. 10, 11"). In v3 there are 25 scenes, Sulaiman appears in Sc. 9 and 11, and the Vaidyar is only a background character (no recruitment scene). Re-number the bible against v3 so shot lists don't point at the wrong scenes.
4. **Vaidyar:** the bible calls him the "third coach". In v3 he's only in the line-up and the voyage montage. Keep him as a **background character**, or restore a short recruitment beat; as the bible stands he's over-promised.
5. **Adam's age and tallness:** the bible says "11–12" and "tall"; the global block says "11-year-old". Fine, just don't generate Adam as 13+ (he must still read as a child in the foul and the fight).

## E2. Characters the bible doesn't list (they appear on screen)

**2026**
- **The referee** (Sc. 6): yellow-card whistle, adult, a worn local man.
- **The ticket boy** (Sc. 6): ~10, school notebook, matchbox-label tickets.
- **The injured boy** (Sc. 3): a kid with a twisted ankle, carried out by the Father.
- **Farmers / paddy extras** (Sc. 2, 6), **gallery spectators** (Sc. 6), **village extras** (Sc. 3).
- **The commentator**: voice only (Sc. 23). He's off-screen, so no face needed, but you need a **voice plan**.

**1950**
- **The two constables** (Sc. 8, 10E): one tips his cap at Jaisal.
- **The tailor**, **the boy who touches the T-shirt**, **the two women at the well**, **the man on the bicycle** (Sc. 8).
- **The fishwife** (Sc. 10E: Jaisal knocks over her basket).
- **MARJAN crew and the ship's cook** (Sc. 11, 12, 15).
- **Post-office extras** (Sc. 13): the fat man, clerks, the messenger (you list him).
- **FIFA official, journalist, clerk, band leader** (Sc. 16).
- **Opposing players:** Swedes (tall, blond), the Italian captain, Brazilians in white, **the Uruguayan striker who says "YES"** (Sc. 22), plus Varela (listed).
- **Bose silhouette** (Sc. 15): one second, but it needs a design: tall figure, long dark coat, round-rimmed spectacles, cap, seen from behind or in silhouette.
- **Maracanã crowd:** thousands of extras. Plan this as a plate / crowd tool, not individual faces.

## E3. Family resemblance (cheap and powerful)
- **Grandpa → little Abu Bakar → Sulaiman → Jaisal** should look related: generate **little Abu Bakar from Grandpa's face anchor** (age-regressed), **Sulaiman as Grandpa's father** (same bone structure, ship-master's bearing), and keep Jaisal's features in the same family. The audience should feel it in Sc. 11 without a word.
- **Adam (Jaisal's nephew)** should echo Jaisal subtly: the same brow line or the same smile.

## E4. Cultural and costume details missing
- **Grandpa Abu Bakar / Sulaiman / Muallim** (Malabar Muslim elders): white mundu and shirt, **prayer cap**, white beard. Not in the bible yet.
- **Shafiq's wife:** head-covering and everyday housewear (a thattam / headscarf with a simple printed cotton dress). Not in the bible.
- **The 1950 team kit in Brazil** (Sc. 16): **sailcloth shirts dyed with turmeric and indigo, hand-stitched numbers, mismatched socks, some barefoot, some in rope-tied boots.** The bible gives the men's faces but not this kit; it's one of the film's best images.
- **Opposition kits (1950):** Sweden yellow, Brazil **white**, Uruguay **sky blue**, Italy dark blue, Spain red, Paraguay (check references). Collect real references so these don't look generic.
- **Jaisal's trainers** (2026 trainers on 1950 cobbles) are a detail the script uses in Sc. 10E.
- **Winning Eleven kits:** keep them mismatched, no black, no numbers (see Part A).

## E5. Props the bible doesn't track (continuity-critical ones in bold)
- **The watch** (you track the chain, but not the object). Fix its design once: *a vintage round wristwatch, gold-toned case, cream dial, thin worn leather strap.* It must read the same in Sc. 1, 4, 11, 23, 25 and be small enough that the boy's wrist makes it hang like a bracelet.
- **The empty first-aid spray** and its cap (Zidhan pockets the cap, Sc. 3) + the **full spray** (Sc. 23 optional).
- **The notebook and pen** (letter, injury log, "SPRAY: 0").
- **Jaisal's folded position list** crossed off in Sc. 10.
- **The dead bandicoot rat**, **the wild boar** and **the cracker trap** (Sc. 2, 4).
- **The matchbox ticket** (Sc. 6), **the mint-tea glass** (Sc. 1).
- **The rubber seeds** and **the chalk** (Sc. 15), **the sailcloth ball** soaked in sea water, **the 15 pairs of striped socks** (Sc. 14), **the telegraph forms** (Sc. 9, 13), **the brass lamp** and **ledgers** (Sc. 13).
- **The coconut stock on deck** (Sc. 12, 15): the pile has to *shrink* across the voyage, so you need a continuity count.

## E6. Locations the bible doesn't list
**2026:** the **fork / village road** used for the "only colour" walk is 1950; for 2026 add the **father's car / field edge** (Sc. 3).
**1950:** the **village road and fork** (Sc. 8), the **market alley** for the thief chase (Sc. 10E), the **sea shallows** for Antappan (Sc. 10B), the **coir beach** (Sc. 10D), the **coconut grove** (Sc. 10A; you have "village ground at golden hour"), the **Madras bazaar** (Sc. 14), **Madras harbour**, the **FIFA office in Rio** (Sc. 16), the **stadium tunnel / anthem** (Sc. 16), the **dressing room** (Sc. 18), the **MARJAN cabin with the route map** (Sc. 14A), and the **night deck in Rio for the quarrel** (Sc. 20).

## E7. Production plan gaps
1. **Dialogue / voices.** The bible covers faces but not voices. You have a lot of dialogue (Malayalam-flavoured English, some Malayalam lines). Decide the voice route (record yourself, a voice model, or MiniMax audio) and lip-sync approach per shot. For a film with this much dialogue this is as big as the faces.
2. **Number of shots.** Roughly 55–70 minutes of material at 5–10 seconds per clip means hundreds of generations. Plan a shot list with a "hero shot" tier (generate many takes) and a "cutaway" tier (one take).
3. **Colour pipeline.** You're right to grade B&W in post; keep a **selective colourize** list for the three exceptions (T-shirts that drain, fire, the watch). The "draining" shirt is an animated grade, so plan its keyframes per scene.
4. **Continuity of mud:** 2026 kids are clean at kick-off and increasingly muddy; the scene bible should say which shot is "clean / splashed / soaked". The MUD-STATE add-on in Part A is for this.
5. **Hardware.** An RTX 5090 (32 GB VRAM) with 64 GB RAM is comfortable for local image generation and LoRA-style work. For **video**, it depends on the model: I can't verify the specs of "MiniMax H3" (it's newer than my knowledge), so check its VRAM, runtime per clip and whether it accepts several reference images before you commit your shot count to it.

## E8. Next steps I'd suggest
1. Fix the three conflicts in E1 (T-shirts, D233 wording, scene numbers).
2. Generate **Adam → Anto → Gopu → Babu → Ragu** anchors, then the bench only when needed.
3. Add the missing characters from E2 to the bible and give each a one-line descriptor (I can write these).
4. Decide the voice route (E7.1) before you lock your shot list.
