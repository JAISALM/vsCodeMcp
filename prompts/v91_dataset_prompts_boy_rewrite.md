# v91 Pro-Grade Dataset — Prompt Rewrite Brief (boy versions)

Source: proven workflow `krea2IDEditProGradeCharacterDataset_v91VisionAssistant` (Civitai model 2805529, author lonecatone23).
The 8 prompt lists below were written for the author's character — a young blonde woman ("Anika").
We need the SAME lists for OUR characters (below). Keep the richness, structure, line counts and technical vocabulary — change the character, not the craft.

## TASK FOR THE REWRITING MODEL

1. For EACH of the 8 lists below, write a boy version: SAME number of lines, SAME order, each line a complete standalone prompt.
2. Use the character descriptions verbatim (below). Jaisal is the PRIMARY — write all 8 lists for Jaisal unless a list is marked for Zidhan.
3. Keep every technical element: camera terms (85mm f/1.8, shallow DOF, dutch angle, pov), lighting (golden hour, overcast rim light), skin texture (visible pores), color grade, bokeh, lens feel. Only change the character + anything inherently feminine.
4. Inherently-feminine lines (lace bra/panties, bikini, dress, cleavage, jewelry) → replace with the best MALE equivalent that keeps the same SHOT TYPE and mood (e.g. "red lace bra and panties, luxury penthouse" → "rolled-up white shirt, open collar, luxury penthouse"; "beach micro bikini, wet hair" → "beach, black t-shirt, wet hair, golden hour").
5. EVERY line must end with (or include): `ONLY ONE character, no other people, no duplicates.` — Krea2 has a known quirk of duplicating the subject (our own rule, D137).
6. Every line should include the global suffix text below (it is also wired into the workflow, but the author re-states style words per line — keep both).
7. Hair rules (Krea2 identity): face is LOCKED by the identity conditioning — prompts may re-state hair/build (author style, harmless) but must NOT fight the reference. Describe hair EXACTLY as in the character description.

## CHARACTER DESCRIPTIONS (use verbatim)

### Jaisal (char1 — PRIMARY)

```
Man, MEDIUM WAVY black hair (falling to eyebrow length), slightly CROOKED naturally bent nose, almond eyes, thin lips, clean-shaven faint stubble, slim build, plain black t-shirt, and skin EXACTLY the same as the reference image.
```

### Zidhan (char2)

```
Man, SHORT neat black hair, FULL short dense beard, slim build, plain white t-shirt, and skin EXACTLY the same as the reference image.
```

## GLOBAL SUFFIX (wired into the workflow — LCPositive node)

```
ignore original clothing completely, photorealistic, high-detail natural skin texture with pores, soft natural lighting, sharp focus,
```

## GENERATION SETTINGS (workflow-locked — do NOT change in prompts)

- Base: Krea 2 Turbo (10 steps, cfg 1, euler/simple, denoise 1.0 = t2i)
- Identity: krea2_identity_edit LoRA @1.0 + Krea2EditModelPatch ref_boost 2.0 / ref_boost_a 0.9 / fit + grounded encodes (768px)
- References: `jaisal_final_ref.png` (face) + full-body ref → both pass through background-removal (BiRefNet) before the patch
- Output: 1080x1350 (Instagram Portrait 4:5), seed FIXED at 13 (deterministic — same line + same seed = same image)
- Post-chain: clarity pass + image adjust + auto-save to Dataset folder + .txt caption per image + face-similarity compare
- Text cleanup (LCTextRemove): author's find-slots are EMPTY = no text removal active

---

## THE 8 AUTHOR LISTS (verbatim — rewrite each for Jaisal)

### LIST 1 — node 257 — 20 lines

