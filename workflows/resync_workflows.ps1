# resync_workflows.ps1 - re-copy the curated workflow mirror (2026-10-25)
# Copies the reusable workflows from the canonical ComfyUI dir into this repo dir,
# so `git diff` shows what changed since the last sync. Safe: only overwrites
# mirror files, never touches the canonical originals.
$src = "E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"
$dst = Split-Path -Parent $MyInvocation.MyCommand.Path
$names = @("CharSwap_v1.1_fro_LOCAL.json","FastH3_Omni_R2V_LOCAL.json","H3_HyperFlow_Fast_LOCAL.json","H3_Recast_LOCAL.json","H3-Person-Removal_LOCAL.json","H3-Person-Removal-Relay-V2_REFERENCE.json","k2f_jaisal_crookednose.json","k2f_jaisal_movie_shot_16x9.json","k2f_jaisal_movie_shot_16x9_d045.json","k2f_jaisal_movie_shot_16x9_oneclick.json","k2f_jaisal_movie_shot_16x9_packrecipe.json","k2f_jaisal_movie_shot_16x9_packrecipe_qwenvae.json","k2f_jaisal_movie_shot_16x9_qwenvae.json","k2f_jaisal_movie_shot_16x9_rawbf16.json","k2f_jaisal_S1_paddy_16x9_oneclick.json","k2f_jaisal_S2_house_16x9_oneclick.json","k2f_jaisal_S3_interior_16x9_oneclick.json","k2f_jaisal_S4_bike_16x9_oneclick.json","k2f_jaisal_S5_7s_ground_16x9_oneclick.json","k2f_jaisal_S6_village_16x9_oneclick.json","k2f_jaisal_scenes.json","k2f_zidhan_S1_paddy_16x9_oneclick.json","k2f_zidhan_scenes.json","k2f_zidhan_sharpnose.json","minimaxH3BackgroundSwap_v21a_LOCAL.json","MiniMax-H3-Character-Swap-Mask_LOCAL.json","RTX_Post_VFX_LOCAL.json","sol_h3_Sol-H3-Studio.json","sol_h3_t2v.json","TTS_Suite_ASR_SRT_Builder_REFERENCE.json","TTS_Suite_OmniVoice_REFERENCE.json","TTS_Suite_TTS_SRT_REFERENCE.json","VRGDG_MiniMaxH3_2Pass_MusicVideo_LOCAL.json","VNCCS_PoseStudio_QI2.1_REFERENCE.json","withers_has_big_nattys.json","withers_has_big_nattys_LOCAL.json")
$missing = 0
foreach ($n in $names) {
  $p = Join-Path $src $n
  if (Test-Path $p) {
    Copy-Item $p $dst -Force
  } else {
    Write-Output "MISSING (skipped): $n"
    $missing++
  }
}
Write-Output "resync done: $((Get-ChildItem $dst -Filter *.json).Count) mirror files, $missing missing at source."
