from flask import Flask, render_template, request, jsonify, url_for, redirect, send_from_directory, Blueprint, session, Response
from datetime import datetime

# Create a Flask app instance
app = Flask(__name__)
app.secret_key = 'your_secret_key_here' # Session ke liye secret key zaroori hai

# Dummy data store (real project mein database use hoga)
courses_data = [] # For Page 1

# Supported languages list
SUPPORTED_LANGS = ['en', 'ar', 'es', 'de', 'pt', 'ru', 'fr', 'it', 'tr']

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
@app.route('/', strict_slashes=False)
def home():
    template_name = get_template_name('home/index', 'en')
    session['lang_code'] = 'en'
    return render_template(template_name, lang_code='en')

# Home page route for other languages (with lang_code in URL)
@lang_routes.route('/', strict_slashes=False)
def index(lang_code):
    template_name = get_template_name('home/index', lang_code)
    session['lang_code'] = lang_code
    return render_template(template_name, lang_code=lang_code)

# --- NEW 404 Error Handler ---
@app.errorhandler(404)
def page_not_found(error):
    # Session se current language code lein, agar na milay to 'en' default rakhein
    lang_code = session.get('lang_code', 'en')
    
    if lang_code == 'en':
        # English home page
        return redirect(url_for('home'), code=302)
    else:
        # Other language home page (using lang_routes.index)
        # Note: Humein yahan lang_routes.index ko call karne ke liye lang_code provide karna hoga
        return redirect(url_for('lang_routes.index', lang_code=lang_code), code=302)
# --- END NEW 404 Error Handler ---

@app.route('/set-language/<lang_code>', strict_slashes=False)
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
@app.route('/gpa-calculator', strict_slashes=False)
def gpa_calculator_en():
    template_name = get_template_name('gpacalculator/gpa-calculator', 'en')
    session['lang_code'] = 'en'
    return render_template(template_name, lang_code='en')

# GPA Calculator route for all other languages (with lang_code in URL)
@lang_routes.route('/gpa-calculator', strict_slashes=False)
def gpa_calculator(lang_code):
    template_name = get_template_name('gpacalculator/gpa-calculator', lang_code)
    session['lang_code'] = lang_code
    return render_template(template_name, lang_code=lang_code)

@app.route('/final-grade-calculator', strict_slashes=False)
def final_grade_calculator_en():
    template_name = get_template_name('finalgrade/finalgradecalculator', 'en')
    session['lang_code'] = 'en'
    return render_template(template_name, lang_code='en')

@lang_routes.route('/final-grade-calculator', strict_slashes=False)
def final_grade_calculator(lang_code):
    template_name = get_template_name('finalgrade/finalgradecalculator', lang_code)
    session['lang_code'] = lang_code
    return render_template(template_name, lang_code=lang_code)
    
# --- Naye routes yahan add kiye gaye hain taake English ka URL theek ho ---
@app.route('/prior-semester-gpa', strict_slashes=False)
def prior_semester_gpa_en():
    template_name = get_template_name('prior-semester-gpa/prior-semester-gpa', 'en')
    session['lang_code'] = 'en'
    return render_template(template_name, lang_code='en')

@lang_routes.route('/prior-semester-gpa', strict_slashes=False)
def prior_semester_gpa(lang_code):
    template_name = get_template_name('prior-semester-gpa/prior-semester-gpa', lang_code)
    session['lang_code'] = lang_code
    return render_template(template_name, lang_code=lang_code)

@app.route('/highschool-gpa', strict_slashes=False)
def highschool_gpa_en():
    template_name = get_template_name('highschool/highschool', 'en')
    session['lang_code'] = 'en'
    return render_template(template_name, lang_code='en')

@lang_routes.route('/highschool-gpa', strict_slashes=False)
def highschool_gpa(lang_code):
    template_name = get_template_name('highschool/highschool', lang_code)
    session['lang_code'] = lang_code
    return render_template(template_name, lang_code=lang_code)

@app.route('/grade-calculator', strict_slashes=False)
def grade_calculator_en():
    template_name = get_template_name('gradecalculator/gradecalculator', 'en')
    session['lang_code'] = 'en'
    return render_template(template_name, lang_code='en')