```
subject Front view.
Subject right side, profile view.
Subject rear view.
Subject left side, profile view.
Upper torso close up of face. beauty shot.
Casual outfit, full body shot, form fitting, neutral background.
Full body shot, white lace bra and panties, luxury penthouse apartment, soft lighting, front view.
Action pose, on beach, black micro bikini, golden hour lighting, seductive look, wet hair.
Wearing a fur-trimmed hood, side profile looking out a rain-speckled window, crisp raindrops on the glass and soft diffused overcast side light illuminating the face, with a subtle rim light on the hair, Shallow depth of field with the focal plane on the near eye, creamy bokeh in the background, High-detail skin texture and natural pores, defined eyelashes, slightly sharpened eyes and lips, hand near face showing glittery nails and textured winter clothing, Warm highlights balanced with slight teal-tinted shadows for a moody yet natural editorial color grade, gentle contrast, soft film grain and a subtle vignette for focus, Lens feel: 85mm, f/1.8, shallow DOF, High-resolution, editorial-quality output.
Standing in a kitchen doorway wearing a cropped red off the shoulder cutoff t-shirt, her hair is styled in loose waves and falls over her shoulder. her eyes are a bright green color, and she has a slight smile on her lips, the lighting is soft and natural, creating a warm and inviting atmosphere.
taking a selfie in a black dress and black high heel shoes in front of an ornate full length mirror, adorned with sparkling jewelry, with a confident and alluring expression, her makeup is subtle and natural, with a hint of blush on her cheeks, she is wearing a short, black dress that accentuates her curves, along with a statement necklace and matching bracelets, full body shot, natural lighting, soft bokeh, shallow DOF.
on knees looking, up, white lace bra and panties, exposed breasts, ass view, looking seductively at viewer, pov top angle view.
sitting at an office desk, dutch angle view, black miniskirt, black high heel shoes, white blouse unbuttoned at the front, cleavage, hair in a neat bun, perfect makeup, mascara, legs crossed, looking at viewer.
late night, city street, red dress with a long slit up the side that exposes her thigh and accentuates her curves, high heels, perfect makeup, red lipstick, dark lighting, shadows, shallow depth of field, blurred background, contrappopsto, hand on hip, hipbone.
Playful 3/4 body shot,tight white button-up shirt tied at the waist with cutoff shorts,  hoop earrings,cleavage, minimal makeup, flat lighting,soft focus, captured on sony a7, professionally shot, dark background
leaning against a balcony railing in a luxury penthouse, city view, golden hour, wearing red lace bra and panties, looking back at viewer with a seductive glance, eye contact rear angle shot, ass focus, 
Black yoga pants, grey sports bra, sweaty, headphones, hair in messy ponytail, wet hair, gym setting, admiring her curves, body focus, eye level view.
pink crop top sweater, underboob, midriff, navel, breasts, white slacks, makeup, outdoors, hair in ponytail, blue sky with clouds, looking at viewer, eye contact, view from below.
A angle from above standing confidently in front of a mirror in a sheer nightgown under soft bedroom lighting, standing in the middle of the frame with her arms crossed, looking directly at the camera with a seductive expression, her hair is styled in loose waves and falls down her back, framing her face, She is wearing minimal makeup, the background is blurred, but the focus is on the woman's face and upper body, which contrasts nicely with the neutral tones of the setting, the lighting is soft and natural, highlighting her features and creating a subtle glow in the otherwise monochromatic image, the overall mood of the image is sophisticated and alluring, making it a captivating piece of photography.
Dynamic shot, cleavage, sideboob, tank top, cyberpunk scene, hair in high ponytail, posing for the camera. 
```

<!-- REWRITE FOR: -->

### LIST 2 — node 258 — 20 lines

