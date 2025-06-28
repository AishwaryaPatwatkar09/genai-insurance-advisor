# GenAI Insurance Advisor

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![Mistral AI](https://img.shields.io/badge/AI-Mistral-orange.svg)](https://mistral.ai)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

AI-powered insurance recommendation platform leveraging Mistral LLM to provide personalized insurance advice for Indian government schemes and private insurance options.

## Project Overview

The GenAI Insurance Advisor is designed to democratize insurance knowledge in India by providing intelligent, personalized recommendations through advanced AI. The platform specializes in government-sponsored programs like PMSBY, PMJJBY, PMJAY, and Atal Pension Yojana, making insurance accessible to both rural and urban populations.

## Features

### Main AI Advisor
- Personalized insurance recommendations using Mistral AI
- Profile analysis based on age, income, location, family size, and health status
- Specialized knowledge of Indian government insurance schemes
- Smart fallback system with rule-based recommendations when AI is unavailable
- Direct integration with official application portals and bank locators

### Premium Calculator
- Interactive cost estimation across multiple insurance schemes
- Real-time calculation of total premiums and coverage amounts
- Comparison between government schemes and private insurance options
- Coverage optimization based on budget constraints
- Support for government schemes (PMSBY, PMJJBY, APY) and private add-ons

### Claim Assistant
- AI-powered troubleshooting for insurance claim issues
- Step-by-step guidance for PMSBY, PMJJBY, and PMJAY claims
- Document requirement checklists and submission procedures
- Official contact information and helpline numbers
- Common claim scenarios and resolution strategies

### Insurance Chatbot
- Real-time question answering about insurance policies
- Context-aware responses specific to Indian insurance market
- Persistent chat history for reference during sessions
- Fallback responses using cached knowledge base
- Support for scheme-specific queries and application guidance

### Personal Dashboard
- Visual overview of user insurance profile and recommendations
- Quick access to suggested schemes and their current status
- Coverage gap analysis and improvement suggestions
- Personalized action items and next steps
- Portfolio tracking and optimization recommendations

## Technology Stack

- **Frontend Framework**: Streamlit with custom theming
- **AI Model**: Mistral AI deployed via Ollama
- **Programming Language**: Python 3.8+
- **Performance Optimization**: Advanced caching system, async operations
- **Data Processing**: Efficient session management and state handling

## Installation and Setup

### Prerequisites
- Python 3.8 or higher
- 4GB+ RAM (recommended for optimal AI performance)
- Internet connection for AI features and external integrations

### Local Development Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/genai-insurance-advisor.git
cd genai-insurance-advisor

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install required dependencies
pip install -r requirements.txt

# Install and setup Ollama
# Visit https://ollama.ai for platform-specific installation instructions

# Download Mistral model
ollama pull mistral

# Run the application
streamlit run app.py
```

### Requirements File
```
streamlit>=1.28.0
ollama>=0.1.7
```

## Supported Insurance Schemes

### Government Schemes
| Scheme | Annual Premium | Coverage | Eligibility | Target Group |
|--------|---------------|----------|-------------|--------------|
| PMSBY | ₹20 | ₹2 Lakh accident protection | All bank account holders | Universal accident coverage |
| PMJJBY | ₹436 | ₹2 Lakh life insurance | Ages 18-50 with bank account | Family financial security |
| PMJAY | Free | ₹5 Lakh health coverage | Income-based eligibility | Eligible families below poverty line |
| APY | ₹42-₹291/month | ₹1,000-₹5,000 monthly pension | Ages 18-40 | Retirement planning |

### Additional Coverage Options
- Health insurance top-up plans
- Term life insurance policies
- State-specific insurance schemes
- Private insurance alternatives and comparisons

## How It Works

### User Journey
1. **Profile Creation**: Users input demographic and financial information including age, occupation, income, location, family size, and health status
2. **AI Analysis**: Mistral AI processes the profile data and generates personalized recommendations
3. **Recommendation Display**: System presents tailored insurance schemes with detailed explanations and cost breakdowns
4. **Interactive Tools**: Users can explore premium calculator, claim assistance, and chatbot features
5. **Action Planning**: Direct links to application portals and implementation guidance

### AI Integration
The platform uses Mistral AI with optimized prompts specifically designed for Indian insurance advisory. The system includes intelligent caching to improve response times and reduce API calls while maintaining high-quality recommendations.

## Performance Optimizations

- **Caching Strategy**: Static data cached indefinitely, AI responses cached for 30 minutes, fallback advice cached for 1 hour
- **Lazy Loading**: Components load only when accessed to improve initial load times
- **Session Management**: Efficient state handling to maintain user context across interactions
- **Fallback Systems**: Complete functionality maintained even when AI services are unavailable
- **Response Optimization**: Streamlined prompts and response formatting for faster processing

## Deployment

### Streamlit Cloud Deployment
1. Push your code to GitHub repository
2. Connect to Streamlit Cloud at share.streamlit.io
3. Deploy directly from your GitHub repository
4. Configure environment variables if needed

### Local Hosting
The application runs on localhost:8501 by default and can be configured for network access through Streamlit configuration.

## Project Structure

```
genai-insurance-advisor/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── README.md                # Project documentation
├── .gitignore               # Git ignore rules
├── .streamlit/              
│   └── config.toml          # Streamlit configuration
└── LICENSE                  # MIT license file
```

## Troubleshooting

### Common Issues
- **Ollama not found**: Ensure Ollama is properly installed and running
- **Mistral model unavailable**: Run `ollama pull mistral` to download the model
- **Slow performance**: Check system resources and consider caching optimization
- **Connection errors**: Verify internet connectivity for AI features

### Fallback Mode
The application includes comprehensive fallback functionality that provides intelligent recommendations even when AI services are unavailable, ensuring consistent user experience.

## Contributing

We welcome contributions to improve the platform. Please follow these guidelines:

1. Fork the repository and create a feature branch
2. Implement your changes with appropriate testing
3. Ensure code quality and documentation standards
4. Submit a pull request with detailed description of changes
5. Participate in code review process

### Areas for Contribution
- Additional insurance scheme integrations
- Multi-language support implementation
- Performance optimization improvements
- User interface and experience enhancements
- Testing and quality assurance

## License

This project is licensed under the MIT License. See the LICENSE file for complete terms and conditions.

## Acknowledgments

- Mistral AI for providing the advanced language model capabilities
- Ollama for local AI model deployment infrastructure
- Streamlit for the comprehensive web application framework
- Government of India for insurance scheme information and accessibility
- Insurance Regulatory and Development Authority of India (IRDAI) for guidelines

## Support and Contact

For issues, questions, or contributions:
- Create an issue in the GitHub repository
- Review the troubleshooting section for common problems
- Check Ollama and Streamlit documentation for technical details

**Built for the Indian insurance community - Making insurance accessible through AI**