@lang_routes.route('/grade-calculator', strict_slashes=False)
def grade_calculator(lang_code):
    template_name = get_template_name('gradecalculator/gradecalculator', lang_code)
    session['lang_code'] = lang_code
    return render_template(template_name, lang_code=lang_code)
    
@app.route('/gpa-planning', strict_slashes=False)
def gpa_planning_en():
    template_name = get_template_name('gpaplan/gpa-planning-calculator', 'en')
    session['lang_code'] = 'en'
    return render_template(template_name, lang_code='en')
    
@lang_routes.route('/gpa-planning', strict_slashes=False)
def gpa_planning(lang_code):
    template_name = get_template_name('gpaplan/gpa-planning-calculator', lang_code)
    session['lang_code'] = lang_code
    return render_template(template_name, lang_code=lang_code)

# --- New routes for Semester Grade Calculator ---
@app.route('/semester-grade-calculator', strict_slashes=False)
def semester_grade_calculator_en():
    template_name = get_template_name('samesterGradeCalcuator/samesterGradecalculator', 'en')
    session['lang_code'] = 'en'
    return render_template(template_name, lang_code='en')

@lang_routes.route('/semester-grade-calculator', strict_slashes=False)
def semester_grade_calculator(lang_code):
    template_name = get_template_name('samesterGradeCalcuator/samesterGradecalculator', lang_code)
    session['lang_code'] = lang_code
    return render_template(template_name, lang_code=lang_code)
    
# --- New routes for Ez-Grader ---
@app.route('/ez-grader', strict_slashes=False)
def ez_grader_en():
    template_name = get_template_name('ez/ez', 'en')
    session['lang_code'] = 'en'
    return render_template(template_name, lang_code='en')

@lang_routes.route('/ez-grader', strict_slashes=False)
def ez_grader(lang_code):
    template_name = get_template_name('ez/ez', lang_code)
    session['lang_code'] = lang_code
    return render_template(template_name, lang_code=lang_code)

# --- NEW ROUTES FOR MIDDLE SCHOOL GPA CALCULATOR ---
@app.route('/middle-school-gpa-calculator', strict_slashes=False)
def middle_school_gpa_calculator_en():
    template_name = get_template_name('middleSchool/middleSchool', 'en')
    session['lang_code'] = 'en'
    return render_template(template_name, lang_code='en')

@lang_routes.route('/middle-school-gpa-calculator', strict_slashes=False)
def middle_school_gpa_calculator(lang_code):
    template_name = get_template_name('middleSchool/middleSchool', lang_code)
    session['lang_code'] = lang_code
    return render_template(template_name, lang_code=lang_code)

# --- NEW ROUTES FOR SGPA to CGPA Converter ---
@app.route('/sgpa-to-cgpa-calculator', strict_slashes=False)
def sgpa_to_cgpa_en():
    template_name = get_template_name('sgpa_to_gpa/sgpatogpa', 'en')
    session['lang_code'] = 'en'
    return render_template(template_name, lang_code='en')

@lang_routes.route('/sgpa-to-cgpa-calculator', strict_slashes=False)
def sgpa_to_cgpa(lang_code):
    template_name = get_template_name('sgpa_to_gpa/sgpatogpa', lang_code)
    session['lang_code'] = lang_code
    return render_template(template_name, lang_code=lang_code)
    
# --- NEW ROUTES FOR SGPA to PERCENTAGE Converter ---
@app.route('/sgpa-to-percentage-calculator', strict_slashes=False)
def sgpa_to_percentage_en():
    template_name = get_template_name('sgpatopercentage/sgpatopercentage', 'en')
    session['lang_code'] = 'en'
    return render_template(template_name, lang_code='en')

@lang_routes.route('/sgpa-to-percentage-calculator', strict_slashes=False)
def sgpa_to_percentage(lang_code):
    template_name = get_template_name('sgpatopercentage/sgpatopercentage', lang_code)
    session['lang_code'] = lang_code
    return render_template(template_name, lang_code=lang_code)
    
@app.route('/sitemap.xml', strict_slashes=False)
def sitemap():
    return send_from_directory(app.root_path, 'sitemap.xml')

# --- Blog Routes (static) ---
@blog_routes.route('/', strict_slashes=False)
def blog_index():
    # Blogs pages mein 'lang_code' pass karne ki zaroorat nahi hai
    # kyunki inki translations nahi hain.
    lang_code = session.get('lang_code', 'en')
    return render_template('blogs/blog_index.html', lang_code=lang_code)

