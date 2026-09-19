'use strict';
const $=id=>document.getElementById(id);
let cases=[],current,draft,activeQuestion,last=null,lastRequest=null,lastOrigin=null,liveAvailable=false;
const clone=x=>structuredClone(x),same=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const finite=(v,min=0,max=1)=>typeof v==='number'&&Number.isFinite(v)&&v>=min&&v<=max;
const money=x=>x.toLocaleString('pt-BR',{style:'currency',currency:'USD',minimumFractionDigits:2,maximumFractionDigits:6});
function node(tag,text,className){const e=document.createElement(tag);if(text!==undefined)e.textContent=text;if(className)e.className=className;return e}
function setStatus(text){$('status').textContent=text}
function themeLabel(){$('theme').textContent=document.body.classList.contains('light')?'Tema escuro':'Tema claro'}
try{document.body.classList.toggle('light',localStorage.getItem('jev-theme')==='light')}catch{}
themeLabel();$('theme').onclick=()=>{document.body.classList.toggle('light');try{localStorage.setItem('jev-theme',document.body.classList.contains('light')?'light':'dark')}catch{}themeLabel()};
function validate(p){
 if(!p||typeof p!=='object'||typeof p.model!=='string'||!p.model.trim())throw Error('Informe um modelo no JSON.');
 if(!p.state||!['string','object'].includes(typeof p.state)||(typeof p.state==='string'&&!p.state.trim())||(typeof p.state==='object'&&!Object.keys(p.state).length))throw Error('Preencha o contexto.');
 if(!p.questions||typeof p.questions!=='object'||Array.isArray(p.questions)||Object.keys(p.questions).length<1||Object.keys(p.questions).length>30)throw Error('Use de 1 a 30 perguntas neste laboratório.');
 for(const [id,q] of Object.entries(p.questions)){
  if(!id||!q||typeof q.instructions!=='string'||!q.instructions.trim())throw Error('Toda pergunta precisa de instruções textuais.');
  const c=q.criteria;
  if(q.type==='choice'){
   if(!c||typeof c!=='object'||Array.isArray(c)||Object.keys(c).length<2||Object.keys(c).length>255||Object.entries(c).some(([k,v])=>!k||(v!==null&&typeof v!=='string')))throw Error('Choice precisa de 2 a 255 alternativas com descrições textuais ou null.');
  }else if(q.type==='score'){
   if(!Array.isArray(c)||c.length<2||c.length>10||c.some(x=>typeof x!=='string'||!x.trim()))throw Error('Score precisa de 2 a 10 descrições ordenadas.');
  }else if(q.type==='noul'){
   if(c!==undefined&&c!==null&&(!c||typeof c!=='object'||Array.isArray(c)||!Object.keys(c).length||Object.entries(c).some(([k,v])=>!['true','false'].includes(k)||typeof v!=='string'||!v.trim())))throw Error('Noul aceita null ou descrições true/false.');
  }else throw Error('Tipo desconhecido. Use Choice, Noul ou Score.');
 }
 // JSON textual não suporta valores não finitos. A codificação conservadora aproxima o limite do servidor.
 const encoded=JSON.stringify(p).replace(/[^\x00-\x7F]/g,ch=>'\\u'+ch.charCodeAt(0).toString(16).padStart(4,'0'));
 if(new TextEncoder().encode(encoded).length>100000)throw Error('Requisição excede o limite local de 100 KB. Reduza o contexto.');
 return p;
}
function readPayload(){
 const p=clone(draft);p.state=$('stateFormat').value==='json'?JSON.parse($('state').value):$('state').value;
 const q=p.questions[activeQuestion];q.type=$('questionType').value;q.instructions=$('question').value;
 const c=JSON.parse($('criteria').value);if(q.type==='noul'&&c===null)delete q.criteria;else q.criteria=c;
 return validate(p);
}
function drawOptions(q){
 $('options').replaceChildren();
 if(q.type==='noul'&&!q.criteria){$('options').append(node('dt','sim / não'),node('dd','O resultado informa a probabilidade de sim, entre 0 e 1.'));return}
 for(const [k,v] of Object.entries(q.criteria||{}))$('options').append(node('dt',k),node('dd',v??'Sem descrição adicional.'));
}
function invalidate(){last=null;lastRequest=null;$('result').hidden=true}
function update(){
 if(!current)return;invalidate();
 try{const p=readPayload();$('payload').textContent=JSON.stringify(p,null,2);drawOptions(p.questions[activeQuestion]);$('simulate').disabled=!current.fixture||!same(p,current.request);$('download').disabled=false;$('live').disabled=false;setStatus($('simulate').disabled?'Requisição editada. Exporte ou consulte o servidor local; não há resposta didática para esse conteúdo.':'')}
 catch(e){$('payload').textContent='Requisição incompleta.';$('simulate').disabled=true;$('download').disabled=true;$('live').disabled=true;setStatus(e instanceof SyntaxError?'JSON inválido no contexto ou nos critérios. Corrija a sintaxe ou restaure o exemplo.':e.message)}
}
function fillQuestion(){const q=draft.questions[activeQuestion];$('questionSelect').value=activeQuestion;$('question').value=q.instructions;$('questionType').value=q.type;$('criteria').value=JSON.stringify(q.criteria??null,null,2);$('kind').textContent=[...new Set(Object.values(draft.questions).map(q=>q.type))].join(' + ');drawOptions(q);$('removeQuestion').disabled=Object.keys(draft.questions).length===1}
function fillSelect(){ $('questionSelect').replaceChildren();for(const [id,q] of Object.entries(draft.questions))$('questionSelect').append(new Option(id+' · '+q.type,id));fillQuestion() }
function select(item){current=item;draft=clone(item.request);activeQuestion=Object.keys(draft.questions)[0];$('caseTitle').textContent=item.title;$('description').textContent=item.description;$('stateFormat').value=typeof draft.state==='string'?'text':'json';$('state').value=typeof draft.state==='string'?draft.state:JSON.stringify(draft.state,null,2);fillSelect();document.querySelectorAll('#cases button').forEach(b=>b.setAttribute('aria-current',String(b.dataset.id===item.id)));update()}
function drawCases(){
 const query=$('caseFilter').value.toLocaleLowerCase('pt-BR').trim();let group='';$('cases').replaceChildren();const filtered=cases.filter(c=>[c.title,c.description,c.group,...Object.values(c.request.questions).map(q=>q.type)].join(' ').toLocaleLowerCase('pt-BR').includes(query));
 for(const item of filtered){if(item.group!==group){group=item.group;$('cases').append(node('p',group,'group-label'))}const b=node('button',item.title);b.dataset.id=item.id;b.setAttribute('aria-current',String(current?.id===item.id));b.onclick=()=>select(item);$('cases').append(b)}
 $('caseCount').textContent=filtered.length?filtered.length+' exemplos · dados fictícios':'Nenhum caso encontrado. Tente outro termo.';
}
$('caseFilter').oninput=drawCases;
$('questionSelect').onchange=()=>{try{const next=$('questionSelect').value;draft=readPayload();activeQuestion=next;fillQuestion();update()}catch(e){$('questionSelect').value=activeQuestion;setStatus('Corrija a pergunta atual antes de trocar: '+e.message)}};
$('questionType').onchange=()=>{const t=$('questionType').value;$('criteria').value=JSON.stringify(t==='choice'?{opcao_a:'Descreva a primeira alternativa.',opcao_b:'Descreva a segunda alternativa.',insuficiente:'Faltam dados.'}:t==='score'?['Condição de menor intensidade','Condição de maior intensidade']:null,null,2);update()};
$('addQuestion').onclick=()=>{try{draft=readPayload();if(Object.keys(draft.questions).length>=30)throw Error('Limite local de 30 perguntas.');let n=1;while(draft.questions['pergunta_'+n])n++;activeQuestion='pergunta_'+n;draft.questions[activeQuestion]={type:'noul',instructions:'Há informação suficiente para este julgamento?'};fillSelect();update();$('question').focus()}catch(e){setStatus(e.message)}};
$('removeQuestion').onclick=()=>{if(Object.keys(draft.questions).length<=1)return;try{draft=readPayload();delete draft.questions[activeQuestion];activeQuestion=Object.keys(draft.questions)[0];fillSelect();update()}catch(e){setStatus(e.message)}};
for(const id of ['state','question','criteria'])$(id).oninput=update;
$('stateFormat').onchange=update;
$('reset').onclick=()=>select(current);
function download(name,content){const blob=new Blob([JSON.stringify(content,null,2)],{type:'application/json'}),url=URL.createObjectURL(blob),a=node('a');a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000)}
$('download').onclick=()=>{try{download(current.id+'-request.json',readPayload());setStatus('Requisição exportada. Revise dados pessoais antes de compartilhar.')}catch(e){setStatus(e.message)}};
$('importRequest').onchange=async event=>{try{const file=event.target.files[0];if(!file)return;if(file.size>100000)throw Error('Arquivo maior que 100 KB.');const p=validate(JSON.parse(await file.text()));select({id:'importado',title:'Sua requisição',description:'Conteúdo importado localmente. Nenhuma consulta é feita até você solicitar.',request:p,sensitive:true,explanation:'',next:'Confirme critérios e permissões antes de usar o resultado.'});setStatus('Requisição importada. Política conservadora: revisão obrigatória para conteúdo personalizado.')}catch(e){setStatus('Importação recusada: '+e.message)}finally{event.target.value=''}};
function bars(container,probabilities,legend){for(const [label,p] of Object.entries(probabilities)){const row=node('div',undefined,'bar-row'),track=node('div',undefined,'bar-track'),fill=node('div',undefined,'bar-fill');fill.style.width=(p*100)+'%';track.append(fill);row.append(node('span',legend?.[label]??label),track,node('span',(p*100).toFixed(1)+'%'));container.append(row)}}
function validateResult(p,response){
 if(!response||typeof response.model!=='string'||!response.answers||!same(Object.keys(response.answers).sort(),Object.keys(p.questions).sort()))throw Error('Resposta incompleta.');
 if(!response.usage||!['input_tokens','output_tokens'].every(k=>Number.isInteger(response.usage[k])&&response.usage[k]>=0))throw Error('Uso de tokens inválido.');
 for(const [id,q] of Object.entries(p.questions)){
  const a=response.answers[id];if(!a||a.type!==q.type)throw Error('Resposta com tipo inesperado.');
  if(q.type==='noul'){if(!finite(a.noul))throw Error('Noul inválido.');continue}
  const keys=Object.keys(q.criteria);if(!a.probabilities||!same(Object.keys(a.probabilities).sort(),keys.sort())||!Object.values(a.probabilities).every(v=>finite(v))||Math.abs(Object.values(a.probabilities).reduce((a,b)=>a+b,0)-1)>.001||!finite(a.confidence))throw Error('Distribuição inválida.');
  if(q.type==='choice'&&(!Object.hasOwn(q.criteria,a.choice)||a.probabilities[a.choice]+1e-6<Math.max(...Object.values(a.probabilities))))throw Error('Alternativa inconsistente.');
  if(q.type==='score'){const expected=Object.values(a.probabilities).reduce((sum,p,i)=>sum+i*p,0);if(!finite(a.score,0,q.criteria.length-1)||Math.abs(expected-a.score)>.01||!a.legend||!same(Object.keys(a.legend).sort(),keys.sort())||keys.some(k=>a.legend[k]!==q.criteria[k]))throw Error('Score ou legend inconsistente.');}
 }
}
function policyText(id,a,t){
 if(current.sensitive)return 'Revisar: domínio supervisionado ou requisição importada.';
 if(a.type==='noul')return Math.max(a.noul,1-a.noul)<t?'Revisar: sinal próximo da indecisão.':'Sinal em observação: '+(a.noul>=.5?'sim':'não')+'. Não executa ação.';
 if(a.confidence<t)return 'Revisar: confidence abaixo do limiar didático.';
 if(a.type==='score')return 'Nota em observação. A ação depende de uma política própria da rubrica.';
 if(['insuficiente','incerto','outro','nenhum','ambiguo','conflito','revisar'].includes(a.choice)||a.probabilities[a.choice]<.9)return 'Revisar: alternativa ou probabilidade exige atenção.';
 return 'Sugestão em observação. Nenhuma ação externa executada.';
}
function showPolicy(){if(!last)return;const t=Number($('threshold').value);$('thresholdValue').textContent=t.toFixed(2).replace('.',',');const texts=Object.entries(last.answers).map(([id,a])=>id+': '+policyText(id,a,t));$('decision').textContent=texts.join(' ')}
function render(response,origin,p){
 validateResult(p,response);last=response;lastRequest=clone(p);lastOrigin=origin;$('result').hidden=false;$('resultTitle').textContent=Object.keys(response.answers).length+' resultado(s) para examinar';$('resultMode').textContent=origin==='simulation'?'SIMULAÇÃO AUTORAL — números inventados; não são uma medição Jev.':'Resposta da API · modelo '+response.model;$('answers').replaceChildren();
 for(const [id,a] of Object.entries(response.answers)){
  const section=node('section',undefined,'answer');section.append(node('h4',id+' · '+a.type),node('p',p.questions[id].instructions));
  if(a.type==='noul'){section.append(node('p',(a.noul*100).toFixed(1)+'% de probabilidade de sim','value'));bars(section,{sim:a.noul,não:1-a.noul});section.append(node('p','Noul não contém um campo confidence separado.','hint'))}
  else{section.append(node('p',a.type==='choice'?a.choice:a.score.toFixed(2)+' / '+(p.questions[id].criteria.length-1),'value'));bars(section,a.probabilities,a.legend);section.append(node('p','Confidence: '+a.confidence.toFixed(2)+' · diferente da probabilidade da alternativa.','hint'))}
  $('answers').append(section);
 }
 $('explanation').textContent=origin==='simulation'?current.explanation:'As probabilidades não explicam o raciocínio. Examine evidências e critérios.';$('next').textContent=current.next;$('threshold').previousElementSibling.innerHTML='Limiar didático de certeza: <output id="thresholdValue"></output>';showPolicy();setStatus(origin==='simulation'?'Exemplo didático carregado.':'Resposta recebida. Nenhuma ação externa executada.');
}
$('threshold').oninput=showPolicy;
$('simulate').onclick=()=>{try{const p=readPayload();if(current.fixture&&same(p,current.request))render(clone(current.fixture),'simulation',p)}catch(e){setStatus(e.message)}};
$('exportResult').onclick=()=>{if(last)download(current.id+'-result.json',{request:lastRequest,response:last,origin:lastOrigin,exported_at:new Date().toISOString(),policy:{threshold:Number($('threshold').value),note:'Política didática, sem ação externa.'}})};
$('live').onclick=async()=>{
 const button=$('live');let sent,caseId;try{sent=JSON.stringify(readPayload());caseId=current.id}catch(e){setStatus(e.message);return}
 button.disabled=true;setStatus('Consultando o provedor…');
 try{const res=await fetch('/api/evaluate',{method:'POST',headers:{'Content-Type':'application/json','X-Jev-Lab':'1'},body:sent,signal:AbortSignal.timeout(10000)});const data=await res.json();if(!res.ok)throw Error(data.error||'Falha na consulta.');let stillCurrent=false;try{stillCurrent=current.id===caseId&&JSON.stringify(readPayload())===sent}catch{}if(stillCurrent)render(data,'live',JSON.parse(sent));else setStatus('Consulta concluída para o contexto anterior. Refaça para o texto atual.')}
 catch(e){setStatus(e.name==='TimeoutError'?'Tempo esgotado. Revise a conexão local.':e.message)}finally{try{readPayload();button.disabled=false}catch{button.disabled=true}}
};
function cost(){const n=Number($('calls').value),t=Number($('tokens').value),p=Number($('price').value);if(![n,t,p].every(x=>Number.isFinite(x)&&x>=0)||!Number.isInteger(n)||!Number.isInteger(t)){$('costTotal').textContent='Revise os valores';$('fullCost').textContent='Revise os valores';return}const base=n*t*p/1e6;$('costTotal').textContent=money(base);const ids=['fallback','llmCost','reviewRate','reviewMinutes','hourCost','overhead'],v=Object.fromEntries(ids.map(k=>[k,Number($(k).value)]));if(!Object.values(v).every(x=>Number.isFinite(x)&&x>=0)||v.fallback>100||v.reviewRate>100){$('fullCost').textContent='Revise percentuais e custos adicionais.';return}const llm=n*v.fallback/100*v.llmCost,human=n*v.reviewRate/100*v.reviewMinutes/60*v.hourCost,total=base+llm+human+v.overhead;$('fullCost').textContent='Jev '+money(base)+' + LLM '+money(llm)+' + revisão '+money(human)+' + infraestrutura '+money(v.overhead)+' = '+money(total)+'.'}
for(const id of ['calls','tokens','price','fallback','llmCost','reviewRate','reviewMinutes','hourCost','overhead'])$(id).oninput=cost;cost();
$('importReport').onchange=async event=>{
 $('reportSummary').hidden=true;
 try{const file=event.target.files[0];if(!file)return;if(file.size>10000000)throw Error('Relatório maior que 10 MB.');const r=JSON.parse(await file.text()),m=r.metrics;if(r.schema_version!==1||!m||!Array.isArray(r.rows)||typeof r.provider!=='string'||!Number.isInteger(m.count)||m.count<1||!Array.isArray(r.labels)||!r.labels.length)throw Error('Use report.json criado por experiment.');for(const k of ['accuracy','coverage'])if(!finite(m[k]))throw Error('Métrica inválida.');
 const box=$('reportSummary');box.replaceChildren();box.append(node('p',r.provider+' · '+m.count+' eventos · '+m.observations+' observações'),node('p','Origem: '+[...new Set(r.rows.map(row=>row.source))].join(', '),'notice'));
 const rows=[['Acurácia',(m.accuracy*100).toFixed(1)+'%'],['Macro-F1',m.macro_f1],['Cobertura',(m.coverage*100).toFixed(1)+'%'],['Precisão das sugestões',m.accepted_precision==null?'Sem sugestões':(m.accepted_precision*100).toFixed(1)+'%'],['Falhas',m.errors],['Brier / ECE',m.brier==null?'Sem probabilidades':m.brier.toFixed(4)+' / '+m.ece.toFixed(4)],['Custo conhecido',money(m.known_cost_usd)],['Observações com custo desconhecido',m.unknown_cost_observations],['p95 declarado (ms)',m.latency_p95_ms==null?'Não informado':m.latency_p95_ms.toFixed(1)]];
 const table=node('table');const caption=node('caption','Métricas da primeira repetição; tempo e custo incluem todas.');table.append(caption);for(const [label,value] of rows){const tr=node('tr'),th=node('th',label);th.scope='row';tr.append(th,node('td',String(value)));table.append(tr)}box.append(table);
 const incorrect=r.rows.filter(row=>row.repetition===0&&(!row.correct||row.error));box.append(node('h3','Erros para investigar ('+incorrect.length+')'));const list=node('ul');for(const row of incorrect.slice(0,100))list.append(node('li',row.id+': esperado '+row.expected+'; recebido '+(row.predicted??'nenhum')+(row.error?' · '+row.error:'')));box.append(list,node('p','Replay e simulação não comprovam desempenho real. Probabilidades e custos dependem do arquivo importado.'));box.hidden=false;$('reportStatus').textContent='Relatório carregado localmente.';
 }catch(e){$('reportStatus').textContent='Importação recusada: '+e.message}finally{event.target.value=''}
};
fetch('cases.json').then(r=>{if(!r.ok)throw Error('Não foi possível carregar os casos.');return r.json()}).then(data=>{cases=data;select(cases.find(c=>c.id===location.hash.slice(1))||cases[1]);drawCases()}).catch(e=>{$('caseTitle').textContent='Exemplos indisponíveis';setStatus(e.message+' Recarregue a página.')});
if(['127.0.0.1','localhost'].includes(location.hostname))fetch('/api/status').then(r=>r.json()).then(s=>{if(s.local){liveAvailable=s.configured;$('mode').textContent=s.configured?'Servidor local conectado · '+(s.provider==='openrouter'?'OpenRouter':'TypeSafe')+' · consultar envia o contexto ao provedor.':'Servidor local conectado · chave não configurada. Exemplos disponíveis.';$('live').hidden=!liveAvailable}}).catch(()=>{});