```
Front view, full body, neutral expression, standing naturally, soft charcoal-gray blouse and matching tailored trousers, soft studio lighting, plain background.
Subject right side, profile view, three-quarter body, calm expression, soft ivory knit sweater and dark navy skirt, natural daylight, clean background.
Subject rear view, full body standing, relaxed posture, warm camel coat over cream trousers, soft even lighting, neutral backdrop.
Subject left side, profile view, upper body, thoughtful expression, muted sage-green blouse, gentle side lighting, shallow depth of field.
Upper torso close-up of face, beauty portrait, soft natural light, subtle smile, high detail skin texture, shallow DOF.
Casual outfit, full body shot, comfortable medium-wash blue jeans and soft heather-gray sweater, neutral background, soft daylight, natural pose.
Full body shot, elegant casual dress in dusty rose, modern apartment interior, soft window lighting, front view, relaxed stance.
Action pose on a sunny beach, light pale-yellow summer dress, golden hour lighting, wind-blown hair, cheerful expression, wet sand underfoot.
Wearing a deep charcoal fur-trimmed hooded coat, side profile looking out a rain-speckled window, crisp raindrops on the glass, soft diffused overcast side light, subtle rim light on hair, shallow depth of field focused on near eye, creamy bokeh, high-detail skin texture, natural pores, defined eyelashes, hand near face showing textured winter clothing, warm highlights with slight teal-tinted shadows, gentle contrast, soft film grain, subtle vignette, 85mm lens feel, f/1.8, editorial quality.
Standing in a kitchen doorway wearing a cropped red off-the-shoulder t-shirt and medium-wash blue jeans, loose waves falling over one shoulder, bright green eyes, slight smile, soft natural lighting, warm inviting atmosphere.
Taking a selfie in a stylish black midi dress and black high heels in front of an ornate full-length mirror, subtle sparkling jewelry, confident expression, natural makeup with soft blush, full body shot, soft natural lighting, gentle bokeh, shallow DOF.
Kneeling pose looking slightly upward, casual soft white top and light-wash blue jeans, friendly expression, soft indoor lighting, eye-level view.
Sitting at an office desk, slight dutch angle, black pencil skirt and crisp white blouse, neat bun hairstyle, polished but natural makeup, legs crossed, looking toward camera, professional office background.
Late night city street, deep red dress with modest side slit, black high heels, elegant makeup with red lipstick, dramatic shadows and soft street lighting, shallow depth of field, blurred background, hand on hip, confident posture.
Playful three-quarter body shot, white button-up shirt tied at the waist with light-wash cutoff denim shorts, hoop earrings, minimal makeup, soft even lighting, gentle focus, dark background, professional photography look.
Leaning against a balcony railing in a luxury penthouse, city skyline view at golden hour, elegant deep-red blouse and matching tailored pants, looking back over shoulder with a calm smile, soft warm light, three-quarter rear angle.
Black yoga pants and heather-gray sports top, light sweat, headphones, messy ponytail, gym interior, natural posture, eye-level view, soft overhead lighting.
Soft pink crop sweater and white trousers, outdoors under blue sky with soft clouds, hair in ponytail, looking at camera with friendly eye contact, slight low angle, natural daylight.
High angle from above, standing confidently in front of a bedroom mirror in a long soft ivory nightgown, arms crossed loosely, looking toward camera with gentle expression, loose waves framing face, minimal makeup, soft bedroom lighting, focus on face and upper body, blurred neutral background, sophisticated calm mood.
Dynamic pose, casual black tank top, cyberpunk-inspired neon city background, high ponytail, energetic stance facing camera, colorful lighting accents, shallow depth of field.
```

<!-- REWRITE FOR: -->

### LIST 3 — node 259 — 25 lines

