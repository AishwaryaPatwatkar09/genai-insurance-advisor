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
import requests

st.set_page_config(
    page_title="GenAI Insurance Advisor", 
    page_icon="🛡️", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

IS_CLOUD_ENV = os.getenv("IS_CLOUD", "true").lower() == "true"

if not IS_CLOUD_ENV:
    try:
        import ollama
        OLLAMA_AVAILABLE = True
    except ImportError:
        OLLAMA_AVAILABLE = False
else:
    OLLAMA_AVAILABLE = False

def get_free_ai_response(prompt, max_retries=3):
    """Use Hugging Face's free inference API"""
    
    models = [
        "microsoft/DialoGPT-large",
        "facebook/blenderbot-400M-distill",
        "microsoft/DialoGPT-medium"
    ]
    
    for model in models:
        for attempt in range(max_retries):
            try:
                API_URL = f"https://api-inference.huggingface.co/models/{model}"
                
                # Check if API key exists
                api_key = ""
                try:
                    api_key = st.secrets.get('HUGGINGFACE_API_KEY', '')
                except:
                    pass
                
                headers = {
                    "Authorization": f"Bearer {api_key}"
                } if api_key else {}
                
                formatted_prompt = f"Insurance Expert: {prompt}\nResponse:"
                
                payload = {
                    "inputs": formatted_prompt,
                    "parameters": {
                        "max_length": 200,
                        "temperature": 0.7,
                        "do_sample": True
                    }
                }
                
                response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
                
                if response.status_code == 200:
                    result = response.json()
                    if isinstance(result, list) and len(result) > 0:
                        if 'generated_text' in result[0]:
                            text = result[0]['generated_text']
                            if "Response:" in text:
                                text = text.split("Response:")[-1].strip()
                            return text
                elif response.status_code == 503:
                    break
                    
            except Exception as e:
                if attempt == max_retries - 1:
                    continue
                
    return get_knowledge_based_response(prompt)

def get_knowledge_based_response(prompt):
    """Fallback knowledge-based responses"""
    prompt_lower = prompt.lower()
    
    if any(word in prompt_lower for word in ['claim', 'file', 'document']):
        return """To file an insurance claim:
        
1. **Report immediately** - Contact your insurer within 24-48 hours
2. **Gather documents** - Policy number, incident details, photos, receipts
3. **Fill forms accurately** - Complete all claim forms truthfully
4. **Submit promptly** - Don't delay submission
5. **Follow up** - Keep track of your claim status
6. **Keep records** - Maintain copies of all communications

Most claims are processed within 7-15 business days if all documents are complete."""

    elif any(word in prompt_lower for word in ['advice', 'recommend', 'choose', 'best']):
        return """Microinsurance Guidance:

**Health Insurance:**
- Covers medical emergencies and hospitalization
- Look for cashless facility at nearby hospitals
- Check waiting periods for pre-existing conditions

**Life Insurance:**
- Provides financial security to your family
- Term insurance offers maximum coverage at low cost
- Consider your family's monthly expenses × 120 months

**General Tips:**
- Start with basic health coverage
- Pay premiums on time to avoid policy lapse
- Understand exclusions and waiting periods
- Keep all policy documents safe
- Review coverage annually"""

    elif any(word in prompt_lower for word in ['premium', 'cost', 'payment', 'afford']):
        return """Managing Insurance Costs:

**Reduce Premiums:**
- Buy policies when young and healthy
- Choose higher deductibles if you can afford them
- Look for group insurance through employers
- Compare quotes from multiple insurers

**Payment Tips:**
- Set up automatic payments to avoid lapses
- Pay annually instead of monthly to save on fees
- Use digital payment methods for convenience
- Keep payment receipts for tax benefits

**Budget Planning:**
- Allocate 10-15% of income for insurance
- Prioritize health insurance first
- Build emergency fund alongside insurance"""

    else:
        return """I'm here to help with your insurance questions! 

**I can assist with:**
- Choosing the right insurance policy
- Understanding claim procedures
- Comparing different insurance options
- Managing premium payments
- Understanding policy terms and conditions

**Popular Topics:**
- Health insurance coverage
- Life insurance planning
- Claim filing process
- Premium calculation
- Policy renewal procedures

Feel free to ask specific questions about any insurance topic!"""
# 1. TRANSLATIONS AND CONFIGURATIONS
TRANSLATIONS = {
    'en': {
        'title': '🛡️ GenAI MicroInsurance Advisor',
        'subtitle': 'Powered by AI • phi3:mini Model',
        'tell_about': 'Tell Us About Yourself',
        'your_age': 'Your Age',
        'occupation': 'Your Occupation',
        'monthly_income': 'Monthly Income',
        'family_size': 'Family Size',
        'location': 'Your City/Village',
        'health_status': 'Health Status',
        'financial_goal': 'Primary Financial Goal',
        'risk_appetite': 'Risk Appetite',
        'get_advice': 'Get AI Advice',
        'new_consultation': 'New Consultation',
        'premium_calculator': 'Premium Calculator',
        'claim_help': 'Claim Help',
        'chat_bot': 'Chat Bot',
        'dashboard': 'Dashboard',
        'ai_ready': 'AI Model Ready',
        'gov_schemes': 'Gov Schemes',
        'min_cost': 'Min Cost',
        'max_coverage': 'Max Coverage',
        'response_time': 'Response Time',
        'per_year': 'Per Year',
        'health_free': 'Health Free',
        'lightning': 'Lightning',
        'main_advisor': 'Main Advisor',
        'preferences': 'Preferences',
        'location_placeholder': 'e.g., Mumbai, Delhi, Pune',
        'enter_location': 'Please enter your city/village name!',
        'plan_ready': 'Your AI-Powered Insurance Plan is Ready!',
        'take_action': 'Take Action Now!',
        'find_banks': 'Find Banks Near Me',
        'check_pmjay': 'Check PMJAY Eligibility',
        'atal_pension': 'Atal Pension Scheme'
    },
    'hi': {
        'title': '🛡️ जेनएआई माइक्रो बीमा सलाहकार',
        'subtitle': 'एआई द्वारा संचालित • phi3:mini मॉडल',
        'tell_about': 'अपने बारे में बताएं',
        'your_age': 'आपकी उम्र',
        'occupation': 'आपका पेशा',
        'monthly_income': 'मासिक आय',
        'family_size': 'परिवार का आकार',
        'location': 'आपका शहर/गांव',
        'health_status': 'स्वास्थ्य स्थिति',
        'financial_goal': 'मुख्य वित्तीय लक्ष्य',
        'risk_appetite': 'जोखिम की भूख',
        'get_advice': 'एआई सलाह प्राप्त करें',
        'new_consultation': 'नई सलाह',
        'premium_calculator': 'प्रीमियम कैलकुलेटर',
        'claim_help': 'क्लेम सहायता',
        'chat_bot': 'चैट बॉट',
        'dashboard': 'डैशबोर्ड',
        'ai_ready': 'एआई मॉडल तैयार',
        'gov_schemes': 'सरकारी योजनाएं',
        'min_cost': 'न्यूनतम लागत',
        'max_coverage': 'अधिकतम कवरेज',
        'response_time': 'प्रतिक्रिया समय',
        'per_year': 'प्रति वर्ष',
        'health_free': 'स्वास्थ्य मुफ्त',
        'lightning': 'बिजली',
        'main_advisor': 'मुख्य सलाहकार',
        'preferences': 'प्राथमिकताएं',
        'location_placeholder': 'जैसे मुंबई, दिल्ली, पुणे',
        'enter_location': 'कृपया अपना शहर/गांव का नाम दर्ज करें!',
        'plan_ready': 'आपकी एआई-संचालित बीमा योजना तैयार है!',
        'take_action': 'अभी कार्य करें!',
        'find_banks': 'मेरे पास बैंक खोजें',
        'check_pmjay': 'PMJAY पात्रता जांचें',
        'atal_pension': 'अटल पेंशन योजना'
    }
}

TRANSLATED_OPTIONS = {
    'en': {
        'occupations': ["Farmer", "Driver", "Teacher", "Shopkeeper", "Labor Worker", "Government Employee", "Self Employed", "Private Employee", "Student", "Retired", "Other"],
        'family_sizes': ["1", "2-3", "4-5", "6+"],
        'health_status': ["Excellent", "Good", "Fair", "Have medical conditions", "Prefer not to say"],
        'financial_goals': ["Basic Protection", "Family Security", "Health Coverage", "Retirement Planning", "Child Education", "Wealth Building"],
        'risk_levels': ["Conservative", "Moderate", "Aggressive"]
    },
    'hi': {
        'occupations': ["किसान", "ड्राइवर", "शिक्षक", "दुकानदार", "मजदूर", "सरकारी कर्मचारी", "स्व-नियोजित", "निजी कर्मचारी", "छात्र", "सेवानिवृत्त", "अन्य"],
        'family_sizes': ["1", "2-3", "4-5", "6+"],
        'health_status': ["उत्कृष्ट", "अच्छा", "ठीक", "चिकित्सा समस्याएं हैं", "नहीं बताना चाहते"],
        'financial_goals': ["बुनियादी सुरक्षा", "पारिवारिक सुरक्षा", "स्वास्थ्य कवरेज", "सेवानिवृत्ति योजना", "बच्चों की शिक्षा", "धन निर्माण"],
        'risk_levels': ["रूढ़िवादी", "मध्यम", "आक्रामक"]
    }
}

LANGUAGES = {
    'en': '🇺🇸 English',
    'hi': '🇮🇳 हिंदी'
}
# 2. CONFIGURATION FUNCTIONS 
@st.cache_data
def get_static_config():
    """Cache static configuration data with language support"""
    lang = st.session_state.get('selected_language', 'en')
    
    return {
        'occupations': TRANSLATED_OPTIONS[lang]['occupations'],
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
        'family_sizes': TRANSLATED_OPTIONS[lang]['family_sizes'],
        'health_status': TRANSLATED_OPTIONS[lang]['health_status'],
        'financial_goals': TRANSLATED_OPTIONS[lang]['financial_goals'],
        'risk_levels': TRANSLATED_OPTIONS[lang]['risk_levels'],
        'claim_types': [
            "Accident Claim (PMSBY)",
            "Life Insurance Claim (PMJJBY)", 
            "Health Insurance Claim (PMJAY)",
            "Other Government Scheme"
        ]
    }

def init_session_state():
    """Initialize session state efficiently"""
    defaults = {
        'advice_generated': False,
        'user_data': {},
        'advice_content': "",
        'processing': False,
        'chat_history': [],
        'premium_calculator': False,
        'claim_assistant': False,
        'selected_language': 'en'
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def clear_language_cache():
    """Clear cached data when language changes"""
    try:
        st.cache_data.clear()
    except:
        pass

def get_text(key, lang='en'):
    """Get translated text"""
    return TRANSLATIONS.get(lang, {}).get(key, TRANSLATIONS['en'].get(key, key))
# 3. AI FUNCTIONS
@st.cache_data(ttl=1800)
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

@st.cache_data(ttl=1800)
def get_cached_genai_advice(age, job, income, location, family_size, health_condition, financial_goal):
    """Cache AI advice to avoid repeated API calls"""
    return get_genai_advice_internal(age, job, income, location, family_size, health_condition, financial_goal)

def get_genai_advice_internal(age, job, income, location, family_size, health_condition, financial_goal):
    """Generate advice using phi3:mini with language support"""
    
    lang = st.session_state.get('selected_language', 'en')
    
    if not OLLAMA_AVAILABLE:
        return get_cached_fallback_advice(age, job, income, location)
    
    if lang == 'hi':
        prompt = f"""भारत के लिए बीमा सलाहकार। हिंदी में सलाह चाहिए:

प्रोफाइल: {age} साल, {job}, ₹{income}/महीना, {location}, परिवार: {family_size}
लक्ष्य: {financial_goal}
स्वास्थ्य: {health_condition}

टॉप 3 बीमा योजनाओं में सुझाव दें:
- प्रीमियम लागत
- कवरेज राशि
- क्यों उपयुक्त है
- कैसे आवेदन करें

PMSBY, PMJJBY, PMJAY पर फोकस करें। संक्षिप्त रखें।"""
    else:
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
        response = ollama.chat(
            model='phi3:mini',
            messages=[{'role': 'user', 'content': prompt}],
            stream=False,
            options={
                'temperature': 0.7,
                'top_p': 0.9,        
                'max_tokens': 200,
                'num_ctx': 1024,
                'num_predict': 200
            }
        )
        
        ai_advice = response['message']['content']
        
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
# 4. FEATURE FUNCTIONS
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

def show_generic_claim_help(claim_type):
    """Generic claim help when AI is not available"""
    help_text = get_cached_claim_help()
    st.info(help_text.get(claim_type, "Contact your insurance provider or bank for specific guidance."))

def claim_assistant():
    """Optimized claim assistant with phi3:mini"""
    st.subheader("🤝 Claim Assistant")
    
    config = get_static_config()
    claim_type = st.selectbox("Select Claim Type:", config['claim_types'])
    
    issue_description = st.text_area("Describe your issue:", 
                                   placeholder="e.g., Hospital denied cashless treatment, Claim rejected, Need help with documents")
    
    if st.button("🤖 Get AI Help") and issue_description:
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
                        model='phi3:mini',
                        messages=[{'role': 'user', 'content': prompt}],
                        stream=False,
                        options={
                            'temperature': 0.3,
                            'max_tokens': 150,
                            'num_ctx': 512,
                            'num_predict': 150
                        }
                    )
                    
                    st.success("🤖 phi3:mini AI Claim Assistant Response (Ultra Fast!):")
                    st.write(response['message']['content'])
                    
                except Exception as e:
                    st.error(f"phi3:mini AI Error: {e}")
                    # Use fallback AI
                    fallback_response = get_free_ai_response(f"Claim help for {claim_type}: {issue_description}")
                    st.info("🤖 Fallback AI Response:")
                    st.write(fallback_response)
            else:
                # Use fallback AI when Ollama is not available
                fallback_response = get_free_ai_response(f"Claim help for {claim_type}: {issue_description}")
                st.info("🤖 AI Response:")
                st.write(fallback_response)

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
    st.subheader("💬 Insurance Chatbot")
    
    # Show recent chat history
    recent_chats = st.session_state.chat_history[-5:] if len(st.session_state.chat_history) > 5 else st.session_state.chat_history
    
    for chat in recent_chats:
        st.write(f"**You:** {chat['question']}")
        st.write(f"**Bot:** {chat['answer']}")
        st.write("---")
    
    # Input for new question - FIXED INDENTATION
    user_question = st.text_input("Ask any insurance question:", 
                                placeholder="e.g., How to apply for PMJAY? What documents needed for PMSBY?")
    
    if st.button("Ask Bot") and user_question:
        
        if OLLAMA_AVAILABLE:
            try:
                prompt = f"""Insurance expert for India. Quick answer:

Q: {user_question}

Give brief, practical answer in 2-3 lines. Focus on actionable steps."""

                response = ollama.chat(
                    model='phi3:mini',
                    messages=[{'role': 'user', 'content': prompt}],
                    stream=False,
                    options={
                        'temperature': 0.3,
                        'max_tokens': 100,
                        'num_ctx': 512,
                        'num_predict': 100
                    }
                )
                
                answer = response['message']['content']
                
            except Exception as e:
                answer = f"I'm having trouble connecting to phi3:mini AI. Please try again or contact your nearest bank for insurance guidance. phi3:mini AI Error: Failed to connect to Ollama. Please check that Ollama is downloaded, running and accessible. https://ollama.com/download"
        else:
            # Use fallback to Hugging Face API
            answer = get_free_ai_response(user_question)
        
        # Add to chat history
        st.session_state.chat_history.append({
            'question': user_question,
            'answer': answer,
            'timestamp': datetime.now().strftime("%H:%M")
        })
        
        # Keep only last 10 chats
        if len(st.session_state.chat_history) > 10:
            st.session_state.chat_history = st.session_state.chat_history[-10:]
        
        st.rerun()

def generate_insurance_pdf(user_data, advice_content):
    """Generate PDF report of insurance recommendations"""
    buffer = io.BytesIO()
    
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    
    title = Paragraph("🛡️ Your Personalized Insurance Plan", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 20))
    
    date_text = f"Generated on: {datetime.now().strftime('%B %d, %Y')}"
    date_para = Paragraph(date_text, styles['Normal'])
    story.append(date_para)
    story.append(Spacer(1, 20))
    
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
    
    rec_title = Paragraph("AI Recommendations", styles['Heading2'])
    story.append(rec_title)
    
    clean_advice = advice_content.replace('##', '').replace('**', '').replace('*', '')
    clean_advice = clean_advice.replace('✅', '✓').replace('🏥', 'Health').replace('💰', 'Money')
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
    st.subheader("💬 Insurance Chatbot")
    
    recent_chats = st.session_state.chat_history[-5:] if len(st.session_state.chat_history) > 5 else st.session_state.chat_history
    
    for chat in recent_chats:
        st.write(f"**You:** {chat['question']}")
        st.write(f"**Bot:** {chat['answer']}")
        st.write("---")
    
    user_question = st.text_input("Ask any insurance question:", 
                                placeholder="e.g., How to apply for PMJAY? What documents needed for PMSBY?")
    if st.button("Ask Bot") and user_question:
        
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
            answer = get_simple_answer(user_question.lower())
        
        st.session_state.chat_history.append({
            'question': user_question,
            'answer': answer,
            'timestamp': datetime.now().strftime("%H:%M")
        })
        
        if len(st.session_state.chat_history) > 10:
            st.session_state.chat_history = st.session_state.chat_history[-10:]
        
        st.rerun()