@blog_routes.route('/<slug>', strict_slashes=False)
def blog_post(slug):
    lang_code = session.get('lang_code', 'en')
    blog_templates = {
        'how-to-improve-your-gpa-effectively': 'blogs/gpa_blog.html',
        'understanding-different-grading-scales': 'blogs/final_gpa_blog.html',
        'achieving-your-target-gpa-guide': 'blogs/target_gpa_blog.html'
    }
    
    template_to_render = blog_templates.get(slug)
    
    if template_to_render:
        return render_template(template_to_render, slug=slug, lang_code=lang_code)
    else:
        return "Blog Post Not Found", 404

# --- Other Static Pages ---
@static_pages.route('/privacy-policy', strict_slashes=False)
def privacy_policy():
    lang_code = session.get('lang_code', 'en')
    return render_template('pages/privacy-policy.html', lang_code=lang_code)

@static_pages.route('/terms-conditions', strict_slashes=False)
def terms_conditions():
    lang_code = session.get('lang_code', 'en')
    return render_template('pages/terms-conditions.html', lang_code=lang_code)

@static_pages.route('/about-us', strict_slashes=False)
def about_us():
    lang_code = session.get('lang_code', 'en')
    return render_template('pages/About-us.html', lang_code=lang_code)

@static_pages.route('/contact', strict_slashes=False)
def contact():
    # Yahan 'lang_code' ko session se le kar pass kiya gaya hai
    lang_code = session.get('lang_code', 'en')
    return render_template('pages/Contact.html', lang_code=lang_code)

# --- API Endpoints ---
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

@api_routes.route('/get_courses', methods=['GET'], strict_slashes=False)
def get_courses():
    return jsonify({'status': 'success', 'courses': courses_data, 'currentGpa': calculate_gpa_from_courses()})

@api_routes.route('/add_course', methods=['POST'], strict_slashes=False)
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

@api_routes.route('/update_course', methods=['POST'], strict_slashes=False)
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

@api_routes.route('/delete_course', methods=['POST'], strict_slashes=False)
def delete_course():
    data = request.json
    index = data.get('index')
    
    if not (0 <= index < len(courses_data)):
        return jsonify({'status': 'error', 'message': 'Course not found at specified index.'}), 404
    
    del courses_data[index]
    
    return jsonify({'status': 'success', 'courses': courses_data, 'currentGpa': calculate_gpa_from_courses()})

@api_routes.route('/reset_courses', methods=['POST'], strict_slashes=False)
def reset_courses():
    global courses_data
    courses_data = []
    return jsonify({'status': 'success', 'message': 'All courses cleared.', 'currentGpa': 0.0})

# --- API Endpoints for Page 2 (Prior Semester / Final GPA Calculator) ---
@api_routes.route('/calculate_combined_gpa', methods=['POST'], strict_slashes=False)
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

@api_routes.route('/calculate_final_cumulative_gpa', methods=['POST'], strict_slashes=False)
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
@api_routes.route('/calculate_required_gpa', methods=['POST'], strict_slashes=False)
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

