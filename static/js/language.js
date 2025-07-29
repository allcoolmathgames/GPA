// static/js/language.js (KEEP THIS AS IS FROM LAST TURN)
const translations = {};

async function loadTranslations(pageName) {
    try {
        const response = await fetch(`/static/lang/${pageName}.json`);
        if (!response.ok) {
            console.warn(`Translation file not found or failed to load: /static/lang/${pageName}.json`);
            return;
        }
        const data = await response.json();
        Object.assign(translations, data);
    } catch (error) {
        console.error("Error loading translations:", error);
    }
}

// Make getTranslation globally available for other scripts
function getTranslation(key) {
    const lang = localStorage.getItem('lang') || 'en';
    if (translations[key] && translations[key][lang]) {
        return translations[key][lang];
    }
    return key; // Return the key itself if translation not found
}

// Make translatePage globally available to re-translate dynamic content
function translatePage() {
    // --- Apply text content translations ---
    document.querySelectorAll('[data-translate]').forEach(element => {
        const key = element.getAttribute('data-translate');
        const lang = localStorage.getItem('lang') || 'en'; // Get current lang again
        if (translations[key] && translations[key][lang]) {
            if (element.tagName === 'TITLE' || (element.tagName === 'META' && element.name === 'description')) {
                element.setAttribute('content', translations[key][lang]);
            } else {
                element.textContent = translations[key][lang];
            }
        } else {
            // Fallback to English if current language translation is missing
            if (translations[key] && translations[key]['en']) {
                element.textContent = translations[key]['en'];
            } else {
                console.warn(`Translation key '${key}' not found for language '${lang}' or 'en'.`);
            }
        }
    });

    // --- Update placeholders ---
    document.querySelectorAll('[data-translate-placeholder]').forEach(element => {
        const key = element.getAttribute('data-translate-placeholder');
        const lang = localStorage.getItem('lang') || 'en'; // Get current lang again
        if (translations[key] && translations[key][lang]) {
            element.placeholder = translations[key][lang];
        } else {
            // Fallback to English if current language translation is missing
            if (translations[key] && translations[key]['en']) {
                element.placeholder = translations[key]['en'];
            }
        }
    });
}


