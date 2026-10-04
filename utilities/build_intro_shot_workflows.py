# -*- coding: utf-8 -*-
"""
Build the 10 Jaisal Kut intro shot workflows (production R2V chain).

Stitching chain (each shot's END frame = next shot's START frame):
  A  table empty            -> jaisal_hand_under_the_table   (walk-in, sits)
  B  jaisal_hand_under_table-> jaisal_with_hand_on_table     (hands onto table)
  C  jaisal_head_left_back_side -> (CAMERA NODE, orbit 180deg) (the twist)
  D  jaisal_head_180_dergree  -> jaisal_with_hand_on_table   (reverse to normal)
  E  jaisal_with_hand_on_table-> plants_Alive                (plants grow)
  F  plants_Alive           -> plants_dead                   (plants die)
  G  plants_dead            -> jaisal_gone_papers_alone      (vanish burst)
  H  jaisal_gone_papers_alone-> mic+paper_2k                 (mic + paper)
  I  mic+paper_2k           -> mic_without paper_final scene (mic alone)
  J  mic_without paper_final scene -> objects (bat+ball+smiley) (join)

Templates:
  R2V  = jaisalproduction1.json  (SLA, 1344x768, turbo LoRA)
  CAM  = E:\\minimax_workflow\\minimaxH3Camera_v20.json (H3LocalCameraEditor i2v)

Link format (UI): [link_id, origin_id, origin_slot, target_id, target_slot, type]

Run:
  & "E:\\comfyUi_latest\\ComfyUI_windows_portable\\python_embeded\\python.exe" "D:\\models\\vsCodeMcp\\utilities\\build_intro_shot_workflows.py"
"""
import json, copy, os

WF_DIR = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"
R2V_TPL = os.path.join(WF_DIR, "jaisalproduction1.json")
CAM_TPL = r"E:\minimax_workflow\minimaxH3Camera_v20.json"

CHAR = ("<Subject 1> is the young schoolboy - short dark hair, a rose-pink collared "
        "shirt, full-length black trousers, a black school bag, a normal school kid, "
        "seated at a simple wooden table.")
SCENE = ("a dark near-black room. A single bare bulb hangs directly above the wooden "
         "table, the ONLY light source, casting a hard top-down shadow. Everything "
         "outside the bulb's light pool fades to pure black. Black & white, high "
         "contrast, fine film grain, 24fps. The room, table, chair and bulb stay "
         "EXACTLY the same in every shot - same position, same light, same camera "
         "height - so the cuts between shots are seamless.")
NOMUSIC = ("non_diegetic_music: NO music, NO instrumental music, NO musical "
           "instruments, NO melody, NO beat, NO rhythm, NO soundtrack, NO song. "
           "Natural ambient sounds only.")

def r2v_prompt(start_desc, end_desc, action, camera, sounds,
               task="[reference generation]", extra_neg=""):
    subj = (f"<Subject 1> is {CHAR}\n"
            f"<Picture 1> is the FIRST frame of this shot: {start_desc}.\n"
            f"<Picture 2> is the LAST frame of this shot: {end_desc}.")
    summary = (f"{task} A single continuous black & white take that animates smoothly "
               f"from <Picture 1> ({start_desc}) to <Picture 2> ({end_desc}). {SCENE}")
    retention = (f"<Subject 1> (appears in this shot): fully_preserved - the boy's face, "
                 f"short dark hair, rose-pink shirt, black trousers and black bag are "
                 f"retained. There is ONLY ONE character - the single boy <Subject 1> - "
                 f"NO other people, NO second boy, NO duplicates, NO extra figures.\n"
                 f"<Picture 1> (first frame): fully_preserved - the opening frame.\n"
                 f"<Picture 2> (last frame): fully_preserved - the closing frame; the "
                 f"shot ENDS exactly on this frame so the next shot's first frame matches.")
    detail = (f"The target video is black & white, high contrast, fine film grain. {SCENE}\n"
              f"[Shot 1] The shot BEGINS from <Picture 1> ({start_desc}). {action} "
              f"Camera: {camera}. The shot ENDS exactly on <Picture 2> ({end_desc}).")
    return (f"subject_definitions:\n{subj}\n\n"
            f"summary:\n{summary}\n\n"
            f"retention_analysis:\n{retention}\n\n"
            f"detailed_description:\n{detail}\n\n"
            f"overall_soundscape:\n{sounds}\n\n"
            f"{NOMUSIC}\n\n"
            f"negative: color, multiple people, second boy, duplicate character, extra "
            f"chairs, extra figures, bright wall, white wall, cream wall, visible "
            f"ceiling, text, subtitles, watermark, logo, {extra_neg}")

