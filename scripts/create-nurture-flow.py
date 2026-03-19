#!/usr/bin/env python3
"""
Create a 21-email video nurture campaign flow in Klaviyo.
Each email sends 1 day apart, guiding subscribers to a video page.
"""

import os
import requests
import json
import time
import sys

API_KEY = os.environ.get("KLAVIYO_API_KEY", "")
REVISION = "2025-01-15"
BASE_URL = "https://a.klaviyo.com/api"
SITE_URL = "https://pelvicfloorexercises.com"

HEADERS = {
    "Authorization": f"Klaviyo-API-Key {API_KEY}",
    "revision": REVISION,
    "accept": "application/json",
    "content-type": "application/json"
}

# From the existing flow
FROM_EMAIL = "shereed@lakecitypt.com"
FROM_LABEL = "Sheree Dibiase PT, PRPC"

# All 21 videos in campaign order
VIDEOS = [
    {
        "slug": "pelvic-floor-exercises-for-women",
        "video_id": "uYsabfqM-9w",
        "title": "Top 5 Pelvic Floor Exercises for Women",
        "subject": "Your first pelvic floor exercise video is ready",
        "preview": "Learn the top 5 exercises from a 40-year specialist",
        "description": "Start your pelvic floor journey with the top 5 exercises every woman should know. Sheree DiBiase, PT, walks you through each movement step by step."
    },
    {
        "slug": "pelvic-floor-exercises-urinary-incontinence",
        "video_id": "Tv0-KM_V8Qk",
        "title": "Top 5 Pelvic Floor Exercises for Urinary Incontinence Relief",
        "subject": "Exercises specifically for incontinence relief",
        "preview": "These 5 exercises target urinary incontinence directly",
        "description": "If you experience any form of urinary leakage, these 5 targeted exercises can help. Learn the techniques that address stress, urge, and mixed incontinence."
    },
    {
        "slug": "pelvic-floor-exercises-incontinence-chair-routine",
        "video_id": "eO0fQHiQH1Q",
        "title": "Pelvic Floor Exercises for Incontinence: 10-Min Chair Routine",
        "subject": "A 10-minute chair routine you can do anywhere",
        "preview": "No gym needed — just a chair and 10 minutes",
        "description": "This seated routine is perfect for the office, at home, or anywhere you have a chair. It's gentle, effective, and takes just 10 minutes."
    },
    {
        "slug": "pelvic-floor-exercises-for-prolapse",
        "video_id": "0fsUk656uqs",
        "title": "Top Pelvic Floor Exercises for Prolapse",
        "subject": "Safe pelvic floor exercises for prolapse",
        "preview": "Expert-guided exercises specifically for prolapse management",
        "description": "Pelvic organ prolapse affects many women, and the right exercises can make a significant difference. Learn which exercises are safe and which to avoid."
    },
    {
        "slug": "pelvic-floor-exercises-for-vaginismus",
        "video_id": "-ajvkXCR3oY",
        "title": "Pelvic Floor Exercises for Vaginismus",
        "subject": "Gentle exercises for vaginismus relief",
        "preview": "Relaxation-focused techniques for pelvic floor tension",
        "description": "Vaginismus requires a different approach — relaxation rather than strengthening. Learn gentle exercises that help your pelvic floor release tension."
    },
    {
        "slug": "standing-pelvic-floor-exercises-prolapse",
        "video_id": "V0stR30sql4",
        "title": "Standing Pelvic Floor Exercises for Prolapse Relief",
        "subject": "Standing exercises for prolapse relief",
        "preview": "Train your pelvic floor against gravity for real-world strength",
        "description": "Standing exercises challenge your pelvic floor against gravity — the way it needs to work in real life. These functional exercises build practical strength."
    },
    {
        "slug": "pelvic-floor-exercises-pregnancy",
        "video_id": "epNBTbigugc",
        "title": "Pelvic Floor Exercises for Pregnant Women",
        "subject": "Safe pelvic floor exercises during pregnancy",
        "preview": "Prepare your body for labor with these safe exercises",
        "description": "Pregnancy is one of the most important times to care for your pelvic floor. These exercises are safe for each trimester and help prepare you for labor."
    },
    {
        "slug": "pelvic-floor-tight-or-weak",
        "video_id": "8ghjha-7uJc",
        "title": "Is Your Pelvic Floor Too Tight or Too Weak?",
        "subject": "Is your pelvic floor too tight or too weak?",
        "preview": "Find out — the answer changes everything about your exercise plan",
        "description": "Many women do the wrong exercises because they don't know if their pelvic floor is too tight or too weak. This video helps you figure out which one you are."
    },
    {
        "slug": "pelvic-floor-exercises-better-than-kegels",
        "video_id": "0SmfjnisWjI",
        "title": "Pelvic Floor Exercises BETTER Than Kegels",
        "subject": "These exercises work better than Kegels",
        "preview": "Why Kegels alone aren't enough — and what to do instead",
        "description": "Kegels are just one piece of the puzzle. Learn the exercises that go beyond basic Kegels to build a truly strong, functional pelvic floor."
    },
    {
        "slug": "lymphedema-after-breast-cancer-surgery",
        "video_id": "CBEPu8Vt-mM",
        "title": "Lymphedema After Breast Cancer Surgery",
        "subject": "Managing lymphedema after breast cancer surgery",
        "preview": "Essential exercises and strategies for lymphedema prevention",
        "description": "Lymphedema is a common concern after breast cancer surgery. Learn the exercises and self-care techniques that can help reduce your risk."
    },
    {
        "slug": "perimenopause-signs",
        "video_id": "CKdsCEzy6L0",
        "title": "How Do I Know If I'm in Perimenopause?",
        "subject": "How to know if you're in perimenopause",
        "preview": "Recognize the signs and learn what you can do about them",
        "description": "Perimenopause often begins earlier than women expect. Learn the common signs and symptoms, and what you can do to manage them effectively."
    },
    {
        "slug": "manual-lymph-drainage-technique",
        "video_id": "IOm9ZfVKbQ4",
        "title": "Manual Lymph Drainage: Essential Technique",
        "subject": "Learn the manual lymph drainage technique",
        "preview": "A hands-on technique you can do at home",
        "description": "Manual lymph drainage is a gentle, effective technique for managing swelling. Watch this step-by-step guide to learn the proper method."
    },
    {
        "slug": "exercises-after-breast-surgery",
        "video_id": "HfSS1waukjw",
        "title": "Easy Gentle Exercises After Breast Surgery",
        "subject": "Gentle recovery exercises after breast surgery",
        "preview": "Safe, easy exercises to support your healing",
        "description": "Recovery after breast surgery requires gentle, progressive movement. These exercises are designed to be safe and supportive during each stage of healing."
    },
    {
        "slug": "best-labor-positions",
        "video_id": "Dj8fSL_dLCQ",
        "title": "Best Labor Positions for Each Stage of Birth",
        "subject": "The best positions for each stage of labor",
        "preview": "Positions that work with gravity and your body's natural movement",
        "description": "The position you use during labor can significantly affect your comfort and progress. Learn the best positions for early labor, active labor, and pushing."
    },
    {
        "slug": "hip-rotation-exercises-pelvic-floor",
        "video_id": "C3ID4g8BvB4",
        "title": "Hip Rotation Exercises for Pelvic Floor Strength",
        "subject": "Hip exercises that strengthen your pelvic floor",
        "preview": "The hidden connection between hip rotators and pelvic health",
        "description": "Your hip rotators are directly connected to your pelvic floor through the obturator internus muscle. These exercises strengthen both at once."
    },
    {
        "slug": "third-trimester-pelvic-floor-exercises",
        "video_id": "tanAnZCVGIo",
        "title": "Third Trimester Pelvic Floor Exercises",
        "subject": "Third trimester exercises to prepare for birth",
        "preview": "Get your pelvic floor ready for labor and delivery",
        "description": "The third trimester is a critical time to prepare your pelvic floor. These exercises focus on both strength and relaxation — both essential for birth."
    },
    {
        "slug": "all-fours-position-labor",
        "video_id": "KhzBzMKUKPU",
        "title": "All Fours Position for Labor & Delivery",
        "subject": "Why the all-fours position is powerful for labor",
        "preview": "This position opens your pelvis and relieves back pressure",
        "description": "The all-fours position is one of the most effective positions for labor. Learn why it works and how to use it during different stages of delivery."
    },
    {
        "slug": "hip-flexor-stretches-labor-prep",
        "video_id": "POz6Kb046ms",
        "title": "Hip Flexor Stretches for Labor Prep",
        "subject": "Hip flexor stretches to prepare for labor",
        "preview": "Tight hip flexors can limit your pushing positions",
        "description": "Tight hip flexors can restrict your pelvis during labor. These stretches open up the hip flexors and prepare your body for more comfortable birthing positions."
    },
    {
        "slug": "exercise-ball-workout-pregnancy",
        "video_id": "3n_Xk13bB00",
        "title": "Exercise Ball Workout for Pregnancy",
        "subject": "Exercise ball workout designed for pregnancy",
        "preview": "Safe, effective exercises using your birth ball",
        "description": "The exercise ball is one of the best tools for pregnancy fitness. Learn safe exercises that strengthen your core, open your pelvis, and prepare you for labor."
    },
    {
        "slug": "deep-squat-pregnancy",
        "video_id": "qLQeOIdSQW4",
        "title": "Deep Squat for Pregnancy",
        "subject": "The deep squat — your best labor preparation exercise",
        "preview": "This single exercise opens your pelvis by up to 30%",
        "description": "The deep squat opens your pelvis by up to 28-30%, strengthens your legs, and lengthens your pelvic floor. Learn the safe way to practice this powerful exercise."
    },
    {
        "slug": "perimenopause-pelvic-floor-health",
        "video_id": "XuJKDaqsj2k",
        "title": "Perimenopause & Pelvic Floor Health",
        "subject": "How perimenopause affects your pelvic floor",
        "preview": "Understanding hormonal changes and what to do about them",
        "description": "Declining estrogen during perimenopause directly affects your pelvic floor muscles and tissues. Learn what's happening and the exercises that help."
    },
]


