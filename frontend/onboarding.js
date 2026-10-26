import { t } from '/i18n.js';
// View state lives in the URL only; onboarding never stores or sends notice data.
const flowNode = id => document.getElementById(id);
const flowScreens = ['welcome-screen', 'tutorial-screen', 'notice-screen'];
let tutorialStep = 1;
function renderFlow(focus = true) {
  const hash = window.location.hash;
  const match = /^#tutorial\/([1-4])$/.exec(hash);
  const screen = hash === '#notice' ? 'notice-screen' : match ? 'tutorial-screen' : 'welcome-screen';
  tutorialStep = match ? Number(match[1]) : 1;
  for (const id of flowScreens) flowNode(id).hidden = id !== screen;
  if (screen === 'tutorial-screen') {
    flowNode('tutorial-title').textContent = t(`tutorial_${tutorialStep}_title`);
    flowNode('tutorial-body').textContent = t(`tutorial_${tutorialStep}_body`);
    flowNode('tutorial-progress').textContent = t('tutorial_progress', {step:tutorialStep,total:4});
    flowNode('tutorial-next').textContent = t(tutorialStep === 4 ? 'tutorial_finish' : 'tutorial_next');
    flowNode('tutorial-screen').dataset.step = String(tutorialStep);
    for (let i = 1; i <= 4; i++) flowNode(`tutorial-art-${i}`).hidden = i !== tutorialStep;
  }
  if (focus) flowNode(screen === 'notice-screen' ? 'reader-title' : screen === 'tutorial-screen' ? 'tutorial-title' : 'welcome-title').focus();
}
const navigateFlow = hash => { window.location.hash = hash; };
flowNode('get-started').addEventListener('click', () => navigateFlow('#tutorial/1'));
flowNode('replay-tutorial').addEventListener('click', () => navigateFlow('#tutorial/1'));
flowNode('skip-tutorial').addEventListener('click', () => navigateFlow('#notice'));
flowNode('tutorial-next').addEventListener('click', () => navigateFlow(tutorialStep === 4 ? '#notice' : `#tutorial/${tutorialStep + 1}`));
flowNode('tutorial-back').addEventListener('click', () => navigateFlow(tutorialStep === 1 ? '#welcome' : `#tutorial/${tutorialStep - 1}`));
window.addEventListener('hashchange', () => renderFlow());
window.addEventListener('notice-language', () => renderFlow(false));
const storyDialog = flowNode('story-dialog');
flowNode('open-story').addEventListener('click', () => storyDialog.showModal());
flowNode('close-story').addEventListener('click', () => storyDialog.close());
storyDialog.addEventListener('close', () => flowNode('open-story').focus());
renderFlow(false);