```
Standing front view, full body, calm neutral expression, tailored wool coat over turtleneck and trousers, soft overcast daylight, quiet cobblestone alley in an old European quarter.  
Three-quarter view, slight turn to the left, gentle closed-mouth smile, cream cable-knit sweater and high-waisted trousers, warm golden-hour side light, stone terrace overlooking a vineyard.  
Profile view facing right, upper body, pensive faraway look, soft linen shirt with rolled sleeves, cool diffused morning light, wooden pier beside a still mountain lake.  
Rear three-quarter view looking over shoulder, full body, soft curious expression, flowing midi skirt and light blouse, gentle backlight with lens flare, path through a bamboo forest.  
Close-up beauty portrait, eyes looking directly at camera with quiet confidence, delicate silk scarf and simple blouse, soft Rembrandt lighting, dimly lit antique bookstore aisle.  
Sitting cross-legged on a low stone bench, relaxed content expression, oversized knit cardigan and wide-leg pants, soft dappled sunlight filtering through leaves, shaded courtyard of an old monastery.  
Leaning against a weathered wooden railing, arms loosely folded, slight amused smile, denim jacket over white tee and cargo pants, cool blue-hour light, elevated walkway above a foggy harbor.  
Walking toward camera along a gravel path, soft open smile, light trench coat and ankle boots, warm late-afternoon sunlight, tree-lined lane leading to a countryside manor.  
Standing in a sunlit conservatory, one hand resting on a metal railing, serene expression, soft floral dress and cardigan, bright natural greenhouse light, surrounded by tropical plants and glass panels.  
Sitting at a small round table outdoors, thoughtful gaze downward, tailored blazer and turtleneck, soft overcast daylight, quiet plaza with a central fountain.  
Kneeling beside a low stone wall, looking up with a gentle smile, rustic linen shirt and trousers, warm golden side light, hillside olive grove at sunset.  
Standing on a narrow stone bridge, hands resting on the parapet, calm contemplative expression, long wool coat and scarf, cool misty morning light, arched bridge over a quiet canal.  
Sitting on the edge of a wide windowsill, soft wistful expression, oversized sweater and leggings, cool blue window light mixed with warm interior lamps, high attic room with sloping ceiling.  
Leaning slightly forward over a wooden counter, focused interested expression, casual button-up shirt and apron, soft warm overhead pendant lights, cozy corner of a pottery studio.  
Standing in an open arched doorway, light breeze in hair, peaceful relaxed expression, simple summer dress, bright midday sunlight, entrance to a whitewashed coastal chapel.  
Sitting on a low stone step, legs loosely crossed, quiet amused smile, corduroy jacket and jeans, soft afternoon light, shaded colonnade of an old university courtyard.  
Three-quarter body shot, one hand lightly touching a railing, confident neutral expression, structured blazer and slim trousers, soft directional window light, modern glass-walled sky lounge.  
Standing beside a tall arched window, looking outward with soft melancholy, cashmere sweater and tailored pants, cool rainy-day ambient light, grand library reading room with high shelves.  
Walking slowly along a wooden boardwalk, gentle smile, light linen shirt and rolled trousers, warm late-day sunlight, elevated walkway through a coastal wetland.  
Sitting on the floor of a sunlit loft, knees drawn up, peaceful introspective expression, soft hoodie and joggers, bright natural skylight, minimalist artist’s studio with large canvases.  
Standing beneath hanging paper lanterns at dusk, soft warm smile, elegant wrap dress, warm glowing lantern light mixed with blue twilight, quiet night market street.  
Leaning back against a wooden post, arms resting loosely, easy relaxed smile, flannel shirt and jeans, soft golden-hour light, rustic porch of a mountain cabin.  
Close-up three-quarter profile looking slightly downward, quiet thoughtful expression, soft turtleneck, gentle side lighting with soft shadows, dimly lit jazz bar corner.  
Full body standing with hands lightly clasped in front, composed neutral expression, tailored overcoat and scarf, soft diffused winter light, snow-dusted path through a silent evergreen forest.  
Sitting on a low stone ledge, elbows resting on knees, open friendly expression, light denim shirt and chinos, soft afternoon sunlight, wide steps leading up to a hillside temple.
```

<!-- REWRITE FOR: -->

### LIST 4 — node 2770 — 25 lines

