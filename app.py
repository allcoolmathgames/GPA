from flask import Flask, render_template, request, jsonify, url_for, redirect, send_from_directory, Blueprint, session

# Create a Flask app instance
app = Flask(__name__)
app.secret_key = 'your_secret_key_here' # Session ke liye secret key zaroori hai

# Dummy data store (real project mein database use hoga)
courses_data = [] # For Page 1

# Supported languages list
SUPPORTED_LANGS = ['en', 'ar', 'es', 'de', 'pt', 'ru']

# --- Helper function to get correct template name ---
def get_template_name(base_path, lang_code):
    if lang_code == 'en':
        return f'{base_path}.html'
    return f'{base_path}_{lang_code}.html'

# --- Blueprints for better organization ---
lang_routes = Blueprint('lang_routes', __name__, url_prefix='/<lang_code>')
static_pages = Blueprint('static_pages', __name__)
api_routes = Blueprint('api_routes', __name__)
blog_routes = Blueprint('blog_routes', __name__, url_prefix='/blogs')
redirect_routes = Blueprint('redirect_routes', __name__)

# --- Routes for pages (Dynamic language support) ---
@lang_routes.before_request
def check_lang_code():
    lang_code = request.view_args.get('lang_code')
    if lang_code not in SUPPORTED_LANGS:
        return "Language not supported", 404

# Home page route for ENGLISH (no lang_code in URL)
@app.route('/')
def home():
    template_name = get_template_name('home/index', 'en')
    session['lang_code'] = 'en'
    return render_template(template_name, lang_code='en')

# Home page route for other languages (with lang_code in URL)
@lang_routes.route('/')
def index(lang_code):
    template_name = get_template_name('home/index', lang_code)
    session['lang_code'] = lang_code
    return render_template(template_name, lang_code=lang_code)

@app.route('/set-language/<lang_code>')
def set_language(lang_code):
    if lang_code in SUPPORTED_LANGS:
        session['lang_code'] = lang_code
    redirect_to = request.args.get('redirect_to')
    if redirect_to:
        if lang_code == 'en':
            # Remove /en from path if it exists
            return redirect(redirect_to.replace('/en/', '/') if redirect_to.startswith('/en/') else redirect_to)
        return redirect(f'/{lang_code}{redirect_to}')
    return redirect(url_for('home'))

# GPA Calculator route for English (no lang_code in URL)
@app.route('/gpa-calculator')
def gpa_calculator_en():
    template_name = get_template_name('gpacalculator/gpa-calculator', 'en')
    session['lang_code'] = 'en'
    return render_template(template_name, lang_code='en')

# GPA Calculator route for all other languages (with lang_code in URL)
@lang_routes.route('/gpa-calculator')
def gpa_calculator(lang_code):
    template_name = get_template_name('gpacalculator/gpa-calculator', lang_code)
    session['lang_code'] = lang_code
    return render_template(template_name, lang_code=lang_code)

@app.route('/final-grade-calculator')
def final_grade_calculator_en():
    template_name = get_template_name('finalgrade/finalgradecalculator', 'en')
    session['lang_code'] = 'en'
    return render_template(template_name, lang_code='en')

@lang_routes.route('/final-grade-calculator')
def final_grade_calculator(lang_code):
    template_name = get_template_name('finalgrade/finalgradecalculator', lang_code)
    session['lang_code'] = lang_code
    return render_template(template_name, lang_code=lang_code)
    
# --- Naye routes yahan add kiye gaye hain taake English ka URL theek ho ---
@app.route('/prior-semester-gpa')
def prior_semester_gpa_en():
    template_name = get_template_name('prior-semester-gpa/prior-semester-gpa', 'en')
    session['lang_code'] = 'en'
    return render_template(template_name, lang_code='en')

@lang_routes.route('/prior-semester-gpa')
def prior_semester_gpa(lang_code):
    template_name = get_template_name('prior-semester-gpa/prior-semester-gpa', lang_code)
    session['lang_code'] = lang_code
    return render_template(template_name, lang_code=lang_code)

