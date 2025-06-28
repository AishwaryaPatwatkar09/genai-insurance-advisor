# ==============================================
# Enhanced GenAI Insurance Advisor - phi3:mini Version (Fast)
# ==============================================

import streamlit as st
import time
import json
from datetime import datetime
import asyncio
from concurrent.futures import ThreadPoolExecutor

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
import io

import os
# Disable Ollama in cloud environment
OLLAMA_AVAILABLE = False

# Try to import ollama, with fallback
try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    st.warning("⚠️ Ollama not installed. Install with: pip install ollama")

# ----------------------- 
# 1. PERFORMANCE OPTIMIZATIONS
# ----------------------- 

# Cache configuration and static data
@st.cache_data
def get_static_config():
    """Cache static configuration data"""
    return {
        'occupations': [
            "Farmer", "Driver", "Teacher", "Shopkeeper", 
            "Labor Worker", "Government Employee", "Self Employed",
            "Private Employee", "Student", "Retired", "Other"
        ],
        'income_brackets': [
            "₹0-5,000", "₹5,000-10,000", "₹10,000-15,000",
            "₹15,000-25,000", "₹25,000-50,000", "₹50,000+"
        ],
        'income_map': {
            "₹0-5,000": 2500,
            "₹5,000-10,000": 7500,
            "₹10,000-15,000": 12500,
            "₹15,000-25,000": 20000,
            "₹25,000-50,000": 37500,
            "₹50,000+": 75000
        },
        'family_sizes': ["1", "2-3", "4-5", "6+"],
        'health_status': ["Excellent", "Good", "Fair", "Have medical conditions", "Prefer not to say"],
        'financial_goals': [
            "Basic Protection", "Family Security", "Health Coverage",
            "Retirement Planning", "Child Education", "Wealth Building"
        ],
        'risk_levels': ["Conservative", "Moderate", "Aggressive"],
        'claim_types': [
            "Accident Claim (PMSBY)",
            "Life Insurance Claim (PMJJBY)", 
            "Health Insurance Claim (PMJAY)",
            "Other Government Scheme"
        ]
    }

# Cache expensive computations
@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_cached_fallback_advice(age, job, income, location):
    """Cache fallback advice to avoid regeneration"""
    return f"""
## 🛡️ Smart Insurance Recommendations

**Your Profile:** {age} years, {job}, ₹{income}/month, {location}

### Essential Coverage Portfolio:

**1. PMSBY - Accident Shield (₹20/year) 🚨**
- India's cheapest accident insurance
- ₹2 lakh coverage for workplace/travel accidents
- Must-have for all working individuals

**2. PMJJBY - Family Protection (₹436/year) 👨‍👩‍👧‍👦**
- ₹2 lakh life insurance coverage
- Automatic premium deduction
- Ideal for families with children

**3. PMJAY - Free Healthcare (₹0/year) 🏥**
- Completely FREE for eligible families
- ₹5 lakh hospitalization coverage
- Covers 1,400+ procedures

**4. State Health Insurance 🏥**
- Check your state's specific schemes
- Often provides additional coverage
- May cover outpatient treatments

### Quick Action Steps:
1. **Today:** Check PMJAY eligibility online
2. **This week:** Visit nearest bank with Aadhaar
3. **Apply for:** PMSBY first (lowest cost, high value)

**Your Total Protection Cost: ₹456/year for complete family coverage!**
"""

# ----------------------- 
# 2. Configuration
# ----------------------- 
st.set_page_config(
    page_title="GenAI Insurance Advisor", 
    page_icon="🛡️", 
    layout="wide",
    initial_sidebar_state="collapsed"  # Start with collapsed sidebar for speed
)