```
Standing front view, full body, relaxed arms at sides, face showing a soft neutral expression, soft oatmeal-beige knit top and stone-gray trousers, soft studio lighting, plain neutral background.
Three-quarter view, slight turn to the right, face wearing a casual open smile, warm terracotta sweater and cream trousers, natural window light, indoor living room setting.
Profile view facing left, upper body, face locked in a thoughtful distant expression, muted dusty-blue blouse, soft side lighting, shallow depth of field.
Rear three-quarter view looking over shoulder, full body, face turning with a gentle curious smile, soft sage-green cardigan over light khaki pants, gentle breeze, outdoor park path.
Close-up beauty portrait, eyes looking slightly off-camera, face holding a soft serene expression, soft diffused light, high detail skin texture.
Sitting cross-legged on a wooden floor, casual soft moss-green sweater and medium-wash blue jeans, face lit with a warm contented smile, warm indoor lighting, cozy home interior.
Leaning against a brick wall, arms crossed loosely, face set in a calm slightly amused expression, faded olive jacket over cream t-shirt, urban street background, soft overcast daylight.
Walking toward camera on a quiet sidewalk, light sand-colored jacket and dark indigo jeans, face showing a relaxed open smile, golden hour lighting, city skyline soft in background.
Standing in a modern kitchen, hand resting on counter, face carrying a soft neutral smile, simple soft lavender blouse and charcoal trousers, soft natural light from windows.
Sitting at a café table outdoors, holding a coffee cup, face wearing a gentle relaxed smile, light butter-yellow dress, sunny afternoon, blurred street behind.
Kneeling on one knee in a garden, looking up, face bright with a calm smile, soft floral-print blouse in pale peach and green, floral background, soft dappled sunlight.
Standing on a balcony overlooking the city, hands on railing, face held in a quiet contemplative expression, elegant deep teal blouse, evening blue hour lighting.
Sitting on the edge of a bed, soft morning light through curtains, loose soft heather-lavender sweater, face soft with a peaceful sleepy expression, relaxed posture.
Leaning forward slightly over a desk, professional soft taupe blouse, office setting, face fixed in a focused concentrated expression, soft overhead light.
Standing in an open doorway, light breeze catching hair, face glowing with a soft happy expression, casual soft coral summer top and white shorts, bright outdoor daylight.
Sitting on a park bench, legs crossed, reading a book, face absorbed in a quiet focused expression, soft rust-orange cardigan over cream top, soft autumn light, trees in background.
Three-quarter body shot, one hand in pocket, medium-wash denim jacket and matching jeans, face displaying an easy confident smile, industrial loft interior, soft window light.
Standing near a large window, looking outside, face set in a soft pensive expression, soft oatmeal sweater, rainy day ambient light, reflections on glass.
Walking along a beach shoreline, light natural-linen outfit in warm sand tones, face carrying a peaceful contented smile, late afternoon sun, gentle waves in background.
Sitting on the floor against a wall, knees drawn up, casual soft slate-blue hoodie, face quiet with an introspective expression, soft indoor lamp light, minimalist room.
Standing under string lights at dusk, light soft blush-pink dress, face lit by a warm soft smile, warm glowing background, relaxed open posture.
Leaning back in a comfortable chair, arms resting on armrests, face relaxed into a contented expression, smart casual soft olive blazer over cream shirt and dark charcoal pants, modern living room.
Close-up profile looking downward, face soft with a reflective expression, soft natural light, outdoor garden setting, shallow depth of field.
Full body standing with hands clasped behind back, formal-casual soft navy blazer and matching pants, face held in a calm composed expression, clean studio backdrop.
Sitting on steps outside a building, elbows on knees, medium-wash denim shirt and jeans with white sneakers, face showing a casual easygoing smile, soft afternoon light, urban architecture behind.
```

<!-- REWRITE FOR: -->

### LIST 5 — node 2842 — 25 lines

