import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json
from typing import Dict, List

# ============================================================================
# PAGE CONFIG & STYLING
# ============================================================================
st.set_page_config(
    page_title="AI Students Hub",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    [data-testid="stMainBlockContainer"] {
        padding: 2rem;
    }
    .metric-box {
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #e5e7eb;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    .card {
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #e5e7eb;
        background-color: #f9fafb;
        margin-bottom: 1rem;
    }
    .section-title {
        font-size: 1.875rem;
        font-weight: bold;
        margin-bottom: 1.5rem;
        color: #1f2937;
    }
    .stat-number {
        font-size: 2.25rem;
        font-weight: bold;
        color: #667eea;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# DATA STRUCTURES & CONSTANTS
# ============================================================================

GRADE_POINT_MAP = {
    'A+': 4.0, 'A': 4.0, 'A-': 3.7,
    'B+': 3.3, 'B': 3.0, 'B-': 2.7,
    'C+': 2.3, 'C': 2.0, 'C-': 1.7,
    'D+': 1.3, 'D': 1.0, 'F': 0.0,
}

MOTIVATIONAL_QUOTES = [
    {
        "quote": "Artificial intelligence is not a substitute for human intelligence; it is a tool to amplify human creativity and problem-solving.",
        "author": "Fei-Fei Li",
        "role": "Co-Director of Stanford Human-Centered AI Institute"
    },
    {
        "quote": "The magic of AI isn't in replacing programmers, but in elevating every programmer to solve problems at a higher level of abstraction.",
        "author": "Andrej Karpathy",
        "role": "AI Researcher & Educator"
    },
    {
        "quote": "Machine learning is the science of getting computers to act without being explicitly programmed.",
        "author": "Andrew Ng",
        "role": "Co-founder of Coursera & DeepLearning.AI"
    },
    {
        "quote": "Mathematics is the language with which God has written the universe; in AI, vectors and matrices are the brushstrokes.",
        "author": "Geoffrey Hinton",
        "role": "Turing Award Winner & Pioneer of Deep Learning"
    },
    {
        "quote": "Consistency is key in mastering AI. Studying 1 hour every day beats 10 hours once a week.",
        "author": "Yann LeCun",
        "role": "Chief AI Scientist at Meta"
    },
    {
        "quote": "The best way to predict the future is to invent it. Build projects, test hypotheses, and never stop learning.",
        "author": "Alan Kay",
        "role": "Computer Scientist"
    }
]

AI_NEWS = [
    {
        "id": "news-1",
        "title": "Gemini 2.5 & Multimodal Reasoning Benchmarks Released",
        "source": "Google DeepMind Blog",
        "date": "2026-07-20",
        "category": "LLMs",
        "summary": "New state-of-the-art benchmarks show significant advances in long-context multimodal reasoning, code generation efficiency, and agentic task execution.",
        "url": "https://deepmind.google/news/",
        "readTime": "4 min read"
    },
    {
        "id": "news-2",
        "title": "Open Source Llama 3.3 70B Benchmark Superiority",
        "source": "Meta AI Research",
        "date": "2026-07-18",
        "category": "Open Source",
        "summary": "Meta releases open weights for high-efficiency models optimized for desktop GPUs and local AI developer workstations, matching closed-source performance.",
        "url": "https://ai.meta.com/blog/",
        "readTime": "6 min read"
    },
    {
        "id": "news-3",
        "title": "Breakthrough in AI-Driven Synthetic Drug Discovery",
        "source": "MIT Technology Review",
        "date": "2026-07-15",
        "category": "Breakthroughs",
        "summary": "Researchers utilize deep generative protein folding models to design novel therapeutic enzymes targeting drug-resistant bacterial strains in record time.",
        "url": "https://www.technologyreview.com/topic/artificial-intelligence/",
        "readTime": "5 min read"
    },
    {
        "id": "news-4",
        "title": "Autonomous AI Coding Agents Achieve 85% SWE-Bench Score",
        "source": "AI Developer Digest",
        "date": "2026-07-10",
        "category": "Robotics",
        "summary": "Next-generation software engineering agents with iterative test-driven feedback loops pass complex multi-file GitHub issue benchmark suites.",
        "url": "https://arxiv.org/",
        "readTime": "7 min read"
    },
    {
        "id": "news-5",
        "title": "EU Artificial Intelligence Act Compliance Standard Finalized",
        "source": "Reuters Tech News",
        "date": "2026-07-05",
        "category": "Ethics",
        "summary": "Global tech companies align on safety evaluations, transparency disclosures, and risk mitigation frameworks for frontier AI models.",
        "url": "https://www.reuters.com/technology/",
        "readTime": "5 min read"
    },
    {
        "id": "news-6",
        "title": "Next-Gen Optical Neural Processing Units (NPUs) Hit 100 TFLOPS/Watt",
        "source": "IEEE Spectrum",
        "date": "2026-06-28",
        "category": "Hardware",
        "summary": "Photonic computing chips demonstrate ultra-low power consumption for matrix multiplication inference in edge AI hardware.",
        "url": "https://spectrum.ieee.org/topic/artificial-intelligence/",
        "readTime": "8 min read"
    }
]

ROADMAP_DATA = {
    "Programming": {
        "description": "Master essential programming concepts, data structures, and tools required for AI development.",
        "topics": [
            {"title": "Python Basics & Syntax", "desc": "Variables, loops, functions, lists, dicts, generators", "link": "https://docs.python.org/3/tutorial/"},
            {"title": "Object-Oriented Programming (OOP)", "desc": "Classes, inheritance, polymorphism, abstraction", "link": "https://realpython.com/python3-object-oriented-programming/"},
            {"title": "SQL & Database Querying", "desc": "SELECT, JOINs, aggregations, indexing", "link": "https://www.sqltutorial.org/"},
            {"title": "Git & GitHub Version Control", "desc": "Commits, branching, pull requests", "link": "https://git-scm.com/doc"},
        ]
    },
    "Mathematics": {
        "description": "Core mathematical concepts underpinning optimization, probability, and neural networks.",
        "topics": [
            {"title": "Calculus", "desc": "Derivatives, gradients, partial derivatives, chain rule", "link": "https://www.khanacademy.org/math/calculus-1"},
            {"title": "Linear Algebra", "desc": "Vectors, matrices, eigenvalues, eigenvectors, SVD", "link": "https://www.3blue1brown.com/topics/linear-algebra"},
            {"title": "Probability", "desc": "Bayes Theorem, random variables, probability distributions", "link": "https://www.khanacademy.org/math/statistics-probability"},
            {"title": "Statistics", "desc": "Hypothesis testing, confidence intervals, p-values", "link": "https://openintro.org/book/os/"},
        ]
    },
    "Data Analysis": {
        "description": "Tools for processing, inspecting, and visualizing datasets before training models.",
        "topics": [
            {"title": "NumPy", "desc": "N-dimensional arrays, broadcasting, vectorization", "link": "https://numpy.org/doc/stable/"},
            {"title": "Pandas", "desc": "DataFrames, Series, cleaning missing data, grouping", "link": "https://pandas.pydata.org/docs/"},
            {"title": "Matplotlib", "desc": "Line graphs, scatter plots, histograms, customization", "link": "https://matplotlib.org/stable/contents.html"},
            {"title": "Seaborn", "desc": "Statistical visualizations, heatmaps, pair plots", "link": "https://seaborn.pydata.org/"},
        ]
    },
    "Machine Learning": {
        "description": "Supervised and unsupervised learning algorithms and evaluation metrics.",
        "topics": [
            {"title": "Regression Models", "desc": "Linear, Polynomial, Ridge, Lasso, Logistic Regression", "link": "https://scikit-learn.org/stable/modules/linear_model.html"},
            {"title": "Classification", "desc": "Decision boundary, precision, recall, F1 score, ROC-AUC", "link": "https://scikit-learn.org/stable/modules/model_evaluation.html"},
            {"title": "Clustering", "desc": "K-Means, Hierarchical, DBSCAN, PCA", "link": "https://scikit-learn.org/stable/modules/clustering.html"},
            {"title": "Decision Trees & Ensembles", "desc": "Gini impurity, Random Forests, Gradient Boosting", "link": "https://scikit-learn.org/stable/modules/tree.html"},
        ]
    },
    "Deep Learning": {
        "description": "Neural networks, transformers, and advanced architectures for AI applications.",
        "topics": [
            {"title": "Neural Network Fundamentals", "desc": "Perceptrons, forward propagation, backpropagation", "link": "https://www.deeplearningbook.org/"},
            {"title": "Convolutional Neural Networks (CNNs)", "desc": "Convolution operation, pooling, architectures (ResNet, VGG)", "link": "https://www.tensorflow.org/tutorials/images/cnn"},
            {"title": "Recurrent Neural Networks (RNNs)", "desc": "LSTM, GRU, sequence-to-sequence models, attention", "link": "https://www.tensorflow.org/tutorials/sequences/text_classification_rnn"},
            {"title": "Transformers & LLMs", "desc": "Self-attention, BERT, GPT, fine-tuning, prompt engineering", "link": "https://huggingface.co/docs"},
        ]
    },
    "AI Specialisations": {
        "description": "Specialized domains in AI: NLP, Computer Vision, Reinforcement Learning, Robotics.",
        "topics": [
            {"title": "Natural Language Processing (NLP)", "desc": "Tokenization, embeddings, sentiment analysis, translation", "link": "https://huggingface.co/course"},
            {"title": "Computer Vision", "desc": "Image classification, object detection, segmentation, OCR", "link": "https://www.tensorflow.org/tutorials/images"},
            {"title": "Reinforcement Learning", "desc": "Q-learning, policy gradients, actor-critic methods", "link": "https://spinningup.openai.com/"},
            {"title": "Robotics & Autonomous Systems", "desc": "ROS, path planning, control systems, sensor fusion", "link": "https://www.ros.org/"},
        ]
    }
}

RESOURCES = [
    {"title": "Python Official Documentation", "category": "Programming", "url": "https://docs.python.org/3/", "tags": ["Python", "Core"]},
    {"title": "PyPI - Python Package Index", "category": "Programming", "url": "https://pypi.org/", "tags": ["Python", "Libraries"]},
    {"title": "Git Official Documentation", "category": "Programming", "url": "https://git-scm.com/doc", "tags": ["Git", "Version Control"]},
    {"title": "Khan Academy Mathematics", "category": "Mathematics", "url": "https://www.khanacademy.org/math", "tags": ["Calculus", "Algebra"]},
    {"title": "3Blue1Brown Math Visuals", "category": "Mathematics", "url": "https://www.3blue1brown.com/", "tags": ["Linear Algebra", "Visual"]},
    {"title": "NumPy Documentation", "category": "Data Analysis", "url": "https://numpy.org/doc/stable/", "tags": ["NumPy", "Arrays"]},
    {"title": "Pandas Documentation", "category": "Data Analysis", "url": "https://pandas.pydata.org/docs/", "tags": ["Pandas", "DataFrames"]},
    {"title": "Scikit-Learn", "category": "Machine Learning", "url": "https://scikit-learn.org/stable/", "tags": ["ML", "Algorithms"]},
    {"title": "TensorFlow Docs", "category": "Machine Learning", "url": "https://www.tensorflow.org/learn", "tags": ["TensorFlow", "Deep Learning"]},
    {"title": "PyTorch Documentation", "category": "Machine Learning", "url": "https://pytorch.org/docs/stable/", "tags": ["PyTorch", "Deep Learning"]},
]

CAREER_PATHS = [
    {
        "title": "Machine Learning Engineer",
        "salary": "$120K - $200K",
        "demand": "Very High",
        "skills": ["Python", "TensorFlow", "PyTorch", "SQL", "Statistics"],
        "courses": ["Deep Learning Specialization", "ML Engineering for Production"],
        "projects": ["Recommendation System", "Image Classification Model"]
    },
    {
        "title": "Data Scientist",
        "salary": "$100K - $180K",
        "demand": "Very High",
        "skills": ["Python", "SQL", "Statistics", "Data Visualization", "Pandas"],
        "courses": ["Statistics Fundamentals", "Data Science Professional Certificate"],
        "projects": ["Predictive Analytics Dashboard", "Customer Segmentation"]
    },
    {
        "title": "AI Research Scientist",
        "salary": "$130K - $220K",
        "demand": "High",
        "skills": ["Advanced Math", "Deep Learning", "Research", "PyTorch", "Paper Writing"],
        "courses": ["Advanced Deep Learning", "Research Methodology"],
        "projects": ["Novel Algorithm Implementation", "Benchmark Dataset"]
    },
    {
        "title": "NLP Engineer",
        "salary": "$115K - $200K",
        "demand": "High",
        "skills": ["Python", "NLP", "Transformers", "LLMs", "NLTK/spaCy"],
        "courses": ["NLP Specialization", "LLM Fine-tuning"],
        "projects": ["Chatbot Application", "Text Classification System"]
    },
    {
        "title": "Computer Vision Engineer",
        "salary": "$110K - $190K",
        "demand": "High",
        "skills": ["Python", "OpenCV", "CNNs", "Object Detection", "Image Processing"],
        "courses": ["Computer Vision Specialization", "Advanced CV Techniques"],
        "projects": ["Object Detection System", "Face Recognition App"]
    },
    {
        "title": "AI/ML Product Manager",
        "salary": "$130K - $210K",
        "demand": "Growing",
        "skills": ["Product Strategy", "Data Analysis", "ML Understanding", "Communication"],
        "courses": ["AI Product Management", "Technical PM"],
        "projects": ["Feature Prioritization", "ML Roadmap"]
    },
]

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

def init_session_state():
    """Initialize all session state variables"""
    if 'assignments' not in st.session_state:
        st.session_state.assignments = []
    if 'study_sessions' not in st.session_state:
        st.session_state.study_sessions = []
    if 'courses' not in st.session_state:
        st.session_state.courses = []
    if 'projects' not in st.session_state:
        st.session_state.projects = []
    if 'certificates' not in st.session_state:
        st.session_state.certificates = []
    if 'roadmap_progress' not in st.session_state:
        st.session_state.roadmap_progress = {}
    if 'bookmarked_resources' not in st.session_state:
        st.session_state.bookmarked_resources = set()
    if 'bookmarked_news' not in st.session_state:
        st.session_state.bookmarked_news = set()
    if 'watched_videos' not in st.session_state:
        st.session_state.watched_videos = set()
    if 'settings' not in st.session_state:
        st.session_state.settings = {
            'student_name': 'Hadia Salman',
            'degree': 'BS Artificial Intelligence',
            'target_gpa': 3.8,
            'weekly_study_hours': 15.0,
            'dark_mode': False,
            'sound_effects': True
        }

init_session_state()

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def calculate_gpa(courses: List[Dict]) -> Dict:
    """Calculate GPA from courses"""
    if not courses:
        return {
            'total_credits': 0,
            'gpa': 0.0,
            'course_count': 0,
            'grade_distribution': {}
        }
    
    total_credits = 0
    total_points = 0
    grade_dist = {}
    
    for course in courses:
        credits = max(1, course.get('credit_hours', 1))
        grade = course.get('grade', 'F').upper()
        point = GRADE_POINT_MAP.get(grade, 0.0)
        
        total_credits += credits
        total_points += credits * point
        grade_dist[grade] = grade_dist.get(grade, 0) + 1
    
    gpa = total_points / total_credits if total_credits > 0 else 0
    
    return {
        'total_credits': total_credits,
        'gpa': round(gpa, 2),
        'course_count': len(courses),
        'grade_distribution': grade_dist
    }

def calculate_weekly_study_hours(sessions: List[Dict]) -> float:
    """Calculate total study hours this week"""
    today = datetime.now()
    week_start = today - timedelta(days=today.weekday())
    
    total_hours = 0
    for session in sessions:
        try:
            session_date = datetime.strptime(session.get('date', ''), '%Y-%m-%d')
            if session_date >= week_start:
                total_hours += session.get('duration_minutes', 0) / 60
        except:
            pass
    
    return round(total_hours, 1)

def get_roadmap_progress() -> float:
    """Calculate overall roadmap completion percentage"""
    if not st.session_state.roadmap_progress:
        return 0
    
    total = sum(len(category.get('topics', [])) for category in ROADMAP_DATA.values())
    completed = sum(st.session_state.roadmap_progress.values())
    
    return round((completed / total * 100) if total > 0 else 0, 1)

# ============================================================================
# PAGE: DASHBOARD
# ============================================================================

def dashboard_page():
    st.markdown('<h1 class="section-title">📊 Dashboard</h1>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📚 Total Assignments", len(st.session_state.assignments))
    with col2:
        st.metric("⏱️ Study Sessions", len(st.session_state.study_sessions))
    with col3:
        gpa_info = calculate_gpa(st.session_state.courses)
        st.metric("🎯 Current GPA", f"{gpa_info['gpa']:.2f}")
    with col4:
        st.metric("📈 Roadmap Progress", f"{get_roadmap_progress():.1f}%")
    
    st.divider()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Weekly Study Hours")
        weekly = calculate_weekly_study_hours(st.session_state.study_sessions)
        st.metric("Target", f"{st.session_state.settings['weekly_study_hours']:.0f}h", 
                  delta=f"{weekly:.1f}h actual")
        
        if st.session_state.study_sessions:
            dates = [s.get('date', '') for s in st.session_state.study_sessions[-7:]]
            hours = [s.get('duration_minutes', 0)/60 for s in st.session_state.study_sessions[-7:]]
            
            df_chart = pd.DataFrame({'Date': dates, 'Hours': hours})
            st.bar_chart(df_chart.set_index('Date'))
    
    with col2:
        st.subheader("Assignment Status")
        if st.session_state.assignments:
            statuses = {}
            for a in st.session_state.assignments:
                status = a.get('status', 'Not Started')
                statuses[status] = statuses.get(status, 0) + 1
            
            df_status = pd.DataFrame(list(statuses.items()), columns=['Status', 'Count'])
            st.bar_chart(df_status.set_index('Status'))
        else:
            st.info("No assignments yet. Add some to see the breakdown!")
    
    with col3:
        st.subheader("Grade Distribution")
        gpa_info = calculate_gpa(st.session_state.courses)
        if gpa_info['grade_distribution']:
            df_grades = pd.DataFrame(list(gpa_info['grade_distribution'].items()), columns=['Grade', 'Count'])
            st.bar_chart(df_grades.set_index('Grade'))
        else:
            st.info("Add courses to see grade distribution!")
    
    st.divider()
    
    quote = MOTIVATIONAL_QUOTES[datetime.now().day % len(MOTIVATIONAL_QUOTES)]
    st.markdown(f"""
    <div class="card">
        <h3>💡 Daily Inspiration</h3>
        <p><em>"{quote['quote']}"</em></p>
        <p><strong>— {quote['author']}</strong><br><span style="font-size: 0.9rem; color: #666;">{quote['role']}</span></p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# PAGE: ASSIGNMENTS
# ============================================================================

def assignments_page():
    st.markdown('<h1 class="section-title">📋 Assignments</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("➕ Add Assignment", use_container_width=True):
            st.session_state.show_assignment_form = not st.session_state.get('show_assignment_form', False)
    
    if st.session_state.get('show_assignment_form', False):
        st.markdown("### Add New Assignment")
        with st.form("assignment_form"):
            title = st.text_input("Assignment Title")
            subject = st.text_input("Subject")
            due_date = st.date_input("Due Date")
            priority = st.selectbox("Priority", ["Low", "Medium", "High", "Urgent"])
            status = st.selectbox("Status", ["Not Started", "In Progress", "Submitted", "Graded"])
            notes = st.text_area("Notes")
            
            if st.form_submit_button("Save Assignment"):
                st.session_state.assignments.append({
                    'id': f"assign-{len(st.session_state.assignments)}",
                    'title': title,
                    'subject': subject,
                    'due_date': str(due_date),
                    'priority': priority,
                    'status': status,
                    'notes': notes,
                    'created_at': datetime.now().isoformat()
                })
                st.session_state.show_assignment_form = False
                st.success("Assignment added!")
                st.rerun()
    
    if st.session_state.assignments:
        st.subheader(f"Total Assignments: {len(st.session_state.assignments)}")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            filter_subject = st.multiselect("Filter by Subject", 
                                           list(set(a['subject'] for a in st.session_state.assignments)))
        with col2:
            filter_priority = st.multiselect("Filter by Priority",
                                           ["Low", "Medium", "High", "Urgent"])
        with col3:
            filter_status = st.multiselect("Filter by Status",
                                          ["Not Started", "In Progress", "Submitted", "Graded"])
        
        for i, assignment in enumerate(st.session_state.assignments):
            should_display = True
            if filter_subject and assignment['subject'] not in filter_subject:
                should_display = False
            if filter_priority and assignment['priority'] not in filter_priority:
                should_display = False
            if filter_status and assignment['status'] not in filter_status:
                should_display = False
            
            if should_display:
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.markdown(f"""
                    <div class="card">
                        <h4>{assignment['title']}</h4>
                        <p><strong>Subject:</strong> {assignment['subject']}</p>
                        <p><strong>Due:</strong> {assignment['due_date']} | <strong>Priority:</strong> {assignment['priority']}</p>
                        <p><strong>Status:</strong> {assignment['status']}</p>
                        {f'<p><strong>Notes:</strong> {assignment["notes"]}</p>' if assignment.get('notes') else ''}
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    if st.button("✏️", key=f"edit_{i}"):
                        st.session_state[f'edit_assignment_{i}'] = True
                with col3:
                    if st.button("🗑️", key=f"delete_{i}"):
                        st.session_state.assignments.pop(i)
                        st.rerun()
    else:
        st.info("No assignments yet. Add one to get started!")

# ============================================================================
# PAGE: ROADMAP
# ============================================================================

def roadmap_page():
    st.markdown('<h1 class="section-title">🗺️ Learning Roadmap</h1>', unsafe_allow_html=True)
    
    overall_progress = get_roadmap_progress()
    st.progress(overall_progress / 100)
    st.metric("Overall Progress", f"{overall_progress:.1f}%")
    
    st.divider()
    
    for category, data in ROADMAP_DATA.items():
        with st.expander(f"📚 {category} - {data['description']}", expanded=False):
            st.write(data['description'])
            
            for topic in data['topics']:
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.markdown(f"**{topic['title']}**  \n{topic['desc']}")
                
                with col2:
                    topic_key = f"{category}_{topic['title']}"
                    is_completed = st.session_state.roadmap_progress.get(topic_key, False)
                    
                    if st.checkbox("Completed", value=is_completed, key=f"roadmap_{topic_key}"):
                        st.session_state.roadmap_progress[topic_key] = True
                    elif is_completed:
                        st.session_state.roadmap_progress[topic_key] = False
                
                with col3:
                    st.link_button("📖 Learn", topic['link'])

# ============================================================================
# PAGE: STUDY PLANNER
# ============================================================================

def study_planner_page():
    st.markdown('<h1 class="section-title">📅 Study Planner</h1>', unsafe_allow_html=True)
    
    if st.button("➕ Log Study Session"):
        st.session_state.show_study_form = not st.session_state.get('show_study_form', False)
    
    if st.session_state.get('show_study_form', False):
        st.markdown("### Log Study Session")
        with st.form("study_form"):
            topic = st.text_input("Topic")
            date = st.date_input("Date")
            duration = st.number_input("Duration (minutes)", min_value=1, step=15)
            session_type = st.selectbox("Session Type", ["Lecture", "Coding", "Reading", "Revision", "Project"])
            notes = st.text_area("Notes")
            
            if st.form_submit_button("Log Session"):
                st.session_state.study_sessions.append({
                    'id': f"sess-{len(st.session_state.study_sessions)}",
                    'topic': topic,
                    'date': str(date),
                    'duration_minutes': duration,
                    'type': session_type,
                    'notes': notes
                })
                st.session_state.show_study_form = False
                st.success("Study session logged!")
                st.rerun()
    
    st.divider()
    
    if st.session_state.study_sessions:
        st.subheader(f"Total Sessions: {len(st.session_state.study_sessions)}")
        
        col1, col2, col3 = st.columns(3)
        weekly_hours = calculate_weekly_study_hours(st.session_state.study_sessions)
        with col1:
            st.metric("This Week", f"{weekly_hours:.1f}h")
        with col2:
            avg_session = sum(s['duration_minutes'] for s in st.session_state.study_sessions) / len(st.session_state.study_sessions) / 60
            st.metric("Avg Session", f"{avg_session:.1f}h")
        with col3:
            st.metric("Total Hours", f"{sum(s['duration_minutes'] for s in st.session_state.study_sessions) / 60:.1f}h")
        
        st.divider()
        
        for i, session in enumerate(reversed(st.session_state.study_sessions)):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"""
                <div class="card">
                    <h4>{session['topic']}</h4>
                    <p><strong>Date:</strong> {session['date']} | <strong>Duration:</strong> {session['duration_minutes']} min | <strong>Type:</strong> {session['type']}</p>
                    {f'<p><strong>Notes:</strong> {session["notes"]}</p>' if session.get('notes') else ''}
                </div>
                """, unsafe_allow_html=True)
            with col2:
                if st.button("🗑️", key=f"delete_study_{i}"):
                    st.session_state.study_sessions.pop(i)
                    st.rerun()
    else:
        st.info("No study sessions yet. Start logging to track your progress!")

# ============================================================================
# PAGE: GPA CALCULATOR
# ============================================================================

def gpa_calculator_page():
    st.markdown('<h1 class="section-title">🎯 GPA Calculator</h1>', unsafe_allow_html=True)
    
    if st.button("➕ Add Course"):
        st.session_state.show_course_form = not st.session_state.get('show_course_form', False)
    
    if st.session_state.get('show_course_form', False):
        st.markdown("### Add Course")
        with st.form("course_form"):
            course_name = st.text_input("Course Name")
            credit_hours = st.number_input("Credit Hours", min_value=1, max_value=4, value=3, step=0.5)
            grade = st.selectbox("Grade", list(GRADE_POINT_MAP.keys()))
            
            if st.form_submit_button("Add Course"):
                st.session_state.courses.append({
                    'id': f"crs-{len(st.session_state.courses)}",
                    'course_name': course_name,
                    'credit_hours': credit_hours,
                    'grade': grade
                })
                st.session_state.show_course_form = False
                st.success("Course added!")
                st.rerun()
    
    st.divider()
    
    gpa_info = calculate_gpa(st.session_state.courses)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("GPA", f"{gpa_info['gpa']:.2f}")
    with col2:
        st.metric("Total Credits", gpa_info['total_credits'])
    with col3:
        st.metric("Courses", gpa_info['course_count'])
    with col4:
        target = st.session_state.settings.get('target_gpa', 0)
        if target > 0:
            st.metric("Target", target, delta=f"{gpa_info['gpa'] - target:.2f}")
    
    st.divider()
    
    if st.session_state.courses:
        st.subheader("Courses")
        
        df_data = []
        for i, course in enumerate(st.session_state.courses):
            df_data.append({
                'Course': course['course_name'],
                'Grade': course['grade'],
                'Credit Hours': course['credit_hours'],
                'Points': course['credit_hours'] * GRADE_POINT_MAP.get(course['grade'], 0)
            })
        
        df = pd.DataFrame(df_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.divider()
        
        for i in range(len(st.session_state.courses)):
            col1, col2 = st.columns([4, 1])
            course = st.session_state.courses[i]
            with col1:
                st.write(f"**{course['course_name']}** — Grade: {course['grade']} ({course['credit_hours']} Credits)")
            with col2:
                if st.button("🗑️", key=f"delete_course_{i}"):
                    st.session_state.courses.pop(i)
                    st.rerun()
    else:
        st.info("No courses added yet. Click 'Add Course' to start calculating your GPA!")

# ============================================================================
# PAGE: RESOURCES & NEWS
# ============================================================================

def resources_page():
    st.markdown('<h1 class="section-title">📚 Resources & AI News</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📖 Learning Resources", "📰 AI News & Trends", "💼 Career Paths"])
    
    with tab1:
        st.subheader("Curated Learning Resources")
        selected_cat = st.selectbox("Filter Category", ["All"] + list(ROADMAP_DATA.keys()))
        
        for res in RESOURCES:
            if selected_cat == "All" or res['category'] == selected_cat:
                with st.container():
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.markdown(f"**{res['title']}** ({res['category']})")
                        st.caption(f"Tags: {', '.join(res['tags'])}")
                    with col2:
                        st.link_button("Visit", res['url'])
                st.divider()

    with tab2:
        st.subheader("Latest Artificial Intelligence News")
        for item in AI_NEWS:
            with st.container():
                st.markdown(f"### {item['title']}")
                st.caption(f"Source: {item['source']} | Date: {item['date']} | Category: {item['category']}")
                st.write(item['summary'])
                st.link_button("Read Full Article", item['url'])
            st.divider()

    with tab3:
        st.subheader("AI Career Paths & Demands")
        for career in CAREER_PATHS:
            with st.expander(f"{career['title']} — Average Salary: {career['salary']} (Demand: {career['demand']})"):
                st.write(f"**Key Skills:** {', '.join(career['skills'])}")
                st.write(f"**Recommended Courses:** {', '.join(career['courses'])}")
                st.write(f"**Suggested Projects:** {', '.join(career['projects'])}")

# ============================================================================
# PAGE: SETTINGS
# ============================================================================

def settings_page():
    st.markdown('<h1 class="section-title">⚙️ Settings & Profile</h1>', unsafe_allow_html=True)
    
    with st.form("settings_form"):
        student_name = st.text_input("Student Name", value=st.session_state.settings['student_name'])
        degree = st.text_input("Degree Program", value=st.session_state.settings['degree'])
        target_gpa = st.number_input("Target GPA", min_value=0.0, max_value=4.0, value=float(st.session_state.settings['target_gpa']), step=0.05)
        weekly_study_hours = st.number_input("Weekly Study Hours Target", min_value=0.0, value=float(st.session_state.settings['weekly_study_hours']), step=1.0)
        
        if st.form_submit_button("Save Settings"):
            st.session_state.settings['student_name'] = student_name
            st.session_state.settings['degree'] = degree
            st.session_state.settings['target_gpa'] = target_gpa
            st.session_state.settings['weekly_study_hours'] = weekly_study_hours
            st.success("Settings updated successfully!")
            st.rerun()

# ============================================================================
# MAIN NAVIGATION SETUP
# ============================================================================

def main():
    st.sidebar.title("🎓 AI Students Hub")
    st.sidebar.markdown(f"**Welcome, {st.session_state.settings['student_name']}!**")
    st.sidebar.caption(st.session_state.settings['degree'])
    
    st.sidebar.divider()
    
    page = st.sidebar.radio(
        "Navigation",
        ["Dashboard", "Assignments", "Roadmap", "Study Planner", "GPA Calculator", "Resources & News", "Settings"]
    )
    
    st.sidebar.divider()
    st.sidebar.markdown("### Quick Stats")
    st.sidebar.metric("Assignments Due", len([a for a in st.session_state.assignments if a.get('status') != 'Graded']))
    st.sidebar.metric("Roadmap Progress", f"{get_roadmap_progress():.1f}%")
    
    if page == "Dashboard":
        dashboard_page()
    elif page == "Assignments":
        assignments_page()
    elif page == "Roadmap":
        roadmap_page()
    elif page == "Study Planner":
        study_planner_page()
    elif page == "GPA Calculator":
        gpa_calculator_page()
    elif page == "Resources & News":
        resources_page()
    elif page == "Settings":
        settings_page()

if __name__ == "__main__":
    main()
