// Welcome popup: email signup for a 50% off code (sent by /api/discount-signup).
// Shared across pages so the offer, copy, and logic live in one place.
(function () {
    var STORAGE_KEY = 'pfe_welcome50';
    var DISMISS_DAYS = 30;
    var SHOW_DELAY_MS = 3000;

    function getState() {
        try { return JSON.parse(localStorage.getItem(STORAGE_KEY)) || {}; } catch (e) { return {}; }
    }

    function setState(state) {
        try { localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); } catch (e) {}
    }

    function shouldShow() {
        var state = getState();
        if (state.subscribed) return false;
        if (state.dismissedAt && Date.now() - state.dismissedAt < DISMISS_DAYS * 864e5) return false;
        // Visitors arriving from our emails (?email=) are already subscribers.
        if (new URLSearchParams(window.location.search).get('email')) return false;
        return true;
    }

    function track(event, props) {
        if (typeof dataLayer !== 'undefined') {
            dataLayer.push(Object.assign({ event: event, popup: 'welcome50', page_path: location.pathname }, props || {}));
        }
    }

    var css = '' +
        '.w50-overlay{position:fixed;inset:0;z-index:10000;background:rgba(30,45,51,.55);display:flex;align-items:center;justify-content:center;padding:20px;opacity:0;transition:opacity .3s ease}' +
        '.w50-overlay.w50-show{opacity:1}' +
        '.w50-modal{position:relative;width:100%;max-width:440px;background:#FAFCFD;border-radius:24px;padding:40px 36px 32px;text-align:center;box-shadow:0 30px 80px rgba(30,45,51,.3);font-family:Karla,-apple-system,BlinkMacSystemFont,sans-serif;color:#1E2D33;transform:translateY(16px);transition:transform .35s cubic-bezier(.25,.46,.45,.94)}' +
        '.w50-show .w50-modal{transform:translateY(0)}' +
        '.w50-close{position:absolute;top:14px;right:14px;width:36px;height:36px;border:none;border-radius:50%;background:rgba(90,173,181,.1);color:#4A5C65;font-size:22px;line-height:1;cursor:pointer}' +
        '.w50-close:hover{background:rgba(90,173,181,.2)}' +
        '.w50-badge{display:inline-block;background:rgba(90,173,181,.12);color:#3D8E96;font-size:.78rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;padding:6px 14px;border-radius:50px;margin-bottom:16px}' +
        '.w50-modal h2{font-family:"Cormorant Garamond",Georgia,serif;font-size:2.4rem;font-weight:600;line-height:1.1;margin:0 0 12px}' +
        '.w50-modal h2 span{background:linear-gradient(135deg,#5AADB5 0%,#7BA4D4 100%);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}' +
        '.w50-modal p{font-size:1rem;line-height:1.6;color:#4A5C65;margin:0 0 22px}' +
        '.w50-form{display:flex;flex-direction:column;gap:10px}' +
        '.w50-form input[type=email]{width:100%;font:inherit;font-size:1rem;padding:15px 18px;border:1.5px solid #E8EEF0;border-radius:50px;background:#fff;color:#1E2D33;outline:none;box-sizing:border-box}' +
        '.w50-form input[type=email]:focus{border-color:#5AADB5;box-shadow:0 0 0 3px rgba(90,173,181,.15)}' +
        '.w50-hp{position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden}' +
        '.w50-submit{font:inherit;font-size:1.05rem;font-weight:700;color:#fff;background:linear-gradient(135deg,#5AADB5 0%,#7BA4D4 100%);border:none;border-radius:50px;padding:15px 24px;cursor:pointer;box-shadow:0 10px 30px rgba(90,173,181,.35)}' +
        '.w50-submit:disabled{opacity:.7;cursor:wait}' +
        '.w50-error{min-height:1.2em;font-size:.88rem;color:#B5566F;margin:2px 0 0}' +
        '.w50-skip{display:inline-block;margin-top:6px;font:inherit;font-size:.88rem;color:#8A9BA3;background:none;border:none;text-decoration:underline;cursor:pointer}' +
        '.w50-fine{font-size:.78rem!important;color:#8A9BA3!important;margin:14px 0 0!important}' +
        '.w50-success-icon{width:56px;height:56px;margin:0 auto 16px;border-radius:50%;background:linear-gradient(135deg,#5AADB5 0%,#7BA4D4 100%);color:#fff;display:flex;align-items:center;justify-content:center}' +
        '@media (max-width:600px){' +
            '.w50-overlay{align-items:flex-end;padding:0}' +
            '.w50-modal{max-width:none;border-radius:24px 24px 0 0;padding:32px 22px calc(24px + env(safe-area-inset-bottom));transform:translateY(100%)}' +
            '.w50-modal h2{font-size:2rem}' +
        '}';

    var formHtml = '' +
        '<span class="w50-badge">New here? Welcome</span>' +
        '<h2 id="w50-title">Get <span>50% Off</span> Your First Course</h2>' +
        '<p>Enter your email and I\'ll send you a code for half off any of my online pelvic floor courses.</p>' +
        '<form class="w50-form" novalidate>' +
            '<label for="w50-email" class="w50-hp">Email address</label>' +
            '<input id="w50-email" type="email" name="email" placeholder="Your email address" autocomplete="email" required>' +
            '<div class="w50-hp" aria-hidden="true"><input type="text" name="website" tabindex="-1" autocomplete="off"></div>' +
            '<button type="submit" class="w50-submit">Send My 50% Code</button>' +
            '<p class="w50-error" role="alert"></p>' +
        '</form>' +
        '<button type="button" class="w50-skip">No thanks</button>' +
        '<p class="w50-fine">You\'ll also get occasional pelvic health tips from Sheree. Unsubscribe anytime.</p>';

    var successHtml = '' +
        '<div class="w50-success-icon"><svg width="28" height="28" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"/></svg></div>' +
        '<h2 id="w50-title">Check Your <span>Inbox</span></h2>' +
        '<p>Your 50% off code is on its way. If you don\'t see it in a few minutes, check your spam or promotions folder.</p>' +
        '<button type="submit" class="w50-submit w50-done">Keep Browsing</button>';

    function open() {
        var style = document.createElement('style');
        style.textContent = css;
        document.head.appendChild(style);

        var overlay = document.createElement('div');
        overlay.className = 'w50-overlay';
        overlay.innerHTML = '<div class="w50-modal" role="dialog" aria-modal="true" aria-labelledby="w50-title">' +
            '<button type="button" class="w50-close" aria-label="Close">&times;</button>' +
            '<div class="w50-content">' + formHtml + '</div></div>';
        document.body.appendChild(overlay);

        var lastFocus = document.activeElement;
        var content = overlay.querySelector('.w50-content');

        function close(reason) {
            if (reason !== 'subscribed') {
                setState({ dismissedAt: Date.now() });
                track('discount_popup_dismiss', { dismiss_method: reason });
            }
            overlay.classList.remove('w50-show');
            document.removeEventListener('keydown', onKey);
            setTimeout(function () { overlay.remove(); }, 300);
            if (lastFocus && lastFocus.focus) lastFocus.focus();
        }

        function onKey(e) {
            if (e.key === 'Escape') close('escape');
        }

        overlay.addEventListener('click', function (e) {
            if (e.target === overlay) close('overlay');
        });
        overlay.querySelector('.w50-close').addEventListener('click', function () { close('close_button'); });
        overlay.querySelector('.w50-skip').addEventListener('click', function () { close('no_thanks'); });
        document.addEventListener('keydown', onKey);

        var form = overlay.querySelector('form');
        var input = form.querySelector('input[type=email]');
        var button = form.querySelector('.w50-submit');
        var error = form.querySelector('.w50-error');

        form.addEventListener('submit', function (e) {
            e.preventDefault();
            var email = input.value.trim();
            if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) {
                error.textContent = 'Please enter a valid email address.';
                input.focus();
                return;
            }
            error.textContent = '';
            button.disabled = true;
            button.textContent = 'Sending…';

            fetch('/api/discount-signup', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email: email, page: location.pathname, website: form.website.value })
            }).then(function (r) {
                return r.json().catch(function () { return {}; }).then(function (data) {
                    if (!r.ok) throw new Error(data.error || 'Something went wrong. Please try again.');
                });
            }).then(function () {
                setState({ subscribed: true });
                track('discount_signup');
                if (typeof _learnq !== 'undefined') {
                    _learnq.push(['identify', { '$email': email }]);
                    _learnq.push(['track', 'Welcome 50 Popup Signup', { 'Page': location.pathname }]);
                }
                content.innerHTML = successHtml;
                var done = content.querySelector('.w50-done');
                done.addEventListener('click', function () { close('subscribed'); });
                done.focus();
            }).catch(function (err) {
                error.textContent = err.message;
                button.disabled = false;
                button.textContent = 'Send My 50% Code';
            });
        });

        requestAnimationFrame(function () {
            overlay.classList.add('w50-show');
            // Don't pop the keyboard open on phones; focus the dialog on desktop only.
            if (window.matchMedia('(min-width: 601px)').matches) input.focus();
        });
        track('discount_popup_view');
    }

    if (!shouldShow()) return;
    setTimeout(open, SHOW_DELAY_MS);
})();
