document.addEventListener('DOMContentLoaded', function() {

<<<<<<< HEAD
    //  Language Switcher Logic ---
=======
    // --- Language Switcher Logic ---
>>>>>>> b68f0f323ea798f7aabda9347c81dab8907576ec
    const languageSwitcher = document.getElementById('language-switcher');
    if (languageSwitcher) {
        languageSwitcher.addEventListener('change', (event) => {
            const selectedLang = event.target.value;
            if (typeof setLanguage === 'function') {
                setLanguage(selectedLang);
            }
        });
        if (typeof getPreferredLanguage === 'function') {
            languageSwitcher.value = getPreferredLanguage();
        }
    }
});