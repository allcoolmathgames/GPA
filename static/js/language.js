document.addEventListener('DOMContentLoaded', () => {
    const languageSwitcher = document.getElementById('language-switcher');
    const defaultLanguage = 'en';
    let translations = {};
    const loadTranslations = async () => {
        try {
            const [commonResponse, indexResponse, gpaCalculatorResponse] = await Promise.all([
                fetch('/static/lang/common.json'),
                fetch('/static/lang/index.json'),
                fetch('/static/lang/gpa-calculator.json')
            ]);
            if (!commonResponse.ok || !indexResponse.ok || !gpaCalculatorResponse.ok) {
                console.error("Could not load one or more translation files.");
                return;
            }
            const commonTranslations = await commonResponse.json();
            const indexTranslations = await indexResponse.json();
            const gpaCalculatorTranslations = await gpaCalculatorResponse.json();
            for (const lang in commonTranslations) {
                if (commonTranslations.hasOwnProperty(lang)) {
                    translations[lang] = {
                        ...commonTranslations[lang],
                        ...indexTranslations[lang],
                        ...gpaCalculatorTranslations[lang]
                    };
                }
            }
            console.log("All translations loaded successfully.");
            const savedLanguage = localStorage.getItem('selectedLanguage') || defaultLanguage;
            applyTranslations(savedLanguage);
            
            if (languageSwitcher) {
                languageSwitcher.value = savedLanguage;
            }
        } catch (error) {
            console.error("Error loading translations:", error);
        }
    };
    const applyTranslations = (lang) => {
        const langData = translations[lang] || translations[defaultLanguage];
        document.querySelectorAll('[data-translate]').forEach(element => {
            const key = element.getAttribute('data-translate');
            const translation = langData[key];
            if (translation) {
                if (typeof translation === 'string') {
                    if (translation.includes('<')) {
                        element.innerHTML = translation;
                    } else {
                        element.textContent = translation;
                    }
                } else if (typeof translation === 'object' && translation.text) {
                    element.textContent = translation.text;
                    if (element.tagName === 'A' && translation.url) {
                        element.href = translation.url;
                    }
                }
            }
        });
        console.log(`Translations applied for language: ${lang}`);
        
        // URLs ke liye naya code
        document.querySelectorAll('a').forEach(link => {
            const href = link.getAttribute('href');
            if (href && href.startsWith('/')) {
                const regex = /^\/(ur|ar|pt|es|de|ru)\b/i; // All languages except English
                const newPath = href.replace(regex, '');
                if (lang === 'en') {
                    link.href = newPath; // English ke liye path se language code hata dein
                } else {
                    link.href = `/${lang}${newPath}`; // Baaki languages ke liye code add karein
                }
            }
        });
    };
    const setLanguage = (lang) => {
        localStorage.setItem('selectedLanguage', lang);
        
        const currentUrl = window.location.pathname;
        let newUrl;
        
        // Pehle se maujood language code ko remove karein
        const regex = /^\/(ur|ar|pt|es|de|ru)\b/i; // Apni languages ke mutabik update karein
        const pathWithoutLang = currentUrl.replace(regex, '');
        if (lang === 'en') {
            newUrl = pathWithoutLang; // English ke liye sirf path rakhein
        } else {
            newUrl = `/${lang}${pathWithoutLang}`; // Baaki languages ke liye code add karein
        }
        
        history.pushState({}, '', newUrl);
    };
    loadTranslations();
    if (languageSwitcher) {
        languageSwitcher.addEventListener('change', (event) => {
            const newLang = event.target.value;
            setLanguage(newLang);
            location.reload(); 
        });
    }
});