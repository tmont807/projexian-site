(function(){
  if(window.top!==window.self&&!document.querySelector('meta[name="pjx-preview"]')){try{window.top.location=window.location.href;}catch(e){document.documentElement.style.display='none';}}
  var hdr=document.getElementById('hdr'),btn=document.getElementById('menuBtn');
  function onScroll(){hdr.classList.toggle('scrolled',window.scrollY>8);}
  addEventListener('scroll',onScroll,{passive:true});onScroll();
  btn.addEventListener('click',function(){var o=document.body.classList.toggle('open');btn.setAttribute('aria-expanded',o);btn.setAttribute('aria-label',o?'Close menu':'Open menu');});
  document.querySelectorAll('#nav a').forEach(function(a){a.addEventListener('click',function(){document.body.classList.remove('open');});});
  addEventListener('keydown',function(e){if(e.key==='Escape'){document.body.classList.remove('open');btn.setAttribute('aria-expanded',false);}});
  // reveal
  var els=document.querySelectorAll('.rv');
  if('IntersectionObserver' in window){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}});},{threshold:.12,rootMargin:'0px 0px -40px 0px'});els.forEach(function(e){io.observe(e);});}
  else els.forEach(function(e){e.classList.add('in');});
  // forms: send visitors back to this site's thank-you page, wherever it is hosted
  document.querySelectorAll('input[data-next]').forEach(function(i){i.value=new URL(i.getAttribute('data-next'),location.href).href;});
  // contact: preselect from ?topic= and &industry=
  var q=new URLSearchParams(location.search),svc=document.getElementById('c-svc'),ind=document.getElementById('c-ind');
  if(svc&&q.get('topic')){[].forEach.call(svc.options,function(o){if(o.dataset.topic===q.get('topic'))svc.value=o.value;});}
  if(ind&&q.get('industry')){[].forEach.call(ind.options,function(o){if(o.dataset.slug===q.get('industry'))ind.value=o.value;});}
  var opp=q.get('opp'),desc=document.getElementById('c-desc')||document.getElementById('p-notes');if(opp&&desc&&!desc.value)desc.value=(desc.id==='p-notes'?'Interested in performing: ':'I would like to discuss this opportunity: ')+opp.slice(0,300);
  var preview=!!document.querySelector('meta[name="pjx-preview"]');
  document.querySelectorAll('form.f').forEach(function(f){f.addEventListener('submit',function(ev){
    if(preview){ev.preventDefault();var n=f.querySelector('.pv-note');if(!n){n=document.createElement('p');n.className='privacy pv-note';n.style.color='var(--navy)';f.appendChild(n);}n.textContent='Preview only: the form works and validates, but nothing is sent until the site is live. On the real site this goes straight to tyler@projexian.com.';return;}var b=f.querySelector('button[type=submit]');if(b){b.disabled=true;b.textContent='Sending…';}});});
})();