# --- NEW GENERIC REDIRECT FOR TRAILING SLASH ---
@redirect_routes.route('/<path:subpath>/', strict_slashes=False)
def remove_trailing_slash_redirect(subpath):
    # Check if the path (subpath) has a blueprint prefix, otherwise it is an app.route path.
    # We try to rebuild the URL without the trailing slash.
    # Note: url_for requires the function name. This is a generic approach.
    
    # Simple check for static files that should not be redirected
    if subpath.endswith(('.xml', '.txt')):
        # XML or other file, do nothing, let it 404 or be handled elsewhere
        # (Though sitemap.xml is handled by app.route, this is a safety check)
        return "Not Found", 404 
    
    # Try to determine the target route:
    # 1. Check for known Blueprint prefixes (manual checking is safer for generic redirects)
    if subpath.startswith('api/'):
        target = subpath.rstrip('/')
        return redirect(url_for('api_routes.' + target.replace('api/', '').replace('-', '_')), code=301)
    elif subpath.startswith('blogs/'):
        target_path = subpath.replace('blogs/', '').rstrip('/')
        if not target_path: # /blogs/ -> /blogs
             return redirect(url_for('blog_routes.blog_index'), code=301)
        else: # /blogs/slug/ -> /blogs/slug
             return redirect(url_for('blog_routes.blog_post', slug=target_path), code=301)
    elif subpath in ['privacy-policy', 'terms-conditions', 'about-us', 'contact']:
        return redirect(url_for('static_pages.' + subpath.replace('-', '_')), code=301)
    
    # 2. Check for language routes (/<lang_code>/path)
    path_parts = subpath.split('/')
    if len(path_parts) >= 2 and path_parts[0] in SUPPORTED_LANGS:
        lang_code = path_parts[0]
        # path is like 'lang_code/path-segment'. We need 'path-segment' for the function name.
        route_name = path_parts[1].replace('-', '_')
        
        # Mapping known route names (to handle hyphenated paths like gpa-calculator)
        route_map = {
            'gpa_calculator': 'gpa_calculator',
            'final_grade_calculator': 'final_grade_calculator',
            'prior_semester_gpa': 'prior_semester_gpa',
            'highschool_gpa': 'highschool_gpa',
            'grade_calculator': 'grade_calculator',
            'gpa_planning': 'gpa_planning',
            'semester_grade_calculator': 'semester_grade_calculator',
            'ez_grader': 'ez_grader',
            'middle_school_gpa_calculator': 'middle_school_gpa_calculator',
            'sgpa_to_cgpa_calculator': 'sgpa_to_cgpa',
            'sgpa_to_percentage_calculator': 'sgpa_to_percentage'
            # Add other lang_routes routes here
        }
        
        target_func_name = route_map.get(route_name)
        if target_func_name:
            # lang_routes.index is for /<lang_code>/
            return redirect(url_for('lang_routes.' + target_func_name, lang_code=lang_code), code=301)
        elif not path_parts[1]: # /lang_code/ -> /lang_code
            return redirect(url_for('lang_routes.index', lang_code=lang_code), code=301)

    # 3. Check for app.route paths (no lang_code or static pages in the path)
    # path is the same as subpath since it's not a blueprint
    route_name = subpath.replace('-', '_')
    app_route_map = {
        'gpa_calculator': 'gpa_calculator_en',
        'final_grade_calculator': 'final_grade_calculator_en',
        'prior_semester_gpa': 'prior_semester_gpa_en',
        'highschool_gpa': 'highschool_gpa_en',
        'grade_calculator': 'grade_calculator_en',
        'gpa_planning': 'gpa_planning_en',
        'semester_grade_calculator': 'semester_grade_calculator_en',
        'ez_grader': 'ez_grader_en',
        'middle_school_gpa_calculator': 'middle_school_gpa_calculator_en',
        'sgpa_to_cgpa_calculator': 'sgpa_to_cgpa_en',
        'sgpa_to_percentage_calculator': 'sgpa_to_percentage_en',
        # Add other app.route function names here
    }
    
    target_func_name = app_route_map.get(route_name)
    if target_func_name:
        return redirect(url_for(target_func_name), code=301)
    
    # Fallback/Default for unhandled paths in redirect_routes (can be a 404 or a general redirect)
    # To avoid redirecting known 301s which should go to a specific target without trailing slash,
    # we can explicitly redirect to the path without the slash, which will be handled by another route.
    # Example: /old-path/ -> /old-path. If /old-path already redirects, this is safe.
    # The default behavior is simply redirecting to the same URL without the slash.
    return redirect(f'/{subpath.rstrip("/")}', code=301)


# --- Redirects (Old, broken links) ---
@redirect_routes.route('/en/', strict_slashes=False)
def en_home_redirect():
    return redirect(url_for('home'), code=301)
    
@redirect_routes.route('/pages/about-us/', strict_slashes=False)
@redirect_routes.route('/ur/pages/about-us/', strict_slashes=False)
def pages_about_us_redirect():
    return redirect(url_for('static_pages.about_us'), code=301)

@redirect_routes.route('/pages/terms-conditions/', strict_slashes=False)
@redirect_routes.route('/ur/pages/terms-conditions/', strict_slashes=False)
def pages_terms_conditions_redirect():
    return redirect(url_for('static_pages.terms_conditions'), code=301)