# Optimized session state initialization
def init_session_state():
    """Initialize session state efficiently"""
    defaults = {
        'advice_generated': False,
        'user_data': {},
        'advice_content': "",
        'processing': False,
        'chat_history': [],
        'premium_calculator': False,
        'claim_assistant': False
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# ----------------------- 
# 3. Optimized GenAI Integration with phi3:mini (FAST)
# ----------------------- 
@st.cache_data(ttl=1800)  # Cache AI responses for 30 minutes
def get_cached_genai_advice(age, job, income, location, family_size, health_condition, financial_goal):
    """Cache AI advice to avoid repeated API calls"""
    return get_genai_advice_internal(age, job, income, location, family_size, health_condition, financial_goal)

def get_genai_advice_internal(age, job, income, location, family_size, health_condition, financial_goal):
    """Generate advice using phi3:mini (super fast model)"""
    
    if not OLLAMA_AVAILABLE:
        return get_cached_fallback_advice(age, job, income, location)
    
    # Optimized prompt for phi3:mini (lightweight and fast)
    prompt = f"""Insurance advisor for India. Quick advice needed:

Profile: {age}yr {job}, ₹{income}/month, {location}, family:{family_size}
Goal: {financial_goal}
Health: {health_condition}

Recommend top 3 insurance schemes with:
- Premium cost
- Coverage amount  
- Why suitable
- How to apply

Focus on PMSBY, PMJJBY, PMJAY. Keep brief."""

    try:
        # Use phi3:mini model with optimized settings for speed
        response = ollama.chat(
            model='phi3:mini',  # Fast, lightweight model
            messages=[{'role': 'user', 'content': prompt}],
            stream=False,
            options={
                'temperature': 0.7,
                'top_p': 0.9,        
                'max_tokens': 200,   # Reduced for faster response
                'num_ctx': 1024,     # Smaller context for speed
                'num_predict': 200   # Limit prediction for faster response
            }
        )
        
        ai_advice = response['message']['content']
        
        # Enhanced response format optimized for phi3:mini output
        full_advice = f"""
## 🤖 AI Insurance Advisor Analysis (Powered by phi3:mini - Lightning Fast!)

{ai_advice}

---

## 📊 Recommended Insurance Portfolio

### 1. PMSBY - Accident Insurance ✅
- **Premium:** ₹20 per year
- **Coverage:** ₹2 lakh accident protection
- **Best for:** Everyone (mandatory recommendation)
- **Apply at:** Any bank branch with Aadhaar

### 2. PMJJBY - Life Insurance ✅  
- **Premium:** ₹436 per year
- **Coverage:** ₹2 lakh life cover
- **Best for:** Families with dependents
- **Apply at:** Bank with auto-debit facility

### 3. PMJAY - Ayushman Bharat Health Insurance ✅
- **Premium:** FREE for eligible families
- **Coverage:** ₹5 lakh per family per year
- **Best for:** Families earning < ₹1.8L annually
- **Check eligibility:** pmjay.gov.in

### 4. Atal Pension Yojana (APY) 💰
- **Premium:** ₹42-₹291 per month (age dependent)
- **Coverage:** ₹1,000-₹5,000 monthly pension
- **Best for:** Retirement planning
- **Apply at:** Any bank

---

## 💡 Your Personalized Action Plan:
1. **This Week:** Visit bank for PMSBY (₹20) - Easiest to start
2. **Next Week:** Apply for PMJJBY if you have family
3. **Check online:** PMJAY eligibility on official website
4. **Long-term:** Consider APY for retirement

**Total Annual Investment:** ₹456-₹3,948 (based on your needs)
**Response time:** Under 10 seconds with phi3:mini!
"""
        
        return full_advice
        
    except Exception as e:
        st.error(f"phi3:mini AI Error: {str(e)}. Using fallback recommendations...")
        return get_cached_fallback_advice(age, job, income, location)

# ----------------------- 
# 4. Optimized Features
# ----------------------- 

def premium_calculator():
    """Optimized premium calculator with cached calculations"""
    st.subheader("💰 Premium Calculator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Government Schemes:**")
        pmsby = st.checkbox("PMSBY - Accident (₹20/year)", value=True)
        pmjjby = st.checkbox("PMJJBY - Life (₹436/year)")
        apy = st.checkbox("Atal Pension Yojana")
        
        apy_amount = "₹42"
        if apy:
            apy_amount = st.selectbox("APY Monthly:", ["₹42", "₹84", "₹168", "₹291"])
    
    with col2:
        st.write("**Additional Coverage:**")
        health_addon = st.checkbox("Health Insurance Top-up")
        health_premium = 500
        if health_addon:
            health_premium = st.slider("Health Premium (₹/month):", 200, 2000, 500)
        
        term_insurance = st.checkbox("Term Insurance")
        term_premium = 800
        if term_insurance:
            term_premium = st.slider("Term Premium (₹/month):", 300, 3000, 800)
    
    # Optimized calculation
    total_annual = 0
    if pmsby: total_annual += 20
    if pmjjby: total_annual += 436
    if apy: 
        apy_map = {"₹42": 504, "₹84": 1008, "₹168": 2016, "₹291": 3492}
        total_annual += apy_map.get(apy_amount, 504)
    if health_addon: 
        total_annual += health_premium * 12
    if term_insurance: 
        total_annual += term_premium * 12
    
    st.metric("💸 Total Annual Premium", f"₹{total_annual:,}", f"₹{total_annual//12:,}/month")
    
    if total_annual > 0:
        coverage_estimate = 200000 + (500000 if health_addon else 0) + (1000000 if term_insurance else 0)
        st.metric("🛡️ Total Coverage", f"₹{coverage_estimate//100000:,} Lakh")

@st.cache_data(ttl=3600)
def get_cached_claim_help():
    """Cache claim help responses"""
    return {
        "Accident Claim (PMSBY)": """
        **PMSBY Claim Process:**
        1. Contact bank immediately
        2. Submit claim form within 30 days
        3. Required: Death certificate/disability certificate
        4. Timeline: 30-60 days
        5. Helpline: 1800-180-1111
        """,
        "Life Insurance Claim (PMJJBY)": """
        **PMJJBY Claim Process:**
        1. Inform bank within 30 days
        2. Submit death certificate + claim form
        3. Bank will process within 30 days
        4. Amount credited to nominee account
        5. Helpline: Contact your bank
        """,
        "Health Insurance Claim (PMJAY)": """
        **PMJAY Claim Help:**
        1. Visit empaneled hospital
        2. Show Ayushman card at admission
        3. Cashless treatment for eligible procedures
        4. For issues: Call 14555
        5. Website: pmjay.gov.in
        """
    }

def claim_assistant():
    """Optimized claim assistant with phi3:mini (fast responses)"""
    st.subheader("🤝 Claim Assistant")
    
    config = get_static_config()
    claim_type = st.selectbox("Select Claim Type:", config['claim_types'])
    
    issue_description = st.text_area("Describe your issue:", 
                                   placeholder="e.g., Hospital denied cashless treatment, Claim rejected, Need help with documents")
    
    if st.button("🤖 Get AI Help ") and issue_description:
        with st.spinner("phi3:mini AI analyzing (5-10 seconds)..."):
            
            if OLLAMA_AVAILABLE:
                try:
                    prompt = f"""Insurance claim help for India:

Type: {claim_type}
Issue: {issue_description}

Quick help needed:
1. What to do now
2. Documents needed
3. Contact info
4. Timeline

Keep brief, actionable advice only."""

                    response = ollama.chat(
                        model='phi3:mini',  # Fast model
                        messages=[{'role': 'user', 'content': prompt}],
                        stream=False,
                        options={
                            'temperature': 0.3,
                            'max_tokens': 150,
                            'num_ctx': 512,     # Smaller for speed
                            'num_predict': 150  # Limit for faster response
                        }
                    )
                    
                    st.success("🤖 phi3:mini AI Claim Assistant Response (Ultra Fast!):")
                    st.write(response['message']['content'])
                    
                except Exception as e:
                    st.error(f"phi3:mini AI Error: {e}")
                    show_generic_claim_help(claim_type)
            else:
                show_generic_claim_help(claim_type)

def show_generic_claim_help(claim_type):
    """Generic claim help when AI is not available"""
    help_text = get_cached_claim_help()
    st.info(help_text.get(claim_type, "Contact your insurance provider or bank for specific guidance."))

# ADD THESE FUNCTIONS AFTER show_generic_claim_help function

def generate_insurance_pdf(user_data, advice_content):
    """Generate PDF report of insurance recommendations"""
    buffer = io.BytesIO()
    
    # Create PDF document
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title = Paragraph("🛡️ Your Personalized Insurance Plan", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 20))
    
    # Generated date
    date_text = f"Generated on: {datetime.now().strftime('%B %d, %Y')}"
    date_para = Paragraph(date_text, styles['Normal'])
    story.append(date_para)
    story.append(Spacer(1, 20))
    
    # User profile
    profile_title = Paragraph("Your Profile", styles['Heading2'])
    story.append(profile_title)
    
    profile_text = f"""
    • Age: {user_data.get('age')} years<br/>
    • Occupation: {user_data.get('job')}<br/>
    • Monthly Income: {user_data.get('income')}<br/>
    • Location: {user_data.get('location')}<br/>
    • Family Size: {user_data.get('family_size')}<br/>
    • Financial Goal: {user_data.get('financial_goal')}<br/>
    """
    
    profile_para = Paragraph(profile_text, styles['Normal'])
    story.append(profile_para)
    story.append(Spacer(1, 20))
    
    # Recommendations
    rec_title = Paragraph("AI Recommendations", styles['Heading2'])
    story.append(rec_title)
    
    # Clean up the advice content for PDF
    clean_advice = advice_content.replace('##', '').replace('**', '').replace('*', '')
    clean_advice = clean_advice.replace('✅', '✓').replace('🏥', 'Health').replace('💰', 'Money')
    # Remove markdown links and make text PDF-friendly
    clean_advice = clean_advice.replace('[', '').replace(']', '').replace('(', '').replace(')', '')
    
    advice_para = Paragraph(clean_advice[:2000], styles['Normal'])  # Limit length
    story.append(advice_para)
    story.append(Spacer(1, 20))
    
    # Contact info
    contact_title = Paragraph("Next Steps", styles['Heading2'])
    story.append(contact_title)
    
    next_steps = """
    1. Visit your nearest bank branch with Aadhaar card<br/>
    2. Apply for PMSBY (₹20/year) first - easiest to start<br/>
    3. Check PMJAY eligibility online at pmjay.gov.in<br/>
    4. Consider PMJJBY if you have family dependents<br/>
    5. Keep this report for reference when visiting bank<br/>
    """
    
    steps_para = Paragraph(next_steps, styles['Normal'])
    story.append(steps_para)
    
    # Footer
    story.append(Spacer(1, 30))
    footer = Paragraph("Generated by GenAI Insurance Advisor • Powered by phi3:mini AI", styles['Italic'])
    story.append(footer)
    
    # Build PDF
    doc.build(story)
    
    buffer.seek(0)
    return buffer

