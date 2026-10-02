// POST /api/discount-signup  { email, page, website }
// Adds the visitor to the SendGrid popup list and emails them the WELCOME50 code.
// Requires the SENDGRID_API_KEY environment variable (set in Vercel, never committed).

const COUPON = 'WELCOME50';
const LIST_ID = '4a04cfdd-edbb-494e-929f-9a0234fe2205'; // "Website Popup - WELCOME50"
const UNSUBSCRIBE_GROUP_ID = 48456; // "Pelvic Floor Pro Marketing"
const FROM = { email: 'shereed@lakecitypt.com', name: 'Sheree DiBiase, PT' };
const SITE = 'https://www.pelvicfloorexercises.com';
const ALLOWED_ORIGINS = [SITE, 'https://pelvicfloorexercises.com'];

// Full-price course pages get a checkout link with the coupon pre-applied.
// Pages whose checkout already uses its own coupon (starter, bundle) fall back to /courses/.
const COURSES = {
    '/constipation-relief-course/': { name: 'Constipation Relief Course', enroll: 'https://sheree-s-site-bb02.thinkific.com/enroll/3654603?price_id=4597690' },
    '/pelvic-wellness-course/': { name: '8-Week Pelvic Wellness Course', enroll: 'https://sheree-s-site-bb02.thinkific.com/enroll/3739521?price_id=4692514' },
    '/pelvic-wellness-masterclass/': { name: '8-Week Pelvic Wellness Course', enroll: 'https://sheree-s-site-bb02.thinkific.com/enroll/3739521?price_id=4692514' },
    '/pelvic-pain-management-class/': { name: 'Pelvic Pain Management Class', enroll: 'https://sheree-s-site-bb02.thinkific.com/enroll/3708123?price_id=4657315' },
    '/stress-urinary-incontinence-class/': { name: 'Stress Urinary Incontinence Class', enroll: 'https://sheree-s-site-bb02.thinkific.com/enroll/3714733?price_id=4664764' }
};

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