@redirect_routes.route('/pages/privacy-policy/', strict_slashes=False)
@redirect_routes.route('/ur/pages/privacy-policy/', strict_slashes=False)
@redirect_routes.route('/ur/pages/privacy-policy', strict_slashes=False)
def pages_privacy_policy_redirect():
    return redirect(url_for('static_pages.privacy_policy'), code=301)

@redirect_routes.route('/gpacalculatorcollege@gmail.com', strict_slashes=False)
def email_contact_redirect():
    return redirect(url_for('static_pages.contact'), code=301)

@redirect_routes.route('/templates/index.html', strict_slashes=False)
@redirect_routes.route('/templates/prior-semester-final-gpa.html', strict_slashes=False)
def templates_redirect():
    return redirect(url_for('home'), code=301)

@app.route('/www.gpacalculatorcollege.com', strict_slashes=False)
def oldpath_redirect():
    return redirect(url_for('home'), code=301)

@redirect_routes.route('/blogs/time-management-tips-for-students', strict_slashes=False)
def blog_redirect():
    return redirect(url_for('blog_routes.blog_index'), code=301)

@redirect_routes.route('/final-gpa', strict_slashes=False)
@redirect_routes.route('/prior-semester-final-gpa', strict_slashes=False)
def prior_semester_final_gpa_redirect():
    return redirect(url_for('prior_semester_gpa_en'), code=301)

@redirect_routes.route('/templates/gpa-planning-calculator.html', strict_slashes=False)
def templates_gpa_planning_calculator_redirect():
    return redirect(url_for('gpa_planning_en'), code=301)

@redirect_routes.route('/en/gpa-calculator', strict_slashes=False)
def gpa_calculator_redirect_en():
    return redirect(url_for('gpa_calculator_en'), code=301)

# *Removed /final-grade-calculator/ redirect because generic slash remover handles it*
# @redirect_routes.route('/final-grade-calculator/', strict_slashes=False)
# def final_grade_calculator_redirect():
#     return redirect(url_for('final_grade_calculator_en'), code=301)

# *Removed /grade-calculator/ redirect because generic slash remover handles it*
# @app.route('/grade-calculator/', strict_slashes=False)
# def grade_calculator_redirect_trailing_slash():
#     return redirect(url_for('grade_calculator_en'), code=301)
    
# *Removed /prior-semester-gpa/ redirect because generic slash remover handles it*
# @app.route('/prior-semester-gpa/', strict_slashes=False)
# def prior_semester_gpa_redirect_trailing_slash():
#     return redirect(url_for('prior_semester_gpa_en'), code=301)

# *Removed /gpa-calculator/ redirect because generic slash remover handles it*
# @redirect_routes.route('/gpa-calculator/', strict_slashes=False)
# def gpa_calculator_redirect():
#     return redirect(url_for('gpa_calculator_en'), code=301)

@redirect_routes.route('/rufinal-grade-calculator/', strict_slashes=False)
def r_final_grade_calculator_redirect():
    return redirect(url_for('lang_routes.final_grade_calculator', lang_code='ru'), code=301)

# *Removed /gpa-planning/ redirect because generic slash remover handles it*
# @redirect_routes.route('/gpa-planning/', strict_slashes=False)
# def gpa_planning_redirect_no_lang():
#     return redirect(url_for('gpa_planning_en'), code=301)
    
@redirect_routes.route('/static/css/rtl.css', strict_slashes=False)
def css_redirect():
    return redirect(url_for('home'), code=301)

@redirect_routes.route('/x-default/final-grade-calculator', strict_slashes=False)
def x_default_final_grade_calculator_redirect():
    return redirect(url_for('final_grade_calculator_en'), code=301)

@redirect_routes.route('/x-default/', strict_slashes=False)
def x_default_home_redirect():
    return redirect(url_for('home'), code=301)

@redirect_routes.route('/high-school-gpa-calculator', strict_slashes=False)
def high_school_gpa_calculator_redirect():
    return redirect(url_for('highschool_gpa_en'), code=301)

# *Removed /high-school-gpa-calculator/ redirect because generic slash remover handles it*
# @redirect_routes.route('/high-school-gpa-calculator/', strict_slashes=False)
# def high_school_gpa_calculator_redirect_trailing_slash():
#     return redirect(url_for('highschool_gpa_en'), code=301)