def build_email_html(video):
    """Build a clean, branded email HTML template for a video."""
    thumbnail = f"https://img.youtube.com/vi/{video['video_id']}/maxresdefault.jpg"
    page_url = f"{SITE_URL}/{video['slug']}/"
    # Use Klaviyo template variable for email personalization
    tracking_url = f"{page_url}?email={{{{ email }}}}"

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{video['title']}</title>
</head>
<body style="margin:0;padding:0;background-color:#F6F9FA;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;">

<!-- Preheader -->
<div style="display:none;max-height:0;overflow:hidden;mso-hide:all;">
    {video['preview']}
</div>

<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background-color:#F6F9FA;">
<tr><td align="center" style="padding:40px 20px;">

<!-- Main Container -->
<table role="presentation" width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%;background-color:#ffffff;border-radius:16px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.06);">

    <!-- Header -->
    <tr>
        <td style="background:linear-gradient(135deg,#1A2830 0%,#243640 100%);padding:32px 40px;text-align:center;">
            <p style="margin:0;color:#8DC8CE;font-size:13px;font-weight:600;letter-spacing:1.5px;text-transform:uppercase;">Pelvic Floor Exercises</p>
        </td>
    </tr>

    <!-- Video Thumbnail -->
    <tr>
        <td style="padding:0;">
            <a href="{tracking_url}" style="display:block;position:relative;">
                <img src="{thumbnail}" alt="{video['title']}" width="600" style="display:block;width:100%;height:auto;border:0;">
            </a>
        </td>
    </tr>

    <!-- Content -->
    <tr>
        <td style="padding:32px 40px;">
            <h1 style="margin:0 0 16px;font-size:24px;line-height:1.3;color:#1E2D33;font-weight:700;">
                {video['title']}
            </h1>
            <p style="margin:0 0 24px;font-size:16px;line-height:1.6;color:#4A5C65;">
                {video['description']}
            </p>

            <!-- CTA Button -->
            <table role="presentation" cellpadding="0" cellspacing="0" style="margin:0 auto;">
            <tr>
                <td style="background:linear-gradient(135deg,#5AADB5 0%,#7BA4D4 100%);border-radius:50px;text-align:center;">
                    <a href="{tracking_url}" style="display:inline-block;padding:16px 40px;color:#ffffff;font-size:16px;font-weight:700;text-decoration:none;letter-spacing:0.3px;">
                        Watch the Video Guide &rarr;
                    </a>
                </td>
            </tr>
            </table>
        </td>
    </tr>

    <!-- Instructor -->
    <tr>
        <td style="padding:0 40px 32px;">
            <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background-color:#F6F9FA;border-radius:12px;padding:20px;">
            <tr>
                <td style="padding:20px;">
                    <p style="margin:0 0 4px;font-size:14px;font-weight:700;color:#1E2D33;">Sheree DiBiase, PT, PRPC, ICLM</p>
                    <p style="margin:0;font-size:13px;color:#8A9BA3;line-height:1.5;">Pelvic floor specialist with 40+ years of clinical experience. Founder of Lake City Physical Therapy.</p>
                </td>
            </tr>
            </table>
        </td>
    </tr>

    <!-- Footer -->
    <tr>
        <td style="background-color:#1A2830;padding:24px 40px;text-align:center;">
            <p style="margin:0 0 8px;font-size:12px;color:#8A9BA3;">
                Lake City Physical Therapy &bull; Coeur d'Alene, ID
            </p>
            <p style="margin:0;font-size:11px;color:#6A7D85;">
                <a href="{{% unsubscribe %}}" style="color:#8DC8CE;text-decoration:underline;">Unsubscribe</a>
                &nbsp;&bull;&nbsp;
                <a href="{{% manage_preferences %}}" style="color:#8DC8CE;text-decoration:underline;">Manage Preferences</a>
            </p>
        </td>
    </tr>

