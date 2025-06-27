import pandas as pd
import spacy
from spacy.matcher import PhraseMatcher
from pdfminer.high_level import extract_text
from io import StringIO
import docx2txt
# Load spaCy model
nlp = spacy.load("en_core_web_sm")


skills_list = [
    # Programming Languages
    "python", "java", "c++", "c#", "c", "javascript", "typescript", 
    "go", "rust", "kotlin", "swift", "php", "ruby", "scala", "r",
    "matlab", "perl", "dart", "elixir", "haskell", "clojure",
    "objective-c", "vb.net", "assembly", "cobol", "fortran",
    
    # Web Development
    "html", "css", "react", "angular", "vue.js", "node.js", "express.js",
    "next.js", "nuxt.js", "svelte", "bootstrap", "tailwind css",
    "sass", "less", "webpack", "vite", "jquery", "asp.net",
    "spring boot", "laravel", "symfony", "codeigniter", "rails",
    "sinatra", "gin", "fiber", "echo",
    
    # Backend Frameworks
    "firebase", "fastapi", "django", "flask", "spring", "spring boot",
    "express", "nest.js", "koa", "hapi", "restify", "actix",
    "rocket", "axum", "warp", "tide",
    
    # Mobile Development
    "react native", "flutter", "ionic", "xamarin", "cordova",
    "android", "ios", "swift ui", "jetpack compose",
    
    # Data Science & AI/ML
    "machine learning", "deep learning", "nlp", "computer vision",
    "data science", "data analysis", "statistics", "artificial intelligence",
    "neural networks", "reinforcement learning", "tensorflow", "pytorch",
    "keras", "scikit-learn", "xgboost", "lightgbm", "catboost",
    "numpy", "pandas", "matplotlib", "seaborn", "plotly", "bokeh",
    "scipy", "statsmodels", "opencv", "pillow", "hugging face",
    "transformers", "spacy", "nltk", "gensim", "langchain",
    "jupyter", "colab", "anaconda", "mlflow", "wandb", "tensorboard",
    
    # Databases
    "sql", "mysql", "postgresql", "sqlite", "oracle", "sql server",
    "mongodb", "cassandra", "couchdb", "redis", "memcached",
    "elasticsearch", "solr", "neo4j", "dynamodb", "firestore",
    "supabase", "planetscale", "cockroachdb", "mariadb",
    
    # Cloud & DevOps
    "aws", "gcp", "google cloud", "azure", "docker", "kubernetes",
    "terraform", "ansible", "jenkins", "github actions", "gitlab ci",
    "circleci", "travis ci", "helm", "istio", "prometheus",
    "grafana", "elk stack", "datadog", "new relic", "sentry",
    "cloudflare", "netlify", "vercel", "heroku", "digitalocean",
    
    # Version Control & Collaboration
    "git", "github", "gitlab", "bitbucket", "svn", "mercurial",
    "jira", "confluence", "slack", "teams", "discord", "notion",
    
    # Operating Systems & Tools
    "linux", "ubuntu", "centos", "debian", "fedora", "arch linux",
    "macos", "windows", "bash", "zsh", "powershell", "cmd",
    "vim", "emacs", "vscode", "intellij", "pycharm", "eclipse",
    "sublime text", "atom", "webstorm", "phpstorm",
    
    # Data Visualization & BI
    "excel", "power bi", "tableau", "qlik", "looker", "metabase",
    "grafana", "d3.js", "chart.js", "highcharts", "plotly dash",
    "streamlit", "shiny", "jupyter notebooks",
    
    # Testing & Quality Assurance
    "unit testing", "integration testing", "selenium", "cypress",
    "jest", "mocha", "chai", "pytest", "junit", "testng",
    "cucumber", "postman", "insomnia", "swagger", "api testing",
    "load testing", "performance testing", "security testing",
    
    # Security
    "cybersecurity", "penetration testing", "ethical hacking",
    "owasp", "ssl/tls", "oauth", "jwt", "encryption", "firewall",
    "vulnerability assessment", "security auditing",
    
    # Blockchain & Cryptocurrency
    "blockchain", "ethereum", "solidity", "web3", "defi", "nft",
    "smart contracts", "bitcoin", "hyperledger", "truffle",
    
    # Game Development
    "unity", "unreal engine", "godot", "pygame", "love2d",
    "phaser", "three.js", "webgl", "opengl", "directx",
    
    # Big Data & Analytics
    "hadoop", "spark", "kafka", "airflow", "dbt", "snowflake",
    "databricks", "bigquery", "redshift", "hive", "pig",
    "storm", "flink", "nifi", "luigi", "prefect",
    
    # API & Integration
    "rest api", "graphql", "grpc", "soap", "webhooks",
    "microservices", "api gateway", "message queues",
    "rabbitmq", "apache kafka", "celery", "sidekiq",
    
    # Specialized Tools & Frameworks
    "opencv", "ffmpeg", "imagemagick", "pil", "wand",
    "beautifulsoup", "scrapy", "requests", "urllib", "httpx",
    "aiohttp", "twisted", "tornado", "gunicorn", "uwsgi",
    "nginx", "apache", "caddy", "traefik",
    
    # Emerging Technologies
    "iot", "edge computing", "serverless", "lambda functions",
    "api gateway", "event-driven architecture", "microservices",
    "containerization", "orchestration", "service mesh",

    #skill not defined before
    "oops", "object oriented programming"
]

patterns = [nlp.make_doc(skill.lower()) for skill in skills_list]

# Setup matcher
matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
matcher.add("SKILL", patterns)


def extract_skills_from_resume(text, skills_list):
    # Apply matcher
    doc = nlp(text.lower())
    matches = matcher(doc)

    # Extract matched skills
    found_skills = set([doc[start:end].text.lower() for _, start, end in matches])

    return sorted(set(found_skills))



# Example usage
df=pd.read_csv('./sample data/UpdatedResumeDataSet.csv')


def extract_text_from_file(uploaded_file):
    if uploaded_file is None:
        return ""

    file_type = uploaded_file.name.split('.')[-1].lower()

    # Handle text file
    if file_type == 'txt':
        stringio = StringIO(uploaded_file.read().decode("utf-8"))
        return stringio.read()

    # Handle docx file
    elif file_type == 'docx':
        return docx2txt.process(uploaded_file)

    # Handle PDF file
    elif file_type == 'pdf':
        text = extract_text(uploaded_file)
        return text

    else:
        return ""

def user_skill(text):
    user_skills=extract_skills_from_resume(text,skills_list)
    return user_skills

def job_description_skill(skills_list):
    df=pd.read_csv('./sample data/UpdatedResumeDataSet.csv')
    df['Required Skills']=df['Resume'].apply(lambda x:extract_skills_from_resume(str(x), skills_list))
    return df