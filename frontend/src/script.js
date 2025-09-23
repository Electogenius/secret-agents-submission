// Minimal, purposeful JS
let apiUrl = 'https://tb6thx4hctkh8-crewai--3000.prod1b.defang.dev/generate';

// Elements
const menuBtn = document.getElementById('menuBtn');
const sidebar = document.getElementById('sidebar');
const main = document.getElementById('main');
const modeBtns = [...document.querySelectorAll('.mode-btn')];
const modeTitle = document.getElementById('modeTitle');
const panels = { general: document.getElementById('chatMode'), questions: document.getElementById('questionMode'), collections: document.getElementById('collectionsMode') };

const chatWindow = document.getElementById('chatWindow');
const chatForm = document.getElementById('chatForm');
const chatInput = document.getElementById('chatInput');
const topicInput = document.getElementById('topicInput');
const collectionsList = document.getElementById('collectionsList');
const collectionsList2 = document.getElementById('collectionsList2');
const exportChatBtn = document.getElementById('exportChat');
const clearChatBtn = document.getElementById('clearChat');
const clearAllBtn = document.getElementById('clearAll');

let state = {
  mode: 'general',
  chat: [], // {who: 'user'|'ai', text}
  collections: [] // {title, questions: [qstr]}
};

// Persistence
const STORAGE_KEY = 'duckai_sample_state_v1';
function saveState(){ localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); }
function loadState(){
  const raw = localStorage.getItem(STORAGE_KEY);
  if(raw){ try{ state = JSON.parse(raw); }catch(e){ state = state; } }
}
loadState();

// UI helpers
function setMode(m){
  state.mode = m;
  modeBtns.forEach(b=>b.classList.toggle('active', b.dataset.mode===m));
  Object.values(panels).forEach(p=>p.classList.add('hidden'));
  panels[m].classList.remove('hidden');
  modeTitle.textContent = m==='general'?'General': m==='questions'?'Question Generation':'Collections';
  saveState();
  renderCollections();
}
modeBtns.forEach(b=>b.addEventListener('click', ()=>setMode(b.dataset.mode)));

// Sidebar toggle
menuBtn.addEventListener('click', ()=>{
  sidebar.classList.toggle('open');
  // main margin handled by css sibling selector
});

// addBubble function as requested
function addBubble(who, content){
  const div = document.createElement('div');
  div.className = 'bubble ' + (who==='user' ? 'user' : 'ai');
  if (who === 'user') {
    div.textContent = content
  } else {
    console.log(marked.parse(content))
    div.innerHTML = marked.parse(content)
  }
  chatWindow.appendChild(div);
  chatWindow.scrollTop = chatWindow.scrollHeight;
  // update state
  state.chat.push({who: who==='user' ? 'user' : 'ai', text: content});
  saveState();
}
window.addBubble = addBubble; // expose

// Render saved chat
function renderChat(){
  chatWindow.innerHTML = '';
  (state.chat || []).forEach(m => {
    const d = document.createElement('div');
    d.className = 'bubble ' + (m.who==='user' ? 'user' : 'ai');
    if (m.who === 'user') {
    d.textContent = m.text
  } else {
    console.log(marked.parse(m.text))
    d.innerHTML = marked.parse(m.text)
  }
    chatWindow.appendChild(d);
  });
  chatWindow.scrollTop = chatWindow.scrollHeight;
}
renderChat();

// Send to API helper
async function postPrompt(promptText){
  try{
    const resp = await fetch(apiUrl, {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({ user_text: promptText })
    });
    if(!resp.ok) throw new Error('Network error');
    const j = await resp.json();
    return j.response || j.result || JSON.stringify(j);
  }catch(e){
    return 'Error: '+e.message;
  }
}

function prelude(){
    let chat = exportChatText()
    return `You are a helpful AI assistant. Your primary job is to clear doubts and explain questions, on a variety of topics.
    ${
        chat.trim() ? `
        You are in the midst of a conversation with the user. Here is the overview of the conversation so far:
        <begin-context>
${chat}
        <end-context>
        ` : ""
    }
    Here begins the user's prompt:
    `
}

