/* braket.js — toggle lingua IT/EN condiviso per i mockup. */
(function(){
  var root=document.documentElement;
  function set(l){
    l=(l==='en')?'en':'it';
    root.setAttribute('data-lang',l); root.setAttribute('lang',l);
    try{localStorage.setItem('site-lang',l);}catch(e){}
    var b=document.querySelectorAll('.langbtn');
    for(var i=0;i<b.length;i++){ b[i].setAttribute('aria-pressed', b[i].getAttribute('data-l')===l?'true':'false'); }
  }
  var saved=null; try{saved=localStorage.getItem('site-lang');}catch(e){}
  if(!saved){ var n=(navigator.language||'it').toLowerCase(); saved=n.indexOf('it')===0?'it':'en'; }
  set(saved);
  document.addEventListener('click',function(e){
    var b=e.target.closest && e.target.closest('.langbtn');
    if(b){ set(b.getAttribute('data-l')); }
  });
})();
