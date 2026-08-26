"use client";
import { useEffect, useState } from "react";
const API=process.env.NEXT_PUBLIC_API_URL||"http://localhost:8000";

type Customer={customer_id:number;customer:string;revenue:number;industry:string;};
export default function Home(){
 const [customers,setCustomers]=useState<Customer[]>([]); const [q,setQ]=useState(""); const [answer,setAnswer]=useState(""); const [evidence,setEvidence]=useState<any>(null); const [loading,setLoading]=useState(false); const [error,setError]=useState("");
 useEffect(()=>{fetch(`${API}/api/v1/business/top-customers`).then(r=>r.json()).then(x=>setCustomers(x.customers||[])).catch(()=>setError("API unavailable. Start the backend first."))},[]);
 async function ask(){if(!q.trim())return;setLoading(true);setError("");try{const r=await fetch(`${API}/api/v1/business/ask`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({question:q})});const x=await r.json();if(!r.ok)throw Error(x.detail||"Request failed");setAnswer(x.answer||"");setEvidence(x.evidence||null)}catch(e:any){setError(e.message)}finally{setLoading(false)}}
 return <main><div className="header"><div><div className="brand">◈ Business Signal</div><div className="muted">AI-powered decision intelligence</div></div><div className="muted">Live workspace</div></div>
 <div className="grid"><div className="card"><div className="muted">Customers</div><div className="metric">{customers.length}</div></div><div className="card"><div className="muted">Data Sources</div><div className="metric">3+</div></div><div className="card"><div className="muted">AI Mode</div><div className="metric">RAG</div></div><div className="card"><div className="muted">Evidence</div><div className="metric">On</div></div></div>
 <div className="card" style={{marginTop:20}}><h2>Ask Business Signal</h2><div className="muted">Ask about revenue, customers, risk, support or company documents.</div><div className="ask"><input value={q} onChange={e=>setQ(e.target.value)} onKeyDown={e=>e.key==="Enter"&&ask()} placeholder="Which customers are at risk and why?"/><button onClick={ask}>{loading?"Thinking...":"Ask AI"}</button></div>{error&&<div className="error">{error}</div>}{answer&&<div><h3>Decision</h3><div className="result">{answer}</div></div>}</div>
 <div className="card customers"><h2>Top Customers</h2>{customers.map(c=><div className="row" key={c.customer_id}><span>{c.customer}</span><span>{c.industry}</span><span>₹{Number(c.revenue).toLocaleString()}</span><span className="risk low">ACTIVE</span></div>)}</div>
 {evidence&&<div className="card" style={{marginTop:20}}><h3>Evidence Trace</h3><div className="muted">Intent: {evidence.intent||"business"}</div><pre className="result">{JSON.stringify(evidence,null,2)}</pre></div>}</main>;
}
