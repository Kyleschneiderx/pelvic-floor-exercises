#!/usr/bin/env python3
"""
Fix SendGrid automation emails by replacing the MailerLite `{$unsubscribe}`
tag with SendGrid's `<%asm_group_unsubscribe_raw_url%>` substitution in
every Dynamic Template referenced by the "Video Nurture Campaign" automation.
"""

import os
import sys
import time
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

API_KEY = os.environ["SENDGRID_API_KEY"]
BASE = "https://api.sendgrid.com/v3"
H = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

AUTOMATION_ID = "cade03ab-d9fd-4c65-8f03-771fb872d858"  # Video Nurture Campaign
OLD_TAG = "{$unsubscribe}"
NEW_TAG = "<%asm_group_unsubscribe_raw_url%>"

EMAILS_DIR = Path(__file__).parent / "mailerlite-emails"
EMAIL_FILES = [
    "email-01-pelvic-floor-exercises-for-women.html",
    "email-02-pelvic-floor-exercises-urinary-incontinence.html",
    "email-03-pelvic-floor-exercises-incontinence-chair-routine.html",
    "email-04-pelvic-floor-exercises-for-prolapse.html",
    "email-05-pelvic-floor-exercises-for-vaginismus.html",
    "email-06-standing-pelvic-floor-exercises-prolapse.html",
    "email-07-pelvic-floor-exercises-pregnancy.html",
    "email-08-pelvic-floor-tight-or-weak.html",
    "email-09-pelvic-floor-exercises-better-than-kegels.html",
    "email-10-lymphedema-after-breast-cancer-surgery.html",
    "email-11-perimenopause-signs.html",
    "email-12-manual-lymph-drainage-technique.html",
    "email-13-exercises-after-breast-surgery.html",
    "email-14-best-labor-positions.html",
    "email-15-hip-rotation-exercises-pelvic-floor.html",
    "email-16-third-trimester-pelvic-floor-exercises.html",
    "email-17-all-fours-position-labor.html",
    "email-18-hip-flexor-stretches-labor-prep.html",
    "email-19-exercise-ball-workout-pregnancy.html",
    "email-20-deep-squat-pregnancy.html",
    "email-21-perimenopause-pelvic-floor-health.html",
    "email-22-labiaplasty-pain-irritation.html",
    "email-23-how-to-apply-vaginal-estrogen-cream.html",
    "email-24-can-pelvic-floor-pt-fix-constipation.html",
    "email-25-can-pelvic-organ-prolapse-cause-constipation.html",
    "email-26-can-pelvic-floor-exercises-cause-constipation.html",
    "email-27-tight-pelvic-floor-constipation.html",
    "email-28-pelvic-floor-exercises-for-beginners-day-1.html",
    "email-29-pelvic-floor-stretches.html",
    "email-30-breast-exams-at-home-ai-screening.html",
    "email-31-midlife-health-sustainable-routine.html",
    "email-32-pelvic-floor-exercises-for-men.html",
]


def get_automation_steps():
    r = requests.get(f"{BASE}/marketing/automations/{AUTOMATION_ID}", headers=H)
    r.raise_for_status()
    return r.json()["steps"]


def get_template(tid):
    r = requests.get(f"{BASE}/templates/{tid}", headers=H)
    r.raise_for_status()
    return r.json()


def patch_version(tid, vid, new_html):
    r = requests.patch(
        f"{BASE}/templates/{tid}/versions/{vid}",
        headers=H,
        json={"html_content": new_html},
    )
    if r.status_code >= 400:
        print(f"    ERROR {r.status_code}: {r.text[:300]}")
        return False
    return True


def active_version(tmpl):
    for v in tmpl.get("versions", []):
        if v.get("active"):
            return v
    return tmpl.get("versions", [None])[0]


def main():
    print("Loading automation steps...")
    steps = get_automation_steps()
    print(f"Found {len(steps)} steps.\n")

    # Build ordered list of templates
    # Step 0 = welcome (use existing template HTML, just swap tag)
    # Steps 1..32 = nurture (use local corrected HTML)
    fixed = 0
    skipped = 0

    for i, step in enumerate(steps):
        msgs = step.get("messages", [])
        if not msgs:
            continue
        msg = msgs[0]
        tid = msg["template_id"]
        subject = msg["subject"]
        print(f"[step {i:02d}] {subject[:55]}")
        print(f"          template={tid}")

        tmpl = get_template(tid)
        v = active_version(tmpl)
        if not v:
            print("          SKIP: no version")
            skipped += 1
            continue

        current_html = v.get("html_content") or ""

        # Determine source HTML
        if i == 0:
            # Welcome email - just swap the tag in place
            if OLD_TAG not in current_html and NEW_TAG in current_html:
                print("          OK: already updated")
                skipped += 1
                continue
            new_html = current_html.replace(OLD_TAG, NEW_TAG)
            # If neither tag present, inject a minimal unsubscribe link before </body>
            if NEW_TAG not in new_html:
                inject = (
                    '<p style="font-size:11px;color:#888;text-align:center;'
                    'margin:24px 0;">'
                    f'<a href="{NEW_TAG}" style="color:#888;">Unsubscribe</a>'
                    "</p>"
                )
                if "</body>" in new_html:
                    new_html = new_html.replace("</body>", inject + "</body>")
                else:
                    new_html = new_html + inject
        else:
            # Nurture email N - load corrected local file
            idx = i - 1
            if idx >= len(EMAIL_FILES):
                print(f"          SKIP: no local file for index {idx}")
                skipped += 1
                continue
            local = EMAILS_DIR / EMAIL_FILES[idx]
            new_html = local.read_text(encoding="utf-8")
            if NEW_TAG not in new_html:
                print(f"          ERROR: local file missing {NEW_TAG}")
                skipped += 1
                continue

        if new_html == current_html:
            print("          OK: no change needed")
            skipped += 1
            continue

        vid = v["id"]
        if patch_version(tid, vid, new_html):
            print(f"          UPDATED version {vid[:8]}")
            fixed += 1
        else:
            skipped += 1

        time.sleep(0.4)

    print(f"\nDone. Fixed: {fixed}  Skipped: {skipped}  Total: {len(steps)}")


if __name__ == "__main__":
    main()