def add_pdf_download_button():
    """Add PDF download functionality"""
    if st.session_state.advice_generated and st.session_state.user_data:
        
        st.markdown("---")
        st.subheader("📄 Save Your Plan")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("📄 Generate & Download PDF Report", type="secondary", use_container_width=True):
                try:
                    with st.spinner("Generating PDF report..."):
                        # Generate PDF
                        pdf_buffer = generate_insurance_pdf(
                            st.session_state.user_data, 
                            st.session_state.advice_content
                        )
                        
                        # Create download
                        st.download_button(
                            label="💾 Download Your Insurance Plan (PDF)",
                            data=pdf_buffer.getvalue(),
                            file_name=f"Insurance_Plan_{datetime.now().strftime('%Y%m%d')}.pdf",
                            mime="application/pdf",
                            type="primary",
                            use_container_width=True
                        )
                        
                        st.success("📄 PDF generated successfully! Click download button above to save your personalized insurance plan.")
                        
                except Exception as e:
                    st.error(f"Error generating PDF: {str(e)}")
                    st.info("PDF feature requires: pip install reportlab")
                    
        st.info("💡 Tip: Save this PDF and take it to your bank when applying for insurance schemes!")

@st.cache_data(ttl=1800)
def get_simple_answer(question):
    """Cache simple chatbot answers"""
    if 'pmjay' in question or 'ayushman' in question:
        return "PMJAY provides ₹5 lakh free health coverage. Check eligibility at pmjay.gov.in or call 14555."
    elif 'pmsby' in question:
        return "PMSBY costs ₹20/year for ₹2 lakh accident coverage. Apply at any bank with Aadhaar and account."
    elif 'pmjjby' in question:
        return "PMJJBY costs ₹436/year for ₹2 lakh life insurance. Available for 18-50 age group through banks."
    elif 'document' in question:
        return "Basic documents: Aadhaar card, bank account, mobile number. Specific schemes may need additional documents."
    else:
        return "For detailed information, visit your nearest bank branch or check the official government insurance websites."

