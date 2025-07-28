document.addEventListener('DOMContentLoaded', () => {
    // Apply initial language from localStorage or default
    // Assuming setLanguage function is available globally (e.g., from common.js)
    if (typeof setLanguage === 'function') {
        setLanguage(localStorage.getItem('lang') || 'en');
    }

    let currentCoursesData = [];

    // Define the allowed grades explicitly
    const allowedGrades = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'D-', 'F'];

    // --- Page 1: Main GPA Calculator Logic Elements (index.html) ---
    const courseNameInput = document.getElementById('courseName');
    const creditsInput = document.getElementById('credits');
    const gradeSelect = document.getElementById('grade');
    const addCourseBtn = document.getElementById('addCourseBtn');
    const clearCourseBtn = document.getElementById('clearCourseBtn');
    const courseTableBody = document.getElementById('courseTableBody');
    const currentGpaDisplay = document.getElementById('currentGpaDisplay');
    const resetCoursesBtn = document.getElementById('resetCoursesBtn');

    // Populate the grade dropdown with allowed grades
    if (gradeSelect) {
        gradeSelect.innerHTML = ''; // Clear existing options
        allowedGrades.forEach(grade => {
            const option = document.createElement('option');
            option.value = grade;
            option.textContent = grade;
            gradeSelect.appendChild(option);
        });
    }

    // Navigation Cards (Assumed to be on index.html)
    const priorSemesterCard = document.getElementById('priorSemesterCard');
    const gpaPlanningCard = document.getElementById('gpaPlanningCard');

    // Initialize addCourseBtn state
    if (addCourseBtn) {
        addCourseBtn.dataset.mode = 'add';
        addCourseBtn.dataset.editingIndex = '';
    }

    // Function to fetch courses and render them for the main GPA calculator
    async function fetchCoursesAndRender() {
        try {
            const response = await fetch('/get_courses', {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' }
            });
            const data = await response.json();
            if (data.status === 'success') {
                currentCoursesData = data.courses;
                renderCourses(currentCoursesData);
                if (currentGpaDisplay) {
                    currentGpaDisplay.textContent = data.currentGpa.toFixed(2);
                }
            } else {
                console.error('Failed to fetch initial courses:', data.message);
                renderCourses([]);
                if (currentGpaDisplay) {
                    currentGpaDisplay.textContent = '0.00';
                }
            }
        } catch (error) {
            console.error('Network error fetching courses:', error);
            renderCourses([]);
            if (currentGpaDisplay) {
                currentGpaDisplay.textContent = '0.00';
            }
        }
    }

    // Function to render courses into the table for the main GPA calculator
    function renderCourses(courses) {
        if (!courseTableBody) return; // Ensure element exists on the page

        courseTableBody.innerHTML = '';

        if (courses.length === 0) {
            const noCoursesRow = courseTableBody.insertRow();
            // Assuming getTranslation function is available globally
            noCoursesRow.innerHTML = `<td colspan="4" data-translate="noCoursesAdded">${typeof getTranslation === 'function' ? getTranslation('No Course Added') : 'No courses added yet.'}</td>`;
            return;
        }

        courses.forEach((course, index) => {
            const row = courseTableBody.insertRow();
            row.innerHTML = `
                <td>${course.name}</td>
                <td>${course.credits}</td>
                <td>${course.grade}</td>
                <td>
                    <a href="#" class="edit-course" data-index="${index}" data-translate="editLink">${typeof getTranslation === 'function' ? getTranslation('editLink') : 'Edit'}</a> |
                    <a href="#" class="delete-course" data-index="${index}" data-translate="deleteLink">${typeof getTranslation === 'function' ? getTranslation('deleteLink') : 'Delete'}</a>
                </td>
            `;
        });
        // Assuming translatePage function is available globally
        if (typeof translatePage === 'function') {
            translatePage();
        }
    }

    // Initial load of courses if elements for main calculator are present
    if (document.querySelector('.input-section') && document.querySelector('.course-list-section') && courseTableBody && currentGpaDisplay) {
        fetchCoursesAndRender();
    }

    // Add/Update Course functionality for main GPA calculator
    if (addCourseBtn) {
        addCourseBtn.addEventListener('click', async () => {
            const courseName = courseNameInput.value.trim();
            const credits = parseFloat(creditsInput.value);
            const grade = gradeSelect.value;
            const mode = addCourseBtn.dataset.mode;
            const editingIndex = addCourseBtn.dataset.editingIndex;

            // Assuming getTranslation function is available globally
            if (!courseName || isNaN(credits) || credits <= 0 || !grade) {
                alert(typeof getTranslation === 'function' ? getTranslation('fillAllFieldsAlert') : 'Please fill in all course details correctly.');
                return;
            }

            // Check for duplicate course name only in 'add' mode
            if (mode === 'add') {
                const isDuplicate = currentCoursesData.some(course => course.name.toLowerCase() === courseName.toLowerCase());
                // Assuming getTranslation function is available globally
                if (isDuplicate) {
                    alert(typeof getTranslation === 'function' ? getTranslation('courseAlreadyAddedAlert') : 'This course is already added. Please edit it instead.');
                    return;
                }
            }
            
            let url;
            let body;

            if (mode === 'add') {
                url = '/add_course';
                body = JSON.stringify({ courseName, credits, grade });
            } else if (mode === 'edit') {
                url = '/update_course';
                body = JSON.stringify({ index: parseInt(editingIndex), courseName, credits, grade });
            }

            try {
                const response = await fetch(url, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: body
                });
                const data = await response.json();
                if (data.status === 'success') {
                    currentCoursesData = data.courses;
                    renderCourses(currentCoursesData);
                    currentGpaDisplay.textContent = data.currentGpa.toFixed(2);

                    // Reset form
                    courseNameInput.value = '';
                    creditsInput.value = '';
                    gradeSelect.value = '';

                    // Reset button to add mode
                    // Assuming getTranslation function is available globally
                    addCourseBtn.textContent = typeof getTranslation === 'function' ? getTranslation('addCourseButton') : 'Add Course';
                    addCourseBtn.dataset.mode = 'add';
                    addCourseBtn.dataset.editingIndex = '';
                    courseNameInput.removeAttribute('readonly');
                } else {
                    alert('Error processing course: ' + (data.message || 'Unknown error'));
                }
            } catch (error) {
                console.error('Error processing course:', error);
                alert('Network error. Could not process course.');
            }
        });
    }

    // Clear button functionality for main GPA calculator
    if (clearCourseBtn) {
        clearCourseBtn.addEventListener('click', () => {
            courseNameInput.value = '';
            creditsInput.value = '';
            gradeSelect.value = '';
            // Assuming getTranslation function is available globally
            addCourseBtn.textContent = typeof getTranslation === 'function' ? getTranslation('addCourseButton') : 'Add Course';
            addCourseBtn.dataset.mode = 'add';
            addCourseBtn.dataset.editingIndex = '';
            courseNameInput.removeAttribute('readonly');
        });
    }

    // Reset All Courses button functionality for main GPA calculator
    if (resetCoursesBtn) {
        resetCoursesBtn.addEventListener('click', async () => {
            // Assuming getTranslation function is available globally
            if (confirm(typeof getTranslation === 'function' ? getTranslation('confirmResetMessage') : 'Are you sure you want to remove all courses?')) {
                try {
                    const response = await fetch('/reset_courses', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' }
                    });
                    const data = await response.json();
                    if (data.status === 'success') {
                        currentCoursesData = [];
                        renderCourses(currentCoursesData);
                        currentGpaDisplay.textContent = '0.00';
                        // Assuming getTranslation function is available globally
                        alert(typeof getTranslation === 'function' ? getTranslation('coursesClearedMessage') : 'All courses have been cleared.');
                    } else {
                        alert('Error clearing courses: ' + (data.message || 'Unknown error'));
                    }
                } catch (error) {
                    console.error('Error resetting courses:', error);
                    alert('Network error. Could not reset courses.');
                }
            }
        });
    }

    // Event Delegation for Update/Delete Buttons on the Course Table (main GPA calculator)
    if (courseTableBody) {
        courseTableBody.addEventListener('click', async (event) => {
            if (event.target.classList.contains('edit-course')) {
                event.preventDefault();
                const index = parseInt(event.target.dataset.index);
                const course = currentCoursesData[index];

                courseNameInput.value = course.name;
                courseNameInput.setAttribute('readonly', 'readonly');
                creditsInput.value = course.credits;
                gradeSelect.value = course.grade;

                // Assuming getTranslation function is available globally
                addCourseBtn.textContent = typeof getTranslation === 'function' ? getTranslation('updateButton') : 'Update Course';
                addCourseBtn.dataset.mode = 'edit';
                addCourseBtn.dataset.editingIndex = index;
            } else if (event.target.classList.contains('delete-course')) {
                event.preventDefault();
                const index = parseInt(event.target.dataset.index);
                // Assuming getTranslation function is available globally
                if (confirm(typeof getTranslation === 'function' ? getTranslation('confirmDeleteMessage') : 'Are you sure you want to delete this course?')) {
                    try {
                        const response = await fetch('/delete_course', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ index: parseInt(index) })
                        });
                        const data = await response.json();
                        if (data.status === 'success') {
                            currentCoursesData = data.courses;
                            renderCourses(currentCoursesData);
                            currentGpaDisplay.textContent = data.currentGpa.toFixed(2);
                            if (addCourseBtn.dataset.mode === 'edit' && addCourseBtn.dataset.editingIndex === String(index)) {
                                clearCourseBtn.click(); // Clear form if the deleted course was being edited
                            }
                        } else {
                            alert('Error deleting course: ' + (data.message || 'Unknown error'));
                        }
                    } catch (error) {
                        console.error('Error deleting course:', error);
                        alert('Network error. Could not delete course.');
                    }
                }
            }
        });
    }

    // Navigation Card Click Listeners (index.html)
    if (priorSemesterCard) {
        priorSemesterCard.addEventListener('click', () => {
            window.location.href = '/prior-semester-gpa';
        });
    }

    if (gpaPlanningCard) {
        gpaPlanningCard.addEventListener('click', () => {
            window.location.href = '/gpa-planning';
        });
    }

    // --- Page 2: Prior Semester / Final GPA Calculator Logic (prior-semester-gpa.html) ---
    const oldTotalCreditsInput = document.getElementById('oldTotalCredits');
    const oldGpaInput = document.getElementById('oldGpa');
    const newSemesterCreditsInput = document.getElementById('newSemesterCredits');
    const newSemesterGpaInput = document.getElementById('newSemesterGpa');
    const calculateCombinedGpaBtn = document.getElementById('calculateCombinedGpaBtn');
    const combinedGpaResult = document.getElementById('combinedGpaResult');
    const clearCombinedBtn = document.getElementById('clearCombinedBtn');

    // This section is for the 'Calculate Final Cumulative GPA' which was removed from prior-semester-gpa.html
    // Keeping the elements here in case they are used on another page (e.g., gpa-planning.html or a dedicated final GPA page)
    const finalTotalCreditsInput = document.getElementById('finalTotalCredits');
    const finalGpaInput = document.getElementById('finalGpa');
    const calculateFinalGpaBtn = document.getElementById('calculateFinalGpaBtn');
    const finalGpaResult = document.getElementById('finalGpaResult');

    if (calculateCombinedGpaBtn) {
        calculateCombinedGpaBtn.addEventListener('click', async () => {
            const oldTotalCredits = parseFloat(oldTotalCreditsInput.value);
            const oldGpa = parseFloat(oldGpaInput.value);
            const newSemesterCredits = parseFloat(newSemesterCreditsInput.value);
            const newSemesterGpa = parseFloat(newSemesterGpaInput.value);

            // Input validation for Prior Semester GPA Calculator
            if (isNaN(oldTotalCredits) || oldTotalCredits < 0 ||
                isNaN(oldGpa) || oldGpa < 0 || oldGpa > 4 ||
                isNaN(newSemesterCredits) || newSemesterCredits < 0 ||
                isNaN(newSemesterGpa) || newSemesterGpa < 0 || newSemesterGpa > 4) {
                // Display error message
                combinedGpaResult.innerHTML = `<p style="color: red;">${typeof getTranslation === 'function' ? getTranslation('invalidInputForCombinedGpa') : 'Please enter valid numbers for all fields. GPA should be between 0 and 4.'}</p>`;
                combinedGpaResult.style.display = 'block';
                return;
            }

            try {
                // Client-side calculation for combined GPA (as per previous instructions for pure HTML/JS)
                const oldGradePoints = oldTotalCredits * oldGpa;
                const newGradePoints = newSemesterCredits * newSemesterGpa;
                const combinedTotalCredits = oldTotalCredits + newSemesterCredits;
                const combinedGradePoints = oldGradePoints + newGradePoints;

                let combinedGpa;
                if (combinedTotalCredits === 0) {
                    combinedGpa = 0; // If no credits, GPA is 0
                } else {
                    combinedGpa = combinedGradePoints / combinedTotalCredits;
                }
                
                combinedGpaResult.innerHTML = `<span style="font-size:1.2em; font-weight:bold; color: var(--dark-text);" data-translate="combinedGpaResultText">${typeof getTranslation === 'function' ? getTranslation('combinedGpaResultText').replace('{{gpa}}', combinedGpa.toFixed(2)) : `Your Combined Cumulative GPA: ${combinedGpa.toFixed(2)}`}</span>`;
                combinedGpaResult.style.display = 'block';
                combinedGpaResult.style.backgroundColor = 'var(--primary-color)'; /* Light cream */
                combinedGpaResult.style.borderColor = 'var(--secondary-color)';
                combinedGpaResult.style.color = 'var(--dark-text)';

            } catch (error) {
                console.error('Error calculating combined GPA:', error);
                alert('An unexpected error occurred during calculation.');
                combinedGpaResult.style.display = 'none';
            }
        });
    }

    if (clearCombinedBtn) {
        clearCombinedBtn.addEventListener('click', () => {
            oldTotalCreditsInput.value = '';
            oldGpaInput.value = '';
            newSemesterCreditsInput.value = '';
            newSemesterGpaInput.value = '';
            combinedGpaResult.innerHTML = '';
            combinedGpaResult.style.display = 'none'; // Hide the result
        });
    }

    // Final GPA Calculator Logic (if present on any page)
    if (calculateFinalGpaBtn) {
        calculateFinalGpaBtn.addEventListener('click', async () => {
            const totalCredits = parseFloat(finalTotalCreditsInput.value);
            const gpa = parseFloat(finalGpaInput.value);

            // Input validation
            if (isNaN(totalCredits) || totalCredits < 0 ||
                isNaN(gpa) || gpa < 0 || gpa > 4) {
                // Display error message
                finalGpaResult.innerHTML = `<p style="color: red;">${typeof getTranslation === 'function' ? getTranslation('invalidInputForFinalGpa') : 'Please enter valid numbers for Total Credits and GPA. GPA should be between 0 and 4.'}</p>`;
                finalGpaResult.style.display = 'block';
                return;
            }

            try {
                // Assuming a client-side calculation for this as well, if no backend endpoint is guaranteed
                const finalCumulativeGpa = gpa; // If it's just displaying existing GPA

                finalGpaResult.innerHTML = `<p data-translate="finalGpaResultText">${typeof getTranslation === 'function' ? getTranslation('finalGpaResultText').replace('{{gpa}}', finalCumulativeGpa.toFixed(2)) : `Your Final Cumulative GPA: ${finalCumulativeGpa.toFixed(2)}`}</p>`;
                finalGpaResult.style.display = 'block';
                if (typeof setLanguage === 'function') {
                    setLanguage(localStorage.getItem('lang') || 'en');
                }
            } catch (error) {
                console.error('Error calculating final GPA:', error);
                alert('An unexpected error occurred during calculation.');
                finalGpaResult.style.display = 'none';
            }
        });
    }


    // --- Page 3: GPA Planning Calculator Logic (gpa-planning.html) ---
    const goalGpaInput = document.getElementById('goalGpa');
    const currentGpaPlanningInput = document.getElementById('currentGpa');
    const currentTotalCreditsInput = document.getElementById('currentTotalCredits');
    const nextSemesterCreditsInput = document.getElementById('nextSemesterCredits');
    const calculateRequiredGpaBtn = document.getElementById('calculateRequiredGpaBtn');
    const requiredGpaResult = document.getElementById('requiredGpaResult');
    const clearPlanningBtn = document.getElementById('clearPlanningBtn');

    if (calculateRequiredGpaBtn) {
        calculateRequiredGpaBtn.addEventListener('click', async () => {
            const goalGpa = parseFloat(goalGpaInput.value);
            const currentGpa = parseFloat(currentGpaPlanningInput.value);
            const currentTotalCredits = parseFloat(currentTotalCreditsInput.value);
            const nextSemesterCredits = parseFloat(nextSemesterCreditsInput.value);

            // Input validation for GPA Planning Calculator
            if (isNaN(goalGpa) || goalGpa < 0 || goalGpa > 4 ||
                isNaN(currentGpa) || currentGpa < 0 || currentGpa > 4 ||
                isNaN(currentTotalCredits) || currentTotalCredits < 0 ||
                isNaN(nextSemesterCredits) || nextSemesterCredits <= 0) { // nextSemesterCredits must be > 0
                // Display error message
                requiredGpaResult.innerHTML = `<p style="color: red;">${typeof getTranslation === 'function' ? getTranslation('invalidInputForPlanningGpa') : 'Please enter valid numbers for all fields. GPAs should be between 0 and 4, and credits must be positive.'}</p>`;
                requiredGpaResult.style.display = 'block';
                return;
            }

            try {
                // Client-side calculation for required GPA
                const currentGradePoints = currentGpa * currentTotalCredits;
                const desiredTotalGradePoints = goalGpa * (currentTotalCredits + nextSemesterCredits);
                const requiredNextSemesterGradePoints = desiredTotalGradePoints - currentGradePoints;
                let requiredGpa;

                if (nextSemesterCredits === 0) {
                    requiredGpa = 0; // Avoid division by zero, though validation already checks for > 0
                } else {
                    requiredGpa = requiredNextSemesterGradePoints / nextSemesterCredits;
                }
                
                let messageKey = "requiredGpaResultText";
                let resultStyle = ''; // Default style

                if (requiredGpa > 4.0) {
                    messageKey = "unrealisticGpaGoal";
                    resultStyle = 'color: red;'; // Indicate it's too high
                } else if (requiredGpa < 0) {
                    messageKey = "gpaGoalAlreadyMet";
                    resultStyle = 'color: green;'; // Indicate goal is already met
                }
                
                let translationText = typeof getTranslation === 'function' ? getTranslation(messageKey) : '';
                if (translationText) {
                    translationText = translationText
                        .replace('{{gpa}}', requiredGpa.toFixed(2))
                        .replace('{{goal}}', goalGpa.toFixed(2));
                } else {
                    // Fallback in case translation isn't available
                    if (requiredGpa > 4.0) {
                            translationText = `To reach a goal GPA of ${goalGpa.toFixed(2)}, you would need an unrealistic GPA of ${requiredGpa.toFixed(2)} in your next semester.`;
                    } else if (requiredGpa < 0) {
                        translationText = `Your current GPA already meets or exceeds your goal of ${goalGpa.toFixed(2)}!`;
                    } else {
                        translationText = `You need a GPA of ${requiredGpa.toFixed(2)} in your next semester to reach a goal GPA of ${goalGpa.toFixed(2)}.`;
                    }
                }

                requiredGpaResult.innerHTML = `<p data-translate="${messageKey}" style="${resultStyle}">${translationText}</p>`;
                requiredGpaResult.style.display = 'block';
                if (typeof setLanguage === 'function') {
                    setLanguage(localStorage.getItem('lang') || 'en');
                }
            } catch (error) {
                console.error('Network error calculating required GPA:', error);
                alert('Network error. Could not calculate required GPA.');
                requiredGpaResult.style.display = 'none';
            }
        });
    }

    if (clearPlanningBtn) {
        clearPlanningBtn.addEventListener('click', () => {
            goalGpaInput.value = '';
            currentGpaPlanningInput.value = '';
            currentTotalCreditsInput.value = '';
            nextSemesterCreditsInput.value = '';
            requiredGpaResult.innerHTML = '';
            requiredGpaResult.style.display = 'none'; // Hide the result
        });
    }

    // --- FAQ Section Toggle (for pages that have it, e.g., index.html and prior-semester-gpa.html) ---
    // This logic needs to be robust for any page it might appear on.
    // Assuming `toggle-icon` is present in HTML for this to work well.
    document.querySelectorAll('.faq-section .faq-item h3').forEach(header => {
        // Add toggle icon if not already present
        if (!header.querySelector('.toggle-icon')) {
            header.innerHTML += ' <span class="toggle-icon">+</span>';
        }
        
        // Hide answers by default, if not already handled by CSS
        const paragraph = header.nextElementSibling;
        if (paragraph && paragraph.tagName === 'P' && paragraph.style.maxHeight === '') {
            paragraph.style.maxHeight = '0';
            paragraph.style.overflow = 'hidden';
            paragraph.style.transition = 'max-height 0.3s ease-out';
        }

        header.addEventListener('click', () => {
            const paragraph = header.nextElementSibling;
            const toggleIcon = header.querySelector('.toggle-icon');

            if (paragraph.style.maxHeight && paragraph.style.maxHeight !== '0px') {
                paragraph.style.maxHeight = '0';
                toggleIcon.textContent = '+';
                header.classList.remove('active'); // Remove active class on collapse
            } else {
                // Close all other open FAQs (accordion behavior)
                document.querySelectorAll('.faq-section .faq-item p').forEach(p => {
                    if (p !== paragraph && p.style.maxHeight && p.style.maxHeight !== '0px') {
                        p.style.maxHeight = '0';
                        p.previousElementSibling.querySelector('.toggle-icon').textContent = '+';
                        p.previousElementSibling.classList.remove('active');
                    }
                });
                paragraph.style.maxHeight = paragraph.scrollHeight + "px"; // Expand to full height
                toggleIcon.textContent = '-';
                header.classList.add('active'); // Add active class on expand
            }
        });
    });
});

// --- Language Switcher Logic ---
// This should ideally be in a common.js file if it's used across multiple pages
const languageSwitcher = document.getElementById('language-switcher');
if (languageSwitcher) {
    languageSwitcher.addEventListener('change', (event) => {
        const selectedLang = event.target.value;
        // Assuming setLanguage function is available globally (e.g., from common.js)
        if (typeof setLanguage === 'function') {
            setLanguage(selectedLang);
        }
    });

    // Set initial value of the language switcher based on preferred language
    // Assuming getPreferredLanguage function is available globally
    if (typeof getPreferredLanguage === 'function') {
        languageSwitcher.value = getPreferredLanguage();
    }
}