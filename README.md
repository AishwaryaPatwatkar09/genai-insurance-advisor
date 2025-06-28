# 🛡️ Enhanced GenAI Insurance Advisor

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![Mistral AI](https://img.shields.io/badge/AI-Mistral-orange.svg)](https://mistral.ai)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An AI-powered insurance advisory platform that leverages the Mistral AI model to provide personalized insurance recommendations for Indian government schemes and private insurance options.

## 🎯 Project Description

The Enhanced GenAI Insurance Advisor is a comprehensive web application designed to democratize insurance knowledge and help users make informed decisions about insurance coverage. Built specifically for the Indian market, it focuses on government-sponsored programs like PMSBY, PMJJBY, PMJAY, and Atal Pension Yojana, making insurance accessible to rural and urban populations alike.

### 🌟 Key Highlights

- **🤖 Mistral AI Integration**: Advanced AI model provides intelligent, personalized insurance recommendations
- **🇮🇳 India-Focused**: Specialized knowledge of Indian insurance schemes and government programs
- **💰 Cost-Effective**: Helps users find coverage starting from just ₹20/year
- **⚡ Performance Optimized**: Cached responses, efficient loading, and optimized user experience
- **🌐 Accessible**: Simple interface designed for users across all literacy levels

## ✨ Features

### 🏠 Main Advisor
- **Personalized AI Recommendations**: Mistral AI analyzes user profile (age, income, family size, health status) to suggest optimal insurance schemes
- **Government Scheme Focus**: Specialized recommendations for PMSBY, PMJJBY, PMJAY, and APY
- **Smart Fallback**: Works even without AI connectivity using intelligent rule-based recommendations
- **Action-Oriented Results**: Direct links to application portals and nearby bank locations

### 💰 Premium Calculator
- **Interactive Cost Planning**: Calculate total insurance costs across multiple schemes
- **Government + Private Mix**: Compare costs for government schemes vs private insurance options
- **Real-time Updates**: Instant calculation of total premiums and coverage amounts
- **Coverage Estimation**: Shows total protection value for selected schemes

### 🤝 Claim Assistant
- **AI-Powered Support**: Mistral AI helps troubleshoot claim issues and provides step-by-step guidance
- **Scheme-Specific Help**: Specialized assistance for PMSBY, PMJJBY, PMJAY claims
- **Document Guidance**: Clear instructions on required documents and procedures
- **Contact Information**: Relevant helpline numbers and official websites

### 💬 Insurance Chatbot
- **Real-time Q&A**: Instant answers to insurance-related questions
- **Contextual Responses**: AI understands Indian insurance context and provides relevant answers
- **Chat History**: Maintains conversation history for reference
- **Fallback Knowledge**: Works with cached responses when AI is unavailable

### 📊 Personal Dashboard
- **Profile Overview**: Visual summary of user's insurance profile
- **Recommendation Tracking**: Quick view of suggested schemes and their status
- **Coverage Analysis**: Overview of current and recommended coverage levels

## 🚀 Technology Stack

- **Frontend**: Streamlit (Interactive Web UI)
- **AI Model**: Mistral AI (via Ollama)
- **Language**: Python 3.8+
- **Caching**: Streamlit's built-in caching system
- **Performance**: Optimized with async operations and efficient data handling

## 📋 Prerequisites

- Python 3.8 or higher
- Internet connection (for AI features)
- 4GB+ RAM recommended for optimal performance

## 🛠️ Installation & Setup

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/enhanced-genai-insurance-advisor.git
cd enhanced-genai-insurance-advisor
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install streamlit ollama
```

### Step 4: Setup Ollama and Mistral
```bash
# Install Ollama (visit https://ollama.ai for platform-specific instructions)
# For Linux/macOS:
curl -fsSL https://ollama.ai/install.sh | sh

# Pull Mistral model
ollama pull mistral
```

### Step 5: Run the Application
```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## 🎮 Usage Guide

### Getting Started
1. **Launch the App**: Open your browser and navigate to the Streamlit URL
2. **Fill Your Profile**: Enter your age, occupation, income, location, and other details
3. **Get AI Recommendations**: Click "Get Mistral AI Insurance Advice" for personalized suggestions
4. **Explore Features**: Use the tabs to access premium calculator, claim help, and chatbot

### Using Different Features

#### Main Advisor
- Fill out the comprehensive form with your personal details
- Receive AI-powered recommendations tailored to your profile
- Get direct links to apply for recommended schemes

#### Premium Calculator
- Select government and private insurance schemes
- Adjust coverage amounts using sliders
- See real-time cost calculations and total coverage

#### Claim Assistant
- Choose your claim type from the dropdown
- Describe your specific issue
- Get AI-powered troubleshooting steps and contact information

#### Chatbot
- Ask any insurance-related question
- Get instant AI-powered responses
- Access your chat history for reference

## 🏗️ Project Structure

```
enhanced-genai-insurance-advisor/
│
├── app.py                 # Main Streamlit application
├── README.md             # Project documentation
├── requirements.txt      # Python dependencies
├── .gitignore           # Git ignore file
└── docs/                # Additional documentation
    ├── setup_guide.md   # Detailed setup instructions
    └── user_manual.md   # Comprehensive user guide
```

## 🔧 Configuration

### AI Model Settings
The application uses optimized settings for Mistral AI:
- **Temperature**: 0.3-0.5 (balanced creativity and accuracy)
- **Max Tokens**: 150-300 (efficient response length)
- **Context Window**: 1024-2048 (adequate context understanding)

### Caching Strategy
- **Static Data**: Cached indefinitely (occupations, income brackets)
- **AI Responses**: Cached for 30 minutes
- **Fallback Advice**: Cached for 1 hour
- **Claim Help**: Cached for 3 hours

## 🎯 Target Audience

### Primary Users
- **Rural Population**: Farmers, laborers, small business owners seeking affordable insurance
- **Urban Middle Class**: Employees looking for comprehensive family coverage
- **Senior Citizens**: Retirees needing health and pension planning
- **Young Professionals**: Starting their insurance journey with government schemes

### Use Cases
- **First-time Insurance Buyers**: Guidance on essential coverage
- **Claim Support**: Help with claim processes and documentation
- **Cost Optimization**: Finding the right balance of coverage and affordability
- **Government Scheme Navigation**: Understanding eligibility and applications

## 🚀 Performance Optimizations

- **Lazy Loading**: Components load only when needed
- **Response Caching**: AI responses cached to reduce API calls
- **Session Management**: Efficient state management for faster interactions
- **Fallback Systems**: App works even when AI is unavailable
- **Optimized Prompts**: Tailored prompts for better AI responses

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the Repository**
2. **Create a Feature Branch**: `git checkout -b feature/new-feature`
3. **Make Changes**: Implement your improvements
4. **Test Thoroughly**: Ensure all features work correctly
5. **Submit Pull Request**: Describe your changes clearly

### Contribution Areas
- 🐛 Bug fixes and performance improvements
- 🚀 New insurance schemes integration
- 🌐 Multi-language support
- 📱 Mobile responsiveness enhancements
- 🧪 Testing and quality assurance

## 📊 Insurance Schemes Covered

### Government Schemes
| Scheme | Premium | Coverage | Target Group |
|--------|---------|----------|--------------|
| **PMSBY** | ₹20/year | ₹2 Lakh accident | All ages |
| **PMJJBY** | ₹436/year | ₹2 Lakh life | 18-50 years |
| **PMJAY** | Free | ₹5 Lakh health | Eligible families |
| **APY** | ₹42-291/month | ₹1-5K pension | 18-40 years |

### Additional Coverage
- Health insurance top-ups
- Term life insurance
- State-specific schemes
- Private insurance options

## 🔒 Privacy & Security

- **No Data Storage**: User data is not permanently stored
- **Session-Based**: Information cleared after session ends
- **Local Processing**: AI processing happens locally when possible
- **Secure Connections**: All external links use HTTPS

## 🚧 Known Limitations

- **AI Dependency**: Full features require Ollama and Mistral setup
- **Internet Required**: AI features need internet connectivity
- **India-Specific**: Primarily designed for Indian insurance market
- **Resource Intensive**: Mistral AI requires adequate system resources

## 🔮 Future Enhancements

- [ ] **Multi-language Support**: Hindi, Tamil, Telugu, and other regional languages
- [ ] **Mobile App**: Native mobile application for better accessibility
- [ ] **Advanced Analytics**: Insurance portfolio analysis and optimization
- [ ] **Integration APIs**: Direct integration with insurance providers
- [ ] **Document Upload**: AI-powered document analysis for claims
- [ ] **Video Guidance**: Interactive video tutorials for scheme applications

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **Mistral AI**: For providing the powerful language model
- **Ollama**: For local AI model deployment
- **Streamlit**: For the amazing web app framework
- **Government of India**: For insurance schemes data and information
- **Insurance Regulatory and Development Authority of India (IRDAI)**: For guidelines and standards

## Support & Contact

- **Issues**: Please report bugs and issues in the GitHub Issues section
- **Discussions**: Join our GitHub Discussions for questions and feature requests
- **Email**: [your-email@domain.com] for direct support

## 🌟 Star the Repository

If you find this project helpful, please consider giving it a star ⭐ on GitHub!

---

**Made with ❤️ for the Indian insurance community**

*Empowering financial security through AI-driven insurance guidance*