def insurance_chatbot():
    """Optimized insurance Q&A chatbot with phi3:mini (lightning fast)"""
    st.subheader("💬 Insurance Chatbot (Powered by phi3:mini - Lightning Fast!)")
    
    # Display only last 5 chats for performance
    recent_chats = st.session_state.chat_history[-5:] if len(st.session_state.chat_history) > 5 else st.session_state.chat_history
    
    for chat in recent_chats:
        st.write(f"**You:** {chat['question']}")
        st.write(f"**Bot:** {chat['answer']}")
        st.write("---")
    
    # New question
    user_question = st.text_input("Ask any insurance question:", 
                                placeholder="e.g., How to apply for PMJAY? What documents needed for PMSBY?")
    
    if st.button("Ask  Bot") and user_question:
        
        if OLLAMA_AVAILABLE:
            try:
                prompt = f"""Insurance expert for India. Quick answer:

Q: {user_question}

Give brief, practical answer in 2-3 lines. Focus on actionable steps."""

                response = ollama.chat(
                    model='phi3:mini',  # Super fast model
                    messages=[{'role': 'user', 'content': prompt}],
                    stream=False,
                    options={
                        'temperature': 0.3,
                        'max_tokens': 100,   # Very short for speed
                        'num_ctx': 512,      # Small context for speed
                        'num_predict': 100   # Fast prediction
                    }
                )
                
                answer = response['message']['content']
                
            except Exception as e:
                answer = "I'm having trouble connecting to phi3:mini AI. Please try again or contact your nearest bank for insurance guidance."
        else:
            # Use cached simple responses
            answer = get_simple_answer(user_question.lower())
        
        # Add to history and keep only last 10 for performance
        st.session_state.chat_history.append({
            'question': user_question,
            'answer': answer,
            'timestamp': datetime.now().strftime("%H:%M")
        })
        
        # Keep only last 10 chats to prevent memory bloat
        if len(st.session_state.chat_history) > 10:
            st.session_state.chat_history = st.session_state.chat_history[-10:]
        
        st.rerun()

