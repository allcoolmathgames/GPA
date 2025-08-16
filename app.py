from flask import Flask, render_template, request, jsonify, url_for, redirect, send_from_directory, g, render_template_string, make_response
from functools import wraps
import re

app = Flask(__name__)

# Dummy data store for the GPA calculator
courses_data = []

# Supported languages list
SUPPORTED_LANGUAGES = ['ur', 'ar', 'pt', 'es', 'fr', 'de', 'ru']

# --- Helper Functions ---
def handle_language_routes(f):
    """Decorator to handle language codes in the URL."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        lang_code = kwargs.pop('lang_code', 'en')
        if lang_code not in SUPPORTED_LANGUAGES and lang_code != 'en':
            # Fallback to English if language code is not supported
            lang_code = 'en'
        g.lang_code = lang_code
        return f(*args, **kwargs)
    return decorated_function

def calculate_gpa_from_courses():
    """Calculates GPA from a list of courses."""
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

def get_translated_paths_from_js():
    """Extracts URL paths from the language.js file using regex."""
    try:
        # Assuming language.js is in the static/js folder
        js_file_path = 'static/js/language.js'
        with open(js_file_path, 'r', encoding='utf-8') as f:
            js_code = f.read()

        # Regex to find links starting with '/' from the JS file
        regex = r"href\s*=\s*`\/\$\{(?:lang|newLang)\}([^`]+)`"
        dynamic_paths = set(re.findall(regex, js_code))

        # Manually add static paths to be included in the sitemap
        static_pages = [
            '/', '/prior-semester-gpa', '/highschool-gpa',
            '/grade-calculator', '/final-grade-calculator',
            '/gpa-calculator', '/gpa-planning', '/blogs',
            '/privacy-policy', '/terms-conditions',
            '/about-us', '/contact'
        ]

        # Add blog post slugs manually as they are not in the JS file
        blog_slugs = [
            '/blogs/how-to-improve-your-gpa-effectively',
            '/blogs/understanding-different-grading-scales',
            '/blogs/achieving-your-target-gpa-guide'
        ]
        return list(dynamic_paths.union(static_pages).union(blog_slugs))
    except FileNotFoundError:
        print("Error: language.js file not found. Sitemap will not include translated URLs.")
        return ['/'] # Return a default path to avoid errors

# --- Routes for Pages ---
@app.route('/<string:lang_code>/')
@app.route('/')
@handle_language_routes
def index(lang_code=None):
    return render_template('index.html')

@app.route('/<string:lang_code>/prior-semester-gpa')
@app.route('/prior-semester-gpa')
@handle_language_routes
def prior_semester_gpa(lang_code=None):
    return render_template('prior-semester-gpa.html')

@app.route('/<string:lang_code>/highschool-gpa')
@app.route('/highschool-gpa')
@handle_language_routes
def highschool_gpa(lang_code=None):
    return render_template('highschool.html')

@app.route('/<string:lang_code>/grade-calculator')
@app.route('/grade-calculator')
@handle_language_routes
def grade_calculator(lang_code=None):
    return render_template('gradecalculator.html')

@app.route('/<string:lang_code>/final-grade-calculator')
@app.route('/final-grade-calculator')
@handle_language_routes
def final_grade_calculator(lang_code=None):
    return render_template('finalgradecalculator.html')

@app.route('/<string:lang_code>/gpa-calculator')
@app.route('/gpa-calculator')
@handle_language_routes
def gpa_calculator(lang_code=None):
    return render_template('gpa-calculator.html')

@app.route('/<string:lang_code>/gpa-planning')
@app.route('/gpa-planning')
@handle_language_routes
def gpa_planning(lang_code=None):
    return render_template('gpa-planning-calculator.html')

# --- Sitemap Route ---
@app.route('/sitemap.xml')
def sitemap():
    pages = get_translated_paths_from_js()
    languages = SUPPORTED_LANGUAGES + ['en'] # Add 'en' for the default language

    sitemap_template = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
{% for page in pages %}
    <url>
        <loc>https://gpacalculatorcollege.com{{ page }}</loc>
        {% for lang in languages %}
            {% if lang == 'en' %}
                <xhtml:link rel="alternate" hreflang="{{ lang }}" href="https://gpacalculatorcollege.com{{ page }}"/>
            {% else %}
                <xhtml:link rel="alternate" hreflang="{{ lang }}" href="https://gpacalculatorcollege.com/{{ lang }}{{ page }}"/>
            {% endif %}
        {% endfor %}
        <xhtml:link rel="alternate" hreflang="x-default" href="https://gpacalculatorcollege.com{{ page }}"/>
    </url>
{% endfor %}
</urlset>
"""

    sitemap_content = render_template_string(sitemap_template, pages=pages, languages=languages)
    response = make_response(sitemap_content)
    response.headers['Content-Type'] = 'application/xml'
    return response

