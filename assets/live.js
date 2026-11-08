/* Projexian — live opportunity data, ticker, charts, maps and small animations */
(function(){
var FEED_URL='data/feed.json';
var ATLAS='assets/vendor/states-10m.json';
var reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
var $=function(id){return document.getElementById(id);};
var esc=function(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});};
var NAMES={AL:'Alabama',AK:'Alaska',AZ:'Arizona',AR:'Arkansas',CA:'California',CO:'Colorado',CT:'Connecticut',DE:'Delaware',DC:'Washington, DC',FL:'Florida',GA:'Georgia',HI:'Hawaii',ID:'Idaho',IL:'Illinois',IN:'Indiana',IA:'Iowa',KS:'Kansas',KY:'Kentucky',LA:'Louisiana',ME:'Maine',MD:'Maryland',MA:'Massachusetts',MI:'Michigan',MN:'Minnesota',MS:'Mississippi',MO:'Missouri',MT:'Montana',NE:'Nebraska',NV:'Nevada',NH:'New Hampshire',NJ:'New Jersey',NM:'New Mexico',NY:'New York',NC:'North Carolina',ND:'North Dakota',OH:'Ohio',OK:'Oklahoma',OR:'Oregon',PA:'Pennsylvania',RI:'Rhode Island',SC:'South Carolina',SD:'South Dakota',TN:'Tennessee',TX:'Texas',UT:'Utah',VT:'Vermont',VA:'Virginia',WA:'Washington',WV:'West Virginia',WI:'Wisconsin',WY:'Wyoming',PR:'Puerto Rico',GU:'Guam',VI:'U.S. Virgin Islands',MP:'Northern Mariana Islands',AS:'American Samoa'};
var FIPS={'01':'AL','02':'AK','04':'AZ','05':'AR','06':'CA','08':'CO','09':'CT','10':'DE','11':'DC','12':'FL','13':'GA','15':'HI','16':'ID','17':'IL','18':'IN','19':'IA','20':'KS','21':'KY','22':'LA','23':'ME','24':'MD','25':'MA','26':'MI','27':'MN','28':'MS','29':'MO','30':'MT','31':'NE','32':'NV','33':'NH','34':'NJ','35':'NM','36':'NY','37':'NC','38':'ND','39':'OH','40':'OK','41':'OR','42':'PA','44':'RI','45':'SC','46':'SD','47':'TN','48':'TX','49':'UT','50':'VT','51':'VA','53':'WA','54':'WV','55':'WI','56':'WY','60':'AS','66':'GU','69':'MP','72':'PR','78':'VI'};
var CATS={"541611": "Management consulting", "115310": "Forestry support", "236118": "Residential remodeling", "236220": "Commercial building construction", "237110": "Water and sewer line construction", "237310": "Highway, street and bridge", "237990": "Heavy and civil construction", "238140": "Masonry", "238160": "Roofing", "238210": "Electrical", "238220": "Plumbing, heating and air conditioning", "238320": "Painting and wall covering", "238330": "Flooring", "238910": "Site preparation", "238990": "Specialty trades", "332410": "Boilers and heat exchangers", "332722": "Fasteners", "334513": "Industrial instruments", "335910": "Batteries", "337126": "Furniture manufacturing", "339940": "Office supplies manufacturing", "423210": "Furniture supply", "423420": "Office equipment supply", "423430": "Computer equipment supply", "423450": "Medical supplies", "423610": "Electrical supplies", "484110": "Local freight", "484121": "Long-distance freight", "484210": "Moving services", "484220": "Specialized freight", "484230": "Specialized freight, long-distance", "488510": "Freight arrangement", "492110": "Couriers and delivery", "493110": "Warehousing and storage", "524298": "Insurance services", "532120": "Truck and trailer rental", "532283": "Home health equipment rental", "532412": "Construction equipment rental", "532490": "Equipment rental", "541330": "Engineering services", "541350": "Building inspection", "541512": "IT systems design", "541519": "IT services", "541614": "Logistics consulting", "541618": "Management consulting", "541620": "Environmental consulting", "541910": "Market research", "541990": "Professional services", "561110": "Office administration", "561210": "Facilities support", "561320": "Temporary staffing", "561410": "Document preparation", "561612": "Security guards", "561621": "Security systems", "561710": "Pest control", "561720": "Janitorial", "561730": "Landscaping and grounds", "561740": "Carpet cleaning", "561790": "Building services", "561920": "Events and trade shows", "561990": "Support services", "562111": "Solid waste", "562112": "Hazardous waste collection", "562119": "Other waste collection", "562910": "Remediation", "562920": "Recycling", "562991": "Portable restrooms and septic", "562998": "Waste management", "611430": "Training", "722310": "Food service", "811192": "Vehicle washing", "811210": "Electronic equipment repair", "811310": "Machinery repair", "812332": "Industrial laundry", "812930": "Parking management"};
var IND={"561720": "Janitorial Services", "561740": "Janitorial Services", "561790": "Janitorial Services", "812332": "Janitorial Services", "561210": "Facility Maintenance", "561730": "Facility Maintenance", "561710": "Facility Maintenance", "561990": "Facility Maintenance", "811310": "Facility Maintenance", "811210": "Facility Maintenance", "115310": "Facility Maintenance", "236118": "Construction and Trades", "236220": "Construction and Trades", "237110": "Construction and Trades", "237310": "Construction and Trades", "237990": "Construction and Trades", "238140": "Construction and Trades", "238160": "Construction and Trades", "238210": "Construction and Trades", "238220": "Construction and Trades", "238320": "Construction and Trades", "238330": "Construction and Trades", "238910": "Construction and Trades", "238990": "Construction and Trades", "562111": "Waste and Environmental", "562112": "Waste and Environmental", "562119": "Waste and Environmental", "562910": "Waste and Environmental", "562920": "Waste and Environmental", "562991": "Waste and Environmental", "562998": "Waste and Environmental", "541620": "Waste and Environmental", "484110": "Transportation and Logistics", "484121": "Transportation and Logistics", "484210": "Transportation and Logistics", "484220": "Transportation and Logistics", "484230": "Transportation and Logistics", "488510": "Transportation and Logistics", "492110": "Transportation and Logistics", "493110": "Transportation and Logistics", "541614": "Transportation and Logistics", "532120": "Equipment Rental", "532283": "Equipment Rental", "532412": "Equipment Rental", "532490": "Equipment Rental", "561612": "Security", "561621": "Security", "332410": "Products and Supply", "332722": "Products and Supply", "334513": "Products and Supply", "335910": "Products and Supply", "337126": "Products and Supply", "339940": "Products and Supply", "423210": "Products and Supply", "423420": "Products and Supply", "423430": "Products and Supply", "423450": "Products and Supply", "423610": "Products and Supply", "541330": "Professional and Technical", "541350": "Professional and Technical", "541512": "Professional and Technical", "541519": "Professional and Technical", "541611": "Professional and Technical", "541618": "Professional and Technical", "541910": "Professional and Technical", "541990": "Professional and Technical", "561110": "Professional and Technical", "561320": "Professional and Technical", "561410": "Professional and Technical", "561920": "Professional and Technical", "611430": "Professional and Technical", "524298": "Professional and Technical", "722310": "Food, Parking and Vehicle Services", "812930": "Food, Parking and Vehicle Services", "811192": "Food, Parking and Vehicle Services"};
function hash(s){var h=2166136261;s=String(s);for(var i=0;i<s.length;i++)h=Math.imul(h^s.charCodeAt(i),16777619);return (h>>>0)/4294967296;}
function fmtDue(d){var y=d.slice(0,4)!==String(new Date().getFullYear());return new Date(d+'T12:00:00').toLocaleDateString('en-US',{month:'short',day:'numeric',year:y?'numeric':undefined});}
function short(s,n){return s.length>n?s.slice(0,n-1).trim()+'…':s;}
function onView(el,fn,th){if(!el)return;if(!('IntersectionObserver' in window)){fn();return;}var io=new IntersectionObserver(function(es){if(es[0].isIntersecting){io.disconnect();fn();}},{threshold:th||.3});io.observe(el);}
function countUp(el,n){if(!el)return;if(reduce){el.textContent=n;return;}var t0=performance.now();(function tick(t){var k=Math.min(1,(t-t0)/1200);el.textContent=Math.round(n*(1-Math.pow(1-k,3)));if(k<1)requestAnimationFrame(tick);})(t0);}

