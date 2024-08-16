# Summer 2024 CS 3200 Finance Bros Repository

This repository is for the Finance Bros project, which is part of the Summer 2024 CS 3200 course. The project is designed to empower users to make strategic financial decisions by providing insights derived from top traders, political influencers, and comprehensive market analyses. It also includes an AI-powered chatbot that provides personalized financial advice to novice investors.

## Description

The Finance Bros project is a social media platform for finance enthusiasts that aims to help users make informed financial decisions. By offering detailed performance metrics and strategies from leading financial figures, the platform provides a unique perspective on investment opportunities. Users can stay informed with real-time data and trends, receive personalized recommendations, and follow the activities of influential traders. This platform is designed to guide both novice and experienced investors through the complexities of the financial market. Additionally, a financial consultant chatbot feature is available and is customized to each users needs.

## Getting Started

### Dependencies

* Python 3.8 or higher
* Flask 2.0.1
* SQLAlchemy 1.4
* PostgreSQL 13
* OpenAI API Key
* Streamlit 1.0.0
* Windows 10 or macOS 10.15 Catalina

### Installing

* Clone the repository from GitHub:
  \`\`\`
  git clone https://github.com/guenbr/cs3200-FinanceBros.git
  \`\`\`
* Set up a virtual environment and activate it:
  \`\`\`
  python -m venv venv
  source venv/bin/activate  # On Windows use `venv\\Scripts\\activate`
  \`\`\`
* Install the required dependencies:
  \`\`\`
  pip install -r requirements.txt
  \`\`\`
* Set up the PostgreSQL database and run the provided SQL script to create necessary tables:
  \`\`\`
  psql -U yourusername -d yourdatabase -f setup.sql
  \`\`\`
* Add your OpenAI API key to the Streamlit secrets:
  \`\`\`
  echo "[openai]\\nopenai_api_key=your_api_key_here" > .streamlit/secrets.toml
  \`\`\`

### Executing program

* Start the Flask development server:
  \`\`\`
  flask run
  \`\`\`
* Start the Streamlit application to use the financial consultation chatbot:
  \`\`\`
  streamlit run 97_reg_chatbot.py
  \`\`\`
* Access the application by navigating to \`http://127.0.0.1:8501/\` in your web browser.

## Help

For common issues:
* Ensure that PostgreSQL is correctly installed and the database is running.
* Virtual environment activation issues on Windows can be resolved by running:
  \`\`\`
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
  \`\`\`
* If you encounter issues with the OpenAI API, ensure that your API key is correctly set in the Streamlit secrets file.
* Check the Flask and Streamlit documentation for more details on error messages.

\`\`\`
flask --help
streamlit --help
\`\`\`

## Authors

* Bryan Guen  
* Ethan Xin  
* Eitan Berenfeld  
* Justin Iverson  
* Jared Mar  
* Daniel Klevak  

## Version History

* 0.3
    * Added AI-powered financial consultation chatbot feature
    * See [commit change](https://github.com/guenbr/cs3200-FinanceBros/commits/main) or [release history](https://github.com/guenbr/cs3200-FinanceBros/releases)
* 0.2
    * Various bug fixes and optimizations
* 0.1
    * Initial Release

## License

Not sure

## Acknowledgments

Not sure

* [awesome-readme](https://github.com/matiassingers/awesome-readme)
* [PurpleBooth](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2)
* [dbader](https://github.com/dbader/readme-template)
* [zenorocha](https://gist.github.com/zenorocha/4526327)
* [fvcproductions](https://gist.github.com/fvcproductions/1bfc2d4aecb01a834b46)
