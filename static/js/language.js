const translations = {}; // This will hold all loaded translations

async function loadTranslations(pageName) {
    try {
        const response = await fetch(`/static/lang/${pageName}.json`);
        if (!response.ok) {
            throw new Error(`Failed to load translations for ${pageName}.json`);
        }
        const data = await response.json();
        Object.assign(translations, data); // Merge page-specific translations
    } catch (error) {
        console.error("Error loading translations:", error);
    }
}

async function setLanguage(lang) {
    localStorage.setItem('lang', lang); // Save preferred language

    // Determine current page to load specific translations
    let currentPage = window.location.pathname.replace(/\//g, '');
    if (currentPage === '') currentPage = 'index'; // Default for homepage

    // Load common translations (e.g., header, footer) and then page-specific
    await loadTranslations('common'); // Assuming you'll have a common.json
    await loadTranslations(currentPage);

    document.querySelectorAll('[data-translate]').forEach(element => {
        const key = element.getAttribute('data-translate');
        if (translations[key] && translations[key][lang]) {
            element.textContent = translations[key][lang];
        } else {
            // Fallback to English if translation not found
            if (translations[key] && translations[key]['en']) {
                element.textContent = translations[key]['en'];
            } else {
                console.warn(`Translation key '${key}' not found for language '${lang}'.`);
            }
        }
    });

    // Update placeholders separately as textContent won't work
    document.querySelectorAll('[data-translate-placeholder]').forEach(element => {
        const key = element.getAttribute('data-translate-placeholder');
        if (translations[key] && translations[key][lang]) {
            element.placeholder = translations[key][lang];
        } else {
            if (translations[key] && translations[key]['en']) {
                element.placeholder = translations[key]['en'];
            }
        }
    });
}

function getTranslation(key) {
    const lang = localStorage.getItem('lang') || 'en';
    if (translations[key] && translations[key][lang]) {
        return translations[key][lang];
    }
    return key; // Return key if translation not found
}

// Initial language set on DOMContentLoaded in script.js, but also useful to call here if needed
// setLanguage(localStorage.getItem('lang') || 'en');