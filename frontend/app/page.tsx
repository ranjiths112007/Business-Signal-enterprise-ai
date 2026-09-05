"use client";

import { DragEvent, useEffect, useRef, useState } from "react";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
const BRAND = "/Business%20Signal%20Neon%20Analytics%20Branding.png";
const EMBLEM = "/Neon%20Business%20Signal%20Emblem.png";

const SAMPLE_BASE = "https://github.com/ranjiths112007/Business-Signal-enterprise-ai/blob/main/data/sample";

type Customer = { customer_id: number; customer: string; revenue: number; industry: string };
type Summary = { customers?: number; total_revenue?: number; open_tickets?: number };
type Analysis = {
  dataset: string;
  columns: string[];
  mapping: Record<string, string | null>;
  requirements: string[];
  missing: string[];
  ready: boolean;
  message: string;
};

const LABELS: Record<string, string> = {
  name: "Customer / company",
  industry: "Industry / sector",
  annual_value: "Annual value",
  customer_id: "Customer reference",
  amount: "Sale amount",
  sale_date: "Sale date",
  priority: "Priority",
  status: "Status",
  subject: "Issue / subject",
  created_at: "Created date",
};

const DATASETS = [
  ["customers", "Customers"],
  ["sales", "Sales"],
  ["support_tickets", "Support"],
] as const;

function Icon({ name }: { name: string }) {
  const paths: Record<string, React.ReactNode> = {
    spark: <path d="m12 3-1.7 5.3L5 10l5.3 1.7L12 17l1.7-5.3L19 10l-5.3-1.7L12 3Z" />,
    upload: <><path d="M12 16V4"/><path d="m7 9 5-5 5 5"/><path d="M5 20h14"/></>,
    arrow: <><path d="M5 12h14"/><path d="m13 6 6 6-6 6"/></>,
    users: <><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/></>,
    database: <><ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v7c0 1.7 3.6 3 8 3s8-1.3 8-3V5"/><path d="M4 12v7c0 1.7 3.6 3 8 3s8-1.3 8-3v-7"/></>,
    check: <path d="m5 12 4 4L19 6"/>,
  };
  return <svg className="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">{paths[name]}</svg>;
}

