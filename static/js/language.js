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
            
            const urlPath = window.location.pathname;
            const urlLangRegex = /^\/(ur|ar|pt|es|fr|de|ru)\b/i;
            const match = urlPath.match(urlLangRegex);

            let currentLanguage;
            if (match && match[1]) {
                currentLanguage = match[1];
                localStorage.setItem('selectedLanguage', currentLanguage);
            } else {
                // Ye naya code hai
                localStorage.removeItem('selectedLanguage');
                currentLanguage = defaultLanguage;
            }
            
            applyTranslations(currentLanguage);
            
            if (languageSwitcher) {
                languageSwitcher.value = currentLanguage;
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
        
        document.querySelectorAll('a').forEach(link => {
            const href = link.getAttribute('href');
            if (href && href.startsWith('/')) {
                const regex = /^\/(ur|ar|pt|es|fr|de|ru)\b/i;
                const newPath = href.replace(regex, '');
                if (lang === 'en') {
                    link.href = newPath;
                } else {
                    link.href = `/${lang}${newPath}`;
                }
            }
        });
    };
    
    const setLanguage = (lang) => {
        if (lang === defaultLanguage) {
            localStorage.removeItem('selectedLanguage');
        } else {
            localStorage.setItem('selectedLanguage', lang);
        }
        
        const currentUrl = window.location.pathname;
        let newUrl;
        
        const regex = /^\/(ur|ar|pt|es|fr|de|ru)\b/i;
        const pathWithoutLang = currentUrl.replace(regex, '');
        if (lang === 'en') {
            newUrl = pathWithoutLang;
        } else {
            newUrl = `/${lang}${pathWithoutLang}`;
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