async function setLanguage(lang) {
    localStorage.setItem('lang', lang);
    document.body.setAttribute('data-lang', lang);

    // Determine the base path of the current page (without language prefix)
    let currentRelativePath = window.location.pathname;
    let basePagePath = currentRelativePath;

    // Remove existing language prefix if present (e.g., /ur/gpa-calculator -> /gpa-calculator)
    if (basePagePath.startsWith('/ur/')) {
        basePagePath = basePagePath.substring(3);
    }
    // Handle root path consistency: /ur/ becomes / for non-ur pages, and /ur/ for ur pages
    if (basePagePath === '') { // If it was just '/' or '/ur/'
        basePagePath = '/';
    }

    // Map page path to its corresponding JSON file name
    const pageJsonMap = {
        '/': 'index', // Root path should map to index
        'gpa-calculator': 'index', // Your main GPA page is often 'index' in terms of content
        'prior-semester-gpa': 'prior-semester-final-gpa',
        'gpa-planning': 'gpa-planning-calculator',
        'blogs': 'blogs',
        'privacy-policy': 'privacy-policy',
        'terms-conditions': 'terms-conditions',
        'about-us': 'about-us',
        'contact': 'contact'
    };
    // Use substring(1) to remove leading slash for lookup, unless it's just '/'
    const actualJsonFileName = pageJsonMap[basePagePath === '/' ? '/' : basePagePath.substring(1)] || null;

    // Load common translations first, then page-specific
    await loadTranslations('common');
    if (actualJsonFileName) {
        await loadTranslations(actualJsonFileName);
    } else {
        console.log(`Translation not explicitly configured for page: ${basePagePath}. Only common translations will apply.`);
    }

    // --- Update current page URL in browser history ---
    let newPathname = '';
    if (lang === 'ur') {
        newPathname = (basePagePath === '/') ? '/ur/' : '/ur' + basePagePath;
    } else {
        newPathname = basePagePath;
    }

    if (window.location.pathname !== newPathname) {
        history.pushState({ path: newPathname }, '', newPathname);
        console.log(`Browser URL updated: ${currentRelativePath} -> ${newPathname}`);
    }

    // --- Update canonical and hreflang links ---
    const canonicalLink = document.querySelector('link[rel="canonical"]');
    if (canonicalLink) {
        // Construct the full absolute URL for the canonical link
        canonicalLink.setAttribute('href', new URL(newPathname, window.location.origin).href);
        console.log(`Canonical updated: ${canonicalLink.href}`);
    }

    document.querySelectorAll('link[rel="alternate"][hreflang]').forEach(link => {
        const hreflang = link.getAttribute('hreflang');
        // Ensure we always work with the base path for hreflang links
        let currentLinkBaseHref = new URL(link.getAttribute('href')).pathname;

        if (currentLinkBaseHref.startsWith('/ur/')) {
            currentLinkBaseHref = currentLinkBaseHref.substring(3);
        }
        if (currentLinkBaseHref === '') {
            currentLinkBaseHref = '/';
        }

        let newAlternateHref = '';
        if (hreflang === 'ur') {
            newAlternateHref = (currentLinkBaseHref === '/') ? '/ur/' : '/ur' + currentLinkBaseHref;
        } else {
            newAlternateHref = currentLinkBaseHref;
        }
        link.setAttribute('href', new URL(newAlternateHref, window.location.origin).href);
        console.log(`Hreflang link (${hreflang}) updated: ${link.href}`);
    });

    // --- Update all internal <a> tags' hrefs ---
    document.querySelectorAll('a[href]').forEach(linkElement => {
        const originalHref = linkElement.getAttribute('href');

        // Check if it's an internal, relative path (starts with / but not //, and no explicit protocol)
        if (originalHref && originalHref.startsWith('/') && !originalHref.startsWith('//') && !originalHref.includes('://')) {
            let linkPath = originalHref;

            // Remove any existing language prefix from the link's path
            if (linkPath.startsWith('/ur/')) {
                linkPath = linkPath.substring(3); 
            }
            if (linkPath === '') { // For home page links
                linkPath = '/';
            }

            let newLinkHref = '';
            if (lang === 'ur') {
                newLinkHref = (linkPath === '/') ? '/ur/' : '/ur' + linkPath;
            } else {
                newLinkHref = linkPath;
            }

            // Only update if the href has truly changed
            if (linkElement.getAttribute('href') !== newLinkHref) {
                linkElement.setAttribute('href', newLinkHref);
                console.log(`Link updated: ${originalHref} -> ${newLinkHref}`);
            }
        } else {
            // console.log(`Skipping non-internal or problematic link (originalHref: ${originalHref}): ${linkElement.href}`);
        }
    });

    // Apply all text content and placeholder translations after links are updated
    translatePage(); 
}


document.addEventListener('DOMContentLoaded', async () => {
    // Ye line language.js mein language-switcher ko handle kar rahi hai
    // agar aapke paas page par multiple language switchers hain.
    const languageSwitchers = document.querySelectorAll('.language-switcher');
    let initialLang = localStorage.getItem('lang') || 'en';

    // Initial language apply
    await setLanguage(initialLang);

    // Set initial value for all switchers and add event listeners
    languageSwitchers.forEach(switcher => {
        switcher.value = initialLang;
        switcher.addEventListener('change', async (event) => {
            const newLang = event.target.value;
            console.log(`Language changed via dropdown to: ${newLang}`);
            await setLanguage(newLang);
            // Update other language switchers on the page to reflect the change
            languageSwitchers.forEach(otherSwitcher => {
                if (otherSwitcher !== event.target) {
                    otherSwitcher.value = newLang;
                }
            });
        });
    });
});