@app.route('/highschool-gpa')
def highschool_gpa_en():
    template_name = get_template_name('highschool/highschool', 'en')
    session['lang_code'] = 'en'
    return render_template(template_name, lang_code='en')

@lang_routes.route('/highschool-gpa')
def highschool_gpa(lang_code):
    template_name = get_template_name('highschool/highschool', lang_code)
    session['lang_code'] = lang_code
    return render_template(template_name, lang_code=lang_code)

@app.route('/grade-calculator')
def grade_calculator_en():
    template_name = get_template_name('gradecalculator/gradecalculator', 'en')
    session['lang_code'] = 'en'
    return render_template(template_name, lang_code='en')

@lang_routes.route('/grade-calculator')
def grade_calculator(lang_code):
    template_name = get_template_name('gradecalculator/gradecalculator', lang_code)
    session['lang_code'] = lang_code
    return render_template(template_name, lang_code=lang_code)
    
@app.route('/gpa-planning')
def gpa_planning_en():
    template_name = get_template_name('gpaplan/gpa-planning-calculator', 'en')
    session['lang_code'] = 'en'
    return render_template(template_name, lang_code='en')
    
@lang_routes.route('/gpa-planning')
def gpa_planning(lang_code):
    template_name = get_template_name('gpaplan/gpa-planning-calculator', lang_code)
    session['lang_code'] = lang_code
    return render_template(template_name, lang_code=lang_code)

# --- New routes for Semester Grade Calculator ---
@app.route('/semester-grade-calculator')
def semester_grade_calculator_en():
    template_name = get_template_name('samesterGradeCalcuator/samesterGradecalculator', 'en')
    session['lang_code'] = 'en'
    return render_template(template_name, lang_code='en')

@lang_routes.route('/semester-grade-calculator')
def semester_grade_calculator(lang_code):
    template_name = get_template_name('samesterGradeCalcuator/samesterGradecalculator', lang_code)
    session['lang_code'] = lang_code
    return render_template(template_name, lang_code=lang_code)
    
# --- Sitemap Route (static) ---
@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory(app.root_path, 'sitemap.xml')

# --- Blog Routes (static) ---
@blog_routes.route('/')
def blog_index():
    return render_template('blogs/blog_index.html')

@blog_routes.route('/<slug>')
def blog_post(slug):
    blog_templates = {
        'how-to-improve-your-gpa-effectively': 'blogs/gpa_blog.html',
        'understanding-different-grading-scales': 'blogs/final_gpa_blog.html',
        'achieving-your-target-gpa-guide': 'blogs/target_gpa_blog.html'
    }
    
    template_to_render = blog_templates.get(slug)
    
    if template_to_render:
        return render_template(template_to_render, slug=slug)
    else:
        return "Blog Post Not Found", 404

# --- Other Static Pages ---
@static_pages.route('/privacy-policy')
def privacy_policy():
    return render_template('pages/privacy-policy.html')

@static_pages.route('/terms-conditions')
def terms_conditions():
    return render_template('pages/terms-conditions.html')

@static_pages.route('/about-us')
def about_us():
    return render_template('pages/About-us.html')

@static_pages.route('/contact')
def contact():
    return render_template('pages/Contact.html')

# --- API Endpoints ---
# (Yahan aapke saare API routes hain, unko maine change nahi kiya kyunke masla routing mein tha)
# --- Helper function to calculate GPA ---
def calculate_gpa_from_courses():
    total_grade_points = 0
    total_credits = 0
    grade_map = {
        'A+': 4.0, 'A': 4.0, 'A-': 3.7,
        'B+': 3.3, 'B': 3.0, 'B-': 2.7,
        'C+': 2.3, 'C': 2.0, 'C-': 1.7,
        'D+': 1.3, 'D': 1.0, 'D-': 0.7,
        'F': 0.0
    }

    for course in courses_data:
        if 'grade' in course and course['grade'] in grade_map and \
           'credits' in course and isinstance(course['credits'], (int, float)):
            grade_points = grade_map[course['grade']] * course['credits']
            total_grade_points += grade_points
            total_credits += course['credits']

    if total_credits == 0:
        return 0.0
    return round(total_grade_points / total_credits, 2)