# --- Blog Routes ---
@app.route('/<string:lang_code>/blogs')
@app.route('/blogs')
@handle_language_routes
def blog_index(lang_code=None):
    return render_template('blogs/blog_index.html')

@app.route('/<string:lang_code>/blogs/<slug>')
@app.route('/blogs/<slug>')
@handle_language_routes
def blog_post(slug, lang_code=None):
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
@app.route('/<string:lang_code>/privacy-policy')
@app.route('/privacy-policy')
@handle_language_routes
def privacy_policy(lang_code=None):
    return render_template('pages/privacy-policy.html')

@app.route('/<string:lang_code>/terms-conditions')
@app.route('/terms-conditions')
@handle_language_routes
def terms_conditions(lang_code=None):
    return render_template('pages/terms-conditions.html')

@app.route('/<string:lang_code>/about-us')
@app.route('/about-us')
@handle_language_routes
def about_us(lang_code=None):
    return render_template('pages/About-us.html')

@app.route('/<string:lang_code>/contact')
@app.route('/contact')
@handle_language_routes
def contact(lang_code=None):
    return render_template('pages/Contact.html')

# --- API Endpoints ---
# GPA Calculator Page Endpoints
@app.route('/get_courses', methods=['GET'])
def get_courses():
    return jsonify({'status': 'success', 'courses': courses_data, 'currentGpa': calculate_gpa_from_courses()})

@app.route('/add_course', methods=['POST'])
def add_course():
    data = request.json
    course_name = data.get('courseName')
    credits = data.get('credits')
    grade = data.get('grade')
    if not course_name or not grade:
        return jsonify({'status': 'error', 'message': 'Course Name and Grade are required.'}), 400
    try:
        credits = float(credits)
        if credits <= 0:
            return jsonify({'status': 'error', 'message': 'Credits must be a positive number.'}), 400
    except (ValueError, TypeError):
        return jsonify({'status': 'error', 'message': 'Invalid Credits value.'}), 400
    grade_map_keys = {'A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'D-', 'F'}
    if grade not in grade_map_keys:
        return jsonify({'status': 'error', 'message': 'Invalid Grade. Allowed grades are A+, A, A-, B+, B, B-, C+, C, C-, D+, D, D-, F.'}), 400
    courses_data.append({'name': course_name, 'credits': credits, 'grade': grade})
    return jsonify({'status': 'success', 'courses': courses_data, 'currentGpa': calculate_gpa_from_courses()})

@app.route('/update_course', methods=['POST'])
def update_course():
    data = request.json
    index = data.get('index')
    new_credits = data.get('credits')
    new_grade = data.get('grade')
    if not (0 <= index < len(courses_data)):
        return jsonify({'status': 'error', 'message': 'Course not found at specified index.'}), 404
    try:
        if new_credits is not None:
            new_credits = float(new_credits)
            if new_credits <= 0:
                return jsonify({'status': 'error', 'message': 'Credits must be a positive number.'}), 400
            courses_data[index]['credits'] = new_credits
        if new_grade:
            grade_map_keys = {'A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'D-', 'F'}
            if new_grade not in grade_map_keys:
                return jsonify({'status': 'error', 'message': 'Invalid Grade. Allowed grades are A+, A, A-, B+, B, B-,C+, C, C-, D+, D, D-, F'}), 400
            courses_data[index]['grade'] = new_grade
        return jsonify({'status': 'success', 'courses': courses_data, 'currentGpa': calculate_gpa_from_courses()})
    except (ValueError, TypeError):
        return jsonify({'status': 'error', 'message': 'Invalid data for update.'}), 400
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'An unexpected error occurred: {str(e)}'}), 500