```
Close-up front view, face showing a soft neutral expression, soft oatmeal-beige knit top, soft studio lighting, plain neutral background.
Three-quarter headshot, slight turn to the right, face wearing a casual open smile, warm terracotta sweater, natural window light, soft indoor background.
Profile headshot facing left, face locked in a thoughtful distant expression, muted dusty-blue blouse, soft side lighting, shallow depth of field.
Over-the-shoulder headshot looking back, face turning with a gentle curious smile, soft sage-green cardigan, gentle outdoor light, soft blurred park background.
Close-up beauty portrait, eyes looking slightly off-camera, face holding a soft serene expression, soft diffused light, high detail skin texture.
Tight headshot, face lit with a warm contented smile, casual soft moss-green sweater, warm indoor lighting, soft cozy background.
Three-quarter headshot, arms out of frame, face set in a calm slightly amused expression, faded olive jacket over cream t-shirt, soft overcast daylight, urban blur behind.
Front headshot, face showing a relaxed open smile, light sand-colored jacket, golden hour lighting, soft city skyline bokeh.
Close-up, face carrying a soft neutral smile, simple soft lavender blouse, soft natural window light, clean neutral background.
Tight portrait, face wearing a gentle relaxed smile, light butter-yellow top, sunny afternoon light, soft blurred outdoor background.
Looking slightly upward headshot, face bright with a calm smile, soft floral-print blouse in pale peach and green, soft dappled sunlight, floral bokeh.
Three-quarter headshot, face held in a quiet contemplative expression, elegant deep teal blouse, evening blue hour lighting, soft city glow behind.
Soft morning headshot, face soft with a peaceful sleepy expression, loose soft heather-lavender sweater, gentle curtain-filtered light.
Close-up, face fixed in a focused concentrated expression, professional soft taupe blouse, soft overhead office light, clean background.
Front headshot, face glowing with a soft happy expression, casual soft coral summer top, bright outdoor daylight, soft natural background.
Tight portrait, face absorbed in a quiet focused expression, soft rust-orange cardigan over cream top, soft autumn light, trees softly blurred.
Three-quarter headshot, face displaying an easy confident smile, medium-wash denim jacket, industrial loft soft window light.
Looking slightly away headshot, face set in a soft pensive expression, soft oatmeal sweater, rainy day ambient light, soft reflections.
Close-up, face carrying a peaceful contented smile, light natural-linen top in warm sand tones, late afternoon sun, gentle soft background.
Tight headshot, face quiet with an introspective expression, casual soft slate-blue hoodie, soft indoor lamp light, minimalist background.
Front portrait, face lit by a warm soft smile, light soft blush-pink top, warm glowing string-light background at dusk.
Three-quarter headshot, face relaxed into a contented expression, smart casual soft olive blazer over cream shirt, modern soft interior light.
Close-up profile looking downward, face soft with a reflective expression, soft natural light, outdoor garden setting, shallow depth of field.
Front headshot, face held in a calm composed expression, formal-casual soft navy blazer, clean studio backdrop, soft even lighting.
Tight portrait, face showing a casual easygoing smile, medium-wash denim shirt, soft afternoon light, soft urban architecture bokeh.
```

<!-- REWRITE FOR: -->

### LIST 6 — node 2843 — 20 lines

