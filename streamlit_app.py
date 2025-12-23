import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="FSM Processor Control Unit | DDCO Project",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern Dark Theme CSS - Stable and Clean
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    /* Base */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    }
    
    /* Hide Streamlit branding but keep sidebar toggle visible */
    #MainMenu, footer {visibility: hidden;}
    
    /* Ensure sidebar toggle button is always visible */
    button[data-testid="stExpandSidebarButton"],
    button[data-testid="stCollapseSidebarButton"] {
        visibility: visible !important;
        opacity: 1 !important;
        background: rgba(99, 102, 241, 0.2) !important;
        border: 1px solid rgba(99, 102, 241, 0.3) !important;
        border-radius: 8px !important;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.95);
        border-right: 1px solid rgba(148, 163, 184, 0.1);
    }
    
    section[data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }
    
    /* Main Header */
    .main-header {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(139, 92, 246, 0.15) 100%);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 16px;
        padding: 28px 32px;
        margin-bottom: 24px;
        text-align: center;
    }
    
    .main-header h1 {
        background: linear-gradient(135deg, #818cf8 0%, #a78bfa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2rem;
        font-weight: 700;
        margin: 0 0 8px 0;
        letter-spacing: -0.02em;
    }
    
    .main-header p {
        color: #94a3b8;
        font-size: 1rem;
        margin: 0;
    }
    
    /* Cards */
    .card {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
        backdrop-filter: blur(10px);
    }
    
    .card-header {
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #94a3b8;
        margin-bottom: 16px;
        padding-bottom: 12px;
        border-bottom: 1px solid rgba(148, 163, 184, 0.1);
    }
    
    /* FSM Diagram Container */
    .fsm-container {
        background: rgba(15, 23, 42, 0.8);
        border-radius: 12px;
        padding: 24px;
        text-align: center;
    }
    
    /* State Pills */
    .state-grid {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        justify-content: center;
    }
    
    .state-pill {
        background: rgba(51, 65, 85, 0.6);
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 20px;
        padding: 10px 18px;
        display: inline-flex;
        flex-direction: column;
        align-items: center;
        min-width: 80px;
        transition: all 0.3s ease;
    }
    
    .state-pill.active {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        border-color: #818cf8;
        box-shadow: 0 0 20px rgba(99, 102, 241, 0.4);
        transform: scale(1.05);
    }
    
    .state-pill .name {
        font-size: 0.8rem;
        font-weight: 600;
        color: #e2e8f0;
    }
    
    .state-pill.active .name {
        color: #ffffff;
    }
    
    .state-pill .id {
        font-size: 0.65rem;
        color: #64748b;
        margin-top: 2px;
    }
    
    .state-pill.active .id {
        color: rgba(255, 255, 255, 0.8);
    }
    
    /* Register Grid */
    .reg-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 12px;
    }
    
    .reg-item {
        background: rgba(51, 65, 85, 0.4);
        border-radius: 10px;
        padding: 14px 10px;
        text-align: center;
        border: 1px solid rgba(148, 163, 184, 0.1);
    }
    
    .reg-label {
        font-size: 0.7rem;
        color: #64748b;
        font-weight: 500;
        text-transform: uppercase;
    }
    
    .reg-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.4rem;
        font-weight: 600;
        color: #818cf8;
        margin-top: 4px;
    }
    
    /* Signal List */
    .signal-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 14px;
        background: rgba(51, 65, 85, 0.3);
        border-radius: 8px;
        margin-bottom: 8px;
        border-left: 3px solid #334155;
        transition: all 0.2s ease;
    }
    
    .signal-item.active {
        background: rgba(34, 197, 94, 0.15);
        border-left-color: #22c55e;
    }
    
    .signal-name {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        color: #cbd5e1;
    }
    
    .signal-badge {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        font-weight: 600;
        padding: 4px 10px;
        border-radius: 6px;
        background: #334155;
        color: #64748b;
    }
    
    .signal-badge.active {
        background: #22c55e;
        color: #ffffff;
    }
    
    /* Console */
    .console {
        background: #0f172a;
        border-radius: 10px;
        padding: 14px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
        max-height: 200px;
        overflow-y: auto;
        border: 1px solid rgba(148, 163, 184, 0.1);
    }
    
    .log-entry {
        padding: 5px 0;
        color: #64748b;
        border-bottom: 1px solid rgba(148, 163, 184, 0.05);
    }
    
    .log-entry:last-child {
        border-bottom: none;
    }
    
    .log-entry.info { color: #60a5fa; }
    .log-entry.success { color: #4ade80; }
    .log-entry.warning { color: #fbbf24; }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        padding: 10px 22px !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4) !important;
    }
    
    /* Status Badge */
    .status-chip {
        display: inline-block;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: #ffffff;
        padding: 10px 24px;
        border-radius: 25px;
        font-weight: 600;
        font-size: 0.95rem;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', monospace !important;
        color: #818cf8 !important;
        font-size: 1.8rem !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #64748b !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(30, 41, 59, 0.6);
        border-radius: 12px;
        padding: 6px;
        gap: 6px;
        border: 1px solid rgba(148, 163, 184, 0.1);
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px !important;
        color: #94a3b8 !important;
        font-weight: 500 !important;
        padding: 10px 20px !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
        color: #ffffff !important;
    }
    
    /* Selectbox */
    .stSelectbox > div > div {
        background: rgba(51, 65, 85, 0.6) !important;
        border: 1px solid rgba(148, 163, 184, 0.2) !important;
        border-radius: 10px !important;
        color: #e2e8f0 !important;
    }
    
    .stSelectbox label {
        color: #94a3b8 !important;
    }
    
    /* DataFrames */
    .stDataFrame {
        border-radius: 10px !important;
        overflow: hidden;
    }
    
    /* Team Cards */
    .team-member {
        background: rgba(51, 65, 85, 0.4);
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .team-member:hover {
        background: rgba(99, 102, 241, 0.15);
        border-color: rgba(99, 102, 241, 0.3);
        transform: translateY(-5px);
    }
    
    .team-member .icon {
        font-size: 2.5rem;
        margin-bottom: 12px;
    }
    
    .team-member .name {
        color: #e2e8f0;
        font-weight: 600;
        font-size: 1rem;
    }
    
    .team-member .usn {
        color: #64748b;
        font-size: 0.85rem;
        margin-top: 6px;
    }
    
    .team-member.highlighted {
        border-color: rgba(129, 140, 248, 0.4);
        box-shadow: 0 0 15px rgba(99, 102, 241, 0.15);
    }
    
    .team-member.highlighted .name {
        color: #a5b4fc;
    }
    
    /* Markdown Text */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #e2e8f0 !important;
    }
    
    .stMarkdown p, .stMarkdown li {
        color: #cbd5e1 !important;
    }
    
    .stMarkdown code {
        background: rgba(51, 65, 85, 0.6) !important;
        color: #818cf8 !important;
    }
    
    /* Tables in markdown */
    .stMarkdown table {
        width: 100%;
    }
    
    .stMarkdown th {
        background: rgba(51, 65, 85, 0.6) !important;
        color: #e2e8f0 !important;
    }
    
    .stMarkdown td {
        color: #cbd5e1 !important;
    }
    
    /* Divider */
    hr {
        border-color: rgba(148, 163, 184, 0.1) !important;
    }
</style>
""", unsafe_allow_html=True)

# Session State
if 'state' not in st.session_state:
    st.session_state.state = 0
if 'cycle' not in st.session_state:
    st.session_state.cycle = 0
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'regs' not in st.session_state:
    st.session_state.regs = [15, 25, 0, 0]
if 'pc' not in st.session_state:
    st.session_state.pc = 0
if 'signals' not in st.session_state:
    st.session_state.signals = {'PCWrite': 0, 'IRWrite': 0, 'MemRead': 0, 'MemWrite': 0, 'RegWrite': 0, 'ALUOp': '00'}
if 'waveform' not in st.session_state:
    st.session_state.waveform = []

STATES = ['IDLE', 'FETCH', 'DECODE', 'EXE_ALU', 'EXE_MEM', 'EXE_BR', 'WB', 'HALT']
INSTR = {'ADD': '000', 'SUB': '001', 'AND': '010', 'OR': '011', 'LOAD': '100', 'STORE': '101', 'BEQ': '110', 'HALT': '111'}

def log(msg, t='info'):
    st.session_state.logs.append({'c': st.session_state.cycle, 'm': msg, 't': t})

def reset():
    st.session_state.state = 0
    st.session_state.cycle = 0
    st.session_state.logs = []
    st.session_state.regs = [15, 25, 0, 0]
    st.session_state.pc = 0
    st.session_state.signals = {'PCWrite': 0, 'IRWrite': 0, 'MemRead': 0, 'MemWrite': 0, 'RegWrite': 0, 'ALUOp': '00'}
    st.session_state.waveform = []
    log("Processor reset", 'success')

def next_state(op):
    s = st.session_state.state
    if s == 0: return 1
    if s == 1: return 2
    if s == 2:
        if op in ['000','001','010','011']: return 3
        if op in ['100','101']: return 4
        if op == '110': return 5
        if op == '111': return 7
    if s in [3,4,5]: return 6
    if s == 6: return 1
    return s

def apply(op):
    st.session_state.signals = {'PCWrite': 0, 'IRWrite': 0, 'MemRead': 0, 'MemWrite': 0, 'RegWrite': 0, 'ALUOp': '00'}
    s = st.session_state.state
    r = st.session_state.regs
    if s == 1:
        st.session_state.signals.update({'MemRead': 1, 'IRWrite': 1, 'PCWrite': 1})
        st.session_state.pc += 1
    elif s == 3:
        st.session_state.signals['ALUOp'] = '10'
        if op == '000': r[2] = (r[0] + r[1]) & 0xFF
        elif op == '001': r[2] = (r[0] - r[1]) & 0xFF
        elif op == '010': r[2] = r[0] & r[1]
        elif op == '011': r[2] = r[0] | r[1]
    elif s == 4:
        if op == '100':
            st.session_state.signals['MemRead'] = 1
            r[0] = 42
        else:
            st.session_state.signals['MemWrite'] = 1
    elif s == 5:
        st.session_state.signals['ALUOp'] = '01'
    elif s == 6:
        if op not in ['101','110','111']:
            st.session_state.signals['RegWrite'] = 1
        st.session_state.signals['PCWrite'] = 1
    
    st.session_state.waveform.append({
        'Cycle': st.session_state.cycle,
        'State': STATES[s],
        'PCWrite': st.session_state.signals['PCWrite'],
        'MemRead': st.session_state.signals['MemRead'],
        'RegWrite': st.session_state.signals['RegWrite']
    })

def step(op):
    name = [k for k,v in INSTR.items() if v == op][0]
    log(f"{STATES[st.session_state.state]} → {name}")
    apply(op)
    if st.session_state.state == 6:
        log(f"{name} completed", 'success')
    nxt = next_state(op)
    if nxt == 7 and st.session_state.state != 7:
        log("HALTED", 'warning')
    st.session_state.state = nxt
    st.session_state.cycle += 1

# FSM Diagram using native SVG (no components.html for stability)
def render_fsm_diagram():
    c = st.session_state.state
    
    def fill(i):
        return "url(#grad)" if i == c else "#334155"
    
    def stroke(i):
        return "#818cf8" if i == c else "#475569"
    
    def txt(i):
        return "#ffffff" if i == c else "#94a3b8"
    
    def glow(i):
        return 'filter="url(#glow)"' if i == c else ''
    
    svg = f'''
    <svg viewBox="0 0 650 320" style="width:100%; height:auto; max-height:320px;">
        <defs>
            <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#6366f1"/>
                <stop offset="100%" style="stop-color:#8b5cf6"/>
            </linearGradient>
            <filter id="glow">
                <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
                <feMerge>
                    <feMergeNode in="coloredBlur"/>
                    <feMergeNode in="SourceGraphic"/>
                </feMerge>
            </filter>
            <marker id="arrowhead" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
                <polygon points="0 0, 8 3, 0 6" fill="#475569"/>
            </marker>
        </defs>
        
        <!-- Background -->
        <rect width="650" height="320" fill="transparent" rx="12"/>
        
        <!-- Arrows -->
        <path d="M 325 55 L 175 90" fill="none" stroke="#475569" stroke-width="1.5" marker-end="url(#arrowhead)"/>
        <path d="M 175 130 L 475 130" fill="none" stroke="#475569" stroke-width="1.5" marker-end="url(#arrowhead)"/>
        <path d="M 455 150 L 105 185" fill="none" stroke="#475569" stroke-width="1.5" marker-end="url(#arrowhead)"/>
        <path d="M 475 150 L 245 185" fill="none" stroke="#475569" stroke-width="1.5" marker-end="url(#arrowhead)"/>
        <path d="M 495 150 L 375 185" fill="none" stroke="#475569" stroke-width="1.5" marker-end="url(#arrowhead)"/>
        <path d="M 515 150 L 545 185" fill="none" stroke="#475569" stroke-width="1.5" marker-end="url(#arrowhead)"/>
        <path d="M 105 245 L 295 275" fill="none" stroke="#475569" stroke-width="1.5" marker-end="url(#arrowhead)"/>
        <path d="M 245 245 L 310 275" fill="none" stroke="#475569" stroke-width="1.5" marker-end="url(#arrowhead)"/>
        <path d="M 375 245 L 335 275" fill="none" stroke="#475569" stroke-width="1.5" marker-end="url(#arrowhead)"/>
        <path d="M 280 290 Q 65 260 155 150" fill="none" stroke="#475569" stroke-width="1.5" stroke-dasharray="4,2" marker-end="url(#arrowhead)"/>
        
        <!-- Labels -->
        <text x="240" y="65" fill="#64748b" font-size="10" font-family="Inter">start</text>
        <text x="310" y="120" fill="#64748b" font-size="9" font-family="Inter">always</text>
        <text x="245" y="172" fill="#64748b" font-size="9" font-family="Inter">ALU</text>
        <text x="335" y="172" fill="#64748b" font-size="9" font-family="Inter">MEM</text>
        <text x="425" y="172" fill="#64748b" font-size="9" font-family="Inter">BR</text>
        <text x="520" y="172" fill="#64748b" font-size="9" font-family="Inter">HALT</text>
        <text x="85" y="268" fill="#64748b" font-size="9" font-family="Inter">loop</text>
        
        <!-- States -->
        <circle cx="325" cy="35" r="26" fill="{fill(0)}" stroke="{stroke(0)}" stroke-width="2" {glow(0)}/>
        <text x="325" y="40" fill="{txt(0)}" font-size="11" font-weight="600" text-anchor="middle" font-family="Inter">IDLE</text>
        
        <circle cx="155" cy="115" r="26" fill="{fill(1)}" stroke="{stroke(1)}" stroke-width="2" {glow(1)}/>
        <text x="155" y="120" fill="{txt(1)}" font-size="11" font-weight="600" text-anchor="middle" font-family="Inter">FETCH</text>
        
        <circle cx="495" cy="115" r="26" fill="{fill(2)}" stroke="{stroke(2)}" stroke-width="2" {glow(2)}/>
        <text x="495" y="120" fill="{txt(2)}" font-size="10" font-weight="600" text-anchor="middle" font-family="Inter">DECODE</text>
        
        <circle cx="85" cy="215" r="26" fill="{fill(3)}" stroke="{stroke(3)}" stroke-width="2" {glow(3)}/>
        <text x="85" y="220" fill="{txt(3)}" font-size="9" font-weight="600" text-anchor="middle" font-family="Inter">EXE_ALU</text>
        
        <circle cx="225" cy="215" r="26" fill="{fill(4)}" stroke="{stroke(4)}" stroke-width="2" {glow(4)}/>
        <text x="225" y="220" fill="{txt(4)}" font-size="9" font-weight="600" text-anchor="middle" font-family="Inter">EXE_MEM</text>
        
        <circle cx="365" cy="215" r="26" fill="{fill(5)}" stroke="{stroke(5)}" stroke-width="2" {glow(5)}/>
        <text x="365" y="220" fill="{txt(5)}" font-size="10" font-weight="600" text-anchor="middle" font-family="Inter">EXE_BR</text>
        
        <circle cx="555" cy="215" r="26" fill="{'#f59e0b' if c==7 else '#334155'}" stroke="{'#fbbf24' if c==7 else '#475569'}" stroke-width="2" {'filter="url(#glow)"' if c==7 else ''}/>
        <text x="555" y="220" fill="{txt(7)}" font-size="11" font-weight="600" text-anchor="middle" font-family="Inter">HALT</text>
        
        <circle cx="315" cy="290" r="26" fill="{fill(6)}" stroke="{stroke(6)}" stroke-width="2" {glow(6)}/>
        <text x="315" y="295" fill="{txt(6)}" font-size="11" font-weight="600" text-anchor="middle" font-family="Inter">WB</text>
    </svg>
    '''
    return svg

# ==================== UI ====================

# Header
st.markdown("""
<div class="main-header">
    <h1>⚙️ FSM Processor Control Unit</h1>
    <p>Interactive Finite State Machine Simulator • DDCO Mini Project</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🎛️ Control Panel")
    
    instr = st.selectbox("Select Instruction", list(INSTR.keys()), format_func=lambda x: f"{x} ({INSTR[x]})")
    op = INSTR[instr]
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("⏭️ Step", use_container_width=True): 
            step(op)
    with c2:
        if st.button("🔄 Reset", use_container_width=True): 
            reset()
    
    if st.button("▶️ Run Full Cycle", use_container_width=True):
        for _ in range(6):
            if st.session_state.state != 7: 
                step(op)
    
    st.markdown("---")
    
    st.markdown("### 📊 Processor Status")
    c1, c2 = st.columns(2)
    c1.metric("Cycles", st.session_state.cycle)
    c2.metric("PC", f"0x{st.session_state.pc:02X}")
    
    st.markdown(f'''<div style="text-align:center; margin:16px 0;">
        <span class="status-chip">{STATES[st.session_state.state]}</span>
    </div>''', unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 👥 Team")
    st.markdown('<span style="color: #818cf8; font-weight: 600;">⚡ Vignesh B S</span> — 1BI24IS187', unsafe_allow_html=True)
    st.markdown("**Rohit Maiya M** — 1BI24IS131")
    st.markdown("**Sartaj Ahmad S** — DIP 14")
    
    st.markdown("---")
    
    st.markdown("### 👨‍🏫 Guide")
    st.markdown("**Dr. Shilpa M**")
    st.caption("Assistant Professor, ISE Dept")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["🔄 Simulator", "📚 Theory", "💻 Verilog", "📝 About"])

with tab1:
    # FSM Diagram
    st.markdown('<div class="card"><div class="card-header">🔄 Finite State Machine Diagram</div>', unsafe_allow_html=True)
    fsm_html = f'''
    <div style="background: rgba(15, 23, 42, 0.9); border-radius: 12px; padding: 20px; display: flex; justify-content: center;">
        {render_fsm_diagram()}
    </div>
    '''
    components.html(fsm_html, height=360, scrolling=False)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # State Pills
    st.markdown('<div class="card"><div class="card-header">📊 State Overview</div><div class="state-grid">', unsafe_allow_html=True)
    state_html = ""
    for i, s in enumerate(STATES):
        active = "active" if i == st.session_state.state else ""
        state_html += f'<div class="state-pill {active}"><span class="name">{s}</span><span class="id">S{i}</span></div>'
    st.markdown(state_html + '</div></div>', unsafe_allow_html=True)
    
    # Three columns
    c1, c2, c3 = st.columns([1, 1, 1.2])
    
    with c1:
        st.markdown('<div class="card"><div class="card-header">📦 Registers</div><div class="reg-grid">', unsafe_allow_html=True)
        reg_html = ""
        for i, v in enumerate(st.session_state.regs):
            reg_html += f'<div class="reg-item"><div class="reg-label">R{i}</div><div class="reg-value">{v:02X}</div></div>'
        st.markdown(reg_html + '</div></div>', unsafe_allow_html=True)
    
    with c2:
        st.markdown('<div class="card"><div class="card-header">🎛️ Control Signals</div>', unsafe_allow_html=True)
        for sig, val in st.session_state.signals.items():
            is_active = val == 1 or val in ['01', '10']
            active_class = "active" if is_active else ""
            st.markdown(f'<div class="signal-item {active_class}"><span class="signal-name">{sig}</span><span class="signal-badge {active_class}">{val}</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with c3:
        st.markdown('<div class="card"><div class="card-header">📝 Execution Log</div><div class="console">', unsafe_allow_html=True)
        log_html = ""
        for l in st.session_state.logs[-10:]:
            log_html += f'<div class="log-entry {l["t"]}">[{l["c"]:02d}] {l["m"]}</div>'
        if not st.session_state.logs:
            log_html = '<div class="log-entry">Ready to execute...</div>'
        st.markdown(log_html + '</div></div>', unsafe_allow_html=True)
    
    # Waveform
    if st.session_state.waveform:
        st.markdown('<div class="card"><div class="card-header">📈 Signal Waveform</div>', unsafe_allow_html=True)
        st.dataframe(pd.DataFrame(st.session_state.waveform[-10:]), use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        ### 🧠 What is a Control Unit?
        
        The Control Unit is the brain of the processor:
        - **Fetches** instructions from memory
        - **Decodes** the opcode
        - **Generates** control signals
        - **Coordinates** datapath components
        
        ### 🔄 Moore FSM Model
        
        We use a **Moore Machine** where outputs depend only on current state:
        
        | Property | Description |
        |----------|-------------|
        | Outputs | State-based only |
        | Stability | Always stable |
        | Timing | Predictable |
        """)
    with c2:
        st.markdown("""
        ### 📋 Instruction Set
        
        | Opcode | Instruction | Operation |
        |--------|-------------|-----------|
        | 000 | ADD | Rd ← Rs + Rt |
        | 001 | SUB | Rd ← Rs - Rt |
        | 010 | AND | Rd ← Rs & Rt |
        | 011 | OR | Rd ← Rs \\| Rt |
        | 100 | LOAD | Rd ← Memory |
        | 101 | STORE | Memory ← Rs |
        | 110 | BEQ | Branch if equal |
        | 111 | HALT | Stop processor |
        """)

with tab3:
    st.markdown("### 💻 Verilog Control Unit Implementation")
    st.code('''module control_unit (
    input clk, reset, start,
    input [2:0] opcode,
    output reg PCWrite, IRWrite, RegWrite,
    output reg MemRead, MemWrite,
    output reg [1:0] ALUOp
);
    // State encoding
    parameter IDLE=0, FETCH=1, DECODE=2,
              EXE_ALU=3, EXE_MEM=4, WB=6, HALT=7;
    
    reg [2:0] state, next;
    
    // State register
    always @(posedge clk or posedge reset)
        state <= reset ? IDLE : next;
    
    // Next state logic
    always @(*) begin
        case (state)
            IDLE: next = start ? FETCH : IDLE;
            FETCH: next = DECODE;
            DECODE: case (opcode)
                3'b000,3'b001,3'b010,3'b011: next = EXE_ALU;
                3'b100,3'b101: next = EXE_MEM;
                3'b111: next = HALT;
            endcase
            EXE_ALU, EXE_MEM: next = WB;
            WB: next = FETCH;
            HALT: next = HALT;
        endcase
    end
    
    // Moore output logic
    always @(*) begin
        {PCWrite, IRWrite, RegWrite, MemRead, MemWrite} = 0;
        case (state)
            FETCH: {PCWrite, IRWrite, MemRead} = 3'b111;
            EXE_ALU: ALUOp = 2'b10;
            WB: {PCWrite, RegWrite} = 2'b11;
        endcase
    end
endmodule''', language='verilog')

with tab4:
    st.markdown("### ℹ️ About This Project")
    st.markdown("""
    This mini-project demonstrates a **Finite State Machine-based Control Unit** 
    for the DDCO course at **Bangalore Institute of Technology**.
    
    **Key Features:**
    - 8-state Moore FSM
    - 8 instructions (ADD, SUB, AND, OR, LOAD, STORE, BEQ, HALT)
    - Interactive web simulation
    - Complete Verilog HDL implementation
    """)
    
    st.markdown("### 👥 Team Members")
    c1, c2, c3 = st.columns(3)
    team_data = [
        ("Vignesh B S", "1BI24IS187", "⚡", True),
        ("Rohit Maiya M", "1BI24IS131", "💻", False),
        ("Sartaj Ahmad S", "DIP 14", "🔧", False)
    ]
    for col, (name, usn, icon, highlight) in zip([c1,c2,c3], team_data):
        with col:
            highlight_class = "highlighted" if highlight else ""
            st.markdown(f'''<div class="team-member {highlight_class}">
                <div class="icon">{icon}</div>
                <div class="name">{name}</div>
                <div class="usn">{usn}</div>
            </div>''', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("**Project Guide:** Dr. Shilpa M — Assistant Professor, ISE Department")
    st.markdown("**Institution:** Bangalore Institute of Technology • Academic Year 2024-25")

# Initialize
if not st.session_state.logs: 
    reset()
