const shell = document.getElementById('app-shell');
const messages = document.getElementById('messages');
const form = document.getElementById('chat-form');
const input = document.getElementById('message-input');
const sendButton = document.getElementById('send-button');
const resetButton = document.getElementById('reset-button');
const statusText = document.getElementById('status-text');
const coreLabel = document.getElementById('core-label');
const linkLabel = document.getElementById('link-label');
const requestStatus = document.getElementById('request-status');
const charsLeft = document.getElementById('chars-left');
let pending = false;
let sessionController = null;
let sessionId = 0;

function setState(state) {
  shell.dataset.state = state;
  const labels = {
    idle: ['AWAITING INPUT', 'STANDBY', 'READY'],
    thinking: ['PROCESSING REQUEST', 'ACTIVE', 'TRANSMITTING'],
    error: ['SIGNAL INTERRUPTED', 'ERROR', 'RETRY AVAILABLE'],
  };
  const [status, core, request] = labels[state];
  statusText.textContent = status;
  coreLabel.textContent = core;
  requestStatus.textContent = request;
}
function addMessage(content, who) {
  const wrapper = document.createElement('div');
  wrapper.className = `message ${who === 'user' ? 'user-message' : 'nova-message'}`;
  const author = document.createElement('span');
  author.className = 'message-author';
  author.textContent = who === 'user' ? 'OPERATOR · YOU' : 'NOVA · SYSTEM';
  const body = document.createElement('div');
  body.className = 'message-body';
  body.textContent = content; // Do not inject LLM output as HTML.
  wrapper.append(author, body);
  messages.append(wrapper);
  messages.scrollTop = messages.scrollHeight;
  return body;
}
function updateInput() {
  charsLeft.textContent = `${input.value.length} / 10000`;
  input.style.height = 'auto';
  input.style.height = `${Math.min(input.scrollHeight, 135)}px`;
}
input.addEventListener('input', updateInput);
input.addEventListener('keydown', (event) => {
  if (event.key === 'Enter' && !event.shiftKey && !event.isComposing) {
    event.preventDefault();
    if (!pending && input.value.trim()) form.requestSubmit();
  }
});
function setPending(value) {
  pending = value;
  sendButton.disabled = value;
  input.disabled = value;
}
form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const message = input.value.trim();
  if (!message || pending) return;
  const mySession = sessionId;
  setPending(true);
  setState('thinking');
  addMessage(message, 'user');
  input.value = '';
  updateInput();
  const answerNode = addMessage('Establishing neural link…', 'nova');
  sessionController = new AbortController();
  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message }),
      signal: sessionController.signal,
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const result = await response.json();
    if (mySession !== sessionId) return;
    if (typeof result.answer !== 'string' || !result.answer.trim()) throw new Error('Empty answer');
    answerNode.textContent = result.answer;
    setState('idle');
    linkLabel.textContent = 'API CONNECTED';
  } catch (error) {
    if (mySession !== sessionId || error.name === 'AbortError') return;
    console.error('NOVA request failed:', error);
    answerNode.textContent = 'Не удалось получить ответ. Проверь подключение к API и попробуй снова.';
    linkLabel.textContent = 'CHECK CONNECTION';
    setState('error');
  } finally {
    if (mySession === sessionId) {
      sessionController = null;
      setPending(false);
      input.focus();
      messages.scrollTop = messages.scrollHeight;
    }
  }
});
resetButton.addEventListener('click', () => {
  sessionId += 1;
  if (sessionController) sessionController.abort();
  sessionController = null;
  setPending(false);
  messages.replaceChildren();
  addMessage('Новая сессия запущена. Все системы готовы.', 'nova');
  input.value = '';
  updateInput();
  setState('idle');
  linkLabel.textContent = 'API CONNECTED';
  input.focus();
});
function refreshClock() {
  document.getElementById('clock').textContent = new Date().toLocaleTimeString('en-GB', { hour12: false });
}
refreshClock();
setInterval(refreshClock, 1000);
updateInput();