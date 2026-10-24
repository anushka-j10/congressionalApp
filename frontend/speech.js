// Never choose an unrelated voice. Locale aliases are language configuration.
export function selectVoice(cfg, voices) {
  const locales = [cfg.speech_synthesis_locale, ...(cfg.speech_aliases || [])].map(value => value.toLowerCase());
  return voices.find(voice => locales.includes(voice.lang.toLowerCase())) ||
    voices.find(voice => locales.some(locale => locale.split('-')[0] === voice.lang.toLowerCase().split('-')[0])) || null;
}

export function createSpeechController(nodes, translate) {
  const synth = window.speechSynthesis;
  let text = '', cfg = null, voice = null;
  function stop() { synth?.cancel(); nodes.pause.textContent = translate('pause'); }
  function refresh() {
    voice = cfg && synth ? selectVoice(cfg, synth.getVoices()) : null;
    nodes.play.disabled = !voice || !text;
    nodes.pause.disabled = nodes.stop.disabled = !voice || !text;
    nodes.note.textContent = text && !voice ? translate('no_voice') : '';
  }
  nodes.play.addEventListener('click', () => {
    if (!voice || !text || !synth) return;
    stop();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.voice = voice;
    utterance.lang = voice.lang;
    utterance.onerror = () => { nodes.note.textContent = translate('voice_error'); };
    synth.speak(utterance);
  });
  nodes.pause.addEventListener('click', () => {
    if (!synth || !voice) return;
    if (synth.paused) { synth.resume(); nodes.pause.textContent = translate('pause'); }
    else { synth.pause(); nodes.pause.textContent = translate('resume'); }
  });
  nodes.stop.addEventListener('click', stop);
  synth?.addEventListener('voiceschanged', refresh);
  window.addEventListener('pagehide', stop);
  return { set(value, configuration) { stop(); text = value; cfg = configuration; refresh(); },
    clear() { stop(); text = ''; cfg = null; refresh(); }, stop };
}
