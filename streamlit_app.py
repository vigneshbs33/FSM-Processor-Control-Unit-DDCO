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

# Fixed Light Theme CSS - Proper text colors
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Fira+Code:wght@400;500&display=swap');
    
    /* Reset and base */
    html, body, [class*="st-"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    
    /* Main app background */
    .stApp {
        background: #f5f7fa !important;
    }
    
    /* Ensure all text is visible - dark text on light background */
    .stApp, .stApp p, .stApp span, .stApp div, .stApp label {
        color: #1f2937 !important;
    }
    
    /* Sidebar styling - ensure visibility */
    section[data-testid="stSidebar"] {
        background: #ffffff !important;
        border-right: 1px solid #e5e7eb !important;
    }
    
    section[data-testid="stSidebar"] * {
        color: #1f2937 !important;
    }
    
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown span,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #1f2937 !important;
    }
    
    /* Header card */
    .header-card {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        padding: 24px 32px;
        border-radius: 16px;
        margin-bottom: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    .header-card h1 {
        color: #ffffff !important;
        font-size: 1.75rem;
        font-weight: 700;
        margin: 0;
    }
    
    .header-card p {
        color: rgba(255, 255, 255, 0.9) !important;
        margin: 8px 0 0 0;
        font-size: 1rem;
    }
    
    /* Content cards */
    .content-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        border: 1px solid #e5e7eb;
    }
    
    .card-title {
        color: #374151 !important;
        font-size: 0.875rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 16px;
        padding-bottom: 8px;
        border-bottom: 2px solid #e5e7eb;
    }
    
    /* State grid */
    .state-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(75px, 1fr));
        gap: 10px;
    }
    
    .state-box {
        background: #f9fafb;
        border: 2px solid #e5e7eb;
        border-radius: 10px;
        padding: 14px 8px;
        text-align: center;
        transition: all 0.2s ease;
    }
    
    .state-box.active {
        background: linear-gradient(135deg, #3b82f6, #1d4ed8);
        border-color: #3b82f6;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.35);
    }
    
    .state-box .name {
        font-size: 0.75rem;
        font-weight: 600;
        color: #374151 !important;
    }
    
    .state-box.active .name {
        color: #ffffff !important;
    }
    
    .state-box .id {
        font-size: 0.65rem;
        color: #9ca3af !important;
        margin-top: 4px;
    }
    
    .state-box.active .id {
        color: rgba(255, 255, 255, 0.85) !important;
    }
    
    /* Register display */
    .reg-container {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 10px;
    }
    
    .reg-box {
        background: #f9fafb;
        border-radius: 10px;
        padding: 14px;
        text-align: center;
        border: 1px solid #e5e7eb;
    }
    
    .reg-label {
        font-size: 0.75rem;
        color: #6b7280 !important;
        font-weight: 500;
    }
    
    .reg-value {
        font-family: 'Fira Code', monospace;
        font-size: 1.5rem;
        font-weight: 600;
        color: #3b82f6 !important;
        margin-top: 4px;
    }
    
    /* Signal rows */
    .signal-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 14px;
        background: #f9fafb;
        border-radius: 8px;
        margin-bottom: 6px;
        border-left: 4px solid #e5e7eb;
    }
    
    .signal-row.high {
        border-left-color: #10b981;
        background: #ecfdf5;
    }
    
    .signal-name {
        font-family: 'Fira Code', monospace;
        font-size: 0.85rem;
        color: #374151 !important;
    }
    
    .signal-value {
        font-family: 'Fira Code', monospace;
        font-size: 0.85rem;
        font-weight: 600;
        padding: 3px 10px;
        border-radius: 6px;
        background: #e5e7eb;
        color: #6b7280 !important;
    }
    
    .signal-value.high {
        background: #10b981;
        color: #ffffff !important;
    }
    
    /* Console log */
    .console-box {
        background: #1f2937;
        border-radius: 10px;
        padding: 14px;
        font-family: 'Fira Code', monospace;
        font-size: 0.8rem;
        max-height: 200px;
        overflow-y: auto;
    }
    
    .log-line {
        padding: 4px 0;
        color: #9ca3af !important;
    }
    
    .log-info { color: #60a5fa !important; }
    .log-success { color: #34d399 !important; }
    .log-warning { color: #fbbf24 !important; }
    
    /* Team cards */
    .team-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 24px;
        text-align: center;
        border: 1px solid #e5e7eb;
        transition: all 0.2s ease;
    }
    
    .team-card:hover {
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
        transform: translateY(-4px);
    }
    
    .team-card .icon { font-size: 2.5rem; margin-bottom: 12px; }
    .team-card .name { font-weight: 600; color: #1f2937 !important; font-size: 1rem; }
    .team-card .usn { color: #6b7280 !important; font-size: 0.875rem; margin-top: 6px; }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        padding: 10px 20px !important;
        font-size: 0.9rem !important;
        box-shadow: 0 4px 6px rgba(79, 70, 229, 0.25) !important;
        transition: all 0.2s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 12px rgba(79, 70, 229, 0.35) !important;
    }
    
    /* Status badge */
    .status-badge {
        display: inline-block;
        padding: 8px 20px;
        border-radius: 25px;
        font-size: 0.9rem;
        font-weight: 600;
        background: #dbeafe;
        color: #1e40af !important;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-family: 'Fira Code', monospace !important;
        color: #4f46e5 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #6b7280 !important;
    }
    
    /* Selectbox */
    .stSelectbox label {
        color: #374151 !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: #ffffff;
        padding: 8px;
        border-radius: 12px;
        gap: 8px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px !important;
        color: #4b5563 !important;
        font-weight: 500 !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: #4f46e5 !important;
        color: #ffffff !important;
    }
    
    /* Tables */
    .stDataFrame {
        background: #ffffff !important;
    }
    
    /* Markdown text */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #1f2937 !important;
    }
    
    .stMarkdown p, .stMarkdown li {
        color: #374151 !important;
    }
    
    /* Caption text */
    .stCaption, small {
        color: #6b7280 !important;
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
        log(f"{name} done", 'success')
    nxt = next_state(op)
    if nxt == 7 and st.session_state.state != 7:
        log("HALTED", 'warning')
    st.session_state.state = nxt
    st.session_state.cycle += 1

# FSM Diagram SVG - Clean with visible text
def fsm_svg():
    c = st.session_state.state
    fill = lambda i: "#4f46e5" if i == c else "#f3f4f6"
    stroke = lambda i: "#4f46e5" if i == c else "#d1d5db"
    txt = lambda i: "#ffffff" if i == c else "#374151"
    
    return f'''
    <div style="background: #ffffff; border-radius: 12px; padding: 20px; border: 1px solid #e5e7eb; overflow-x: auto;">
        <svg viewBox="0 0 620 300" style="width: 100%; min-width: 480px; height: auto;">
            <defs>
                <marker id="arr" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
                    <polygon points="0 0, 8 3, 0 6" fill="#9ca3af"/>
                </marker>
            </defs>
            
            <!-- Arrows -->
            <path d="M 310 50 L 160 85" fill="none" stroke="#d1d5db" stroke-width="1.5" marker-end="url(#arr)"/>
            <path d="M 160 125 L 460 125" fill="none" stroke="#d1d5db" stroke-width="1.5" marker-end="url(#arr)"/>
            <path d="M 440 145 L 90 180" fill="none" stroke="#d1d5db" stroke-width="1.5" marker-end="url(#arr)"/>
            <path d="M 460 145 L 230 180" fill="none" stroke="#d1d5db" stroke-width="1.5" marker-end="url(#arr)"/>
            <path d="M 480 145 L 360 180" fill="none" stroke="#d1d5db" stroke-width="1.5" marker-end="url(#arr)"/>
            <path d="M 500 145 L 530 180" fill="none" stroke="#d1d5db" stroke-width="1.5" marker-end="url(#arr)"/>
            <path d="M 90 240 L 280 265" fill="none" stroke="#d1d5db" stroke-width="1.5" marker-end="url(#arr)"/>
            <path d="M 230 240 L 295 265" fill="none" stroke="#d1d5db" stroke-width="1.5" marker-end="url(#arr)"/>
            <path d="M 360 240 L 320 265" fill="none" stroke="#d1d5db" stroke-width="1.5" marker-end="url(#arr)"/>
            <path d="M 265 280 Q 50 250 140 145" fill="none" stroke="#d1d5db" stroke-width="1.5" stroke-dasharray="4,2" marker-end="url(#arr)"/>
            
            <!-- Labels -->
            <text x="225" y="60" fill="#6b7280" font-size="9" font-family="Inter, sans-serif">start</text>
            <text x="295" y="115" fill="#6b7280" font-size="8" font-family="Inter, sans-serif">always</text>
            <text x="230" y="165" fill="#6b7280" font-size="8" font-family="Inter, sans-serif">ALU</text>
            <text x="320" y="165" fill="#6b7280" font-size="8" font-family="Inter, sans-serif">MEM</text>
            <text x="410" y="165" fill="#6b7280" font-size="8" font-family="Inter, sans-serif">BR</text>
            <text x="505" y="165" fill="#6b7280" font-size="8" font-family="Inter, sans-serif">HALT</text>
            <text x="70" y="260" fill="#6b7280" font-size="8" font-family="Inter, sans-serif">loop</text>
            
            <!-- States -->
            <circle cx="310" cy="30" r="26" fill="{fill(0)}" stroke="{stroke(0)}" stroke-width="2"/>
            <text x="310" y="34" fill="{txt(0)}" font-size="10" font-weight="600" text-anchor="middle" font-family="Inter, sans-serif">IDLE</text>
            
            <circle cx="140" cy="110" r="26" fill="{fill(1)}" stroke="{stroke(1)}" stroke-width="2"/>
            <text x="140" y="114" fill="{txt(1)}" font-size="10" font-weight="600" text-anchor="middle" font-family="Inter, sans-serif">FETCH</text>
            
            <circle cx="480" cy="110" r="26" fill="{fill(2)}" stroke="{stroke(2)}" stroke-width="2"/>
            <text x="480" y="114" fill="{txt(2)}" font-size="9" font-weight="600" text-anchor="middle" font-family="Inter, sans-serif">DECODE</text>
            
            <circle cx="70" cy="210" r="26" fill="{fill(3)}" stroke="{stroke(3)}" stroke-width="2"/>
            <text x="70" y="214" fill="{txt(3)}" font-size="8" font-weight="600" text-anchor="middle" font-family="Inter, sans-serif">EXE_ALU</text>
            
            <circle cx="210" cy="210" r="26" fill="{fill(4)}" stroke="{stroke(4)}" stroke-width="2"/>
            <text x="210" y="214" fill="{txt(4)}" font-size="8" font-weight="600" text-anchor="middle" font-family="Inter, sans-serif">EXE_MEM</text>
            
            <circle cx="350" cy="210" r="26" fill="{fill(5)}" stroke="{stroke(5)}" stroke-width="2"/>
            <text x="350" y="214" fill="{txt(5)}" font-size="8" font-weight="600" text-anchor="middle" font-family="Inter, sans-serif">EXE_BR</text>
            
            <circle cx="530" cy="210" r="26" fill="{fill(7)}" stroke="{'#f59e0b' if c==7 else '#d1d5db'}" stroke-width="2"/>
            <text x="530" y="214" fill="{txt(7)}" font-size="10" font-weight="600" text-anchor="middle" font-family="Inter, sans-serif">HALT</text>
            
            <circle cx="300" cy="280" r="26" fill="{fill(6)}" stroke="{stroke(6)}" stroke-width="2"/>
            <text x="300" y="284" fill="{txt(6)}" font-size="10" font-weight="600" text-anchor="middle" font-family="Inter, sans-serif">WB</text>
        </svg>
    </div>
    '''

# ==================== UI ====================

# Header
st.markdown("""
<div class="header-card">
    <h1>⚙️ FSM Processor Control Unit</h1>
    <p>Interactive Finite State Machine Simulator • DDCO Mini Project</p>
</div>
""", unsafe_allow_html=True)

# Sidebar - Always visible
with st.sidebar:
    st.markdown("### 🎛️ Control Panel")
    
    instr = st.selectbox("Select Instruction", list(INSTR.keys()), format_func=lambda x: f"{x} ({INSTR[x]})")
    op = INSTR[instr]
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("⏭️ Step", use_container_width=True): step(op)
    with c2:
        if st.button("🔄 Reset", use_container_width=True): reset()
    
    if st.button("▶️ Run Full Cycle", use_container_width=True):
        for _ in range(6):
            if st.session_state.state != 7: step(op)
    
    st.markdown("---")
    
    st.markdown("### 📊 Processor Status")
    c1, c2 = st.columns(2)
    c1.metric("Cycles", st.session_state.cycle)
    c2.metric("PC", f"0x{st.session_state.pc:02X}")
    
    st.markdown(f'''<div style="text-align:center; margin:12px 0;">
        <span class="status-badge">{STATES[st.session_state.state]}</span>
    </div>''', unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 👥 Team Members")
    st.markdown("**Vignesh B S** — 1BI24IS187")
    st.markdown("**Rohit Maiya M** — 1BI24IS131")
    st.markdown("**Sartaj Ahmad S** — DIP 14")
    
    st.markdown("---")
    
    st.markdown("### 👨‍🏫 Project Guide")
    st.markdown("**Dr. Shilpa M**")
    st.caption("Assistant Professor, ISE Dept")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["🔄 Simulator", "📚 Theory", "💻 Verilog Code", "📝 About"])

with tab1:
    # FSM Diagram
    st.markdown('<div class="content-card"><div class="card-title">🔄 Finite State Machine Diagram</div>', unsafe_allow_html=True)
    components.html(fsm_svg(), height=340, scrolling=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # States
    st.markdown('<div class="content-card"><div class="card-title">📊 State Overview</div><div class="state-grid">', unsafe_allow_html=True)
    state_html = ""
    for i, s in enumerate(STATES):
        active = "active" if i == st.session_state.state else ""
        state_html += f'<div class="state-box {active}"><div class="name">{s}</div><div class="id">S{i}</div></div>'
    st.markdown(state_html + '</div></div>', unsafe_allow_html=True)
    
    # Three columns
    c1, c2, c3 = st.columns([1, 1, 1.3])
    
    with c1:
        st.markdown('<div class="content-card"><div class="card-title">📦 Registers</div><div class="reg-container">', unsafe_allow_html=True)
        reg_html = ""
        for i, v in enumerate(st.session_state.regs):
            reg_html += f'<div class="reg-box"><div class="reg-label">R{i}</div><div class="reg-value">{v:02X}</div></div>'
        st.markdown(reg_html + '</div></div>', unsafe_allow_html=True)
    
    with c2:
        st.markdown('<div class="content-card"><div class="card-title">🎛️ Control Signals</div>', unsafe_allow_html=True)
        for sig, val in st.session_state.signals.items():
            is_high = val == 1 or val in ['01', '10']
            high_class = "high" if is_high else ""
            st.markdown(f'<div class="signal-row {high_class}"><span class="signal-name">{sig}</span><span class="signal-value {high_class}">{val}</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with c3:
        st.markdown('<div class="content-card"><div class="card-title">📝 Execution Log</div><div class="console-box">', unsafe_allow_html=True)
        log_html = ""
        for l in st.session_state.logs[-10:]:
            log_html += f'<div class="log-line log-{l["t"]}">[{l["c"]:02d}] {l["m"]}</div>'
        if not st.session_state.logs:
            log_html = '<div class="log-line">Ready to execute...</div>'
        st.markdown(log_html + '</div></div>', unsafe_allow_html=True)
    
    # Waveform
    if st.session_state.waveform:
        st.markdown('<div class="content-card"><div class="card-title">📈 Signal Waveform</div>', unsafe_allow_html=True)
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
    st.markdown("### Verilog Control Unit Implementation")
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
    st.markdown("### About This Project")
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
    for col, (name, usn, icon) in zip([c1,c2,c3], [
        ("Vignesh B S", "1BI24IS187", "🎯"),
        ("Rohit Maiya M", "1BI24IS131", "💻"),
        ("Sartaj Ahmad S", "DIP 14", "🔧")
    ]):
        with col:
            st.markdown(f'''<div class="team-card">
                <div class="icon">{icon}</div>
                <div class="name">{name}</div>
                <div class="usn">{usn}</div>
            </div>''', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("**Project Guide:** Dr. Shilpa M — Assistant Professor, ISE Department")
    st.markdown("**Institution:** Bangalore Institute of Technology • Academic Year 2024-25")

# Initialize
if not st.session_state.logs: reset()