@api_routes.route('/get_courses', methods=['GET'])
def get_courses():
    return jsonify({'status': 'success', 'courses': courses_data, 'currentGpa': calculate_gpa_from_courses()})

@api_routes.route('/add_course', methods=['POST'])
def add_course():
    data = request.json
    course_name = data.get('courseName')
    credits = data.get('credits')
    grade = data.get('grade')
    grade_map_keys = {'A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'D-', 'F'}
    
    if not course_name or not grade:
        return jsonify({'status': 'error', 'message': 'Course Name and Grade are required.'}), 400
    try:
        credits = float(credits)
        if credits <= 0:
            return jsonify({'status': 'error', 'message': 'Credits must be a positive number.'}), 400
    except (ValueError, TypeError):
        return jsonify({'status': 'error', 'message': 'Invalid Credits value.'}), 400
    
    if grade not in grade_map_keys:
        return jsonify({'status': 'error', 'message': 'Invalid Grade. Allowed grades are A+, A, A-, B+, B, B-', 'C+': 2.3, 'C': 2.0, 'C-': 1.7, 'D+': 1.3, 'D': 1.0, 'D-': 0.7, 'F': 0.0}), 400

    courses_data.append({'name': course_name, 'credits': credits, 'grade': grade})
    
    return jsonify({'status': 'success', 'courses': courses_data, 'currentGpa': calculate_gpa_from_courses()})

@api_routes.route('/update_course', methods=['POST'])
def update_course():
    data = request.json
    index = data.get('index')
    new_credits = data.get('credits')
    new_grade = data.get('grade')
    grade_map_keys = {'A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'D-', 'F'}
    
    if not (0 <= index < len(courses_data)):
        return jsonify({'status': 'error', 'message': 'Course not found at specified index.'}), 404
    
    try:
        if new_credits is not None:
            new_credits = float(new_credits)
            if new_credits <= 0:
                return jsonify({'status': 'error', 'message': 'Credits must be a positive number.'}), 400
            courses_data[index]['credits'] = new_credits
        
        if new_grade:
            if new_grade not in grade_map_keys:
                return jsonify({'status': 'error', 'message': 'Invalid Grade. Allowed grades are A+, A, A-, B+, B, B-', 'C+': 2.3, 'C': 2.0, 'C-': 1.7, 'D+': 1.3, 'D': 1.0, 'D-': 0.7, 'F': 0.0}), 400
            courses_data[index]['grade'] = new_grade
            
        return jsonify({'status': 'success', 'courses': courses_data, 'currentGpa': calculate_gpa_from_courses()})
    except (ValueError, TypeError):
        return jsonify({'status': 'error', 'message': 'Invalid data for update.'}), 400
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'An unexpected error occurred: {str(e)}'}), 500

@api_routes.route('/delete_course', methods=['POST'])
def delete_course():
    data = request.json
    index = data.get('index')
    
    if not (0 <= index < len(courses_data)):
        return jsonify({'status': 'error', 'message': 'Course not found at specified index.'}), 404
    
    del courses_data[index]
    
    return jsonify({'status': 'success', 'courses': courses_data, 'currentGpa': calculate_gpa_from_courses()})

@api_routes.route('/reset_courses', methods=['POST'])
def reset_courses():
    global courses_data
    courses_data = []
    return jsonify({'status': 'success', 'message': 'All courses cleared.', 'currentGpa': 0.0})