// Chat form behavior
chatForm.addEventListener('submit', async (e)=>{
  e.preventDefault();
  const txt = (chatInput.value || '').trim();
  if(!txt) return;
  addBubble('user', txt);
  chatInput.value = '';
  // send prompt
  const res = await postPrompt(prelude() + txt);
  addBubble('ai', res);
});

// Export chat function (returns chat log string)
function exportChatText(){
  // "user: …, ai: …, user: …, ai: …"
  return state.chat.map(m => `${m.who.toUpperCase()}: ${m.text}`).join('\n\n');
}
exportChatBtn.addEventListener('click', ()=>{
  const txt = exportChatText();
  // quick copy-to-clipboard
  navigator.clipboard?.writeText(txt).then(()=>alert('Chat copied to clipboard'), ()=>alert('Export:\n'+txt));
});

// Clear chat
clearChatBtn.addEventListener('click', ()=>{
  state.chat = [];
  saveState();
  renderChat();
});

// Clear all local (including collections)
clearAllBtn.addEventListener('click', ()=>{
  if(!confirm('Clear all saved chat and collections?')) return;
  state = {mode:'general', chat:[], collections:[]};
  saveState();
  renderChat();
  renderCollections();
});

// Question generation behavior
function makeCollection(title, questions){
  return { title, questions };
}
function renderCollections(){
  [collectionsList, collectionsList2].forEach(listEl=>{
    listEl.innerHTML = '';
    (state.collections || []).forEach((col, idx)=>{
      const wrapper = document.createElement('div');
      wrapper.className = 'collection';
      const head = document.createElement('div');
      head.className = 'col-head';
      const title = document.createElement('div');
      title.className = 'col-title';
      title.textContent = col.title;
      const meta = document.createElement('div');
      meta.className = 'small';
      meta.textContent = `${col.questions.length} questions`;
      head.appendChild(title);
      head.appendChild(meta);
      const body = document.createElement('div');
      body.className = 'col-body';
      col.questions.forEach(q=>{
        const qEl = document.createElement('div');
        qEl.className = 'question';
        qEl.textContent = q;
        qEl.title = 'Double-click to ask AI for explanation';
        qEl.addEventListener('dblclick', async ()=>{
          // switch to general, add user bubble with the question and prompt AI to explain
          setMode('general');
          addBubble('user', q);
          const prompt = `Explain the answer to the question: ${q}`;
          const res = await postPrompt(prompt);
          addBubble('ai', res);
        });
        body.appendChild(qEl);
      });
      head.addEventListener('click', ()=> body.classList.toggle('open'));
      wrapper.appendChild(head);
      wrapper.appendChild(body);
      listEl.appendChild(wrapper);
    });
    if((state.collections || []).length===0){
      const none = document.createElement('div');
      none.className = 'small';
      none.textContent = 'No collections yet. Create one by entering a topic above.';
      listEl.appendChild(none);
    }
  });
}
renderCollections();

// When user enters a topic
topicInput?.addEventListener('keydown', async (e)=>{
  if(e.key !== 'Enter') return;
  const topic = (topicInput.value || '').trim();
  if(!topic) return;
  topicInput.value = '';
  const prompt = `Generate 10 practice questions on the topic: ${topic} without answers`;
  const res = await postPrompt(prompt);
  // Try to split into individual questions by lines or numbers
  const items = res.split(/\r?\n/).map(s=>s.replace(/^\s*\d+[\).\s-]*/,'').trim()).filter(Boolean);
  const title = `Topic: ${topic}`;
  state.collections = state.collections || [];
  state.collections.unshift(makeCollection(title, items));
  saveState();
  renderCollections();
  setMode('collections');
});

// expose export function and chat retrieval
window.getChatLogText = exportChatText; // as requested

// initialize mode
setMode(state.mode || 'general');
