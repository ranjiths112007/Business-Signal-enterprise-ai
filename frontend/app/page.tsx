"use client";

import { DragEvent, useEffect, useRef, useState } from "react";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
const BRAND = "/Business%20Signal%20Neon%20Analytics%20Branding.png";
const EMBLEM = "/Neon%20Business%20Signal%20Emblem.png";

type Customer = { customer_id:number; customer:string; revenue:number; industry:string };
type Summary = { customers?:number; total_revenue?:number; open_tickets?:number };

function Icon({name}:{name:string}) {
  const p:Record<string,React.ReactNode>={
    grid:<><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></>,
    users:<><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/></>,
    chart:<><path d="M3 3v18h18"/><path d="m7 16 4-5 3 3 6-8"/></>,
    shield:<><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10Z"/><path d="m9 12 2 2 4-4"/></>,
    spark:<><path d="m12 3-1.8 5.2L5 10l5.2 1.8L12 17l1.8-5.2L19 10l-5.2-1.8L12 3Z"/><path d="m19 16-.8 2.2L16 19l2.2.8L19 22l.8-2.2L19 16Z"/></>,
    database:<><ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v7c0 1.7 3.6 3 8 3s8-1.3 8-3V5"/><path d="M4 12v7c0 1.7 3.6 3 8 3s8-1.3 8-3v-7"/></>,
    upload:<><path d="M12 16V4"/><path d="m7 9 5-5 5 5"/><path d="M5 20h14"/></>,
    arrow:<><path d="M5 12h14"/><path d="m13 6 6 6-6 6"/></>,
  };
  return <svg className="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">{p[name]}</svg>;
}