var feedP=null;
function feed(){if(!feedP)feedP=fetch(FEED_URL,{cache:'no-cache'}).then(function(r){if(!r.ok)throw 0;return r.json();}).then(function(f){
  var today=new Date().toISOString().slice(0,10);
  f.items=f.items.filter(function(i){return i.due>=today;});
  f.items.forEach(function(it,i){if(!it.p){it.lon+=(hash(it.t+i)-.5)*1.4;it.lat+=(hash(i+'y'+it.t)-.5)*.9;}});
  return f;});return feedP;}
var atlasP=null;
function atlas(){if(!atlasP)atlasP=fetch(ATLAS).then(function(r){return r.json();});return atlasP;}
function updLine(f){var d=new Date(f.updated);return 'Source: SAM.gov public data · updated '+d.toLocaleString('en-US',{month:'short',day:'numeric',hour:'numeric',minute:'2-digit'});}

/* ---------- ticker ---------- */
function ticker(f){var el=$('tickerTrack');if(!el)return;
  var items=f.items.slice().sort(function(a,b){return a.due<b.due?-1:1;}).slice(0,40);
  var h=items.map(function(i){return '<span><em>'+esc(short(i.t,60))+'</em> '+esc(i.c?i.c+', '+i.s:(NAMES[i.s]||i.s))+' · due '+fmtDue(i.due)+'</span>';}).join('');
  el.innerHTML=h+h;el.style.setProperty('--dur',Math.max(90,items.length*7)+'s');el.parentElement.parentElement.hidden=false;}