# --- API Endpoints for Page 2 (Prior Semester / Final GPA Calculator) ---
@api_routes.route('/calculate_combined_gpa', methods=['POST'])
def calculate_combined_gpa():
    data = request.json
    try:
        old_total_credits = float(data.get('oldTotalCredits'))
        old_gpa = float(data.get('oldGpa'))
        new_semester_credits = float(data.get('newSemesterCredits'))
        new_semester_gpa = float(data.get('newSemesterGpa'))

        if old_total_credits < 0 or old_gpa < 0 or new_semester_credits < 0 or new_semester_gpa < 0:
            return jsonify({'status': 'error', 'message': 'All credit and GPA values must be non-negative.'}), 400
        if old_gpa > 4.0 or new_semester_gpa > 4.0:
            return jsonify({'status': 'error', 'message': 'GPA cannot exceed 4.0.'}), 400

        old_grade_points = old_total_credits * old_gpa
        new_grade_points = new_semester_credits * new_semester_gpa
        
        combined_total_credits = old_total_credits + new_semester_credits
        combined_total_grade_points = old_grade_points + new_grade_points
        
        combined_gpa = round(combined_total_grade_points / combined_total_credits, 2) if combined_total_credits > 0 else 0.0
        
        return jsonify({'status': 'success', 'combinedGpa': combined_gpa})
    except (ValueError, TypeError):
        return jsonify({'status': 'error', 'message': 'Invalid input: Please provide valid numbers.'}), 400
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'An unexpected error occurred: {str(e)}'}), 500

@api_routes.route('/calculate_final_cumulative_gpa', methods=['POST'])
def calculate_final_cumulative_gpa():
    data = request.json
    try:
        total_credits = float(data.get('totalCredits'))
        gpa = float(data.get('gpa'))

        if total_credits < 0 or gpa < 0:
            return jsonify({'status': 'error', 'message': 'Credits and GPA must be non-negative.'}), 400
        if gpa > 4.0:
            return jsonify({'status': 'error', 'message': 'GPA cannot exceed 4.0.'}), 400

        final_gpa = round(gpa, 2)

        return jsonify({'status': 'success', 'finalGpa': final_gpa})
    except (ValueError, TypeError):
        return jsonify({'status': 'error', 'message': 'Invalid input: Please provide valid numbers.'}), 400
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'An unexpected error occurred: {str(e)}'}), 500

# --- API Endpoints for Page 3 (GPA Planning) ---
@api_routes.route('/calculate_required_gpa', methods=['POST'])
def calculate_required_gpa():
    data = request.json
    try:
        goal_gpa = float(data.get('goalGpa'))
        current_gpa = float(data.get('currentGpa'))
        current_total_credits = float(data.get('currentTotalCredits'))
        next_semester_credits = float(data.get('nextSemesterCredits'))
        
        if goal_gpa < 0 or current_gpa < 0 or current_total_credits < 0 or next_semester_credits <= 0:
            return jsonify({'status': 'error', 'message': 'All credit and GPA values must be non-negative, and Next Semester Credits must be greater than zero.'}), 400
        if goal_gpa > 4.0 or current_gpa > 4.0:
            return jsonify({'status': 'error', 'message': 'GPA cannot exceed 4.0.'}), 400

        desired_total_grade_points = (current_total_credits + next_semester_credits) * goal_gpa
        current_grade_points = current_total_credits * current_gpa
        
        required_grade_points_for_next_semester = desired_total_grade_points - current_grade_points
        
        required_gpa = round(required_grade_points_for_next_semester / next_semester_credits, 2)
        
        message = ""
        if required_gpa > 4.0:
            message = 'The required GPA is very high. It might be impossible to achieve your goal with the given credits.'
        elif required_gpa < 0.0:
            message = 'The required GPA is negative, meaning you can achieve your goal even with a lower GPA in the next semester.'
        
        return jsonify({'status': 'success', 'requiredGpa': required_gpa, 'message': message})
    except (ValueError, TypeError):
        return jsonify({'status': 'error', 'message': 'Invalid input: Please provide valid numbers.'}), 400
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'An unexpected error occurred: {str(e)}'}), 500