function sendgrid(path, method, body) {
    return fetch('https://api.sendgrid.com/v3' + path, {
        method: method,
        headers: {
            'Authorization': 'Bearer ' + process.env.SENDGRID_API_KEY,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(body)
    });
}

function buildEmail(course) {
    var ctaUrl = course ? course.enroll + '&coupon=' + COUPON : SITE + '/courses/';
    var ctaLabel = course ? 'Get 50% Off the ' + course.name : 'Browse the Courses';
    var intro = course
        ? 'Here\'s your code for 50% off the <strong>' + course.name + '</strong>. The button below applies it for you at checkout.'
        : 'Here\'s your code for 50% off any of my online courses. Enter it at checkout, or pick a course below.';

    var html = '<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>' +
        '<body style="margin:0;padding:0;background-color:#F6F9FA;font-family:Arial,Helvetica,sans-serif;">' +
        '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background-color:#F6F9FA;"><tr><td align="center" style="padding:32px 16px;">' +
        '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:560px;background-color:#ffffff;border-radius:16px;overflow:hidden;">' +
        '<tr><td style="background:linear-gradient(135deg,#5AADB5 0%,#7BA4D4 100%);background-color:#5AADB5;padding:28px 40px;text-align:center;">' +
        '<p style="margin:0;font-size:13px;font-weight:700;letter-spacing:2px;color:#ffffff;">YOUR WELCOME GIFT</p></td></tr>' +
        '<tr><td style="padding:36px 40px 8px;">' +
        '<h1 style="margin:0 0 16px;font-family:Georgia,serif;font-size:28px;font-weight:normal;color:#1E2D33;">Welcome! Here\'s 50% off.</h1>' +
        '<p style="margin:0 0 24px;font-size:16px;line-height:1.6;color:#4A5C65;">' + intro + '</p>' +
        '</td></tr>' +
        '<tr><td style="padding:0 40px 28px;" align="center">' +
        '<table role="presentation" cellpadding="0" cellspacing="0" style="border:2px dashed #5AADB5;border-radius:12px;"><tr><td style="padding:16px 36px;text-align:center;">' +
        '<p style="margin:0 0 4px;font-size:12px;letter-spacing:1.5px;color:#8A9BA3;">YOUR CODE</p>' +
        '<p style="margin:0;font-size:30px;font-weight:700;letter-spacing:3px;color:#1E2D33;">' + COUPON + '</p>' +
        '</td></tr></table></td></tr>' +
        '<tr><td style="padding:0 40px 32px;" align="center">' +
        '<table role="presentation" cellpadding="0" cellspacing="0"><tr><td style="background-color:#5AADB5;border-radius:50px;">' +
        '<a href="' + ctaUrl + '" style="display:inline-block;padding:16px 36px;color:#ffffff;font-size:16px;font-weight:700;text-decoration:none;">' + ctaLabel + ' &rarr;</a>' +
        '</td></tr></table>' +
        (course ? '<p style="margin:16px 0 0;font-size:14px;color:#8A9BA3;">Or use it on <a href="' + SITE + '/courses/" style="color:#3D8E96;">any of my courses</a>.</p>' : '') +
        '</td></tr>' +
        '<tr><td style="padding:0 40px 32px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background-color:#F6F9FA;border-radius:12px;"><tr><td style="padding:20px;">' +
        '<p style="margin:0 0 4px;font-size:14px;font-weight:700;color:#1E2D33;">Sheree DiBiase, PT, PRPC, ICLM</p>' +
        '<p style="margin:0;font-size:13px;color:#8A9BA3;line-height:1.5;">Pelvic floor specialist with 40+ years of clinical experience. Founder of Lake City Physical Therapy.</p>' +
        '</td></tr></table></td></tr>' +
        '<tr><td style="background-color:#1A2830;padding:24px 40px;text-align:center;">' +
        '<p style="margin:0 0 8px;font-size:12px;color:#8A9BA3;">Lake City Physical Therapy &bull; Coeur d\'Alene, ID</p>' +
        '<p style="margin:0;font-size:11px;color:#6A7D85;"><a href="<%asm_group_unsubscribe_raw_url%>" style="color:#8DC8CE;text-decoration:underline;">Unsubscribe</a></p>' +
        '</td></tr></table></td></tr></table></body></html>';

    var text = 'Welcome! Here\'s 50% off.\n\n' +
        (course ? 'Your code for 50% off the ' + course.name + ': ' : 'Your code for 50% off any of my online courses: ') + COUPON + '\n\n' +
        ctaLabel + ': ' + ctaUrl + '\n\n' +
        'Sheree DiBiase, PT, PRPC, ICLM\nLake City Physical Therapy, Coeur d\'Alene, ID';

    return { html: html, text: text };
}

module.exports = async function (req, res) {
    if (req.method !== 'POST') {
        res.setHeader('Allow', 'POST');
        return res.status(405).json({ error: 'Method not allowed' });
    }

    var origin = req.headers.origin;
    if (origin && ALLOWED_ORIGINS.indexOf(origin) === -1 && !/\.vercel\.app$/.test(origin)) {
        return res.status(403).json({ error: 'Forbidden' });
    }

    var body = req.body || {};
    if (typeof body === 'string') {
        try { body = JSON.parse(body); } catch (e) { body = {}; }
    }

    // Honeypot: bots fill the hidden "website" field. Pretend success.
    if (body.website) {
        return res.status(200).json({ ok: true });
    }

    var email = String(body.email || '').trim().toLowerCase();
    if (!EMAIL_RE.test(email) || email.length > 254) {
        return res.status(400).json({ error: 'Please enter a valid email address.' });
    }

    if (!process.env.SENDGRID_API_KEY) {
        console.error('SENDGRID_API_KEY is not set');
        return res.status(500).json({ error: 'Something went wrong. Please try again.' });
    }

    var page = typeof body.page === 'string' ? body.page : '';
    var course = COURSES[page] || null;
    var content = buildEmail(course);

    try {
        var send = await sendgrid('/mail/send', 'POST', {
            personalizations: [{ to: [{ email: email }] }],
            from: FROM,
            subject: 'Your 50% off code is inside',
            content: [
                { type: 'text/plain', value: content.text },
                { type: 'text/html', value: content.html }
            ],
            asm: { group_id: UNSUBSCRIBE_GROUP_ID },
            categories: ['welcome50-popup']
        });

        if (!send.ok) {
            console.error('SendGrid mail/send failed', send.status, await send.text());
            return res.status(502).json({ error: 'We couldn\'t send your code. Please try again.' });
        }

        // Saving the contact shouldn't block the visitor if it fails.
        var add = await sendgrid('/marketing/contacts', 'PUT', {
            list_ids: [LIST_ID],
            contacts: [{ email: email }]
        });
        if (!add.ok) {
            console.error('SendGrid marketing/contacts failed', add.status, await add.text());
        }

        return res.status(200).json({ ok: true });
    } catch (err) {
        console.error('discount-signup error', err);
        return res.status(500).json({ error: 'Something went wrong. Please try again.' });
    }
};
