# Instagram

## Render a carousel
1. Copy `templates/carousel.html` to `<work>/ig/<name>/index.html`. Write 8 `<section class="slide">` blocks, each in a fresh style (see `content.md`).
2. Render the slides with `python render_carousel.py --html <work>/ig/<name>/index.html --name <name> --count 8 --out <pictures>/Instagram`.
   - Each slide renders at `index.html#<n>`. Headless Chrome uses a private profile and `--virtual-time-budget=6000` so web fonts load.
   - To re-render only some slides: `--only 2 3`.
   - A hung render (a heavy WebGL page, for example) is killed after 45 s; render something lighter instead.
3. Look at the PNGs (Read the image) before posting; check for overflow and clipped text.
4. Write `<name>-caption.txt` next to the slides.

## Schedule (web)
1. Click New post in the left rail (use its ref), then **Post**.
2. Call `browser_upload` on the hidden `filechooser (multiple)` with every slide path in order. No native dialog opens.
3. Open the crop button (bottom-left of the preview) and choose **4:5**. Click Next, then Next. Heavy slides (500 KB–1 MB) may need Next clicked twice.
4. Click the caption box, then paste the caption (`python clip.py <name>-caption.txt`).
5. Check the **Share to Facebook** toggle against the owner's wishes. To turn it off, use "Don't share this post", never "Stop sharing all posts".
6. Toggle **Schedule**. Click the date button, pick the day in the calendar, then click the Hours, Minutes and AM/PM spinbuttons and type digits, plus `A` or `P`.
7. Click Schedule and wait for "has been scheduled". "Done" goes to the profile.
8. Coordinates move between dialogs, so take a fresh screenshot before every `click_at`.
9. Escape opens "Discard post?". Click Cancel.
10. Cadence: about 2 a day (morning and evening), 8+ hours apart, scheduled 3–8 days ahead. Track each name, date, time and style in the run-state memory.

## Comments and replies
- **Comment on niche leaders' posts:** add a substantive take, with no links.
- **Reply to commenters:**
  1. Check that the owner hasn't already replied ("View all N replies").
  2. Click the comment's Reply ref; it pre-fills "@user ".
  3. Press End, then Ctrl+V, then click the **Post** button next to the box. Its position varies, so take a screenshot first. Enter also posts, but can land as a top-level @mention.
- **The throttle is silent.** After about 3 replies in a few minutes, Post just does nothing and the text stays in the box. Clear the box, log the reply as pending, and retry after at least an hour. Don't hammer it.
- Comments load lazily. To find someone further down, scroll with the `ref` of the last loaded comment, so the pane scrolls rather than the page.
- If you post a duplicate by mistake, delete it with "..." then Delete.

## Account notes
- A personal account followed by friends and family can be pointed at a niche, but keep the old feed. Never trim its follows without asking.
- The bio and link edits that work only in the app are the owner's to do.