# --- Yeh route hata diya gaya hai taake redirect loop na bane ---
# @app.route('/blogs/', strict_slashes=False)
# def blog_index_redirect_trailing_slash():
#     return redirect(url_for('blog_routes.blog_index'), code=301)

@app.route('/en/panning', strict_slashes=False)
def en_gpa_planning_redirect():
    return redirect(url_for('gpa_planning_en'), code=301)
    
# *Removed /semester-grade-calculator/ redirect because generic slash remover handles it*
# @app.route('/semester-grade-calculator/', strict_slashes=False)
# def semester_grade_calculator_redirect():
#     return redirect(url_for('semester_grade_calculator_en'), code=301)

# *Removed Ez-Grader redirects because generic slash remover handles it*
# @redirect_routes.route('/ez-grader/', strict_slashes=False)
# def ez_grader_redirect_trailing_slash():
#     return redirect(url_for('ez_grader_en'), code=301)

# *Removed Middle School redirects because generic slash remover handles it*
# @redirect_routes.route('/middle-school-gpa-calculator/', strict_slashes=False)
# def middle_school_gpa_calculator_redirect_trailing_slash():
#     return redirect(url_for('middle_school_gpa_calculator_en'), code=301)

# Naye redirect routes aapki request ke mutabiq
@redirect_routes.route('/ez-grader/<path:subpath>', strict_slashes=False)
def ez_grader_catch_all_redirect(subpath):
    return redirect(url_for('ez_grader_en'), code=301)

# *Removed static page redirects under lang_routes because generic slash remover handles the trailing slash*
@lang_routes.route('/privacy-policy', strict_slashes=False)
def privacy_policy_redirect(lang_code):
    return redirect(url_for('static_pages.privacy_policy'), code=301)

@lang_routes.route('/terms-conditions', strict_slashes=False)
def terms_conditions_redirect(lang_code):
    return redirect(url_for('static_pages.terms_conditions'), code=301)

@lang_routes.route('/about-us', strict_slashes=False)
def about_us_redirect(lang_code):
    return redirect(url_for('static_pages.about_us'), code=301)

@lang_routes.route('/contact', strict_slashes=False)
def contact_redirect(lang_code):
    return redirect(url_for('static_pages.contact'), code=301)

# *Removed /blogs/ and /blogs/<path:subpath>/ redirects because generic slash remover handles the trailing slash*
@lang_routes.route('/blogs/', strict_slashes=False)
def blogs_index_redirect(lang_code):
    return redirect(url_for('blog_routes.blog_index'), code=301)

@lang_routes.route('/blogs/<path:subpath>', strict_slashes=False)
def blogs_post_redirect(lang_code, subpath):
    return redirect(url_for('blog_routes.blog_post', slug=subpath), code=301)

# --- NEW REDIRECTS ADDED HERE ---
# *Removed calcolatrice-voti-semestre/ redirect because generic slash remover handles it*
# @redirect_routes.route('/calcolatrice-voti-semestre/', strict_slashes=False)
# def calcolatrice_voti_semestre_redirect():
#     return redirect(url_for('semester_grade_calculator_en'), code=301)

# *Removed calcolatore-gpa-scuola-superiore/ redirect because generic slash remover handles it*
# @redirect_routes.route('/calcolatore-gpa-scuola-superiore/', strict_slashes=False)
# def calcolatore_gpa_scuola_superiore_it_redirect():
#     return redirect(url_for('lang_routes.highschool_gpa', lang_code='it'), code=301)

@redirect_routes.route('/calcolatrice-voto-finale', strict_slashes=False)
def calcolatrice_voto_finale_no_slash_redirect():
    return redirect(url_for('final_grade_calculator_en'), code=301)

# *Removed calcolatrice-media-voti/ redirect because generic slash remover handles it*
# @redirect_routes.route('/calcolatrice-media-voti/', strict_slashes=False)
# def calcolatrice_media_voti_redirect():
#     return redirect(url_for('grade_calculator_en'), code=301)

@redirect_routes.route('/calculateur-notes-semestrielles', strict_slashes=False)
def calculateur_notes_semestrielles_redirect():
    return redirect(url_for('semester_grade_calculator_en'), code=301)

@redirect_routes.route('/calcolatore-gpa', strict_slashes=False)
def calcolatore_gpa_redirect():
    return redirect(url_for('gpa_calculator_en'), code=301)
    