# ----------------------- 
# 5. Main Optimized Streamlit App
# ----------------------- 
def main():
    # Header with enhanced design
    st.title("🛡️ GenAI MicroInsurance Advisor")
    st.markdown("*Powered by AI • phi3:mini Model*")
    
    # Show AI status
    if OLLAMA_AVAILABLE:
        st.success("✅ AI Model Ready")
    else:
        st.warning("⚠️ Using Smart Recommendations (Install Ollama + phi3:mini for full AI features)")
    
    # Enhanced metrics dashboard
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Gov Schemes", "10+", "Available")
    with col2:
        st.metric("Min Cost", "₹20", "Per Year")
    with col3:
        st.metric("Max Coverage", "₹5L", "Health Free")
    with col4:
        st.metric("AI Model", "phi3:mini", "⚡ Fast" if OLLAMA_AVAILABLE else "Offline")
    with col5:
        st.metric("Response Time", "<10s", "Lightning")
    
    # Navigation tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏠 Main Advisor", "💰 Premium Calculator", "🤝 Claim Help", "💬 Chat Bot", "📊 Dashboard"])
    
    with tab1:
        # Main advisor logic
        if st.session_state.advice_generated and st.session_state.advice_content:
            # Display results
            st.success("🎉 Your phi3:mini AI-Powered Insurance Plan is Ready!")
            
            # New consultation button
            if st.button("🔄 New Consultation", type="secondary"):
                # Clear session state efficiently
                for key in ['advice_generated', 'user_data', 'advice_content', 'processing']:
                    st.session_state[key] = False if 'generated' in key or 'processing' in key else {}
                st.rerun()
        

            # Display advice
            st.markdown(st.session_state.advice_content)
            
            add_pdf_download_button()
            # Fixed action buttons with correct URLs
            st.markdown("---")
            st.subheader("🎯 Take Action Now!")
            
            location = st.session_state.user_data.get('location', 'India')
            
            col1, col2, col3 = st.columns(3)
            with col1:
                bank_url = f"https://www.google.com/maps/search/banks+near+{location.replace(' ', '+')}"
                st.markdown(f'<a href="{bank_url}" target="_blank"><button style="background:#FF4B4B;color:white;padding:10px;border:none;border-radius:5px;width:100%;">🏦 Find Banks Near Me</button></a>', unsafe_allow_html=True)
            
            with col2:
                # Fixed PMJAY URL
                pmjay_url = "https://pmjay.gov.in/"
                st.markdown(f'<a href="{pmjay_url}" target="_blank"><button style="background:#00CC66;color:white;padding:10px;border:none;border-radius:5px;width:100%;">🏥 Check PMJAY Eligibility</button></a>', unsafe_allow_html=True)
            
            with col3:
                # Fixed APY link - using the correct government website
                apy_url = "https://financialservices.gov.in/beta/en/atal-pension-yojna"
                st.markdown(f'<a href="{apy_url}" target="_blank"><button style="background:#0066CC;color:white;padding:10px;border:none;border-radius:5px;width:100%;">💰 Atal Pension Scheme</button></a>', unsafe_allow_html=True)
            
        else:
            # Enhanced input form with cached options
            st.subheader("📝 Tell Us About Yourself")
            
            config = get_static_config()
            
            with st.form("user_form", clear_on_submit=False):            
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    age = st.number_input("Your Age", min_value=18, max_value=100, value=30)
                    job = st.selectbox("Your Occupation", config['occupations'])
                    family_size = st.selectbox("Family Size", config['family_sizes'])
                
                with col2:
                    income = st.selectbox("Monthly Income", config['income_brackets'])
                    location = st.text_input("Your City/Village", placeholder="e.g., Mumbai, Delhi, Pune")
                    health_condition = st.selectbox("Health Status", config['health_status'])
                
                with col3:
                    financial_goal = st.selectbox("Primary Financial Goal", config['financial_goals'])
                    
                    # Additional preferences
                    st.write("**Preferences:**")
                    risk_appetite = st.radio("Risk Appetite:", config['risk_levels'], horizontal=True)
                
                # Submit button
                submitted = st.form_submit_button("🚀 Get phi3:mini AI Advice", type="primary", use_container_width=True)
            
            # Process form submission
            if submitted and not st.session_state.processing:
                if not location.strip():
                    st.error("Please enter your city/village name!")
                    return
                
                st.session_state.processing = True
                
                # Convert income to number using cached mapping
                income_num = config['income_map'][income]
                
                # Store enhanced user data
                st.session_state.user_data = {
                    'age': age,
                    'job': job,
                    'income': income,
                    'income_num': income_num,
                    'location': location,
                    'family_size': family_size,
                    'health_condition': health_condition,
                    'financial_goal': financial_goal,
                    'risk_appetite': risk_appetite
                }
                
                # Ultra-fast processing display for phi3:mini
                progress_container = st.container()
                with progress_container:
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # Super fast progress updates for phi3:mini
                    steps = [
                        (25, "🧠 Analyzing profile..."),
                        (60, "🤖 Consulting phi3:mini (ultra fast)..."),
                        (90, "📊 Generating recommendations..."),
                        (100, "✅ Ready in seconds!")
                    ]
                    
                    for progress, message in steps:
                        status_text.text(message)
                        progress_bar.progress(progress)
                        time.sleep(0.2)  # Even faster for phi3:mini
                    
                    # Generate advice using cached function
                    try:
                        advice = get_cached_genai_advice(age, job, income_num, location, family_size, health_condition, financial_goal)
                        
                        st.session_state.advice_content = advice
                        st.session_state.advice_generated = True
                        st.session_state.processing = False
                        
                        status_text.text("🎉 Complete in under 10 seconds!")
                        time.sleep(0.3)
                        
                        progress_bar.empty()
                        status_text.empty()
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Error generating advice: {str(e)}")
                        st.session_state.processing = False
    
    with tab2:
        premium_calculator()
    
    with tab3:
        claim_assistant()
    
    with tab4:
        insurance_chatbot()
    
    with tab5:
        # Dashboard with user stats
        st.subheader("📊 Your Insurance Dashboard")
        
        if st.session_state.user_data:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Your Age Group", f"{st.session_state.user_data.get('age')} years", "Active earning phase")
            
            with col2:
                income = st.session_state.user_data.get('income_num', 0)
                st.metric("Monthly Income", f"₹{income:,}", "Eligible for govt schemes")
            
            with col3:
                family = st.session_state.user_data.get('family_size', '1')
                st.metric("Family Size", family, "Coverage needed")
            
            # Recommendations summary
            st.write("### 📋 Quick Recommendations:")
            st.info("✅ PMSBY (₹20) - Essential accident cover")
            st.info("✅ PMJJBY (₹436) - Life insurance for family")
            st.info("✅ PMJAY - Check eligibility for free health cover")
            
        else:
            st.info("Complete the main advisor form to see your personalized dashboard!")

# Installation reminder for phi3:mini
st.sidebar.markdown("### 🔧 Setup Instructions (phi3:mini)")
st.sidebar.code("pip install ollama streamlit")
st.sidebar.code("ollama pull phi3:mini")
st.sidebar.markdown("**Then run:** `streamlit run app.py`")
st.sidebar.success("✅ phi3:mini is super fast - responses in 5-10 seconds!")

# Run the enhanced app
if __name__ == "__main__":
    main()