SHOTS = [
 dict(key="A", kind="r2v", save="jaisal_intro_A_walkin",
      refs=["table empty.png", "jaisal_hand_under_the_table.png"], length=124,
      prompt=r2v_prompt(
        "the empty dark room - wooden table, one chair, single bare bulb above, NO person",
        "the boy seated at the table, both hands resting UNDER the table edge",
        "the bare bulb swings gently; a chair scrapes across the floor; the boy <Subject 1> "
        "enters from the darkness, drags the chair, and sits down, hands dropping under the "
        "table. He does NOT stand, does NOT leave, is NOT duplicated.",
        "a WIDE STATIC eye-level shot (35mm), the camera is locked and does NOT move, push, "
        "drift, tilt, pan or zoom.",
        "room tone, a soft chair scrape, a gentle breath.",
        extra_neg="the boy standing, the boy leaving, a second person")),

 dict(key="B", kind="r2v", save="jaisal_intro_B_setup",
      refs=["jaisal_hand_under_the_table.png", "jaisal_with_hand_on_table.png"], length=73,
      prompt=r2v_prompt(
        "the boy seated at the table, both hands UNDER the table edge",
        "the boy seated at the table, both hands placed FLAT ON the tabletop",
        "the boy <Subject 1> slowly brings both hands up from under the table and rests them "
        "flat on the tabletop, looking forward, ready to speak. He stays seated, does NOT "
        "stand, is NOT duplicated.",
        "a MEDIUM shot, slight low angle (50mm), the camera is locked and static.",
        "soft cloth movement, a quiet breath.",
        extra_neg="the boy standing, hands under the table at the end, a second person")),

 dict(key="C", kind="cam", save="jaisal_intro_C_headtwist_180",
      refs=["jaisal_head_left_back_side.png"], length=243,
      cam_traj='[{"time":0,"azimuth":0,"elevation":0,"distance":1},'
               '{"time":0.5,"azimuth":90,"elevation":0,"distance":0.9},'
               '{"time":1,"azimuth":180,"elevation":0,"distance":0.8}]',
      cam_instr=("The boy <Subject 1> is seated at the table, hands on the tabletop, seen from "
                 "his LEFT side. The camera orbits SLOWLY 180 degrees around him at a steady "
                 "rate, pushing in slightly, ending at his BACK (180 degrees). His body stays "
                 "still; only the camera moves. Black & white, high contrast, fine film grain. "
                 "The room, table, chair and single bare bulb stay exactly the same. ONLY ONE "
                 "boy, no duplicates. Ends with the camera at his BACK.")),

 dict(key="D", kind="r2v", save="jaisal_intro_D_reverse",
      refs=["jaisal_head_180_dergree.png", "jaisal_with_hand_on_table.png"], length=175,
      prompt=r2v_prompt(
        "the boy's head turned 180 degrees (back view), body still at the table",
        "the boy back to NORMAL - facing forward, both hands flat on the tabletop",
        "everything REVERSES perfectly: the head un-rotates from 180 degrees back to facing "
        "forward, the camera un-orbits, and we land on the ordinary seated boy <Subject 1> "
        "facing the camera, hands on the table. The weird version was his mind. He is NOT "
        "duplicated.",
        "a MEDIUM shot (50mm); the camera orbits back from the 180-degree position to the "
        "front, then holds static.",
        "reversed room tone, a soft breath, then stillness.",
        extra_neg="the head staying turned, a second person")),

 dict(key="E", kind="r2v", save="jaisal_intro_E_plants_grow",
      refs=["jaisal_with_hand_on_table.png", "plants_Alive.png"], length=311,
      prompt=r2v_prompt(
        "the boy seated at the table, hands on the tabletop, table otherwise empty",
        "small green plants and a rose GROWN on the table around the boy",
        "plants GROW (they do not fade in): one tiny stem pushes through the table surface, "
        "another follows, a rose slowly opens, and small plants populate the table. The boy "
        "<Subject 1> stays seated and still, watching. He is NOT duplicated.",
        "a MEDIUM shot that slowly PUSHES to a close-up (50mm to 85mm).",
        "soft rustling of growing leaves, a gentle low hum.",
        extra_neg="the boy standing, plants fading in magically, a second person")),

 dict(key="F", kind="r2v", save="jaisal_intro_F_plants_die",
      refs=["plants_Alive.png", "plants_dead.png"], length=430,
      prompt=r2v_prompt(
        "small green plants and a rose alive on the table around the seated boy",
        "the SAME plants now DEAD and withered on the table",
        "while the boy <Subject 1> sits in silence: a leaf falls, a stem bends, the rose "
        "closes, and the plants slowly wither and die, the table emptying out. No AI glow, no "
        "holograms - just limitation. The boy stays seated, is NOT duplicated.",
        "a CLOSE-UP shot (85mm), the camera is locked and static.",
        "a dry leaf crack, a slow breath, then silence.",
        extra_neg="plants staying alive, glowing effects, holograms, a second person")),

 dict(key="G", kind="r2v", save="jaisal_intro_G_vanish_burst",
      refs=["plants_dead.png", "jaisal_gone_papers_alone.png"], length=73,
      prompt=r2v_prompt(
        "the boy seated at the table with dead plants",
        "the boy COMPLETELY GONE - the chair is empty, replaced by loose floating papers",
        "ABSENCE FIRST: the boy <Subject 1> VANISHES - a burst of loose sheets of paper "
        "erupts from the exact space where he was sitting, physically displacing him, drifting "
        "forward through the room. The chair is now EMPTY. There is NO PERSON remaining in the "
        "final frame. No fire, no smoke, no glowing particles, no holograms.",
        "a MEDIUM WIDE shot (35mm), the camera is locked and static.",
        "a burst of paper rustle, then quiet room tone.",
        task="[keyframe completion]",
        extra_neg="man, person, human, face, head, body, arms, hands, legs, clothing, "
                  "silhouette, ghost, transparent person, partial person, duplicate person, "
                  "visible human, humanoid, mannequin, glowing particles, fire, smoke, hologram")),

 dict(key="H", kind="r2v", save="jaisal_intro_H_mic_paper",
      refs=["jaisal_gone_papers_alone.png", "mic+paper_2k.png"], length=73,
      prompt=r2v_prompt(
        "loose papers floating in the dark room, the chair empty, NO person",
        "a MICROPHONE settled among the floating papers",
        "a microphone emerges from the darkness and settles among the floating papers. The "
        "papers keep drifting. There is NO PERSON in this shot - only the papers and the "
        "microphone. No glowing effects.",
        "a MEDIUM WIDE shot (35mm), the camera is locked and static.",
        "a soft thud as the microphone lands, paper rustle.",
        extra_neg="man, person, human, face, body, a second microphone, glowing particles, "
                  "hologram")),

 dict(key="I", kind="r2v", save="jaisal_intro_I_mic_alone",
      refs=["mic+paper_2k.png", "mic_without paper_final scene.png"], length=56,
      prompt=r2v_prompt(
        "a microphone among floating papers in the dark room",
        "ONLY the microphone - the papers are gone",
        "the floating papers drift back and VANISH into the darkness, leaving ONLY the "
        "microphone in the light. There is NO PERSON. No glowing effects.",
        "a MEDIUM shot (50mm), the camera is locked and static.",
        "paper rustle fading out, quiet room tone.",
        extra_neg="man, person, human, face, body, papers remaining in the final frame, "
                  "glowing particles")),

 dict(key="J", kind="r2v", save="jaisal_intro_J_objects_join",
      refs=["mic_without paper_final scene.png", "obj_cricket_bat_00002_.png",
            "obj_soccer_ball_00002_.png", "obj_paper_smiley_00002_.png"], length=73,
      prompt=(
        "subject_definitions:\n"
        "<Subject 1> is the microphone already settled in the light in the dark room.\n"
        "<Picture 1> is the FIRST frame: only the microphone in the light.\n"
        "<Picture 2> is a reference for the CRICKET BAT (vertical, blade down, handle up).\n"
        "<Picture 3> is a reference for the round SOCCER BALL.\n"
        "<Picture 4> is a reference for the PAPER with a simple curved smile line.\n\n"
        "summary:\n[reference generation] A single continuous black & white take. "
        + SCENE + " Cricket objects join the microphone: a cricket bat and stumps fly into "
        "the light, a round soccer ball rolls in underneath them, and one paper with a curved "
        "smile line settles on TOP of the bat as a crude head. These are fragments of ideas - "
        "mic = voice, cricket = sports, papers = stories.\n\n"
        "retention_analysis:\n"
        "<Subject 1> (the microphone): fully_preserved - the microphone stays in the light.\n"
        "<Picture 2> (cricket bat): attribute_transfer - exactly ONE cricket bat, vertical.\n"
        "<Picture 3> (soccer ball): attribute_transfer - exactly ONE round soccer ball.\n"
        "<Picture 4> (paper smiley): attribute_transfer - exactly ONE paper with a smile line.\n\n"
        "detailed_description:\n"
        "The target video is black & white, high contrast, fine film grain. " + SCENE + "\n"
        "[Shot 1] The shot BEGINS from <Picture 1> (only the microphone in the light). A "
        "cricket bat and a set of stumps fly into the light, then a round soccer ball rolls in "
        "underneath them, and one paper with a curved smile line settles on TOP of the bat as "
        "a crude head. Keep exactly ONE cricket bat, exactly ONE round soccer ball, exactly "
        "ONE set of stumps, exactly ONE paper. The ball rests on the table, the bat stands "
        "vertically balanced on top of the ball, the paper is attached to the HANDLE of the "
        "bat. There is NO PERSON. No fire, no smoke, no glowing particles, no holograms, no "
        "colorful effects - the impact comes from paper, physical objects, motion, shadows "
        "and sound only.\n\n"
        "overall_soundscape:\na soft bat tap, a ball rolling, a paper settling, quiet room tone.\n\n"
        + NOMUSIC + "\n\n"
        "negative: color, multiple bats, two bats, multiple balls, two balls, extra papers, "
        "many papers, man, person, human, face, body, glowing particles, fire, smoke, "
        "hologram, text, subtitles, watermark")),
]