```
Low-angle front view of a person mid-serve on a tennis court, racket arm fully extended upward, focused determined expression, wearing a bright white moisture-wicking polo shirt, navy blue athletic shorts, white ankle socks, and white tennis shoes, bright midday sunlight, green court surface.
Side-tracking shot of a runner sprinting along a track, arms pumping, legs in full stride, intense concentrated expression, wearing a neon yellow sleeveless running tank, black compression shorts, white crew socks, and bright orange running shoes, golden hour side light, blurred stadium background.
Over-the-shoulder view from the passenger seat of a person driving a convertible, both hands on the steering wheel, relaxed open smile, wearing a soft sky-blue short-sleeve button-up shirt, khaki chino shorts, and tan canvas sneakers, sunny coastal highway, wind-blown hair.
Three-quarter front view of a cyclist leaning into a turn on a paved trail, focused calm expression, wearing a matte black cycling jersey, bright red padded cycling shorts, white ankle socks, and black cycling shoes, soft morning light, green tree-lined path.
Low-angle shot of a basketball player jumping for a layup, right arm extended toward the hoop, determined expression, wearing a royal blue sleeveless jersey, matching royal blue basketball shorts, white crew socks, and black high-top sneakers, indoor gym lighting, polished wooden court.
Side view of a person mid-stride hiking uphill on a rocky trail, poles planted, steady focused expression, wearing a forest-green moisture-wicking long-sleeve shirt, charcoal gray hiking pants, thick gray wool socks, and brown hiking boots, soft overcast daylight, mountain landscape.
Front three-quarter view of a soccer player striking a ball with the right foot, body leaned forward, intense concentrated expression, wearing a bright red soccer jersey, white athletic shorts, red soccer socks, and black cleats, sunny afternoon, green grass field.
High-angle tracking shot of a skateboarder carving down a smooth ramp, balanced posture, joyful open smile, wearing a light gray graphic T-shirt, dark olive cargo shorts, white crew socks, and black skate shoes, bright outdoor skatepark light.
Side view of a person mid-swing in golf, club following through, calm focused expression, wearing a soft white polo shirt, navy blue tailored golf shorts, white ankle socks, and white golf shoes, golden late-afternoon light, manicured green fairway.
Low-angle front view of a volleyball player leaping to spike the ball, arm cocked back, determined expression, wearing a bright teal sleeveless athletic top, matching teal volleyball shorts, white ankle socks, and white court shoes, indoor gym fluorescent lighting.
Three-quarter rear view of a kayaker paddling hard through calm water, torso twisted with the stroke, focused expression, wearing a bright orange life vest over a navy blue short-sleeve rash guard, black board shorts, and bare feet, soft morning lake light.
Side-tracking shot of a person jogging along a beach shoreline, arms swinging naturally, relaxed contented smile, wearing a soft coral tank top, light gray running shorts, white ankle socks, and turquoise running shoes, warm late-afternoon sunlight, gentle waves.
Front low-angle view of a boxer throwing a right cross in a gym, gloves extended, intense focused expression, wearing a black sleeveless training shirt, red boxing shorts, white hand wraps visible, and black boxing shoes, soft overhead gym lighting.
Three-quarter view of a rock climber reaching upward on an indoor wall, body stretched, concentrated expression, wearing a light purple climbing tank top, dark gray climbing pants, white ankle socks, and bright yellow climbing shoes, even indoor climbing-gym light.
Side view of a person jumping rope mid-air, knees slightly bent, energetic smile, wearing a bright lime-green athletic T-shirt, black athletic shorts, white crew socks, and gray cross-training shoes, outdoor park soft daylight.
Over-the-shoulder view of a surfer paddling out on a board, arms alternating strokes, calm focused expression, wearing a deep navy short-sleeve rash guard and matching navy board shorts, soft morning ocean light, gentle swell.
Low-angle front view of a person mid-dunk on a basketball court, ball held high, powerful determined expression, wearing a black sleeveless jersey with white side panels, matching black shorts with white trim, white crew socks, and red high-top sneakers, indoor arena lighting.
Side view of a horseback rider cantering along a dirt trail, upright balanced posture, peaceful smile, wearing a soft beige long-sleeve riding shirt, dark brown riding breeches, tall black riding boots, and a matching beige helmet, soft golden-hour countryside light.
Three-quarter tracking shot of a person rollerblading along a waterfront path, arms slightly out for balance, joyful open smile, wearing a bright turquoise athletic tank top, black knee-length athletic shorts, white ankle socks, and black inline skates, sunny afternoon light.
Front view of a tennis player lunging for a low forehand, racket extended, focused intense expression, wearing a soft white sleeveless tennis top, light pink athletic skirt, white ankle socks, and white tennis shoes, bright court sunlight, clean blue hard-court surface.
```

<!-- REWRITE FOR: -->

### LIST 7 — node 260 — 25 lines