/* ---------- bar charts ---------- */
function bars(el,rows,brass){if(!el||!rows.length)return;var max=rows[0][1];
  el.innerHTML=rows.map(function(r){return '<div class="bar"><span>'+esc(r[0])+'</span><span class="t"><i class="'+(brass?'b':'')+'" style="--w:'+(r[1]/max)+'"></i></span><span class="c">'+r[1]+'</span></div>';}).join('');
  onView(el,function(){el.classList.add('in');});}
function intel(f){var o=$('iOpen');if(!o)return;
  var n=(f.stats&&f.stats.open)||f.items.length;onView(o,function(){countUp(o,n);});
  document.querySelectorAll('.iUpd').forEach(function(u){u.textContent=updLine(f);});
  var by={},cat={};f.items.forEach(function(i){by[i.s]=(by[i.s]||0)+1;cat[i.n]=(cat[i.n]||0)+1;});
  bars($('iBars'),Object.keys(by).map(function(k){return [NAMES[k]||k,by[k]];}).sort(function(a,b){return b[1]-a[1];}).slice(0,8));
  bars($('iCats'),Object.keys(cat).map(function(k){return [CATS[k]||k,cat[k]];}).sort(function(a,b){return b[1]-a[1];}).slice(0,8),true);}

/* ---------- night to day (home) ---------- */
function nightMap(f,us){var box=$('nightmap');if(!box||!window.d3)return;
  var W=960,H=560,svg=d3.select(box).append('svg').attr('viewBox','0 0 '+W+' '+H).attr('role','img').attr('aria-label','Map of the United States as morning reaches each time zone');
  var nat=topojson.feature(us,us.objects.nation),st=topojson.mesh(us,us.objects.states,function(a,b){return a!==b;});
  var pr=d3.geoAlbersUsa().fitExtent([[10,10],[W-10,H-10]],nat),path=d3.geoPath(pr);
  svg.append('path').datum(nat).attr('d',path).attr('fill','#E7E4DC');
  svg.append('path').datum(st).attr('d',path).attr('fill','none').attr('stroke','#F3F0E9').attr('stroke-width',1);
  var pts=f.items.map(function(i){var p=pr([i.lon,i.lat]);return p?{x:p[0],y:p[1]}:null;}).filter(Boolean);
  var dots=svg.append('g').selectAll('circle').data(pts).join('circle').attr('cx',function(d){return d.x;}).attr('cy',function(d){return d.y;}).attr('r',3.4).attr('fill','#142638').attr('opacity',0);
  var defs=svg.append('defs'),g=defs.append('linearGradient').attr('id','dusk').attr('x1',0).attr('x2',1);
  g.append('stop').attr('offset','0').attr('stop-color','#142638').attr('stop-opacity',.86);
  g.append('stop').attr('offset','.82').attr('stop-color','#142638').attr('stop-opacity',.86);
  g.append('stop').attr('offset','1').attr('stop-color','#142638').attr('stop-opacity',0);
  var clip=defs.append('clipPath').attr('id','natclip');clip.append('path').datum(nat).attr('d',path);
  var night=svg.append('rect').attr('x',0).attr('y',0).attr('height',H).attr('width',W+120).attr('fill','url(#dusk)').attr('clip-path','url(#natclip)');
  var line=svg.append('line').attr('y1',0).attr('y2',H).attr('stroke','#A58A5B').attr('stroke-width',1.2).attr('stroke-dasharray','3 5');
  var clock=$('nightClock');
  function frame(k){var x=(W+120)*(1-k);night.attr('width',x);line.attr('x1',x).attr('x2',x).attr('opacity',k<1?1:0);
    dots.attr('opacity',function(d){return d.x>x-110?1:0;}).attr('r',function(d){var dd=d.x-(x-110);return dd>0&&dd<30?5.5:3.4;});
    if(clock){var m=300+Math.round(k*240);clock.textContent=(Math.floor(m/60))+':'+String(m%60).padStart(2,'0')+' AM ET';}}
  frame(0);
  onView(box,function(){if(reduce){frame(1);return;}var t0=performance.now();(function tick(t){var k=Math.min(1,(t-t0)/5200);frame(d3.easeCubicInOut(k));if(k<1)requestAnimationFrame(tick);})(t0);},.4);}