export default function Home(){
  const [customers,setCustomers]=useState<Customer[]>([]); const [summary,setSummary]=useState<Summary>({});
  const [q,setQ]=useState(""); const [answer,setAnswer]=useState(""); const [evidence,setEvidence]=useState<any>(null);
  const [loading,setLoading]=useState(false); const [error,setError]=useState("");
  const [file,setFile]=useState<File|null>(null); const [dataset,setDataset]=useState("customers"); const [replace,setReplace]=useState(false); const [uploading,setUploading]=useState(false); const [uploadMessage,setUploadMessage]=useState("");
  const [showAll,setShowAll]=useState(false); const inputRef=useRef<HTMLInputElement>(null);

  async function refresh(){
    try{ const [a,b]=await Promise.all([fetch(`${API}/api/v1/business/top-customers`),fetch(`${API}/api/v1/business/summary`)]); if(!a.ok||!b.ok) throw Error(); const top=await a.json(); const stats=await b.json(); setCustomers(top.customers||[]); setSummary(stats||{}); setError(""); }
    catch{setError("Backend API is not reachable. Start the backend on port 8000.");}
  }
  useEffect(()=>{refresh()},[]);
  function go(id:string){document.getElementById(id)?.scrollIntoView({behavior:"smooth",block:"start"})}
  async function ask(){
    if(!q.trim()||loading)return; setLoading(true);setError("");
    try{const r=await fetch(`${API}/api/v1/business/ask`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({question:q})});const x=await r.json();if(!r.ok)throw Error(x.detail||"Request failed");setAnswer(x.answer||"No decision returned.");setEvidence(x.evidence||null)}catch(e:any){setError(e.message||"Request failed")}finally{setLoading(false)}
  }
  function choose(f:File|null){if(f?.name.toLowerCase().endsWith(".csv"))setFile(f);else if(f)setError("Please choose a CSV file.")}
  function drop(e:DragEvent<HTMLDivElement>){e.preventDefault();choose(e.dataTransfer.files?.[0]||null)}
  async function upload(){
    if(!file||uploading)return; setUploading(true);setError("");setUploadMessage("");
    try{const form=new FormData();form.append("file",file);const r=await fetch(`${API}/api/v1/data/upload?dataset=${dataset}&replace=${replace}`,{method:"POST",body:form});const x=await r.json();if(!r.ok)throw Error(x.detail||"Upload failed");setUploadMessage(`${x.rows_imported} rows imported into ${dataset.replace("_"," ")}.`);setFile(null);if(inputRef.current)inputRef.current.value="";await refresh()}catch(e:any){setError(e.message||"Upload failed")}finally{setUploading(false)}
  }
  const total=Number(summary.total_revenue||0), count=Number(summary.customers??customers.length), tickets=Number(summary.open_tickets||0);
  const visible=showAll?customers:customers.slice(0,6);
  return <div className="shell">
    <aside className="sidebar">
      <div className="logoLockup"><img src={EMBLEM} className="emblem" alt="Business Signal"/><div><div className="logoName">Business Signal</div><div className="logoSub">DECISION INTELLIGENCE</div></div></div>
      <div className="navLabel">WORKSPACE</div>
      <nav>{[["Overview","overview","grid"],["Customers","customers","users"],["Revenue","metrics","chart"],["Risk & Signals","risk","shield"]].map(([label,id,icon])=><button className="navItem" key={label} onClick={()=>go(id)}><Icon name={icon}/><span>{label}</span></button>)}</nav>
      <div className="navLabel second">INTELLIGENCE</div>
      <nav><button className="navItem" onClick={()=>go("ask-ai")}><Icon name="spark"/><span>Ask AI</span></button><button className="navItem" onClick={()=>go("evidence")}><Icon name="database"/><span>Evidence</span></button></nav>
      <div className="sideBottom"><div className="system"><span className="liveDot"/>API connected</div><div className="sideBrand"><img src={EMBLEM} alt=""/><span>Business Signal AI</span></div></div>
    </aside>
    <main className="content">
      <header className="topbar"><div><div className="eyebrow">ENTERPRISE CONTROL CENTER</div><h1>Business intelligence</h1></div><div className="topActions"><div className="apiStatus"><span className="liveDot"/>Live API</div><div className="avatar">BS</div></div></header>
      <section id="overview" className="hero"><div className="heroCopy"><div className="pill">✦ AI-powered decision intelligence</div><h2>Your data.<br/><span>Your decisions.</span></h2><p>Connect real business data, surface meaningful signals, and ask questions in natural language. No fabricated metrics.</p><div className="heroButtons"><button className="primary" onClick={()=>go("ask-ai")}>Ask Business Signal <Icon name="arrow"/></button><button className="ghost" onClick={()=>go("import")}>Import data</button></div></div><div className="heroArt"><img src={BRAND} alt="Business Signal"/></div></section>
      <section id="metrics" className="metrics">
        <div className="metricCard"><div className="metricIcon cyan"><Icon name="users"/></div><div><span>Customers</span><strong>{count.toLocaleString()}</strong><small>From connected database</small></div></div>
        <div className="metricCard"><div className="metricIcon purple"><Icon name="chart"/></div><div><span>Revenue</span><strong>₹{total.toLocaleString(undefined,{maximumFractionDigits:0})}</strong><small>Recorded sales</small></div></div>
        <div className="metricCard"><div className="metricIcon green"><Icon name="shield"/></div><div><span>Open tickets</span><strong>{tickets.toLocaleString()}</strong><small>Current support backlog</small></div></div>
        <div className="metricCard"><div className="metricIcon blue"><Icon name="database"/></div><div><span>Data status</span><strong>{count||total||tickets?"LIVE":"EMPTY"}</strong><small>{count||total||tickets?"Using your database":"Import a CSV to begin"}</small></div></div>
      </section>
      <section id="ask-ai" className="aiPanel"><div className="panelHeader"><div><div className="sectionKicker"><Icon name="spark"/> BUSINESS COPILOT</div><h3>Ask Business Signal</h3><p>Ask about customers, revenue, support, risk, or indexed documents.</p></div><div className="engineBadge">RAG + SQL</div></div><div className="queryBox"><div className="queryIcon"><Icon name="spark"/></div><input value={q} onChange={e=>setQ(e.target.value)} onKeyDown={e=>e.key==="Enter"&&ask()} placeholder="e.g. Which customers are at risk and why?"/><button onClick={ask} disabled={loading}>{loading?"Analyzing…":"Run analysis"}<Icon name="arrow"/></button></div><div className="suggestions">{["Which customers are at risk and why?","Which customers generated the most revenue?","Summarize current support load"].map(x=><button key={x} onClick={()=>setQ(x)}>{x}</button>)}</div>{answer&&<div className="answerBox"><div className="answerHead"><span><span className="liveDot"/>Decision returned</span><span>Evidence {evidence?"available":"not attached"}</span></div><div className="answerText">{answer}</div></div>}</section>
      <section id="import" className="panel importPanel"><div className="panelHeader compact"><div><div className="sectionKicker"><Icon name="upload"/> YOUR BUSINESS DATA</div><h3>Bring your data in</h3><p>CSV import is the source of truth for the dashboard. Nothing is presented as real until it exists in your database.</p></div></div><div className="importControls"><select value={dataset} onChange={e=>setDataset(e.target.value)}><option value="customers">Customers</option><option value="sales">Sales</option><option value="support_tickets">Support tickets</option></select><div className={`dropzone ${file?"selected":""}`} onDragOver={e=>e.preventDefault()} onDrop={drop} onClick={()=>inputRef.current?.click()}><input ref={inputRef} type="file" accept=".csv,text/csv" onChange={e=>choose(e.target.files?.[0]||null)}/><Icon name="upload"/><strong>{file?file.name:"Drop CSV here"}</strong><span>{file?`${(file.size/1024).toFixed(1)} KB · ready to import`:"or click to choose a file"}</span></div><label className="replaceToggle"><input type="checkbox" checked={replace} onChange={e=>setReplace(e.target.checked)}/> Replace dataset</label><button className="smallButton" onClick={upload} disabled={!file||uploading}>{uploading?"Importing…":"Import data"}<Icon name="arrow"/></button></div><p className="importHint">Customers: name, industry, annual_value · Sales: customer_id, amount, sale_date · Support: customer_id, priority, status, subject, created_at</p>{uploadMessage&&<div className="successBox">{uploadMessage}</div>}</section>
      <section id="customers" className="panel customerPanel"><div className="panelHeader compact"><div><div className="sectionKicker"><Icon name="users"/> CUSTOMER INTELLIGENCE</div><h3>{count?"Customers":"Your customers"}</h3><p>{count?`${count.toLocaleString()} records in the connected database.`:"No customer records yet. Import a customers CSV to populate this table."}</p></div>{customers.length>6&&<button className="smallButton" onClick={()=>setShowAll(v=>!v)}>{showAll?"Show less":"View all"}<Icon name="arrow"/></button>}</div>{customers.length>0&&<div className="tableHead"><span>Customer</span><span>Industry</span><span>Revenue</span><span>ID</span></div>}{visible.map(c=><div className="customerRow" key={c.customer_id}><div className="customerName"><div className="customerAvatar">{c.customer?.slice(0,1).toUpperCase()||"•"}</div><div><strong>{c.customer}</strong><small>Customer #{c.customer_id}</small></div></div><span>{c.industry||"—"}</span><strong>₹{Number(c.revenue||0).toLocaleString()}</strong><span className="idTag">#{c.customer_id}</span></div>)}{!customers.length&&<div className="empty">Waiting for your data.</div>}</section>
      <section id="risk" className="twoCol"><div className="panel signalPanel"><div className="sectionKicker"><Icon name="shield"/> RISK & SIGNALS</div><h3>Evidence-based signals</h3><p className="panelDesc">Risk analysis is calculated from revenue movement and support activity. It is not a fixed health score.</p><div className="signalRows"><div><span>Customer risk engine</span><strong>AVAILABLE</strong></div><div><span>Revenue comparison</span><strong>90 / 180 days</strong></div><div><span>Support pressure</span><strong>{tickets} open tickets</strong></div></div></div><div className="panel dataState"><div className="sectionKicker"><Icon name="database"/> DATA COVERAGE</div><h3>{count?"Live dataset":"No dataset"}</h3><div className="coverage"><strong>{count.toLocaleString()}</strong><span>customer records</span></div><p>{count?"Dashboard values are being read from the backend database.":"Import your CSV to replace the empty state with your real business data."}</p></div></section>
      <section id="evidence" className="panel evidencePanel"><div className="panelHeader compact"><div><div className="sectionKicker"><Icon name="database"/> TRUST LAYER</div><h3>Evidence</h3><p>Responses can expose the backend evidence used for the decision.</p></div></div>{evidence?<pre className="evidenceCode">{JSON.stringify(evidence,null,2)}</pre>:<div className="evidenceEmpty"><div className="evidenceIcon"><Icon name="database"/></div><div><strong>No evidence attached yet</strong><p>Run an AI question to see the returned evidence.</p></div></div>}</section>
      {error&&<div className="errorBox globalError">{error}</div>}
      <footer><div><strong>Business Signal</strong>Decision intelligence for real business data.</div><span>FastAPI · PostgreSQL · RAG · SQL</span></footer>
    </main>
  </div>;
}