@redirect_routes.route('/calcolatore-gpa-scuola-superiore', strict_slashes=False)
def calcolatore_gpa_scuola_superiore_redirect():
    return redirect(url_for('highschool_gpa_en'), code=301)

# *Removed calcolatrice-voto-finale/ redirect because generic slash remover handles it*
# @redirect_routes.route('/calcolatrice-voto-finale/', strict_slashes=False)
# def calcolatrice_voto_finale_slash_redirect():
#     return redirect(url_for('final_grade_calculator_en'), code=301)

@redirect_routes.route('/calcolatrice-voto', strict_slashes=False)
def calcolatrice_voto_redirect():
    return redirect(url_for('gpa_calculator_en'), code=301)
    
# *Removed sgpa-to-cgpa-calculator/ redirect because generic slash remover handles it*
# @redirect_routes.route('/sgpa-to-cgpa-calculator/', strict_slashes=False)
# def sgpa_to_cgpa_redirect_trailing_slash():
#     return redirect(url_for('sgpa_to_cgpa_en'), code=301)
    
# NEW REDIRECTS FOR SGPA TO PERCENTAGE
@redirect_routes.route('/sgpa-to-percentage/', strict_slashes=False)
def sgpa_to_percentage_redirect():
    return redirect(url_for('sgpa_to_percentage_en'), code=301)
    
# *Removed sgpa-to-percentage-calculator/ redirect because generic slash remover handles it*
# @redirect_routes.route('/sgpa-to-percentage-calculator/', strict_slashes=False)
# def sgpa_to_percentage_redirect_trailing_slash():
#     return redirect(url_for('sgpa_to_percentage_en'), code=301)

@lang_routes.route('/calcolatrice-voti-semestre', strict_slashes=False)
def it_semester_grade_calculator_redirect(lang_code):
    return redirect(url_for('lang_routes.semester_grade_calculator', lang_code=lang_code), code=301)
    
@lang_routes.route('/calcolatrice-voto-finale', strict_slashes=False)
def it_final_grade_calculator_redirect(lang_code):
    return redirect(url_for('lang_routes.final_grade_calculator', lang_code=lang_code), code=301)
    
@lang_routes.route('/calculateur-notes-semestrielles', strict_slashes=False)
def fr_semester_grade_calculator_redirect(lang_code):
    return redirect(url_for('lang_routes.semester_grade_calculator', lang_code=lang_code), code=301)

@lang_routes.route('/calcolatore-gpa', strict_slashes=False)
def it_gpa_calculator_redirect(lang_code):
    return redirect(url_for('lang_routes.gpa_calculator', lang_code=lang_code), code=301)

@lang_routes.route('/calcolatore-gpa-scuola-superiore', strict_slashes=False)
def it_highschool_gpa_redirect(lang_code):
    return redirect(url_for('lang_routes.highschool_gpa', lang_code=lang_code), code=301)
    
@lang_routes.route('/calcolatrice-voto', strict_slashes=False)
def it_grade_calculator_redirect(lang_code):
    return redirect(url_for('lang_routes.grade_calculator', lang_code=lang_code), code=301)


# --- END OF NEW REDIRECTS ---

# Register Blueprints
app.register_blueprint(lang_routes)
app.register_blueprint(static_pages)
app.register_blueprint(api_routes, url_prefix='/api')
app.register_blueprint(blog_routes)
app.register_blueprint(redirect_routes)

if __name__ == '__main__':
    # User ne request ki thi:
    # "Jab bhe head section bna'na ha <meta name="robots" content="noindex, nofollow"> Ye section hamesha same rehna chahiyay matlab no index or no nofollow or han agar mein nay asa code dia ha jis mein mein nay khud index of follow kia hua ha tous ko noindex or nofollow ni krna us ko index he rehnay dena ha lekin end pr lazmi bta dena ha mujy"
    # Ye code Flask routes aur redirects ke liye hai. <meta> tag template files (jinhe render_template se call kiya gaya hai) mein hota hai.
    # Lekin **301 Redirects** aur **API Endpoints** mein **HTML/Head section** nahi hota, isliye robots meta tag ki zaroorat nahi hai.
    # Ye code `__name__ == '__main__':` block ke andar Flask app ko run kar raha hai, jahan meta tag ka koi role nahi hai.
    app.run(debug=True)