@app.route('/delete_course', methods=['POST'])
def delete_course():
    data = request.json
    index = data.get('index')
    if not (0 <= index < len(courses_data)):
        return jsonify({'status': 'error', 'message': 'Course not found at specified index.'}), 404
    del courses_data[index]
    return jsonify({'status': 'success', 'courses': courses_data, 'currentGpa': calculate_gpa_from_courses()})

@app.route('/reset_courses', methods=['POST'])
def reset_courses():
    global courses_data
    courses_data = []
    return jsonify({'status': 'success', 'message': 'All courses cleared.', 'currentGpa': 0.0})

# Prior Semester / Final GPA Calculator Page Endpoints
@app.route('/calculate_combined_gpa', methods=['POST'])
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

@app.route('/calculate_final_cumulative_gpa', methods=['POST'])
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

# GPA Planning Page Endpoints
@app.route('/calculate_required_gpa', methods=['POST'])
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
@app.route('/pages/about-us/')
def pages_about_us_redirect():
    return redirect(url_for('about_us'), code=301)

@app.route('/pages/terms-conditions/')
def pages_terms_conditions_redirect():
    return redirect(url_for('terms_conditions'), code=301)

@app.route('/pages/privacy-policy/')
def pages_privacy_policy_redirect():
    return redirect(url_for('privacy_policy'), code=301)

@app.route('/templates/index.html')
def templates_index_redirect():
    return redirect(url_for('index'), code=301)

@app.route('/ur/pages/privacy-policy/')
def ur_pages_privacy_policy_redirect_with_slash():
    return redirect(url_for('privacy_policy', lang_code='ur'), code=301)

@app.route('/ur/pages/privacy-policy')
def ur_pages_privacy_policy_redirect():
    return redirect(url_for('privacy_policy', lang_code='ur'), code=301)

@app.route('/templates/prior-semester-final-gpa.html')
def templates_prior_semester_final_gpa_redirect():
    return redirect(url_for('prior_semester_gpa'), code=301)

@app.route('/ur/pages/about-us/')
def ur_pages_about_us_redirect():
    return redirect(url_for('about_us', lang_code='ur'), code=301)

@app.route('/ur/pages/terms-conditions/')
def ur_pages_terms_conditions_redirect():
    return redirect(url_for('terms_conditions', lang_code='ur'), code=301)

@app.route('/gpacalculatorcollege@gmail.com')
def email_contact_redirect():
    return redirect(url_for('contact'), code=301)

@app.route('/blogs/time-management-tips-for-students')
def blog_redirect():
    return redirect(url_for('blog_index'), code=301)

@app.route('/final-gpa')
def final_gpa_redirect():
    return redirect(url_for('prior_semester_gpa'), code=301)

@app.route('/prior-semester-final-gpa')
def prior_semester_final_gpa_redirect():
    return redirect(url_for('prior_semester_gpa'), code=301)

@app.route('/templates/gpa-planning-calculator.html')
def templates_gpa_planning_calculator_redirect():
    return redirect(url_for('gpa_planning'), code=301)

@app.route('/x-default/final-grade-calculator')
def x_default_final_grade_calculator_redirect():
    return redirect(url_for('final_grade_calculator'), code=301)

@app.route('/x-default/')
def x_default_root_redirect():
    return redirect(url_for('index'), code=301)

if __name__ == '__main__':
    app.run(debug=True)