# --- Redirects ---
@redirect_routes.route('/pages/about-us/')
@redirect_routes.route('/ur/pages/about-us/')
def pages_about_us_redirect():
    return redirect(url_for('static_pages.about_us'), code=301)

@redirect_routes.route('/pages/terms-conditions/')
@redirect_routes.route('/ur/pages/terms-conditions/')
def pages_terms_conditions_redirect():
    return redirect(url_for('static_pages.terms_conditions'), code=301)

@redirect_routes.route('/pages/privacy-policy/')
@redirect_routes.route('/ur/pages/privacy-policy/')
@redirect_routes.route('/ur/pages/privacy-policy')
def pages_privacy_policy_redirect():
    return redirect(url_for('static_pages.privacy_policy'), code=301)

@redirect_routes.route('/gpacalculatorcollege@gmail.com')
def email_contact_redirect():
    return redirect(url_for('static_pages.contact'), code=301)

@redirect_routes.route('/templates/index.html')
@redirect_routes.route('/templates/prior-semester-final-gpa.html')
def templates_redirect():
    return redirect(url_for('home'), code=301)

@redirect_routes.route('/blogs/time-management-tips-for-students')
def blog_redirect():
    return redirect(url_for('blog_routes.blog_index'), code=301)

@redirect_routes.route('/final-gpa')
@redirect_routes.route('/prior-semester-final-gpa')
def prior_semester_final_gpa_redirect():
    return redirect(url_for('prior_semester_gpa_en'), code=301)

@redirect_routes.route('/templates/gpa-planning-calculator.html')
def templates_gpa_planning_calculator_redirect():
    return redirect(url_for('gpa_planning_en'), code=301)

@redirect_routes.route('/en/gpa-calculator')
def gpa_calculator_redirect_en():
    return redirect(url_for('gpa_calculator_en'), code=301)

@redirect_routes.route('/final-grade-calculator/')
def final_grade_calculator_redirect():
    return redirect(url_for('final_grade_calculator_en'), code=301)

# Trailing slash wali URL ko redirect karne ka naya route
@app.route('/grade-calculator/')
def grade_calculator_redirect_trailing_slash():
    return redirect(url_for('grade_calculator_en'), code=301)
    
@app.route('/prior-semester-gpa/')
def prior_semester_gpa_redirect_trailing_slash():
    return redirect(url_for('prior_semester_gpa_en'), code=301)

@redirect_routes.route('/gpa-calculator/')
def gpa_calculator_redirect():
    return redirect(url_for('gpa_calculator_en'), code=301)

@redirect_routes.route('/rufinal-grade-calculator/')
def r_final_grade_calculator_redirect():
    return redirect(url_for('lang_routes.final_grade_calculator', lang_code='ru'), code=301)

@redirect_routes.route('/gpa-planning/')
def gpa_planning_redirect_no_lang():
    return redirect(url_for('gpa_planning_en'), code=301)
    
@redirect_routes.route('/static/css/rtl.css')
def css_redirect():
    return redirect(url_for('home'), code=301)

@redirect_routes.route('/x-default/final-grade-calculator')
def x_default_final_grade_calculator_redirect():
    return redirect(url_for('final_grade_calculator_en'), code=301)

@redirect_routes.route('/x-default/')
def x_default_home_redirect():
    return redirect(url_for('home'), code=301)

# --- Yeh route hata diya gaya hai taake redirect loop na bane ---
# @app.route('/blogs/')
# def blog_index_redirect_trailing_slash():
#    return redirect(url_for('blog_routes.blog_index'), code=301)

@app.route('/en/gpa-planning')
def en_gpa_planning_redirect():
    return redirect(url_for('gpa_planning_en'), code=301)

# Register Blueprints
app.register_blueprint(lang_routes)
app.register_blueprint(static_pages)
app.register_blueprint(api_routes, url_prefix='/api')
app.register_blueprint(blog_routes)
app.register_blueprint(redirect_routes)

if __name__ == '__main__':
    app.run(debug=True)