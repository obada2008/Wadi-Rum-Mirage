/* Wadi Rum Mirage: local, passive URL structure inspector. Never fetches or navigates input. */
(()=>{'use strict';
const L=document.documentElement.lang==='en'?'en':'ar';
const t=(ar,en)=>L==='ar'?ar:en;
const suspiciousTlds=new Set(['zip','mov','xyz','top','click','icu','work']);
const shorteners=new Set(['bit.ly','tinyurl.com','t.co','is.gd','cutt.ly','rb.gy','tiny.cc']);
const knownBrands=['google','microsoft','paypal','apple','facebook','instagram','whatsapp','amazon'];
function inspect(input){
 const raw=input.trim();if(!raw||raw.length>2048)throw Error(t('أدخل رابطًا بطول أقل من 2049 حرفًا.','Enter a URL under 2049 characters.'));
 if(/[\u0000-\u001f\u007f]/.test(raw)||/\s/.test(raw))throw Error(t('الرابط يحتوي فراغات أو محارف غير مقبولة.','The URL contains whitespace or invalid control characters.'));
 const explicit=/^[a-z][a-z0-9+.-]*:/i.test(raw),value=explicit?raw:'https://'+raw;
 let u;try{u=new URL(value)}catch{throw Error(t('تعذّر تفسير الرابط.','Unable to parse the URL.'))}
 if(!['http:','https:'].includes(u.protocol))throw Error(t('يسمح فقط بروابط HTTP أو HTTPS.','Only HTTP and HTTPS URLs are supported.'));
 const hostname=u.hostname.toLowerCase(),host=hostname.replace(/\.$/,'');
 if(!host||!host.includes('.')&&!/^\[.*\]$/.test(host)&&host!=='localhost')throw Error(t('أدخل نطاقًا صالحًا.','Enter a valid hostname.'));
 const out=[];const add=(id,score,ar,en,evidence)=>out.push({id,score,title:t(ar,en),evidence});
 if(u.protocol==='http:')add('HTTP',16,'اتصال HTTP غير مشفّر','Unencrypted HTTP connection','http://');
 if(u.username||u.password||/^[^/]*@/.test(value.replace(/^https?:\/\//i,'')))add('USERINFO',26,'بيانات قبل @ قد تخفي الوجهة الحقيقية','User-info before @ may disguise the real destination','@');
 if(/^\d{1,3}(\.\d{1,3}){3}$/.test(host)||/^\[.*\]$/.test(host))add('IP',21,'الرابط يستخدم عنوان IP بدل اسم نطاق','IP address instead of a hostname',host);
 if(host.includes('xn--'))add('PUNYCODE',19,'النطاق يتضمن Punycode ويحتاج تدقيقًا بصريًا','Punycode hostname needs visual scrutiny',host);
 if(shorteners.has(host.replace(/^www\./,'')))add('SHORTENER',18,'رابط مختصر يخفي الوجهة النهائية','Short link conceals the destination',host);
 if(host.split('.').length>=5)add('SUBDOMAINS',10,'عدد كبير من النطاقات الفرعية','Unusually many subdomains',host);
 if(suspiciousTlds.has(host.split('.').pop()))add('TLD',9,'امتداد نطاق يحتاج تحققًا إضافيًا','Domain extension warrants additional verification','.'+host.split('.').pop());
 if(u.port&&!['80','443'].includes(u.port))add('PORT',10,'منفذ غير اعتيادي','Nonstandard port',u.port);
 if(raw.length>130)add('LENGTH',7,'رابط طويل يصعب مراجعته','Long URL is hard to review',String(raw.length));
 const path=decodeURIComponentSafe(u.pathname),tail=path.split('/').pop().toLowerCase();
 if(/\.(exe|scr|msi|apk|bat|cmd|ps1|vbs|jar|dmg|hta)$/i.test(tail))add('DOWNLOAD',27,'امتداد ملف قابل للتنفيذ','Potential executable download',tail);
 for(const [name,val] of u.searchParams){if(/^(url|redirect|redirect_uri|next|goto|dest|destination|target|returnurl)$/i.test(name)&&/^https?:\/\//i.test(val)){add('REDIRECT',17,'معامل قد يعيد التوجيه إلى موقع آخر','Parameter may redirect to another site',name);break}}
 const normalized=host.replace(/[013457]/g,ch=>({'0':'o','1':'l','3':'e','4':'a','5':'s','7':'t'})[ch]);
 if(knownBrands.some(b=>normalized.includes(b)&&host.split('.').slice(-2).join('.')!==b+'.com'&&host.split('.').slice(-2).join('.')!==b+'.org'))add('BRAND',22,'اسم علامة تجارية ضمن نطاق غير مؤكد الملكية','Brand name appears within an unverified domain',host);
 const total=Math.min(100,out.reduce((s,x)=>s+x.score,0)),level=total>=45?'high':total>=20?'moderate':'limited';
 return {host,scheme:u.protocol.replace(':',''),path:path||'/',total,level,indicators:out,assumed:!explicit};
}
function decodeURIComponentSafe(s){try{return decodeURIComponent(s)}catch{return s}}
const $=id=>document.getElementById(id);
function run(){let report=$('url-report');report.replaceChildren();let r;try{r=inspect($('url-input').value);document.dispatchEvent(new CustomEvent('wrm:url-analyzed',{detail:{input:$('url-input').value,report:r}}))}catch(e){let p=document.createElement('p');p.className='error';p.textContent=e.message;report.append(p);return}
 const heading=document.createElement('div');heading.className='url-verdict';let title=document.createElement('h3');title.textContent=r.level==='high'?t('مؤشرات مرتفعة تستدعي الحذر','Elevated structural indicators'):r.level==='moderate'?t('مؤشرات تستدعي مراجعة','Indicators warrant review'):t('مؤشرات محدودة لا تثبت الأمان','Limited indicators do not prove safety');let value=document.createElement('strong');value.textContent=r.total+'/100';heading.append(title,value);report.append(heading);
 const detail=document.createElement('p');detail.className='url-muted';detail.textContent=t('المضيف: ','Hostname: ')+r.host+' · '+r.scheme.toUpperCase();report.append(detail);
 if(!r.indicators.length){let p=document.createElement('p');p.textContent=t('لم تُرصد أنماط مطابقة للقواعد الحالية. هذا لا يعني أن الرابط آمن.','No matching indicators were found. This does not mean the link is safe.');report.append(p)}
 r.indicators.forEach(i=>{let div=document.createElement('div');div.className='url-signal';let b=document.createElement('b');b.textContent=i.id+' · '+i.title;let p=document.createElement('span');p.textContent=i.evidence;div.append(b,p);report.append(div)});
 let note=document.createElement('p');note.className='url-muted';note.textContent=t('تحليل محلي لهيكل الرابط فقط. لا نفتح الوجهة أو نفحص السمعة أو نثبت هوية المؤسسة.','Passive local URL structure review only. No destination visited, no reputation lookup, no identity verification.');report.append(note);
}
window.addEventListener('DOMContentLoaded',()=>{$('url-check')?.addEventListener('click',run);$('url-input')?.addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault();run()}});document.querySelectorAll('[data-url-example]').forEach(btn=>btn.addEventListener('click',()=>{$('url-input').value=btn.dataset.urlExample;run()}))});
window.WRMInspectURL=inspect;
})();