```
Front view, standing in sheer black lingerie, soft studio lighting, hands resting lightly on hips, neutral background.
Right side profile, wearing a silk robe slipped off one shoulder, soft window light, looking slightly downward.
Rear view, standing in lace panties only, looking back over shoulder, warm low-key lighting, plain backdrop.
Left side profile, upper body in a barely-there bralette, hand running through hair, shallow depth of field.
Close-up beauty shot of face and bare shoulders, soft parted lips, dramatic side lighting, high detail skin texture.
Full body, kneeling on a bed in white lace bra and panties, hands on thighs, soft bedroom lighting.
Sitting on the edge of a luxury bathtub, wrapped loosely in a towel that slips at the chest, steam in the air, soft ambient light.
Standing in a doorway wearing an unbuttoned men’s shirt and nothing else, one hand holding the frame, warm interior light.
Leaning against a large window at night, city lights behind, wearing a sheer nightgown, hands pressed to the glass.
Lying on her side on a rumpled bed, propped on one elbow, wearing only black panties, soft lamplight, looking toward camera.
Kneeling on the floor, back arched slightly, wearing a strappy bodysuit, soft overhead lighting, looking up.
Sitting in an armchair with legs draped over the arm, silk slip dress riding up, soft evening light, relaxed sensual expression.
Standing in a hotel room, back to camera, looking over shoulder, wearing only a garter belt and stockings, soft window light.
Sitting on a kitchen counter, wearing an oversized sweater that slips off one shoulder and nothing underneath, soft morning light.
Leaning forward over a desk, blouse unbuttoned low, black skirt hiked slightly, office setting, dramatic side lighting.
Standing in a rain-speckled glass shower stall, water running down bare skin, steam, soft diffused light, hands in hair.
Lying on her back on silk sheets, one arm above her head, wearing a thin camisole and panties, soft moonlight through curtains.
Sitting cross-legged on the floor in front of a mirror, wearing only a lace bralette and shorts, soft vanity lighting.
Standing on a balcony at night in a sheer robe open at the front, city skyline behind, cool blue ambient light.
Kneeling on a couch, facing camera, wearing a low-cut tank top pulled down at one shoulder and short shorts, warm indoor light.
Lying on her stomach on a bed, propped on elbows, wearing a thin tank top and panties, soft natural window light.
Sitting on the edge of a pool at night, wet skin, wearing a micro bikini, underwater lights glowing, looking toward camera.
Standing in a dimly lit hallway, back against the wall, wearing a short silk robe loosely tied, soft rim lighting.
Sitting on the floor with legs extended, leaning back on her hands, wearing only a long open cardigan, soft lamplight.
Standing in front of a full-length mirror, adjusting a sheer bodysuit, soft bedroom lighting, three-quarter view.
```

<!-- REWRITE FOR: -->

### LIST 8 — node 2772 — 7 lines

```
Standing near a large window, looking outside, face set in a soft pensive expression, soft cream-colored sweater, rainy day ambient light, reflections on glass.
Walking along a beach shoreline, light beige linen outfit, face carrying a peaceful contented smile, late afternoon sun, gentle waves in background.
Sitting on the floor against a wall, knees drawn up, casual heather-gray hoodie, face quiet with an introspective expression, soft indoor lamp light, minimalist room.
Standing under string lights at dusk, pale soft-pink dress, face lit by a warm soft smile, warm glowing background, relaxed open posture.
Leaning back in a comfortable chair, arms resting on armrests, face relaxed into a contented expression, smart casual navy-blue blazer over a white shirt and dark charcoal trousers, modern living room.
Sitting on the edge of a luxury bathtub, wrapped loosely in a towel that slips at the chest, steam in the air, soft ambient light.
Side view of a person mid-stride hiking uphill on a rocky trail, poles planted, steady focused expression, wearing a forest-green moisture-wicking long-sleeve shirt, charcoal gray hiking pants, thick gray wool socks, and brown hiking boots, soft overcast daylight, mountain landscape.
```

<!-- REWRITE FOR: -->

---

## OUTPUT FORMAT (what to hand back)

One block per list, same order, labelled `LIST n — node <id> (Jaisal)`, each line a complete prompt ending with the ONLY-ONE-character rule. Paste-ready: the lines go directly into the CR Prompt List node body (one prompt per line).
