import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="FSM Processor Control Unit",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Clean, Professional CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    .stApp {
        background: #0e1117;
    }
    
    /* Header */
    .main-header {
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
        padding: 2rem 2.5rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px rgba(59, 130, 246, 0.25);
    }
    
    .main-header h1 {
        color: white;
        font-size: 1.75rem;
        font-weight: 700;
        margin: 0;
    }
    
    .main-header p {
        color: rgba(255,255,255,0.85);
        margin: 0.5rem 0 0 0;
        font-size: 0.95rem;
    }
    
    /* Cards */
    .card {
        background: #1a1f2e;
        border-radius: 12px;
        padding: 1.25rem;
        border: 1px solid #2d3548;
    }
    
    .card-header {
        color: #94a3b8;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 1rem;
    }
    
    /* State Grid */
    .state-grid {
        display: grid;
        grid-template-columns: repeat(8, 1fr);
        gap: 8px;
    }
    
    .state-box {
        background: #1e2433;
        border: 2px solid #2d3548;
        border-radius: 10px;
        padding: 12px 8px;
        text-align: center;
        transition: all 0.2s ease;
    }
    
    .state-box.active {
        background: linear-gradient(135deg, #10b981, #3b82f6);
        border-color: #10b981;
        transform: scale(1.02);
        box-shadow: 0 0 20px rgba(16, 185, 129, 0.3);
    }
    
    .state-box .name {
        color: #e2e8f0;
        font-size: 0.7rem;
        font-weight: 600;
    }
    
    .state-box.active .name {
        color: white;
    }
    
    .state-box .id {
        color: #64748b;
        font-size: 0.6rem;
        margin-top: 2px;
    }
    
    .state-box.active .id {
        color: rgba(255,255,255,0.8);
    }
    
    /* Registers */
    .reg-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 10px;
    }
    
    .reg-box {
        background: #1e2433;
        border-radius: 10px;
        padding: 14px;
        text-align: center;
        border: 1px solid #2d3548;
    }
    
    .reg-label {
        color: #64748b;
        font-size: 0.7rem;
        font-weight: 500;
    }
    
    .reg-value {
        color: #3b82f6;
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.5rem;
        font-weight: 600;
        margin-top: 4px;
    }
    
    /* Signals */
    .signal-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 12px;
        background: #1e2433;
        border-radius: 8px;
        margin-bottom: 6px;
        border-left: 3px solid #2d3548;
    }
    
    .signal-row.active {
        border-left-color: #10b981;
        background: rgba(16, 185, 129, 0.1);
    }
    
    .signal-name {
        color: #94a3b8;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
    }
    
    .signal-val {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        padding: 3px 10px;
        border-radius: 4px;
        background: #0e1117;
        color: #64748b;
    }
    
    .signal-val.high {
        background: #10b981;
        color: white;
    }
    
    /* Console */
    .console {
        background: #0a0d12;
        border-radius: 8px;
        padding: 12px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        max-height: 200px;
        overflow-y: auto;
        border: 1px solid #1e2433;
    }
    
    .log-line { padding: 3px 0; color: #64748b; }
    .log-info { color: #3b82f6; }
    .log-success { color: #10b981; }
    .log-warning { color: #f59e0b; }
    
    /* Team */
    .team-box {
        background: #1e2433;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        border: 1px solid #2d3548;
        transition: transform 0.2s ease;
    }
    
    .team-box:hover {
        transform: translateY(-2px);
    }
    
    .team-box .icon { font-size: 2.5rem; margin-bottom: 10px; }
    .team-box .name { color: #e2e8f0; font-weight: 600; font-size: 0.95rem; }
    .team-box .usn { color: #64748b; font-size: 0.8rem; margin-top: 4px; }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6, #8b5cf6) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 0.6rem 1rem !important;
        transition: all 0.2s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.35) !important;
    }
    
    /* Metrics in sidebar */
    [data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', monospace;
        color: #3b82f6;
    }
    
    /* Section titles */
    .section-title {
        color: #e2e8f0;
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    /* Table styling */
    .dataframe {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.8rem !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_state' not in st.session_state:
    st.session_state.current_state = 0
if 'cycle' not in st.session_state:
    st.session_state.cycle = 0
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'registers' not in st.session_state:
    st.session_state.registers = [15, 25, 0, 0]
if 'pc' not in st.session_state:
    st.session_state.pc = 0
if 'signals' not in st.session_state:
    st.session_state.signals = {'PCWrite': 0, 'IRWrite': 0, 'MemRead': 0, 'MemWrite': 0, 'RegWrite': 0, 'ALUOp': '00'}
if 'waveform_data' not in st.session_state:
    st.session_state.waveform_data = []

# Constants
STATES = ['IDLE', 'FETCH', 'DECODE', 'EXE_ALU', 'EXE_MEM', 'EXE_BR', 'WB', 'HALT']
INSTRUCTIONS = {'ADD': '000', 'SUB': '001', 'AND': '010', 'OR': '011', 'LOAD': '100', 'STORE': '101', 'BEQ': '110', 'HALT': '111'}

def add_log(msg, t='info'):
    st.session_state.logs.append({'cycle': st.session_state.cycle, 'msg': msg, 'type': t})

def reset():
    st.session_state.current_state = 0
    st.session_state.cycle = 0
    st.session_state.logs = []
    st.session_state.registers = [15, 25, 0, 0]
    st.session_state.pc = 0
    st.session_state.signals = {'PCWrite': 0, 'IRWrite': 0, 'MemRead': 0, 'MemWrite': 0, 'RegWrite': 0, 'ALUOp': '00'}
    st.session_state.waveform_data = []
    add_log("Processor reset", 'success')

def get_next(op):
    s = st.session_state.current_state
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

def apply_signals(op):
    st.session_state.signals = {'PCWrite': 0, 'IRWrite': 0, 'MemRead': 0, 'MemWrite': 0, 'RegWrite': 0, 'ALUOp': '00'}
    s = st.session_state.current_state
    if s == 1:
        st.session_state.signals.update({'MemRead': 1, 'IRWrite': 1, 'PCWrite': 1})
        st.session_state.pc += 1
    elif s == 3:
        st.session_state.signals['ALUOp'] = '10'
        r = st.session_state.registers
        if op == '000': r[2] = (r[0] + r[1]) & 0xFF
        elif op == '001': r[2] = (r[0] - r[1]) & 0xFF
        elif op == '010': r[2] = r[0] & r[1]
        elif op == '011': r[2] = r[0] | r[1]
    elif s == 4:
        if op == '100':
            st.session_state.signals['MemRead'] = 1
            st.session_state.registers[0] = 42
        else:
            st.session_state.signals['MemWrite'] = 1
    elif s == 5:
        st.session_state.signals['ALUOp'] = '01'
    elif s == 6:
        if op not in ['101','110','111']:
            st.session_state.signals['RegWrite'] = 1
        st.session_state.signals['PCWrite'] = 1
    
    st.session_state.waveform_data.append({
        'Cycle': st.session_state.cycle,
        'State': STATES[s],
        'PCWrite': st.session_state.signals['PCWrite'],
        'MemRead': st.session_state.signals['MemRead'],
        'RegWrite': st.session_state.signals['RegWrite']
    })

def step(op):
    name = [k for k,v in INSTRUCTIONS.items() if v == op][0]
    add_log(f"{STATES[st.session_state.current_state]} → {name}")
    apply_signals(op)
    if st.session_state.current_state == 6:
        add_log(f"{name} done", 'success')
    nxt = get_next(op)
    if nxt == 7 and st.session_state.current_state != 7:
        add_log("HALTED", 'warning')
    st.session_state.current_state = nxt
    st.session_state.cycle += 1

# FSM Diagram Component
def fsm_diagram_html():
    current = st.session_state.current_state
    return f'''
    <div style="background: #1a1f2e; border-radius: 16px; padding: 20px; border: 1px solid #2d3548;">
        <svg viewBox="0 0 700 380" style="width: 100%; height: auto;">
            <defs>
                <marker id="arrow" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
                    <polygon points="0 0, 8 3, 0 6" fill="#4b5563"/>
                </marker>
                <linearGradient id="activeGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:#10b981"/>
                    <stop offset="100%" style="stop-color:#3b82f6"/>
                </linearGradient>
            </defs>
            
            <!-- Arrows -->
            <path d="M 350 70 L 200 120" fill="none" stroke="#4b5563" stroke-width="1.5" marker-end="url(#arrow)"/>
            <path d="M 200 160 L 350 160 L 500 160" fill="none" stroke="#4b5563" stroke-width="1.5" marker-end="url(#arrow)"/>
            <path d="M 480 180 L 120 230" fill="none" stroke="#4b5563" stroke-width="1.5" marker-end="url(#arrow)"/>
            <path d="M 500 180 L 280 230" fill="none" stroke="#4b5563" stroke-width="1.5" marker-end="url(#arrow)"/>
            <path d="M 520 180 L 420 230" fill="none" stroke="#4b5563" stroke-width="1.5" marker-end="url(#arrow)"/>
            <path d="M 540 180 L 580 230" fill="none" stroke="#4b5563" stroke-width="1.5" marker-end="url(#arrow)"/>
            <path d="M 120 290 L 320 330" fill="none" stroke="#4b5563" stroke-width="1.5" marker-end="url(#arrow)"/>
            <path d="M 280 290 L 340 330" fill="none" stroke="#4b5563" stroke-width="1.5" marker-end="url(#arrow)"/>
            <path d="M 420 290 L 370 330" fill="none" stroke="#4b5563" stroke-width="1.5" marker-end="url(#arrow)"/>
            <path d="M 300 350 Q 80 300 180 180" fill="none" stroke="#4b5563" stroke-width="1.5" stroke-dasharray="4,2" marker-end="url(#arrow)"/>
            
            <!-- State: IDLE -->
            <circle cx="350" cy="50" r="35" fill="{'url(#activeGrad)' if current==0 else '#1e2433'}" stroke="{'#10b981' if current==0 else '#2d3548'}" stroke-width="2"/>
            <text x="350" y="50" fill="{'white' if current==0 else '#94a3b8'}" font-size="11" font-weight="600" text-anchor="middle" dominant-baseline="middle">IDLE</text>
            
            <!-- State: FETCH -->
            <circle cx="180" cy="150" r="35" fill="{'url(#activeGrad)' if current==1 else '#1e2433'}" stroke="{'#10b981' if current==1 else '#2d3548'}" stroke-width="2"/>
            <text x="180" y="150" fill="{'white' if current==1 else '#94a3b8'}" font-size="11" font-weight="600" text-anchor="middle" dominant-baseline="middle">FETCH</text>
            
            <!-- State: DECODE -->
            <circle cx="520" cy="150" r="35" fill="{'url(#activeGrad)' if current==2 else '#1e2433'}" stroke="{'#10b981' if current==2 else '#2d3548'}" stroke-width="2"/>
            <text x="520" y="150" fill="{'white' if current==2 else '#94a3b8'}" font-size="10" font-weight="600" text-anchor="middle" dominant-baseline="middle">DECODE</text>
            
            <!-- State: EXE_ALU -->
            <circle cx="100" cy="260" r="35" fill="{'url(#activeGrad)' if current==3 else '#1e2433'}" stroke="{'#10b981' if current==3 else '#2d3548'}" stroke-width="2"/>
            <text x="100" y="260" fill="{'white' if current==3 else '#94a3b8'}" font-size="9" font-weight="600" text-anchor="middle" dominant-baseline="middle">EXE_ALU</text>
            
            <!-- State: EXE_MEM -->
            <circle cx="260" cy="260" r="35" fill="{'url(#activeGrad)' if current==4 else '#1e2433'}" stroke="{'#10b981' if current==4 else '#2d3548'}" stroke-width="2"/>
            <text x="260" y="260" fill="{'white' if current==4 else '#94a3b8'}" font-size="9" font-weight="600" text-anchor="middle" dominant-baseline="middle">EXE_MEM</text>
            
            <!-- State: EXE_BR -->
            <circle cx="420" cy="260" r="35" fill="{'url(#activeGrad)' if current==5 else '#1e2433'}" stroke="{'#10b981' if current==5 else '#2d3548'}" stroke-width="2"/>
            <text x="420" y="260" fill="{'white' if current==5 else '#94a3b8'}" font-size="9" font-weight="600" text-anchor="middle" dominant-baseline="middle">EXE_BR</text>
            
            <!-- State: HALT -->
            <circle cx="580" cy="260" r="35" fill="{'url(#activeGrad)' if current==7 else '#1e2433'}" stroke="{'#f59e0b' if current==7 else '#2d3548'}" stroke-width="2"/>
            <text x="580" y="260" fill="{'white' if current==7 else '#94a3b8'}" font-size="11" font-weight="600" text-anchor="middle" dominant-baseline="middle">HALT</text>
            
            <!-- State: WRITEBACK -->
            <circle cx="350" cy="350" r="35" fill="{'url(#activeGrad)' if current==6 else '#1e2433'}" stroke="{'#10b981' if current==6 else '#2d3548'}" stroke-width="2"/>
            <text x="350" y="350" fill="{'white' if current==6 else '#94a3b8'}" font-size="10" font-weight="600" text-anchor="middle" dominant-baseline="middle">WB</text>
            
            <!-- Labels -->
            <text x="270" y="95" fill="#64748b" font-size="8">start</text>
            <text x="340" y="145" fill="#64748b" font-size="8">always</text>
            <text x="280" y="205" fill="#64748b" font-size="7">ALU</text>
            <text x="370" y="205" fill="#64748b" font-size="7">MEM</text>
            <text x="460" y="205" fill="#64748b" font-size="7">BR</text>
            <text x="560" y="205" fill="#64748b" font-size="7">HALT</text>
            <text x="120" y="305" fill="#64748b" font-size="7">loop</text>
        </svg>
    </div>
    '''

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
    
    instruction = st.selectbox("Instruction", list(INSTRUCTIONS.keys()), format_func=lambda x: f"{x} ({INSTRUCTIONS[x]})")
    opcode = INSTRUCTIONS[instruction]
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("⏭️ Step", use_container_width=True): step(opcode)
    with c2:
        if st.button("🔄 Reset", use_container_width=True): reset()
    
    if st.button("▶️ Run Full Cycle", use_container_width=True):
        for _ in range(6):
            if st.session_state.current_state != 7: step(opcode)
    
    st.markdown("---")
    st.markdown("### 📊 Status")
    c1, c2 = st.columns(2)
    c1.metric("Cycles", st.session_state.cycle)
    c2.metric("PC", f"0x{st.session_state.pc:02X}")
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #3b82f6, #8b5cf6); padding: 12px; border-radius: 8px; text-align: center; margin-top: 10px;">
        <div style="color: rgba(255,255,255,0.8); font-size: 0.7rem;">Current State</div>
        <div style="color: white; font-size: 1.1rem; font-weight: 700;">{STATES[st.session_state.current_state]}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 👥 Team")
    st.caption("**Vignesh B S** • 1BI24IS187")
    st.caption("**Rohit Maiya M** • 1BI24IS131")
    st.caption("**Sartaj Ahmad S** • DIP 14")
    st.markdown("---")
    st.caption("**Guide:** Dr. Shilpa M")
    st.caption("ISE Department")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["🔄 Simulator", "📚 Theory", "💻 Code", "📝 About"])

with tab1:
    # FSM Diagram
    st.markdown('<div class="section-title">🔄 FSM State Diagram</div>', unsafe_allow_html=True)
    components.html(fsm_diagram_html(), height=420)
    
    # State boxes
    st.markdown('<div class="section-title">📊 States</div>', unsafe_allow_html=True)
    state_html = '<div class="state-grid">'
    for i, s in enumerate(STATES):
        active = "active" if i == st.session_state.current_state else ""
        state_html += f'<div class="state-box {active}"><div class="name">{s}</div><div class="id">S{i}</div></div>'
    state_html += '</div>'
    st.markdown(state_html, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Three columns
    c1, c2, c3 = st.columns([1, 1, 1.5])
    
    with c1:
        st.markdown('<div class="section-title">📦 Registers</div>', unsafe_allow_html=True)
        reg_html = '<div class="reg-grid">'
        for i, v in enumerate(st.session_state.registers):
            reg_html += f'<div class="reg-box"><div class="reg-label">R{i}</div><div class="reg-value">{v:02X}</div></div>'
        reg_html += '</div>'
        st.markdown(reg_html, unsafe_allow_html=True)
    
    with c2:
        st.markdown('<div class="section-title">🎛️ Signals</div>', unsafe_allow_html=True)
        for sig, val in st.session_state.signals.items():
            is_high = val == 1 or val in ['01', '10']
            active = "active" if is_high else ""
            high = "high" if is_high else ""
            st.markdown(f'''<div class="signal-row {active}">
                <span class="signal-name">{sig}</span>
                <span class="signal-val {high}">{val}</span>
            </div>''', unsafe_allow_html=True)
    
    with c3:
        st.markdown('<div class="section-title">📝 Log</div>', unsafe_allow_html=True)
        log_html = '<div class="console">'
        for l in st.session_state.logs[-10:]:
            log_html += f'<div class="log-line log-{l["type"]}">[{l["cycle"]:02d}] {l["msg"]}</div>'
        if not st.session_state.logs:
            log_html += '<div class="log-line">Ready...</div>'
        log_html += '</div>'
        st.markdown(log_html, unsafe_allow_html=True)
    
    # Waveform
    if st.session_state.waveform_data:
        st.markdown('<div class="section-title">📈 Waveform</div>', unsafe_allow_html=True)
        st.dataframe(pd.DataFrame(st.session_state.waveform_data[-10:]), use_container_width=True, hide_index=True)

with tab2:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        ### 🧠 Control Unit
        The Control Unit orchestrates instruction execution by:
        - **Fetching** instructions from memory
        - **Decoding** the opcode
        - **Generating** control signals
        - **Coordinating** datapath components
        
        ### 🔄 FSM Approach
        We use a **Moore Machine** where outputs depend only on current state:
        
        | Property | Moore | Mealy |
        |----------|-------|-------|
        | Outputs | State only | State + Input |
        | Stability | Stable | May glitch |
        """)
    with c2:
        st.markdown("""
        ### 📋 Instruction Set
        
        | Op | Instr | Operation |
        |----|-------|-----------|
        | 000 | ADD | Rd ← Rs + Rt |
        | 001 | SUB | Rd ← Rs - Rt |
        | 010 | AND | Rd ← Rs & Rt |
        | 011 | OR | Rd ← Rs \\| Rt |
        | 100 | LOAD | Rd ← Mem |
        | 101 | STORE | Mem ← Rs |
        | 110 | BEQ | Branch |
        | 111 | HALT | Stop |
        """)

with tab3:
    st.code('''module control_unit (
    input clk, reset, start,
    input [2:0] opcode,
    output reg PCWrite, IRWrite, RegWrite,
    output reg MemRead, MemWrite,
    output reg [1:0] ALUOp
);
    parameter IDLE=0, FETCH=1, DECODE=2, 
              EXE_ALU=3, EXE_MEM=4, WB=6, HALT=7;
    
    reg [2:0] state, next;
    
    always @(posedge clk or posedge reset)
        state <= reset ? IDLE : next;
    
    always @(*) begin
        case (state)
            IDLE: next = start ? FETCH : IDLE;
            FETCH: next = DECODE;
            DECODE: case (opcode)
                3'b000,3'b001,3'b010,3'b011: next = EXE_ALU;
                3'b100,3'b101: next = EXE_MEM;
                3'b111: next = HALT;
                default: next = FETCH;
            endcase
            EXE_ALU,EXE_MEM: next = WB;
            WB: next = FETCH;
            HALT: next = HALT;
        endcase
    end
    
    always @(*) begin
        {PCWrite,IRWrite,RegWrite,MemRead,MemWrite} = 0;
        case (state)
            FETCH: {PCWrite,IRWrite,MemRead} = 3'b111;
            EXE_ALU: ALUOp = 2'b10;
            WB: {PCWrite,RegWrite} = 2'b11;
        endcase
    end
endmodule''', language='verilog')

with tab4:
    st.markdown("### 📝 About")
    st.markdown("""
    This project demonstrates a **Finite State Machine-based Control Unit** 
    for the DDCO course at Bangalore Institute of Technology.
    
    **Features:** 8-state FSM • 8 instructions • Interactive simulation • Verilog code
    """)
    
    st.markdown("### 👥 Team")
    c1, c2, c3 = st.columns(3)
    for col, (name, usn, icon) in zip([c1,c2,c3], [
        ("Vignesh B S", "1BI24IS187", "🎯"),
        ("Rohit Maiya M", "1BI24IS131", "💻"),
        ("Sartaj Ahmad S", "DIP 14", "🔧")
    ]):
        with col:
            st.markdown(f'''<div class="team-box">
                <div class="icon">{icon}</div>
                <div class="name">{name}</div>
                <div class="usn">{usn}</div>
            </div>''', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("**Guide:** Dr. Shilpa M • ISE Department")

# Init
if not st.session_state.logs: reset()
