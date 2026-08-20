const API="http://127.0.0.1:8000";
let videoId=null;

function extractVideoId(url){
  try{
    const u=new URL(url);
    if(u.hostname==="youtu.be") return u.pathname.slice(1);
    return u.hostname.includes("youtube.com") ? u.searchParams.get("v") : null;
  }catch{return null}
}
async function tab(){
  const tabs=await chrome.tabs.query({active:true,currentWindow:true});
  return tabs[0];
}
function status(x){document.getElementById("status").textContent=x}
function time(sec){
  if(sec==null)return "?";
  sec=Math.floor(sec); return `${Math.floor(sec/60)}:${String(sec%60).padStart(2,"0")}`;
}
async function load(){
  const t=await tab();
  videoId=extractVideoId(t?.url||"");
  document.getElementById("videoTitle").textContent=videoId?(t.title||"YouTube video"):"Open a YouTube video";
  document.getElementById("videoId").textContent=videoId?`Video ID: ${videoId}`:"";
  status(videoId?"Ready":"Not YouTube");
}
async function ask(q){
  if(!videoId){status("Open a YouTube video first");return}
  if(!q?.trim())return;
  const btn=document.getElementById("ask");
  btn.disabled=true; document.getElementById("answer").textContent="Thinking..."; status("Retrieving...");
  try{
    const r=await fetch(`${API}/api/v1/rag/ask`,{
      method:"POST",headers:{"Content-Type":"application/json"},
      body:JSON.stringify({video_id:videoId,question:q.trim()})
    });
    const data=await r.json();
    if(!r.ok)throw new Error(data.detail||`HTTP ${r.status}`);
    document.getElementById("answer").textContent=data.answer;
    const box=document.getElementById("sources"); box.innerHTML="";
    (data.sources||[]).forEach(s=>{
      const d=document.createElement("div"); d.className="source";
      d.textContent=`${time(s.start)} — chunk ${s.chunk_id ?? "?"}`;
      box.appendChild(d);
    });
    status("Completed");
  }catch(e){document.getElementById("answer").textContent=`Error: ${e.message}`;status("Error")}
  finally{btn.disabled=false}
}
document.getElementById("ask").onclick=()=>ask(document.getElementById("question").value);
document.getElementById("question").onkeydown=e=>{if(e.key==="Enter"&&!e.shiftKey){e.preventDefault();ask(e.target.value)}};
document.querySelectorAll(".quick button").forEach(b=>b.onclick=()=>{document.getElementById("question").value=b.dataset.q;ask(b.dataset.q)});
load();