</table>
<!-- End Main Container -->

</td></tr>
</table>
</body>
</html>"""


def create_template(video, index):
    """Create an email template in Klaviyo and return its ID."""
    name = f"Video Nurture #{index + 1}: {video['title']}"
    html = build_email_html(video)

    payload = {
        "data": {
            "type": "template",
            "attributes": {
                "name": name,
                "editor_type": "CODE",
                "html": html
            }
        }
    }

    resp = requests.post(f"{BASE_URL}/templates/", headers=HEADERS, json=payload)
    if resp.status_code == 201:
        template_id = resp.json()["data"]["id"]
        print(f"  [OK] Template #{index + 1}: {template_id} — {video['title']}")
        return template_id
    else:
        print(f"  [ERROR] Template #{index + 1}: {resp.status_code} — {resp.text}")
        return None


def create_list(name):
    """Create a new list in Klaviyo."""
    payload = {
        "data": {
            "type": "list",
            "attributes": {
                "name": name
            }
        }
    }
    resp = requests.post(f"{BASE_URL}/lists/", headers=HEADERS, json=payload)
    if resp.status_code == 201:
        list_id = resp.json()["data"]["id"]
        print(f"  [OK] List created: {list_id} — {name}")
        return list_id
    else:
        print(f"  [ERROR] List: {resp.status_code} — {resp.text}")
        return None


def build_flow_definition(list_id, template_ids):
    """Build the complete flow definition JSON."""
    actions = []
    action_counter = 1

    for i, (video, template_id) in enumerate(zip(VIDEOS, template_ids)):
        # Add 1-day time delay before each email (except the first)
        if i > 0:
            delay_temp_id = f"delay_{i}"
            delay_action = {
                "temporary_id": delay_temp_id,
                "type": "time-delay",
                "data": {
                    "value": 1,
                    "unit": "days"
                },
                "links": {
                    "next": f"email_{i}"
                }
            }
            actions.append(delay_action)

        # Add email action
        email_temp_id = f"email_{i}"
        email_action = {
            "temporary_id": email_temp_id,
            "type": "send-email",
            "data": {
                "message": {
                    "from_email": FROM_EMAIL,
                    "from_label": FROM_LABEL,
                    "reply_to_email": None,
                    "cc_email": None,
                    "bcc_email": None,
                    "subject_line": video["subject"],
                    "preview_text": video["preview"],
                    "template_id": template_id,
                    "smart_sending_enabled": True,
                    "transactional": False,
                    "add_tracking_params": True,
                    "custom_tracking_params": None,
                    "additional_filters": None,
                    "name": f"Email #{i + 1} — {video['title']}"
                },
                "status": "draft"
            },
            "links": {
                # Point to next delay, or null for the last email
                "next": f"delay_{i + 1}" if i < len(VIDEOS) - 1 else None
            }
        }
        actions.append(email_action)

    definition = {
        "triggers": [
            {
                "type": "list",
                "id": list_id
            }
        ],
        "profile_filter": None,
        "actions": actions,
        "entry_action_id": "email_0"
    }

    return definition


def create_flow(list_id, template_ids):
    """Create the complete flow in Klaviyo."""
    definition = build_flow_definition(list_id, template_ids)

    payload = {
        "data": {
            "type": "flow",
            "attributes": {
                "name": "Video Nurture Campaign",
                "definition": definition
            }
        }
    }

    resp = requests.post(f"{BASE_URL}/flows/", headers=HEADERS, json=payload)
    if resp.status_code == 201:
        flow_id = resp.json()["data"]["id"]
        print(f"\n  [OK] Flow created: {flow_id}")
        return flow_id
    else:
        print(f"\n  [ERROR] Flow: {resp.status_code}")
        print(json.dumps(resp.json(), indent=2))
        return None


def main():
    print("=" * 60)
    print("KLAVIYO VIDEO NURTURE CAMPAIGN BUILDER")
    print("=" * 60)

    # Step 1: Create dedicated list
    print("\n1. Creating nurture campaign list...")
    list_id = create_list("Video Nurture Campaign")
    if not list_id:
        sys.exit(1)

    # Step 2: Create all 21 email templates
    print(f"\n2. Creating {len(VIDEOS)} email templates...")
    template_ids = []
    for i, video in enumerate(VIDEOS):
        template_id = create_template(video, i)
        if not template_id:
            print(f"   Failed at template #{i + 1}. Stopping.")
            sys.exit(1)
        template_ids.append(template_id)
        # Small delay to stay within rate limits
        time.sleep(0.2)

    print(f"\n   All {len(template_ids)} templates created.")

    # Step 3: Create the flow
    print("\n3. Creating nurture flow...")
    flow_id = create_flow(list_id, template_ids)
    if not flow_id:
        sys.exit(1)

    print("\n" + "=" * 60)
    print("DONE!")
    print(f"  Flow ID: {flow_id}")
    print(f"  List ID: {list_id}")
    print(f"  Templates: {len(template_ids)}")
    print(f"  Emails: 21 (1-day delay between each)")
    print(f"  Status: DRAFT (set to live in Klaviyo UI)")
    print("=" * 60)


if __name__ == "__main__":
    main()