LANGUAGES = {
    'en': '🇺🇸 English',
    'hi': '🇮🇳 हिंदी'
}

def get_text(key, lang='en'):
    """Get translated text"""
    return TRANSLATIONS.get(lang, {}).get(key, TRANSLATIONS['en'].get(key, key))
# 5. Main Optimized Streamlit App
def main():
    if 'advice_generated' not in st.session_state:
        st.session_state.advice_generated = False
    if 'user_data' not in st.session_state:
        st.session_state.user_data = {}
    if 'advice_content' not in st.session_state:
        st.session_state.advice_content = ""
    if 'processing' not in st.session_state:
        st.session_state.processing = False
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'selected_language' not in st.session_state:
        st.session_state.selected_language = 'en'
        
    lang = st.session_state.get('selected_language', 'en')

    col1, col2 = st.columns([4, 1])
    with col1:
            st.markdown(f"# {get_text('title', lang)}")
            st.markdown(f"*{get_text('subtitle', lang)}*")
    with col2:
            selected_lang = st.selectbox(
                "🌍",
                options=list(LANGUAGES.keys()),
                format_func=lambda x: LANGUAGES[x],
                key="language_selector",
                index=list(LANGUAGES.keys()).index(st.session_state.get('selected_language', 'en'))
            )
        
            if selected_lang != st.session_state.get('selected_language', 'en'):
                st.session_state.selected_language = selected_lang
                clear_language_cache()  # Clear cache when language changes
                st.rerun()
            
    if OLLAMA_AVAILABLE:
            st.success(f"✅ {get_text('ai_ready', lang)}")
    else:
            st.warning("⚠️ Using Smart Recommendations (Install Ollama + phi3:mini for full AI features)")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        # Use safer approach with fallback
        gov_schemes_text = get_text('gov_schemes', lang) if 'gov_schemes' in TRANSLATIONS.get(lang, {}) else "Gov Schemes"
        st.metric(gov_schemes_text, "10+", "Available")
    
    with col2:
        min_cost_text = get_text('min_cost', lang) if 'min_cost' in TRANSLATIONS.get(lang, {}) else "Min Cost"
        st.metric(min_cost_text, "₹20", get_text('per_year', lang))
    
    with col3:
        max_coverage_text = get_text('max_coverage', lang) if 'max_coverage' in TRANSLATIONS.get(lang, {}) else "Max Coverage"
        health_free_text = get_text('health_free', lang) if 'health_free' in TRANSLATIONS.get(lang, {}) else "Health Free"
        st.metric(max_coverage_text, "₹5L", health_free_text)
    
    with col4:
        st.metric("AI Model", "phi3:mini", f"⚡ Online" if OLLAMA_AVAILABLE else "Offline")
    
    with col5:
        response_time_text = get_text('response_time', lang) if 'response_time' in TRANSLATIONS.get(lang, {}) else "Response Time"
        st.metric(response_time_text, "<30s", "Real-time")  
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        f"🏠 {get_text('main_advisor', lang)}", 
        f"💰 {get_text('premium_calculator', lang)}", 
        f"🤝 {get_text('claim_help', lang)}", 
        f"💬 {get_text('chat_bot', lang)}", 
        f"📊 {get_text('dashboard', lang)}"
    ])
    
    with tab1:
        lang = st.session_state.get('selected_language', 'en')
    
        if st.session_state.advice_generated and st.session_state.advice_content:
            st.success(f"🎉 {get_text('plan_ready', lang)}")
        
            if st.button(f"🔄 {get_text('new_consultation', lang)}", type="secondary"):
                for key in ['advice_generated', 'user_data', 'advice_content', 'processing']:
                    st.session_state[key] = False if 'generated' in key or 'processing' in key else {}
                st.rerun()
        
            st.markdown(st.session_state.advice_content)
            add_pdf_download_button()        
            st.markdown("---")
            st.subheader(f"🎯 {get_text('take_action', lang)}")
        
            location = st.session_state.user_data.get('location', 'India')
        
            col1, col2, col3 = st.columns(3)
            with col1:
                bank_url = f"https://www.google.com/maps/search/banks+near+{location.replace(' ', '+')}"
                st.markdown(f'<a href="{bank_url}" target="_blank"><button style="background:#FF4B4B;color:white;padding:10px;border:none;border-radius:5px;width:100%;">🏦 {get_text("find_banks", lang)}</button></a>', unsafe_allow_html=True)
        
            with col2:
                pmjay_url = "https://pmjay.gov.in/"
                st.markdown(f'<a href="{pmjay_url}" target="_blank"><button style="background:#00CC66;color:white;padding:10px;border:none;border-radius:5px;width:100%;">🏥 {get_text("check_pmjay", lang)}</button></a>', unsafe_allow_html=True)
        
            with col3:
                apy_url = "https://financialservices.gov.in/beta/en/atal-pension-yojna"
                st.markdown(f'<a href="{apy_url}" target="_blank"><button style="background:#0066CC;color:white;padding:10px;border:none;border-radius:5px;width:100%;">💰 {get_text("atal_pension", lang)}</button></a>', unsafe_allow_html=True)
    
        else:
            st.subheader(f"📝 {get_text('tell_about', lang)}")
            config = get_static_config()

            with st.form("user_form", clear_on_submit=False):            
                col1, col2, col3 = st.columns(3)
    
                with col1:
                    age = st.number_input(get_text('your_age', lang), min_value=18, max_value=100, value=30)
                    job = st.selectbox(get_text('occupation', lang), config['occupations'])
                    family_size = st.selectbox(get_text('family_size', lang), config['family_sizes'])
    
                with col2:
                    income = st.selectbox(get_text('monthly_income', lang), config['income_brackets'])
                    location = st.text_input(get_text('location', lang), placeholder=get_text('location_placeholder', lang))
                    health_condition = st.selectbox(get_text('health_status', lang), config['health_status'])
    
                with col3:
                    financial_goal = st.selectbox(get_text('financial_goal', lang), config['financial_goals'])
        
                    st.write(f"**{get_text('preferences', lang)}:**")
                    risk_appetite = st.radio(f"{get_text('risk_appetite', lang)}:", config['risk_levels'], horizontal=True)
    
                submitted = st.form_submit_button(f"🚀 {get_text('get_advice', lang)}", type="primary", use_container_width=True)
        
                if submitted and not st.session_state.processing:
                    if not location.strip():
                        st.error(get_text('enter_location', lang))
                    else:
                        st.session_state.processing = True
                
                        st.session_state.user_data = {
                            'age': age,
                            'job': job,
                            'income': income,
                            'income_num': config['income_map'].get(income, 10000),
                            'location': location,
                            'family_size': family_size,
                            'health_condition': health_condition,
                            'financial_goal': financial_goal,
                            'risk_appetite': risk_appetite
                        }
                        try:
                            advice = get_cached_genai_advice(
                                age=age,
                                job=job, 
                                income=config['income_map'].get(income, 10000),
                                location=location,
                                family_size=family_size,
                                health_condition=health_condition,
                                financial_goal=financial_goal
                            )
                    
                            st.session_state.advice_content = advice
                            st.session_state.advice_generated = True
                    
                        except Exception as e:
                            st.error(f"Error generating advice: {str(e)}")
                            st.session_state.advice_content = get_cached_fallback_advice(age, job, income, location)
                            st.session_state.advice_generated = True
                
                        finally:
                            st.session_state.processing = False
                
                        st.success("✅ Analysis complete! Your personalized insurance plan is ready.")
                        st.rerun()

            if st.session_state.processing:
                with st.spinner(f"🤖 phi3:mini AI analyzing your profile... ({get_text('response_time', lang)})"):
                    pass
    
    with tab2:
        premium_calculator()
    
    with tab3:
        claim_assistant()
    
    with tab4:
        insurance_chatbot()
    
    with tab5:
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
            
            st.write("### 📋 Quick Recommendations:")
            st.info("✅ PMSBY (₹20) - Essential accident cover")
            st.info("✅ PMJJBY (₹436) - Life insurance for family")
            st.info("✅ PMJAY - Check eligibility for free health cover")
            
        else:
            st.info("Complete the main advisor form to see your personalized dashboard!")

    st.sidebar.markdown("### 🔧 Setup Instructions (phi3:mini)")
    st.sidebar.code("pip install ollama streamlit")
    st.sidebar.code("ollama pull phi3:mini")
    st.sidebar.markdown("**Then run:** `streamlit run app.py`")
    st.sidebar.success("✅ phi3:mini is super fast - responses in 5-10 seconds!")

if __name__ == "__main__":
    main()