export default function Home() {
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [summary, setSummary] = useState<Summary>({});
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [evidence, setEvidence] = useState<any>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [dataset, setDataset] = useState<(typeof DATASETS)[number][0]>("customers");
  const [file, setFile] = useState<File | null>(null);
  const [dragging, setDragging] = useState(false);
  const [analysis, setAnalysis] = useState<Analysis | null>(null);
  const [mapping, setMapping] = useState<Record<string, string | null>>({});
  const [replace, setReplace] = useState(false);
  const [importing, setImporting] = useState(false);
  const [showAll, setShowAll] = useState(false);
  const [message, setMessage] = useState("");
  const inputRef = useRef<HTMLInputElement>(null);

  async function refresh() {
    try {
      const [customersRes, summaryRes] = await Promise.all([
        fetch(`${API}/api/v1/business/top-customers?limit=50`),
        fetch(`${API}/api/v1/business/summary`),
      ]);
      if (!customersRes.ok || !summaryRes.ok) throw new Error();
      const [top, stats] = await Promise.all([customersRes.json(), summaryRes.json()]);
      setCustomers(top.customers || []);
      setSummary(stats || {});
      setError("");
    } catch {
      setError("Backend is not running. Start the API on port 8000.");
    }
  }

  useEffect(() => { refresh(); }, []);

  async function ask() {
    if (!question.trim() || loading) return;
    setLoading(true);
    setError("");
    try {
      const res = await fetch(`${API}/api/v1/business/ask`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Question failed");
      setAnswer(data.answer || "No answer returned.");
      setEvidence(data.evidence || null);
    } catch (e: any) {
      setError(e.message || "Question failed");
    } finally {
      setLoading(false);
    }
  }

  function choose(next: File | null) {
    if (!next) return;
    setError("");
    setMessage("");
    if (!next.name.toLowerCase().endsWith(".csv")) {
      setError("Please choose a CSV file.");
      return;
    }
    setFile(next);
    setAnalysis(null);
    setMapping({});
  }

  function drop(event: DragEvent<HTMLDivElement>) {
    event.preventDefault();
    setDragging(false);
    choose(event.dataTransfer.files?.[0] || null);
  }

  async function inspect() {
    if (!file || importing) return;
    setImporting(true);
    setError("");
    try {
      const form = new FormData();
      form.append("file", file);
      const res = await fetch(`${API}/api/v1/data/analyze?dataset=${dataset}`, { method: "POST", body: form });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Could not inspect the file");
      setAnalysis(data);
      setMapping(data.mapping || {});
    } catch (e: any) {
      setError(e.message || "Could not inspect the file");
    } finally {
      setImporting(false);
    }
  }

  async function importData() {
    if (!file || !analysis?.ready || importing) return;
    setImporting(true);
    setError("");
    try {
      const form = new FormData();
      form.append("file", file);
      form.append("mapping", JSON.stringify(mapping));
      const res = await fetch(`${API}/api/v1/data/upload?dataset=${dataset}&replace=${replace}`, { method: "POST", body: form });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Import failed");
      setMessage(`${data.rows_imported} rows imported. Business Signal is now using the data.`);
      setFile(null);
      setAnalysis(null);
      setMapping({});
      if (inputRef.current) inputRef.current.value = "";
      await refresh();
    } catch (e: any) {
      setError(e.message || "Import failed");
    } finally {
      setImporting(false);
    }
  }

  const count = Number(summary.customers ?? customers.length);
  const revenue = Number(summary.total_revenue ?? 0);
  const tickets = Number(summary.open_tickets ?? 0);
  const visibleCustomers = showAll ? customers : customers.slice(0, 6);

  return (
    <main className="page">
      <header className="header">
        <a className="brand" href="#top" aria-label="Business Signal home">
          <img src={EMBLEM} alt="" />
          <span>Business Signal</span>
        </a>
        <nav><a href="#demo">Demo</a><a href="#data">Data</a><a href="#results">Results</a></nav>
        <span className="projectTag">AI ENGINEERING PROJECT</span>
      </header>

      <section id="top" className="hero">
        <div className="heroCopy">
          <div className="eyebrow">BUSINESS SIGNAL · PROJECT SHOWCASE</div>
          <h1>Ask a business question.<br /><em>Find the signal.</em></h1>
          <p>Explore a small end-to-end AI engineering project that combines structured data, SQL, retrieval and grounded AI answers.</p>
          <div className="heroActions">
            <button className="primary" onClick={() => document.getElementById("demo")?.scrollIntoView({ behavior: "smooth" })}>Try the demo <Icon name="arrow" /></button>
            <a className="textButton" href="https://github.com/ranjiths112007/Business-Signal-enterprise-ai" target="_blank" rel="noreferrer">View source ↗</a>
          </div>
        </div>
        <img className="brandArt" src={BRAND} alt="Business Signal" />
      </section>

      <section className="techStrip" aria-label="Project stack">
        <span>FastAPI</span><span>PostgreSQL</span><span>SQL agent</span><span>RAG</span><span>Gemini</span><span>Evidence</span>
      </section>

      <section id="demo" className="workspace">
        <div className="sectionTitle"><span className="number">01</span><div><h2>Ask Business Signal</h2><p>Ask a question and inspect the answer plus its evidence.</p></div></div>
        <div className="askCard">
          <div className="askHeader"><Icon name="spark" /><span>Natural-language business analysis</span></div>
          <textarea value={question} onChange={(e) => setQuestion(e.target.value)} onKeyDown={(e) => { if ((e.ctrlKey || e.metaKey) && e.key === "Enter") ask(); }} placeholder="Which customers are at risk and why?" />
          <div className="askFooter"><div className="examples">{["Which customers are at risk and why?", "Who generated the most revenue?", "What is the current support load?"].map((item) => <button key={item} onClick={() => setQuestion(item)}>{item}</button>)}</div><button className="primary compact" onClick={ask} disabled={loading}>{loading ? "Analyzing…" : "Run question"}<Icon name="arrow" /></button></div>
          {answer && <div className="answer"><div><span className="answerLabel">ANSWER</span><span className="evidenceState">{evidence ? "Evidence attached" : "No evidence"}</span></div><p>{answer}</p></div>}
        </div>
      </section>

      <section id="data" className="workspace">
        <div className="sectionTitle"><span className="number">02</span><div><h2>Optional: use your own CSV</h2><p>The demo data is already included. Bring your own file only when you want to test the mapper.</p></div></div>
        <div className="dataCard">
          <div className="dataTop"><div className="tabs">{DATASETS.map(([value, label]) => <button key={value} className={dataset === value ? "active" : ""} onClick={() => { setDataset(value); setFile(null); setAnalysis(null); setMapping({}); }}>{label}</button>)}</div><a className="sampleLink" href={`${SAMPLE_BASE}/${dataset}.csv`} target="_blank" rel="noreferrer">Open demo CSV ↗</a></div>
          <div className={`dropzone ${dragging ? "dragging" : ""} ${file ? "selected" : ""}`} onDragEnter={(e) => { e.preventDefault(); setDragging(true); }} onDragOver={(e) => e.preventDefault()} onDragLeave={() => setDragging(false)} onDrop={drop} onClick={() => inputRef.current?.click()}>
            <input ref={inputRef} type="file" accept=".csv,text/csv" onChange={(e) => choose(e.target.files?.[0] || null)} />
            <div className="uploadMark"><Icon name="upload" /></div>
            <strong>{file ? file.name : "Drop a CSV here"}</strong>
            <span>{file ? `${(file.size / 1024).toFixed(1)} KB · ready to inspect` : "or click to browse"}</span>
          </div>
          {file && !analysis && <button className="primary inspect" onClick={(e) => { e.stopPropagation(); inspect(); }} disabled={importing}>{importing ? "Inspecting…" : "Inspect columns"}<Icon name="arrow" /></button>}
          {analysis && <div className="mapping">
            <div className="mappingHeader"><div><strong>Column mapping</strong><p>{analysis.message}</p></div><span className={analysis.ready ? "ready" : "review"}>{analysis.ready ? "READY" : "REVIEW"}</span></div>
            <div className="mappingGrid">{analysis.requirements.map((field) => <label key={field}><span>{LABELS[field] || field}</span><select value={mapping[field] || ""} onChange={(e) => setMapping((m) => ({ ...m, [field]: e.target.value || null }))}><option value="">Choose column</option>{analysis.columns.map((column) => <option value={column} key={column}>{column}</option>)}</select></label>)}</div>
            <div className="mappingFooter"><span>{analysis.ready ? <><Icon name="check" /> All required fields mapped</> : "Map the missing fields to continue."}</span><div><label className="replace"><input type="checkbox" checked={replace} onChange={(e) => setReplace(e.target.checked)} /> Replace dataset</label><button className="primary compact" onClick={importData} disabled={!analysis.ready || importing}>{importing ? "Importing…" : "Import data"}<Icon name="arrow" /></button></div></div>
          </div>}
          <div className="dataNote"><strong>Demo CSVs</strong><span>Customers: company, industry, annual value</span><span>Sales: customer name, amount, date</span><span>Support: customer name, priority, status, issue, date</span><small>Column names can differ in your own files; the mapper handles common variations.</small></div>
          {message && <div className="success">{message}</div>}
          {error && <div className="error">{error}</div>}
        </div>
      </section>

      <section id="results" className="workspace">
        <div className="sectionTitle"><span className="number">03</span><div><h2>What the demo data says</h2><p>These values come from the local database seeded for this project.</p></div></div>
        <div className="stats"><div><span>Customers</span><strong>{count.toLocaleString()}</strong></div><div><span>Recorded revenue</span><strong>₹{revenue.toLocaleString(undefined, { maximumFractionDigits: 0 })}</strong></div><div><span>Open tickets</span><strong>{tickets.toLocaleString()}</strong></div></div>
        <div className="resultsGrid">
          <div className="resultCard"><div className="resultHeader"><div><span className="resultKicker"><Icon name="users" /> CUSTOMER DATA</span><h3>{count ? "Demo customers" : "No customer data yet"}</h3></div>{customers.length > 6 && <button className="textButton" onClick={() => setShowAll((v) => !v)}>{showAll ? "Show less" : "View all"}</button>}</div>
            {customers.length ? visibleCustomers.map((customer) => <div className="customer" key={customer.customer_id}><div className="avatar">{customer.customer.slice(0, 1).toUpperCase()}</div><div><strong>{customer.customer}</strong><small>{customer.industry || "No industry"}</small></div><b>₹{Number(customer.revenue || 0).toLocaleString()}</b></div>) : <div className="empty">No demo data loaded yet.</div>}
          </div>
          <div className="resultCard"><div className="resultHeader"><div><span className="resultKicker"><Icon name="database" /> EVIDENCE</span><h3>{evidence ? "Trace from the answer" : "Ready for evidence"}</h3></div></div>{evidence ? <pre>{JSON.stringify(evidence, null, 2)}</pre> : <div className="evidenceEmpty"><p>Run a question above to see the structured evidence returned by Business Signal.</p></div>}</div>
        </div>
      </section>

      <footer><div><img src={EMBLEM} alt="" /><span>Business Signal</span></div><small>AI engineering project · SQL + RAG + evidence</small></footer>
    </main>
  );
}
