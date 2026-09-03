"use client";

import { useEffect, useMemo, useState } from "react";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
const BRAND = "/Business%20Signal%20Neon%20Analytics%20Branding.png";
const EMBLEM = "/Neon%20Business%20Signal%20Emblem.png";

type Customer = {
  customer_id: number;
  customer: string;
  revenue: number;
  industry: string;
};

type Summary = {
  customers?: number;
  total_revenue?: number;
  open_tickets?: number;
};

function Icon({ name }: { name: string }) {
  const paths: Record<string, React.ReactNode> = {
    grid: <><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></>,
    users: <><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/></>,
    chart: <><path d="M3 3v18h18"/><path d="m7 16 4-5 3 3 6-8"/></>,
    shield: <><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10Z"/><path d="m9 12 2 2 4-4"/></>,
    spark: <><path d="m12 3-1.8 5.2L5 10l5.2 1.8L12 17l1.8-5.2L19 10l-5.2-1.8L12 3Z"/><path d="m19 16-.8 2.2L16 19l2.2.8L19 22l.8-2.2L22 19l-2.2-.8L19 16Z"/></>,
    database: <><ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v7c0 1.7 3.6 3 8 3s8-1.3 8-3V5"/><path d="M4 12v7c0 1.7 3.6 3 8 3s8-1.3 8-3v-7"/></>,
    arrow: <><path d="M5 12h14"/><path d="m13 6 6 6-6 6"/></>,
    activity: <><path d="M3 12h4l3-8 4 16 3-8h4"/></>,
  };
  return <svg className="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">{paths[name]}</svg>;
}