/* ---------- solicitation -> bid (services) ---------- */
function docAnim(){var box=$('docanim');if(!box)return;
  onView(box,function(){box.classList.add('play');},.45);}

/* ---------- opportunities page ---------- */
function opps(f,us){var root=$('opp');if(!root)return;
  var all=f.items.map(function(i,k){i.ix=k;i.ind=IND[i.n]||'Other';i.cat=CATS[i.n]||i.n;i.type=i.k==='ss'?'Sources sought / RFI':'Solicitation';return i;});
  var state={st:'',ind:'',ag:'',cat:'',type:'',q:'',lens:'contracts',sel:null,lim:20};
  // filters
  function opts(id,vals,label){var el=$(id);el.innerHTML='<option value="">'+label+'</option>'+vals.map(function(v){return '<option value="'+esc(v[0])+'">'+esc(v[1])+'</option>';}).join('');}
  function uniq(fn){var m={};all.forEach(function(i){var v=fn(i);if(v)m[v]=(m[v]||0)+1;});return Object.keys(m).sort();}
  opts('fInd',uniq(function(i){return i.ind;}).map(function(v){return [v,v];}),'All industries');
  opts('fSt',uniq(function(i){return i.s;}).sort(function(a,b){return (NAMES[a]||a)<(NAMES[b]||b)?-1:1;}).map(function(v){return [v,NAMES[v]||v];}),'All locations');
  opts('fAg',uniq(function(i){return i.a;}).map(function(v){return [v,v];}),'All agencies');
  opts('fCat',uniq(function(i){return i.cat;}).map(function(v){return [v,v];}),'All categories');
  opts('fType',[['Solicitation','Solicitation'],['Sources sought / RFI','Sources sought / RFI']],'All types');
  [['fInd','ind'],['fSt','st'],['fAg','ag'],['fCat','cat'],['fType','type']].forEach(function(p){$(p[0]).addEventListener('change',function(e){state[p[1]]=e.target.value;state.sel=null;render();});});
  $('fQ').addEventListener('input',function(e){state.q=e.target.value.toLowerCase();state.sel=null;render();});
  $('fReset').addEventListener('click',function(){['fInd','fSt','fAg','fCat','fType'].forEach(function(i){$(i).value='';});$('fQ').value='';state.st=state.ind=state.ag=state.cat=state.type=state.q='';state.sel=null;render();});
  function filtered(ignoreState){return all.filter(function(i){return (ignoreState||!state.st||i.s===state.st)&&(!state.ind||i.ind===state.ind)&&(!state.ag||i.a===state.ag)&&(!state.cat||i.cat===state.cat)&&(!state.type||i.type===state.type)&&(!state.q||(i.t+' '+i.a+' '+i.c+' '+(NAMES[i.s]||'')).toLowerCase().indexOf(state.q)>=0);});}
  // map
  var W=975,H=610,svg=d3.select('#oppmap').attr('viewBox','0 0 '+W+' '+H);
  var feats=topojson.feature(us,us.objects.states).features,main=feats.filter(function(d){return +d.id<60;});
  var pr=d3.geoAlbersUsa().fitExtent([[8,8],[W-8,H-8]],{type:'FeatureCollection',features:main}),path=d3.geoPath(pr);
  var gS=svg.append('g'),gD=svg.append('g'),gR=svg.append('g');
  var paths=gS.selectAll('path').data(main).join('path').attr('class','ost').attr('d',path).attr('tabindex',0).attr('role','button')
    .attr('aria-label',function(d){return NAMES[FIPS[d.id]]||d.properties.name;})
    .on('click',function(e,d){pickState(FIPS[d.id]);}).on('keydown',function(e,d){if(e.key==='Enter'||e.key===' '){e.preventDefault();pickState(FIPS[d.id]);}})
    .on('mousemove',function(e,d){tip(e,FIPS[d.id]);}).on('mouseleave',hideTip);
  var TERR=[['72','PR'],['78','VI'],['66','GU'],['69','MP'],['60','AS']],tp={};
  $('terrRow').innerHTML=TERR.map(function(t){return '<button class="tcell" data-s="'+t[1]+'"><svg viewBox="0 0 120 50" data-id="'+t[0]+'"></svg><span class="tn">'+NAMES[t[1]]+'</span><span class="tc" data-c="'+t[1]+'"></span></button>';}).join('');
  TERR.forEach(function(t){var fe=feats.filter(function(d){return d.id===t[0];})[0];if(!fe)return;var p=d3.geoMercator().fitExtent([[6,5],[114,45]],fe);tp[t[1]]=p;
    var s=d3.select('#terrRow svg[data-id="'+t[0]+'"]');s.append('path').datum(fe).attr('class','ost').attr('d',d3.geoPath(p));s.append('g').attr('class','tdots');});
  root.querySelectorAll('.tcell').forEach(function(b){b.addEventListener('click',function(){pickState(b.dataset.s);});b.addEventListener('mousemove',function(e){tip(e,b.dataset.s);});b.addEventListener('mouseleave',hideTip);});
  var tipEl=$('otip');
  function tip(e,s){var r=root.querySelector('.omap').getBoundingClientRect();var n=filtered(true).filter(function(i){return i.s===s;}).length;
    tipEl.innerHTML='<b>'+esc(NAMES[s]||s)+'</b> · '+n+' open';tipEl.style.left=(e.clientX-r.left)+'px';tipEl.style.top=(e.clientY-r.top)+'px';tipEl.style.opacity=1;}
  function hideTip(){tipEl.style.opacity=0;}
  function pickState(s){state.st=state.st===s?'':s;$('fSt').value=state.st;state.sel=null;render();
    if(window.innerWidth<820)$('oList').scrollIntoView({behavior:'smooth',block:'start'});}
  // lenses
  root.querySelectorAll('[data-lens]').forEach(function(b){b.addEventListener('click',function(){state.lens=b.dataset.lens;root.querySelectorAll('[data-lens]').forEach(function(x){x.setAttribute('aria-selected',x===b);});render();});});
  var LENS={contracts:{note:'Open federal contracts in our tracked categories, live from SAM.gov.',cta:''},
    partners:{note:'Every open contract needs a capable local crew. Darker states have more work waiting for a partner.',cta:'<a class="link" href="contact.html?topic=partnerships">Join the partner network <span class="ar">→</span></a>'},
    leads:{note:'Demonstration: how lead generation clients see activity in their target market. Live prospect data is delivered per engagement.',cta:'<a class="link" href="lead-generation.html#inquiry">Request lead generation information <span class="ar">→</span></a>'}};
  var demo=null;
  function demoPts(){if(demo)return demo;demo=[];var metros=[[-74,40.7,9],[-118.2,34,8],[-87.6,41.9,8],[-95.4,29.8,6],[-96.8,32.8,6],[-84.4,33.7,5],[-80.2,25.8,5],[-77,38.9,6],[-122.3,47.6,4],[-104.9,39.7,4],[-112,33.4,4],[-71.1,42.4,4],[-93.3,45,3],[-90.2,38.6,3],[-86.8,36.2,3],[-80.8,35.2,3],[-97.7,30.3,3],[-122.4,37.8,5],[-83,42.3,3],[-81.4,28.5,3]];
    metros.forEach(function(m,j){for(var i=0;i<m[2]*6;i++){var p=pr([m[0]+(hash(j+'a'+i)-.5)*2.2,m[1]+(hash(j+'b'+i)-.5)*1.4]);if(p)demo.push(p);}});return demo;}
  function render(){var list=filtered(),forMap=filtered(true),by={};forMap.forEach(function(i){by[i.s]=(by[i.s]||0)+1;});
    var max=Math.max(1,d3.max(Object.values(by))||1),col=function(n){return n?d3.interpolateRgb('#C9C3B4',state.lens==='partners'?'#A58A5B':'#142638')(Math.sqrt(n/max)):'#E7E4DC';};
    if(state.lens==='leads')col=function(){return '#E7E4DC';};
    paths.style('fill',function(d){return col(by[FIPS[d.id]]||0);}).classed('sel',function(d){return FIPS[d.id]===state.st;});
    TERR.forEach(function(t){var s=d3.select('#terrRow svg[data-id]'+'[data-id="'+t[0]+'"]');s.selectAll('.ost').style('fill',col(by[t[1]]||0));
      var c=root.querySelector('[data-c="'+t[1]+'"]');if(c)c.textContent=(by[t[1]]||0)+' open';
      var b=root.querySelector('.tcell[data-s="'+t[1]+'"]');if(b)b.classList.toggle('sel',state.st===t[1]);
      var p=tp[t[1]];if(p)s.select('.tdots').selectAll('circle').data(state.lens==='leads'?[]:forMap.filter(function(i){return i.s===t[1];})).join('circle').attr('r',3).attr('class','odot').attr('cx',function(d){return p([d.lon,d.lat])[0];}).attr('cy',function(d){return p([d.lon,d.lat])[1];});});
    var dd=state.lens==='leads'?[]:forMap.filter(function(i){return pr([i.lon,i.lat]);});
    gD.selectAll('circle.odot').data(dd,function(d){return d.ix;}).join('circle').attr('class',function(d){return 'odot'+(state.st&&d.s!==state.st?' dim':'');}).attr('r',3.4)
      .attr('cx',function(d){return pr([d.lon,d.lat])[0];}).attr('cy',function(d){return pr([d.lon,d.lat])[1];});
    gD.selectAll('rect.demo').data(state.lens==='leads'?demoPts():[]).join('rect').attr('class','demo').attr('width',3).attr('height',3).attr('x',function(d){return d[0]-1.5;}).attr('y',function(d){return d[1]-1.5;});
    $('lensNote').innerHTML=esc(LENS[state.lens].note)+(LENS[state.lens].cta?'<div style="margin-top:12px">'+LENS[state.lens].cta+'</div>':'');
    // summary + list
    var where=state.st?(NAMES[state.st]||state.st):'all states and territories';
    $('oCount').innerHTML='<b>'+list.length+'</b> open opportunit'+(list.length===1?'y':'ies')+' · '+esc(where);
    $('oClear').hidden=!(state.st||state.ind||state.ag||state.cat||state.type||state.q);
    list.sort(function(a,b){return a.due<b.due?-1:1;});
    $('oList').innerHTML=list.length?list.slice(0,state.lim).map(function(i){var q='contact.html?topic=contracting&opp='+encodeURIComponent(i.t+' ('+(i.c?i.c+', ':'')+i.s+', due '+i.due+')');
      return '<article class="orow'+(state.sel===i.ix?' on':'')+'" data-id="'+i.ix+'" tabindex="0"><div class="o-main"><h3>'+(i.u?'<a href="opp/'+i.u+'.html">'+esc(i.t)+'</a>':esc(i.t))+'</h3><p>'+esc(i.a||'Federal agency')+' · '+esc(i.c?i.c+', '+i.s:(NAMES[i.s]||i.s))+'</p></div>'+
        '<div class="o-meta"><span>'+esc(i.cat)+'</span><span>'+esc(i.type)+'</span></div><div class="o-due"><span class="label">Due</span>'+fmtDue(i.due)+'</div><a class="link o-go" href="'+q+'">Inquire <span class="ar">→</span></a></article>';}).join('')+
      (list.length>state.lim?'<div style="padding:26px 0"><button type="button" class="btn ghost" id="oMore">Show more ('+(list.length-state.lim)+' remaining)</button></div>':''):'<p class="body" style="padding:30px 0">No open opportunities match these filters today. New solicitations post every business day.</p>';
    var more=$('oMore');if(more)more.addEventListener('click',function(){state.lim+=20;render();});
    $('oList').querySelectorAll('.orow').forEach(function(r){var go=function(e){if(e.target.closest('a'))return;focusOpp(+r.dataset.id);};r.addEventListener('click',go);r.addEventListener('keydown',function(e){if(e.key==='Enter')go(e);});});
    radar();}
  function focusOpp(id){state.sel=id;$('oList').querySelectorAll('.orow').forEach(function(r){r.classList.toggle('on',+r.dataset.id===id);});radar(true);
    if(window.innerWidth<820)root.querySelector('.omap').scrollIntoView({behavior:'smooth',block:'center'});}
  function radar(fresh){gR.selectAll('*').remove();var i=all[state.sel];var pan=$('pairing');if(i==null||state.sel==null){pan.hidden=true;return;}
    var p=pr([i.lon,i.lat]);if(!p){var t=tp[i.s];pan.hidden=false;}
    pan.hidden=false;pan.innerHTML='<div class="label">Selected opportunity</div><h4>'+esc(short(i.t,80))+'</h4><p>'+esc(i.c?i.c+', '+(NAMES[i.s]||i.s):(NAMES[i.s]||i.s))+' · due '+fmtDue(i.due)+'</p><ol class="pairs"><li>We review the full solicitation and confirm the requirements.</li><li>We match it with a vetted local partner near the place of performance.</li><li>We price, submit and manage the contract as your single point of contact.</li></ol>';
    if(!p)return;
    gR.append('circle').attr('cx',p[0]).attr('cy',p[1]).attr('r',6).attr('class','rcore');
    if(reduce)return;
    [0,1,2].forEach(function(k){gR.append('circle').attr('cx',p[0]).attr('cy',p[1]).attr('class','rring').style('animation-delay',(k*.7)+'s');});}
  // deep link ?state=XX
  var qs=new URLSearchParams(location.search);if(qs.get('state')&&NAMES[qs.get('state').toUpperCase()]){state.st=qs.get('state').toUpperCase();$('fSt').value=state.st;}
  $('oClear').addEventListener('click',function(){$('fReset').click();});
  $('oUpd').textContent=updLine(f);countUp($('oTotal'),all.length);
  render();root.classList.add('ready');}

/* ---------- boot ---------- */
docAnim();
var needs=$('tickerTrack')||$('iOpen')||$('nightmap')||$('opp');
if(needs){feed().then(function(f){
  ticker(f);intel(f);
  if(($('nightmap')||$('opp'))&&window.d3){atlas().then(function(us){nightMap(f,us);opps(f,us);});}
}).catch(function(){document.querySelectorAll('[data-live]').forEach(function(e){e.hidden=true;});var o=$('opp');if(o)o.classList.add('offline');});}
})();