def load(p):
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)

def save(wf, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(wf, f, ensure_ascii=False, separators=(",", ":"))

def find_node(wf, ntype):
    for n in wf["nodes"]:
        if n.get("type") == ntype:
            return n
    return None

def find_nodes(wf, ntype):
    return [n for n in wf["nodes"] if n.get("type") == ntype]

def get_link(wf, link_id):
    for l in wf["links"]:
        if l[0] == link_id:
            return l
    return None

def ensure_link(wf, link_id, src_id, src_slot, tgt_id, tgt_slot, ltype):
    l = get_link(wf, link_id)
    if l is None:
        l = [link_id, src_id, src_slot, tgt_id, tgt_slot, ltype]
        wf["links"].append(l)
    else:
        l[1] = src_id; l[2] = src_slot; l[3] = tgt_id; l[4] = tgt_slot
    return l

def clone_loadimage(wf, src_node, new_id, filename):
    new = copy.deepcopy(src_node)
    new["id"] = new_id
    new["widgets_values"] = [filename, "image"]
    for out in new.get("outputs", []):
        out["links"] = None
    wf["nodes"].append(new)
    return new

def build_r2v(shot):
    wf = load(R2V_TPL)
    r2v = find_node(wf, "MiniMaxH3ReferenceToVideo")
    prompt_node = find_node(wf, "PrimitiveStringMultiline")
    save_node = find_node(wf, "SaveVideo")
    li_nodes = find_nodes(wf, "LoadImage")          # template has 3 (137,139,148)
    refs = shot["refs"]
    n_refs = len(refs)
    # ensure enough LoadImage nodes (clone a 4th for shot J)
    while len(li_nodes) < n_refs:
        base = li_nodes[0]
        new_id = max(n["id"] for n in wf["nodes"]) + 1
        new_node = clone_loadimage(wf, base, new_id, refs[len(li_nodes)])
        li_nodes.append(new_node)
    # wire each ref -> its LoadImage node -> R2V ref_image_i slot
    for i in range(n_refs):
        li = li_nodes[i]
        li["widgets_values"] = [refs[i], "image"]
        lid = 300 + i
        ensure_link(wf, lid, li["id"], 0, r2v["id"], i, "IMAGE")
        for out in li.get("outputs", []):
            if out.get("name") == "IMAGE":
                out["links"] = [lid]
        for inp in r2v["inputs"]:
            if inp.get("name") == f"ref_image_{i}":
                inp["link"] = lid
    # clear unused ref slots (only ref_image_<digit>, NOT ref_image_size)
    import re
    for inp in r2v["inputs"]:
        name = inp.get("name", "")
        m = re.match(r"^ref_image_(\d+)$", name)
        if m:
            idx = int(m.group(1))
            if idx >= n_refs:
                inp["link"] = None
    # prompt
    if prompt_node is not None:
        prompt_node["widgets_values"] = [shot["prompt"]]
    # length (R2V widget index 3 is effective; the length link is dangling)
    if r2v.get("widgets_values") and len(r2v["widgets_values"]) > 3:
        r2v["widgets_values"][3] = shot["length"]
    # save prefix
    if save_node is not None and save_node.get("widgets_values"):
        save_node["widgets_values"][0] = shot["save"]
    return wf

def build_cam(shot):
    wf = load(CAM_TPL)
    li = find_node(wf, "LoadImage")
    if li is not None:
        li["widgets_values"] = [shot["refs"][0], "image"]
    cam = find_node(wf, "H3LocalCameraEditor")
    if cam is not None and cam.get("widgets_values"):
        wv = list(cam["widgets_values"])
        if len(wv) > 0:
            wv[0] = shot["cam_traj"]
        if len(wv) > 3:
            wv[3] = shot["cam_instr"]
        cam["widgets_values"] = wv
    save_node = find_node(wf, "SaveVideo")
    if save_node is not None and save_node.get("widgets_values"):
        save_node["widgets_values"][0] = shot["save"]
    return wf

def main():
    created = []
    for shot in SHOTS:
        wf = build_r2v(shot) if shot["kind"] == "r2v" else build_cam(shot)
        path = os.path.join(WF_DIR, shot["save"] + ".json")
        save(wf, path)
        created.append(shot["save"] + ".json")
        print("built:", shot["save"] + ".json",
              "refs=" + str(shot["refs"]), "len=" + str(shot["length"]))
    print("\n=== " + str(len(created)) + " workflows created in " + WF_DIR + " ===")
    for c in created:
        print("  " + c)

if __name__ == "__main__":
    main()