export default function Home() {
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [summary, setSummary] = useState<Summary>({});
  const [q, setQ] = useState("");
  const [answer, setAnswer] = useState("");
  const [evidence, setEvidence] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [active, setActive] = useState("Overview");

  useEffect(() => {
    Promise.all([
      fetch(`${API}/api/v1/business/top-customers`).then((r) => r.json()),
      fetch(`${API}/api/v1/business/summary`).then((r) => r.json()),
    ])
      .then(([top, stats]) => {
        setCustomers(top.customers || []);
        setSummary(stats || {});
      })
      .catch(() => setError("API unavailable. Start the backend first."));
  }, []);

  async function ask() {
    if (!q.trim() || loading) return;
    setLoading(true);
    setError("");
    try {
      const r = await fetch(`${API}/api/v1/business/ask`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: q }),
      });
      const x = await r.json();
      if (!r.ok) throw Error(x.detail || "Request failed");
      setAnswer(x.answer || "No decision returned.");
      setEvidence(x.evidence || null);
    } catch (e: any) {
      setError(e.message || "Request failed");
    } finally {
      setLoading(false);
    }
  }

  const totalRevenue = Number(summary.total_revenue ?? customers.reduce((n, c) => n + Number(c.revenue || 0), 0));
  const customerCount = Number(summary.customers ?? customers.length);
  const ticketCount = Number(summary.open_tickets ?? 0);
  const avgRevenue = customerCount ? totalRevenue / customerCount : 0;

  const prompts = [
    "Which customers are at risk and why?",
    "Which customers generated the most revenue?",
    "Give me a business health summary",
  ];

  const healthItems = useMemo(() => [
    { label: "Revenue signal", value: "Strong", cls: "positive" },
    { label: "Customer activity", value: "Healthy", cls: "positive" },
    { label: "Support load", value: ticketCount ? `${ticketCount} open` : "Stable", cls: ticketCount > 10 ? "warning" : "positive" },
  ], [ticketCount]);

  return (
    <div className="shell">
      <aside className="sidebar">
        <div className="logoLockup">
          <img src={EMBLEM} alt="Business Signal" className="emblem" />
          <div><div className="logoName">Business Signal</div><div className="logoSub">DECISION INTELLIGENCE</div></div>
        </div>
        <div className="navLabel">WORKSPACE</div>
        <nav>
          {["Overview", "Customers", "Revenue", "Risk & Signals"].map((item, i) => (
            <button key={item} className={`navItem ${active === item ? "active" : ""}`} onClick={() => setActive(item)}>
              <Icon name={i === 0 ? "grid" : i === 1 ? "users" : i === 2 ? "chart" : "shield"}/><span>{item}</span>
            </button>
          ))}
        </nav>
        <div className="navLabel second">INTELLIGENCE</div>
        <nav>
          <button className="navItem" onClick={() => document.getElementById("ask-ai")?.scrollIntoView({ behavior: "smooth" })}><Icon name="spark"/><span>Ask AI</span><span className="kbd">⌘K</span></button>
          <button className="navItem" onClick={() => document.getElementById("evidence")?.scrollIntoView({ behavior: "smooth" })}><Icon name="database"/><span>Evidence</span></button>
        </nav>
        <div className="sideBottom">
          <div className="system"><span className="liveDot"/>All systems operational</div>
          <div className="sideBrand"><img src={EMBLEM} alt=""/> <span>Business Signal AI</span></div>
        </div>
      </aside>

      <main className="content">
        <header className="topbar">
          <div><div className="eyebrow">ENTERPRISE CONTROL CENTER</div><h1>{active === "Overview" ? "Business overview" : active}</h1></div>
          <div className="topActions"><div className="apiStatus"><span className="liveDot"/>Live API</div><div className="avatar">BS</div></div>
        </header>

        <section className="hero">
          <div className="heroCopy">
            <div className="pill"><span className="sparkMini">✦</span> AI-powered decision intelligence</div>
            <h2>Turn business data into <span>decisions.</span></h2>
            <p>Detect signals, understand what changed, and act with evidence-backed intelligence across your business.</p>
            <div className="heroButtons"><button className="primary" onClick={() => document.getElementById("ask-ai")?.scrollIntoView({ behavior: "smooth" })}>Ask Business Signal <Icon name="arrow"/></button><button className="ghost" onClick={() => document.getElementById("customers")?.scrollIntoView({ behavior: "smooth" })}>View customers</button></div>
          </div>
          <div className="heroArt"><img src={BRAND} alt="Business Signal — Enterprise Decision Intelligence"/></div>
        </section>

        <section className="metrics">
          <div className="metricCard"><div className="metricIcon cyan"><Icon name="users"/></div><div><span>Total customers</span><strong>{customerCount.toLocaleString()}</strong><small>Active business accounts</small></div></div>
          <div className="metricCard"><div className="metricIcon purple"><Icon name="chart"/></div><div><span>Total revenue</span><strong>₹{totalRevenue.toLocaleString(undefined, { maximumFractionDigits: 0 })}</strong><small>₹{avgRevenue.toLocaleString(undefined, { maximumFractionDigits: 0 })} avg. / customer</small></div></div>
          <div className="metricCard"><div className="metricIcon green"><Icon name="activity"/></div><div><span>Open support tickets</span><strong>{ticketCount.toLocaleString()}</strong><small>{ticketCount ? "Needs attention" : "No active backlog"}</small></div></div>
          <div className="metricCard"><div className="metricIcon blue"><Icon name="shield"/></div><div><span>AI evidence mode</span><strong>ON</strong><small>Traceable answers</small></div></div>
        </section>

        <section id="ask-ai" className="aiPanel">
          <div className="panelHeader"><div><div className="sectionKicker"><Icon name="spark"/> BUSINESS COPILOT</div><h3>Ask Business Signal</h3><p>Query customers, revenue, support, risk, or indexed documents.</p></div><div className="engineBadge"><span className="pulse"/>RAG + SQL</div></div>
          <div className="queryBox"><div className="queryIcon"><Icon name="spark"/></div><input value={q} onChange={(e) => setQ(e.target.value)} onKeyDown={(e) => e.key === "Enter" && ask()} placeholder="Ask a business question…"/><button onClick={ask} disabled={loading}>{loading ? "Analyzing…" : "Run analysis"}<Icon name="arrow"/></button></div>
          <div className="suggestions">{prompts.map((p) => <button key={p} onClick={() => setQ(p)}>{p}</button>)}</div>
          {error && <div className="errorBox">{error}</div>}
          {answer && <div className="answerBox"><div className="answerHead"><span><span className="liveDot"/>Decision returned</span><span>Evidence {evidence ? "available" : "not attached"}</span></div><div className="answerText">{answer}</div></div>}
        </section>

        <section className="twoCol">
          <div id="customers" className="panel customerPanel">
            <div className="panelHeader compact"><div><div className="sectionKicker"><Icon name="users"/> CUSTOMER INTELLIGENCE</div><h3>Top customers</h3></div><button className="smallButton">View all <Icon name="arrow"/></button></div>
            <div className="tableHead"><span>Customer</span><span>Industry</span><span>Revenue</span><span>Status</span></div>
            {customers.length === 0 && <div className="empty">No customer data returned yet.</div>}
            {customers.slice(0, 6).map((c, index) => <div className="customerRow" key={c.customer_id}><div className="customerName"><div className={`customerAvatar avatar${index % 4}`}>{c.customer.slice(0, 1).toUpperCase()}</div><div><strong>{c.customer}</strong><small>ID #{c.customer_id}</small></div></div><span>{c.industry || "—"}</span><strong>₹{Number(c.revenue).toLocaleString()}</strong><span className="statusTag"><i/>ACTIVE</span></div>)}
          </div>
          <div className="panel healthPanel">
            <div className="sectionKicker"><Icon name="shield"/> SIGNAL HEALTH</div><h3>Business pulse</h3><p className="panelDesc">A quick read of your current operating signals.</p>
            <div className="pulseOrb"><div className="orbCore">98<span>%</span></div><small>HEALTH SCORE</small></div>
            <div className="healthList">{healthItems.map((item) => <div key={item.label}><span>{item.label}</span><strong className={item.cls}>{item.value}</strong></div>)}</div>
          </div>
        </section>

        <section id="evidence" className="panel evidencePanel">
          <div className="panelHeader compact"><div><div className="sectionKicker"><Icon name="database"/> TRUST LAYER</div><h3>Evidence & capabilities</h3></div><div className="capabilities">{["RAG", "SQL Agent", "Risk Engine", "Prompt Guard", "PostgreSQL", "pgvector"].map(x => <span key={x}>{x}</span>)}</div></div>
          {evidence ? <pre className="evidenceCode">{JSON.stringify(evidence, null, 2)}</pre> : <div className="evidenceEmpty"><div className="evidenceIcon"><Icon name="shield"/></div><div><strong>Evidence trace is ready</strong><p>Run an AI analysis above to inspect the intent, source evidence, and supporting data behind the decision.</p></div></div>}
        </section>

        <footer><div><strong>Business Signal</strong><span>Detect · Analyze · Predict · Act</span></div><span>Enterprise Decision Intelligence</span></footer>
      </main>
    </div>
  );
}
